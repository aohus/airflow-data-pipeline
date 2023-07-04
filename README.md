# programmers-study-pipeline

programmers 스터디(실리콘밸리에서 날아온 데이터 엔지니어링 스타터 키트 with Python)에서 실습한 내용을 정리한 repository 입니다.

## Environments

- AWS 이용
  - worflow management platform : EC2 server에 airflow 설치
  - datastore : S3, redshift, mysql

# dags

1.  weather to redshift

    - get daily temperature info from open weather api and save data to redshift
    - using xcom_pull
    - try two ways to save to redshift : full refresh / incremental update

2.  mysql to redshift

    - mysql -> s3 -> redshift
    - try two ways to save to redshift : full refresh / clean up s3 bucket & daily incremental update

3.  namegendercsv to redshift

    - download csv file through download api and save data to redshift
    - using xcom_pull

# docs

1. [SQL for dataengineer](docs/SQL_for_dataengineer.md)
2. [transaction](docs/transaction.md)
3. [airflow](docs/airflow.md)
4. [Redshift](docs/Redshift.md)
5. [full refresh & incremental update](docs/full_refresh_and_incremental_update.md)
