# Database Setup Guide

## Setting Up the Database Using MySQL Workbench

### 1. Install MySQL Workbench
- Download MySQL Workbench from the official website: [MySQL Download](https://dev.mysql.com/downloads/installer/)
- Follow the installation steps based on your operating system.

### 2. Create the Database
1. Open MySQL Workbench and connect to your MySQL server.
2. Click on the "SQL Editor" to open a new query tab.
3. Run the following SQL command to create the database if needed:
   ```sql
   CREATE DATABASE company_db;
   USE company_db;
   ```

### 3. Execute the Schema
1. In MySQL Workbench, open the `schema.sql` file.
2. Ensure that the "company_db" database is selected.
3. Click on the "Execute" button to run the script and create the tables.

Once executed, your database will be set up and ready for use!

