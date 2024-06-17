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
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actions`
--

LOCK TABLES `actions` WRITE;
/*!40000 ALTER TABLE `actions` DISABLE KEYS */;
INSERT INTO `actions` VALUES (1,'hit','Piezo electric element been hit'),(2,'ledupdate','The leds have been updated'),(3,'startsound','Piezo buzzer played the start sound'),(4,'reloadsound','Piezo buzzer played the reload sound'),(5,'highscoresound','Piezo buzzer played the highscore sound'),(6,'encoderturn','Rotary encoder turned'),(7,'press','Button pressed'),(8,'oledupdate','the OLED display has been updated'),(9,'scoreupdate','4x7segment display has been updated');
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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
INSERT INTO `devices` VALUES (1,'piezoelectric1','sensor','Piezo electric element of target 1'),(2,'piezoelectric2','sensor','Piezo electric element of target 2'),(3,'piezoelectric3','sensor','Piezo electric element of target 3'),(4,'piezoelectric4','sensor','Piezo electric element of target 4'),(5,'piezoelectric5','sensor','Piezo electric element of target 5'),(6,'piezoelectric6','sensor','Piezo electric element of target 6'),(7,'piezoelectric7','sensor','Piezo electric element of target 7'),(8,'piezoelectric8','sensor','Piezo electric element of target 8'),(9,'led1','actuator','LED of target 1'),(10,'led2','actuator','LED of target 2'),(11,'led3','actuator','LED of target 3'),(12,'led4','actuator','LED of target 4'),(13,'led5','actuator','LED of target 5'),(14,'led6','actuator','LED of target 6'),(15,'led7','actuator','LED of target 7'),(16,'led8','actuator','LED of target 8'),(17,'buzzer','actuator','Piezo buzzer'),(18,'scoreboard','display','4x7segment display'),(19,'encoder','sensor','Rotary encoder'),(20,'button1','sensor','Button 1'),(21,'button2','sensor','Button 2'),(22,'oled','display','OLED display');
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
  `device_id` int DEFAULT NULL,
  `action_id` int NOT NULL,
  `parameters` json DEFAULT NULL,
  `session_id` int DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `action_id` (`action_id`),
  KEY `device_id` (`device_id`),
  KEY `session_id` (`session_id`),
  CONSTRAINT `history_ibfk_1` FOREIGN KEY (`action_id`) REFERENCES `actions` (`id`),
  CONSTRAINT `history_ibfk_2` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`),
  CONSTRAINT `history_ibfk_3` FOREIGN KEY (`session_id`) REFERENCES `sessions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history`
--

