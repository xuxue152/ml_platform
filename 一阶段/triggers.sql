use homework;
-- 用户注册时间自动记录
DELIMITER //
CREATE TRIGGER before_user_insert
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    SET NEW.registered_at = NOW();
END //
DELIMITER ;

-- 项目创建时间自动记录
DELIMITER //
CREATE TRIGGER before_project_insert
BEFORE INSERT ON projects
FOR EACH ROW
BEGIN
    SET NEW.created_at = NOW();
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

-- 预测时间自动记录
DELIMITER //
CREATE TRIGGER before_prediction_insert
BEFORE INSERT ON predictions
FOR EACH ROW
BEGIN
    SET NEW.predicted_at = NOW();
END //
DELIMITER ;