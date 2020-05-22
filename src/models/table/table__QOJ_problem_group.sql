CREATE TABLE IF NOT EXISTS QOJ_problem_group(
pg_id INT NOT NULL AUTO_INCREMENT,
pg_name VARCHAR(40) NOT NULL,
pg_activate INT NOT NULL DEFAULT 1,
pg_exam INT NOT NULL DEFAULT 0,
pg_exam_start DATETIME NULL DEFAULT NULL,
pg_exam_end DATETIME NULL DEFAULT NULL,
pg_date DATETIME NOT NULL DEFAULT NOW(),
class_id INT NOT NULL,
FOREIGN KEY(class_id) REFERENCES QOJ_class(class_id) ON DELETE CASCADE ON UPDATE CASCADE,
PRIMARY KEY(pg_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;