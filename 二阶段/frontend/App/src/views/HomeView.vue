<!--<script setup>-->
<!--import TheWelcome from '../components/TheWelcome.vue'-->
<!--</script>-->

<template>
  <div class="auth-container" role="main" aria-live="polite">
    <!-- 登录表单 -->
    <section
      v-if="!showRegisterForm"
      class="login-form form-card"
      aria-label="登录表单"
    >
      <header class="form-header">
        <h1>欢迎回来</h1>
        <p>请登录您的账户</p>
      </header>

      <form @submit.prevent="handleLogin" novalidate>
        <div
          class="input-group"
          :class="{ focused: focusedField === 'login-email' }"
        >
          <label for="login-email">邮箱</label>
          <input
            id="login-email"
            v-model.trim="loginData.email"
            type="email"
            required
            placeholder="请输入您的邮箱"
            @focus="focusedField = 'login-email'"
            @blur="focusedField = ''"
            autocomplete="email"
            aria-required="true"
            aria-describedby="login-email-desc"
          />
          <span class="input-icon" aria-hidden="true">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
              <polyline points="22,6 12,13 2,6" />
            </svg>
          </span>
          <span id="login-email-desc" class="visually-hidden">
            请输入有效的邮箱地址
          </span>
        </div>

        <div
          class="input-group"
          :class="{ focused: focusedField === 'login-password' }"
        >
          <label for="login-password">密码</label>
          <input
            id="login-password"
            v-model="loginData.password"
            type="password"
            required
            placeholder="请输入您的密码"
            @focus="focusedField = 'login-password'"
            @blur="focusedField = ''"
            autocomplete="current-password"
            aria-required="true"
          />
          <span class="input-icon" aria-hidden="true">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
          </span>
        </div>

        <div class="form-actions">
          <button
            type="submit"
            class="primary-btn"
            :aria-busy="loadingLogin.toString()"
            :disabled="loadingLogin"
          >
            {{ loadingLogin ? "登录中..." : "登录" }}
          </button>

          <p class="toggle-form-text">
            还没有账户?
            <span
              @click="toggleForm"
              role="button"
              tabindex="0"
              @keyup.enter="toggleForm"
              aria-label="切换到注册表单"
            >
              立即注册
            </span>
          </p>
        </div>
      </form>

      <transition name="fade" appear>
        <div
          v-if="loginMessage"
          :class="[
            'message',
            loginError ? 'error-message' : 'success-message',
            { flash: loginFlash },
          ]"
          role="alert"
          aria-live="assertive"
        >
          {{ loginMessage }}
        </div>
      </transition>
    </section>

    <!-- 注册表单 -->
    <section
      v-else
      class="register-form form-card"
      aria-label="注册表单"
    >
      <header class="form-header">
        <h1>创建账户</h1>
        <p>开始您的旅程</p>
      </header>

      <form @submit.prevent="handleRegister" novalidate>
        <div
          class="input-group"
          :class="{ focused: focusedField === 'register-email' }"
        >
          <label for="register-email">邮箱</label>
          <input
            id="register-email"
            v-model.trim="registerData.email"
            type="email"
            required
            placeholder="请输入您的邮箱"
            @focus="focusedField = 'register-email'"
            @blur="focusedField = ''"
            autocomplete="email"
            aria-required="true"
            aria-describedby="register-email-desc"
          />
          <span class="input-icon" aria-hidden="true">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
              <polyline points="22,6 12,13 2,6" />
            </svg>
          </span>
          <span id="register-email-desc" class="visually-hidden">
            请输入有效的邮箱地址
          </span>
        </div>

        <div
          class="input-group"
          :class="{ focused: focusedField === 'register-password' }"
        >
          <label for="register-password">密码</label>
          <input
            id="register-password"
            v-model="registerData.password"
            type="password"
            required
            placeholder="请设置您的密码"
            @focus="focusedField = 'register-password'"
            @blur="focusedField = ''"
            autocomplete="new-password"
            aria-required="true"
          />
          <span class="input-icon" aria-hidden="true">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
          </span>
        </div>

        <div class="form-actions">
          <button
            type="submit"
            class="primary-btn"
            :aria-busy="loadingRegister.toString()"
            :disabled="loadingRegister"
          >
            {{ loadingRegister ? "注册中..." : "注册" }}
          </button>

          <p class="toggle-form-text">
            已有账户?
            <span
              @click="toggleForm"
              role="button"
              tabindex="0"
              @keyup.enter="toggleForm"
              aria-label="切换到登录表单"
            >
              返回登录
            </span>
          </p>
        </div>
      </form>

      <transition name="fade" appear>
        <div
          v-if="registerMessage"
          class="message success-message"
          :class="{ flash: registerFlash }"
          role="alert"
          aria-live="assertive"
        >
          {{ registerMessage }}
        </div>
      </transition>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const loginData = ref({ email: "", password: "" });
