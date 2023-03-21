-- create database hbnb_test_db if it does not exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- create user hbnb_test in localhost if it does not exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- grant user hbnb_test all privilleges on hbnb_test_db database only
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- grant user hbnb_test SELECT privileges on performance_schema database only
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