LOCK TABLES `history` WRITE;
/*!40000 ALTER TABLE `history` DISABLE KEYS */;
-- INSERT INTO `history` VALUES (1,3,9,'{\"volume\": \"high\"}',1,'2024-05-27 08:00:00'),(2,1,1,'{\"force\": \"medium\"}',1,'2024-05-27 08:00:02'),(3,13,10,'{\"score\": \"10\"}',1,'2024-05-27 08:00:03'),(4,2,5,'{\"
-- us\": \"on\"}',1,'2024-05-27 08:00:03'),(5,1,1,'{\"force\": \"high\"}',1,'2024-05-27 08:00:05'),(6,13,10,'{\"score\": \"20\"}',1,'2024-05-27 08:00:06'),(7,2,5,'{\"status\": \"on\"}',1,'2024-05-27 08:00:06'),(8,4,9,'{\"sound\": \"reload\"}',1,'2024-05-27 08:00:08'),(9,1,1,'{\"force\": \"low\"}',1,'2024-05-27 08:00:10'),(10,13,10,'{\"score\": \"30\"}',1,'2024-05-27 08:00:11'),(11,2,5,'{\"status\": \"on\"}',1,'2024-05-27 08:00:11'),(12,5,9,'{\"sound\": \"stop\"}',1,'2024-05-27 09:00:00'),(13,10,12,'{\"state\": \"pressed\"}',NULL,'2024-05-27 09:00:05'),(14,7,11,'{\"direction\": \"left\"}',NULL,'2024-05-27 09:00:10'),(15,8,11,'{\"direction\": \"right\"}',NULL,'2024-05-27 09:00:15'),(16,11,13,'{\"state\": \"pressed\"}',NULL,'2024-05-27 09:00:20'),(17,3,9,'{\"volume\": \"high\"}',2,'2024-05-27 09:00:00'),(18,1,2,'{\"force\": \"medium\"}',2,'2024-05-27 09:00:02'),(19,13,10,'{\"score\": \"10\"}',2,'2024-05-27 09:00:03'),(20,2,6,'{\"status\": \"on\"}',2,'2024-05-27 09:00:03'),(21,1,2,'{\"force\": \"high\"}',2,'2024-05-27 09:00:05'),(22,13,10,'{\"score\": \"20\"}',2,'2024-05-27 09:00:06'),(23,2,6,'{\"status\": \"on\"}',2,'2024-05-27 09:00:06'),(24,4,9,'{\"sound\": \"reload\"}',2,'2024-05-27 09:00:08'),(25,1,2,'{\"force\": \"low\"}',2,'2024-05-27 09:00:10'),(26,13,10,'{\"score\": \"30\"}',2,'2024-05-27 09:00:11'),(27,2,6,'{\"status\": \"on\"}',2,'2024-05-27 09:00:11'),(28,5,9,'{\"sound\": \"stop\"}',2,'2024-05-27 10:00:00'),(29,3,9,'{\"volume\": \"high\"}',3,'2024-05-27 10:00:00'),(30,1,3,'{\"force\": \"medium\"}',3,'2024-05-27 10:00:02'),(31,13,10,'{\"score\": \"10\"}',3,'2024-05-27 10:00:03'),(32,2,7,'{\"status\": \"on\"}',3,'2024-05-27 10:00:03'),(33,1,3,'{\"force\": \"high\"}',3,'2024-05-27 10:00:05'),(34,13,10,'{\"score\": \"20\"}',3,'2024-05-27 10:00:06'),(35,2,7,'{\"status\": \"on\"}',3,'2024-05-27 10:00:06'),(36,4,9,'{\"sound\": \"reload\"}',3,'2024-05-27 10:00:08'),(37,1,3,'{\"force\": \"low\"}',3,'2024-05-27 10:00:10'),(38,13,10,'{\"score\": \"30\"}',3,'2024-05-27 10:00:11'),(39,2,7,'{\"status\": \"on\"}',3,'2024-05-27 10:00:11'),(40,5,9,'{\"sound\": \"stop\"}',3,'2024-05-27 11:00:00'),(41,10,12,'{\"state\": \"pressed\"}',NULL,'2024-05-27 11:00:05'),(42,7,11,'{\"direction\": \"left\"}',NULL,'2024-05-27 11:00:10'),(43,8,11,'{\"direction\": \"right\"}',NULL,'2024-05-27 11:00:15'),(44,11,13,'{\"state\": \"pressed\"}',NULL,'2024-05-27 11:00:20'),(45,3,9,'{\"volume\": \"high\"}',4,'2024-05-27 11:00:00'),(46,1,4,'{\"force\": \"medium\"}',4,'2024-05-27 11:00:02'),(47,13,10,'{\"score\": \"10\"}',4,'2024-05-27 11:00:03'),(48,2,8,'{\"status\": \"on\"}',4,'2024-05-27 11:00:03'),(49,1,4,'{\"force\": \"high\"}',4,'2024-05-27 11:00:05'),(50,13,10,'{\"score\": \"20\"}',4,'2024-05-27 11:00:06'),(51,2,8,'{\"status\": \"on\"}',4,'2024-05-27 11:00:06'),(52,4,9,'{\"sound\": \"reload\"}',4,'2024-05-27 11:00:08'),(53,1,4,'{\"force\": \"low\"}',4,'2024-05-27 11:00:10'),(54,13,10,'{\"score\": \"30\"}',4,'2024-05-27 11:00:11'),(55,2,8,'{\"status\": \"on\"}',4,'2024-05-27 11:00:11'),(56,5,9,'{\"sound\": \"stop\"}',4,'2024-05-27 12:00:00'),(57,3,9,'{\"volume\": \"high\"}',5,'2024-05-27 12:00:00'),(58,1,1,'{\"force\": \"medium\"}',5,'2024-05-27 12:00:02'),(59,13,10,'{\"score\": \"10\"}',5,'2024-05-27 12:00:03'),(60,2,5,'{\"status\": \"on\"}',5,'2024-05-27 12:00:03'),(61,1,1,'{\"force\": \"high\"}',5,'2024-05-27 12:00:05'),(62,13,10,'{\"score\": \"20\"}',5,'2024-05-27 12:00:06'),(63,2,5,'{\"status\": \"on\"}',5,'2024-05-27 12:00:06'),(64,4,9,'{\"sound\": \"reload\"}',5,'2024-05-27 12:00:08'),(65,1,1,'{\"force\": \"low\"}',5,'2024-05-27 12:00:10'),(66,13,10,'{\"score\": \"30\"}',5,'2024-05-27 12:00:11'),(67,2,5,'{\"status\": \"on\"}',5,'2024-05-27 12:00:11'),(68,5,9,'{\"sound\": \"stop\"}',5,'2024-05-27 13:00:00'),(69,10,12,'{\"state\": \"pressed\"}',NULL,'2024-05-27 13:00:05'),(70,7,11,'{\"direction\": \"left\"}',NULL,'2024-05-27 13:00:10'),(71,8,11,'{\"direction\": \"right\"}',NULL,'2024-05-27 13:00:15'),(72,11,13,'{\"state\": \"pressed\"}',NULL,'2024-05-27 13:00:20'),(73,3,9,'{\"volume\": \"high\"}',6,'2024-05-27 13:00:00'),(74,1,2,'{\"force\": \"medium\"}',6,'2024-05-27 13:00:02'),(75,13,10,'{\"score\": \"10\"}',6,'2024-05-27 13:00:03'),(76,2,6,'{\"status\": \"on\"}',6,'2024-05-27 13:00:03'),(77,1,2,'{\"force\": \"high\"}',6,'2024-05-27 13:00:05'),(78,13,10,'{\"score\": \"20\"}',6,'2024-05-27 13:00:06'),(79,2,6,'{\"status\": \"on\"}',6,'2024-05-27 13:00:06'),(80,4,9,'{\"sound\": \"reload\"}',6,'2024-05-27 13:00:08'),(81,1,2,'{\"force\": \"low\"}',6,'2024-05-27 13:00:10'),(82,13,10,'{\"score\": \"30\"}',6,'2024-05-27 13:00:11'),(83,2,6,'{\"status\": \"on\"}',6,'2024-05-27 13:00:11'),(84,5,9,'{\"sound\": \"stop\"}',6,'2024-05-27 14:00:00'),(85,10,12,'{\"state\": \"pressed\"}',NULL,'2024-05-27 14:00:05'),(86,7,11,'{\"direction\": \"left\"}',NULL,'2024-05-27 14:00:10'),(87,8,11,'{\"direction\": \"right\"}',NULL,'2024-05-27 14:00:15'),(88,11,13,'{\"state\": \"pressed\"}',NULL,'2024-05-27 14:00:20'),(89,3,9,'{\"volume\": \"high\"}',7,'2024-05-27 14:00:00'),(90,1,3,'{\"force\": \"medium\"}',7,'2024-05-27 14:00:02'),(91,13,10,'{\"score\": \"10\"}',7,'2024-05-27 14:00:03'),(92,2,7,'{\"status\": \"on\"}',7,'2024-05-27 14:00:03'),(93,1,3,'{\"force\": \"high\"}',7,'2024-05-27 14:00:05'),(94,13,10,'{\"score\": \"20\"}',7,'2024-05-27 14:00:06'),(95,2,7,'{\"status\": \"on\"}',7,'2024-05-27 14:00:06'),(96,4,9,'{\"sound\": \"reload\"}',7,'2024-05-27 14:00:08'),(97,1,3,'{\"force\": \"low\"}',7,'2024-05-27 14:00:10'),(98,13,10,'{\"score\": \"30\"}',7,'2024-05-27 14:00:11'),(99,2,7,'{\"status\": \"on\"}',7,'2024-05-27 14:00:11'),(100,5,9,'{\"sound\": \"stop\"}',7,'2024-05-27 15:00:00'),(101,10,12,'{\"state\": \"pressed\"}',NULL,'2024-05-27 15:00:05'),(102,7,11,'{\"direction\": \"left\"}',NULL,'2024-05-27 15:00:10'),(103,8,11,'{\"direction\": \"right\"}',NULL,'2024-05-27 15:00:15'),(104,11,13,'{\"state\": \"pressed\"}',NULL,'2024-05-27 15:00:20'),(105,3,9,'{\"volume\": \"high\"}',8,'2024-05-27 15:00:00'),(106,1,4,'{\"force\": \"medium\"}',8,'2024-05-27 15:00:02'),(107,13,10,'{\"score\": \"10\"}',8,'2024-05-27 15:00:03'),(108,2,8,'{\"status\": \"on\"}',8,'2024-05-27 15:00:03'),(109,1,4,'{\"force\": \"high\"}',8,'2024-05-27 15:00:05'),(110,13,10,'{\"score\": \"20\"}',8,'2024-05-27 15:00:06'),(111,2,8,'{\"status\": \"on\"}',8,'2024-05-27 15:00:06'),(112,4,9,'{\"sound\": \"reload\"}',8,'2024-05-27 15:00:08'),(113,1,4,'{\"force\": \"low\"}',8,'2024-05-27 15:00:10'),(114,13,10,'{\"score\": \"30\"}',8,'2024-05-27 15:00:11'),(115,2,8,'{\"status\": \"on\"}',8,'2024-05-27 15:00:11'),(116,5,9,'{\"sound\": \"stop\"}',8,'2024-05-27 16:00:00'),(117,10,12,'{\"state\": \"pressed\"}',NULL,'2024-05-27 16:00:05'),(118,7,11,'{\"direction\": \"left\"}',NULL,'2024-05-27 16:00:10'),(119,8,11,'{\"direction\": \"right\"}',NULL,'2024-05-27 16:00:15'),(120,11,13,'{\"state\": \"pressed\"}',NULL,'2024-05-27 16:00:20');
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
  `training_course_id` int NOT NULL,
  `start_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `end_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `training_course_id` (`training_course_id`),
  CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `sessions_ibfk_2` FOREIGN KEY (`training_course_id`) REFERENCES `trainingcourses` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
-- INSERT INTO `sessions` VALUES (1,1,1,'2024-05-27 08:00:00','2024-05-27 09:00:00'),(2,1,2,'2024-05-27 09:00:00','2024-05-27 10:00:00'),(3,2,1,'2024-05-27 10:00:00','2024-05-27 11:00:00'),(4,2,2,'2024-05-27 11:00:00','2024-05-27 12:00:00'),(5,3,1,'2024-05-27 12:00:00','2024-05-27 13:00:00'),(6,3,2,'2024-05-27 13:00:00','2024-05-27 14:00:00'),(7,4,1,'2024-05-27 14:00:00','2024-05-27 15:00:00'),(8,4,2,'2024-05-27 15:00:00','2024-05-27 16:00:00'),(9,1,1,'2024-05-27 16:00:00','2024-05-27 17:00:00'),(10,1,2,'2024-05-27 17:00:00','2024-05-27 18:00:00'),(11,1,1,'2024-05-28 08:00:00','2024-05-28 09:00:00'),(12,1,2,'2024-05-28 09:00:00','2024-05-28 10:00:00'),(13,2,1,'2024-05-28 10:00:00','2024-05-28 11:00:00'),(14,2,2,'2024-05-28 11:00:00','2024-05-28 12:00:00'),(15,3,1,'2024-05-28 12:00:00','2024-05-28 13:00:00'),(16,3,2,'2024-05-28 13:00:00','2024-05-28 14:00:00'),(17,4,1,'2024-05-28 14:00:00','2024-05-28 15:00:00'),(18,4,2,'2024-05-28 15:00:00','2024-05-28 16:00:00'),(19,1,1,'2024-05-28 16:00:00','2024-05-28 17:00:00');
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trainingcourses`
--

DROP TABLE IF EXISTS `trainingcourses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trainingcourses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `sequence` json NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trainingcourses`
--

LOCK TABLES `trainingcourses` WRITE;
/*!40000 ALTER TABLE `trainingcourses` DISABLE KEYS */;
-- INSERT INTO `trainingcourses` VALUES (1,'Training Course 1','{\"sequence\": [\"target1\", \"target1\", \"target3\", \"target2\", \"target4\", \"reload\", \"target1\", \"target1\", \"target3\", \"target2\", \"target4\"]}'),(2,'Training Course 2','{\"sequence\": [\"target2\", \"target4\", \"target3\", \"target1\", \"target2\", \"reload\", \"target2\", \"target3\", \"target1\", \"target1\", \"target2\"]}');
/*!40000 ALTER TABLE `trainingcourses` ENABLE KEYS */;
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
  `highscore` varchar(255),
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
-- INSERT INTO `users` VALUES (1,'user1','0000'),(2,'user2','0000'),(3,'user3','0000'),(4,'user4','0000');
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