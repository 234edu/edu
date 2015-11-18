use `elearning`;

insert into `Roles`(`role_name`,`description`) values
("admin","administration purposes for courses and users"),
("teacher","full administrative rights on courses settings (CRUD)"),
("assistant","partial administrative rights on courses settings (read only)"),
("student","course attending rights"),
("observer","read only rights");

