-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 20, 2025 at 03:01 AM
-- Server version: 8.0.30
-- PHP Version: 8.3.10

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
('81628ce16a9e');

-- --------------------------------------------------------

--
-- Table structure for table `analisis_keramaian`
--

CREATE TABLE `analisis_keramaian` (
  `id` int NOT NULL,
  `id_keramaian` int NOT NULL,
  `image` varchar(255) NOT NULL,
  `status` enum('SEPI','NORMAL','PADAT') NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `analisis_tumpukan`
--

CREATE TABLE `analisis_tumpukan` (
  `id` int NOT NULL,
  `id_tumpukan` int NOT NULL,
  `image` varchar(255) NOT NULL,
  `status` enum('OK','FULL') NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `keramaian`
--

CREATE TABLE `keramaian` (
  `id` int NOT NULL,
  `nama_lokasi` varchar(35) NOT NULL,
  `alamat` varchar(35) NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `laporan`
--

CREATE TABLE `laporan` (
  `id` int NOT NULL,
  `judul_laporan` text NOT NULL,
  `deskripsi` text NOT NULL,
  `estimasi` varchar(20) NOT NULL,
  `kategori` enum('KERAMAIAN','TUMPUKAN_SAMPAH') DEFAULT NULL,
  `status_pengerjaan` enum('BARU','DIBACA','SELESAI') DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id_user` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `laporan`
--

INSERT INTO `laporan` (`id`, `judul_laporan`, `deskripsi`, `estimasi`, `kategori`, `status_pengerjaan`, `created_at`, `updated_at`, `id_user`) VALUES
(2, 'Keramaian di taman (updated)', 'Sampah menumpuk di gang kecil', '3 hari', 'TUMPUKAN_SAMPAH', 'BARU', '2025-05-20 02:04:31', '2025-05-20 02:25:16', 1),
(3, 'Keramaian di taman (updated)', 'Sampah menumpuk di gang kecil', '3 hari', 'TUMPUKAN_SAMPAH', 'DIBACA', '2025-05-20 02:05:09', '2025-05-20 02:09:52', 1),
(4, 'RAME', 'RUAMEE', '3 hari', 'KERAMAIAN', 'BARU', '2025-05-20 02:09:32', NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `tumpukan_sampah`
--

CREATE TABLE `tumpukan_sampah` (
  `id` int NOT NULL,
  `nama_lokasi` varchar(35) NOT NULL,
  `alamat` varchar(35) NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tumpukan_sampah`
--

INSERT INTO `tumpukan_sampah` (`id`, `nama_lokasi`, `alamat`, `latitude`, `longitude`, `created_at`, `updated_at`) VALUES
(2, 'TPS Rawasari', 'Jl. Rawasari Selatan', -6.17539, 106.827, '2025-05-15 17:00:36', NULL),
(3, 'TPS Cempaka Putih', 'Jl. Cempaka Putih Tengah', -6.17394, 106.858, '2025-05-15 17:01:04', NULL),
(4, 'TPS Matraman', 'Jl. Matraman Raya', -6.20139, 106.871, '2025-05-15 17:01:13', NULL),
(5, 'TPS Kramat Jati', 'Jl. Raya Bogor', -6.27219, 106.864, '2025-05-15 17:01:22', NULL),
(6, 'TPS Pulogadung', 'Jl. Raya Bekasi', -6.20886, 106.9, '2025-05-15 17:01:34', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id_user` int NOT NULL,
  `role` enum('ADMIN','USER','STAFF') NOT NULL,
  `name_lengkap` varchar(30) NOT NULL,
  `email` varchar(35) NOT NULL,
  `no_telepon` varchar(13) NOT NULL,
  `username` varchar(15) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id_user`, `role`, `name_lengkap`, `email`, `no_telepon`, `username`, `password`, `created_at`, `updated_at`) VALUES
(1, 'ADMIN', 'Ghanza', 'beta@gmail.com', '082229350946', 'beta', '$2b$12$VCGStCuXMG1Uda.2mI0wu.BbSetr4rJMGl2oe0fiOZILMfouVs8ha', '2025-05-15 17:03:09', '2025-05-15 17:04:59');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `analisis_keramaian`
--
ALTER TABLE `analisis_keramaian`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_keramaian` (`id_keramaian`);

--
-- Indexes for table `analisis_tumpukan`
--
ALTER TABLE `analisis_tumpukan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_tumpukan` (`id_tumpukan`);

--
-- Indexes for table `keramaian`
--
ALTER TABLE `keramaian`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `laporan`
--
ALTER TABLE `laporan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `tumpukan_sampah`
--
ALTER TABLE `tumpukan_sampah`
  ADD PRIMARY KEY (`id`);

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
-- AUTO_INCREMENT for table `analisis_keramaian`
--
ALTER TABLE `analisis_keramaian`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `analisis_tumpukan`
--
ALTER TABLE `analisis_tumpukan`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `keramaian`
--
ALTER TABLE `keramaian`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `laporan`
--
ALTER TABLE `laporan`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `tumpukan_sampah`
--
ALTER TABLE `tumpukan_sampah`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `analisis_keramaian`
--
ALTER TABLE `analisis_keramaian`
  ADD CONSTRAINT `analisis_keramaian_ibfk_1` FOREIGN KEY (`id_keramaian`) REFERENCES `keramaian` (`id`);

--
-- Constraints for table `analisis_tumpukan`
--
ALTER TABLE `analisis_tumpukan`
  ADD CONSTRAINT `analisis_tumpukan_ibfk_1` FOREIGN KEY (`id_tumpukan`) REFERENCES `tumpukan_sampah` (`id`);

--
-- Constraints for table `laporan`
--
ALTER TABLE `laporan`
  ADD CONSTRAINT `laporan_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
