<template>
  <div class="auth-container">
    <!-- 登录表单 -->
    <div v-if="!showRegisterForm" class="login-form form-card">
      <div class="form-header">
        <h1>欢迎回来</h1>
        <p>请登录您的账户</p>
      </div>
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label for="login-email">邮箱</label>
          <input
            id="login-email"
            v-model="loginData.email"
            type="email"
            required
            placeholder="请输入您的邮箱"
          />
          <span class="input-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
              <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
          </span>
        </div>

        <div class="input-group">
          <label for="login-password">密码</label>
          <input
            id="login-password"
            v-model="loginData.password"
            type="password"
            required
            placeholder="请输入您的密码"
          />
          <span class="input-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </span>
        </div>

        <div class="form-actions">
          <button type="submit" class="primary-btn">
            登录
          </button>
          <p class="toggle-form-text">
            还没有账户? <span @click="showRegisterForm = true">立即注册</span>
          </p>
        </div>
      </form>

      <transition name="fade">
        <div v-if="loginMessage" :class="['message', {'error-message': loginError}, {'flash': loginFlash}]">
          {{ loginMessage }}
        </div>
      </transition>
    </div>

    <!-- 注册表单 -->
    <div v-else class="register-form form-card">
      <div class="form-header">
        <h1>创建账户</h1>
        <p>开始您的旅程</p>
      </div>
      <form @submit.prevent="handleRegister">
        <div class="input-group">
          <label for="register-email">邮箱</label>
          <input
            id="register-email"
            v-model="registerData.email"
            type="email"
            required
            placeholder="请输入您的邮箱"
          />
          <span class="input-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
              <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
          </span>
        </div>

        <div class="input-group">
          <label for="register-password">密码</label>
          <input
            id="register-password"
            v-model="registerData.password"
            type="password"
            required
            placeholder="请设置您的密码"
          />
          <span class="input-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </span>
        </div>

        <div class="form-actions">
          <button type="submit" class="primary-btn">
            注册
          </button>
          <p class="toggle-form-text">
            已有账户? <span @click="showRegisterForm = false">返回登录</span>
          </p>
        </div>
      </form>

      <transition name="fade">
        <div v-if="registerMessage" class="message" :class="{'flash': registerFlash}">
          {{ registerMessage }}
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
// 原有脚本部分保持不变
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

// 登录相关状态
const loginData = ref({
  email: '',
  password: ''
})
const loginMessage = ref('')
const loginError = ref(false)
const loginFlash = ref(false)

// 注册相关状态
const showRegisterForm = ref(false)
const registerData = ref({
  email: '',
  password: ''
})
const registerMessage = ref('')
const registerFlash = ref(false)

const triggerFlash = (type) => {
  if (type === 'login') {
    loginFlash.value = true
    setTimeout(() => {
      loginFlash.value = false
    }, 1000)
  } else {
    registerFlash.value = true
    setTimeout(() => {
      registerFlash.value = false
    }, 1000)
  }
}

const handleLogin = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/login', loginData.value)

    // 登录成功
    loginMessage.value = '登录成功！'
    loginError.value = false
    triggerFlash('login')

    // 存储用户信息或跳转
    // localStorage.setItem('user', JSON.stringify(response.data))
    // router.push('/dashboard')

  } catch (error) {
    if (error.response && error.response.status === 404) {
      // 用户不存在，显示注册表单
      loginMessage.value = '用户不存在，请注册新账户'
      loginError.value = true
      triggerFlash('login')
      showRegisterForm.value = true
      registerData.value.email = loginData.value.email
    } else {
      loginMessage.value = error.response?.data?.detail || '登录失败'
      loginError.value = true
      triggerFlash('login')
    }
  }
}

const handleRegister = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/register', registerData.value)
    registerMessage.value = '注册成功！请登录'
    triggerFlash('register')

    // 注册成功后自动切换回登录表单
    setTimeout(() => {
      showRegisterForm.value = false
      loginData.value.email = registerData.value.email
      registerMessage.value = ''
    }, 1500)

  } catch (error) {
    registerMessage.value = error.response?.data?.detail || '注册失败'
    triggerFlash('register')
  }
}
</script>

<style scoped>
/* 基础样式 */
:root {
  --primary-color: #4361ee;
  --primary-hover: #3a56d4;
  --error-color: #f94144;
  --success-color: #43aa8b;
  --text-color: #2b2d42;
  --light-text: #8d99ae;
  --bg-color: #f8f9fa;
  --card-bg: #ffffff;
  --border-radius: 12px;
  --box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --transition: all 0.3s ease;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: var(--bg-color);
  color: var(--text-color);
  line-height: 1.6;
}

/* 容器样式 */
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
  width: 100%;
}

.form-card {
  background-color: var(--card-bg);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  padding: 2.5rem;
  width: 100%;
  max-width: 420px;
  transition: var(--transition);
}

.form-header {
  margin-bottom: 2rem;
  text-align: center;
}

.form-header h1 {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-color);
}

.form-header p {
  color: var(--light-text);
  font-size: 0.95rem;
}

/* 输入框样式 */
.input-group {
  position: relative;
  margin-bottom: 1.5rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-color);
}

.input-group input {
  width: 100%;
  padding: 0.8rem 1rem 0.8rem 2.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: var(--transition);
  background-color: #f8fafc;
}

.input-group input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
}

.input-icon {
  position: absolute;
  left: 1rem;
  bottom: 0.8rem;
  color: var(--light-text);
}

/* 按钮样式 */
.form-actions {
  margin-top: 2rem;
}

.primary-btn {
  width: 100%;
  padding: 0.9rem;
  background-color: var(--primary-color);
  color: black;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
  margin-bottom: 1.5rem;
}

.primary-btn:hover {
  background-color: var(--primary-hover);
  transform: translateY(-1px);
}

/* 切换表单文本 */
.toggle-form-text {
  text-align: center;
  color: var(--light-text);
  font-size: 0.9rem;
}

.toggle-form-text span {
  color: var(--primary-color);
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
}

.toggle-form-text span:hover {
  text-decoration: underline;
}

/* 消息提示 */
.message {
  margin-top: 1.5rem;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  text-align: center;
  transition: var(--transition);
}

.error-message {
  background-color: rgba(249, 65, 68, 0.1);
  color: var(--error-color);
  border: 1px solid rgba(249, 65, 68, 0.2);
}

.flash {
  animation: flash 0.5s 2;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes flash {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.05);
  }
}

/* 响应式设计 */
@media (max-width: 480px) {
  .form-card {
    padding: 1.5rem;
  }

  .form-header h1 {
    font-size: 1.5rem;
  }
}
</style>
