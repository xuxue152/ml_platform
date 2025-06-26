use homework;
-- 所有用户信息视图
CREATE VIEW admin_user_view AS
SELECT user_id, email, role, registered_at
FROM users;

-- 所有实验信息视图
CREATE VIEW admin_experiment_view AS
SELECT e.experiment_id, u.email, e.model_name, e.name, e.date, e.status, e.parameters
FROM experiments e
JOIN users u ON e.user_id = u.user_id;

-- 用户实验统计视图
CREATE VIEW user_experiment_stats AS
SELECT u.user_id, u.email,
       COUNT(e.experiment_id) AS total_experiments,
       SUM(CASE WHEN e.status = 'completed' THEN 1 ELSE 0 END) AS completed_experiments,
       SUM(CASE WHEN e.status = 'failed' THEN 1 ELSE 0 END) AS failed_experiments
FROM users u
LEFT JOIN experiments e ON u.user_id = e.user_id
GROUP BY u.user_id, u.email;