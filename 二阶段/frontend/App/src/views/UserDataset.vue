<template>
  <div class="management-container">
    <div class="management-header">
      <h2>个人数据集管理</h2>

      <!-- 上传按钮 -->
      <button @click="triggerFileSelect" class="refresh-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="23 4 23 10 17 10"></polyline>
          <polyline points="1 20 1 14 7 14"></polyline>
          <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
        </svg>
        上传数据集
        <input type="file" ref="fileInput" @change="handleFileChange" style="display: none" />
      </button>

      <!-- 刷新按钮 -->
      <button @click="fetchDatasets" class="refresh-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="23 4 23 10 17 10"></polyline>
          <polyline points="1 20 1 14 7 14"></polyline>
          <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
        </svg>
        刷新数据
      </button>
    </div>

    <!-- 加载中状态 -->
    <div class="card-container">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- 空状态 -->
      <div v-else-if="datasets.length === 0" class="empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19.21 15.98A7 7 0 0 0 8.14 6.23M6 10H2M6 6H2M6 14H2M6 18H2M18 4a2 2 0 0 0-2-2h-1a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2z"></path>
        </svg>
        <p>暂无数据集数据</p>
      </div>

      <!-- 表格内容 -->
      <div v-else class="table-responsive">
        <table class="data-table">
          <thead>
            <tr>
              <th>数据集名称</th>
              <th>上传时间</th>
              <th>保存路径</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="exp in datasets" :key="exp.name">
              <td>{{ exp.name }}</td>
              <td>{{ formatDate(exp.uploaded_at) }}</td>
              <td>{{ exp.file_path }}</td>
              <td class="actions">
                <router-link
                  :to="`/datasets/${exp.name}`"
                >
                  查看
                </router-link>
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
import { useRoute } from 'vue-router'

const route = useRoute()
const projectName = route.params.name
const datasets = ref([])
const loading = ref(true)
const fileInput = ref(null)

const userId = parseInt(localStorage.getItem('user_id'))  // 注意 key 的一致性

const triggerFileSelect = () => {
  fileInput.value.click()
}

const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const datasetName = file.name.split('.')[0]
  const formData = new FormData()
  formData.append('name', datasetName)
  formData.append('user_id', userId)
  formData.append('file', file)

  try {
    const response = await axios.post(
      `http://localhost:8000/api/projects/${projectName}/create_dataset`,
      formData
    )
    alert(response.data.message || '上传成功')
    fetchDatasets()
  } catch (err) {
    console.error(err.response?.data || err.message)
    alert('上传失败')
  }
}

const fetchDatasets = async () => {
  try {
    loading.value = true
    const response = await axios.post(`http://localhost:8000/api/projects/${projectName}/datasets`, {
      user_id: userId
    })
    datasets.value = response.data
  } catch (error) {
    console.error(error.response?.data || error.message)
    alert('获取数据集失败')
  } finally {
    loading.value = false
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleString()
}

onMounted(fetchDatasets)
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
