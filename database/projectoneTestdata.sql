CREATE DATABASE  IF NOT EXISTS `projectone` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `projectone`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: projectone
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actions`
--

DROP TABLE IF EXISTS `actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` int NOT NULL,
  `description` text NOT NULL,
  `parameters` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `actions_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actions`
--

LOCK TABLES `actions` WRITE;
/*!40000 ALTER TABLE `actions` DISABLE KEYS */;
INSERT INTO `actions` VALUES (1,1,'Piezo electric 1 action','{\"parameter1\": \"value1\"}'),(2,2,'Piezo electric 2 action','{\"parameter2\": \"value2\"}'),(3,3,'Piezo electric 3 action','{\"parameter3\": \"value3\"}'),(4,4,'Piezo electric 4 action','{\"parameter4\": \"value4\"}'),(5,5,'Rotary encoder action','{\"parameter5\": \"value5\"}'),(6,6,'Button 1 action','{\"parameter6\": \"value6\"}'),(7,7,'Button 2 action','{\"parameter7\": \"value7\"}'),(8,8,'LED 1 action','{\"parameter8\": \"value8\"}'),(9,9,'LED 2 action','{\"parameter9\": \"value9\"}'),(10,10,'OLED action','{\"parameter10\": \"value10\"}'),(11,11,'4x7segment display action','{\"parameter11\": \"value11\"}'),(12,12,'Piezo buzzer action','{\"parameter12\": \"value12\"}');
/*!40000 ALTER TABLE `actions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(50) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
INSERT INTO `devices` VALUES (1,'piezo1','piezo','Piezo electric 1'),(2,'piezo2','piezo','Piezo electric 2'),(3,'piezo3','piezo','Piezo electric 3'),(4,'piezo4','piezo','Piezo electric 4'),(5,'encoder1','encoder','Rotary encoder'),(6,'button1','button','Button 1'),(7,'button2','button','Button 2'),(8,'led1','led','LED 1'),(9,'led2','led','LED 2'),(10,'oled','oled','OLED display'),(11,'display','display','4x7segment display'),(12,'buzzer','buzzer','Piezo buzzer');
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `history`
--

DROP TABLE IF EXISTS `history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_id` int NOT NULL,
  `session_id` int DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `action_id` (`action_id`),
  KEY `session_id` (`session_id`),
  CONSTRAINT `history_ibfk_1` FOREIGN KEY (`action_id`) REFERENCES `actions` (`id`),
  CONSTRAINT `history_ibfk_2` FOREIGN KEY (`session_id`) REFERENCES `sessions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history`
--