const registerData = ref({ email: "", password: "" });
const showRegisterForm = ref(false);

const loginMessage = ref("");
const registerMessage = ref("");
const loginError = ref(false);
const loginFlash = ref(false);
const registerFlash = ref(false);
const focusedField = ref("");

const loadingLogin = ref(false);
const loadingRegister = ref(false);

const toggleForm = () => {
  showRegisterForm.value = !showRegisterForm.value;
  loginMessage.value = "";
  registerMessage.value = "";
  loginError.value = false;
  focusedField.value = "";
};

const triggerFlash = (type) => {
  if (type === "login") {
    loginFlash.value = true;
    setTimeout(() => (loginFlash.value = false), 1000);
  } else {
    registerFlash.value = true;
    setTimeout(() => (registerFlash.value = false), 1000);
  }
};

const handleLogin = async () => {
  if (loadingLogin.value) return;
  loadingLogin.value = true;
  try {
    const res = await axios.post("http://localhost:8000/api/login", loginData.value);
    const {user_id, role, email } = res.data;
    localStorage.setItem('user_id', user_id);
    localStorage.setItem('email', email);
    loginMessage.value = "登录成功！";
    loginError.value = false;
    triggerFlash("login");
    if (role == 'admin'){
      window.location.href = '/admin';}
    else {
      window.location.href = '/user';
    }
  } catch (err) {
    if (err.response?.status === 404) {
      loginMessage.value = "用户不存在，请注册新账户";
      loginError.value = true;
      triggerFlash("login");
      showRegisterForm.value = true;
      registerData.value.email = loginData.value.email;
    } else {
      loginMessage.value = err.response?.data?.detail || "登录失败";
      loginError.value = true;
      triggerFlash("login");
    }
  } finally {
    loadingLogin.value = false;
  }
};

const handleRegister = async () => {
  if (loadingRegister.value) return;
  loadingRegister.value = true;
  try {
    await axios.post("http://localhost:8000/api/register", registerData.value);
    registerMessage.value = "注册成功！请登录";
    triggerFlash("register");
    setTimeout(() => {
      showRegisterForm.value = false;
      loginData.value.email = registerData.value.email;
      registerMessage.value = "";
    }, 1500);
  } catch (err) {
    registerMessage.value = err.response?.data?.detail || "注册失败";
    triggerFlash("register");
  } finally {
    loadingRegister.value = false;
  }
};
</script>

<style scoped>
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
  --box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08),
    0 4px 6px rgba(0, 0, 0, 0.04);
  --transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1.25rem;
  background-color: var(--bg-color);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin: auto;
  top: 0;
	left: 0;
	right: 0;
	bottom: 0;
}

.form-card {
  background-color: var(--card-bg);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  padding: 2.75rem 2.5rem 3rem;
  width: 100%;
  max-width: 420px;
  transition: var(--transition);
  user-select: none;
}

.form-header {
  margin-bottom: 2.25rem;
  text-align: center;
  user-select: text;
}

