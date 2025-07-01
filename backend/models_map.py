from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier,
                              AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier)
from sklearn.linear_model import (LogisticRegression, RidgeClassifier,
                                  SGDClassifier)
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR, LinearSVR, NuSVR
from sklearn.linear_model import (LinearRegression, Ridge, Lasso,
                                  ElasticNet, SGDRegressor, BayesianRidge)

from sklearn.neural_network import MLPClassifier, MLPRegressor
from xgboost import XGBClassifier
from lightgbm import LGBMRegressor
from catboost import CatBoostClassifier

model_name_map = {
    # 分类模型
    "randomforest": "随机森林分类器",
    "logisticregression": "逻辑回归",
    "svm": "支持向量机",
    "decisiontree": "决策树分类器",
    "gbdt": "梯度提升分类器",
    "adaboost": "自适应提升分类器",
    "bagging": "Bagging 分类器",
    "extratrees": "极端随机森林分类器",
    "ridge": "岭分类器",
    "sgd": "随机梯度下降分类器",
    "linearsvm": "线性支持向量机",
    "nusvm": "Nu支持向量机分类器",
    "extratree": "极端随机树分类器",
    "gaussiannb": "高斯朴素贝叶斯分类器",
    "bernoullinb": "伯努利朴素贝叶斯分类器",
    "multinomialnb": "多项式朴素贝叶斯分类器",
    "knn": "K近邻分类器",
    "radiusnn": "基于半径的近邻分类器",
    "lda": "线性判别分析",
    "qda": "二次判别分析",
    "gpc": "高斯过程分类器",
    "mlp_c": "多层感知机分类器",

    # 回归模型
    "linearregression": "线性回归",
    "ridgeregression": "岭回归",
    "lasso": "Lasso 回归",
    "elasticnet": "ElasticNet 回归",
    "sgdregressor": "随机梯度下降回归",
    "bayesianridge": "贝叶斯岭回归",
    "randomforestreg": "随机森林回归",
    "gbdtreg": "梯度提升回归",
    "svr": "支持向量回归",
    "linearsvr": "线性支持向量回归",
    "nusvr": "Nu 支持向量回归",
    "mlp_r": "多层感知机回归器",
    "xgboost": "极端梯度提升分类器",
    "lightgbm": "轻量梯度提升回归器",
    "catboost": "类别提升分类器"
}



sklearn_model_map = {
    # 分类模型
    "randomforest": RandomForestClassifier,
    "logisticregression": LogisticRegression,
    "svm": SVC,
    "decisiontree": DecisionTreeClassifier,
    "mlp_c": MLPClassifier,
    "mlp_r": MLPRegressor,
    "gbdt": GradientBoostingClassifier,
    "adaboost": AdaBoostClassifier,
    "bagging": BaggingClassifier,
    "extratrees": ExtraTreesClassifier,
    "ridge": RidgeClassifier,
    "sgd": SGDClassifier,
    "linearsvm": LinearSVC,
    "nusvm": NuSVC,
    "extratree": ExtraTreeClassifier,
    "gaussiannb": GaussianNB,
    "bernoullinb": BernoulliNB,
    "multinomialnb": MultinomialNB,
    "knn": KNeighborsClassifier,
    "radiusnn": RadiusNeighborsClassifier,
    "lda": LinearDiscriminantAnalysis,
    "qda": QuadraticDiscriminantAnalysis,
    "gpc": GaussianProcessClassifier,
    "xgboost": XGBClassifier,
    "catboost": CatBoostClassifier,
    # 回归模型
    "linearregression": LinearRegression,
    "ridgeregression": Ridge,
    "lasso": Lasso,
    "elasticnet": ElasticNet,
    "sgdregressor": SGDRegressor,
    "bayesianridge": BayesianRidge,
    "randomforestreg": RandomForestRegressor,
    "gbdtreg": GradientBoostingRegressor,
    "svr": SVR,
    "linearsvr": LinearSVR,
    "nusvr": NuSVR,
    "lightgbm": LGBMRegressor

}

