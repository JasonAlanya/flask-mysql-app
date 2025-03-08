-- Create the database dynamically using environment variables
SET @api_user = IFNULL(NULLIF('{API_USER}', ''), 'api_user');
SET @api_password = IFNULL(NULLIF('{API_PASSWORD}', ''), 'securepassword');

-- Create jobs table
CREATE TABLE
    `jobs` (
        `id` int NOT NULL AUTO_INCREMENT COMMENT 'Id of the job',
        `job` varchar(255) DEFAULT NULL COMMENT 'Name of the job',
        PRIMARY KEY (`id`)
    );

-- Create departments table
CREATE TABLE
    `departments` (
        `id` int NOT NULL AUTO_INCREMENT COMMENT 'Id of the department',
        `department` varchar(255) DEFAULT NULL COMMENT 'Name of the department',
        PRIMARY KEY (`id`)
    );

-- Create hired_employees table
CREATE TABLE
    `hired_employees` (
        `id` int NOT NULL AUTO_INCREMENT COMMENT 'Id of the employee',
        `name` varchar(255) DEFAULT NULL COMMENT 'Name and surname of the employee',
        `datetime` varchar(25) DEFAULT NULL COMMENT 'Hire datetime in ISO format',
        `department_id` int DEFAULT NULL COMMENT 'Id of the department which the employee was hired for',
        `job_id` int DEFAULT NULL COMMENT 'Id of the job which the employee was hired for',
        PRIMARY KEY (`id`),
        KEY `department_id_idx` (`department_id`),
        KEY `job_id_idx` (`job_id`),
        CONSTRAINT `department_id` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`),
        CONSTRAINT `job_id` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`)
    );

DELIMITER / /
-- Stored procedure to retrieve employees hired per quarter in 2021
CREATE PROCEDURE GetHiredPerQuarter () BEGIN
SELECT
    d.department,
    j.job,
    SUM(
        CASE
            WHEN QUARTER (he.datetime) = 1 THEN 1
            ELSE 0
        END
    ) AS Q1,
    SUM(
        CASE
            WHEN QUARTER (he.datetime) = 2 THEN 1
            ELSE 0
        END
    ) AS Q2,
    SUM(
        CASE
            WHEN QUARTER (he.datetime) = 3 THEN 1
            ELSE 0
        END
    ) AS Q3,
    SUM(
        CASE
            WHEN QUARTER (he.datetime) = 4 THEN 1
            ELSE 0
        END
    ) AS Q4
FROM
    hired_employees he
    JOIN departments d ON he.department_id = d.id
    JOIN jobs j ON he.job_id = j.id
WHERE
    YEAR (he.datetime) = 2021
GROUP BY
    d.department,
    j.job
ORDER BY
    d.department ASC,
    j.job ASC;

END / /
-- Stored procedure to retrieve departments that hired more employees than the average in 2021
CREATE PROCEDURE GetDepartmentsAboveAvg () BEGIN
WITH
    department_hiring AS (
        SELECT
            d.id,
            d.department,
            COUNT(he.id) AS hired
        FROM
            hired_employees he
            JOIN departments d ON he.department_id = d.id
        WHERE
            YEAR (he.datetime) = 2021
        GROUP BY
            d.id,
            d.department
    ),
    hiring_avg AS (
        SELECT
            AVG(hired) AS avg_hired
        FROM
            department_hiring
    )
SELECT
    dh.id,
    dh.department,
    dh.hired
FROM
    department_hiring dh
WHERE
    hired > (
        SELECT
            avg_hired
        FROM
            hiring_avg
    )
ORDER BY
    hired DESC;

END / /
-- Stored procedure to insert data into jobs table
CREATE PROCEDURE InsertJob (IN job_id INT, IN job_name VARCHAR(255)) BEGIN
INSERT INTO
    jobs (id, job)
VALUES
    (job_id, job_name);

END / /
-- Stored procedure to insert data into departments table
CREATE PROCEDURE InsertDepartment (
    IN department_id INT,
    IN department_name VARCHAR(255)
) BEGIN
INSERT INTO
    departments (id, department)
VALUES
    (department_id, department_name);

END / /
-- Stored procedure to insert a single hired employee
CREATE PROCEDURE InsertHiredEmployee (
    IN employee_id INT,
    IN employee_name VARCHAR(255),
    IN employee_datetime varchar(25),
    IN department_id INT,
    IN job_id INT
) BEGIN
INSERT INTO
    hired_employees (id, name, datetime, department_id, job_id)
VALUES
    (
        employee_id,
        employee_name,
        employee_datetime,
        department_id,
        job_id
    );

END / / 

DELIMITER ;

-- Create a restricted user for the API using environment variables
SET @create_user = CONCAT('CREATE USER IF NOT EXISTS ''', @api_user, '''@''%'' IDENTIFIED BY ''', @api_password, '''');
PREPARE stmt FROM @create_user;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

FLUSH PRIVILEGES;
