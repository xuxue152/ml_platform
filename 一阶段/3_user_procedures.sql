-- 用户更新个人信息
DELIMITER //
CREATE PROCEDURE user_update_profile(
    IN p_user_id INT,
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(100)
    )
BEGIN
    UPDATE users 
    SET email = p_email, 
        password = CASE WHEN p_password IS NOT NULL AND p_password != '' 
                         THEN p_password 
                         ELSE password END
    WHERE user_id = p_user_id;
END //
DELIMITER ;

-- 用户创建新实验
DELIMITER //
CREATE PROCEDURE user_create_experiment(
    IN p_user_id INT,
    IN p_name VARCHAR(100),
    IN p_parameters TEXT,
    OUT p_experiment_id INT)
BEGIN
    INSERT INTO experiments (user_id, name, date, status, parameters)
    VALUES (p_user_id, p_name, CURDATE(), 'pending', p_parameters);
    
    SET p_experiment_id = LAST_INSERT_ID();
END //
DELIMITER ;

-- 用户上传数据集
DELIMITER //
CREATE PROCEDURE user_upload_dataset(
    IN p_user_id INT,
    IN p_type VARCHAR(20),
    IN p_file_path VARCHAR(255),
    OUT p_dataset_id INT)
BEGIN
    INSERT INTO datasets (user_id, type, file_path)
    VALUES (p_user_id, p_type, p_file_path);
    
    SET p_dataset_id = LAST_INSERT_ID();
END //
DELIMITER ;

-- 用户训练模型
DELIMITER //
CREATE PROCEDURE user_train_model(
    IN p_user_id INT,
    IN p_experiment_id INT,
    IN p_model_name VARCHAR(100),
    IN p_model_type VARCHAR(50),
    IN p_parameters TEXT,
    IN p_file_path VARCHAR(255),
    OUT p_model_id INT)
BEGIN
    INSERT INTO models (user_id, experiment_id, model_name, model_type, parameters, file_path)
    VALUES (p_user_id, p_experiment_id, p_model_name, p_model_type, p_parameters, p_file_path);
    
    SET p_model_id = LAST_INSERT_ID();
    
    -- 更新实验状态
    UPDATE experiments SET status = 'completed' WHERE experiment_id = p_experiment_id;
END //
DELIMITER ;

-- 用户执行预测
DELIMITER //
CREATE PROCEDURE user_make_prediction(
    IN p_model_id INT,
    IN p_dataset_id INT,
    IN p_result TEXT,
    IN p_metrics TEXT,
    OUT p_prediction_id INT)
BEGIN
    INSERT INTO predictions (model_id, dataset_id, result, metrics)
    VALUES (p_model_id, p_dataset_id, p_result, p_metrics);
    
    SET p_prediction_id = LAST_INSERT_ID();
END //
DELIMITER ;