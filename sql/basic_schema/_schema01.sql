
-- DROP TABLE IF EXISTS `mcqs`;
-- DROP TABLE IF EXISTS `dcqs`;
-- DROP TABLE IF EXISTS `topics`;
-- DROP TABLE IF EXISTS `categories`;


-- CREATE TABLE
--      IF NOT EXISTS `categories` (
--           `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
--           `name` VARCHAR(255) NOT NULL UNIQUE,
--           `user_id` INT UNSIGNED NOT NULL,
--           PRIMARY KEY (`id`),
--           FOREIGN KEY (`user_id`) REFERENCES `quiz`.`users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
--      ) ENGINE = InnoDB;

-- CREATE TABLE
--      IF NOT EXISTS `topics` (
--           `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
--           `title` VARCHAR(100) NOT NULL UNIQUE,
--           `description` VARCHAR(2048) NOT NULL DEFAULT "",
--           `date_added` DATETIME NOT NULL DEFAULT NOW(),
--           `level` ENUM('100', '200', '300', '400', '500', '600') NOT NULL DEFAULT '100',
--           `category_id` INT UNSIGNED NOT NULL,
--           `user_id` INT UNSIGNED NOT NULL,
--           PRIMARY KEY (`id`),
--           CONSTRAINT `fk_topics_cat` FOREIGN KEY (`category_id`) REFERENCES `quiz`.`categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
--           FOREIGN KEY (`user_id`) REFERENCES `quiz`.`users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
--      ) ENGINE = InnoDB;

-- CREATE TABLE
--      IF NOT EXISTS `mcqs` (
--           `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
--           `query` VARCHAR(512) NOT NULL,
--           `A` VARCHAR(100) NOT NULL,
--           `B` VARCHAR(100) NOT NULL,
--           `C` VARCHAR(100) NOT NULL,
--           `D` VARCHAR(100) NOT NULL,
--           `explanation` VARCHAR(1024) NOT NULL,
--           `correct` ENUM ('A', 'B', 'C', 'D') NOT NULL,
--           `difficulty` ENUM ('Easy', 'Medium', 'Hard', 'Impossible') NOT NULL DEFAULT 'Easy',
--           `topic_id` INT UNSIGNED NOT NULL,
--           `user_id` INT UNSIGNED NOT NULL,
--           PRIMARY KEY (`id`),
--           CONSTRAINT `fk_questions_topic` FOREIGN KEY (`topic_id`) REFERENCES `quiz`.`topics` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
--           FOREIGN KEY (`user_id`) REFERENCES `quiz`.`users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
--      ) ENGINE = InnoDB;

-- CREATE TABLE
--      IF NOT EXISTS `dcqs` (
--           `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
--           `query` VARCHAR(255) NOT NULL,
--           `correct` BOOLEAN NOT NULL,
--           `explanation` VARCHAR(512) NOT NULL,
--           `user_id` INT UNSIGNED NOT NULL,
--           `topic_id` INT UNSIGNED NOT NULL,
--           PRIMARY KEY `pk_id` (`id`),
--           FOREIGN KEY (`user_id`) REFERENCES `quiz`.`users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
--           FOREIGN KEY (`topic_id`) REFERENCES `quiz`.`topics` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
--      ) ENGINE = InnoDB;


-- DROP TABLE IF EXISTS `activity`;
CREATE TABLE `activity` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `plan` ENUM('Free', 'Scholar', 'Genius', 'Admin') NOT NULL DEFAULT 'Free',
  `balance` DECIMAL NOT NULL DEFAULT 0.0,
  `quizzes_left` INT UNSIGNED NOT NULL DEFAULT 10,
  `challenges_left` INT UNSIGNED NOT NULL DEFAULT 5,
  `renewed_at` DATETIME NOT NULL DEFAULT NOW(),
  `user_id` INT UNSIGNED NOT NULL UNIQUE,
  PRIMARY KEY `pk_id`(`id`),
  FOREIGN KEY (`user_id`) REFERENCES `quiz`.`users`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;


-- INSERT INTO
--      categories (name, user_id)
-- VALUES
--      ('Medicine', 1),
--      ('Pharmacy', 1),
--      ('Engineering', 1),
--      ('Programming', 2),
--      ('Nutrition', 3);
-- INSERT INTO
--      topics (title, category_id, user_id)
-- VALUES
-- ('Engine 101', 13, 1),
-- ('Engine 202', 2, 2),
-- ('Math 121', 1, 1),
-- ('Math 234', 1, 3),
-- ('Computer Programming 101', 14, 2),
-- ('Lang 101', 3, 1),
-- ('Lit 232', 3, 2),
-- ('Phy 321', 2, 1),
-- ('Math 214', 1, 3),
-- ('Intro C++', 14, 2);
-- INSERT INTO mcqs(query, A, B, C, D, explanation, correct, difficulty, topic_id, user_id) VALUES
-- ('Test Question 41', 'Aa', 'Bb', 'Cc', 'Dd', 'explained', 'A', 'Easy', 10, 1),
-- ('Test Question 23', 'Aa', 'Bb', 'Cc', 'Dd', 'explained', 'B', 'Easy', 9, 1),
-- ('Test Question 53', 'Aa', 'Bb', 'Cc', 'Dd', 'explained', 'A', 'Easy', 5, 1),
-- ('Test Question 55', 'Aa', 'Bb', 'Cc', 'Dd', 'explained', 'A', 'Easy', 3, 1),
-- ('Test Question 25', 'Aa', 'Bb', 'Cc', 'Dd', 'explained', 'D', 'Easy', 3, 1),
-- ('Test Question 87', 'Aa', 'Bb', 'Cc', 'Dd', 'explained', 'A', 'Easy', 2, 2),
-- ('Test Question 01', 'Aa', 'Bb', 'Cc', 'Dd', 'explained', 'B', 'Easy', 1, 2),
-- ('Test Question 14', 'Aa', 'Bb', 'Cc', 'Dd', 'explained', 'D', 'Easy', 5, 2),
-- ('Test Question 90', 'Aa', 'Bb', 'Cc', 'Dd', 'explained', 'C', 'Easy', 6, 2),
-- ('Test Question 11', 'Aa', 'Bb', 'Cc', 'Dd', 'explained', 'A', 'Easy', 8, 2)
-- ;
-- INSERT INTO dcqs(query, correct, explanation, user_id, topic_id) VALUES
-- ('Dual choice question 1', TRUE, 'Explained', 2, 1),
-- ('Dual choice question 2', TRUE, 'Explained', 2, 1),
-- ('Dual choice question 3', TRUE, 'Explained', 2, 1),
-- ('Dual choice question 4', TRUE, 'Explained', 2, 1),
-- ('Dual choice question 5', TRUE, 'Explained', 2, 1),
-- ('Dual choice question 6', TRUE, 'Explained', 2, 1),
-- ('Dual choice question 7', TRUE, 'Explained', 2, 1),
-- ('Dual choice question 11', TRUE, 'Explained', 2, 1),
-- ('Dual choice question 12', TRUE, 'Explained', 2, 1),
-- ('Dual choice question 13', TRUE, 'Explained', 2, 1),
-- ('Dual choice question 14', TRUE, 'Explained', 2, 1)
-- ;