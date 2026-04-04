-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 04, 2026 at 05:31 AM
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
-- Database: `chestxraydb`
--

-- --------------------------------------------------------

--
-- Table structure for table `ai_analysis`
--

CREATE TABLE `ai_analysis` (
  `id` int(11) NOT NULL,
  `study_id` int(11) DEFAULT NULL,
  `ai_status` varchar(50) DEFAULT NULL,
  `confidence_score` float DEFAULT NULL,
  `ai_result` text DEFAULT NULL,
  `processed_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ai_analysis`
--

INSERT INTO `ai_analysis` (`id`, `study_id`, `ai_status`, `confidence_score`, `ai_result`, `processed_at`) VALUES
(1, 1, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-16 16:22:33'),
(2, 2, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-16 16:22:39'),
(3, 3, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-16 16:22:45'),
(4, 4, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-16 16:22:56'),
(5, 5, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-26 09:24:35'),
(6, 11, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-30 04:42:27'),
(7, 12, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-30 05:20:06'),
(8, 13, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-30 05:33:13'),
(9, 14, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-30 09:51:50'),
(10, 15, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-30 16:12:20'),
(11, 16, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-30 16:31:17'),
(12, 17, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-30 18:03:18'),
(13, 18, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-30 18:25:31'),
(14, 19, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-31 03:42:06'),
(15, 20, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-31 05:03:53'),
(16, 21, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-31 05:47:08'),
(17, 22, 'Completed', 0.94, 'No critical abnormalities detected', '2026-03-31 05:57:20'),
(18, 23, 'Completed', 0.94, 'No critical abnormalities detected', '2026-04-03 01:39:05'),
(19, 24, 'Completed', 0.94, 'No critical abnormalities detected', '2026-04-03 01:59:21'),
(20, 25, 'Completed', 0.94, 'No critical abnormalities detected', '2026-04-03 02:11:55'),
(21, 26, 'Completed', 0.94, 'No critical abnormalities detected', '2026-04-03 02:34:30'),
(22, 27, 'Completed', 0.94, 'No critical abnormalities detected', '2026-04-03 04:39:33'),
(23, 28, 'Completed', 0.94, 'No critical abnormalities detected', '2026-04-03 06:15:46'),
(24, 29, 'Completed', 0.94, 'No critical abnormalities detected', '2026-04-03 06:42:40');

-- --------------------------------------------------------

--
-- Table structure for table `cases`
--

CREATE TABLE `cases` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `patient_name` varchar(100) DEFAULT NULL,
  `patient_age` int(11) DEFAULT NULL,
  `diagnosis` varchar(255) DEFAULT NULL,
  `priority` varchar(50) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `ai_findings` text DEFAULT NULL,
  `ai_confidence` int(11) DEFAULT NULL,
  `final_diagnosis` varchar(255) DEFAULT NULL,
  `doctor_notes` text DEFAULT NULL,
  `decision` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `report_id` varchar(50) DEFAULT NULL,
  `finalized` tinyint(1) DEFAULT NULL,
  `signed_by` varchar(150) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL,
  `case_code` varchar(20) DEFAULT NULL,
  `ai_result` varchar(100) DEFAULT NULL,
  `scan_id` int(11) DEFAULT NULL,
  `doctor_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `doctors`
--

CREATE TABLE `doctors` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `hospital_email` varchar(150) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `role_requested` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `theme` varchar(20) DEFAULT NULL,
  `notifications_enabled` tinyint(1) DEFAULT NULL,
  `profile_photo` varchar(255) DEFAULT NULL,
  `preferred_language` varchar(50) DEFAULT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctors`
--

INSERT INTO `doctors` (`id`, `first_name`, `last_name`, `hospital_email`, `phone_number`, `role_requested`, `password`, `theme`, `notifications_enabled`, `profile_photo`, `preferred_language`, `specialization`, `created_at`) VALUES
(11, 'Mallavarapu', 'Mahendra Reddy', 'mahendramallavarapu0@gmail.com', '7396687732', 'doctor', 'Ammulu@2004', 'Light', 1, 'profile_photos/formal_pic.jpeg', 'English (US)', 'Doctor', '2026-04-03 09:18:45'),
(12, 'Sai', 'Tejaswi', 'saitejaswi71@gmail.com', '8121107943', 'doctor', 'Ammulu@1987', 'Light', 1, NULL, 'English (US)', NULL, '2026-04-03 09:18:45'),
(13, 'Arjun', 'Reddy', 'yaswanthmallavarapu8@gmail.com', '9393528008', 'doctor', 'Ammulu@4567', 'Light', 1, NULL, 'English (US)', NULL, '2026-04-03 09:18:45'),
(14, 'John', 'Reddy', 'srilathamallarapumallarapu@gmail.com', '7141235689', 'doctor', 'Ammulu@345', 'Light', 1, NULL, 'English (US)', NULL, '2026-04-03 09:18:45'),
(15, 'John', 'doe', 'john@gmail.com', '9392850086', 'doctor', 'Ammulu@9000', 'Light', 1, NULL, 'English (US)', NULL, '2026-04-03 09:18:45'),
(16, 'yachendra', 'nath', 'yachendra6310@gmail.com', '9030988648', 'doctor', 'Yach@123', 'Light', 1, NULL, 'English (US)', NULL, '2026-04-03 09:18:45'),
(17, 'Chaitanya', 'prakash', 'chaitanyaprakashkonisetty@gmail.com', '9849184777', 'doctor', 'Chaitu@2004', 'Light', 1, NULL, 'English (US)', NULL, '2026-04-03 09:18:45'),
(20, 'Swarna', 'Kousik', 'kousikssvv34@gmail.com', '9640638489', 'doctor', 'Chotu@2006', 'Light', 1, NULL, 'English (US)', NULL, '2026-04-03 09:18:45'),
(21, 'Deva', 'Devaa', 'punugotideva618@gmail.com', '7993537243', 'doctor', 'Deva@1234', 'Light', 1, NULL, 'English (US)', NULL, '2026-04-03 09:18:45'),
(22, 'pushpa', 'kanth', 'srik29924@gmail.com', '7729047460', 'doctor', 'Srik@12345', 'Light', 1, NULL, 'English (US)', NULL, '2026-04-03 09:18:45'),
(23, 'vamsi', 'krishna', 'pvvamsik2005@gmail.com', '7901595868', 'doctor', 'Kohli@2026', 'Light', 1, NULL, 'English (US)', NULL, '2026-04-03 09:18:45'),
(24, 'jaanu', 'reddy', 'jaanu@gmail.com', '8122245889', 'doctor', 'Jaanu@1987', 'Light', 1, NULL, 'English (US)', NULL, '2026-04-03 09:18:45'),
(25, 'Test', 'Doctor', 'test.doctor@hospital.com', '9876543210', 'doctor', 'Password123!', 'Light', 1, NULL, 'English (US)', NULL, '2026-04-03 09:18:45');

-- --------------------------------------------------------

--
-- Table structure for table `doctor_privacy_settings`
--

CREATE TABLE `doctor_privacy_settings` (
  `id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `data_sharing` tinyint(1) DEFAULT NULL,
  `history_retention` tinyint(1) DEFAULT NULL,
  `diagnostics` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `faqs`
--

CREATE TABLE `faqs` (
  `id` int(11) NOT NULL,
  `question` text NOT NULL,
  `answer` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `faqs`
--

INSERT INTO `faqs` (`id`, `question`, `answer`) VALUES
(1, 'What is a chest X-ray?', 'A chest X-ray is an imaging test that uses small amounts of radiation to create pictures of the chest.'),
(2, 'What diseases can be detected using chest X-ray?', 'Chest X-rays can detect pneumonia, tuberculosis, lung cancer, and other lung conditions.'),
(3, 'Is chest X-ray safe?', 'Yes, chest X-rays are generally safe and use a very small amount of radiation.'),
(4, 'How long does the scan take?', 'The scan usually takes only a few minutes.'),
(5, 'Do I need preparation for chest X-ray?', 'Usually no special preparation is needed.');

-- --------------------------------------------------------

--
-- Table structure for table `feedbacks`
--

CREATE TABLE `feedbacks` (
  `id` int(11) NOT NULL,
  `technician_id` int(11) DEFAULT NULL,
  `feedback_type` varchar(50) DEFAULT NULL,
  `subject` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `screenshot_path` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedbacks`
--

INSERT INTO `feedbacks` (`id`, `technician_id`, `feedback_type`, `subject`, `description`, `screenshot_path`, `created_at`) VALUES
(1, 1, 'yes very aaswsome', 'prifile not working', 'worst app', 'feedback_uploads/1_Screenshot (2).png', '2026-03-16 16:34:40');

-- --------------------------------------------------------

--
-- Table structure for table `pacs_archives`
--

CREATE TABLE `pacs_archives` (
  `id` int(11) NOT NULL,
  `study_id` int(11) DEFAULT NULL,
  `archive_location` varchar(255) DEFAULT NULL,
  `archive_status` varchar(50) DEFAULT NULL,
  `archived_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pacs_archives`
--

INSERT INTO `pacs_archives` (`id`, `study_id`, `archive_location`, `archive_status`, `archived_at`) VALUES
(1, 1, 'PACS_SERVER/study_1.dcm', 'Archived', '2026-03-16 16:22:33'),
(2, 2, 'PACS_SERVER/study_2.dcm', 'Archived', '2026-03-16 16:22:39'),
(3, 3, 'PACS_SERVER/study_3.dcm', 'Archived', '2026-03-16 16:22:45'),
(4, 4, 'PACS_SERVER/study_4.dcm', 'Archived', '2026-03-16 16:22:56'),
(5, 5, 'PACS_SERVER/study_5.dcm', 'Archived', '2026-03-26 09:24:35'),
(6, 11, 'PACS_SERVER/study_11.dcm', 'Archived', '2026-03-30 04:42:27'),
(7, 12, 'PACS_SERVER/study_12.dcm', 'Archived', '2026-03-30 05:20:06'),
(8, 13, 'PACS_SERVER/study_13.dcm', 'Archived', '2026-03-30 05:33:13'),
(9, 14, 'PACS_SERVER/study_14.dcm', 'Archived', '2026-03-30 09:51:50'),
(10, 15, 'PACS_SERVER/study_15.dcm', 'Archived', '2026-03-30 16:12:20'),
(11, 16, 'PACS_SERVER/study_16.dcm', 'Archived', '2026-03-30 16:31:17'),
(12, 17, 'PACS_SERVER/study_17.dcm', 'Archived', '2026-03-30 18:03:18'),
(13, 18, 'PACS_SERVER/study_18.dcm', 'Archived', '2026-03-30 18:25:31'),
(14, 19, 'PACS_SERVER/study_19.dcm', 'Archived', '2026-03-31 03:42:06'),
(15, 20, 'PACS_SERVER/study_20.dcm', 'Archived', '2026-03-31 05:03:53'),
(16, 21, 'PACS_SERVER/study_21.dcm', 'Archived', '2026-03-31 05:47:08'),
(17, 22, 'PACS_SERVER/study_22.dcm', 'Archived', '2026-03-31 05:57:20'),
(18, 23, 'PACS_SERVER/study_23.dcm', 'Archived', '2026-04-03 01:39:05'),
(19, 24, 'PACS_SERVER/study_24.dcm', 'Archived', '2026-04-03 01:59:21'),
(20, 25, 'PACS_SERVER/study_25.dcm', 'Archived', '2026-04-03 02:11:55'),
(21, 26, 'PACS_SERVER/study_26.dcm', 'Archived', '2026-04-03 02:34:30'),
(22, 27, 'PACS_SERVER/study_27.dcm', 'Archived', '2026-04-03 04:39:33'),
(23, 28, 'PACS_SERVER/study_28.dcm', 'Archived', '2026-04-03 06:15:46'),
(24, 29, 'PACS_SERVER/study_29.dcm', 'Archived', '2026-04-03 06:42:40');

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `id` int(11) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `mrn` varchar(50) DEFAULT NULL,
  `patient_code` varchar(50) DEFAULT NULL,
  `reason_for_xray` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`id`, `full_name`, `date_of_birth`, `gender`, `mrn`, `patient_code`, `reason_for_xray`, `created_at`) VALUES
(1, 'koduru Nishitha', '2026-02-04', 'female', '0535', NULL, 'lung cancer ', '2026-03-16 15:35:33'),
(2, 'vamsi begam', '2025-10-01', 'male', '1659', NULL, 'left lung infection cancer ', '2026-03-16 15:38:39'),
(3, 'Chinni krishna', '2026-02-14', 'male', '0659', NULL, 'chest infection ', '2026-03-16 15:40:24'),
(4, 'karthik', '2025-12-01', 'male', '1162', NULL, 'chest infection ', '2026-03-16 15:41:30'),
(5, 'saitejaswi', '2026-03-02', 'female', '4242', NULL, '', '2026-03-16 15:52:49'),
(6, 'mahendra  reddy', '2004-04-01', 'Male', '0555', NULL, 'forwarded to the radiology for scanning ', '2026-03-17 02:58:58'),
(7, 'vishal reddy', '2026-03-01', 'Male', '0342', NULL, 'N/A', '2026-03-17 03:03:20'),
(8, 'Anjali Sharma', '2026-03-03', 'female', '0234', NULL, 'lung cancer ', '2026-03-17 05:16:43'),
(9, 'Swathi', '2025-10-02', 'female', '0668', NULL, 'shortage of breathing ', '2026-03-17 08:12:36'),
(10, 'Sanjana Reddy', '2025-06-12', 'female', '0112', NULL, 'chest pain ', '2026-03-18 03:01:14'),
(11, 'Ramu', '2026-03-01', 'male', '0324', NULL, 'chest cancer ', '2026-03-18 03:11:57'),
(12, 'priya  reddy', '2026-03-01', 'Female', '0576', NULL, 'chest level abnormalities', '2026-03-19 04:04:53'),
(13, 'jaanu', '2026-03-10', 'female', '0579', NULL, 'chest infection ', '2026-03-19 04:19:53'),
(14, 'rani', '2026-03-18', 'female', '0987', NULL, 'rest of the chest ', '2026-03-19 04:22:16'),
(15, 'Sowmya', '2026-03-11', 'female', '0677', NULL, 'chest infection ', '2026-03-19 08:21:05'),
(16, 'raju', '2026-03-11', 'male', '0879', NULL, 'lung cancer ', '2026-03-19 08:34:44'),
(25, 'malli', '2026-03-02', 'male', '0654', NULL, 'chest broken ', '2026-03-25 04:11:10'),
(26, 'phani', '2026-04-25', 'male', '0932', NULL, 'chest infection', '2026-03-25 05:30:50'),
(27, 'Ammu', '2026-03-10', 'female', '0213', NULL, 'shortness of breath ', '2026-03-26 07:52:24'),
(28, 'sandhya', '2004-03-02', 'female', '0321', NULL, 'chestbroken', '2026-03-26 09:10:00'),
(29, 'anju Reddy', '2026-03-03', 'female', '0898', NULL, 'chest infection ', '2026-03-27 03:44:43'),
(30, 'jaan', '2026-01-14', 'male', '0945', NULL, 'chest infection ', '2026-03-27 03:46:38'),
(31, 'mahi', '2026-03-24', 'male', '0657', NULL, 'chest xray ', '2026-03-27 03:51:46'),
(32, 'lion', '2026-03-08', 'male', '0909', NULL, 'chest cancer ', '2026-03-27 04:19:28'),
(34, 'dhoni', '2026-03-02', 'male', '0007', NULL, 'chest right side pain', '2026-03-29 13:28:15'),
(35, 'rakshi', '2026-02-03', 'female', '0907', NULL, 'pneumonia ', '2026-03-29 14:14:49'),
(36, 'Test Test', '1990-01-01', 'male', 'MRN-TEST', NULL, 'Testing', '2026-03-29 15:36:16'),
(37, 'Deepthi', '2025-07-01', 'female', '0921', NULL, 'shortness of breath and chest right side infection ', '2026-03-29 16:51:35'),
(38, 'John Cena', '2026-01-04', 'male', '0567', NULL, 'chest xray infant diaper ', '2026-03-30 03:23:56'),
(40, 'Andrew', '2025-09-02', 'male', '0651', NULL, 'right lung cancer ', '2026-03-30 03:34:07'),
(41, 'Raju', '2026-03-18', 'male', '0435', NULL, 'chest xray ', '2026-03-30 03:54:11'),
(43, 'mohan', '2026-03-17', 'male', '0365', NULL, 'Chest pain ', '2026-03-30 03:56:58'),
(44, 'Rani', '2026-03-17', 'female', '0673', NULL, 'chest xray ', '2026-03-30 04:13:54'),
(45, 'jahnavi', '2026-03-09', 'male', '0432', NULL, 'pneumonia ', '2026-03-30 04:19:18'),
(46, 'Mary', '2026-02-02', 'female', '0999', NULL, 'chest xray ', '2026-03-30 04:31:34'),
(47, 'Sowmya', '2026-03-02', 'female', '0655', NULL, 'chest xray ', '2026-03-30 04:42:03'),
(48, 'priya', '2026-03-10', 'female', '0333', NULL, 'chest infection ', '2026-03-30 05:19:34'),
(49, 'Sandy', '2026-02-04', 'male', '0667', NULL, 'chest xray triage ', '2026-03-30 05:32:51'),
(50, 'Anu', '2025-12-11', 'female', '0777', NULL, 'chest infection ', '2026-03-30 09:51:11'),
(52, 'Dishitha', '2026-03-08', 'female', '0338', NULL, 'pneumonia ', '2026-03-30 15:03:03'),
(53, 'joshna', '2026-03-03', 'male', '0511', NULL, 'chest xray ', '2026-03-30 16:11:49'),
(54, 'ruchita', '2012-03-15', 'female', '0076', NULL, 'pneumonia ', '2026-03-30 16:30:37'),
(55, 'Dharani', '2007-04-05', 'female', '0888', NULL, 'chest cancer ', '2026-03-30 16:57:53'),
(57, 'kavya maran', '2006-03-30', 'female', '0773', NULL, 'chest xray infant ', '2026-03-30 17:24:24'),
(58, 'bhanu', '2026-02-09', 'male', '0211', NULL, 'chest xray ', '2026-03-30 18:02:50'),
(59, 'Mario', '2026-03-17', 'male', '0854', NULL, 'chest right side infection ', '2026-03-30 18:22:07'),
(61, 'yamini', '2026-03-10', 'female', '0500', NULL, 'chest xray ', '2026-03-30 18:25:03'),
(62, 'v Sharma', '2025-11-04', 'male', '0410', NULL, 'chest infection ', '2026-03-31 03:40:18'),
(64, 'Sushma Reddy', '2008-04-08', 'Female', '0232', NULL, 'Chest infection', '2026-03-31 04:20:27'),
(65, 'Ravi Kumar', '2026-03-10', 'male', '0787', NULL, 'chest xray ', '2026-03-31 04:59:09'),
(66, 'Vardhan', '2026-03-11', 'male', '0455', NULL, 'chest xray ', '2026-03-31 05:03:25'),
(70, 'sariyu chowdary', '2026-03-02', 'Female', '0798', NULL, 'chest xray', '2026-03-31 05:25:24'),
(71, 'Sai varshini', '2026-03-03', 'female', '1112', NULL, 'chest xray infant diaper infection ', '2026-03-31 05:46:45'),
(73, 'Nishitha Koduru', '2026-03-01', 'Female', '0552', NULL, 'soft lung replace ', '2026-03-31 05:56:18'),
(79, 'sai  ram', '2026-03-09', 'Male', '0118', NULL, 'chest xray', '2026-03-31 09:03:37'),
(81, 'Siri reddy', '2026-04-07', 'Female', '0550', NULL, 'N/A', '2026-04-03 01:34:48'),
(82, 'John  Ahmed', '2026-04-03', 'Male', '0924', NULL, 'N/A', '2026-04-03 01:45:24'),
(83, 'srilatha sri', '2026-04-16', 'Female', '0023', NULL, 'N/A', '2026-04-03 01:48:11'),
(84, 'shalini devi', '2026-02-01', 'Female', '0056', NULL, 'N/A', '2026-04-03 02:10:38'),
(85, 'gowthami reddy', '2026-04-01', 'Female', '0670', NULL, 'N/A', '2026-04-03 02:33:40'),
(86, 'Termi mani pal chand', '2026-01-01', 'male', '0156', NULL, '', '2026-04-03 04:33:28'),
(87, 'shri Prasad', '2026-04-07', 'male', '0045', NULL, '', '2026-04-03 06:15:23'),
(88, 'Shayam', '2026-04-02', 'male', '0145', NULL, 'chest xray triage ', '2026-04-03 06:29:59'),
(89, 'Shobin', '2026-04-08', 'male', '0178', NULL, 'chest infection ', '2026-04-03 06:42:02');

-- --------------------------------------------------------

--
-- Table structure for table `radiologist_reviews`
--

CREATE TABLE `radiologist_reviews` (
  `id` int(11) NOT NULL,
  `study_id` int(11) DEFAULT NULL,
  `doctor_name` varchar(100) DEFAULT NULL,
  `review_status` varchar(50) DEFAULT NULL,
  `review_notes` text DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ris_worklist`
--

CREATE TABLE `ris_worklist` (
  `id` int(11) NOT NULL,
  `study_id` int(11) DEFAULT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `worklist_status` varchar(50) DEFAULT NULL,
  `assigned_doctor` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ris_worklist`
--

INSERT INTO `ris_worklist` (`id`, `study_id`, `patient_id`, `worklist_status`, `assigned_doctor`, `created_at`) VALUES
(1, 11, 50, 'Pending Review', 'Dr. Mallavarapu Mahendra', '2026-03-30 04:42:27'),
(2, 12, 51, 'Pending Review', 'Dr. Sai Tejaswi', '2026-03-30 05:20:06'),
(3, 13, 52, 'Pending Review', 'Dr. Sai Tejaswi', '2026-03-30 05:33:13'),
(4, 14, 53, 'Pending Review', 'Dr. vamsi krishna', '2026-03-30 09:51:50'),
(5, 15, 55, 'Pending Review', 'Dr. Sai Tejaswi', '2026-03-30 16:12:20'),
(6, 16, 56, 'Pending Review', 'Dr. Sai Tejaswi', '2026-03-30 16:31:17'),
(7, 17, 59, 'Pending Review', 'Dr. Sai Tejaswi', '2026-03-30 18:03:18'),
(8, 18, 61, 'Pending Review', 'Dr. Mallavarapu Mahendra', '2026-03-30 18:25:31'),
(9, 19, 62, 'Pending Review', 'Dr. Sai Tejaswi', '2026-03-31 03:42:06'),
(10, 20, 64, 'Pending Review', 'Dr. Sai Tejaswi', '2026-03-31 05:03:53'),
(11, 21, 66, 'Pending Review', 'Dr. Mallavarapu Mahendra', '2026-03-31 05:47:08'),
(12, 22, 67, 'Pending Review', 'Dr. Mallavarapu Mahendra', '2026-03-31 05:57:20'),
(13, 23, 70, 'Pending Review', 'Dr. Mallavarapu Mahendra', '2026-04-03 01:39:05'),
(14, 24, 73, 'Pending Review', 'Dr. Mallavarapu Mahendra', '2026-04-03 01:59:21'),
(15, 25, 75, 'Pending Review', 'Dr. Mallavarapu Mahendra', '2026-04-03 02:11:55'),
(16, 26, 76, 'Pending Review', 'Dr. Mallavarapu Mahendra', '2026-04-03 02:34:30'),
(17, 27, 77, 'Pending Review', 'Dr. Mallavarapu Mahendra Reddy', '2026-04-03 04:39:33'),
(18, 28, 78, 'Pending Review', 'Dr. Mallavarapu Mahendra Reddy', '2026-04-03 06:15:46'),
(19, 29, 80, 'Pending Review', 'Dr. Mallavarapu Mahendra Reddy', '2026-04-03 06:42:40');

-- --------------------------------------------------------

--
-- Table structure for table `scans`
--

CREATE TABLE `scans` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `scan_id` varchar(50) DEFAULT NULL,
  `patient` varchar(100) DEFAULT NULL,
  `scan_type` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `scan_status` varchar(50) DEFAULT NULL,
  `scan_code` varchar(50) DEFAULT NULL,
  `review_status` varchar(50) DEFAULT NULL,
  `quality_validated_at` datetime DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `uploaded_at` datetime DEFAULT NULL,
  `exposure_level` varchar(50) DEFAULT NULL,
  `sharpness_level` varchar(50) DEFAULT NULL,
  `technician_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `scans`
--

INSERT INTO `scans` (`id`, `patient_id`, `scan_id`, `patient`, `scan_type`, `status`, `scan_status`, `scan_code`, `review_status`, `quality_validated_at`, `image_path`, `uploaded_at`, `exposure_level`, `sharpness_level`, `technician_id`, `created_at`) VALUES
(1, 1, NULL, NULL, NULL, 'started', 'Started', 'SCN-1001', NULL, NULL, 'uploaded_scans/scan_1.jpg', '2026-03-27 04:54:59', NULL, NULL, NULL, '2026-03-16 15:35:45'),
(2, 2, NULL, NULL, NULL, 'started', 'Completed', 'SCN-1002', 'Accepted', '2026-03-16 15:44:06', NULL, NULL, NULL, NULL, NULL, '2026-03-16 15:38:45'),
(3, 3, NULL, NULL, NULL, 'started', 'Started', 'SCN-1003', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-16 15:40:33'),
(4, 4, NULL, NULL, NULL, 'started', 'Started', 'SCN-1004', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-16 15:41:36'),
(5, 1, NULL, NULL, NULL, 'started', 'Started', 'SCN-1005', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-16 15:42:51'),
(6, 5, NULL, NULL, NULL, 'started', 'Started', 'SCN-1006', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-16 15:52:57'),
(7, 1, NULL, NULL, NULL, 'started', 'Started', 'SCN-1007', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-16 16:11:05'),
(8, 2, NULL, NULL, NULL, 'started', 'Started', 'SCN-1008', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-16 16:11:12'),
(9, 3, NULL, NULL, NULL, 'started', 'Started', 'SCN-1009', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-16 16:11:19'),
(10, 1, NULL, NULL, NULL, 'started', 'Started', 'SCN-1010', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-17 02:59:29'),
(11, 1, NULL, NULL, NULL, 'started', 'Started', 'SCN-1011', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-17 03:01:19'),
(12, 8, NULL, NULL, NULL, 'started', 'Started', 'SCN-1012', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-17 05:16:53'),
(13, 9, NULL, NULL, NULL, 'started', 'Started', 'SCN-1013', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-17 08:12:43'),
(14, 10, NULL, NULL, NULL, 'started', 'Started', 'SCN-1014', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-18 03:01:25'),
(15, 11, NULL, NULL, NULL, 'started', 'Started', 'SCN-1015', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-18 03:12:03'),
(16, 12, NULL, NULL, NULL, 'started', 'Started', 'SCN-1016', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-19 04:04:57'),
(17, 13, NULL, NULL, NULL, 'started', 'Started', 'SCN-1017', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-19 04:20:00'),
(18, 14, NULL, NULL, NULL, 'started', 'Started', 'SCN-1018', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-19 04:22:24'),
(19, 15, NULL, NULL, NULL, 'started', 'Started', 'SCN-1019', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-19 08:21:12'),
(20, 16, NULL, NULL, NULL, 'started', 'Started', 'SCN-1020', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-19 08:34:50'),
(21, 17, NULL, NULL, NULL, 'started', 'Started', 'SCN-1021', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-19 08:48:55'),
(22, 18, NULL, NULL, NULL, 'started', 'Started', 'SCN-1022', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-19 08:49:59'),
(23, 22, NULL, NULL, NULL, 'started', 'Started', 'SCN-1023', NULL, NULL, 'uploaded_scans/scan_23.jpg', '2026-03-20 08:09:47', NULL, NULL, NULL, '2026-03-20 08:09:20'),
(24, 23, NULL, NULL, NULL, 'started', 'Started', 'SCN-1024', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-24 03:30:15'),
(25, 24, NULL, NULL, NULL, 'started', 'Started', 'SCN-1025', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-24 04:45:15'),
(26, 25, NULL, NULL, NULL, 'started', 'Completed', 'SCN-1026', 'Accepted', '2026-03-25 05:37:03', 'uploaded_scans/scan_26.jpg', '2026-03-25 05:36:33', NULL, NULL, NULL, '2026-03-25 04:11:18'),
(27, 26, NULL, NULL, NULL, 'started', 'Started', 'SCN-1027', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-25 05:31:39'),
(28, 27, NULL, NULL, NULL, 'started', 'Started', 'SCN-1028', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-26 07:52:32'),
(29, 28, NULL, NULL, NULL, 'started', 'Completed', 'SCN-1029', 'Accepted', '2026-03-26 09:15:37', 'uploaded_scans/scan_29.jpg', '2026-03-26 09:14:59', NULL, NULL, NULL, '2026-03-26 09:10:46'),
(30, 29, NULL, NULL, NULL, 'started', 'Started', 'SCN-1030', NULL, NULL, 'uploaded_scans/scan_30.jpg', '2026-03-27 05:19:16', NULL, NULL, NULL, '2026-03-27 03:44:52'),
(31, 30, NULL, NULL, NULL, 'started', 'Started', 'SCN-1031', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-27 03:46:43'),
(32, 31, NULL, NULL, NULL, 'started', 'Started', 'SCN-1032', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-27 03:51:52'),
(33, 32, NULL, NULL, NULL, 'started', 'Started', 'SCN-1033', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-27 04:19:35'),
(34, 32, NULL, NULL, NULL, 'started', 'Started', 'SCN-1034', NULL, NULL, 'uploaded_scans/scan_34.jpg', '2026-03-27 05:00:20', NULL, NULL, NULL, '2026-03-27 04:59:23'),
(35, 10, NULL, NULL, NULL, 'started', 'Started', 'SCN-1035', NULL, NULL, 'uploaded_scans/scan_35.jpg', '2026-03-27 06:54:24', NULL, NULL, NULL, '2026-03-27 06:50:21'),
(36, 27, NULL, NULL, NULL, 'started', 'Started', 'SCN-1036', NULL, NULL, 'uploaded_scans/scan_36.jpg', '2026-03-27 07:27:44', NULL, NULL, NULL, '2026-03-27 07:27:19'),
(37, 33, NULL, NULL, NULL, 'started', 'Started', 'SCN-1037', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-27 16:43:13'),
(38, 34, NULL, NULL, NULL, 'started', 'Started', 'SCN-1038', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-29 13:29:16'),
(39, 35, NULL, NULL, NULL, 'started', 'Started', 'SCN-1039', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-29 14:16:21'),
(40, 35, NULL, NULL, NULL, 'started', 'Started', 'SCN-1040', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-29 14:16:31'),
(41, 37, NULL, NULL, NULL, 'started', 'Started', 'SCN-1041', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-29 16:52:08'),
(42, 38, NULL, NULL, NULL, 'started', 'Started', 'SCN-1042', NULL, NULL, 'uploaded_scans/scan_42.jpg', '2026-03-30 03:25:03', NULL, NULL, NULL, '2026-03-30 03:24:41'),
(43, 40, NULL, NULL, NULL, 'started', 'Started', 'SCN-1043', NULL, NULL, 'uploaded_scans/scan_43.jpg', '2026-03-30 03:34:43', NULL, NULL, NULL, '2026-03-30 03:34:25'),
(44, 41, NULL, NULL, NULL, 'started', 'Started', 'SCN-1044', NULL, NULL, 'uploaded_scans/scan_44.jpg', '2026-03-30 03:54:36', NULL, NULL, 7, '2026-03-30 03:54:19'),
(45, 43, NULL, NULL, NULL, 'started', 'Started', 'SCN-1045', NULL, NULL, 'uploaded_scans/scan_45.jpg', '2026-03-30 03:57:17', NULL, NULL, 7, '2026-03-30 03:57:05'),
(46, 44, NULL, NULL, NULL, 'started', 'Started', 'SCN-1046', NULL, NULL, 'uploaded_scans/scan_46.jpg', '2026-03-30 04:14:21', NULL, NULL, 7, '2026-03-30 04:14:00'),
(47, 101, NULL, NULL, NULL, 'started', 'Started', 'SCN-1047', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-30 04:18:48'),
(48, 45, NULL, NULL, NULL, 'started', 'Started', 'SCN-1048', NULL, NULL, 'uploaded_scans/scan_48.jpg', '2026-03-30 04:19:37', NULL, NULL, 7, '2026-03-30 04:19:22'),
(49, 46, NULL, NULL, NULL, 'started', 'Started', 'SCN-1049', NULL, NULL, 'uploaded_scans/scan_49.jpg', '2026-03-30 04:31:50', NULL, NULL, 7, '2026-03-30 04:31:39'),
(50, 47, NULL, NULL, NULL, 'started', 'Started', 'SCN-1050', NULL, NULL, 'uploaded_scans/scan_50.jpg', '2026-03-30 04:42:22', NULL, NULL, 7, '2026-03-30 04:42:09'),
(51, 48, NULL, NULL, NULL, 'started', 'Started', 'SCN-1051', NULL, NULL, 'uploaded_scans/scan_51.jpg', '2026-03-30 05:19:53', NULL, NULL, 7, '2026-03-30 05:19:39'),
(52, 49, NULL, NULL, NULL, 'started', 'Started', 'SCN-1052', NULL, NULL, 'uploaded_scans/scan_52.jpg', '2026-03-30 05:33:08', NULL, NULL, 7, '2026-03-30 05:32:55'),
(53, 50, NULL, NULL, NULL, 'started', 'Started', 'SCN-1053', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-30 09:51:19'),
(54, 52, NULL, NULL, NULL, 'started', 'Started', 'SCN-1054', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-30 15:03:11'),
(55, 53, NULL, NULL, NULL, 'started', 'Started', 'SCN-1055', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-30 16:11:54'),
(56, 54, NULL, NULL, NULL, 'started', 'Started', 'SCN-1056', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-30 16:30:49'),
(57, 55, NULL, NULL, NULL, 'started', 'Started', 'SCN-1057', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-30 16:57:59'),
(58, 57, NULL, NULL, NULL, 'started', 'Started', 'SCN-1058', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-30 17:24:31'),
(59, 58, NULL, NULL, NULL, 'started', 'Started', 'SCN-1059', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-30 18:02:55'),
(60, 59, NULL, NULL, NULL, 'started', 'Started', 'SCN-1060', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-30 18:22:13'),
(61, 61, NULL, NULL, NULL, 'started', 'Started', 'SCN-1061', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-30 18:25:08'),
(62, 62, NULL, NULL, NULL, 'started', 'Started', 'SCN-1062', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-31 03:40:27'),
(63, 65, NULL, NULL, NULL, 'started', 'Started', 'SCN-1063', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-31 04:59:14'),
(64, 66, NULL, NULL, NULL, 'started', 'Started', 'SCN-1064', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-31 05:03:29'),
(65, 70, NULL, NULL, NULL, 'started', 'Started', 'SCN-1065', NULL, NULL, 'uploaded_scans/scan_65.jpg', '2026-03-31 05:36:37', NULL, NULL, 9, '2026-03-31 05:25:27'),
(66, 71, NULL, NULL, NULL, 'started', 'Started', 'SCN-1066', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-03-31 05:46:50'),
(67, 73, NULL, NULL, NULL, 'started', 'Started', 'SCN-1067', NULL, NULL, 'uploaded_scans/scan_67.jpg', '2026-03-31 05:56:54', NULL, NULL, 9, '2026-03-31 05:56:20'),
(68, 79, NULL, NULL, NULL, 'started', 'Started', 'SCN-1068', NULL, NULL, NULL, NULL, NULL, NULL, 12, '2026-03-31 09:03:45'),
(69, 81, NULL, NULL, NULL, 'started', 'Started', 'SCN-1069', NULL, NULL, NULL, NULL, NULL, NULL, 9, '2026-04-03 01:34:50'),
(70, 81, NULL, NULL, NULL, 'started', 'Started', 'SCN-1070', NULL, NULL, 'uploaded_scans/scan_70.jpg', '2026-04-03 01:38:40', NULL, NULL, 9, '2026-04-03 01:35:10'),
(71, 1, NULL, NULL, NULL, 'started', 'Started', 'SCN-1071', NULL, NULL, NULL, NULL, NULL, NULL, 9, '2026-04-03 01:43:14'),
(72, 82, NULL, NULL, NULL, 'started', 'Started', 'SCN-1072', NULL, NULL, NULL, NULL, NULL, NULL, 9, '2026-04-03 01:45:26'),
(73, 83, NULL, NULL, NULL, 'started', 'Started', 'SCN-1073', NULL, NULL, 'uploaded_scans/scan_73.jpg', '2026-04-03 01:59:03', NULL, NULL, 9, '2026-04-03 01:48:15'),
(74, 1, NULL, NULL, NULL, 'started', 'Started', 'SCN-1074', NULL, NULL, NULL, NULL, NULL, NULL, 9, '2026-04-03 02:04:54'),
(75, 84, NULL, NULL, NULL, 'started', 'Started', 'SCN-1075', NULL, NULL, 'uploaded_scans/scan_75.jpg', '2026-04-03 02:11:43', NULL, NULL, 9, '2026-04-03 02:10:41'),
(76, 85, NULL, NULL, NULL, 'started', 'Started', 'SCN-1076', NULL, NULL, 'uploaded_scans/scan_76.jpg', '2026-04-03 02:34:13', NULL, NULL, 9, '2026-04-03 02:33:44'),
(77, 86, NULL, NULL, NULL, 'started', 'Started', 'SCN-1077', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-04-03 04:33:37'),
(78, 87, NULL, NULL, NULL, 'started', 'Started', 'SCN-1078', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-04-03 06:15:30'),
(79, 88, NULL, NULL, NULL, 'started', 'Started', 'SCN-1079', NULL, NULL, NULL, NULL, NULL, NULL, 7, '2026-04-03 06:30:05'),
(80, 89, NULL, NULL, NULL, 'started', 'Started', 'SCN-1080', NULL, NULL, 'uploaded_scans/scan_80.jpg', '2026-04-03 06:42:32', NULL, NULL, 7, '2026-04-03 06:42:07');

-- --------------------------------------------------------

--
-- Table structure for table `scan_preparations`
--

CREATE TABLE `scan_preparations` (
  `id` int(11) NOT NULL,
  `scan_id` int(11) DEFAULT NULL,
  `position_patient` tinyint(1) DEFAULT NULL,
  `proper_distance` tinyint(1) DEFAULT NULL,
  `radiation_safety` tinyint(1) DEFAULT NULL,
  `remove_metal` tinyint(1) DEFAULT NULL,
  `calibration_verified` tinyint(1) DEFAULT NULL,
  `exposure_settings` tinyint(1) DEFAULT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `scan_preparations`
--

INSERT INTO `scan_preparations` (`id`, `scan_id`, `position_patient`, `proper_distance`, `radiation_safety`, `remove_metal`, `calibration_verified`, `exposure_settings`, `patient_id`, `created_at`) VALUES
(1, 1, 1, 1, 1, 1, 1, 1, NULL, '2026-03-16 15:35:45'),
(2, 2, 1, 1, 1, 1, 1, 1, NULL, '2026-03-16 15:38:46'),
(3, 3, 1, 1, 1, 1, 1, 1, NULL, '2026-03-16 15:40:33'),
(4, 4, 1, 1, 1, 1, 1, 1, NULL, '2026-03-16 15:41:36'),
(5, 6, 1, 1, 1, 1, 1, 1, NULL, '2026-03-16 15:52:57'),
(6, 10, 1, 1, 1, 1, 1, 1, NULL, '2026-03-17 02:59:57'),
(7, 12, 1, 1, 1, 1, 1, 1, NULL, '2026-03-17 05:16:54'),
(8, 13, 1, 1, 1, 1, 1, 1, NULL, '2026-03-17 08:12:43'),
(9, 14, 1, 1, 1, 1, 1, 1, NULL, '2026-03-18 03:01:25'),
(10, 15, 1, 1, 1, 1, 1, 1, NULL, '2026-03-18 03:12:03'),
(11, 16, 1, 1, 1, 1, 1, 1, NULL, '2026-03-19 04:05:16'),
(12, 17, 1, 1, 1, 1, 1, 1, NULL, '2026-03-19 04:20:00'),
(13, 18, 1, 1, 1, 1, 1, 1, NULL, '2026-03-19 04:22:24'),
(14, 19, 1, 1, 1, 1, 1, 1, NULL, '2026-03-19 08:21:12'),
(15, 20, 1, 1, 1, 1, 1, 1, NULL, '2026-03-19 08:34:50'),
(16, 21, 1, 1, 1, 1, 1, 1, NULL, '2026-03-19 08:48:55'),
(17, 22, 1, 1, 1, 1, 1, 1, NULL, '2026-03-19 08:49:59'),
(18, 23, 1, 1, 1, 1, 1, 1, NULL, '2026-03-20 08:09:28'),
(19, 24, 1, 1, 1, 1, 1, 1, NULL, '2026-03-24 03:30:15'),
(20, 25, 1, 1, 1, 1, 1, 1, NULL, '2026-03-24 04:45:15'),
(21, 26, 1, 1, 1, 1, 1, 1, NULL, '2026-03-25 04:11:18'),
(22, 26, 0, 1, 1, 1, 1, 1, NULL, '2026-03-25 05:33:03'),
(23, 28, 1, 1, 1, 1, 1, 1, NULL, '2026-03-26 07:52:32'),
(24, 29, 1, 1, 0, 1, 0, 1, NULL, '2026-03-26 09:11:19'),
(25, 30, 1, 1, 1, 1, 1, 1, NULL, '2026-03-27 03:44:52'),
(26, 31, 1, 1, 1, 1, 1, 1, NULL, '2026-03-27 03:46:43'),
(27, 32, 1, 1, 1, 1, 1, 1, NULL, '2026-03-27 03:51:52'),
(28, 33, 1, 1, 1, 1, 1, 1, NULL, '2026-03-27 04:19:35'),
(29, 37, 1, 1, 1, 1, 1, 1, NULL, '2026-03-27 16:43:13'),
(30, 38, 1, 1, 1, 1, 1, 1, NULL, '2026-03-29 13:29:16'),
(31, 39, 1, 1, 1, 1, 1, 1, NULL, '2026-03-29 14:16:21'),
(32, 40, 1, 1, 1, 1, 1, 1, NULL, '2026-03-29 14:16:31'),
(33, 41, 1, 1, 1, 1, 1, 1, NULL, '2026-03-29 16:52:09'),
(34, 42, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 03:24:41'),
(35, 43, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 03:34:25'),
(36, 44, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 03:54:19'),
(37, 45, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 03:57:06'),
(38, 46, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 04:14:00'),
(39, 47, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 04:18:48'),
(40, 48, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 04:19:22'),
(41, 49, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 04:31:39'),
(42, 50, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 04:42:09'),
(43, 51, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 05:19:39'),
(44, 52, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 05:32:55'),
(45, 53, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 09:51:19'),
(46, 54, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 15:03:11'),
(47, 55, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 16:11:54'),
(48, 56, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 16:30:49'),
(49, 57, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 16:58:00'),
(50, 58, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 17:24:31'),
(51, 59, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 18:02:55'),
(52, 60, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 18:22:13'),
(53, 61, 1, 1, 1, 1, 1, 1, NULL, '2026-03-30 18:25:08'),
(54, 62, 1, 1, 1, 1, 1, 1, NULL, '2026-03-31 03:40:27'),
(55, 63, 1, 1, 1, 1, 1, 1, NULL, '2026-03-31 04:59:14'),
(56, 64, 1, 1, 1, 1, 1, 1, NULL, '2026-03-31 05:03:29'),
(57, 65, 1, 1, 1, 1, 1, 1, NULL, '2026-03-31 05:25:36'),
(58, 66, 1, 1, 1, 1, 1, 1, NULL, '2026-03-31 05:46:50'),
(59, 67, 1, 1, 1, 1, 1, 1, NULL, '2026-03-31 05:56:36'),
(60, 68, 1, 1, 1, 1, 1, 1, NULL, '2026-03-31 09:04:12'),
(61, 69, 1, 1, 1, 1, 1, 1, NULL, '2026-04-03 01:35:01'),
(62, 70, 1, 1, 1, 1, 1, 1, NULL, '2026-04-03 01:35:18'),
(63, 72, 1, 1, 1, 1, 1, 1, NULL, '2026-04-03 01:45:34'),
(64, 73, 1, 1, 1, 1, 1, 1, NULL, '2026-04-03 01:48:24'),
(65, 75, 1, 1, 1, 1, 1, 1, NULL, '2026-04-03 02:10:49'),
(66, 76, 1, 1, 1, 1, 1, 1, NULL, '2026-04-03 02:33:52'),
(67, 77, 1, 1, 1, 1, 1, 1, NULL, '2026-04-03 04:33:37'),
(68, 78, 1, 1, 1, 1, 1, 1, NULL, '2026-04-03 06:15:30'),
(69, 79, 1, 1, 1, 1, 1, 1, NULL, '2026-04-03 06:30:05'),
(70, 80, 1, 1, 1, 1, 1, 1, NULL, '2026-04-03 06:42:07');

-- --------------------------------------------------------

--
-- Table structure for table `studies`
--

CREATE TABLE `studies` (
  `id` int(11) NOT NULL,
  `scan_id` int(11) DEFAULT NULL,
  `session_id` varchar(100) DEFAULT NULL,
  `dicom_path` varchar(255) DEFAULT NULL,
  `file_size_mb` float DEFAULT NULL,
  `upload_progress` int(11) DEFAULT NULL,
  `study_status` varchar(50) DEFAULT NULL,
  `assigned_doctor` varchar(100) DEFAULT NULL,
  `encrypted` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `studies`
--

INSERT INTO `studies` (`id`, `scan_id`, `session_id`, `dicom_path`, `file_size_mb`, `upload_progress`, `study_status`, `assigned_doctor`, `encrypted`, `created_at`) VALUES
(1, 1, '4D0784-XP-SAFE', 'dicom_packages/scan_1.dcm', 14.2, 95, 'Distributed', 'Dr. Bennett', 1, '2026-03-16 16:20:40'),
(2, 2, '42BEB6-XP-SAFE', 'dicom_packages/scan_2.dcm', 14.2, 90, 'Distributed', 'Dr. Bennett', 1, '2026-03-16 16:20:47'),
(3, 3, '04C0EA-XP-SAFE', 'dicom_packages/scan_3.dcm', 14.2, 90, 'Distributed', 'Dr. Bennett', 1, '2026-03-16 16:20:52'),
(4, 4, '4E281E-XP-SAFE', 'dicom_packages/scan_4.dcm', 14.2, 90, 'Distributed', 'Dr. Bennett', 1, '2026-03-16 16:20:57'),
(5, 29, '9B8AF6-XP-SAFE', 'dicom_packages/scan_29.dcm', 14.2, 90, 'Distributed', 'Dr. Bennett', 1, '2026-03-26 09:16:51'),
(6, 49, '5EA71F-XP-SAFE', 'dicom_packages/scan_49.dcm', 14.2, 0, 'Processing', 'Dr. Mallavarapu Mahendra', 1, '2026-03-30 04:31:57'),
(7, 49, '33AA8B-XP-SAFE', 'dicom_packages/scan_49.dcm', 14.2, 0, 'Processing', 'Dr. Mallavarapu Mahendra', 1, '2026-03-30 04:32:07'),
(8, 49, '6A309C-XP-SAFE', 'dicom_packages/scan_49.dcm', 14.2, 0, 'Processing', 'Dr. Mallavarapu Mahendra', 1, '2026-03-30 04:32:08'),
(9, 49, '0B65FF-XP-SAFE', 'dicom_packages/scan_49.dcm', 14.2, 0, 'Processing', 'Dr. John doe', 1, '2026-03-30 04:32:12'),
(10, 49, '9F7D6F-XP-SAFE', 'dicom_packages/scan_49.dcm', 14.2, 0, 'Processing', 'Dr. John doe', 1, '2026-03-30 04:32:15'),
(11, 50, '17E93E-XP-SAFE', 'dicom_packages/scan_50.dcm', 14.2, 0, 'Distributed', 'Dr. Mallavarapu Mahendra', 1, '2026-03-30 04:42:27'),
(12, 51, '99F4AA-XP-SAFE', 'dicom_packages/scan_51.dcm', 14.2, 0, 'Distributed', 'Dr. Sai Tejaswi', 1, '2026-03-30 05:20:06'),
(13, 52, '836F77-XP-SAFE', 'dicom_packages/scan_52.dcm', 14.2, 0, 'Distributed', 'Dr. Sai Tejaswi', 1, '2026-03-30 05:33:13'),
(14, 53, 'DA335D-XP-SAFE', 'dicom_packages/scan_53.dcm', 14.2, 0, 'Distributed', 'Dr. vamsi krishna', 1, '2026-03-30 09:51:50'),
(15, 55, 'BBAF04-XP-SAFE', 'dicom_packages/scan_55.dcm', 14.2, 0, 'Distributed', 'Dr. Sai Tejaswi', 1, '2026-03-30 16:12:20'),
(16, 56, '9FF9D6-XP-SAFE', 'dicom_packages/scan_56.dcm', 14.2, 0, 'Distributed', 'Dr. Sai Tejaswi', 1, '2026-03-30 16:31:17'),
(17, 59, '4F7D86-XP-SAFE', 'dicom_packages/scan_59.dcm', 14.2, 0, 'Distributed', 'Dr. Sai Tejaswi', 1, '2026-03-30 18:03:18'),
(18, 61, '010C80-XP-SAFE', 'dicom_packages/scan_61.dcm', 14.2, 0, 'Distributed', 'Dr. Mallavarapu Mahendra', 1, '2026-03-30 18:25:31'),
(19, 62, 'B4A6CE-XP-SAFE', 'dicom_packages/scan_62.dcm', 14.2, 0, 'Distributed', 'Dr. Sai Tejaswi', 1, '2026-03-31 03:42:05'),
(20, 64, '224F45-XP-SAFE', 'dicom_packages/scan_64.dcm', 14.2, 0, 'Distributed', 'Dr. Sai Tejaswi', 1, '2026-03-31 05:03:53'),
(21, 66, '54A5E4-XP-SAFE', 'dicom_packages/scan_66.dcm', 14.2, 0, 'Distributed', 'Dr. Mallavarapu Mahendra', 1, '2026-03-31 05:47:08'),
(22, 67, 'CEBD32-XP-SAFE', 'dicom_packages/scan_67.dcm', 14.2, 0, 'Distributed', 'Dr. Mallavarapu Mahendra', 1, '2026-03-31 05:57:20'),
(23, 70, '705E44-XP-SAFE', 'dicom_packages/scan_70.dcm', 14.2, 0, 'Distributed', 'Dr. Mallavarapu Mahendra', 1, '2026-04-03 01:39:04'),
(24, 73, 'FD7E43-XP-SAFE', 'dicom_packages/scan_73.dcm', 14.2, 0, 'Distributed', 'Dr. Mallavarapu Mahendra', 1, '2026-04-03 01:59:20'),
(25, 75, '174A20-XP-SAFE', 'dicom_packages/scan_75.dcm', 14.2, 0, 'Distributed', 'Dr. Mallavarapu Mahendra', 1, '2026-04-03 02:11:55'),
(26, 76, '8AC190-XP-SAFE', 'dicom_packages/scan_76.dcm', 14.2, 0, 'Distributed', 'Dr. Mallavarapu Mahendra', 1, '2026-04-03 02:34:30'),
(27, 77, '62A534-XP-SAFE', 'dicom_packages/scan_77.dcm', 14.2, 0, 'Distributed', 'Dr. Mallavarapu Mahendra Reddy', 1, '2026-04-03 04:39:33'),
(28, 78, 'F5DE19-XP-SAFE', 'dicom_packages/scan_78.dcm', 14.2, 0, 'Distributed', 'Dr. Mallavarapu Mahendra Reddy', 1, '2026-04-03 06:15:45'),
(29, 80, 'E54917-XP-SAFE', 'dicom_packages/scan_80.dcm', 14.2, 0, 'Distributed', 'Dr. Mallavarapu Mahendra Reddy', 1, '2026-04-03 06:42:40');

-- --------------------------------------------------------

--
-- Table structure for table `support_tickets`
--

CREATE TABLE `support_tickets` (
  `id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `status` varchar(50) DEFAULT 'OPEN',
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `support_tickets`
--

INSERT INTO `support_tickets` (`id`, `doctor_id`, `message`, `status`, `created_at`) VALUES
(1, 1, 'Unable to view scan report', 'OPEN', '2026-03-16 20:37:26'),
(2, 2, 'AI prediction not loading', 'OPEN', '2026-03-16 20:37:26'),
(3, 0, 'nothing', 'OPEN', '2026-03-16 15:07:35'),
(4, 0, 'nothing', 'OPEN', '2026-03-16 15:07:55');

-- --------------------------------------------------------

--
-- Table structure for table `technicians`
--

CREATE TABLE `technicians` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `role_requested` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `profile_photo` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `technicians`
--

INSERT INTO `technicians` (`id`, `first_name`, `last_name`, `email`, `phone_number`, `role_requested`, `password`, `created_at`, `profile_photo`) VALUES
(7, 'greeshma', 'malineni', 'mahendramallavarapu532@gmail.com', '9398523694', 'technician', 'Ammulu@2004', '2026-03-25 04:08:26', NULL),
(8, 'chotu', 'kisik', 'mahiiloveubangaram2004@gmail.com', '9640638489', 'technician', 'Ammulu@298', '2026-03-26 06:43:55', NULL),
(9, 'Preethi', 'Reddy', 'mahendramallavarapu555@gmail.com', '7386997732', 'technician', 'Preethi@1234', '2026-03-30 16:42:13', NULL),
(10, 'Test', 'Tech', 'test.tech@hospital.com', '8765432109', 'technician', 'Password123!', '2026-03-31 05:11:03', NULL),
(11, 'Ramya', 'Reddy', 'yaswanthmallavarapu8@gmail.com', '8211136978', 'technician', 'Mahi@1234', '2026-03-31 08:56:11', NULL),
(12, 'Teju', 'sri', 'molakathallasaitejaswi4242.sse@saveetha.com', '8232469692', 'technician', 'Ammulu@2002', '2026-03-31 08:59:07', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `technician_password_reset_otp`
--

CREATE TABLE `technician_password_reset_otp` (
  `id` int(11) NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `otp_code` varchar(10) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `expires_at` datetime DEFAULT NULL,
  `is_used` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `technician_password_reset_otp`
--

INSERT INTO `technician_password_reset_otp` (`id`, `email`, `otp_code`, `created_at`, `expires_at`, `is_used`) VALUES
(1, 'mahendramallavarapu532@gmail.com', '636506', '2026-03-16 15:18:42', '2026-03-16 15:23:42', 1),
(2, 'mahendramallavarapu555@gmail.com', '555556', '2026-03-16 15:20:30', '2026-03-16 15:25:30', 1);

-- --------------------------------------------------------

--
-- Table structure for table `triage_cases`
--

CREATE TABLE `triage_cases` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `patient_name` varchar(100) DEFAULT NULL,
  `patient_age` int(11) DEFAULT NULL,
  `diagnosis` varchar(255) DEFAULT NULL,
  `priority` enum('CRITICAL','URGENT','ROUTINE') DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `ai_findings` text DEFAULT NULL,
  `ai_confidence` int(11) DEFAULT NULL,
  `final_diagnosis` varchar(255) DEFAULT NULL,
  `doctor_notes` text DEFAULT NULL,
  `decision` enum('PENDING','ACCEPTED','REJECTED') DEFAULT NULL,
  `status` enum('PENDING','COMPLETED') DEFAULT NULL,
  `report_id` varchar(50) DEFAULT NULL,
  `finalized` tinyint(1) DEFAULT NULL,
  `signed_by` varchar(150) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL,
  `case_code` varchar(20) DEFAULT NULL,
  `ai_result` varchar(100) DEFAULT NULL,
  `doctor_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `triage_cases`
--

INSERT INTO `triage_cases` (`id`, `patient_id`, `patient_name`, `patient_age`, `diagnosis`, `priority`, `image_url`, `ai_findings`, `ai_confidence`, `final_diagnosis`, `doctor_notes`, `decision`, `status`, `report_id`, `finalized`, `signed_by`, `created_at`, `reviewed_at`, `case_code`, `ai_result`, `doctor_id`) VALUES
(20, 29, 'anju Reddy', 0, 'Normal', 'ROUTINE', 'uploaded_scans/scan_30.jpg', 'Detected Normal', 52, NULL, NULL, 'ACCEPTED', 'COMPLETED', NULL, 1, '', '2026-03-27 05:19:16', '2026-03-27 09:18:28', 'SC-5520', 'Normal', 11),
(21, 10, 'Sanjana Reddy', 0, 'Normal', 'ROUTINE', 'uploaded_scans/scan_35.jpg', 'Detected Normal', 51, NULL, NULL, 'PENDING', 'PENDING', NULL, 0, NULL, '2026-03-27 06:54:28', NULL, 'SC-5521', 'Normal', 12),
(22, 27, 'Ammu', 0, 'Normal', 'ROUTINE', 'uploaded_scans/scan_36.jpg', 'Detected Normal', 51, NULL, NULL, 'PENDING', 'PENDING', NULL, 0, NULL, '2026-03-27 07:27:45', NULL, 'SC-5522', 'Normal', 12),
(33, 70, 'sariyu chowdary', 0, 'Normal', 'ROUTINE', 'uploaded_scans/scan_65.jpg', 'Detected Normal', 51, NULL, NULL, 'PENDING', 'PENDING', NULL, 0, NULL, '2026-03-31 05:36:38', NULL, 'SC-5533', 'Normal', 12),
(34, 73, 'Nishitha Koduru', 0, 'Normal', 'ROUTINE', 'uploaded_scans/scan_67.jpg', 'Detected Normal', 55, NULL, NULL, 'PENDING', 'PENDING', NULL, 0, NULL, '2026-03-31 05:56:55', NULL, 'SC-5534', 'Normal', 11),
(35, 81, 'Siri reddy', -1, 'Normal', 'ROUTINE', 'uploaded_scans/scan_70.jpg', 'Detected Normal', 50, NULL, NULL, 'PENDING', 'PENDING', NULL, 0, NULL, '2026-04-03 01:38:42', NULL, 'SC-5535', 'Normal', 11),
(36, 83, 'srilatha sri', -1, 'Normal', 'ROUTINE', 'uploaded_scans/scan_73.jpg', 'Detected Normal', 52, NULL, NULL, 'PENDING', 'PENDING', NULL, 0, NULL, '2026-04-03 01:59:03', NULL, 'SC-5536', 'Normal', 11),
(37, 84, 'shalini devi', 0, 'Normal', 'URGENT', 'uploaded_scans/scan_75.jpg', 'Detected Normal', 56, '', 'ICD-10: J18.9\n\n', 'ACCEPTED', 'COMPLETED', NULL, 0, NULL, '2026-04-03 02:11:44', '2026-04-03 02:46:14', 'SC-5537', 'Normal', 11),
(38, 85, 'gowthami reddy', 0, 'Normal', 'URGENT', 'uploaded_scans/scan_76.jpg', 'Detected Normal', 54, 'No specific findings detected.', 'Clinical correlation recommended. Consider repeat CXR in 4–6 weeks after treatment.\n\nClinical Notes: ICD-10: J18.9\n\n', 'ACCEPTED', 'COMPLETED', NULL, 1, 'Mallavarapu Mahendra', '2026-04-03 02:34:14', '2026-04-03 03:10:20', 'SC-5538', 'Normal', 11),
(39, 89, 'Shobin', -1, 'Normal', 'ROUTINE', 'uploaded_scans/scan_80.jpg', 'Detected Normal', 50, NULL, NULL, 'PENDING', 'PENDING', NULL, 0, NULL, '2026-04-03 06:42:36', NULL, 'SC-5539', 'Normal', 11);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ai_analysis`
--
ALTER TABLE `ai_analysis`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_id` (`study_id`),
  ADD KEY `ix_ai_analysis_id` (`id`);

--
-- Indexes for table `cases`
--
ALTER TABLE `cases`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `ix_cases_id` (`id`);

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `hospital_email` (`hospital_email`),
  ADD UNIQUE KEY `phone_number` (`phone_number`),
  ADD KEY `ix_doctors_id` (`id`);

--
-- Indexes for table `doctor_privacy_settings`
--
ALTER TABLE `doctor_privacy_settings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_doctor_privacy_settings_id` (`id`);

--
-- Indexes for table `faqs`
--
ALTER TABLE `faqs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `feedbacks`
--
ALTER TABLE `feedbacks`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pacs_archives`
--
ALTER TABLE `pacs_archives`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_id` (`study_id`),
  ADD KEY `ix_pacs_archives_id` (`id`);

--
-- Indexes for table `patient`
--
ALTER TABLE `patient`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `mrn` (`mrn`),
  ADD UNIQUE KEY `patient_code` (`patient_code`),
  ADD KEY `ix_patient_id` (`id`);

--
-- Indexes for table `radiologist_reviews`
--
ALTER TABLE `radiologist_reviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_id` (`study_id`),
  ADD KEY `ix_radiologist_reviews_id` (`id`);

--
-- Indexes for table `ris_worklist`
--
ALTER TABLE `ris_worklist`
  ADD PRIMARY KEY (`id`),
  ADD KEY `study_id` (`study_id`),
  ADD KEY `ix_ris_worklist_id` (`id`);

--
-- Indexes for table `scans`
--
ALTER TABLE `scans`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_scans_scan_code` (`scan_code`),
  ADD KEY `ix_scans_id` (`id`);

--
-- Indexes for table `scan_preparations`
--
ALTER TABLE `scan_preparations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `scan_id` (`scan_id`),
  ADD KEY `ix_scan_preparations_id` (`id`);

--
-- Indexes for table `studies`
--
ALTER TABLE `studies`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `session_id` (`session_id`),
  ADD KEY `scan_id` (`scan_id`),
  ADD KEY `ix_studies_id` (`id`);

--
-- Indexes for table `support_tickets`
--
ALTER TABLE `support_tickets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `technicians`
--
ALTER TABLE `technicians`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `ix_technicians_id` (`id`);

--
-- Indexes for table `technician_password_reset_otp`
--
ALTER TABLE `technician_password_reset_otp`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_technician_password_reset_otp_id` (`id`);

--
-- Indexes for table `triage_cases`
--
ALTER TABLE `triage_cases`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_triage_cases_id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ai_analysis`
--
ALTER TABLE `ai_analysis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `cases`
--
ALTER TABLE `cases`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `doctor_privacy_settings`
--
ALTER TABLE `doctor_privacy_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `faqs`
--
ALTER TABLE `faqs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `feedbacks`
--
ALTER TABLE `feedbacks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `pacs_archives`
--
ALTER TABLE `pacs_archives`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `patient`
--
ALTER TABLE `patient`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=90;

--
-- AUTO_INCREMENT for table `radiologist_reviews`
--
ALTER TABLE `radiologist_reviews`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ris_worklist`
--
ALTER TABLE `ris_worklist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `scans`
--
ALTER TABLE `scans`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT for table `scan_preparations`
--
ALTER TABLE `scan_preparations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=71;

--
-- AUTO_INCREMENT for table `studies`
--
ALTER TABLE `studies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `support_tickets`
--
ALTER TABLE `support_tickets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `technicians`
--
ALTER TABLE `technicians`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `technician_password_reset_otp`
--
ALTER TABLE `technician_password_reset_otp`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `triage_cases`
--
ALTER TABLE `triage_cases`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ai_analysis`
--
ALTER TABLE `ai_analysis`
  ADD CONSTRAINT `ai_analysis_ibfk_1` FOREIGN KEY (`study_id`) REFERENCES `studies` (`id`);

--
-- Constraints for table `cases`
--
ALTER TABLE `cases`
  ADD CONSTRAINT `cases_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`id`);

--
-- Constraints for table `pacs_archives`
--
ALTER TABLE `pacs_archives`
  ADD CONSTRAINT `pacs_archives_ibfk_1` FOREIGN KEY (`study_id`) REFERENCES `studies` (`id`);

--
-- Constraints for table `radiologist_reviews`
--
ALTER TABLE `radiologist_reviews`
  ADD CONSTRAINT `radiologist_reviews_ibfk_1` FOREIGN KEY (`study_id`) REFERENCES `studies` (`id`);

--
-- Constraints for table `ris_worklist`
--
ALTER TABLE `ris_worklist`
  ADD CONSTRAINT `ris_worklist_ibfk_1` FOREIGN KEY (`study_id`) REFERENCES `studies` (`id`);

--
-- Constraints for table `scan_preparations`
--
ALTER TABLE `scan_preparations`
  ADD CONSTRAINT `scan_preparations_ibfk_1` FOREIGN KEY (`scan_id`) REFERENCES `scans` (`id`);

--
-- Constraints for table `studies`
--
ALTER TABLE `studies`
  ADD CONSTRAINT `studies_ibfk_1` FOREIGN KEY (`scan_id`) REFERENCES `scans` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
