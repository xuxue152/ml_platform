<template>
  <div class="app-wrapper">
    <header class="topbar">
      <div class="logo">机器学习综合课程设计</div>
      <div class="user-email" :title="'查看个人信息'">
        <a href="#" @click.prevent="toggleUserPanel">{{ user.email || '加载中...' }}</a>
      </div>
    </header>

    <!-- 用户信息展示面板 -->
    <div v-if="showUserPanel" class="user-panel-overlay" @click.self="closePanels">
      <div class="user-panel">
        <h3>个人信息</h3>
        <div class="user-info">
          <div class="info-row">
            <span class="info-label">用户ID：</span>
            <span class="info-value">{{ user.user_id }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">邮箱：</span>
            <span class="info-value">{{ user.email }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">角色：</span>
            <span class="info-value role-badge">{{ formatRole(user.role) }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">注册时间：</span>
            <span class="info-value">{{ formatDate(user.registered_at) }}</span>
          </div>
        </div>
        <div class="panel-actions">
          <button @click="showUpdateModal = true">修改信息</button>
          <button @click="closePanels">关闭</button>
        </div>
      </div>
    </div>

    <router-view />

    <!-- 修改信息模态框 -->
    <div v-if="showUpdateModal" class="modal-overlay" @click.self="closePanels">
      <div class="modal">
        <h3>修改个人信息</h3>
        <form @submit.prevent="handleUpdate">
          <label for="new-email">新邮箱：</label>
          <input v-model="form.new_email" id="new-email" type="email" required />

          <label for="new-password">新密码：</label>
          <input v-model="form.new_password" id="new-password" type="password" required />

          <div class="modal-actions">
            <button type="submit">保存</button>
            <button type="button" @click="closePanels">取消</button>
          </div>
        </form>
        <p class="status-message" v-if="status">{{ status }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const user = ref({
  user_id: null,
  email: '',
  role: '',
  registered_at: null
})
const showUserPanel = ref(false)
const showUpdateModal = ref(false)
const form = ref({
  new_email: '',
  new_password: ''
})
const status = ref('')

onMounted(async () => {
  await fetchUserData()
})

const fetchUserData = async () => {
  try {
    const userId = localStorage.getItem('user_id')
    if (!userId) return
    const response = await axios.post('http://localhost:8000/api/user', {user_id: userId})
    user.value = response.data
    form.value.new_email = user.value.email
  } catch (err) {
    console.error('获取用户信息失败:', err)
  }
}

const toggleUserPanel = () => {
  showUserPanel.value = !showUserPanel.value
  showUpdateModal.value = false
}

const closePanels = () => {
  showUserPanel.value = false
  showUpdateModal.value = false
  status.value = ''
}

const formatRole = (role) => {
  const roles = {
    'user': '普通用户',
    'admin': '管理员'
  }
  return roles[role] || role
}

const formatDate = (dateString) => {
  if (!dateString) return '未知时间'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const handleUpdate = async () => {
  try {
    const userId = localStorage.getItem('user_id')
    const payload = {
      user_id: userId,
      new_email: form.value.new_email,
      new_password: form.value.new_password
    }

    const res = await axios.post('http://localhost:8000/api/update_user', payload)
    user.value.email = form.value.new_email
    localStorage.setItem('email', form.value.new_email)
    status.value = '更新成功'
    setTimeout(() => {
      showUpdateModal.value = false
      status.value = ''
    }, 1500)
  } catch (err) {
    status.value = '更新失败: ' + (err.response?.data?.detail || '未知错误')
  }
}
</script>

<style scoped>
.app-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  height: 100%;
  width: 100%;
  padding-top: 4em;
}

.topbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 4em;
  background-color: var(--card-bg);
  box-shadow: var(--box-shadow);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  z-index: 999;
}

.user-email a {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--primary-color);
  text-decoration: underline;
  cursor: pointer;
}

.logo {
  font-weight: 700;
  font-size: 1.4rem;
  color: var(--primary-color);
}

/* 用户信息面板样式 - 与模态框保持一致但位于左侧 */
.user-panel-overlay {
  position: fixed;
  top: 4em;
  left: 250px;
  background-color: rgba(0, 0, 0, 0.4);
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
}

.user-panel {
  font-weight: 800;
  font-size: 1.6rem;
  background-color: var(--card-bg);
  padding: 1.5rem;
  margin-top: 1rem;
  margin-left: 18rem;
  width: 400px;
  border-radius: 12px;
  color: white;
}

.user-panel h3 {
  margin-bottom: 1rem;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label {
  font-weight: 500;
}

.info-value {
  text-align: right;
}

.role-badge {
  padding: 0.15rem 0.5rem;
  border-radius: 1rem;
  font-weight: 500;
}

.panel-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

.panel-actions button{
  font-weight: 800; /* 加粗程度更高（从700提升到800或900） */
  font-size: 1.6rem; /* 字体稍微放大 */
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  background-color: var(--primary-color);
  color: white;
  cursor: pointer;
}

.modal-actions button {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  background-color: var(--primary-color);
  color: white;
  cursor: pointer;
}

/* 修改信息模态框样式 */
.modal-overlay {
  position: fixed;
  top: 4em;
  right: 1rem;
  background-color: rgba(0, 0, 0, 0.4);
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
}

.modal {
  background-color: var(--card-bg);
  padding: 1.5rem;
  margin-top: 1rem;
  width: 320px;
  border-radius: 12px;
  color: white;
}

.modal h3 {
  margin-bottom: 1rem;
}

.modal label {
  display: block;
  margin-top: 1rem;
  font-weight: 500;
}

.modal input {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.25rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.status-message {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: var(--success-color);
}
</style>
