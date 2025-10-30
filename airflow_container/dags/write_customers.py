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
    'insert_customers_every_5_min',
    default_args=default_args,
    description='Insert new customer entries every 5 minutes',
    schedule='*/5 * * * *',  # Every 5 minutes
    catchup=False,
    tags=['mysql', 'customers'],
)

def generate_customer_data(**context):
    """Generate random customer data"""
    first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Emily', 'Chris', 'Lisa']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    cities = ['New York','Taiwan', 'London','Houston','Phoenix']
    randomnum = random.randint(1,10)
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    username = f"{randomnum}{first_name[0].lower()}{last_name.lower()}"
    city = random.choice(cities)
    
    # Push data to XCom for the next task
    context['ti'].xcom_push(key='first_name', value=first_name)
    context['ti'].xcom_push(key='last_name', value=last_name)
    context['ti'].xcom_push(key='email', value=email)
    context['ti'].xcom_push(key='username', value=username)
    context['ti'].xcom_push(key='city', value=city)
    

generate_data = PythonOperator(
    task_id='generate_customer_data',
    python_callable=generate_customer_data,
    dag=dag,
)

# Insert customer into MySQL table
# Note: Adjust the SQL based on your actual table schema
insert_customer = SQLExecuteQueryOperator(
    task_id='insert_customer',
    conn_id='mysql_default',  # Configure this connection in Airflow UI
    sql="""
        INSERT INTO customers (first_name, last_name, email, username, city, created_at)
        VALUES (
            '{{ ti.xcom_pull(task_ids='generate_customer_data', key='first_name') }}',
            '{{ ti.xcom_pull(task_ids='generate_customer_data', key='last_name') }}',
            '{{ ti.xcom_pull(task_ids='generate_customer_data', key='email') }}',
            '{{ ti.xcom_pull(task_ids='generate_customer_data', key='username') }}',
            '{{ ti.xcom_pull(task_ids='generate_customer_data', key='city') }}',
            NOW()
        );
    """,
    dag=dag,
)

# Set task dependencies
generate_data >> insert_customer