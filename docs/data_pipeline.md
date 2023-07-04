# Spark/Athena 내용 시나리오

- 비구조화된 데이터 처리하기
- 비구조화된 데이터를 비싼 RedShift에 올려도 별로 할 수 있는 것이 없다.
- 싼 스토리지인 S3에 저장 후 Spark&ATHENA를 통해 processing하여 S3 or Redshift로 저장하는 것이 일반적인 사용방법이다.

# 데이터 파이프라인이란

- ETL : Extract, Transform, Load
- Data Pipeline, ETL, Data Workflow, DAG
  - ETL
  - Called DAG in Airflow
- ETL vs ELT
  - ETL: 데이터
- Data Lake
  - (사실 비슷하다.) 스케일이 큰 느낌, 비정형데이터를 포함하는 느낌,
  - 데이터레이크와 데이터 웨어하우스를 따로 쓰는 경우
    - 로그 -> 데이터레이크 -> transform -> 데이터웨어하우스/데이터마트 구조를 생각한다.
  - Structured Data + Unstructured Data in various formats
  - More like a historical data storage (no retention policy)
  - Order of magnitude bigger than Data Warehouse in terms of size
- Data Warehouse
  - Focusing more on refined and structured data with some retention policy
  - Usually BI tools (Looker, Tableau, Superset, ...) connect with Data Warehouse

### Data Pipeline의 정의

- 데이터를 소스로부터 목적지로 복사하는 작업
  - 코딩(파이썬 or 스칼라) 혹은 SQL 을 통해 이루어짐
  - 대부분의 목적지는 데이터 웨어하우스
- 데이터 소스의 예:
  - click stream, call data, ads performance data, transactions, sensor data
  - 구체적인 examples: production databases, log files, API, stream data(kafka)

Data Pipeline의 종류1

- raw data ETL jobs
  1.  외부와 내부 데이터 소스에서 데이터를 읽어다가(많은 경우 API 를통함)
  2.  적당한 데이터 포맷 변환 후(데이터 크기가 커지면 Spark 등이 필요해짐)
  3.  데이터 웨어하우스 로드

Data Pipeline의 종류2

- Summary/Report jobs 1) DW(or DL)로부터 데이터를 읽어 다시 DW에 쓰는 ETL 2) Raw data를 읽어서 일종의 리포트 형태나 서머리 형태의 테이블을 다시 만드는 용도 3) 특수한 형태로는 AB테스트 결과를 분석하는 데이터 파이프라인도 존재
  요약 테이블은 SQL만으로 만들고 분석가가 하는 것이 맞음. 이를 어떻게 편하게 할 수 있을지는 데이터 엔지니어들의 문제. ex)DBT 사용

Data Pipeline의 종류3

- production data jobs
  1.  DW로부터 데이터를 읽어 다른 storage로 쓰는 ETL
      a. 써머리 정보가 프로덕션 환경에서 성능 이유로 필요한 경우
      b. 혹은 머신러닝 모델에서 필요한 피쳐들을 미리 계산해두는 경우
  2.  흔한 타겟 스토리지
      a. Cassandra/HBase/DynamoDB 와 같은 NoSQL
      b. MySQL 등 RDB(OLTP)
      c. Redis/Memcache 같은 캐시
      d. ElasticSearch와 같은 검색엔진

next, 간단한 ETL 작성해봄

# AIRFLOW

구성

- 총 5개의 컴포넌트로 구성
  - Web Server
  - Scheduler
  - Worker
  - Database
  - Queue

### airflow productionizing

- airflow.cfg
  - any changes here will be reflected when you restart the webserver and scheduler
- airflow 같은 툴은 vpn 뒤에 설치하는 것이 좋다.
- airflow disck volumn이 부족해서 무제가 생기는 경우가 있다.
  - 주기적으로 로그 파일을 삭제해주어야한다.
  - 1.  로그가 많이 쌓이는 경우 -> /dev/airflow/logs in (Core section of airflow.cfg)
  - 2.  data 보낼 때, local data로 다운 받았다가 s3로 보내는 경우.
- airflow 서버 자체도 모니터링을 따로 해야한다. 로그 파일 때문에 디스크 용량 문제생겨서 안돌고 하면 스스로 문제를 보고하지 못한다.
- api open -> health check!

### Dag Dependencies

- explicit trigger : 끝나면 다음 dag 호출
  - TriggerDagOperator
- reactive trigger : 어떤 일이 일어났는지 주기적으로 확인하여, 일어났다면 실행
  - ExternalTaskSensor
