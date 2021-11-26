#!/usr/bin/env bash

airflow initdb
airflow webserver -p 8080
airflow scheduler