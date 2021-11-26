from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import date, datetime, timedelta
from configparser import ConfigParser

import pandas as pd
import psycopg2 as pg

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def extract_sql(sql_path):
    config = ConfigParser()
    config.read("config/postgres.cfg")

    dbconnect = pg.connect(
        dbname=config.get("postgres", "DATABASE"),
        user=config.get("postgres", "USER"),
        password=config.get("postgres", "PASSWORD"),
        host=config.get("postgres", "HOST")
        )
    
    with open(sql_path) as f:
        sql = f.read()
    df = pd.read_sql(sql, con=dbconnect)
    filename = sql_path.rsplit(".", maxsplit=1)[0].rsplit("/", maxsplit=1)[0]
    df.to_csv(f"{filename}_%s.csv" % date.today().strftime("%Y%m%d"), encoding='utf-8', index=False)
    return 

with DAG('call_postgres_sql',
    start_date=datetime(2020, 6, 1),
    max_active_runs=3,
    schedule_interval='@once',
    default_args=default_args,
    catchup=False
    ) as dag:
    
    aggr_sales = PythonOperator(
        task_id='output_aggr_sales',
        python_callable=extract_sql, 
        op_kwargs={"sql_path":'/opt/airflow/config/sql/aggr_sales.sql'},
        dag=dag
        )
        
    top_selling_product = PythonOperator(
        task_id='output_top_selling_product',
        python_callable=extract_sql, 
        op_kwargs={"sql_path":'/opt/airflow/config/sql/top_selling_product.sql'}, 
        dag=dag
        )
        
    top_purchase_customer = PythonOperator(
        task_id='output_top_purchase_customer',
        python_callable=extract_sql, 
        op_kwargs={"sql_path":'/opt/airflow/config/sql/top_purchase_customer.sql'},
        dag=dag
        )
        
    non_pants_buyer = PythonOperator(
        task_id='output_non_pants_buyer',
        python_callable=extract_sql, 
        op_kwargs={"sql_path":'/opt/airflow/config/sql/non_pants_buyer.sql'},
        dag=dag
        )
    
    aggr_sales
    top_selling_product
    top_purchase_customer
    non_pants_buyer
