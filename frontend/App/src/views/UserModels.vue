<template>
  <div class="management-container">
    <div class="management-header">
      <h2>模型库</h2>
      <button @click="fetchmodels" class="refresh-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="23 4 23 10 17 10"></polyline>
          <polyline points="1 20 1 14 7 14"></polyline>
          <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
        </svg>
        刷新数据
      </button>
    </div>

    <div class="card-container">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>

      <div v-else-if="models.length === 0" class="empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19.21 15.98A7 7 0 0 0 8.14 6.23M6 10H2M6 6H2M6 14H2M6 18H2M18 4a2 2 0 0 0-2-2h-1a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2z"></path>
        </svg>
        <p>暂无模型数据</p>
      </div>

      <div v-else class="table-responsive">
        <table class="data-table">
          <thead>
            <tr>
              <th>模型名称</th>
              <th>中文名</th>
              <th>参数</th>
              <th>模型类别</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="exp in models" :key="exp.name">
              <td>{{ exp.name }}</td>
              <td>{{ exp.chinese_name}}</td>
              <td>{{ getParameterKeys(exp.parameters) }}</td>
              <td>
                <span :class="['role-badge', { 'classify': exp.model_type === 'classify'}]">
                  {{ exp.model_type }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const models = ref([])
const loading = ref(true)

const fetchmodels = async () => {
  try {
    loading.value = true
    const response = await axios.get('http://localhost:8000/api/all_models')
    models.value = response.data
  } catch (error) {

    console.error('获取模型数据失败:', error)
  } finally {
    loading.value = false
  }
}

const getParameterKeys = (paramStr) => {
  try {
    const parsed = JSON.parse(paramStr)
    return Object.keys(parsed).join(', ')
  } catch (e) {
    return '参数错误'
  }
}

onMounted(fetchmodels)
</script>

<style scoped>
.role-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  background-color: #f0fff4; /* 淡绿色背景 */
  color: #38a169;            /* 深绿色字体 */
}

.role-badge.classify {
  background-color: #ebf8ff;
  color: #3182ce;
}

.management-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.management-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.management-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
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
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background-color: #e2e8f0;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #4361ee;
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
  padding: 3rem 0;
  color: #718096;
}

.empty-state svg {
  margin-bottom: 1rem;
  stroke: #cbd5e0;
}

.table-responsive {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.data-table th {
  font-weight: 600;
  color: #4a5568;
  background-color: #f7fafc;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.active {
  background-color: #f0fff4;
  color: #38a169;
}

.status-badge.inactive {
  background-color: #fffaf0;
  color: #dd6b20;
}

.status-badge.completed {
  background-color: #ebf8ff;
  color: #3182ce;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.375rem 0.75rem;
  border: none;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn.delete {
  background-color: #fff5f5;
  color: #e53e3e;
}

.action-btn.delete:hover {
  background-color: #fed7d7;
}
</style>
