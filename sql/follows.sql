USE quiz;

CREATE TABLE IF NOT EXISTS
  `follows` (
    `follower_id` INT UNSIGNED NOT NULL,
    `followed_id` INT UNSIGNED NOT NULL,
    `date_followed` DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY `pk_id` (`follower_id`, `followed_id`)
  ) ENGINE = InnoDB;


CREATE OR REPLACE VIEW `_fstats` AS SELECT users.id, users.email, users.type,
 COUNT(follows.follower_id) AS followers FROM users 
 LEFT JOIN follows ON follows.followed_id = users.id
  GROUP BY users.id;

CREATE OR REPLACE VIEW `_tstats` AS  SELECT _fstats.*, count(topics.id) AS topics FROM _fstats LEFT JOIN
topics ON _fstats.id = topics.user_id GROUP BY _fstats.id;

CREATE OR REPLACE VIEW `_qstats` AS SELECT _tstats.*, COUNT(quiz.id) AS total_quiz FROM _tstats LEFT JOIN
quiz ON _tstats.id = quiz.user_id GROUP BY _tstats.id;

CREATE OR REPLACE VIEW `followings` AS SELECT users.id, users.email, users_profile.department,
 users_profile.level, follows.date_followed, follows.followed_id 
FROM follows LEFT JOIN users ON users.id = follower_id LEFT JOIN
 users_profile ON users.id = users_profile.user_id;


DROP PROCEDURE IF EXISTS `fetch_followers`;
DELIMITER $$
CREATE PROCEDURE `fetch_followers`(
`user_id` INT
) BEGIN

  --
  
END $$
DELIMITER ;