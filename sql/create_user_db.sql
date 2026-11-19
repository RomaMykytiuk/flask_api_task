CREATE USER flask_user WITH PASSWORD 'CHANGE_ME';

CREATE DATABASE flask_school OWNER flask_user;

GRANT ALL PRIVILEGES ON DATABASE flask_school TO flask_user;