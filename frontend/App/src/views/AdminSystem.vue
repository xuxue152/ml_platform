<template>
  <div class="admin-system">
    <!-- 左侧导航栏 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <h2>管理系统</h2>
      </div>
      <nav class="sidebar-nav">
        <router-link
          to="/admin/users"
          class="nav-item"
          :class="{ active: $route.path === '/admin/users' }"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          用户管理
        </router-link>
        <router-link
          to="/admin/projects"
          class="nav-item"
          :class="{ active: $route.path === '/admin/projects' }"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19.21 15.98A7 7 0 0 0 8.14 6.23M6 10H2M6 6H2M6 14H2M6 18H2M18 4a2 2 0 0 0-2-2h-1a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2z"></path>
          </svg>
          项目管理
        </router-link>
        <router-link
          to="/admin/models"
          class="nav-item"
          :class="{ active: $route.path === '/admin/models' }"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19.21 15.98A7 7 0 0 0 8.14 6.23M6 10H2M6 6H2M6 14H2M6 18H2M18 4a2 2 0 0 0-2-2h-1a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2z"></path>
          </svg>
          模型管理
        </router-link>
        <router-link
          to="/"
          class="nav-item logout"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          返回首页
        </router-link>
      </nav>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminSystem'
}
</script>

<style scoped>
.admin-system {
  display: flex;
  min-height: 200vh;
  margin: 0; /* 移除默认外边距 */
  padding: 0; /* 移除默认内边距 */
}

.sidebar {
  position: fixed;
  top: 4em;
  left: 0;
  height: 100vh; /* 撑满整个视口高度 */
  width: 250px;
  background-color: #2d3748;
  color: white;
  padding: 1.5rem 0;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.sidebar-header {
  padding: 0 1.5rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  color: white;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  padding: 1rem 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.2s ease;
  gap: 0.75rem;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: white;
}

.nav-item.active {
  background-color: #4361ee;
  color: white;
}

.nav-item svg {
  stroke: currentColor;
}

.logout {
  margin-top: auto;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 1rem;
}

.main-content {
  margin-left: 250px; /* 留出 sidebar 宽度 */
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}


</style>
