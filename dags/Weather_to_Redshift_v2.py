from airflow import DAG
from airflow.operators.python import PythonOperator

# from airflow.operators import PythonOperator
from airflow.models import Variable
from airflow.hooks.postgres_hook import PostgresHook

from datetime import datetime
from datetime import timedelta

import requests
import logging
import psycopg2
import json


def get_Redshift_connection():
    # autocommit is False by default
    hook = PostgresHook(postgres_conn_id="redshift_dev_db")
    return hook.get_conn().cursor()


def extract(**context):
    lat = context["params"]["lat"]
    lon = context["params"]["lon"]
    part = context["params"]["part"]
    API_key = Variable.get("open_weather_api_key")

    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API_key}&units=metric"
    data = requests.get(url).json()
    return data


def transform(**context):
    weather_list = []
    data = context["task_instance"].xcom_pull(key="return_value", task_ids="extract")
    for day in data["daily"]:
        weather_list.append(
            tuple(
                [
                    datetime.fromtimestamp(day["dt"]).strftime("%Y-%m-%d"),
                    day["temp"]["day"],
                    day["temp"]["min"],
                    day["temp"]["max"],
                ]
            )
        )
    return weather_list


def load(**context):
    schema = context["params"]["schema"]
    table = context["params"]["table"]
    weather_list = context["task_instance"].xcom_pull(
        key="return_value", task_ids="transform"
    )
    conn = get_Redshift_connection()

    # create temp table & copy all data from original table
    create_sql = f"""DROP TABLE IF EXISTS {schema}.temp_{table};
    CREATE TABLE {schema}.temp_{table} (LIKE {schema}.{table} INCLUDING DEFAULTS; INSERT INTO {schema}.temp_{table} SELECT * FROM {schema}.{table};"""
    try:
        conn.execute(create_sql)
        conn.execute("COMMIT;")
    except Exeption as e:
        conn.execute("ROLLBACK;")
        raise

    # insert new data into temp table
    insert_sql = f"INSERT INTO {schema}.temp_{table} VALUES " + ",".json(weather_list)
    try:
        conn.execute(insert_sql)
        conn.execute("COMMIT;")
    except Exeption as e:
        conn.execute("ROLLBACK;")
        raise

    # alter original table
    alter_sql = f"""DELETE FROM {schema}.{table};
    INSERT INTO {schema}.{table}
    SELECT date, temp, min_tmp, max_temp FROM (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY date ORDER BY created_date DESC) seq
        FROM {schema}.temp_{table}
    )
    WHERE seq = 1;"""
    try:
        conn.execute(alter_sql)
        conn.execute("COMMIT;")
    except Exeption as e:
        conn.execute("ROLLBACK;")
        raise


"""
CREATE TABLE dbtnghk528.weather_forecast (
    date date,
    temp float,
    min_temp float,
    max_temp float,
    updated_date timestamp default GETDATE()
);
"""

dag = DAG(
    dag_id="Weather_to_Redshift_aohus",
    start_date=datetime(2023, 2, 18),  # 날짜가 미래인 경우 실행이 안됨
    schedule_interval="0 2 * * *",  # 적당히 조절
    max_active_runs=1,
    catchup=False,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=3),
    },
)

extract = PythonOperator(
    task_id="extract",
    python_callable=extract,
    params={"lat": 37.5665, "lon": 126.9780, "part": "hourly,minutely"},
    dag=dag,
)


transform = PythonOperator(
    task_id="transform", python_callable=transform, params={}, dag=dag
)

load = PythonOperator(
    task_id="load",
    python_callable=load,
    params={"schema": "dbtnghk528", "table": "weather_forecast"},
    dag=dag,
)

extract >> transform >> load
