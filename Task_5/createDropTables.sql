-- Declare database name
-- DECLARE @databasename AS VARCHAR(100)='task_5'
-- 
-- Declare  table name to be created
-- DECLARE @createtable AS VARCHAR(100)='rawdata'
-- 
-- Declare  table name to be deleted
-- DECLARE @droptable AS VARCHAR(100)='rawdata'
-- 
-- Insert value 
-- DECLARE @insertValue AS INT = 11
-- 
-- Update a value
-- DECLARE @updateValue AS INT = 9
-- 

USE task_5

-- This is to create a table on the database
CREATE TABLE `task_5`.`rawdata` (
  `idrawdata` INT NOT NULL,
  PRIMARY KEY (`idrawdata`));

-- This is to drop a table from the database called tobedeletedtable
DROP TABLE `task_5`.`tobedeletedtable`;


-- THis is to Insert a value in a database
INSERT INTO `task_5`.`rawdata` (`idrawdata`) VALUES ('11');


-- This is to Update a value in a database
UPDATE `task_5`.`rawdata` SET `idrawdata` = '5' WHERE (`idrawdata` = '10');