.form-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 0.4rem;
}

.form-header p {
  color: var(--light-text);
  font-size: 1rem;
  letter-spacing: 0.02em;
}

.input-group {
  position: relative;
  margin-bottom: 1.8rem;
  transition: var(--transition);
}

.input-group input {
  width: 100%;
  padding: 0.9rem 1rem 0.9rem 2.75rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-size: 1rem;
  background-color: #fefefe;
  color: var(--text-color);
  transition: var(--transition);
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.04);
}

.input-group input::placeholder {
  color: var(--light-text);
  font-weight: 400;
  font-size: 0.95rem;
  letter-spacing: 0.01em;
}

.input-group input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 8px 3px rgba(67, 97, 238, 0.25);
  background-color: #fff;
}

.input-group.focused .input-icon {
  color: var(--primary-color);
  transform: scale(1.1);
  transition: color 0.3s ease, transform 0.3s ease;
}

.input-icon {
  position: absolute;
  left: 1rem;
  bottom: 0.9rem;
  color: var(--light-text);
  pointer-events: none;
  transition: color 0.3s ease;
}

.input-group label {
  display: block;
  margin-bottom: 0.65rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-color);
  user-select: none;
  letter-spacing: 0.01em;
}

/* 按钮 */
.primary-btn {
  width: 100%;
  padding: 1.05rem 0;
  background-color: var(--primary-color);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition);
  box-shadow: 0 6px 12px rgba(67, 97, 238, 0.4);
  user-select: none;
  will-change: transform;
}

.primary-btn:hover:not(:disabled),
.primary-btn:focus:not(:disabled) {
  background-color: var(--primary-hover);
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 14px rgba(67, 97, 238, 0.6);
  outline: none;
}

.primary-btn:disabled {
  background-color: #a1a9d7;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

/* 切换文字 */
.toggle-form-text {
  text-align: center;
  color: var(--light-text);
  font-size: 0.95rem;
  letter-spacing: 0.01em;
  user-select: none;
  margin-top: -0.5rem;
}

.toggle-form-text span {
  color: var(--primary-color);
  font-weight: 600;
  cursor: pointer;
  user-select: none;
  transition: color 0.3s ease;
}

.toggle-form-text span:hover,
.toggle-form-text span:focus {
  text-decoration: underline;
  outline: none;
}

/* 消息提示 */
.message {
  margin-top: 1.8rem;
  padding: 0.85rem 1rem;
  border-radius: 10px;
  font-size: 0.95rem;
  text-align: center;
  transition: var(--transition);
  user-select: none;
  letter-spacing: 0.01em;
}

.success-message {
  background-color: rgba(67, 170, 139, 0.12);
  color: var(--success-color);
  border: 1.5px solid rgba(67, 170, 139, 0.3);
}


.flash {
  animation: flash 0.5s 2;
}

@keyframes flash {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.08);
  }
}

/* 响应式调整 */
@media (max-width: 480px) {
  .form-card {
    padding: 2rem 1.75rem 2.5rem;
  }
  .form-header h1 {
    font-size: 1.75rem;
  }
  .input-group input {
    padding-left: 2.4rem;
    font-size: 0.95rem;
  }
}

@media (max-width: 360px) {
  .form-card {
    padding: 1.5rem 1.2rem 2rem;
  }
  .input-group input {
    font-size: 0.9rem;
    padding-left: 2.2rem;
  }
}

/* 无障碍辅助类 */
.visually-hidden {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: -1px !important;
  overflow: hidden !important;
  clip: rect(0 0 0 0) !important;
  white-space: nowrap !important;
  border: 0 !important;
}
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background-color: #f9fbff;
}

.form-card {
  width: 100%;
  max-width: 400px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 12px 24px rgba(0,0,0,0.12);
  padding: 3rem 2.5rem;
  box-sizing: border-box;
  text-align: center;
}

.form-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #1a2537;
  margin-bottom: 0.25rem;
}

