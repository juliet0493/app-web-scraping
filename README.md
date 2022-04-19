# Running Airflow ETL with Docker

## Project Structure
The main project directory will be as follow:
```
./dags - Contains DAG files.
./logs - Contains logs from task execution and scheduler.
./plugins - Contains custom plugins.
./config - Contains configuration files (Sql scripts and postgres credentials).
./scripts - Contains bash scripts
```

## Setting up environment

### Environment file, .env
```
AIRFLOW_UID=50000
DB_PASSWORD=XXXXXX
```

### Postgres credentials, postgres.cfg
```
[postgres]
USER=lb_hiring
PASSWORD=XXXXXX
DATABASE=postgres
HOST=XXXXXX
```

### Initiating Airflow in Docker
`docker-compose --env-file .env up`

#### docker-compose.yaml
- **airflow-scheduler** - The scheduler monitors all tasks and DAGs, then triggers the task instances once their dependencies are complete.
- **airflow-webserver** - The webserver is available at http://localhost:8080.
- **airflow-worker** - The worker that executes the tasks given by the scheduler.
- **airflow-init** - The initialization service.
- **flower** - The flower app for monitoring the environment. It is available at http://localhost:5555.
- **postgres** - The database.
- **redis** - The redis - broker that forwards messages from scheduler to worker
- for more details please refer to [airflow doc](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)

### Running DAG
**./scripts/entrypoint.sh**
```
airflow initdb
airflow webserver -p 8080
airflow scheduler
```

### DAGs
Contains tasks that scrap data from webpage and update the data into postgres table.
