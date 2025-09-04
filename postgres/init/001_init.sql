CREATE DATABASE sample_db;
-- テーブルの作成
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INT
);
-- データの操作
-- INSERT INTO users (id, name, age) VALUES (1, 'Alice', 25);