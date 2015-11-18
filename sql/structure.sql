CREATE SCHEMA IF NOT EXISTS `elearning` DEFAULT CHARACTER SET utf8 ;

use `elearning`;

drop table if exists `Users_Roles`;
drop table if exists `Users`;
drop table if exists `Roles`;
drop table if exists `Course_Settings`;
drop table if exists `Courses`;

create table `Roles`(
	id tinyint primary key auto_increment,
    role_name VARCHAR(10) NOT NULL UNIQUE,
    description VARCHAR(100)
);

create table `Users` (
	id VARCHAR(12) primary key, #numar matricol
	account VARCHAR(30) NOT NULL UNIQUE,
    passkey VARCHAR(100) NOT NULL,#example for MD5 hashing
    first_name VARCHAR(30),
    surname VARCHAR(30),
    email VARCHAR(30) NOT NULL UNIQUE,
    role tinyint references `Roles`(id)
    #rol maxim e.g. un profesor poate avea rol de student pentru alte cursuri dar un student nu poate avea rol de profesor
);

create table `Course_Settings`(
	id int primary key
    #more settings
);

create table `Courses`(
	id int primary key auto_increment,
    course_subject VARCHAR(12),
    settings int references `Course_Settings`(id)
);

create table `Users_Roles`(
	user_id int references `Users`(id),
    role_id int references `Roles`(id),
    course_id int references `Courses`(id),
    primary key(user_id,course_id)
);