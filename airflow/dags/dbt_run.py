from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'retries': 1,
}

with DAG(
    'dbt_run_docker',
    default_args=default_args,
    #schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['dbt'],
) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='docker exec 121d3b09260a dbt run',
    )

    print_success = BashOperator(
        task_id='print_success',
        bash_command='echo "dbt run completed successfully!"',
    )

    dbt_run >> print_success