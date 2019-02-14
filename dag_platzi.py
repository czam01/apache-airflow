import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator




# Jinja templating is used so that this values are replaced on execution
# time when passed to operators

year = '{{ macros.ds_format(ds, "%Y-%m-%d", "%Y") }}'
month = '{{ macros.ds_format(ds, "%Y-%m-%d", "%m") }}'
day = '{{ macros.ds_format(ds, "%Y-%m-%d", "%d") }}'


WORKFLOW_DEFAULT_ARGS = {
    'email': ['email@gmail.com', 'email2@bgmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='pampa_main_etl',
    description='Pampa Main ETL DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2017, 11, 1),
    catchup=False,
    concurrency=3,
    default_args=WORKFLOW_DEFAULT_ARGS
)

def greeting():
    import logging
    logging.info('Hello World!')

############ Cloudwatch logs to S3 ############
cloudwatch = PythonOperator(
    task_id='extract_cloudwatch_all',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

############ Mongo snapshots to S3 ############
accounts_mongo = PythonOperator(
    task_id='extract_mongo_accounts',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

profiles_mongo = PythonOperator(
    task_id='extract_mongo_profiles',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

contacts_relateds_mongo = PythonOperator(
    task_id='extract_mongo_contacts_relateds',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

user_contacts_mongo = PythonOperator(
    task_id='extract_mongo_user_contacts',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

verified_contacts_mongo = PythonOperator(
    task_id='extract_mongo_verified_contacts',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

############ Glue ############
payments_glue = PythonOperator(
    task_id='glue_process_payments',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

referrals_glue = PythonOperator(
    task_id='glue_process_referrals',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

prizes_glue = PythonOperator(
    task_id='glue_process_prizes',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

cashouts_glue = PythonOperator(
    task_id='glue_process_cashouts',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

cashins_glue = PythonOperator(
    task_id='glue_process_cashins',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

phone_contacts_glue = PythonOperator(
    task_id='glue_process_phone_contacts',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

mach_card_receptions_glue = PythonOperator(
    task_id='glue_process_mach_card_receptions',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

email_verifications_glue = PythonOperator(
    task_id='glue_process_email_verifications',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

cloudwatch >> payments_glue
cloudwatch >> referrals_glue
cloudwatch >> prizes_glue
cloudwatch >> cashouts_glue
cloudwatch >> cashins_glue
cloudwatch >> phone_contacts_glue
cloudwatch >> mach_card_receptions_glue
cloudwatch >> email_verifications_glue

accounts_glue = PythonOperator(
    task_id='glue_process_accounts',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

profiles_glue = PythonOperator(
    task_id='glue_process_profiles',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

verified_contacts_glue = PythonOperator(
    task_id='glue_process_verified_contacts',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

user_contacts_glue = PythonOperator(
    task_id='glue_process_user_contacts',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

contacts_relateds_glue = PythonOperator(
    task_id='glue_process_contacts_relateds',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

accounts_mongo >> accounts_glue
profiles_mongo >> profiles_glue
verified_contacts_mongo >> verified_contacts_glue
user_contacts_mongo >> user_contacts_glue
contacts_relateds_mongo >> contacts_relateds_glue

############ Aggregates ############

user_agg_daily_glue = PythonOperator(
    task_id='glue_calc_daily_user_agg',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

user_detail_glue = PythonOperator(
    task_id='glue_process_user_detail',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

payments_glue >> user_agg_daily_glue
prizes_glue >> user_agg_daily_glue

user_agg_daily_glue >> user_detail_glue
accounts_glue >> user_detail_glue
profiles_glue >> user_detail_glue
verified_contacts_glue >> user_detail_glue
user_contacts_glue >> user_detail_glue
payments_glue >> user_detail_glue
cashouts_glue >> user_detail_glue
referrals_glue >> user_detail_glue

############ Delivery ############

# Sources are crawled on phone_contacts_glue
# Target is not partitioned unecessary to crawl
clean_phone_contacts = PythonOperator(
    task_id='clean_phone_contacts',
    python_callable=greeting,
    dag=dag
)



load_drop_phone_contacts_query = PythonOperator(
    task_id='load_drop_phone_contacts_query',
    python_callable=greeting,
    dag=dag
)

load_create_phone_contacts_query = PythonOperator(
    task_id='load_create_phone_contacts_query',
    python_callable=greeting,
    dag=dag
)

phone_contacts_glue >> clean_phone_contacts
clean_phone_contacts >> load_drop_phone_contacts_query
load_drop_phone_contacts_query >> load_create_phone_contacts_query

deliver_accounts_athena = PythonOperator(
    task_id='athena_deliver_accounts',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

accounts_glue >> deliver_accounts_athena

deliver_user_detail_athena = PythonOperator(
    task_id='athena_deliver_user_detail',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

user_detail_glue >> deliver_user_detail_athena

############ Segment Daily Update ############
extract_user_detail_query = PythonOperator(
    task_id='extract_user_detail_query',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

transform_segment_daily_update = PythonOperator(
    task_id='transform_segment_daily_update',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

filter_segment_remove_duplicates = PythonOperator(
    task_id='filter_segment_remove_duplicates',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

load_segment_daily_update = PythonOperator(
    task_id='load_segment_daily_update',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

deliver_user_detail_athena >> extract_user_detail_query
extract_user_detail_query >> transform_segment_daily_update
transform_segment_daily_update >> filter_segment_remove_duplicates
filter_segment_remove_duplicates >> load_segment_daily_update

load_segment_replace_uploaded_list = PythonOperator(
    task_id='load_segment_replace_uploaded_list',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)

load_segment_daily_update >> load_segment_replace_uploaded_list

############ Zendesk Daily extraction ############
extract_zendesk_to_s3 = PythonOperator(
    task_id='extract_zendesk_to_s3',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)


extract_zendesk_to_local = PythonOperator(
    task_id='extract_zendesk_to_local',
    python_callable=greeting,
    provide_context=True,
    dag=dag
)


transform_manual_validations = PythonOperator(
    task_id='transform_manual_validations',
    python_callable=greeting,
    dag=dag
)



load_local_to_s3 = PythonOperator(
    task_id='load_local_to_s3',
    python_callable=greeting,
    dag=dag
)



load_drop_manual_validations_query = PythonOperator(
    task_id='load_drop_manual_validations_query',
    python_callable=greeting,
    dag=dag
)


load_create_manual_validations_query = PythonOperator(
    task_id='load_create_manual_validations_query',
    python_callable=greeting,
    dag=dag
)

extract_zendesk_to_s3 >> extract_zendesk_to_local
extract_zendesk_to_local >> transform_manual_validations
transform_manual_validations >> load_local_to_s3
load_local_to_s3 >> load_drop_manual_validations_query
load_drop_manual_validations_query >> load_create_manual_validations_query


############ Externals ############

load_mach_registrations = PythonOperator(
    task_id='load_mach_registrations',
    python_callable=greeting,
    provide_context=False,
    dag=dag
)

deliver_accounts_athena >> load_mach_registrations


############ Analytics ############

# Sources are crawled previously
# Target is not partitioned unecessary to crawl
calc_phones_value = PythonOperator(
    task_id='calc_phones_value',
    python_callable=greeting,
    dag=dag
)

contacts_relateds_glue >> calc_phones_value
verified_contacts_glue >> calc_phones_value
user_detail_glue >> calc_phones_value

calc_contacts_score = PythonOperator(
    task_id='calc_contacts_score',
    python_callable=greeting,
    dag=dag
)



load_create_contacts_score_query = PythonOperator(
    task_id='load_create_contacts_score_query',
    python_callable=greeting,
    dag=dag
)


load_create_contacts_score_detail_query = PythonOperator(
    task_id='load_create_contacts_score_detail_query',
    python_callable=greeting,
    dag=dag
)

load_create_phone_contacts_query >> calc_contacts_score
deliver_user_detail_athena >> calc_contacts_score
calc_contacts_score >> load_create_contacts_score_query
calc_contacts_score >> load_create_contacts_score_detail_query
