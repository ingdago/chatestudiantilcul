-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: chat_db
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `contactos`
--

DROP TABLE IF EXISTS `contactos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contactos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `contacto_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `contacto_id` (`contacto_id`),
  CONSTRAINT `contactos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `contactos_ibfk_2` FOREIGN KEY (`contacto_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contactos`
--

LOCK TABLES `contactos` WRITE;
/*!40000 ALTER TABLE `contactos` DISABLE KEYS */;
INSERT INTO `contactos` VALUES (17,3,2),(18,7,2),(19,7,1),(24,4,1),(25,3,1),(27,1,3),(28,4,2),(29,4,3),(32,1,2),(45,2,1),(46,2,3),(47,1,8);
/*!40000 ALTER TABLE `contactos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grupos`
--

DROP TABLE IF EXISTS `grupos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grupos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `creador` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos`
--

LOCK TABLES `grupos` WRITE;
/*!40000 ALTER TABLE `grupos` DISABLE KEYS */;
INSERT INTO `grupos` VALUES (1,'sistemas distribuidos','dago'),(2,'Inteligencia Artificial','dago'),(3,'Diseño Web','dago'),(4,'Electrónica','dago'),(5,'Investigación','dago'),(6,'Contabilidad','dago'),(7,'Contabilidad l','dago'),(10,'Redes l','dago'),(11,'Compiladores','dago'),(12,'Electiva disciplinar l','dago'),(13,'educacion fisica','dago'),(14,'Calculo ll','dago');
/*!40000 ALTER TABLE `grupos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mensajes`
--

DROP TABLE IF EXISTS `mensajes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mensajes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `remitente_id` int DEFAULT NULL,
  `receptor_id` int DEFAULT NULL,
  `mensaje` text,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `grupo_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `remitente_id` (`remitente_id`),
  KEY `receptor_id` (`receptor_id`),
  KEY `grupo_id` (`grupo_id`),
  CONSTRAINT `mensajes_ibfk_1` FOREIGN KEY (`remitente_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `mensajes_ibfk_2` FOREIGN KEY (`receptor_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `mensajes_ibfk_3` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mensajes`
--

LOCK TABLES `mensajes` WRITE;
/*!40000 ALTER TABLE `mensajes` DISABLE KEYS */;
INSERT INTO `mensajes` VALUES (1,1,2,'hola','2024-11-11 00:39:51',NULL),(2,2,1,'hola','2024-11-11 00:39:56',NULL),(3,1,2,'jaja','2024-11-11 00:40:35',NULL),(4,2,1,'bnbn','2024-11-11 00:40:42',NULL),(5,1,NULL,'buenas noches','2024-11-11 00:40:56',6),(6,2,NULL,'todo bn','2024-11-11 00:41:11',6),(7,1,3,'hola','2024-11-11 01:18:31',NULL),(8,2,1,'hola','2024-11-11 01:19:36',NULL),(9,1,3,'ey','2024-11-11 01:20:54',NULL),(10,2,1,'hh','2024-11-11 01:21:12',NULL),(11,1,2,'hola','2024-11-11 18:43:10',NULL),(12,1,2,'hola','2024-11-11 18:58:26',NULL),(13,2,1,'hoy es lunes','2024-11-11 18:58:35',NULL),(14,2,NULL,'buenos dias','2024-11-11 18:58:45',6),(15,2,1,'hola','2024-11-11 18:58:54',NULL),(16,2,1,'jajaj','2024-11-11 18:58:58',NULL),(17,1,3,'hola','2024-11-15 04:18:53',NULL),(18,3,1,'hola','2024-11-15 04:22:18',NULL),(19,1,3,'jajja','2024-11-15 04:22:22',NULL),(20,1,2,'hola','2024-11-15 04:25:28',NULL),(21,3,2,'hola','2024-11-15 04:26:27',NULL),(22,3,2,'hola','2024-11-15 04:26:51',NULL),(23,2,1,'Ey','2024-11-15 04:29:20',NULL),(24,2,3,'holaa','2024-11-15 04:41:58',NULL),(25,1,3,'ey','2024-11-15 04:46:46',NULL),(26,1,2,'yu','2024-11-15 04:50:18',NULL),(27,1,3,'hola mami','2024-11-15 04:57:29',NULL),(28,3,1,'dime hijo','2024-11-15 04:57:34',NULL),(29,1,3,'hola','2024-11-15 05:07:28',NULL),(30,3,1,'jaja','2024-11-15 05:07:32',NULL),(31,2,1,'Hola','2024-11-15 05:07:46',NULL),(32,1,2,'jajajja','2024-11-15 05:08:01',NULL),(33,2,NULL,'Buenas','2024-11-15 05:08:18',6),(34,1,NULL,'h','2024-11-15 05:08:27',6),(35,3,NULL,'m','2024-11-15 05:08:35',6),(36,1,2,'ey','2024-11-15 05:15:51',NULL),(37,1,2,'Dago','2024-11-15 05:27:14',NULL),(38,1,2,'Jaja','2024-11-15 05:27:25',NULL),(39,2,1,'HOLA','2024-11-15 05:27:42',NULL),(40,1,2,'Ey','2024-11-15 05:31:48',NULL),(41,2,1,'jaja','2024-11-15 05:31:55',NULL),(42,1,2,'Dago','2024-11-15 05:36:10',NULL),(43,2,1,'h','2024-11-15 05:36:25',NULL),(44,1,2,'jaja','2024-11-15 05:38:20',NULL),(45,1,3,'hola','2024-11-15 05:49:49',NULL),(46,3,1,'jajaj','2024-11-15 05:49:55',NULL),(47,1,3,'jaja','2024-11-15 05:50:10',NULL),(48,1,NULL,'hola','2024-11-15 05:50:24',6),(49,3,NULL,'jajaja','2024-11-15 05:50:49',6);
/*!40000 ALTER TABLE `mensajes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_nombre` (`usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'dago','$2b$12$fHOlDSYovRqIZvVUQiW42.lEBaN6A8u4vdPdh1jcv8ZrFp2o7XkQu'),(2,'asary','$2b$12$690gZc6oXvnkYFep52H8veBHXSj8JCUThy84Te.SG4ax4pC3zq1oG'),(3,'monica','$2b$12$C2upjjkDycC8rlhk5VhSv.1S2xCkk6PK4Yk/IdTsntipuPk2Lv.F.'),(4,'edgar','$2b$12$ecmorRXj13pvc66j9omHs.adz9Tgk92BkPBGx8qUA0pGoq3KcUe0u'),(5,'rebeca','$2b$12$M2aHq2dxcmwvstHIgEBTU.ulzu5LBRD8R9hTB1jLojEFzTnAVNOsW'),(6,'pablo','$2b$12$xUqv9MzQK0m4/xPqxleGWuHBnCjCeWHrof.ACq7jTdHCaJmt5Heqa'),(7,'javier','$2b$12$4MHKwHzuo0aCSznYY9MPoeMPz1tptjWaR/E0FbOBrl5wMMRof6MM.'),(8,'cardozo','$2b$12$f2kk0.58Kqo6UwsnxxZFh.2Gkov2lHyITMbI.6AR/YZRQeOShZ7/6'),(9,'Melany','$2b$12$YxlYXqk1zlGh8QByio12Gu9.4bbLRwQAqrSFTxJyAXW0.LHbM/aPq'),(10,'Elisabeth','$2b$12$/2cWbDxYhLGOCJ36JLOIru4ZsDICt.BHp7UIA18zkzkOyA2WB2HcO'),(11,'pedro','$2b$12$keAulsI7.w5tgtScssaph.xZjMpthfFXysmYw.7o5Kr9uoTHPkNju'),(12,'juan','$2b$12$nfHp.voQhttg3sMHnRr8geLaejAPACws3W/RmxvYya6h1m.6MsXzS'),(13,'mariela','$2b$12$MdctudZydHkvJdJq6U9uY.EV7ItNEKj4VsgLscC0exbBY15XwrcWi'),(14,'patricia','$2b$12$KhDxFd/OnlOcMNoLP150meYB2.0ckR8gEqhDvE1Ixvz.Ptycta2HS'),(15,'farid','$2b$12$EaT1GT3uCyGS1DbHwEVtQ.HNGPZxpL/.GITHAOIqkLIuZ5GFYMeU2'),(17,'fabiola','$2b$12$ru.nhpiKQbjB8cSRqIZTUOcLQUS/S4nEfbVDfhKOTNPTUV2torxa2'),(18,'dagoberto','$2b$12$rTxYg4vRTVd2kX6vk6AqNubnDjLUUmNiVZPNc9eIrSY3WKETqK3uK'),(19,'Mauricio','$2b$12$a0qx6vuT5wGEd8tolcrH7e/LqbxADJ9Rj4d25UDk/69qTHRvBv..m'),(20,'isaac','$2b$12$Tf58JvEmZkIKb5APp7VPqeRKXknrYLShH02RbNCFo44Wod7LUvHB6'),(21,'paola','$2b$12$nDfQcCkFo58El1wTiiuLtezLZ5uS.//N17P3Co6XxVHoCcoKwErmy'),(22,'paula','$2b$12$3kqhqGoBjLL30ryB38ZjPu9iqIT4zFkH4SOJna0rbqeKaAYm44vSC'),(23,'Gissela','$2b$12$H0.MS414aUhnyk.U4vJpLeNGeOhgNMb5UF2qDdJuPfxI7eci16TYG'),(24,'Aliana','$2b$12$/INhdedOBHulHx05zw6HzOaXlNuodM.RzRbFcD1Ea.96JRSifQ4y6');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios_grupos`
--

DROP TABLE IF EXISTS `usuarios_grupos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_grupos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `grupo_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `grupo_id` (`grupo_id`),
  CONSTRAINT `usuarios_grupos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `usuarios_grupos_ibfk_2` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_grupos`
--

LOCK TABLES `usuarios_grupos` WRITE;
/*!40000 ALTER TABLE `usuarios_grupos` DISABLE KEYS */;
INSERT INTO `usuarios_grupos` VALUES (1,1,6),(6,2,11),(8,2,6),(9,3,6),(10,1,11),(11,3,11),(12,1,12);
/*!40000 ALTER TABLE `usuarios_grupos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-17 14:31:14