.form-header p {
  font-size: 1rem;
  color: #6b7280;
  margin-bottom: 2rem;
}

.input-group {
  position: relative;
  margin-bottom: 1.8rem;
}

.input-group input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  font-size: 1rem;
  border: 1.5px solid #cbd5e1;
  border-radius: 12px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.input-group input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 6px rgba(79, 70, 229, 0.5);
  outline: none;
}

.input-icon {
  position: absolute;
  top: 50%;
  left: 1rem;
  transform: translateY(-50%);
  color: #94a3b8;
  font-size: 1.3rem;
  pointer-events: none;
  transition: color 0.3s ease;
}

.input-group input:focus + .input-icon {
  color: #4f46e5;
}

.primary-btn {
  width: 100%;
  padding: 1.1rem 0;
  background-color: #4f46e5;
  color: white;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1.1rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.15s ease;
}

.primary-btn:hover,
.primary-btn:focus {
  background-color: #4338ca;
  transform: translateY(-2px);
}

.toggle-form-text {
  margin-top: 1.2rem;
  font-size: 0.95rem;
  color: #6b7280;
}

.toggle-form-text span {
  color: #4f46e5;
  cursor: pointer;
  font-weight: 600;
  margin-left: 4px;
  transition: color 0.3s ease;
}

.toggle-form-text span:hover,
.toggle-form-text span:focus {
  color: #4338ca;
  text-decoration: underline;
}

/* 响应式 */
@media (max-width: 480px) {
  .form-card {
    padding: 2rem 1.5rem;
  }
  .form-header h1 {
    font-size: 1.6rem;
  }
  .input-group input {
    padding-left: 2.5rem;
    font-size: 0.95rem;
  }
  .primary-btn {
    padding: 0.9rem 0;
    font-size: 1rem;
  }
}

/*                       */
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background-color: #f9fbff;
}

.form-card {
  width: 100%;
  max-width: 400px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 12px 24px rgba(0,0,0,0.12);
  padding: 3rem 2.5rem;
  box-sizing: border-box;
  text-align: center;
}

.form-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #1a2537;
  margin-bottom: 0.25rem;
}

.form-header p {
  font-size: 1rem;
  color: #6b7280;
  margin-bottom: 2rem;
}

.input-group {
  position: relative;
  margin-bottom: 1.8rem;
}

.input-group input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  font-size: 1rem;
  border: 1.5px solid #cbd5e1;
  border-radius: 12px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.input-group input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 6px rgba(79, 70, 229, 0.5);
  outline: none;
}

.input-icon {
  position: absolute;
  top: 50%;
  left: 1rem;
  transform: translateY(-50%);
  color: #94a3b8;
  font-size: 1.3rem;
  pointer-events: none;
  transition: color 0.3s ease;
}

.input-group input:focus + .input-icon {
  color: #4f46e5;
}

.primary-btn {
  width: 100%;
  padding: 1.1rem 0;
  background-color: #4f46e5;
  color: white;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1.1rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.15s ease;
}

.primary-btn:hover,
.primary-btn:focus {
  background-color: #4338ca;
  transform: translateY(-2px);
}

.toggle-form-text {
  margin-top: 1.2rem;
  font-size: 0.95rem;
  color: #6b7280;
}

.toggle-form-text span {
  color: #4f46e5;
  cursor: pointer;
  font-weight: 600;
  margin-left: 4px;
  transition: color 0.3s ease;
}

.toggle-form-text span:hover,
.toggle-form-text span:focus {
  color: #4338ca;
  text-decoration: underline;
}

/* 响应式 */
@media (max-width: 480px) {
  .form-card {
    padding: 2rem 1.5rem;
  }
  .form-header h1 {
    font-size: 1.6rem;
  }
  .input-group input {
    padding-left: 2.5rem;
    font-size: 0.95rem;
  }
  .primary-btn {
    padding: 0.9rem 0;
    font-size: 1rem;
  }
}

</style>

