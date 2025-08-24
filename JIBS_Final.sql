-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema JIBS
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema JIBS
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `JIBS` DEFAULT CHARACTER SET utf8 ;
USE `JIBS` ;

-- -----------------------------------------------------
-- Table `JIBS`.`Product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `JIBS`.`Product` (
  `Product_ID` VARCHAR(20) NOT NULL,
  `Product_Name` VARCHAR(50) NOT NULL,
  `Product_Material` VARCHAR(45) NOT NULL,
  `Net_Wt` INT NOT NULL,
  `Gold_Wt` INT NULL,
  `Gold_Crt` INT NOT NULL,
  `Silver_Wt` INT NULL,
  `Diamond_Crt` INT NULL,
  `Diamond_Cost` INT NULL,
  `Making_Charge` INT NOT NULL,
  `Total_Price` INT NOT NULL,
  PRIMARY KEY (`Product_ID`),
  UNIQUE INDEX `Product_ID_UNIQUE` (`Product_ID` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `JIBS`.`Customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `JIBS`.`Customer` (
  `Customer_ID` VARCHAR(20) NOT NULL,
  `Customer_Name` VARCHAR(60) NOT NULL,
  `Cust_PhoneNo` BIGINT(10)NOT NULL,
  `Cust_Email` VARCHAR(45) NOT NULL,
  `Cust_Address` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`Customer_ID`),
  UNIQUE INDEX `Customer_ID_UNIQUE` (`Customer_ID` ASC) VISIBLE,
  UNIQUE INDEX `Cust_PhoneNo_UNIQUE` (`Cust_PhoneNo` ASC) VISIBLE,
  UNIQUE INDEX `Cust_Email_UNIQUE` (`Cust_Email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `JIBS`.`Payment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `JIBS`.`Payment` (
  `Payment_ID` VARCHAR(20) NOT NULL,
  `Payment_Date` DATE NOT NULL,
  `Payment_Amount` INT NOT NULL,
  `Payment_Type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Payment_ID`),
  UNIQUE INDEX `Payment_ID_UNIQUE` (`Payment_ID` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `JIBS`.`Supplier`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `JIBS`.`Supplier` (
  `Supplier_ID` VARCHAR(20) NOT NULL,
  `Supplier_Name` VARCHAR(45) NOT NULL,
  `Supplier_PhoneNo` BIGINT(10) NOT NULL,
  `Supplier_Address` VARCHAR(100) NOT NULL,
  `Supplier_Email` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `Supplier_ID_UNIQUE` (`Supplier_ID` ASC) VISIBLE,
  PRIMARY KEY (`Supplier_ID`),
  UNIQUE INDEX `Supplier_PhoneNo_UNIQUE` (`Supplier_PhoneNo` ASC) VISIBLE,
  UNIQUE INDEX `Supplier_Email_UNIQUE` (`Supplier_Email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `JIBS`.`Login`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `JIBS`.`Login` (
  `UserName` VARCHAR(50) NOT NULL,
  `Password` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `UserName_UNIQUE` (`UserName` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `JIBS`.`Purchase`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `JIBS`.`Purchase` (
  `Product_ID` VARCHAR(20) NOT NULL,
  `Customer_ID` VARCHAR(20) NOT NULL,
  `Payment_ID` VARCHAR(20) NOT NULL,
  `Purchase_Date` DATE NOT NULL,
  `Bill_Amount` FLOAT NOT NULL,
  `Bill_ID` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`Bill_ID`),
  INDEX `proid_idx` (`Product_ID` ASC) VISIBLE,
  INDEX `payid_idx` (`Payment_ID` ASC) VISIBLE,
  INDEX `custid_idx` (`Customer_ID` ASC) VISIBLE,
  UNIQUE INDEX `Bill_ID_UNIQUE` (`Bill_ID` ASC) VISIBLE,
  UNIQUE INDEX `Product_ID_UNIQUE` (`Product_ID` ASC) VISIBLE,
  UNIQUE INDEX `Customer_ID_UNIQUE` (`Customer_ID` ASC) VISIBLE,
  UNIQUE INDEX `Payment_ID_UNIQUE` (`Payment_ID` ASC) VISIBLE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `JIBS`.`Employee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `JIBS`.`Employee` (
  `Employee_ID` VARCHAR(45) NOT NULL,
  `Employee_Name` VARCHAR(45) NOT NULL,
  `UserName` VARCHAR(45) NOT NULL,
  `Employee_PhoneNo` BIGINT(10) NOT NULL,
  `Employee_Email` VARCHAR(45) NOT NULL,
  `Employee_Address` VARCHAR(70) NOT NULL,
  `Employee_Type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Employee_ID`),
  INDEX `userlog_idx` (`UserName` ASC) VISIBLE,
  UNIQUE INDEX `UserName_UNIQUE` (`UserName` ASC) VISIBLE,
  UNIQUE INDEX `Employee_ID_UNIQUE` (`Employee_ID` ASC) VISIBLE,
  UNIQUE INDEX `Employee_Email_UNIQUE` (`Employee_Email` ASC) VISIBLE,
  UNIQUE INDEX `Employee_PhoneNo_UNIQUE` (`Employee_PhoneNo` ASC) VISIBLE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `JIBS`.`Inventory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `JIBS`.`Inventory` (
  `Product_Id` VARCHAR(20) NOT NULL,
  `Product_Quantity` INT NOT NULL,
  `Supplier_Id` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`Product_Id`),
  UNIQUE INDEX `Product_Id_UNIQUE` (`Product_Id` ASC) VISIBLE)
ENGINE = InnoDB;

DELIMITER //

CREATE TRIGGER update_inventory_quantity AFTER INSERT ON Purchase
FOR EACH ROW
BEGIN
  UPDATE Inventory
  SET Product_Quantity = Product_Quantity - 1
  WHERE Product_Id = NEW.Product_ID;
END;//

DELIMITER //

CREATE TRIGGER calculate_total_price BEFORE UPDATE ON Product
FOR EACH ROW
BEGIN
  SET NEW.Total_Price = (NEW.Net_Wt * NEW.Making_Charge) + (NEW.Gold_Wt * NEW.Gold_Crt) + (NEW.Silver_Wt * NEW.Diamond_Crt) + NEW.Diamond_Cost;
END;//

DELIMITER //

CREATE PROCEDURE GetSupplierDetails(IN supplierID VARCHAR(20))
BEGIN
    SELECT * FROM Supplier WHERE Supplier_ID = supplierID;
END;//

DELIMITER //

CREATE PROCEDURE GetPaymentDetails(IN paymentID VARCHAR(20))
BEGIN
    SELECT * FROM Payment WHERE Payment_ID = paymentID;
END;//

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;