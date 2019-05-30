#!/bin/bash
# This script setups the environment for a local execution of airflow (i.e on your computer)

# Points to the parent folder of the setup script
AIRFLOW_HOME="$(dirname "$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )")"

cat <<EOF > $AIRFLOW_HOME/.env
PIPENV_VENV_IN_PROJECT=True
AIRFLOW_HOME=$AIRFLOW_HOME
EOF

cat <<EOF > $AIRFLOW_HOME/airflow.cfg

[core]
airflow_home = $AIRFLOW_HOME
dags_folder = $AIRFLOW_HOME/dags
base_log_folder = $AIRFLOW_HOME/logs

remote_logging = False
encrypt_s3_logs = False
logging_level = INFO
log_format = [%%(asctime)s] {%%(filename)s:%%(lineno)d} %%(levelname)s - %%(message)s
simple_log_format = %%(asctime)s %%(levelname)s - %%(message)s
executor = SequentialExecutor
sql_alchemy_conn = sqlite:////$AIRFLOW_HOME/airflow.db
sql_alchemy_pool_size = 5
sql_alchemy_pool_recycle = 3600
parallelism = 32
dag_concurrency = 16
dags_are_paused_at_creation = True
non_pooled_task_slot_count = 128
max_active_runs_per_dag = 16
load_examples = False
plugins_folder = $AIRFLOW_HOME/plugins
fernet_key = QfQ90TaCFkE9fSLJnoikJCRxj4cnqFX69D1_Lbnhinw=
donot_pickle = False
dagbag_import_timeout = 30
task_runner = BashTaskRunner
default_impersonation =
security =
unit_test_mode = False
task_log_reader = file.task
enable_xcom_pickling = True
killed_task_cleanup_time = 60

[cli]
api_client = airflow.api.client.local_client
endpoint_url = http://localhost:8080

[api]
auth_backend = airflow.api.auth.backend.default

[operators]
default_owner = Airflow
default_cpus = 1
default_ram = 512
default_disk = 512
default_gpus = 0

[webserver]
base_url = http://localhost:8080
web_server_host = 0.0.0.0
web_server_port = 8080
web_server_ssl_cert =
web_server_ssl_key =
web_server_worker_timeout = 120
worker_refresh_batch_size = 1
worker_refresh_interval = 30
secret_key = temporary_key
workers = 4
worker_class = sync
access_logfile = -
error_logfile = -
expose_config = False
authenticate = False
filter_by_owner = False
owner_mode = user
dag_default_view = tree
dag_orientation = LR
demo_mode = False
log_fetch_timeout_sec = 5
hide_paused_dags_by_default = False
page_size = 100

[email]
email_backend = airflow.utils.email.send_email_smtp

[smtp]
smtp_host = $SMTP_HOST
smtp_starttls = True
smtp_ssl = False
smtp_user = $SMTP_USER
smtp_password = $SMTP_PASS
smtp_port = $SMTP_PORT
smtp_mail_from = mail@mail.com

[celery]
celery_app_name = airflow.executors.celery_executor
worker_concurrency = 16
worker_log_server_port = 8793
broker_url = sqla+mysql://airflow:airflow@localhost:3306/airflow
result_backend = db+mysql://airflow:airflow@localhost:3306/airflow
flower_host = 0.0.0.0
flower_port = 5555
default_queue = default
celery_config_options = airflow.config_templates.default_celery.DEFAULT_CELERY_CONFIG

[dask]
cluster_address = 127.0.0.1:8786

[scheduler]
job_heartbeat_sec = 5
scheduler_heartbeat_sec = 5
run_duration = -1
min_file_process_interval = 0
dag_dir_list_interval = 300
print_stats_interval = 30
child_process_log_directory = $AIRFLOW_HOME/logs/scheduler
scheduler_zombie_task_threshold = 300
catchup_by_default = False
max_tis_per_query = 0
statsd_on = False
statsd_host = localhost
statsd_port = 8125
statsd_prefix = airflow
max_threads = 2
authenticate = False

[ldap]
uri =
user_filter = objectClass=*
user_name_attr = uid
group_member_attr = memberOf
superuser_filter =
data_profiler_filter =
bind_user = cn=Manager,dc=example,dc=com
bind_password = insecure
basedn = dc=example,dc=com
cacert = /etc/ca/ldap_ca.crt
search_scope = LEVEL

[mesos]
master = localhost:5050
framework_name = Airflow
task_cpu = 1
task_memory = 256
checkpoint = False
authenticate = False

[kerberos]
ccache = /tmp/airflow_krb5_ccache
principal = airflow
reinit_frequency = 3600
kinit_path = kinit
keytab = airflow.keytab

[github_enterprise]
api_rev = v3

[admin]
hide_sensitive_variable_fields = True

EOF
