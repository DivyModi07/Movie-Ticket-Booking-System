-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 28, 2025 at 10:39 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `movie_booking`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookingpayment`
--

CREATE TABLE `bookingpayment` (
  `booking_id` varchar(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `entry_key` varchar(255) NOT NULL,
  `num_of_tickets` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `seat_numbers` varchar(255) DEFAULT NULL,
  `booking_status` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookingpayment`
--

INSERT INTO `bookingpayment` (`booking_id`, `user_id`, `entry_key`, `num_of_tickets`, `amount`, `seat_numbers`, `booking_status`) VALUES
('B01', 'Divy89', 'AMD-TH01-M04-250227-17:00:00', 1, 256.00, 'B12', 'booked'),
('B02', 'Meet89', 'AMD-TH01-M04-250227-17:00:00', 1, 256.00, 'H8', 'booked'),
('B03', 'Meet89', 'AMD-TH01-M04-250227-17:00:00', 1, 256.00, 'D2', 'booked'),
('B04', 'Divy89', 'AMD-TH01-M04-250227-17:00:00', 1, 256.00, NULL, 'cancelled'),
('B05', 'Divy89', 'AMD-TH01-M04-250227-17:00:00', 1, 256.00, NULL, 'cancelled'),
('B06', 'Divy89', 'AMD-TH01-M05-250301-17:00:00', 3, 768.00, 'B9, B10, B11', 'booked'),
('B07', 'Meet89', 'AMD-TH01-M05-250301-17:00:00', 2, 512.00, NULL, 'cancelled'),
('B08', 'Divy89', 'AMD-TH01-M05-250301-17:00:00', 2, 512.00, 'D8, D7', 'booked'),
('B09', 'Divy89', 'AMD-TH01-M05-250301-17:00:00', 2, 512.00, 'H9, H10', 'booked'),
('B10', 'Divy89', 'AMD-TH01-M05-250301-17:00:00', 2, 512.00, NULL, 'cancelled');

-- --------------------------------------------------------

--
-- Table structure for table `movieshowtimes`
--

CREATE TABLE `movieshowtimes` (
  `entry_key` varchar(255) NOT NULL,
  `city` varchar(20) NOT NULL,
  `theater_name` varchar(255) NOT NULL,
  `movie_name` varchar(30) NOT NULL,
  `genre` varchar(30) NOT NULL,
  `movie_duration` varchar(12) NOT NULL,
  `movie_price` int(6) NOT NULL,
  `show_date` date NOT NULL,
  `show_time` varchar(12) NOT NULL,
  `available_seats` int(11) NOT NULL,
  `total_seats` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `movieshowtimes`
--

INSERT INTO `movieshowtimes` (`entry_key`, `city`, `theater_name`, `movie_name`, `genre`, `movie_duration`, `movie_price`, `show_date`, `show_time`, `available_seats`, `total_seats`) VALUES
('AMD-TH01-M04-250227-17:00:00', 'Ahmedabad', 'PVR', 'Chhaava', 'Historical action', '02:20:00', 200, '2025-02-27', '17:00:00', 125, 128),
('AMD-TH01-M04-250301-09:00:00', 'Ahmedabad', 'PVR', 'Chhaava', 'Historical action', '02:20:00', 150, '2025-03-01', '09:00:00', 128, 128),
('AMD-TH01-M04-250301-21:00:00', 'Ahmedabad', 'PVR', 'Chhaava', 'Historical action', '02:20:00', 250, '2025-03-01', '21:00:00', 128, 128),
('AMD-TH01-M04-250302-09:00:00', 'Ahmedabad', 'PVR', 'Chhaava', 'Historical action', '02:20:00', 150, '2025-03-02', '09:00:00', 128, 128),
('AMD-TH01-M04-250302-21:00:00', 'Ahmedabad', 'PVR', 'Chhaava', 'Historical action', '02:20:00', 250, '2025-03-02', '21:00:00', 128, 128),
('AMD-TH01-M05-250301-13:00:00', 'Ahmedabad', 'PVR', 'Crazxy', 'Thriller', '01:33:00', 180, '2025-03-01', '13:00:00', 128, 128),
('AMD-TH01-M05-250301-17:00:00', 'Ahmedabad', 'PVR', 'Crazxy', 'Thriller', '01:33:00', 200, '2025-03-01', '17:00:00', 121, 128),
('AMD-TH01-M05-250302-13:00:00', 'Ahmedabad', 'PVR', 'Crazxy', 'Thriller', '01:33:00', 180, '2025-03-02', '13:00:00', 128, 128),
('AMD-TH01-M05-250302-17:00:00', 'Ahmedabad', 'PVR', 'Crazxy', 'Thriller', '01:33:00', 200, '2025-03-02', '17:00:00', 128, 128),
('AMD-TH02-M05-250301-09:00:00', 'Ahmedabad', 'Inox', 'Crazxy', 'Thriller', '01:33:00', 150, '2025-03-01', '09:00:00', 128, 128),
('AMD-TH02-M05-250302-09:00:00', 'Ahmedabad', 'Inox', 'Crazxy', 'Thriller', '01:33:00', 150, '2025-03-02', '09:00:00', 128, 128),
('AMD-TH02-M05-250303-09:00:00', 'Ahmedabad', 'Inox', 'Crazxy', 'Thriller', '01:33:00', 150, '2025-03-03', '09:00:00', 128, 128),
('SRT-TH01-M05-250302-09:00:00', 'Surat', 'PVR', 'Crazxy', 'Thriller', '01:33:00', 150, '2025-03-02', '09:00:00', 128, 128);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` varchar(10) NOT NULL,
  `name` varchar(20) NOT NULL,
  `password` varchar(12) NOT NULL,
  `mobile_no` varchar(14) NOT NULL,
  `role` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `name`, `password`, `mobile_no`, `role`) VALUES
('admin91', 'admin', '101010', '9189909097', 'admin'),
('Bhavi78', 'Bhavin', '181818', '7890789098', 'user'),
('Divy89', 'Divy', '123456', '8900890097', 'user'),
('Hetan78', 'Hetansh', '111111', '7890789090', 'user'),
('Kavis98', 'Kavish', '223344', '9870987090', 'user'),
('Meet89', 'Meet', '123456', '8990899090', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bookingpayment`
--
ALTER TABLE `bookingpayment`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `entry_key` (`entry_key`);

--
-- Indexes for table `movieshowtimes`
--
ALTER TABLE `movieshowtimes`
  ADD PRIMARY KEY (`entry_key`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookingpayment`
--
ALTER TABLE `bookingpayment`
  ADD CONSTRAINT `bookingpayment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `bookingpayment_ibfk_2` FOREIGN KEY (`entry_key`) REFERENCES `movieshowtimes` (`entry_key`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
