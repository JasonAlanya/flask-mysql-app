CREATE TABLE `jobs` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Id of the job',
  `job` varchar(255) DEFAULT NULL COMMENT 'Name of the job',
  PRIMARY KEY (`id`)
);

CREATE TABLE `departments` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Id of the department',
  `department` varchar(255) DEFAULT NULL COMMENT 'Name of the department',
  PRIMARY KEY (`id`)
);

CREATE TABLE `hired_employees` (
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
)