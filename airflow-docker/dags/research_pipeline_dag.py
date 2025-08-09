from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from airflow.hooks.base import BaseHook

import pandas as pd
import os
from sqlalchemy import create_engine
from q2_pipeline_db.processors.class_data_processor import DataProcessor

# Config
DATA_DIR = "/opt/airflow/q2_pipeline_db/data"
SQL_PATH = "/opt/airflow/q2_pipeline_db/sql/create_tables.sql"
conn = BaseHook.get_connection("postgres_default")
POSTGRES_CONN_STRING = f"postgresql+psycopg2://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"

# Global storage (simple)
cleaned_data = {}

# DAG definition
default_args = {
    'owner': 'airflow',
}

dag = DAG(
    dag_id='research_pipeline',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    description="Extract, Clean, Load research articles into PostgreSQL"
)

# Task 1: Create Tables
create_tables = PostgresOperator(
    task_id='create_tables',
    postgres_conn_id='postgres_default',
    sql=SQL_PATH,
    dag=dag
)

# Extract & Clean (ใช้ DataProcessor)
def extract_and_clean(filename, source_name, **kwargs):
    filepath = os.path.join(DATA_DIR, filename)
    df = pd.read_csv(filepath)

    processor = DataProcessor(df)
    processor.standardize_columns()
    processor.handle_missing_values()
    processor.deduplicate()

    cleaned = processor.get_dataframe()
    cleaned["SOURCE"] = source_name  # เพิ่มคอลัมน์ SOURCE เพื่อให้ใช้ใน merge
    cleaned_data[source_name] = cleaned

# สร้าง task สำหรับแต่ละไฟล์
extract_scopus = PythonOperator(
    task_id='extract_scopus',
    python_callable=extract_and_clean,
    op_kwargs={'filename': 'scopus_selected.csv', 'source_name': 'scopus'},
    dag=dag
)

extract_tci = PythonOperator(
    task_id='extract_tci',
    python_callable=extract_and_clean,
    op_kwargs={'filename': 'tci_selected.csv', 'source_name': 'tci'},
    dag=dag
)

extract_wos = PythonOperator(
    task_id='extract_wos',
    python_callable=extract_and_clean,
    op_kwargs={'filename': 'wos_selected.csv', 'source_name': 'wos'},
    dag=dag
)

# Transform & Load
def transform_and_load(**kwargs):
    engine = create_engine(POSTGRES_CONN_STRING)

    # 1. รวมข้อมูลจากทุกแหล่ง
    merged_df = pd.concat(cleaned_data.values(), ignore_index=True)

    # 2. เตรียมตาราง sources (insert ถ้ายังไม่มี)
    sources = merged_df["SOURCE"].unique()
    with engine.begin() as conn:
        for s in sources:
            conn.execute(
                "INSERT INTO sources (source_name) VALUES (%s) ON CONFLICT DO NOTHING", (s,)
            )

    # 3. ดึง source_id จากตาราง sources
    source_df = pd.read_sql("SELECT * FROM sources", engine)

    # 4. รวมข้อมูล source_id
    merged_df = merged_df.merge(source_df, left_on='SOURCE', right_on='source_name')
    final_df = merged_df[[
        'ARTICLE_NAME', 'AUTHOR', 'OUTPUT_YEAR', 'JOURNAL',
        'VOLUME', 'ISSUE', 'PAGE_RANGE', 'DOC_TYPE', 'source_id'
    ]]

    # 5. โหลดลงตาราง articles
    final_df.to_sql('articles', engine, if_exists='append', index=False)

transform_and_load = PythonOperator(
    task_id='transform_and_load',
    python_callable=transform_and_load,
    dag=dag
)

# ask Dependencies
create_tables >> [extract_scopus, extract_tci, extract_wos] >> transform_and_load
