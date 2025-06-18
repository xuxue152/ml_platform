-- 用户个人信息视图
CREATE VIEW user_profile_view AS
SELECT user_id, username, email, role, registered_at
FROM users;

-- 用户实验信息视图
CREATE VIEW user_experiment_view AS
SELECT experiment_id, name, date, status, parameters, result
FROM experiments;

-- 用户数据集视图
CREATE VIEW user_dataset_view AS
SELECT dataset_id, type, file_path, uploaded_at
FROM datasets;

-- 用户模型视图
CREATE VIEW user_model_view AS
SELECT model_id, model_name, model_type, parameters, trained_at, file_path
FROM models;

-- 用户预测结果视图
CREATE VIEW user_prediction_view AS
SELECT p.prediction_id, m.model_name, d.type AS dataset_type, 
       p.predicted_at, p.metrics
FROM predictions p
JOIN models m ON p.model_id = m.model_id
JOIN datasets d ON p.dataset_id = d.dataset_id;