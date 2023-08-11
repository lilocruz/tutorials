from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess
import requests

# Default arguments for the DAG
default_args = {
    'owner': 'user',
    'start_date': datetime(2023, 8, 11),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

# DAG definition
dag = DAG(
    'execute_splinter_ezzytable',
    default_args=default_args,
    description='Execute the provided Splinter EzzyTable script',
    schedule_interval=None, # Manual triggering
    tags=['automation']
)

def execute_script():
    # URL to the raw GitHub content
    github_url = 'https://raw.githubusercontent.com/lilocruz/tutorials/master/splinter_ezzytable.py' # Update with the correct URL
    response = requests.get(github_url)
    script_content = response.text

    # Save the script to a temporary file
    script_path = '/tmp/splinter_ezzytable.py' # Update with the path where you want to save the script
    with open(script_path, 'w') as file:
        file.write(script_content)

    # Command to execute the script
    command = [
        'python', script_path,
        '--min_wait_time', '1',
        '--max_wait_time', '5',
        '-r', '1024x766',
        '--incognito',
        '--debug',
        '-k', 'reserva',
        '--incognito',
        '--debug',
        '--headless',
        'ezzytable.com'
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise Exception('Script execution failed')

# Task to execute the provided script
execute_script_task = PythonOperator(
    task_id='execute_script',
    python_callable=execute_script,
    dag=dag
)
