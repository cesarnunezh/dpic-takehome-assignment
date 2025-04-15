from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime
from data_pipeline import fetch_data, cleaning, data_to_db
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_summary_email():
    summary = "Weekly pipeline run completed. \n New rows added: 300. \n Dashboard updated."

    sender = "sender@example.com"
    message = MIMEMultipart()
    message["From"] = "sender@example.com"
    message["To"] = "recipient@example.com"
    message["Subject"] = "DPIC Weekly summary"
    message.attach(MIMEText(summary,"plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, "password")
        server.send_message(message)

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 4, 15),
    "retries": 1,
}

with DAG(
    dag_id="dpic_weekly_pipeline",
    default_args=default_args,
    description="Weekly pipeline for cleaning, loading and reporting",
    schedule_interval="@weekly",
    catchup=False,
) as dag:

    fetch_task = PythonOperator(
        task_id="fetch_raw_data",
        python_callable=fetch_data.main,
    )

    clean_task = PythonOperator(
        task_id="clean_data",
        python_callable=cleaning.main,
    )

    load_db_task = PythonOperator(
        task_id="load_db_data",
        python_callable=data_to_db.main,
    )

    email_task = PythonOperator(
        task_id="send_email_summary",
        python_callable=send_summary_email,
    )

    fetch_task >> clean_task >> load_db_task >> email_task
