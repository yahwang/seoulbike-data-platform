from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pendulum
import requests
import json
import os
from utils.slack_alert import SlackAlert
from airflow.hooks.S3_hook import S3Hook
from airflow.hooks.postgres_hook import PostgresHook


def extract_content_id(st_data): 
    if '.' in st_data['stationName']:
        st_data['stationName'] = st_data['stationName'].split('.')[0]
    else:
        st_data['stationName'] = 0
    return st_data

def get_data_from_api(*args, **kwargs):
    auth_key = '6f5....'
    response1 = requests.get(f'http://openapi.seoul.go.kr:8088/{auth_key}/json/bikeList/1/1000')
    response2 = requests.get(f'http://openapi.seoul.go.kr:8088/{auth_key}/json/bikeList/1001/2000')
    file_date = datetime.now(tz=local_tz)

    if response1.status_code==200 and response2.status_code==200:
        rent_api = response1.json()['rentBikeStatus']['row'] + response2.json()['rentBikeStatus']['row']
        res = [ dict( list(station.items())[:3] ) for station in rent_api ]
        return file_date, res
    else:
        raise ValueError('GET API DATA FAILED')

def upload_string_to_S3(*args, **kwargs):
    ti = kwargs['ti']
    file_date, data = ti.xcom_pull(task_ids="get_data_from_api")
    file_date = file_date.strftime("%Y%m%d-%H%M%S")
    hook = S3Hook('S3_conn')
    key = f'bike-api-{file_date}.json'
    hook.load_string(json.dumps(data), key, kwargs['bucket_name'])

def save_to_local(*args, **kwargs):
    ti = kwargs['ti']
    file_date, data = ti.xcom_pull(task_ids="get_data_from_api")
    file_date = file_date.strftime("%Y%m%d-%H%M%S")
    filename = f'bike-api-{file_date}.json'
    dirname = "/usr/local/airflow/bike_data/"
    with open(os.path.join(dirname,filename),'w') as output:
        json.dump(data, output)

def upload_to_postgres(*args, **kwargs):
    ti = kwargs['ti']
    file_date, data = ti.xcom_pull(task_ids="get_data_from_api")
    file_date = file_date.strftime("%Y-%m-%d %H:%M:%S%z")
    data = [extract_content_id(i) for i in list(data)]
    # DbApiHook.insert_rows
    pg_hook = PostgresHook(postgres_conn_id='postgres_conn', schema='seoulbike')    
    rows = [ [st_data['stationName'], st_data['rackTotCnt'],st_data['parkingBikeTotCnt'], file_date] for st_data in data ]
    pg_hook.insert_rows(table='bike_realtime_log_tz', rows=rows) # autocommit
    pg_hook.get_conn().close()

alert = SlackAlert('#airflow')
local_tz = pendulum.timezone("Asia/Seoul")

default_args = {
    "owner": "yahwang",
    "depends_on_past": False,
    "start_date": datetime(2019, 6, 21, tzinfo=local_tz),
    "retries": 1,
    "retry_delay": timedelta(seconds=1),
    "provide_context": True,
    "on_failure_callback": alert.slack_fail_alert
}

dag = DAG("api_to_save", 
            description="Send bike data to S3", 
            catchup=False,
            default_args=default_args, 
            schedule_interval='@once'
        )

get_data_task = PythonOperator(task_id="get_data_from_api", 
        python_callable=get_data_from_api,
        dag=dag
        )

save_to_local_task = PythonOperator(task_id="save_to_local", 
        python_callable=save_to_local,
        dag=dag
        )

upload_to_postgres_task = PythonOperator(task_id="upload_to_postgres", 
        python_callable=upload_to_postgres,
        dag=dag
        )

'''
upload_to_S3_task = PythonOperator(
    task_id='upload_to_S3',
    python_callable=upload_string_to_S3,
    op_kwargs={
        'bucket_name': 'seoul-bike-data',
    },
    dag=dag)
'''

get_data_task >> save_to_local_task
get_data_task >> upload_to_postgres_task