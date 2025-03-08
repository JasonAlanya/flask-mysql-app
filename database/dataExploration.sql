-- Number of employees hired for each job and department in 2021 divided by quarter. The
-- table must be ordered alphabetically by department and job.

SELECT 
    d.department, 
    j.job, 
    SUM(CASE WHEN QUARTER(DATE(he.datetime)) = 1 THEN 1 ELSE 0 END) AS Q1,
    SUM(CASE WHEN QUARTER(DATE(he.datetime)) = 2 THEN 1 ELSE 0 END) AS Q2,
    SUM(CASE WHEN QUARTER(DATE(he.datetime)) = 3 THEN 1 ELSE 0 END) AS Q3,
    SUM(CASE WHEN QUARTER(DATE(he.datetime)) = 4 THEN 1 ELSE 0 END) AS Q4
FROM hired_employees he
JOIN departments d ON he.department_id = d.id
JOIN jobs j ON he.job_id = j.id
WHERE YEAR(DATE(he.datetime)) = 2021
GROUP BY d.department, j.job
ORDER BY d.department ASC, j.job ASC;

-- List of ids, name and number of employees hired of each department that hired more
-- employees than the mean of employees hired in 2021 for all the departments, ordered
-- by the number of employees hired (descending).
WITH department_hiring AS (
    SELECT 
        d.id, 
        d.department, 
        COUNT(he.id) AS hired
    FROM hired_employees he
    JOIN departments d ON he.department_id = d.id
    WHERE YEAR(DATE(he.datetime)) = 2021
    GROUP BY d.id, d.department
), hiring_avg AS (
    SELECT 
		AVG(hired) AS avg_hired 
    FROM department_hiring
)
SELECT 
    dh.id, 
    dh.department, 
    dh.hired
FROM department_hiring dh
WHERE hired > (SELECT avg_hired FROM hiring_avg)
ORDER BY hired DESC;
