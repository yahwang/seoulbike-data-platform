import pendulum
import requests
import json
import os
from datetime import datetime
import psycopg2
import io

def msg_to_slack(msg):
    webhook_url = os.environ['webhook_url']
    data = {
        'text':'TASK FAILED! REASON : ' + msg,
        'username': 'FROM AWS LAMBDA',
        'channel': 'seoulbike-lambda',
        'icon_emoji': ':robot_face:'
        }
    response = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

def extract_content_id(st_data): 
    if '.' in st_data['stationName']:
        st_data['stationName'] = st_data['stationName'].split('.')[0]
    else:
        st_data['stationName'] = '0'
    return st_data

def lambda_handler(event, context):
    auth_key = os.environ['auth_key']
    local_tz = pendulum.timezone("Asia/Seoul")
    
    # GET API
    response1 = requests.get(f'http://openapi.seoul.go.kr:8088/{auth_key}/json/bikeList/1/1000')
    response2 = requests.get(f'http://openapi.seoul.go.kr:8088/{auth_key}/json/bikeList/1001/2000')
    file_date = datetime.now(tz=local_tz)
    
    # MAKE DATA AVALIABLE TO INSERT TO DB 
    if response1.status_code==200 and response2.status_code==200:
        try:
            rent_api = response1.json()['rentBikeStatus']['row'] + response2.json()['rentBikeStatus']['row']
            data = [ dict( list(station.items())[:3] ) for station in rent_api ]
            data = [ extract_content_id(i) for i in list(data) ]
            rows = [ [st_data['stationName'], st_data['rackTotCnt'],st_data['parkingBikeTotCnt'], str(file_date)] for st_data in data ]
        except:
            raise LambdaError('API DATA IS WRONG')
        
    # INSERT DATA TO POSTGRES DB
        try:
            conn = psycopg2.connect(database="seoulbike",
                                   host=os.environ['db_host'], 
                                   user=os.environ['db_user'],
                                   password=os.environ['db_pw'],
                                   connect_timeout=1)
    
            cursor = conn.cursor()
            # USING StringIO AND copy_from(COPY command) FOR PERFORMANCE
            csv_file_like_object = io.StringIO()
            for row in rows:
                csv_file_like_object.write(','.join(row) + '\n')
            csv_file_like_object.seek(0)
            cursor.copy_from(csv_file_like_object, 'bike_realtime_log_tz', sep=',', columns=['st_id','st_cradle','st_parking','log_time'])
            
            conn.commit()
            csv_file_like_object.close()
            conn.close()
            
            return { 'statusCode': 200, 'body': json.dumps('Insert Complete') }
        
        except:
            raise LambdaError('DB UPLOAD FAILED!!')

    else:
        raise LambdaError('GET API FAILED')

class LambdaError(Exception):
 
    def __init__(self, msg):
        super().__init__(msg)
        msg_to_slack(msg)
        