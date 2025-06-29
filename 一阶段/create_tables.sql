-- 创建数据库
CREATE DATABASE IF NOT EXISTS homework;
USE homework;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role VARCHAR(20) NOT NULL,
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 数据集表
CREATE TABLE IF NOT EXISTS datasets (
    name VARCHAR(100) PRIMARY KEY,
    user_id INT NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    measures JSON,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 模型表
CREATE TABLE IF NOT EXISTS models (
    name VARCHAR(100) PRIMARY KEY,
    model_type VARCHAR(50) NOT NULL,
    parameters JSON,
    CHECK (model_type IN ('classify', 'regression'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 实验表
CREATE TABLE IF NOT EXISTS experiments (
    experiment_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 预测表
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    experiment_id INT ,
    model_name VARCHAR(100) NOT NULL,
    dataset_name VARCHAR(100) NOT NULL,
    parameters JSON,
    user_id INT,
    status VARCHAR(20) NOT NULL,
    metrics JSON,
    predicted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (model_name) REFERENCES models(name) ON DELETE CASCADE,
    CHECK (status IN ('completed', 'training', 'failed', 'pending'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 项目表
CREATE TABLE IF NOT EXISTS projects(
    user_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)ENGINE=InnoDB DEFAULT CHARSET = utf8mb4;
