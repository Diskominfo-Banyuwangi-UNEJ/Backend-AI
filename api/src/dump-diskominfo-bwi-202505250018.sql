-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: diskominfo-bwi
-- ------------------------------------------------------
-- Server version	8.0.30

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('8d300dd9a151');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `analisis_keramaian`
--

DROP TABLE IF EXISTS `analisis_keramaian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `analisis_keramaian` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_keramaian` int NOT NULL,
  `image` varchar(255) NOT NULL,
  `status` enum('SEPI','NORMAL','PADAT') NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_keramaian` (`id_keramaian`),
  CONSTRAINT `analisis_keramaian_ibfk_1` FOREIGN KEY (`id_keramaian`) REFERENCES `keramaian` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analisis_keramaian`
--

LOCK TABLES `analisis_keramaian` WRITE;
/*!40000 ALTER TABLE `analisis_keramaian` DISABLE KEYS */;
/*!40000 ALTER TABLE `analisis_keramaian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `analisis_tumpukan`
--

DROP TABLE IF EXISTS `analisis_tumpukan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `analisis_tumpukan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_tumpukan` int NOT NULL,
  `image` varchar(255) NOT NULL,
  `status` enum('OK','FULL') NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_tumpukan` (`id_tumpukan`),
  CONSTRAINT `analisis_tumpukan_ibfk_1` FOREIGN KEY (`id_tumpukan`) REFERENCES `tumpukan_sampah` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analisis_tumpukan`
--

LOCK TABLES `analisis_tumpukan` WRITE;
/*!40000 ALTER TABLE `analisis_tumpukan` DISABLE KEYS */;
/*!40000 ALTER TABLE `analisis_tumpukan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keramaian`
--

DROP TABLE IF EXISTS `keramaian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `keramaian` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama_lokasi` varchar(35) NOT NULL,
  `alamat` varchar(35) NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keramaian`
--

LOCK TABLES `keramaian` WRITE;
/*!40000 ALTER TABLE `keramaian` DISABLE KEYS */;
/*!40000 ALTER TABLE `keramaian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `laporan`
--

DROP TABLE IF EXISTS `laporan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `laporan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_user` int NOT NULL,
  `judul_laporan` text NOT NULL,
  `deskripsi` text NOT NULL,
  `estimasi` varchar(20) NOT NULL,
  `kategori` enum('KERAMAIAN','TUMPUKAN_SAMPAH') DEFAULT NULL,
  `status_pengerjaan` enum('DITERIMA','DALAM_PENGERJAAN','SELESAI') DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_user` (`id_user`),
  CONSTRAINT `laporan_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `laporan`
--

LOCK TABLES `laporan` WRITE;
/*!40000 ALTER TABLE `laporan` DISABLE KEYS */;
/*!40000 ALTER TABLE `laporan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pengaduan`
--

DROP TABLE IF EXISTS `pengaduan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pengaduan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_user` int NOT NULL,
  `katerogi_pengaduan` enum('KERAMAIAN','TUMPUKAN_SAMPAH') NOT NULL,
  `status_pengaduan` enum('BARU','DIBACA','SELESAI') NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_user` (`id_user`),
  CONSTRAINT `pengaduan_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pengaduan`
--

LOCK TABLES `pengaduan` WRITE;
/*!40000 ALTER TABLE `pengaduan` DISABLE KEYS */;
/*!40000 ALTER TABLE `pengaduan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tumpukan_sampah`
--

DROP TABLE IF EXISTS `tumpukan_sampah`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tumpukan_sampah` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama_lokasi` varchar(35) NOT NULL,
  `alamat` varchar(35) NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tumpukan_sampah`
--

LOCK TABLES `tumpukan_sampah` WRITE;
/*!40000 ALTER TABLE `tumpukan_sampah` DISABLE KEYS */;
INSERT INTO `tumpukan_sampah` VALUES (2,'TPS Rawasari','Jl. Rawasari Selatan',-6.17539,106.827,'2025-05-15 17:00:36',NULL),(3,'TPS Cempaka Putih','Jl. Cempaka Putih Tengah',-6.17394,106.858,'2025-05-15 17:01:04',NULL),(4,'TPS Matraman','Jl. Matraman Raya',-6.20139,106.871,'2025-05-15 17:01:13',NULL),(5,'TPS Kramat Jati','Jl. Raya Bogor',-6.27219,106.864,'2025-05-15 17:01:22',NULL),(6,'TPS Pulogadung','Jl. Raya Bekasi',-6.20886,106.9,'2025-05-15 17:01:34',NULL);
/*!40000 ALTER TABLE `tumpukan_sampah` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id_user` int NOT NULL AUTO_INCREMENT,
  `role` enum('ADMIN','PEMERINTAH') NOT NULL,
  `nama_instansi` enum('KOMINFO','DISHUB','DLH','SATPOL_PP') NOT NULL,
  `name_lengkap` varchar(30) NOT NULL,
  `email` varchar(35) NOT NULL,
  `username` varchar(15) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'ADMIN','KOMINFO','Ghanza','beta@gmail.com','beta','$2b$12$1hha4PqfatWddkPsyLedhuXZSV5GuYTmjsEG70IzzjlXmUVQwtcB.','2025-05-24 17:14:11','2025-05-24 17:14:41');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'diskominfo-bwi'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-25  0:18:45
