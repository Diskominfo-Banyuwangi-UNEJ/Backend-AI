-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 14, 2025 at 04:12 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `diskominfo-bwi`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('79020c897a8c');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id_user` int NOT NULL,
  `role` enum('ADMIN','USER','STAFF') NOT NULL,
  `name_lengkap` varchar(30) NOT NULL,
  `tanggal_lahir` datetime NOT NULL,
  `email` varchar(35) NOT NULL,
  `no_telepon` varchar(13) NOT NULL,
  `jenis_kelamin` enum('MALE','FEMALE','OTHER') NOT NULL,
  `username` varchar(15) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id_user`, `role`, `name_lengkap`, `tanggal_lahir`, `email`, `no_telepon`, `jenis_kelamin`, `username`, `password`, `created_at`, `updated_at`) VALUES
(1, 'STAFF', 'BUDI Updated', '1985-05-15 00:00:00', 'budi.admin@example.com', '08198765432', 'MALE', 'budi_admin', '$2b$12$1vcICxemGYUXgkEZZPE8iOLWQj8f2W8..CL0rmUIU1/VCwUx7H2Mi', '2025-04-06 16:01:37', '2025-04-06 16:01:50'),
(2, 'ADMIN', 'Admin Utama', '1990-01-01 00:00:00', 'admin@example.com', '08123456789', 'MALE', 'admin', '$2b$12$18BO3wXIEcTENO2KN.bFbuVfUlICekzT/yhZgyYkSDpc.mKEWbYq.', '2025-04-06 16:02:17', NULL),
(3, 'ADMIN', 'Angga Dwi Kurniawan Oh my god', '2003-08-12 00:00:00', 'angganteng12@gmail.com', '082229350946', 'MALE', 'angga', '$2b$12$UoajhObK8wOlYhC9MRcu2OxyneQsgOxnAaanqApvUFuWsgfsAYDHG', '2025-04-07 13:37:18', '2025-04-07 13:40:05'),
(4, 'ADMIN', 'Ghanza', '2003-08-12 00:00:00', 'beta@gmail.com', '082229350946', 'MALE', 'beta', '$2b$12$TCgn5YnOoX72xjihPYIb4OYjJyCi0ZU1RNGO/YxygE.Z9Rck.zTUu', '2025-04-14 03:39:36', '2025-04-14 03:40:23');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
