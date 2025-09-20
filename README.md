# Redis Cache with MySQL in Python

This project demonstrates how to use **Redis Cloud (Redis Labs)** as a caching layer for a **MySQL database** in Python.  
It includes handling of **wrong key types** in Redis to prevent errors when a key already exists with a different data type.

---

## Features

- Connect to **Redis Cloud** and **MySQL**
- Use Redis as a **cache layer** to reduce load on MySQL
- Automatically handles **wrong-type keys** in Redis
- Cache results in Redis with **expiration (TTL)**
- Python code with MySQL fallback

---

## Requirements

Install Python packages:

```bash
pip install redis mysql-connector-python

##mysql Commands
CREATE DATABASE testdb;
USE testdb;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100)
);

INSERT INTO users (name, email)
VALUES ('Alice', 'alice@example.com'),
       ('Bob', 'bob@example.com');
