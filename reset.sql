-- Set username to your username
-- Open mysql prompt
-- source filename (reset.sql)
drop database play;
create database play character set utf8;
grant all on play.* to <username>@localhost;
flush privileges;
