use homework;
-- 所有用户信息视图
CREATE VIEW admin_user_view AS
SELECT user_id, email, role, registered_at
FROM users;
