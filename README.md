# seoulbike-data-platform

서울 자전거 따릉이 데이터 플랫폼 구축

## Description

Dashboard : 실시간 대여소 잔여 자전거 대수 ( 현재는 1분 단위로 구성 )

Stations Info : 대여소 정보

## Structure

> Version 1

<img src="./imgs/structure.png" alt="png">

> Version 2

<img src="./imgs/structure_v2.png" alt="png2">

> Database

<img src="./imgs/db_structure.png" alt="png3">

#### INDEX

``` sql
CREATE INDEX idx_bike_id ON bike_realtime_log_tz(st_id)
CREATE INDEX idx_realtime ON bike_realtime_log_tz(log_time)
CREATE INDEX idx_id_realtime ON bike_realtime_log_tz(st_id, log_time)
```

## Requirements

> 따릉이 자전거 데이터

API 제공 URL : http://data.seoul.go.kr/dataList/datasetView.do?infId=OA-15493&srvType=A&serviceKind=1

[데이터 관련 정리](https://github.com/yahwang/seoulbike-data-platform/tree/master/Data_API)

> Web Page

    python == 3.6.8

    Django == 2.2.2
    django-bootstrap-form==3.4
    django-environ==0.4.5
    django-extensions==2.1.9
    django-filter==2.1.0
    django-rest-swagger==2.2.0
    django-tables2==2.0.6
    djangorestframework==3.9.4

> airflow 1.10.3 For Version 1

Using Custom Docker

https://github.com/yahwang/docker-airflow

[DAG 파일](https://github.com/yahwang/seoulbike-data-platform/tree/master/dags/api_to_save.py)

<img src="./imgs/airflow_dag.jpg" alt="dag">

> superset 0.28.1

Using Custom Docker

https://github.com/yahwang/docker-superset

## Preview

> Dashboard

<img src="./imgs/dashboard.gif" alt="dashboard">

> Filter

<img src="./imgs/filter.gif" alt="filter">

## Stations Info CRUD

> RETRIEVE & FILTER

<img src="./imgs/screen_1.jpg" alt="sc1">

> CREATE & UPDATE

<img src="./imgs/screen_2.jpg" alt="sc2">



