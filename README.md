# data pipeline with Apache Airflow 
모든 dags 폴더에는 같은 일을 하는 dag가 version1, 2로 나뉘어 작성되어있습니다. version2는 xcom_pull, incremental update, transaction, plugins로 airflow 기능과 코드 책임 분리를 적용한 내용입니다.

## Environments
- AWS 이용
  - worflow management platform : EC2 server에 airflow 설치
  - datastore : S3, redshift, mysql

# dags

1.  weather to redshift

    - get daily temperature info from open weather api and save data to redshift
    - using xcom_pull
    - try two ways to save to redshift
      - full refresh
      - incremental update(how to, detail)
        - Create a temporary table.
        - Copy data from the original table to the temporary table.
        - Insert new data obtained from an API into the temporary table.
        - Delete data from the original table.
        - Use the ROW_NUMBER function in the temporary table to eliminate duplicates.
        - Copy the deduplicated data from the temporary table back to the original table.
    - make custom operator : S3ToRedshiftOperator

2.  mysql to redshift

    - mysql -> s3 -> redshift
    - try two ways to save to redshift
      - full refresh
      - clean up s3 bucket & daily incremental update

3.  namegendercsv to redshift

    - download csv file through download api and save data to redshift
    - using xcom_pull
    - transaction

4.  build summary

    - Create and store a summary table to track the first and last channel for each user
    - separate summary code into a module within the plugins
    - transaction

# docs

1. [SQL for dataengineer](docs/SQL_for_dataengineer.md)
2. [data_pipeline](docs/data_pipeline.md)
3. [Redshift](docs/Redshift.md)
4. [full refresh & incremental update](docs/full_refresh_and_incremental_update.md)
5. [transaction](docs/transaction.md)
