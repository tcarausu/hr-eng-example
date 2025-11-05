CREATE ROLE openmind_user LOGIN PASSWORD 'openmind' INHERIT;
CREATE DATABASE openmind OWNER openmind_user;

ALTER DATABASE openmind SET search_path = openmind_ext, public;
