-- 用户注册时间自动记录
DELIMITER //
CREATE TRIGGER before_user_insert
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    SET NEW.registered_at = NOW();
END //
DELIMITER ;

-- 数据集上传时间自动记录
DELIMITER //
CREATE TRIGGER before_dataset_insert
BEFORE INSERT ON datasets
FOR EACH ROW
BEGIN
    SET NEW.uploaded_at = NOW();
END //
DELIMITER ;

-- 模型训练时间自动记录
DELIMITER //
CREATE TRIGGER before_model_insert
BEFORE INSERT ON models
FOR EACH ROW
BEGIN
    SET NEW.trained_at = NOW();
END //
DELIMITER ;

-- 预测时间自动记录
DELIMITER //
CREATE TRIGGER before_prediction_insert
BEFORE INSERT ON predictions
FOR EACH ROW
BEGIN
    SET NEW.predicted_at = NOW();
END //
DELIMITER ;

-- 实验状态变更日志
CREATE TABLE experiment_status_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    experiment_id INT NOT NULL,
    old_status VARCHAR(20),
    new_status VARCHAR(20) NOT NULL,
    changed_at DATETIME NOT NULL,
    changed_by INT,
    FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id) ON DELETE CASCADE
);

DELIMITER //
CREATE TRIGGER after_experiment_status_update
AFTER UPDATE ON experiments
FOR EACH ROW
BEGIN
    IF OLD.status != NEW.status THEN
        INSERT INTO experiment_status_log (experiment_id, old_status, new_status, changed_at, changed_by)
        VALUES (NEW.experiment_id, OLD.status, NEW.status, NOW(), NEW.user_id);
    END IF;
END //
DELIMITER ;