LOCK TABLES `history` WRITE;
/*!40000 ALTER TABLE `history` DISABLE KEYS */;
INSERT INTO `history` VALUES (1,1,1,'2024-05-27 08:05:00'),(2,2,1,'2024-05-27 08:10:00'),(3,3,2,'2024-05-27 09:05:00'),(4,4,2,'2024-05-27 09:10:00'),(5,5,3,'2024-05-27 10:05:00'),(6,6,4,'2024-05-27 11:05:00'),(7,7,4,'2024-05-27 11:10:00'),(8,8,5,'2024-05-27 12:05:00'),(9,9,5,'2024-05-27 12:10:00'),(10,10,6,'2024-05-27 13:05:00'),(11,11,7,'2024-05-27 14:05:00'),(12,12,7,'2024-05-27 14:10:00'),(13,1,8,'2024-05-27 15:05:00'),(14,2,8,'2024-05-27 15:10:00'),(15,3,9,'2024-05-27 16:05:00'),(16,4,9,'2024-05-27 16:10:00'),(17,5,10,'2024-05-27 17:05:00'),(18,6,11,'2024-05-27 08:05:00'),(19,7,11,'2024-05-27 08:10:00'),(20,8,12,'2024-05-27 09:05:00'),(21,9,12,'2024-05-27 09:10:00'),(22,10,13,'2024-05-27 10:05:00'),(23,11,14,'2024-05-27 11:05:00'),(24,12,14,'2024-05-27 11:10:00'),(25,1,15,'2024-05-27 12:05:00'),(26,2,15,'2024-05-27 12:10:00'),(27,3,16,'2024-05-27 13:05:00'),(28,4,17,'2024-05-27 14:05:00'),(29,5,17,'2024-05-27 14:10:00'),(30,6,18,'2024-05-27 15:05:00'),(31,7,18,'2024-05-27 15:10:00'),(32,8,19,'2024-05-27 16:05:00'),(33,9,20,'2024-05-27 17:05:00'),(34,10,21,'2024-05-28 08:05:00'),(35,11,21,'2024-05-28 08:10:00'),(36,12,22,'2024-05-28 09:05:00'),(37,1,22,'2024-05-28 09:10:00'),(38,2,23,'2024-05-28 10:05:00'),(39,3,24,'2024-05-28 11:05:00'),(40,4,25,'2024-05-28 12:05:00'),(41,5,25,'2024-05-28 12:10:00'),(42,6,26,'2024-05-28 13:05:00'),(43,7,27,'2024-05-28 14:05:00'),(44,8,27,'2024-05-28 14:10:00'),(45,9,28,'2024-05-28 15:05:00'),(46,10,29,'2024-05-28 16:05:00'),(47,11,30,'2024-05-28 17:05:00');
/*!40000 ALTER TABLE `history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `training_scheme_id` int NOT NULL,
  `start_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `end_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `training_scheme_id` (`training_scheme_id`),
  CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `sessions_ibfk_2` FOREIGN KEY (`training_scheme_id`) REFERENCES `trainingschemes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
INSERT INTO `sessions` VALUES (1,1,1,'2024-05-27 08:00:00','2024-05-27 09:00:00'),(2,1,2,'2024-05-27 09:00:00','2024-05-27 10:00:00'),(3,2,1,'2024-05-27 10:00:00','2024-05-27 11:00:00'),(4,2,2,'2024-05-27 11:00:00','2024-05-27 12:00:00'),(5,3,1,'2024-05-27 12:00:00','2024-05-27 13:00:00'),(6,3,2,'2024-05-27 13:00:00','2024-05-27 14:00:00'),(7,4,1,'2024-05-27 14:00:00','2024-05-27 15:00:00'),(8,4,2,'2024-05-27 15:00:00','2024-05-27 16:00:00'),(9,5,1,'2024-05-27 16:00:00','2024-05-27 17:00:00'),(10,5,2,'2024-05-27 17:00:00','2024-05-27 18:00:00'),(11,1,1,'2024-05-28 08:00:00','2024-05-28 09:00:00'),(12,1,2,'2024-05-28 09:00:00','2024-05-28 10:00:00'),(13,2,1,'2024-05-28 10:00:00','2024-05-28 11:00:00'),(14,2,2,'2024-05-28 11:00:00','2024-05-28 12:00:00'),(15,3,1,'2024-05-28 12:00:00','2024-05-28 13:00:00'),(16,3,2,'2024-05-28 13:00:00','2024-05-28 14:00:00'),(17,4,1,'2024-05-28 14:00:00','2024-05-28 15:00:00'),(18,4,2,'2024-05-28 15:00:00','2024-05-28 16:00:00'),(19,5,1,'2024-05-28 16:00:00','2024-05-28 17:00:00'),(20,5,2,'2024-05-28 17:00:00','2024-05-28 18:00:00'),(21,1,1,'2024-05-29 08:00:00','2024-05-29 09:00:00'),(22,1,2,'2024-05-29 09:00:00','2024-05-29 10:00:00'),(23,2,1,'2024-05-29 10:00:00','2024-05-29 11:00:00'),(24,2,2,'2024-05-29 11:00:00','2024-05-29 12:00:00'),(25,3,1,'2024-05-29 12:00:00','2024-05-29 13:00:00'),(26,3,2,'2024-05-29 13:00:00','2024-05-29 14:00:00'),(27,4,1,'2024-05-29 14:00:00','2024-05-29 15:00:00'),(28,4,2,'2024-05-29 15:00:00','2024-05-29 16:00:00'),(29,5,1,'2024-05-29 16:00:00','2024-05-29 17:00:00'),(30,5,2,'2024-05-29 17:00:00','2024-05-29 18:00:00');
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trainingschemes`
--

DROP TABLE IF EXISTS `trainingschemes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trainingschemes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `sequence` json NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trainingschemes`
--

LOCK TABLES `trainingschemes` WRITE;
/*!40000 ALTER TABLE `trainingschemes` DISABLE KEYS */;
INSERT INTO `trainingschemes` VALUES (1,'Training Scheme 1','Description for Training Scheme 1','{\"sequence1\": \"action1\", \"sequence2\": \"action2\"}'),(2,'Training Scheme 2','Description for Training Scheme 2','{\"sequence1\": \"action3\", \"sequence2\": \"action4\"}');
/*!40000 ALTER TABLE `trainingschemes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'user1','password1'),(2,'user2','password2'),(3,'user3','password3'),(4,'user4','password4'),(5,'user5','password5');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-03 11:16:04
