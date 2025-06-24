<template>
  <div class="app-wrapper">
    <header class="topbar">
      <div class="logo">机器学习综合课程设计</div>
      <div class="user-email" :title="'修改个人信息'">
    {{ userEmail }}
  </div>
    </header>
    <router-view />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const userEmail = ref('')

onMounted(() => {
  // 从localStorage/sessionStorage中获取当前用户信息
  userEmail.value = localStorage.getItem('email') || '访客用户'
})
</script>

<style>
html,body,app{
  height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
}
.app-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  height: 100%;
  width: 100%;
  padding-top: 4em; /* 留出顶部高度 */
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

.logo {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--primary-color);
}

.user-email {
  font-size: 0.95rem;
  color: var(--text-color);
}
</style>
