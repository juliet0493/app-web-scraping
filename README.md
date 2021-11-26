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

### Running Airflow in Docker
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
Contains tasks that take data from postgres and output the return data as csv.
- **aggr_sales** - Aggregated sales.
- **top_selling_product** - Top three selling product ids on a monthly basis.
- **top_purchase_customer** - Top three customer_ids based on transaction value on a monthly basis.
- **non_pants_buyer** - Customer_ids (having transactions) who have never purchased pants(subcategory) from yet.
