DROP DATABASE IF EXISTS `quiz`;
CREATE DATABASE `quiz` DEFAULT CHARACTER
SET
     utf8 COLLATE utf8_unicode_ci;
USE quiz;
CREATE TABLE
     IF NOT EXISTS `users` (
          `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
          `user_name` VARCHAR(50),
          `email` VARCHAR(100) NOT NULL UNIQUE,
          `password` VARCHAR(100) NOT NULL,
          `admin` BOOLEAN NOT NULL DEFAULT FALSE,
          PRIMARY KEY `user_id` (`id`)
     ) ENGINE = InnoDB;
CREATE TABLE
     IF NOT EXISTS `categories` (
          `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
          `name` VARCHAR(255) NOT NULL UNIQUE,
          PRIMARY KEY (`id`)
     ) ENGINE = InnoDB;
CREATE TABLE
     IF NOT EXISTS `topics` (
          `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
          `title` VARCHAR(100) NOT NULL UNIQUE,
          `description` VARCHAR (1024) NOT NULL DEFAULT "",
          `category_id` INT UNSIGNED NOT NULL,
          PRIMARY KEY (`id`),
          CONSTRAINT `fk_topics_cat` FOREIGN KEY (`category_id`) REFERENCES `quiz`.`categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
     ) ENGINE = InnoDB;
CREATE TABLE
     IF NOT EXISTS `questions` (
          `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
          `question` VARCHAR(512) NOT NULL UNIQUE,
          `A` VARCHAR(100) NOT NULL,
          `B` VARCHAR(100) NOT NULL,
          `C` VARCHAR(100) NOT NULL,
          `D` VARCHAR(100) NOT NULL,
          `explanation` VARCHAR(2048) NOT NULL DEFAULT ' ',
          `correct` ENUM ('A', 'B', 'C', 'D') NOT NULL DEFAULT 'A',
          `topic_id` INT UNSIGNED NOT NULL,
          `user_id` INT UNSIGNED NOT NULL,
          PRIMARY KEY (`id`),
          CONSTRAINT `fk_questions_topic` FOREIGN KEY (`topic_id`) REFERENCES `quiz`.`topics` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
          FOREIGN KEY (`user_id`) REFERENCES `quiz`.`users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
     ) ENGINE = InnoDB;
CREATE TABLE
     IF NOT EXISTS `quiz` (
          `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
          `title` VARCHAR(100) NOT NULL UNIQUE,
          `questions` VARCHAR(2048) NOT NULL,
          `user_id` INT UNSIGNED NOT NULL,
          `topic_id` INT UNSIGNED NOT NULL,
          `duration` INT UNSIGNED NOT NULL DEFAULT '1800',
          FOREIGN KEY (`topic_id`) REFERENCES `quiz`.`topics`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
          PRIMARY KEY `quiz_id` (`id`),
          CONSTRAINT `fk_quiz_users`
            FOREIGN KEY (`user_id`)
            REFERENCES `quiz`.`users` (`id`)
            ON DELETE NO ACTION
            ON UPDATE CASCADE
) ENGINE = InnoDB;
