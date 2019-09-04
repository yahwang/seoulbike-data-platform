import pendulum
import requests
import json
import os
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

def extract_content_id(st_data): 
    if '.' in st_data['stationName']:
        st_data['stationName'] = st_data['stationName'].split('.')[0]
    else:
        st_data['stationName'] = 0
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
        rent_api = response1.json()['rentBikeStatus']['row'] + response2.json()['rentBikeStatus']['row']
        data = [ dict( list(station.items())[:3] ) for station in rent_api ]
        data = [extract_content_id(i) for i in list(data)]
        rows = [ [st_data['stationName'], st_data['rackTotCnt'],st_data['parkingBikeTotCnt'], file_date] for st_data in data ]
        
        
    # INSERT DATA TO POSTGRES DB
        conn = psycopg2.connect(database="seoulbike",
                               host=os.environ['db_host'], 
                               user=os.environ['db_user'],
                               password=os.environ['db_pw'])

        cursor = conn.cursor(cursor_factory = RealDictCursor)
        query = "INSERT INTO bike_realtime_log_tz(st_id, st_cradle, st_parking, log_time) values (%s, %s, %s, %s);"
        cursor.executemany(query, rows)
        conn.commit()
        conn.close()
        
        return { 'statusCode': 200, 'body': json.dumps('Insert Complete') }
    else:
        webhook_url = os.environ['webhook_url']
        data = {
            'text':'TASK FAILED!',
            'username': 'FROM AWS LAMBDA',
            'channel': 'seoulbike-lambda',
            'icon_emoji': ':robot_face:'
            }
        response = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        raise Exception('GET API FAILED')