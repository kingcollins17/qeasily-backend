USE quiz;

-- DROP TABLE IF EXISTS `challenges`;
CREATE TABLE
     IF NOT EXISTS `challenges` (
          `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
          `name` VARCHAR(255) NOT NULL,
          `quizzes` VARCHAR(255) NOT NULL,
          `paid` BOOLEAN NOT NULL DEFAULT FALSE,
          `entry_fee` FLOAT NOT NULL DEFAULT '0.00',
          `reward` FLOAT NOT NULL DEFAULT '0.00',
          `date_added` DATETIME DEFAULT NOW(),
          `duration` INT UNSIGNED NOT NULL DEFAULT 1,
          `user_id` INT UNSIGNED NOT NULL,
          PRIMARY KEY `pk_id` (`id`),
          CONSTRAINT `fk_ch_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
     ) ENGINE = InnoDB;

DROP TABLE IF EXISTS `leaderboards`;
CREATE TABLE
     `leaderboards` (
          `challenge_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
          `user_id` INT UNSIGNED NOT NULL,
          `points` INT UNSIGNED NOT NULL DEFAULT 0,
          PRIMARY KEY `pk_id` (`challenge_id`, `user_id`),
          CONSTRAINT `fk_lead_chal` FOREIGN KEY (`challenge_id`) 
          REFERENCES `challenges` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
          CONSTRAINT `fk_l_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
     ) ENGINE = InnoDB;