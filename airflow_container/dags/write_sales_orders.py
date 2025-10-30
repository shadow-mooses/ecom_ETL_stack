from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import random
import string


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'insert_new_sales_orders_every_five_minutes',
    default_args=default_args,
    description='Insert_new_sales_orders',
    schedule='*/5 * * * *',  # Every 5 minutes
    catchup=False,
    tags=['mysql', 'sales_orders'],
)

def generate_order_data(**context):
    
    order_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded']
    
    customer_id = random.randint(1, 172)
    store_id = random.randint(1, 7)
    order_id = random.randint(100000, 999999)
    product_id = random.randint(1, 25)
    order_status = random.choice(order_statuses)

    context['ti'].xcom_push(key='customer_id', value=customer_id)
    context['ti'].xcom_push(key='store_id', value=store_id)
    context['ti'].xcom_push(key='order_id', value=order_id)
    context['ti'].xcom_push(key='product_id', value=product_id)
    context['ti'].xcom_push(key='order_status', value=order_status)


generate_data = PythonOperator(
    task_id='generate_customer_data',
    python_callable=generate_order_data,
    dag=dag,
)

# Insert customer into MySQL table
# Note: Adjust the SQL based on your actual table schema
insert_customer = SQLExecuteQueryOperator(
    task_id='insert_order',
    conn_id='mysql_default',  # Configure this connection in Airflow UI
    sql="""
        INSERT INTO sales_orders (customer_id, store_id, unique_id, product_id, order_status, order_date)
        VALUES (
            '{{ ti.xcom_pull(task_ids='generate_customer_data', key='customer_id') }}',
            '{{ ti.xcom_pull(task_ids='generate_customer_data', key='store_id') }}',
            '{{ ti.xcom_pull(task_ids='generate_customer_data', key='order_id') }}',
            '{{ ti.xcom_pull(task_ids='generate_customer_data', key='product_id') }}',
            '{{ ti.xcom_pull(task_ids='generate_customer_data', key='order_status') }}',
            NOW()
        );
    """,
    dag=dag,
)

# Set task dependencies
generate_data >> insert_customer