params_map = {
    # 分类模型参数
    "randomforest": {
        "n_estimators": [10, 200],
        "max_depth": [1, 20],
        "min_samples_split": [2, 10],
        "min_samples_leaf": [1, 4],
        "bootstrap": [True, False]
    },
    "logisticregression": {
        "penalty": ["l1", "l2", "elasticnet", None],
        "C": [0.001, 100],
        "solver": ["newton-cg", "lbfgs", "liblinear", "sag", "saga"],
        "max_iter": [100, 500]
    },
    "svm": {
        "C": [0.1, 100],
        "kernel": ["linear", "poly", "rbf", "sigmoid"],
        "gamma": ["scale", "auto", 0.1, 10],
        "degree": [2, 4]
    },
    "decisiontree": {
        "criterion": ["gini", "entropy"],
        "max_depth": [1, 20],
        "min_samples_split": [2, 10],
        "min_samples_leaf": [1, 4]
    },
    "mlp_c": {
        "hidden_layer_sizes": [(50,), (100,), (50, 50), (100, 50), (100, 100)],
        "activation": ["identity", "logistic", "tanh", "relu"],
        "solver": ["lbfgs", "sgd", "adam"],
        "alpha": [0.0001, 0.01],
        "learning_rate": ["constant", "invscaling", "adaptive"]
    },
    "mlp-r": {
    "hidden_layer_sizes": [(50,), (100,), (50, 50), (100, 50), (100, 100)],
    "activation": ["identity", "logistic", "tanh", "relu"],
    "solver": ["lbfgs", "sgd", "adam"],
    "alpha": [0.0001, 0.01],
    "learning_rate": ["constant", "invscaling", "adaptive"],
    "max_iter": [200, 500]
},
    "lda": {
    "solver": ["svd", "lsqr", "eigen"],
    "shrinkage": ["auto", None, 0.0, 1.0],
    "n_components": [None, 1, 2],
    "tol": [1e-4, 1e-2]
},
    "qda": {
    "reg_param": [0.0, 1.0],
    "tol": [1e-4, 1e-2]
},
    "gbdt": {
        "n_estimators": [50, 200],
        "learning_rate": [0.01, 0.2],
        "max_depth": [3, 7],
        "min_samples_split": [2, 5],
        "min_samples_leaf": [1, 2]
    },
    "adaboost": {
        "n_estimators": [50, 200],
        "learning_rate": [0.01, 1.0],
        "algorithm": ["SAMME", "SAMME.R"]
    },
    "bagging": {
        "n_estimators": [10, 100],
        "max_samples": [0.5, 1.0],
        "max_features": [0.5, 1.0],
        "bootstrap": [True, False]
    },
    "knn": {
        "n_neighbors": [3, 10],
        "weights": ["uniform", "distance"],
        "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
        "p": [1, 2]
    },
    "gaussiannb": {
        "var_smoothing": [1e-9, 1e-7]
    },

    # 回归模型参数
    "linearregression": {
        "fit_intercept": [True, False],
        "normalize": [True, False],
        "positive": [True, False]
    },
    "ridgeregression": {
        "alpha": [0.1, 10.0],
        "fit_intercept": [True, False],
        "normalize": [True, False],
        "solver": ["auto", "svd", "cholesky", "lsqr", "sparse_cg"]
    },
    "lasso": {
        "alpha": [0.1, 10.0],
        "fit_intercept": [True, False],
        "normalize": [True, False],
        "selection": ["cyclic", "random"]
    },
    "randomforestreg": {
        "n_estimators": [10, 200],
        "max_depth": [1, 20],
        "min_samples_split": [2, 10],
        "min_samples_leaf": [1, 4]
    },
    "svr": {
        "kernel": ["linear", "poly", "rbf", "sigmoid"],
        "C": [0.1, 100],
        "epsilon": [0.01, 0.5]
    },
    "gbdtreg": {
        "n_estimators": [50, 200],
        "learning_rate": [0.01, 0.2],
        "max_depth": [3, 7],
        "min_samples_split": [2, 5]
    },
    "extratrees": {
        "n_estimators": [10, 200],
        "max_depth": [1, 20],
        "min_samples_split": [2, 10],
        "min_samples_leaf": [1, 4],
        "bootstrap": [True, False]
    },
    "ridge": {
        "alpha": [0.1, 10.0],
        "fit_intercept": [True, False],
        "normalize": [True, False]
    },
    "sgd": {
        "loss": ["hinge", "log_loss", "modified_huber", "squared_hinge", "perceptron"],
        "penalty": ["l2", "l1", "elasticnet"],
        "alpha": [0.0001, 0.01],
        "max_iter": [1000, 5000]
    },
    "linearsvm": {
        "C": [0.1, 100],
        "loss": ["hinge", "squared_hinge"],
        "max_iter": [1000, 5000]
    },
    "nusvm": {
        "nu": [0.1, 0.9],
        "kernel": ["linear", "poly", "rbf", "sigmoid"],
        "degree": [2, 4],
        "gamma": ["scale", "auto"]
    },
    "extratree": {
        "criterion": ["gini", "entropy"],
        "max_depth": [1, 20],
        "min_samples_split": [2, 10],
        "min_samples_leaf": [1, 4]
    },
    "bernoullinb": {
        "alpha": [0.1, 1.0],
        "binarize": [0.0, 1.0],
        "fit_prior": [True, False]
    },
    "multinomialnb": {
        "alpha": [0.1, 1.0],
        "fit_prior": [True, False]
    },
    "radiusnn": {
        "radius": [1.0, 10.0],
        "weights": ["uniform", "distance"],
        "p": [1, 2]
    },
    "gpc": {
        "kernel": [None],  # 默认RBF内核
        "max_iter_predict": [100, 500]
    },

    # 新增回归模型参数
    "elasticnet": {
        "alpha": [0.1, 10.0],
        "l1_ratio": [0.1, 0.9],
        "fit_intercept": [True, False],
        "normalize": [True, False]
    },
    "sgdregressor": {
        "loss": ["squared_error", "huber", "epsilon_insensitive"],
        "penalty": ["l2", "l1", "elasticnet"],
        "alpha": [0.0001, 0.01],
        "max_iter": [1000, 5000]
    },
    "bayesianridge": {
        "alpha_1": [1e-6, 1e-4],
        "alpha_2": [1e-6, 1e-4],
        "lambda_1": [1e-6, 1e-4],
        "lambda_2": [1e-6, 1e-4],
        "fit_intercept": [True, False]
    },
    "linearsvr": {
        "C": [0.1, 100],
        "epsilon": [0.01, 1.0],
        "loss": ["epsilon_insensitive", "squared_epsilon_insensitive"],
        "max_iter": [1000, 5000]
    },
    "nusvr": {
        "nu": [0.1, 0.9],
        "C": [0.1, 100],
        "kernel": ["linear", "poly", "rbf", "sigmoid"],
        "degree": [2, 4],
        "gamma": ["scale", "auto"]
    },
    "cnn": {
        "num_conv_layers": [1, 5],
        "num_filters": [16, 64],
        "kernel_size": [3, 5],
        "activation": ["relu", "tanh"],
        "pooling": ["max", "avg"],
        "fc_units": [64, 256]
    },
    "rnn": {
        "hidden_size": [32, 128],
        "num_layers": [1, 3],
        "bidirectional": [True, False],
        "dropout": [0.0, 0.5]
    },
    "lstm": {
        "hidden_size": [64, 256],
        "num_layers": [1, 3],
        "bidirectional": [True, False],
        "dropout": [0.0, 0.5]
    },
    "gru": {
        "hidden_size": [64, 256],
        "num_layers": [1, 3],
        "bidirectional": [True, False],
        "dropout": [0.0, 0.5]
    },
    "transformer": {
        "num_layers": [2, 12],
        "d_model": [128, 768],
        "num_heads": [4, 12],
        "ffn_dim": [256, 2048],
        "dropout": [0.0, 0.3]
    },
    "bert": {
        "pretrained_model": ["bert-base-uncased", "bert-base-chinese"],
        "max_length": [128, 512],
        "num_labels": [2, 10],
        "dropout": [0.1, 0.3]
    },
    "resnet": {
        "resnet_version": ["resnet18", "resnet50", "resnet101"],
        "pretrained": [True, False],
        "num_classes": [10, 1000]
    },
    "unet": {
        "encoder_name": ["resnet34", "resnet50"],
        "encoder_weights": ["imagenet", None],
        "classes": [1, 3, 21],
        "activation": ["sigmoid", "softmax2d"]
    },
    "autoencoder": {
        "input_dim": [64, 256],
        "latent_dim": [16, 64],
        "num_layers": [1, 3],
        "activation": ["relu", "tanh"]
    },
    "xgboost": {
      "n_estimators": [50, 500],
      "max_depth": [3, 15],
      "learning_rate": [0.01, 0.3],
      "subsample": [0.5, 1.0],
      "colsample_bytree": [0.5, 1.0],
      "min_child_weight": [1, 10],
      "gamma": [0, 5],
      "reg_alpha": [0, 5],
      "reg_lambda": [0, 5]
    },
    "lightgbm": {
      "n_estimators": [50, 500],
      "learning_rate": [0.01, 0.3],
      "num_leaves": [31, 256],
      "max_depth": [3, 15],
      "min_child_samples": [5, 50],
      "subsample": [0.5, 1.0],
      "colsample_bytree": [0.5, 1.0],
      "reg_alpha": [0.0, 5.0],
      "reg_lambda": [0.0, 5.0]
    },
    "catboost": {
      "iterations": [100, 1000],
      "depth": [4, 10],
      "learning_rate": [0.01, 0.3],
      "l2_leaf_reg": [1.0, 10.0],
      "bagging_temperature": [0.0, 1.0],
      "random_strength": [0.0, 1.0]
    }
}
