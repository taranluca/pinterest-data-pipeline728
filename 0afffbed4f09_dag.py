from airflow.models import DAG
from datetime import datetime
from datetime import timedelta
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'taran_luca_0afffbed4f09',
    'depends_on_past': False,
    'email': ['taranlucapatel@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'start_date': datetime(2024, 10, 28),
    'retry_delay': timedelta(minutes=5),
    'end_date': datetime(2024, 11, 28),
}
with DAG(dag_id='0afffbed4f09_dag',
         default_args=default_args,
         schedule_interval='0 0 * * *',
         catchup=False,
         tags=['0afffbed4f09_dag']
         ) as dag:

  opr_run_now = DatabricksRunNowOperator(
    task_id = 'run_now',
    databricks_conn_id = 'databricks_default',
    job_id = 1075507191048015
  )