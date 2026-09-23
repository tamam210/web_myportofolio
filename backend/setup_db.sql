-- Setup database MySQL/MariaDB untuk chatbot.
-- ANGKA rahasia di file ini cuma placeholder.
-- Password yang bener diambil dari DATABASE_URL di file .env
-- (file .env TIDAK ikut naik ke GitHub, aman).
--
-- Cara jalanin:
--   1. Buka backend/.env, pastikan DATABASE_URL memakai password asli lu
--   2. Edit file ini: ganti GANTI_PASSWORD dengan password dari .env
--   3. sudo mariadb < setup_db.sql

CREATE DATABASE IF NOT EXISTS mycv;

CREATE USER IF NOT EXISTS 'gwuser'@'localhost' IDENTIFIED BY 'GANTI_PASSWORD';
CREATE USER IF NOT EXISTS 'gwuser'@'127.0.0.1' IDENTIFIED BY 'GANTI_PASSWORD';

GRANT ALL PRIVILEGES ON mycv.* TO 'gwuser'@'localhost';
GRANT ALL PRIVILEGES ON mycv.* TO 'gwuser'@'127.0.0.1';

FLUSH PRIVILEGES;