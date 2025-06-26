use homework;
-- 用户个人信息视图
CREATE OR REPLACE VIEW user_profile_view AS
SELECT
    user_id,
    email,
    role,
    registered_at,
    (SELECT COUNT(*) FROM experiments WHERE user_id = users.user_id) AS experiment_count,
    (SELECT COUNT(*) FROM models WHERE user_id = users.user_id) AS model_count,
    (SELECT COUNT(*) FROM datasets WHERE user_id = users.user_id) AS dataset_count
FROM
    users;

