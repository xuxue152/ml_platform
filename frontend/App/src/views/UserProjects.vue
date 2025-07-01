<template>
  <div class="projects-container">
    <div class="header-section">
      <h1>项目管理</h1>
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
          新建项目
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>加载项目中...</p>
    </div>

    <div v-else-if="projects.length === 0" class="empty-state">
      <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line>
        <line x1="16" y1="17" x2="8" y2="17"></line>
        <polyline points="10 9 9 9 8 9"></polyline>
      </svg>
      <h3>暂无项目</h3>
      <p>点击上方按钮创建您的第一个项目</p>
    </div>

    <div v-else class="projects-grid">
      <div v-for="project in projects" :key="project.name" class="project-card">
        <router-link :to="`/projects/${project.name}`" class="project-link" @click.native="() => setProjectId(project.project_id)">
          <div class="project-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
          </div>
          <h3 class="project-name">{{ project.name }}（id: {{ project.project_id }}）</h3>
          <h3 class="project-name">
            <span class="project-count">{{ project.project_count }} 个实验</span>
          </h3>
          <div class="project-meta">
            <span class="meta-item">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              创建于: {{ formatDate(project.created_at) }}
            </span>
          </div>
        </router-link>
        <button @click.stop="confirmDelete(project.project_id)" class="delete-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            <line x1="10" y1="11" x2="10" y2="17"></line>
            <line x1="14" y1="11" x2="14" y2="17"></line>
          </svg>
        </button>
      </div>
    </div>

    <!-- 创建项目对话框 -->
    <div v-if="showCreateDialog" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>创建新项目</h3>
          <button @click="showCreateDialog = false" class="close-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="input-group">
            <label for="project-name">项目名称</label>
            <input
              id="project-name"
              v-model="newProjectName"
              type="text"
              placeholder="输入项目名称"
              @keyup.enter="createProject"
            />
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCreateDialog = false" class="cancel-btn">取消</button>
          <button @click="createProject" class="confirm-btn" :disabled="!newProjectName">创建</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const projects = ref([])
const loading = ref(true)
const showCreateDialog = ref(false)
const newProjectName = ref('')
const userId = localStorage.getItem('user_id')

const refreshData = async () => {
  await fetchProjects()
}
const setProjectId = (id) => {
  localStorage.setItem('project_id', id)
}

// 获取所有项目
const fetchProjects = async () => {
  try {
    loading.value = true
    const userId = localStorage.getItem('user_id')
    const response = await axios.post('http://localhost:8000/api/projects',{user_id: userId})
    projects.value = response.data
  } catch (error) {
    console.error('获取项目列表失败:', error)
  } finally {
    loading.value = false
  }
}

const createProject = async () => {
  if (!newProjectName.value.trim()) return

  try {
    await axios.post('http://localhost:8000/api/create_project', {
      name: newProjectName.value.trim() ,user_id : userId
    })
    await fetchProjects()
    showCreateDialog.value = false
    newProjectName.value = ''
  } catch (error) {
    if (error.response && error.response.status === 400) {
    } else {
      console.error('创建项目失败:', error)
    }
  }
}

// 删除项目
const confirmDelete = (projectID) => {
  if (confirm(`确定要删除项目吗？此操作不可撤销。`)) {
    deleteProject(projectID)
  }
}

const deleteProject = async (projectID) => {
  try {
    await axios.delete('http://localhost:8000/api/delete_project', {
      data: { project_id: projectID }  // 注意这里要用 data 字段
    })
    await fetchProjects()
  } catch (error) {
    console.error('删除项目失败:', error)
  }
}

// 格式化日期
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

// 初始化加载数据
onMounted(fetchProjects)
</script>

<style scoped>
.projects-container {
  max-width: 1400px;  /* 增加最大宽度 */
  margin: 0 auto;
  padding: 2rem;
  width: 100%;  /* 确保容器使用全部可用宽度 */
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
  width: 100%;  /* 确保头部使用全部宽度 */
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
  width: 100%;
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
  width: 100%;
}

.empty-state h3 {
  font-size: 1.25rem;
  margin: 1rem 0 0.5rem;
  color: #2d3748;
}

.empty-state p {
  font-size: 0.95rem;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
  width: 100%;  /* 确保网格使用全部宽度 */
  justify-items: start;  /* 项目卡片从左对齐 */
}

.project-card {
  position: relative;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  transition: all 0.2s ease;
  width: 100%;  /* 确保卡片填充网格单元格 */
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.project-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.project-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
  color: #4361ee;
}

.project-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #2d3748;
  text-align: center;
}

.project-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #718096;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.delete-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fff5f5;
  border: none;
  border-radius: 50%;
  color: #e53e3e;
  cursor: pointer;
  transition: all 0.2s ease;
  opacity: 0;
}

.project-card:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  background-color: #fed7d7;
}

/* 模态框样式 */
.modal-overlay {
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
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
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

.modal-body {
  padding: 1.5rem;
}

.input-group {
  margin-bottom: 1rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #4a5568;
}

.input-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.input-group input:focus {
  outline: none;
  border-color: #4361ee;
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
}

.modal-footer {
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

/* 响应式调整 */
@media (max-width: 768px) {
  .projects-container {
    padding: 1.5rem;
  }

  .projects-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .projects-container {
    padding: 1rem;
  }

  .header-section {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>
