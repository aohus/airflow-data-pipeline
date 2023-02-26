# programmers-study-pipeline

programmers 스터디(실리콘밸리에서 날아온 데이터 엔지니어링 스타터 키트 with Python)에서 공부한 내용을 정리한 repository 입니다.

1. 제공된 EC2 server에 airflow를 설치
2. airflow를 통한 ETL process 구현
   1. weather to redshift
   - task1: get daily temperature info through open weather api
   - task2: redshift table format에 맞춰 transform
   - task3-1: save data to redshift (full refresh)
   - task3-2: save data to redshift (incremental update)
   2. mysql to redshift
   - task1: clean up s3 bucket
   - task2-1: mysql to s3 (full refresh)
   - task2-2: mysql to s3 (daily incremental update)
   - task3: s3 to redshift
   3. namegendercsv to redshift
   - task1: download csv file through download api
   - task2: remove header
   - task3: save data to redshift
