<template>
  <div class="management-container">
    <div class="management-header">
      <h2>用户管理</h2>
      <button @click="fetchUsers" class="refresh-btn">
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

      <div v-else-if="users.length === 0" class="empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
        <p>暂无用户数据</p>
      </div>

      <div v-else class="table-responsive">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>邮箱</th>
              <th>角色</th>
              <th>注册时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.user_id">
              <td>{{ user.user_id }}</td>
              <td>{{ user.email }}</td>
              <td>
                <span :class="['role-badge', { 'admin': user.role === 'admin' }]">
                  {{ user.role }}
                </span>
              </td>
              <td>{{ user.registered_at }}</td>
              <td class="actions">
                <button
                  v-if="user.role !== 'admin'"
                  @click="promoteUser(user.user_id)"
                  class="action-btn promote"
                >
                  设为管理员
                </button>
                <button
                  @click="deleteUser(user.user_id)"
                  class="action-btn delete"
                >
                  删除
                </button>
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

const users = ref([])
const loading = ref(true)

const fetchUsers = async () => {
  try {
    loading.value = true
    const response = await axios.get('http://localhost:8000/api/all_users')
    users.value = response.data
  } catch (error) {
    console.error('获取用户数据失败:', error)
  } finally {
    loading.value = false
  }
}

const deleteUser = async (userId) => {
  if (!confirm('确定要删除此用户吗？')) return

  try {
    await axios.delete('http://localhost:8000/api/manager_users', { data: { user_id: userId } })
    await fetchUsers()
  } catch (error) {
    console.error('删除用户失败:', error)
  }
}

const promoteUser = async (userId) => {
  if (!confirm('确定要将此用户提升为管理员吗？')) return

  try {
    await axios.post('http://localhost:8000/api/promote_user', { user_id: userId })
    await fetchUsers()
  } catch (error) {
    console.error('提升用户权限失败:', error)
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
/* 保持之前的样式不变 */
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

.role-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  background-color: #e2e8f0;
  color: #4a5568;
}

.role-badge.admin {
  background-color: #ebf8ff;
  color: #3182ce;
}

.actions {
  flex-direction: row;
  align-items: center;
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

.action-btn.promote {
  flex-direction: row;
  align-items: center;
  background-color: #ebf8ff;
  color: #3182ce;
}

.action-btn.promote:hover {
  background-color: #bee3f8;
}

.action-btn.delete {
  flex-direction: row;
  align-items: center;
  background-color: #fff5f5;
  color: #e53e3e;
}

.action-btn.delete:hover {
  background-color: #fed7d7;
}
</style>
