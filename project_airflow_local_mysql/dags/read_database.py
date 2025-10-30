from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

with DAG(
    'mysql_reader_dag',
    start_date=datetime(2024, 1, 1),
    #schedule_interval='@daily',
    catchup=False,
) as dag:
    
    read_from_mysql = SQLExecuteQueryOperator(
        task_id='read_from_mysql',
        conn_id='mysql_default',
        sql='SELECT * FROM sample_data.customers LIMIT 3',
    )