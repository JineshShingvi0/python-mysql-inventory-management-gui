-- MySQL dump 10.13  Distrib 8.4.11, for Linux (x86_64)
--
-- Host: localhost    Database: inventory_management
-- ------------------------------------------------------
-- Server version	8.4.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `loyalty_points` int DEFAULT '0',
  `total_spent` decimal(10,2) DEFAULT '0.00',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Jinesh','9881353338','jinesh@gmail.com','Kondhwa',190,0.00,'2026-08-21 10:59:38'),(4,'Priya','9087654321','priya@example.com','Mukund Nagar',25,0.00,'2026-08-21 13:13:04'),(5,'Yogita','8237309256','yogita@gmail.com','Salisbury Park',76,0.00,'2026-08-21 13:45:53'),(6,'Vibha','9850955458','vibha@gmail.com','Salisbury Park',2,0.00,'2026-08-21 13:46:25'),(7,'Aditya','9881353339','aditya@gmail.com','Viman Nagar',14,0.00,'2026-08-21 13:47:05'),(8,'Bhavya','9881353331','bhavya@gmail.com','Lullanagar',42,0.00,'2026-08-21 13:47:31'),(9,'Devansh','9881353332','Devansh@gmail.com','kondhwa',6,0.00,'2026-08-21 13:52:30'),(10,'Krish','9881353333','krish@gmail.com','Gangadham',33,0.00,'2026-08-21 13:52:57'),(11,'Ram','8237309257',NULL,NULL,2,0.00,'2026-08-22 17:23:33'),(12,'Kalyan','9870654321',NULL,NULL,3,0.00,'2026-08-26 05:39:22'),(13,'Darshan','9881352226',NULL,NULL,0,0.00,'2026-08-26 05:45:54'),(14,'Pranav','9807654321',NULL,NULL,0,0.00,'2026-08-26 06:16:51');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `barcode` varchar(50) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `purchase_price` decimal(10,2) NOT NULL,
  `selling_price` decimal(10,2) NOT NULL,
  `stock` int NOT NULL DEFAULT '0',
  `minimum_stock` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `barcode` (`barcode`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'890100000001','sunflower oil','oil',175.00,300.00,105,10),(2,'290000000002','groundnut oil','oil',150.00,250.00,81,10),(3,'290000000003','men\'s tshirt','clothing',175.00,350.00,45,10),(4,'290000000004','balaji wafers','snacks',7.00,10.00,60,5),(5,'290000000005','dairy milk chocolate','snacks',50.00,75.00,105,10),(6,'290000000006','rice','grocery',40.00,150.00,117,10),(8,'890100000003','water bottles','grocery',4.00,10.00,96,10),(9,'290000000009','cow milk','grocery',30.00,39.00,47,5);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchases`
--

DROP TABLE IF EXISTS `purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchases` (
  `purchase_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `supplier` varchar(150) DEFAULT NULL,
  `quantity` int NOT NULL,
  `purchase_price` decimal(10,2) NOT NULL,
  `total_cost` decimal(10,2) NOT NULL,
  `purchase_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`purchase_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchases`
--

LOCK TABLES `purchases` WRITE;
/*!40000 ALTER TABLE `purchases` DISABLE KEYS */;
INSERT INTO `purchases` VALUES (1,1,'Test Supplier',10,150.00,1500.00,'2026-08-25 17:37:08'),(2,5,'Dairy Milk Company',100,7.00,700.00,'2026-08-26 06:01:07');
/*!40000 ALTER TABLE `purchases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `returns`
--

DROP TABLE IF EXISTS `returns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `returns` (
  `return_id` int NOT NULL AUTO_INCREMENT,
  `sale_id` int NOT NULL,
  `sale_item_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `refund_amount` decimal(10,2) NOT NULL,
  `return_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`return_id`),
  KEY `sale_id` (`sale_id`),
  KEY `sale_item_id` (`sale_item_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `returns_ibfk_1` FOREIGN KEY (`sale_id`) REFERENCES `sales` (`sale_id`),
  CONSTRAINT `returns_ibfk_2` FOREIGN KEY (`sale_item_id`) REFERENCES `sale_items` (`sale_item_id`),
  CONSTRAINT `returns_ibfk_3` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `returns`
--

