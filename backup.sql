-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: quiz
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Temporary view structure for view `_fstats`
--

DROP TABLE IF EXISTS `_fstats`;
/*!50001 DROP VIEW IF EXISTS `_fstats`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `_fstats` AS SELECT 
 1 AS `id`,
 1 AS `email`,
 1 AS `type`,
 1 AS `followers`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `_qstats`
--

DROP TABLE IF EXISTS `_qstats`;
/*!50001 DROP VIEW IF EXISTS `_qstats`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `_qstats` AS SELECT 
 1 AS `id`,
 1 AS `email`,
 1 AS `type`,
 1 AS `followers`,
 1 AS `topics`,
 1 AS `total_quiz`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `_tstats`
--

DROP TABLE IF EXISTS `_tstats`;
/*!50001 DROP VIEW IF EXISTS `_tstats`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `_tstats` AS SELECT 
 1 AS `id`,
 1 AS `email`,
 1 AS `type`,
 1 AS `followers`,
 1 AS `topics`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb3_unicode_ci NOT NULL,
  `user_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `challenges`
--

DROP TABLE IF EXISTS `challenges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `challenges` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb3_unicode_ci NOT NULL,
  `quizzes` varchar(255) COLLATE utf8mb3_unicode_ci NOT NULL,
  `paid` tinyint(1) NOT NULL DEFAULT '0',
  `entry_fee` float NOT NULL DEFAULT '0',
  `reward` float NOT NULL DEFAULT '0',
  `user_id` int unsigned NOT NULL,
  `date_added` datetime DEFAULT CURRENT_TIMESTAMP,
  `duration` int unsigned NOT NULL DEFAULT '7',
  PRIMARY KEY (`id`),
  KEY `fk_ch_users` (`user_id`),
  CONSTRAINT `fk_ch_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dcqs`
--

DROP TABLE IF EXISTS `dcqs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dcqs` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `query` varchar(255) COLLATE utf8mb3_unicode_ci NOT NULL,
  `correct` tinyint(1) NOT NULL,
  `explanation` varchar(512) COLLATE utf8mb3_unicode_ci NOT NULL,
  `user_id` int unsigned NOT NULL,
  `topic_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `topic_id` (`topic_id`),
  CONSTRAINT `dcqs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `dcqs_ibfk_2` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `followings`
--

DROP TABLE IF EXISTS `followings`;
/*!50001 DROP VIEW IF EXISTS `followings`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `followings` AS SELECT 
 1 AS `id`,
 1 AS `email`,
 1 AS `department`,
 1 AS `level`,
 1 AS `date_followed`,
 1 AS `followed_id`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `follows`
--

DROP TABLE IF EXISTS `follows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `follows` (
  `follower_id` int unsigned NOT NULL,
  `followed_id` int unsigned NOT NULL,
  `date_followed` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`follower_id`,`followed_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `fstats`
--

DROP TABLE IF EXISTS `fstats`;
/*!50001 DROP VIEW IF EXISTS `fstats`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `fstats` AS SELECT 
 1 AS `id`,
 1 AS `email`,
 1 AS `type`,
 1 AS `followers`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `leaderboards`
--

DROP TABLE IF EXISTS `leaderboards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leaderboards` (
  `challenge_id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `points` int unsigned NOT NULL DEFAULT '0',
  `progress` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`challenge_id`,`user_id`),
  KEY `fk_l_users` (`user_id`),
  CONSTRAINT `fk_l_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_lead_chal` FOREIGN KEY (`challenge_id`) REFERENCES `challenges` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mcqs`
--

DROP TABLE IF EXISTS `mcqs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mcqs` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `query` varchar(512) COLLATE utf8mb3_unicode_ci NOT NULL,
  `A` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
  `B` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
  `C` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
  `D` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
  `explanation` varchar(1024) COLLATE utf8mb3_unicode_ci NOT NULL,
  `correct` enum('A','B','C','D') COLLATE utf8mb3_unicode_ci NOT NULL,
  `difficulty` enum('Easy','Medium','Hard','Impossible') COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT 'Easy',
  `topic_id` int unsigned NOT NULL,
  `user_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_questions_topic` (`topic_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `fk_questions_topic` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`) ON DELETE CASCADE,
  CONSTRAINT `mcqs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `quiz`
--

DROP TABLE IF EXISTS `quiz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quiz` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
  `questions` varchar(2048) COLLATE utf8mb3_unicode_ci NOT NULL,
  `user_id` int unsigned NOT NULL,
  `topic_id` int unsigned NOT NULL,
  `duration` int unsigned NOT NULL DEFAULT '1800',
  `likes` int unsigned NOT NULL DEFAULT '0',
  `description` varchar(2048) COLLATE utf8mb3_unicode_ci NOT NULL,
  `date_added` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `qualified` enum('Basic','Scholar','Any') COLLATE utf8mb3_unicode_ci NOT NULL,
  `difficulty` enum('Easy','Medium','Hard','Mixed') COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT 'Mixed',
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `topic_id` (`topic_id`),
  KEY `fk_quiz_users` (`user_id`),
  CONSTRAINT `fk_quiz_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `quiz_ibfk_1` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `topics`
--

DROP TABLE IF EXISTS `topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topics` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
  `description` varchar(2048) COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
  `date_added` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `category_id` int unsigned NOT NULL,
  `user_id` int unsigned NOT NULL,
  `level` enum('100','200','300','400','500','600') COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '100',
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `fk_topics_cat` (`category_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `fk_topics_cat` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `topics_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `tstats`
--

DROP TABLE IF EXISTS `tstats`;
/*!50001 DROP VIEW IF EXISTS `tstats`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `tstats` AS SELECT 
 1 AS `id`,
 1 AS `email`,
 1 AS `type`,
 1 AS `followers`,
 1 AS `topics`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
  `password` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
  `type` enum('Basic','Scholar','Admin') COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT 'Basic',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users_profile`
--

DROP TABLE IF EXISTS `users_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_profile` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) COLLATE utf8mb3_unicode_ci NOT NULL,
  `last_name` varchar(255) COLLATE utf8mb3_unicode_ci NOT NULL,
  `reg_no` char(11) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `department` varchar(255) COLLATE utf8mb3_unicode_ci NOT NULL,
  `level` enum('100','200','300','400','500','600') COLLATE utf8mb3_unicode_ci NOT NULL,
  `user_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `reg_no` (`reg_no`),
  CONSTRAINT `users_profile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `_fstats`
--

/*!50001 DROP VIEW IF EXISTS `_fstats`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `_fstats` AS select `users`.`id` AS `id`,`users`.`email` AS `email`,`users`.`type` AS `type`,count(`follows`.`follower_id`) AS `followers` from (`users` left join `follows` on((`follows`.`followed_id` = `users`.`id`))) group by `users`.`id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `_qstats`
--

/*!50001 DROP VIEW IF EXISTS `_qstats`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `_qstats` AS select `_tstats`.`id` AS `id`,`_tstats`.`email` AS `email`,`_tstats`.`type` AS `type`,`_tstats`.`followers` AS `followers`,`_tstats`.`topics` AS `topics`,count(`quiz`.`id`) AS `total_quiz` from (`_tstats` left join `quiz` on((`_tstats`.`id` = `quiz`.`user_id`))) group by `_tstats`.`id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `_tstats`
--

/*!50001 DROP VIEW IF EXISTS `_tstats`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `_tstats` AS select `_fstats`.`id` AS `id`,`_fstats`.`email` AS `email`,`_fstats`.`type` AS `type`,`_fstats`.`followers` AS `followers`,count(`topics`.`id`) AS `topics` from (`_fstats` left join `topics` on((`_fstats`.`id` = `topics`.`user_id`))) group by `_fstats`.`id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `followings`
--

/*!50001 DROP VIEW IF EXISTS `followings`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `followings` AS select `users`.`id` AS `id`,`users`.`email` AS `email`,`users_profile`.`department` AS `department`,`users_profile`.`level` AS `level`,`follows`.`date_followed` AS `date_followed`,`follows`.`followed_id` AS `followed_id` from ((`follows` left join `users` on((`users`.`id` = `follows`.`follower_id`))) left join `users_profile` on((`users`.`id` = `users_profile`.`user_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `fstats`
--

/*!50001 DROP VIEW IF EXISTS `fstats`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `fstats` AS select `users`.`id` AS `id`,`users`.`email` AS `email`,`users`.`type` AS `type`,count(`follows`.`follower_id`) AS `followers` from (`users` left join `follows` on((`follows`.`followed_id` = `users`.`id`))) group by `users`.`id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `tstats`
--

/*!50001 DROP VIEW IF EXISTS `tstats`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `tstats` AS select `fstats`.`id` AS `id`,`fstats`.`email` AS `email`,`fstats`.`type` AS `type`,`fstats`.`followers` AS `followers`,count(`topics`.`id`) AS `topics` from (`fstats` left join `topics` on((`fstats`.`id` = `topics`.`user_id`))) group by `fstats`.`id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-06  9:06:26
