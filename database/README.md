# Database Setup Guide

## Overview
This setup containerizes and start a MySQL 8.0 database with predefined tables and views for managing employee records. The database is dynamically configured using environment variables.

## Folder Structure
```
database/
┣ mysql-init/
┃ ┗ init.sql           # SQL script to create tables and stored procedures
┣ .env                 # Environment variables file
┣ dockerEntrypoint.sh  # Custom entrypoint script for MySQL container
┣ dockerfile           # Dockerfile to build the MySQL image
┗ README.md            # Documentation
```

## Environment Variables (.env)
Configure the following variables in the `.env` file:
```
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=companydb
API_USER=api_user
API_PASSWORD=securepassword
```
An example is provided in `.env.example`.

## Building the Docker Image
Run the following command to build the MySQL image:
```sh
docker build -t my-company-db .
```

## Running the MySQL Container
Start the container using the environment variables from `.env`:
```sh
docker run --name mysql-container --env-file .env -p 3306:3306 -d my-company-db
```

## How It Works
1. The **Dockerfile** copies the initialization script and sets up a custom entrypoint.
2. The **dockerEntrypoint.sh** script:
   - Starts MySQL in the background.
   - Waits until MySQL is ready.
   - Replaces placeholders in `init.sql` with environment variables.
   - Executes `init.sql` to create tables, stored procedures, and a restricted API user.
3. The container remains running with MySQL fully initialized.
