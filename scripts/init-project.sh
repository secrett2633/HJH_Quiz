#!/bin/bash

poetry install
poetry shell

pre-commit install


PSQL_COMMANDS="
    CREATE DATABASE test_db;
    CREATE DATABASE prod_db;
    CREATE DATABASE dev_db;
    ALTER DATABASE test_db SET TIMEZONE TO 'Asia/Seoul';
    ALTER DATABASE prod_db SET TIMEZONE TO 'Asia/Seoul';
    ALTER DATABASE dev_db SET TIMEZONE TO 'Asia/Seoul';
"

sleep 7

echo "$PSQL_COMMANDS" | docker exec -i postgresql psql -U postgres

export PYTHONPATH=$PWD
export ENV_STATE="dev"
python backend/core/init_db.py
