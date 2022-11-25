# My solution for Apex Systems

## Requirements
- `Docker` v20
- `docker-compose` v2.12.2
- At least 10 GB of storage available for building the images
- A work directory to execute this instructions: `/app`
- Inside this work directory:
  - Create a `shared_data` subdirectory `/app/shared_data/`
    - The `airshow.mp4` file must be stored inside this directory
  - Create a `secrets` subdirectory `/app/secrets`
  - Create the text file: `/app/secrets/config.ini`
    - Place the following content inside this file
    ```ini
    [postgres]
    host=postgres
    database=videodb
    user=videodb-user
    password=videodb-password
    ```
    The `user`, `database`, and `password` can be changed as desired.  
  - Create the text file: `/app/secrets/POSTGRES_PASSWORD`
    - Write the same password from `/app/secrets/config.ini` inside this file.
    - If using the data shown here, the content of this file must be:
    ```
    videodb-password
    ```

    Otherwise, adjust accordingly
    >Note: Following best practices, sensitive data MUST NOT be hard coded and much less 
    versioned with the rest of the code. Thus, this manual approach works for demonstration
    purposes only. Ideally, these parameters would be loaded at runtime from an encrypted 
    storage such as `AWS Secrets Manager`, `Azure Key Vault`, `Kubernetes Secrets`, or similar tools


## Execution Instructions
1. `cd` to the work directory mentioned in the requirements
1. Clone this repository
1. Launch the `PostgreSQL` container
    ```bash
    docker-compose up -d
    ```
1. `cd` into the app directory
1. Create the `Docker` image for this application
    ``` bash
    docker build -t cm-solution .
    ``` 
1. Launch the image
```
docker run -it -v $(pwd)/shared_data:/app/data -v $(pwd)/secrets:/app/secrets --network repo_cluster cm-solution python main.py /app/data/airshow.mp4
```

### Please note

Some basic elements, such as the `data base`, and the `user` for this database 
will be created at launch time of the `PostgreSQL` instance. However, the table
for the application is not created at this time.

To validate this, you could log into the Postgres instance and query the postgres server
directly
