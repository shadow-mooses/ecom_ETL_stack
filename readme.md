# Building Designing a modern analytics workflow




### How to run
1. create an environment to run dbt and airflow either with conda or venv.
2. setup your tech stack:
   1. Mysql - Database
      1. Navigate to the container directory and execute `docker compose up` to initialize the database.
      2. Explore the data base with `mysqlsh` then `\c root@localhost:3306`.
   2. Airflow - Orchestrator
      1. Make sure you have enough memory allocated to run airlfow, you'll need about 4mb. Run this code `docker run --rm "debian:bookworm-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'`
      2. Download the docker compose file then run `docker init`. Optional: create an `.env` file with `AIRFLOW_UID=50000` variable to prevent issues with userid during initialization.
      3. run `docker compose up airflow-init` to initialize. You should get an exit code of `airflow-init-1 exited with code 0`
      4. then run `docker compose up`
      5. visit `localhost:8080` to see the airflow gui
   3. dbt - transformation
      1. 
3. Connecting the orchestrator to the database
   1. Create the `airflow user` in the database with all permissions
   2. 


## cleaning up
run `docker compose down --volumes --rmi all` to close down gracefully airlfow

