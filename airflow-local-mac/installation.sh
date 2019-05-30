#!/bin/bash
USER_HOME=/Users/myuser 
git clone https://github.com/pyenv/pyenv.git $USER_HOME/.pyenv
export PYENV_ROOT="$USER_HOME/.pyenv"
echo "export PYENV_ROOT=$USER_HOME/.pyenv" >> $USER_HOME/.bashrc
export PATH="$PYENV_ROOT/bin:$PATH"
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> $USER_HOME/.bashrc
eval "$(pyenv init -)"
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> $USER_HOME/.bashrc
export LDFLAGS="-L/usr/local/opt/sqlite/lib -L/usr/local/opt/zlib/lib" 
export CPPFLAGS="-I/usr/local/opt/sqlite/include -I/usr/local/opt/zlib/include"
pip install -U pip
pip install pipenv
mkdir $USER_HOME/airflow
cd $USER_HOME/airflow
# We copy our dags froma a S3 bucket
aws s3 cp --recursive s3://Your_Bucket/ $(pwd)
# Run this command to load your environment variables in our case we called from Parameter Store in AWS
source scripts/variables.sh
echo "source $USER_HOME/airflow/scripts/variables.sh" >> $USER_HOME/.bashrc
# Script to create airflow.cfg
sh local_setup.sh
# Necessary for newer versions of airflow
export SLUGIFY_USES_TEXT_UNIDECODE=yes
export PIPENV_VENV_IN_PROJECT=True
pipenv install --python 3.6.5
pipenv run airflow initdb
pipenv run airflow scheduler
pipenv run airflow webserver
