import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'project_pipeline_dag',
    default_args=default_args,
    description='A DAG for collecting data and training the model',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# mounted path from the docker-compose file
# This is the path inside the container where your project is mounted
project_path = '/opt/project'


# Define tasks using BashOperator
fetch_task = BashOperator(
    task_id='fetch_data',
    bash_command=f'cd {project_path} && pip install kaggle && pip install pandas && python src/fetch_data.py',
    dag=dag,
)

preprocess_task = BashOperator(
    task_id='preprocess_data',
    bash_command=f'cd {project_path} && python src/preprocess.py',
    dag=dag,
)

train_task = BashOperator(
    task_id='train_model',
    bash_command=f'cd {project_path} && pip install tensorflow && python src/model/train.py',
    dag=dag,
)

#evaluate_task = BashOperator(
#    task_id='evaluate_model',
#    bash_command=f'cd {project_path} && pip install mlflow && pip install tensorflow && python mlflow.py',
#    dag=dag,
#)

#dvc_version_task = BashOperator(
#    task_id='version_with_dvc',
#    bash_command=f'''
#    cd {project_path} &&
#    dvc repro &&
#    git add data/*.dvc src/api/model.keras.dvc .gitignore &&
#    git commit -m "Update data and model via Airflow" || echo "No changes to commit" &&
#    dvc push || echo "DVC push failed, check authentication"
#    ''',
#    dag=dag,
#)

# Define task dependencies
fetch_task >> preprocess_task >> train_task #>> dvc_version_task

#dvc init &&
#   dvc remote modify gdrive_remote gdrive_use_service_account true &&
#    dvc remote modify gdrive_remote gdrive_service_account_json_file_path src/dvc.json
#    dvc remote add -d gdrive_remote gdrive://Joq6kLb1Y8FmvCgGwcjJu8Hu8ZqQ5