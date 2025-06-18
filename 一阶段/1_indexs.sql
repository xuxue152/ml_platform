-- 用户表索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- 实验表索引
CREATE INDEX idx_experiments_user_id ON experiments(user_id);
CREATE INDEX idx_experiments_status ON experiments(status);
CREATE INDEX idx_experiments_date ON experiments(date);

-- 数据集表索引
CREATE INDEX idx_datasets_user_id ON datasets(user_id);
CREATE INDEX idx_datasets_type ON datasets(type);

-- 模型表索引
CREATE INDEX idx_models_user_id ON models(user_id);
CREATE INDEX idx_models_model_type ON models(model_type);

-- 预测表索引
CREATE INDEX idx_predictions_model_id ON predictions(model_id);
CREATE INDEX idx_predictions_dataset_id ON predictions(dataset_id);