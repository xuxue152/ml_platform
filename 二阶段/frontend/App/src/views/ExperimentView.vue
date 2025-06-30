<template>
  <div class="predictions-container">
    <div class="header-section">
      <h1>预测管理</h1>
      <div class="header-actions">
        <button @click="refreshData" class="refresh-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21.5 2v6h-6M2.5 22v-6h6M21.5 22a10 10 0 0 0-10-10 10 10 0 0 0-1.8.15M2.5 2a10 10 0 0 0 10 10 10 10 0 0 0 1.8-.15"></path>
          </svg>
          刷新数据
        </button>
        <button @click="showCreateDialog = true" class="create-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          新建预测
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>加载预测中...</p>
    </div>

    <div v-else-if="predictions.length === 0" class="empty-state">
      <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
      </svg>
      <h3>暂无预测</h3>
      <p>点击上方按钮创建您的第一个预测</p>
    </div>

    <div v-else class="predictions-grid">
      <div v-for="prediction in predictions" :key="prediction.prediction_id" class="prediction-card">
        <div class="prediction-content" @click="showPredictionDetail(prediction)">
          <div class="prediction-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
            </svg>
          </div>
          <h3 class="prediction-name">{{ prediction.name }}</h3>
          <div class="prediction-meta">
            <span class="meta-item">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5"></path>
                <path d="M8.5 8.5v.01"></path>
                <path d="M16 15.5v.01"></path>
                <path d="M12 12v.01"></path>
                <path d="M11 17v.01"></path>
                <path d="M7 14v.01"></path>
              </svg>
              模型: {{ prediction.model_name }}
            </span>
            <span class="meta-item" :class="getStatusClass(prediction.status)">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
              </svg>
              状态: {{ getStatusText(prediction.status) }}
            </span>
          </div>
          <div class="prediction-meta">
            <span class="meta-item">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              创建于: {{ formatDate(prediction.created_at) }}
            </span>
          </div>
        </div>
        <div class="prediction-actions">
          <button
            @click.stop="runPrediction(prediction.prediction_id)"
            class="action-btn run-btn"
            :disabled="prediction.status === 'training'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            运行
          </button>
          <button @click.stop="confirmDelete(prediction.prediction_id)" class="action-btn delete-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              <line x1="10" y1="11" x2="10" y2="17"></line>
              <line x1="14" y1="11" x2="14" y2="17"></line>
            </svg>
            删除
          </button>
        </div>
      </div>
    </div>

    <!-- 创建预测对话框 -->
    <div v-if="showCreateDialog" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>创建新预测</h3>
          <button @click="showCreateDialog = false" class="close-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="input-group">
            <label for="prediction-name">预测名称</label>
            <input
              id="prediction-name"
              v-model="newPrediction.name"
              type="text"
              placeholder="输入预测名称"
            />
          </div>

          <div class="input-group">
            <label>选择模型</label>
            <select v-model="newPrediction.model_name" @change="loadModelParams">
              <option value="" disabled>请选择模型</option>
              <option v-for="model in models" :key="model.name" :value="model.name">
                {{ model.name }} ({{ model.type }})
              </option>
            </select>
          </div>

          <div class="input-group">
            <label>选择数据集</label>
            <select v-model="newPrediction.dataset_name">
              <option value="" disabled>请选择数据集</option>
              <option v-for="dataset in datasets" :key="dataset.name" :value="dataset.name">
                {{ dataset.name }}
              </option>
            </select>
          </div>

          <div v-if="modelParams.length > 0" class="params-section">
            <h4>模型参数配置</h4>
            <div v-for="param in modelParams" :key="param.name" class="param-item">
              <label>{{ param.label }} ({{ param.name }})</label>

              <!-- 数值范围参数 -->
              <div v-if="param.type === 'range'" class="range-param">
                <input
                  type="range"
                  v-model.number="newPrediction.parameters[param.name]"
                  :min="param.options[0]"
                  :max="param.options[1]"
                  :step="param.step || 1"
                  class="slider"
                >
                <input
                  type="number"
                  v-model.number="newPrediction.parameters[param.name]"
                  :min="param.options[0]"
                  :max="param.options[1]"
                  class="number-input"
                >
                <span class="range-values">{{ param.options[0] }} - {{ param.options[1] }}</span>
              </div>

              <!-- 枚举类型参数 -->
              <select v-else v-model="newPrediction.parameters[param.name]">
                <option v-for="option in param.options" :key="option" :value="option">
                  {{ option }}
                </option>
              </select>
            </div>
          </div>

          <div class="metrics-section">
            <h4>评估指标</h4>
            <div class="metrics-grid">
              <div v-for="metric in availableMetrics" :key="metric.value" class="metric-item">
                <label>
                  <input type="checkbox" v-model="newPrediction.metrics[metric.value]">
                  {{ metric.label }}
                </label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCreateDialog = false" class="cancel-btn">取消</button>
          <button
            @click="createPrediction"
            class="confirm-btn"
            :disabled="!isFormValid"
          >
            创建
          </button>
        </div>
      </div>
    </div>

    <!-- 预测详情对话框 -->
    <div v-if="selectedPrediction" class="detail-overlay">
      <div class="detail-content">
        <div class="detail-header">
          <h3>{{ selectedPrediction.name }}</h3>
          <button @click="selectedPrediction = null" class="close-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="detail-body">
          <div class="detail-section">
            <h4>基本信息</h4>
            <div class="detail-row">
              <span class="detail-label">预测ID:</span>
              <span class="detail-value">{{ selectedPrediction.prediction_id }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">模型名称:</span>
              <span class="detail-value">{{ selectedPrediction.model_name }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">数据集:</span>
              <span class="detail-value">{{ selectedPrediction.dataset_name }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">状态:</span>
              <span class="detail-value" :class="getStatusClass(selectedPrediction.status)">
                {{ getStatusText(selectedPrediction.status) }}
              </span>
            </div>
            <div class="detail-row">
              <span class="detail-label">创建时间:</span>
              <span class="detail-value">{{ formatDateTime(selectedPrediction.created_at) }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">运行时间:</span>
              <span class="detail-value">{{ selectedPrediction.predicted_at ? formatDateTime(selectedPrediction.predicted_at) : '未运行' }}</span>
            </div>
          </div>

          <div class="detail-section">
            <h4>模型参数</h4>
            <div class="params-grid">
              <div v-for="(value, key) in selectedPrediction.parameters" :key="key" class="param-row">
                <span class="param-label">{{ key }}:</span>
                <span class="param-value">{{ value }}</span>
              </div>
            </div>
          </div>

          <div v-if="selectedPrediction.status === 'completed'" class="detail-section">
            <h4>评估结果</h4>
            <div class="metrics-grid">
              <div v-for="(value, key) in selectedPrediction.metrics" :key="key" class="metric-row">
                <span class="metric-label">{{ key }}:</span>
                <span class="metric-value">
                  {{ typeof value === 'object' ? JSON.stringify(value) : value }}
                </span>
              </div>
            </div>
          </div>

          <div v-if="selectedPrediction.status === 'failed'" class="detail-section error-section">
            <h4>错误信息</h4>
            <div class="error-message">
              {{ selectedPrediction.error_message || '未知错误' }}
            </div>
          </div>
        </div>
        <div class="detail-footer">
          <button
            @click="runPrediction(selectedPrediction.prediction_id)"
            class="action-btn run-btn"
            :disabled="selectedPrediction.status === 'training'"
          >
            运行预测
          </button>
          <button @click="selectedPrediction = null" class="action-btn close-btn">
            关闭
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const projectName = route.params.name
const userId = localStorage.getItem('user_id')
const experimentId = localStorage.getItem('experiment_id')
const experimentName = route.params.experiment_name
const predictions = ref([])
const loading = ref(true)
const showCreateDialog = ref(false)
const selectedPrediction = ref(null)
const models = ref([])
const datasets = ref([])

const newPrediction = ref({
  name: '',
  model_name: '',
  dataset_name: '',
  parameters: {},
  metrics: {}
})

const modelParams = ref([])

const availableMetrics = [
  { value: 'accuracy', label: '准确率' },
  { value: 'f1', label: 'F1值' },
  { value: 'precision', label: '精确率' },
  { value: 'recall', label: '召回率' },
  { value: 'roc_auc', label: 'AUC值' },
  { value: 'log_loss', label: '对数损失' },
  { value: 'confusion_matrix', label: '混淆矩阵' },
  { value: 'classification_report', label: '分类报告' },
  { value: 'mse', label: '均方误差' },
  { value: 'mae', label: '平均绝对误差' },
  { value: 'r2', label: 'R²决定系数' },
  { value: 'explained_variance', label: '可解释方差' },
  { value: 'median_absolute_error', label: '中位绝对误差' }
]

const paramsMap = {
  "randomforest": {
    "n_estimators": [10, 200],
    "max_depth": [1, 20],
    "min_samples_split": [2, 10],
    "min_samples_leaf": [1, 4],
    "bootstrap": [true, false]
  },
  "logisticregression": {
    "penalty": ["l1", "l2", "elasticnet", null],
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
    "hidden_layer_sizes": [[50], [100], [50, 50], [100, 50], [100, 100]],
    "activation": ["identity", "logistic", "tanh", "relu"],
    "solver": ["lbfgs", "sgd", "adam"],
    "alpha": [0.0001, 0.01],
    "learning_rate": ["constant", "invscaling", "adaptive"]
  },
  "mlp-r": {
    "hidden_layer_sizes": [[50], [100], [50, 50], [100, 50], [100, 100]],
    "activation": ["identity", "logistic", "tanh", "relu"],
    "solver": ["lbfgs", "sgd", "adam"],
    "alpha": [0.0001, 0.01],
    "learning_rate": ["constant", "invscaling", "adaptive"],
    "max_iter": [200, 500]
  },
  "lda": {
    "solver": ["svd", "lsqr", "eigen"],
    "shrinkage": ["auto", null, 0.0, 1.0],
    "n_components": [null, 1, 2],
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
    "bootstrap": [true, false]
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
  "linearregression": {
    "fit_intercept": [true, false],
    "normalize": [true, false],
    "positive": [true, false]
  },
  "ridgeregression": {
    "alpha": [0.1, 10.0],
    "fit_intercept": [true, false],
    "normalize": [true, false],
    "solver": ["auto", "svd", "cholesky", "lsqr", "sparse_cg"]
  },
  "lasso": {
    "alpha": [0.1, 10.0],
    "fit_intercept": [true, false],
    "normalize": [true, false],
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
    "bootstrap": [true, false]
  },
  "ridge": {
    "alpha": [0.1, 10.0],
    "fit_intercept": [true, false],
    "normalize": [true, false]
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
    "fit_prior": [true, false]
  },
  "multinomialnb": {
    "alpha": [0.1, 1.0],
    "fit_prior": [true, false]
  },
  "radiusnn": {
    "radius": [1.0, 10.0],
    "weights": ["uniform", "distance"],
    "p": [1, 2]
  },
  "gpc": {
    "kernel": [null],
    "max_iter_predict": [100, 500]
  },
  "elasticnet": {
    "alpha": [0.1, 10.0],
    "l1_ratio": [0.1, 0.9],
    "fit_intercept": [true, false],
    "normalize": [true, false]
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
    "fit_intercept": [true, false]
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
    "bidirectional": [true, false],
    "dropout": [0.0, 0.5]
  },
  "lstm": {
    "hidden_size": [64, 256],
    "num_layers": [1, 3],
    "bidirectional": [true, false],
    "dropout": [0.0, 0.5]
  },
  "gru": {
    "hidden_size": [64, 256],
    "num_layers": [1, 3],
    "bidirectional": [true, false],
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
    "pretrained": [true, false],
    "num_classes": [10, 1000]
  },
  "unet": {
    "encoder_name": ["resnet34", "resnet50"],
    "encoder_weights": ["imagenet", null],
    "classes": [1, 3, 21],
    "activation": ["sigmoid", "softmax2d"]
  },
  "autoencoder": {
    "input_dim": [64, 256],
    "latent_dim": [16, 64],
    "num_layers": [1, 3],
    "activation": ["relu", "tanh"]
  }
};


// 获取所有预测
const fetchPredictions = async () => {
  try {
    loading.value = true
    const response = await axios.post(
      `http://localhost:8000/api/experiments/${experimentName}/predictions`,
      { experiment_id: experimentId }
    )
    predictions.value = response.data
  } catch (error) {
    console.error('获取预测列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 获取所有模型
const fetchModels = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/all_models')
    models.value = response.data
  } catch (error) {
    console.error('获取模型列表失败:', error)
  }
}

// 获取所有数据集
const fetchDatasets = async () => {
  try {
    const response = await axios.post(
      `http://localhost:8000/api/projects/${projectName}/datasets`,
      { user_id: userId }
    )
    datasets.value = response.data
  } catch (error) {
    console.error('获取数据集列表失败:', error)
  }
}

// 刷新数据
const refreshData = async () => {
  await fetchPredictions()
}

// 加载模型参数
const loadModelParams = () => {
  const modelName = newPrediction.value.model_name
  if (!modelName || !paramsMap[modelName]) {
    modelParams.value = []
    newPrediction.value.parameters = {}
    return
  }

  const params = paramsMap[modelName]
  modelParams.value = Object.keys(params).map(name => {
    const options = params[name]
    const isRange = Array.isArray(options) && options.length === 2 &&
                   typeof options[0] === 'number' && typeof options[1] === 'number'

    return {
      name,
      label: name.replace(/_/g, ' '),
      type: isRange ? 'range' : 'enum',
      options: isRange ? options : Array.isArray(options) ? options : [options],
      step: isRange ? (options[1] - options[0]) / 100 : undefined
    }
  })

  // 初始化参数默认值
  newPrediction.value.parameters = {}
  modelParams.value.forEach(param => {
    if (param.type === 'range') {
      newPrediction.value.parameters[param.name] = param.options[0]
    } else {
      newPrediction.value.parameters[param.name] = param.options[0]
    }
  })

  // 初始化指标选择
  newPrediction.value.metrics = {}
  availableMetrics.forEach(metric => {
    newPrediction.value.metrics[metric.value] = false
  })
}

const createPrediction = async () => {
  if (!isFormValid.value) return

  try {
    const payload = {
      ...newPrediction.value,
      experiment_id: experimentId,
      user_id: userId,
    }

    await axios.post(
      `http://localhost:8000/api/experiments/${experimentId}/create_predictions`,
      payload
    )

    await fetchPredictions()
    showCreateDialog.value = false
    resetNewPrediction()
  } catch (error) {
    if (error.response && error.response.status === 400) {
      alert('预测名称已存在')
    } else {
      console.error('创建预测失败:', error)
    }
  }
}

const runPrediction = async (predictionId) => {
  try {
    const prediction = predictions.value.find(p => p.prediction_id === predictionId)
    if (prediction) {
      prediction.status = 'training'
    }

    await axios.post(
      `http://localhost:8000/api/experiments/${experimentName}/run_prediction`,
      { prediction_id: predictionId }
    )

    await fetchPredictions()
    if (selectedPrediction.value) {
      selectedPrediction.value = predictions.value.find(p => p.prediction_id === predictionId)
    }
  } catch (error) {
    console.error('运行预测失败:', error)
    if (error.response && error.response.data) {
      alert(`运行失败: ${error.response.data.detail}`)
    }
  }
}

const confirmDelete = (predictionId) => {
  if (confirm('确定要删除此预测吗？此操作不可撤销。')) {
    deletePrediction(predictionId)
  }
}

const deletePrediction = async (predictionId) => {
  try {
    await axios.delete(
      `http://localhost:8000/api/experiments/${experimentId}/prediction`,
      {
        data: { prediction_id: predictionId }  // 注意这里使用 data 字段
      }
    )
    await fetchPredictions()
    if (selectedPrediction.value?.prediction_id === predictionId) {
      selectedPrediction.value = null
    }
  } catch (error) {
    console.error('删除预测失败:', error)
  }
}

const showPredictionDetail = (prediction) => {
  selectedPrediction.value = { ...prediction }
}

const resetNewPrediction = () => {
  newPrediction.value = {
    name: '',
    model_name: '',
    dataset_name: '',
    parameters: {},
    metrics: {}
  }
  modelParams.value = []
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const options = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

const formatDateTime = (dateString) => {
  if (!dateString) return ''
  const options = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

const getStatusClass = (status) => {
  switch (status) {
    case 'completed': return 'status-completed'
    case 'failed': return 'status-failed'
    case 'training': return 'status-training'
    default: return 'status-pending'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'completed': return '已完成'
    case 'failed': return '失败'
    case 'training': return '训练中'
    default: return '待处理'
  }
}

const isFormValid = computed(() => {
  return (
    newPrediction.value.name.trim() &&
    newPrediction.value.model_name &&
    newPrediction.value.dataset_name &&
    Object.values(newPrediction.value.metrics).some(v => v)
  )
})

onMounted(() => {
  fetchPredictions()
  fetchModels()
  fetchDatasets()
})
</script>

<style scoped>
.predictions-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-section h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 600;
  color: #2d3748;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #edf2f7;
  border: none;
  border-radius: 6px;
  color: #4a5568;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background-color: #e2e8f0;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background-color: #4361ee;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.create-btn:hover {
  background-color: #3a56d4;
  transform: translateY(-1px);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 5px solid #e2e8f0;
  border-top: 5px solid #4361ee;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
  text-align: center;
  color: #718096;
}

.empty-state h3 {
  font-size: 1.25rem;
  margin: 1rem 0 0.5rem;
  color: #2d3748;
}

.empty-state p {
  font-size: 0.95rem;
}

.predictions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.prediction-card {
  position: relative;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
}

.prediction-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.prediction-content {
  flex: 1;
  cursor: pointer;
}

.prediction-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
  color: #4361ee;
}

.prediction-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #2d3748;
  text-align: center;
}

.prediction-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  font-size: 0.85rem;
  color: #718096;
  margin-bottom: 0.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  background-color: #f7fafc;
}

.status-completed {
  background-color: #f0fff4;
  color: #38a169;
}

.status-failed {
  background-color: #fff5f5;
  color: #e53e3e;
}

.status-training {
  background-color: #fffaf0;
  color: #dd6b20;
}

.status-pending {
  background-color: #ebf8ff;
  color: #3182ce;
}

.prediction-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.run-btn {
  background-color: #ebf8ff;
  color: #3182ce;
}

.run-btn:hover:not(:disabled) {
  background-color: #bee3f8;
}

.delete-btn {
  background-color: #fff5f5;
  color: #e53e3e;
}

.delete-btn:hover {
  background-color: #fed7d7;
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 模态框样式 */
.modal-overlay, .detail-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content, .detail-content {
  background-color: white;
  border-radius: 12px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.detail-content {
  max-width: 900px;
}

.modal-header, .detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3, .detail-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #718096;
  cursor: pointer;
  padding: 0.25rem;
}

.close-btn:hover {
  color: #2d3748;
}

.modal-body, .detail-body {
  padding: 1.5rem;
  overflow-y: auto;
}

.detail-body {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.input-group {
  margin-bottom: 1.5rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #4a5568;
}

.input-group input,
.input-group select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.input-group input:focus,
.input-group select:focus {
  outline: none;
  border-color: #4361ee;
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
}

.params-section, .metrics-section {
  margin-top: 1.5rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

.params-section h4, .metrics-section h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1rem;
  color: #2d3748;
}

.param-item {
  margin-bottom: 1rem;
}

.param-item label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #4a5568;
}

.range-param {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.slider {
  flex: 1;
}

.number-input {
  width: 80px;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
}

.range-values {
  font-size: 0.75rem;
  color: #718096;
  min-width: 100px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.75rem;
}

.metric-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.metric-item label {
  font-size: 0.875rem;
  cursor: pointer;
}

.modal-footer, .detail-footer {
  display: flex;
  justify-content: flex-end;
  padding: 1.25rem 1.5rem;
  border-top: 1px solid #e2e8f0;
  gap: 0.75rem;
}

.cancel-btn {
  padding: 0.75rem 1.25rem;
  background-color: #edf2f7;
  border: none;
  border-radius: 8px;
  color: #4a5568;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn:hover {
  background-color: #e2e8f0;
}

.confirm-btn {
  padding: 0.75rem 1.25rem;
  background-color: #4361ee;
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.confirm-btn:hover:not(:disabled) {
  background-color: #3a56d4;
}

.confirm-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 详情样式 */
.detail-section {
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

.detail-section h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1rem;
  color: #2d3748;
}

.detail-row {
  display: flex;
  margin-bottom: 0.75rem;
}

.detail-label {
  font-weight: 500;
  color: #4a5568;
  min-width: 100px;
}

.detail-value {
  color: #718096;
}

.params-grid, .metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
}

.param-row, .metric-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background-color: #f7fafc;
  border-radius: 4px;
}

.param-label, .metric-label {
  font-weight: 500;
}

.param-value, .metric-value {
  color: #718096;
}

.error-section {
  background-color: #fff5f5;
  border-color: #fed7d7;
}

.error-message {
  color: #e53e3e;
  white-space: pre-wrap;
}

@media (max-width: 768px) {
  .predictions-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }

  .header-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .modal-content, .detail-content {
    width: 95%;
  }

  .params-grid, .metrics-grid {
    grid-template-columns: 1fr;
  }
}
</style>
