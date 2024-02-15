DROP DATABASE IF EXISTS `quiz`;
CREATE DATABASE `quiz` DEFAULT CHARACTER
SET
     utf8 COLLATE utf8_unicode_ci;

USE quiz;

CREATE TABLE
     IF NOT EXISTS `users` (
          `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
          `user_name` VARCHAR(50) UNIQUE,
          `email` VARCHAR(100) NOT NULL UNIQUE,
          `password` VARCHAR(100) NOT NULL,
          `type` ENUM ('Basic', 'Scholar','Admin') NOT NULL DEFAULT 'Basic',
          PRIMARY KEY `user_id` (`id`)
     ) ENGINE = InnoDB;

DROP TABLE IF EXISTS `users_profile`;

CREATE TABLE
     `users_profile` (
          `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
          `first_name` VARCHAR(255) NOT NULL,
          `last_name` VARCHAR(255) NOT NULL,
          `reg_no` CHAR(11) UNIQUE,
          `department` VARCHAR(255) NOT NULL,
          `level` ENUM('100', '200', '300', '400', '500', '600') NOT NULL,
          `user_id` INT UNSIGNED NOT NULL UNIQUE,
          PRIMARY KEY `pk_id` (`id`),
          FOREIGN KEY (`user_id`) REFERENCES `quiz`.`users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
     ) ENGINE = InnoDB;


