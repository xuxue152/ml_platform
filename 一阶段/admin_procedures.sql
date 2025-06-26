use homework;
-- 删除用户及其所有关联数据
DELIMITER //
CREATE PROCEDURE admin_delete_user(IN p_user_id INT)
BEGIN
    -- 先删除依赖数据
    DELETE FROM predictions WHERE model_name IN (SELECT name FROM models WHERE user_id = p_user_id);
    DELETE FROM model_dataset WHERE model_name IN (SELECT name FROM models WHERE user_id = p_user_id);
    DELETE FROM models WHERE user_id = p_user_id;
    DELETE FROM experiments WHERE user_id = p_user_id;
    DELETE FROM datasets WHERE user_id = p_user_id;
    -- 最后删除用户
    DELETE FROM users WHERE user_id = p_user_id;
END //
DELIMITER ;

-- 删除实验及其关联数据
DELIMITER //
CREATE PROCEDURE admin_delete_experiment(IN p_experiment_id INT)
BEGIN
    -- 删除实验
    DELETE FROM experiments WHERE experiment_id = p_experiment_id;
END //
DELIMITER ;