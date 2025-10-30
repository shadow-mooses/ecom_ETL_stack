## Tech stack
- local instance of mysql running on host machine
- containerized version of airflow
- standalone installation of dbt

## Schedules
- Airflow to generate new data for data warehouse cluster every five minutes
- Airflow to trigger data cleaning and write data to a compute cluster every 10 minutes
- dbt to refresh it's sources/models (dbt run) every 15 minutes.

## Data Flow

Airflow to generate and write new lines of data every minute to the sales/orders/customers tables in mysql - this is to simulate online orders coming through.
Build data transformations in dbt - this is to simulate transformations of tables for an analyst or bi tool to manipulate and dashboard.
Airflow to trigger a dbt run every 5 minutes to refresh tables.

## Initialization notes
Airflow - container
1. Create a virtual environment with either conda or venv for the services.
2. run `pip install -r requirements.txt` 
3. create your directory for your ELT project
4. create an `.env` file with the argument `AIRFLOW_UID=50000` in the same directory as the docker compose file.
5. run `docker compose up airflow-init` in your directory to initialize the airflow container.
6. then run `docker compose up`.
7. Navigate to the airflow GUI at `localhost:8080` then go to connections > create new connections.
8. Create the new mysql connection and use `host.docker.internal`, this allows airflow to look outside of the container for the port.

Mysql - local instance
1. Initialize the local instance of mysql server either by downloading the mysql client or by the command line.
2. create an airflow user and password, grant them permissions to access the database (Airflow will need to this to interact with the mysql database)

dbt - container
1. create a new directory in your ELT project `mkdir -p dbt ~/.dbt`
2. run `docker-compose exec dbt bash` to move to the container cli.
3. run `docker deps` and `docker debug` to make sure everything is running smoothly.



bugs to fix
integrity  error - need to allow duplicate records in customer id