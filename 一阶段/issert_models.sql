use homework;
-- 分类模型
INSERT INTO models (name, model_type, parameters) VALUES
('randomforest', 'classify', '{"n_estimators": [10, 200], "max_depth": [1, 20], "min_samples_split": [2, 10], "min_samples_leaf": [1, 4], "bootstrap": [true, false]}'),
('logisticregression', 'classify', '{"penalty": ["l1", "l2", "elasticnet", null], "C": [0.001, 100], "solver": ["newton-cg", "lbfgs", "liblinear", "sag", "saga"], "max_iter": [100, 500]}'),
('svm', 'classify', '{"C": [0.1, 100], "kernel": ["linear", "poly", "rbf", "sigmoid"], "gamma": ["scale", "auto", 0.1, 10], "degree": [2, 4]}'),
('decisiontree', 'classify', '{"criterion": ["gini", "entropy"], "max_depth": [1, 20], "min_samples_split": [2, 10], "min_samples_leaf": [1, 4]}'),
('mlp_c', 'classify', '{"hidden_layer_sizes": [[50], [100], [50, 50], [100, 50], [100, 100]], "activation": ["identity", "logistic", "tanh", "relu"], "solver": ["lbfgs", "sgd", "adam"], "alpha": [0.0001, 0.01], "learning_rate": ["constant", "invscaling", "adaptive"]}'),
('gbdt', 'classify', '{"n_estimators": [50, 200], "learning_rate": [0.01, 0.2], "max_depth": [3, 7], "min_samples_split": [2, 5], "min_samples_leaf": [1, 2]}'),
('adaboost', 'classify', '{"n_estimators": [50, 200], "learning_rate": [0.01, 1.0], "algorithm": ["SAMME", "SAMME.R"]}'),
('bagging', 'classify', '{"n_estimators": [10, 100], "max_samples": [0.5, 1.0], "max_features": [0.5, 1.0], "bootstrap": [true, false]}'),
('extratrees', 'classify', '{"n_estimators": [10, 200], "max_depth": [1, 20], "min_samples_split": [2, 10], "min_samples_leaf": [1, 4], "bootstrap": [true, false]}'),
('ridge', 'classify', '{"alpha": [0.1, 10.0], "fit_intercept": [true, false], "normalize": [true, false]}'),
('sgd', 'classify', '{"loss": ["hinge", "log_loss", "modified_huber", "squared_hinge", "perceptron"], "penalty": ["l2", "l1", "elasticnet"], "alpha": [0.0001, 0.01], "max_iter": [1000, 5000]}'),
('linearsvm', 'classify', '{"C": [0.1, 100], "loss": ["hinge", "squared_hinge"], "max_iter": [1000, 5000]}'),
('nusvm', 'classify', '{"nu": [0.1, 0.9], "kernel": ["linear", "poly", "rbf", "sigmoid"], "degree": [2, 4], "gamma": ["scale", "auto"]}'),
('extratree', 'classify', '{"criterion": ["gini", "entropy"], "max_depth": [1, 20], "min_samples_split": [2, 10], "min_samples_leaf": [1, 4]}'),
('gaussiannb', 'classify', '{"var_smoothing": [1e-9, 1e-7]}'),
('bernoullinb', 'classify', '{"alpha": [0.1, 1.0], "binarize": [0.0, 1.0], "fit_prior": [true, false]}'),
('multinomialnb', 'classify', '{"alpha": [0.1, 1.0], "fit_prior": [true, false]}'),
('knn', 'classify', '{"n_neighbors": [3, 10], "weights": ["uniform", "distance"], "algorithm": ["auto", "ball_tree", "kd_tree", "brute"], "p": [1, 2]}'),
('radiusnn', 'classify', '{"radius": [1.0, 10.0], "weights": ["uniform", "distance"], "p": [1, 2]}'),
('lda', 'classify', '{"solver": ["svd", "lsqr", "eigen"], "shrinkage": ["auto", null, 0.0, 1.0], "n_components": [null, 1, 2], "tol": [1e-4, 1e-2]}'),
('qda', 'classify', '{"reg_param": [0.0, 1.0], "tol": [1e-4, 1e-2]}'),
('gpc', 'classify', '{"kernel": [null], "max_iter_predict": [100, 500]}');

-- 回归模型
INSERT INTO models (name, model_type, parameters) VALUES
('mlp_r', 'regression', '{"hidden_layer_sizes": [[50], [100], [50, 50], [100, 50], [100, 100]], "activation": ["identity", "logistic", "tanh", "relu"], "solver": ["lbfgs", "sgd", "adam"], "alpha": [0.0001, 0.01], "learning_rate": ["constant", "invscaling", "adaptive"], "max_iter": [200, 500]}'),
('linearregression', 'regression', '{"fit_intercept": [true, false], "normalize": [true, false], "positive": [true, false]}'),
('ridgeregression', 'regression', '{"alpha": [0.1, 10.0], "fit_intercept": [true, false], "normalize": [true, false], "solver": ["auto", "svd", "cholesky", "lsqr", "sparse_cg"]}'),
('lasso', 'regression', '{"alpha": [0.1, 10.0], "fit_intercept": [true, false], "normalize": [true, false], "selection": ["cyclic", "random"]}'),
('elasticnet', 'regression', '{"alpha": [0.1, 10.0], "l1_ratio": [0.1, 0.9], "fit_intercept": [true, false], "normalize": [true, false]}'),
('sgdregressor', 'regression', '{"loss": ["squared_error", "huber", "epsilon_insensitive"], "penalty": ["l2", "l1", "elasticnet"], "alpha": [0.0001, 0.01], "max_iter": [1000, 5000]}'),
('bayesianridge', 'regression', '{"alpha_1": [1e-6, 1e-4], "alpha_2": [1e-6, 1e-4], "lambda_1": [1e-6, 1e-4], "lambda_2": [1e-6, 1e-4], "fit_intercept": [true, false]}'),
('randomforestreg', 'regression', '{"n_estimators": [10, 200], "max_depth": [1, 20], "min_samples_split": [2, 10], "min_samples_leaf": [1, 4]}'),
('gbdtreg', 'regression', '{"n_estimators": [50, 200], "learning_rate": [0.01, 0.2], "max_depth": [3, 7], "min_samples_split": [2, 5]}'),
('svr', 'regression', '{"kernel": ["linear", "poly", "rbf", "sigmoid"], "C": [0.1, 100], "epsilon": [0.01, 0.5]}'),
('linearsvr', 'regression', '{"C": [0.1, 100], "epsilon": [0.01, 1.0], "loss": ["epsilon_insensitive", "squared_epsilon_insensitive"], "max_iter": [1000, 5000]}'),
('nusvr', 'regression', '{"nu": [0.1, 0.9], "C": [0.1, 100], "kernel": ["linear", "poly", "rbf", "sigmoid"], "degree": [2, 4], "gamma": ["scale", "auto"]}');