LOCK TABLES `returns` WRITE;
/*!40000 ALTER TABLE `returns` DISABLE KEYS */;
INSERT INTO `returns` VALUES (1,3,5,4,2,20.00,'2026-08-25 16:41:47'),(2,15,29,8,2,20.00,'2026-08-25 16:42:26'),(3,16,32,3,3,1050.00,'2026-08-25 16:43:49'),(4,16,30,2,1,250.00,'2026-08-25 17:05:19');
/*!40000 ALTER TABLE `returns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sale_items`
--

DROP TABLE IF EXISTS `sale_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sale_items` (
  `sale_item_id` int NOT NULL AUTO_INCREMENT,
  `sale_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `selling_price` decimal(10,2) NOT NULL,
  `purchase_price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`sale_item_id`),
  KEY `sale_id` (`sale_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `sale_items_ibfk_1` FOREIGN KEY (`sale_id`) REFERENCES `sales` (`sale_id`),
  CONSTRAINT `sale_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale_items`
--

LOCK TABLES `sale_items` WRITE;
/*!40000 ALTER TABLE `sale_items` DISABLE KEYS */;
INSERT INTO `sale_items` VALUES (1,1,3,10,350.00,0.00,3500.00),(2,1,2,10,250.00,0.00,2500.00),(3,2,4,1,10.00,0.00,10.00),(4,2,5,10,75.00,0.00,750.00),(5,3,4,23,10.00,0.00,230.00),(6,4,3,5,350.00,0.00,1750.00),(7,5,5,9,75.00,0.00,675.00),(8,5,2,5,250.00,0.00,1250.00),(9,6,2,1,250.00,0.00,250.00),(10,7,4,1,10.00,0.00,10.00),(11,8,4,1,10.00,0.00,10.00),(12,8,5,2,75.00,0.00,150.00),(13,8,3,2,350.00,0.00,700.00),(14,8,6,1,150.00,0.00,150.00),(15,8,1,1,300.00,0.00,300.00),(16,9,4,1,10.00,0.00,10.00),(17,9,5,2,75.00,0.00,150.00),(18,9,3,1,350.00,0.00,350.00),(19,10,4,10,10.00,0.00,100.00),(20,10,2,10,250.00,0.00,2500.00),(21,10,3,5,350.00,0.00,1750.00),(22,11,4,13,10.00,0.00,130.00),(23,12,6,2,150.00,0.00,300.00),(24,13,1,2,300.00,0.00,600.00),(25,13,3,10,350.00,0.00,3500.00),(26,14,4,5,10.00,0.00,50.00),(27,14,1,2,300.00,0.00,600.00),(28,14,2,1,250.00,0.00,250.00),(29,15,8,4,10.00,0.00,40.00),(30,16,2,3,250.00,0.00,750.00),(31,16,8,2,10.00,0.00,20.00),(32,16,3,5,350.00,0.00,1750.00),(33,17,9,3,39.00,0.00,117.00),(34,17,5,2,75.00,0.00,150.00),(35,18,4,1,10.00,0.00,10.00),(36,19,4,1,10.00,7.00,10.00);
/*!40000 ALTER TABLE `sale_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales` (
  `sale_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int DEFAULT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `gst_amount` decimal(10,2) DEFAULT '0.00',
  `discount_amount` decimal(10,2) DEFAULT '0.00',
  `payment_method` varchar(20) NOT NULL,
  `sale_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sale_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--

LOCK TABLES `sales` WRITE;
/*!40000 ALTER TABLE `sales` DISABLE KEYS */;
INSERT INTO `sales` VALUES (1,1,6372.00,972.00,600.00,'Card','2026-08-22 08:47:51'),(2,8,896.80,136.80,0.00,'Cash','2026-08-22 08:59:53'),(3,7,271.40,41.40,0.00,'Cash','2026-08-22 16:39:47'),(4,8,2065.00,315.00,0.00,'UPI','2026-08-22 16:43:08'),(5,1,2157.93,329.18,96.25,'UPI','2026-08-22 17:23:04'),(6,11,295.00,45.00,0.00,'Cash','2026-08-22 17:23:33'),(7,1,11.80,1.80,0.00,'Cash','2026-08-23 05:02:48'),(8,1,1545.80,235.80,0.00,'Cash','2026-08-23 05:37:23'),(9,1,571.71,87.21,25.50,'Cash','2026-08-24 06:41:00'),(10,1,5133.00,783.00,0.00,'Cash','2026-08-24 06:52:57'),(11,8,153.40,23.40,0.00,'Cash','2026-08-24 07:00:01'),(12,10,354.00,54.00,0.00,'UPI','2026-08-24 08:06:20'),(13,5,4838.00,738.00,0.00,'Card','2026-08-24 08:21:46'),(14,10,1062.00,162.00,0.00,'Cash','2026-08-24 12:19:35'),(15,7,47.20,7.20,0.00,'Cash','2026-08-24 14:47:57'),(16,5,2824.92,430.92,126.00,'Cash','2026-08-24 18:49:53'),(17,12,315.06,48.06,0.00,'UPI','2026-08-26 05:39:22'),(18,13,11.80,1.80,0.00,'Cash','2026-08-26 05:45:54'),(19,14,11.80,1.80,0.00,'UPI','2026-08-26 06:16:51');
/*!40000 ALTER TABLE `sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_movements`
--

DROP TABLE IF EXISTS `stock_movements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_movements` (
  `movement_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `movement_type` varchar(20) NOT NULL,
  `quantity` int NOT NULL,
  `stock_after` int NOT NULL,
  `movement_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`movement_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `stock_movements_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_movements`
--

LOCK TABLES `stock_movements` WRITE;
/*!40000 ALTER TABLE `stock_movements` DISABLE KEYS */;
INSERT INTO `stock_movements` VALUES (1,2,'STOCK IN',50,100,'2026-08-22 08:47:12'),(2,3,'SALE',10,70,'2026-08-22 08:47:51'),(3,2,'SALE',10,90,'2026-08-22 08:47:51'),(4,4,'SALE',1,24,'2026-08-22 08:59:53'),(5,5,'SALE',10,20,'2026-08-22 08:59:53'),(6,2,'STOCK IN',10,100,'2026-08-22 16:39:21'),(7,4,'SALE',23,1,'2026-08-22 16:39:48'),(8,3,'SALE',5,65,'2026-08-22 16:43:08'),(9,4,'STOCK IN',90,91,'2026-08-22 17:21:35'),(10,5,'SALE',9,11,'2026-08-22 17:23:04'),(11,2,'SALE',5,95,'2026-08-22 17:23:04'),(12,2,'SALE',1,94,'2026-08-22 17:23:33'),(13,4,'SALE',1,90,'2026-08-23 05:02:48'),(14,4,'SALE',1,89,'2026-08-23 05:37:23'),(15,5,'SALE',2,9,'2026-08-23 05:37:23'),(16,3,'SALE',2,63,'2026-08-23 05:37:23'),(17,6,'SALE',1,119,'2026-08-23 05:37:23'),(18,1,'SALE',1,99,'2026-08-23 05:37:23'),(19,4,'SALE',1,88,'2026-08-24 06:41:00'),(20,5,'SALE',2,7,'2026-08-24 06:41:00'),(21,3,'SALE',1,62,'2026-08-24 06:41:00'),(22,4,'SALE',10,78,'2026-08-24 06:52:57'),(23,2,'SALE',10,84,'2026-08-24 06:52:57'),(24,3,'SALE',5,57,'2026-08-24 06:52:57'),(25,4,'SALE',13,65,'2026-08-24 07:00:01'),(26,6,'SALE',2,117,'2026-08-24 08:06:20'),(27,1,'SALE',2,97,'2026-08-24 08:21:46'),(28,3,'SALE',10,47,'2026-08-24 08:21:46'),(29,4,'SALE',5,60,'2026-08-24 12:19:35'),(30,1,'SALE',2,95,'2026-08-24 12:19:35'),(31,2,'SALE',1,83,'2026-08-24 12:19:35'),(32,8,'SALE',4,96,'2026-08-24 14:47:57'),(33,2,'SALE',3,80,'2026-08-24 18:49:54'),(34,8,'SALE',2,94,'2026-08-24 18:49:54'),(35,3,'SALE',5,42,'2026-08-24 18:49:54'),(36,2,'RETURN',1,81,'2026-08-25 17:05:19'),(37,1,'STOCK IN',10,105,'2026-08-25 17:37:08'),(38,9,'SALE',3,47,'2026-08-26 05:39:22'),(39,5,'SALE',2,5,'2026-08-26 05:39:22'),(40,4,'SALE',1,61,'2026-08-26 05:45:54'),(41,5,'STOCK IN',100,105,'2026-08-26 06:01:07'),(42,4,'SALE',1,60,'2026-08-26 06:16:51');
/*!40000 ALTER TABLE `stock_movements` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-26 11:57:30
