use homework;

-- 删除项目及其关联实验
DELIMITER //
CREATE PROCEDURE user_delete_project(IN p_project_name VARCHAR(100),IN p_user_id INT)
BEGIN
    -- 删除该项目关联的实验
    DELETE FROM experiments WHERE project_name = p_project_name AND user_id = p_user_id;
    -- 删除该项目本身
    DELETE FROM projects WHERE name = p_project_name AND user_id = p_user_id;
END //
DELIMITER ;

-- 删除实验及其关联预测
DELIMITER //
CREATE PROCEDURE user_delete_experiment(IN p_experiment_id int)
BEGIN
    -- 删除该实验关联的预测
    DELETE FROM predictions WHERE experiment_id = p_experiment_id;
    -- 删除该实验本身
    DELETE FROM experiments WHERE name = p_experiment_id;
END //
DELIMITER ;

-- 删除预测
DELIMITER //
CREATE PROCEDURE user_delete_prediction(IN p_prediction_id int)
BEGIN
    DELETE FROM predictions WHERE prediction_id = p_prediction_id;
END;
//
DELIMITER ;

-- 删除数据集
DELIMITER //
CREATE PROCEDURE user_delete_dataset(IN p_user_id int,IN p_dataset_name VARCHAR(100))
BEGIN
    DELETE FROM datasets WHERE user_id = p_user_id AND name = p_dataset_name;
END;
//
DELIMITER ;

-- 通过名称返回数据集对应的path
DELIMITER //
CREATE PROCEDURE get_dataset_path(
    IN p_dataset_name VARCHAR(100),
    OUT p_file_path VARCHAR(255)
)
BEGIN
    SELECT file_path
    INTO p_file_path
    FROM datasets
    WHERE name = p_dataset_name;
END //
DELIMITER ;

-- 返回用户项目
DELIMITER //
create
    definer = root@localhost procedure get_user_projects(IN p_user_id int)
BEGIN
    SELECT
        name AS project_name,
        created_at
    FROM
        projects
    WHERE
        user_id = p_user_id;
END//
DELIMITER ;

-- 返回用户实验信息
DELIMITER //
create
    definer = root@localhost procedure get_user_experiments(IN p_user_id int,p_project_name VARCHAR(100))
BEGIN
    SELECT
        e.experiment_id,
        e.name,
        (SELECT COUNT(*) FROM predictions WHERE experiment_id = e.experiment_id) AS prediction_count
    FROM
        experiments e,projects p
    WHERE
        e.user_id = p_user_id AND p.name=p_project_name;
END //
DELIMITER ;

-- 返回用户项目
DELIMITER //
create
    definer = root@localhost procedure get_user_projects(IN p_user_id int)
BEGIN
    SELECT
        name AS project_name,
        created_at
    FROM
        projects
    WHERE
        user_id = p_user_id;
END//
DELIMITER ;

-- 返回用户数据集
DELIMITER //
create
    definer = root@localhost procedure get_user_datasets(IN p_user_id int)
BEGIN
    SELECT
        name AS dataset_name,
        file_path,
        uploaded_at
    FROM
        datasets
    WHERE
        user_id = p_user_id;
END//
DELIMITER ;

-- 返回模型
DELIMITER //
CREATE DEFINER = root@localhost PROCEDURE get_all_models()
BEGIN
    SELECT
        name AS model_name,
        model_type,
        parameters
    FROM
        models;
END //
DELIMITER ;

-- 返回实验所有预测
DELIMITER //
create
    definer = root@localhost procedure get_predictions(IN p_experiment_id int)
BEGIN
    SELECT
        p.prediction_id
    FROM
        predictions p
    WHERE
        p.experiment_id = p_experiment_id;
END //
DELIMITER ;

-- 返回预测结果
DELIMITER //
create
    definer = root@localhost procedure get_prediction(IN p_prediction_id int)
BEGIN
    SELECT
        p.model_name,
        p.dataset_name,
        p.parameters,
        p.status,
        p.predicted_at,
        p.metrics
    FROM
        predictions p
    WHERE
        p.prediction_id=p_prediction_id;
END //
DELIMITER ;
