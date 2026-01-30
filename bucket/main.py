
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def print_hello():
    return "Hello World! This DAG was loaded directly from GCS and is running on GKE."

# Define the DAG
with DAG(
    'hello_world_gke123',
    default_args=default_args,
    description='Simple Hello World for GKE/GCS setup',
    schedule_interval=timedelta(days=1), # Runs daily, or trigger manually
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['example', 'gke'],
) as dag:

    # Task 1: Python Task
    task_hello_python = PythonOperator(
        task_id='hello_from_python',
        python_callable=print_hello,
    )

    # Task 2: Bash Task (checks the worker environment)
    task_hello_bash = BashOperator(
        task_id='hello_from_bash',
        bash_command='echo "Running on $(hostname) in the Airflow Worker pod."'
    )

    # Set dependencies
    task_hello_python >> task_hello_bash
