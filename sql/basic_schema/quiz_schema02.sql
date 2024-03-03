USE quiz;

-- DROP TABLE IF EXISTS `quiz`;

-- CREATE TABLE
--      IF NOT EXISTS `quiz` (
--           `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
--           `title` VARCHAR(100) NOT NULL UNIQUE,
--           `questions` VARCHAR(2048) NOT NULL,
--           `user_id` INT UNSIGNED NOT NULL,
--           `topic_id` INT UNSIGNED NOT NULL,
--           `duration` INT UNSIGNED NOT NULL DEFAULT '1800',
--           `likes` INT UNSIGNED NOT NULL DEFAULT 0,
--           `description` VARCHAR(2048) NOT NULL,
--           `date_added` DATETIME NOT NULL DEFAULT NOW(),
--           `qualified` ENUM ('Basic', 'Scholar', 'Any') NOT NULL,
--           `difficulty` ENUM ('Easy', 'Medium', 'Hard', 'Mixed') NOT NULL DEFAULT 'Mixed',
--           FOREIGN KEY (`topic_id`) REFERENCES `quiz`.`topics` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
--           PRIMARY KEY `quiz_id` (`id`),
--           CONSTRAINT `fk_quiz_users` FOREIGN KEY (`user_id`) REFERENCES `quiz`.`users` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE
--      ) ENGINE = InnoDB;

INSERT INTO
     quiz (
          title,
          questions,
          user_id,
          topic_id,
          `description`
     )
VALUES
     (
          'Test quiz 0x0',
          '[1,2,4,5,6,7,8,9,10]',
          1,
          2,
          'Test description'
     ),
     (
          'Test quiz 0x1',
          '[10,12,14,5,16,7,8,9,1]',
          1,
          3,
          'Test description'
     ),
     (
          'Test quiz 0x',
          '[1,12,4,5,6,17,8,19,10]',
          16,
          4,
          'Test description'
     ),
     (
          'Test quiz 301',
          '[12,4,15,6,7,8,19,10]',
          16,
          4,
          'Test description'
     );