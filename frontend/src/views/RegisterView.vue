<template>
  <div class="auth-page">
    <!-- 左侧插图区（与登录页对称） -->
    <div class="panel-left">
      <div class="brand-mark">
        <div class="brand-icon">
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <rect width="28" height="28" rx="7" fill="rgba(255,255,255,0.2)"/>
            <path d="M14 5L7 9.5V18.5L14 23L21 18.5V9.5L14 5Z" stroke="white" stroke-width="1.5" stroke-linejoin="round"/>
            <path d="M14 5V23M7 9.5L21 18.5M21 9.5L7 18.5" stroke="white" stroke-width="1" stroke-opacity="0.5"/>
          </svg>
        </div>
        <span class="brand-name">EduAssistant</span>
      </div>

      <!-- 注册页插图（主题：出发/新旅程） -->
      <div class="illustration-wrap">
        <svg viewBox="0 0 420 380" fill="none" xmlns="http://www.w3.org/2000/svg" class="main-svg">
          <!-- 背景装饰圆 -->
          <circle cx="210" cy="190" r="150" fill="white" fill-opacity="0.04"/>
          <circle cx="210" cy="190" r="110" fill="white" fill-opacity="0.04"/>

          <!-- 大型开放书本（注册/新开始主题） -->
          <g class="float-mid">
            <!-- 书本左页 -->
            <path d="M100 100 L210 140 L210 300 L100 260 Z" fill="rgba(255,255,255,0.1)" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
            <!-- 书本右页 -->
            <path d="M320 100 L210 140 L210 300 L320 260 Z" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.25)" stroke-width="1.5"/>
            <!-- 书脊 -->
            <line x1="210" y1="140" x2="210" y2="300" stroke="rgba(255,255,255,0.4)" stroke-width="2.5"/>
            <!-- 左页线条（文字感） -->
            <line x1="122" y1="168" x2="198" y2="188" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
            <line x1="122" y1="181" x2="196" y2="199" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <line x1="124" y1="194" x2="195" y2="211" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <line x1="126" y1="207" x2="195" y2="222" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <line x1="128" y1="220" x2="196" y2="234" stroke="rgba(255,255,255,0.1)" stroke-width="1.5"/>
            <!-- 右页线条 -->
            <line x1="222" y1="188" x2="298" y2="168" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
            <line x1="224" y1="199" x2="298" y2="181" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <line x1="225" y1="211" x2="296" y2="194" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <line x1="225" y1="222" x2="294" y2="207" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
            <line x1="224" y1="234" x2="292" y2="220" stroke="rgba(255,255,255,0.1)" stroke-width="1.5"/>
          </g>

          <!-- 笔（寓意注册/书写） -->
          <g class="pencil-float">
            <rect x="256" y="48" width="14" height="88" rx="3" fill="rgba(240,180,40,0.5)" stroke="rgba(240,180,40,0.7)" stroke-width="1.5" transform="rotate(28 256 48)"/>
            <!-- 笔尖 -->
            <polygon points="285,94 278,108 292,108" fill="rgba(240,180,40,0.8)" transform="rotate(28 285 94)"/>
            <!-- 笔擦 -->
            <rect x="256" y="48" width="14" height="12" rx="2" fill="rgba(255,150,150,0.5)" transform="rotate(28 256 48)"/>
          </g>

          <!-- 星星气泡（装饰） -->
          <g class="float-slow">
            <circle cx="68" cy="120" r="22" fill="rgba(255,255,255,0.07)" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
            <path d="M68 110 L70 104 L72 110 L78 112 L72 114 L70 120 L68 114 L62 112 Z" fill="rgba(255,255,255,0.5)"/>
          </g>

          <g class="float-fast">
            <circle cx="352" cy="256" r="18" fill="rgba(240,180,40,0.1)" stroke="rgba(240,180,40,0.35)" stroke-width="1.5"/>
            <path d="M352 248 L354 243 L356 248 L361 250 L356 252 L354 257 L352 252 L347 250 Z" fill="rgba(240,180,40,0.65)"/>
          </g>

          <!-- 小飘浮书本 -->
          <g class="float-slow" style="animation-delay: 1s">
            <rect x="46" y="230" width="66" height="84" rx="5" fill="rgba(96,165,250,0.15)" stroke="rgba(96,165,250,0.35)" stroke-width="1.5"/>
            <rect x="46" y="230" width="8" height="84" rx="4" fill="rgba(96,165,250,0.25)"/>
            <rect x="60" y="248" width="40" height="3.5" rx="1.75" fill="rgba(255,255,255,0.3)"/>
            <rect x="60" y="259" width="32" height="2.5" rx="1.25" fill="rgba(255,255,255,0.2)"/>
            <rect x="60" y="267" width="36" height="2.5" rx="1.25" fill="rgba(255,255,255,0.2)"/>
          </g>

          <g class="float-mid" style="animation-delay: 0.6s">
            <rect x="308" y="154" width="58" height="74" rx="5" fill="rgba(167,139,250,0.15)" stroke="rgba(167,139,250,0.35)" stroke-width="1.5"/>
            <rect x="308" y="154" width="8" height="74" rx="4" fill="rgba(167,139,250,0.25)"/>
            <rect x="322" y="170" width="36" height="3.5" rx="1.75" fill="rgba(255,255,255,0.3)"/>
            <rect x="322" y="181" width="28" height="2.5" rx="1.25" fill="rgba(255,255,255,0.2)"/>
          </g>

          <!-- 星星散布 -->
          <g class="stars-twinkle">
            <path d="M44 62 L46 56 L48 62 L54 64 L48 66 L46 72 L44 66 L38 64 Z" fill="rgba(240,180,40,0.6)"/>
            <path d="M360 100 L362 94 L364 100 L370 102 L364 104 L362 110 L360 104 L354 102 Z" fill="rgba(255,255,255,0.45)"/>
            <path d="M372 300 L374 294 L376 300 L382 302 L376 304 L374 310 L372 304 L366 302 Z" fill="rgba(96,165,250,0.5)"/>
            <path d="M38 320 L40 314 L42 320 L48 322 L42 324 L40 330 L38 324 L32 322 Z" fill="rgba(167,139,250,0.55)"/>
            <circle cx="100" cy="52" r="4" fill="rgba(255,255,255,0.45)"/>
            <circle cx="362" cy="196" r="4.5" fill="rgba(240,180,40,0.5)"/>
            <circle cx="76" cy="290" r="3.5" fill="rgba(96,165,250,0.5)"/>
            <circle cx="330" cy="336" r="3" fill="rgba(255,255,255,0.4)"/>
            <circle cx="118" cy="156" r="2.5" fill="rgba(255,255,255,0.4)"/>
            <circle cx="302" cy="82" r="2.5" fill="rgba(240,180,40,0.5)"/>
          </g>
        </svg>
      </div>

      <div class="left-tagline">
        <h2>加入学习社区</h2>
        <p>注册账号，开启专属 AI 学习体验</p>
      </div>

      <div class="left-footer">© 2025 EduAssistant · 智能教育助手</div>
    </div>

    <!-- 右侧注册表单 -->
    <div class="panel-right">
      <div class="form-box">
        <div class="form-header">
          <h1 class="form-title">创建账号</h1>
          <p class="form-subtitle">填写信息，开启你的学习旅程</p>
        </div>

        <div class="field-group">
          <label class="field-label">用户名</label>
          <div class="field-wrap" :class="{ error: errors.username, focused: focus.username }">
            <svg class="field-icon" width="17" height="17" viewBox="0 0 17 17" fill="none">
              <circle cx="8.5" cy="5.5" r="3" stroke="currentColor" stroke-width="1.4"/>
              <path d="M1.5 15.5c0-3.038 3.134-5.5 7-5.5s7 2.462 7 5.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
            </svg>
            <input
              v-model="form.username"
              type="text"
              placeholder="请输入用户名"
              autocomplete="username"
              @focus="focus.username = true"
              @blur="focus.username = false; validateField('username')"
              @keyup.enter="handleRegister"
            />
          </div>
          <span v-if="errors.username" class="error-text">{{ errors.username }}</span>
        </div>

        <div class="field-group">
          <label class="field-label">密码</label>
          <div class="field-wrap" :class="{ error: errors.password, focused: focus.password }">
            <svg class="field-icon" width="17" height="17" viewBox="0 0 17 17" fill="none">
              <rect x="2.5" y="7.5" width="12" height="8" rx="2" stroke="currentColor" stroke-width="1.4"/>
              <path d="M5.5 7.5V5a3 3 0 016 0v2.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
            </svg>
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="请输入密码"
              autocomplete="new-password"
              @focus="focus.password = true"
              @blur="focus.password = false; validateField('password')"
              @keyup.enter="handleRegister"
            />
            <button class="eye-btn" type="button" @click="showPassword = !showPassword" tabindex="-1">
              <svg v-if="!showPassword" width="17" height="17" viewBox="0 0 17 17" fill="none">
                <path d="M1 8.5C2.8 5.1 5.4 3 8.5 3S14.2 5.1 16 8.5c-1.8 3.4-4.4 5.5-7.5 5.5S2.8 11.9 1 8.5Z" stroke="currentColor" stroke-width="1.4"/>
                <circle cx="8.5" cy="8.5" r="2.25" stroke="currentColor" stroke-width="1.4"/>
              </svg>
              <svg v-else width="17" height="17" viewBox="0 0 17 17" fill="none">
                <path d="M1 1l15 15M6.5 6.6A2.25 2.25 0 0010.4 10.5M3.5 4.2C2.2 5.5 1.4 6.9 1 8.5c1.8 3.4 4.4 5.5 7.5 5.5 1.4 0 2.7-.4 3.8-1.1M7.5 3.1C7.8 3 8.1 3 8.5 3c3.1 0 5.7 2.1 7.5 5.5-.4.7-.8 1.4-1.4 2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <span v-if="errors.password" class="error-text">{{ errors.password }}</span>
        </div>

        <div class="field-group">
          <label class="field-label">确认密码</label>
          <div class="field-wrap" :class="{ error: errors.confirmPassword, focused: focus.confirmPassword }">
            <svg class="field-icon" width="17" height="17" viewBox="0 0 17 17" fill="none">
              <path d="M2.5 9.5L6.5 13.5L14.5 4.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <input
              v-model="form.confirmPassword"
              :type="showConfirm ? 'text' : 'password'"
              placeholder="请再次输入密码"
              autocomplete="new-password"
              @focus="focus.confirmPassword = true"
              @blur="focus.confirmPassword = false; validateField('confirmPassword')"
              @keyup.enter="handleRegister"
            />
            <button class="eye-btn" type="button" @click="showConfirm = !showConfirm" tabindex="-1">
              <svg v-if="!showConfirm" width="17" height="17" viewBox="0 0 17 17" fill="none">
                <path d="M1 8.5C2.8 5.1 5.4 3 8.5 3S14.2 5.1 16 8.5c-1.8 3.4-4.4 5.5-7.5 5.5S2.8 11.9 1 8.5Z" stroke="currentColor" stroke-width="1.4"/>
                <circle cx="8.5" cy="8.5" r="2.25" stroke="currentColor" stroke-width="1.4"/>
              </svg>
              <svg v-else width="17" height="17" viewBox="0 0 17 17" fill="none">
                <path d="M1 1l15 15M6.5 6.6A2.25 2.25 0 0010.4 10.5M3.5 4.2C2.2 5.5 1.4 6.9 1 8.5c1.8 3.4 4.4 5.5 7.5 5.5 1.4 0 2.7-.4 3.8-1.1M7.5 3.1C7.8 3 8.1 3 8.5 3c3.1 0 5.7 2.1 7.5 5.5-.4.7-.8 1.4-1.4 2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <span v-if="errors.confirmPassword" class="error-text">{{ errors.confirmPassword }}</span>
        </div>

        <button class="submit-btn" :disabled="loading" @click="handleRegister">
          <span v-if="!loading" class="btn-text">注 册</span>
          <span v-else class="btn-loader">
            <span></span><span></span><span></span>
          </span>
        </button>

        <p class="switch-link">
          已有账号？
          <router-link to="/login">去登录 →</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()
const loading = ref(false)
const showPassword = ref(false)
const showConfirm = ref(false)

const form = reactive({ username: '', password: '', confirmPassword: '' })
const errors = reactive({ username: '', password: '', confirmPassword: '' })
const focus = reactive({ username: false, password: false, confirmPassword: false })

function validateField(field: keyof typeof form) {
  if (field === 'username') {
    errors.username = form.username.trim() ? '' : '请输入用户名'
  } else if (field === 'password') {
    errors.password = form.password ? '' : '请输入密码'
  } else if (field === 'confirmPassword') {
    if (!form.confirmPassword) {
      errors.confirmPassword = '请再次输入密码'
    } else if (form.confirmPassword !== form.password) {
      errors.confirmPassword = '两次输入的密码不一致'
    } else {
      errors.confirmPassword = ''
    }
  }
}

async function handleRegister() {
  validateField('username')
  validateField('password')
  validateField('confirmPassword')
  if (errors.username || errors.password || errors.confirmPassword) return
  if (form.password !== form.confirmPassword) {
    errors.confirmPassword = '两次输入的密码不一致'
    return
  }

  loading.value = true
  try {
    await authStore.register(form.username, form.password)
    message.success('注册成功，欢迎加入！')
    router.push('/')
  } catch (e: any) {
    message.error(e.response?.data?.detail || '注册失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ===== 根容器 ===== */
.auth-page {
  display: flex;
  min-height: 100vh;
  font-family: 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif;
}

/* ===== 左侧面板 ===== */
.panel-left {
  flex: 0 0 56%;
  background: linear-gradient(145deg, #0b3d2e 0%, #0f5c44 40%, #1a7a5e 75%, #0d4d38 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 36px 40px 32px;
  position: relative;
  overflow: hidden;
}

.panel-left::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(circle at 20% 20%, rgba(255,255,255,0.04) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(240,180,40,0.06) 0%, transparent 50%);
  pointer-events: none;
}

.brand-mark {
  display: flex;
  align-items: center;
  gap: 10px;
  align-self: flex-start;
  position: relative;
  z-index: 1;
}

.brand-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-name {
  color: white;
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 0.02em;
  opacity: 0.95;
}

.illustration-wrap {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 460px;
  position: relative;
  z-index: 1;
}

.main-svg {
  width: 100%;
  height: auto;
  max-height: 360px;
  filter: drop-shadow(0 20px 60px rgba(0,0,0,0.25));
}

.left-tagline {
  text-align: center;
  color: white;
  position: relative;
  z-index: 1;
}

.left-tagline h2 {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 8px;
  opacity: 0.95;
  letter-spacing: 0.02em;
}

.left-tagline p {
  font-size: 14px;
  opacity: 0.65;
  line-height: 1.6;
}

.left-footer {
  color: rgba(255,255,255,0.35);
  font-size: 12px;
  position: relative;
  z-index: 1;
}

/* ===== 右侧面板 ===== */
.panel-right {
  flex: 0 0 44%;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 40px;
}

.form-box {
  width: 100%;
  max-width: 360px;
}

.form-header {
  margin-bottom: 32px;
}

.form-title {
  font-size: 30px;
  font-weight: 800;
  color: #0b3d2e;
  line-height: 1.2;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}

.form-subtitle {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
}

/* ===== 表单字段 ===== */
.field-group {
  margin-bottom: 18px;
}

.field-label {
  display: block;
  font-size: 13.5px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 7px;
  letter-spacing: 0.01em;
}

.field-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  padding: 0 14px;
  height: 46px;
  background: #fafafa;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
}

.field-wrap.focused {
  border-color: #0f5c44;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(15, 92, 68, 0.08);
}

.field-wrap.error {
  border-color: #ef4444;
  background: #fff8f8;
}

.field-icon {
  color: #9ca3af;
  flex-shrink: 0;
  transition: color 0.2s;
}

.field-wrap.focused .field-icon {
  color: #0f5c44;
}

.field-wrap input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 14px;
  color: #111827;
  line-height: 1;
}

.field-wrap input::placeholder {
  color: #d1d5db;
}

.eye-btn {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  color: #9ca3af;
  transition: color 0.2s;
  flex-shrink: 0;
}

.eye-btn:hover {
  color: #6b7280;
}

.error-text {
  display: block;
  font-size: 12px;
  color: #ef4444;
  margin-top: 5px;
  padding-left: 2px;
}

/* ===== 注册按钮 ===== */
.submit-btn {
  width: 100%;
  height: 48px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, #0b3d2e 0%, #0f5c44 100%);
  color: white;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.15em;
  cursor: pointer;
  margin-top: 24px;
  margin-bottom: 20px;
  transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 4px 20px rgba(11, 61, 46, 0.28);
  display: flex;
  align-items: center;
  justify-content: center;
}

.submit-btn:hover:not(:disabled) {
  opacity: 0.92;
  transform: translateY(-1px);
  box-shadow: 0 6px 28px rgba(11, 61, 46, 0.35);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-text {
  letter-spacing: 0.2em;
}

.btn-loader {
  display: flex;
  align-items: center;
  gap: 5px;
}

.btn-loader span {
  display: block;
  width: 7px;
  height: 7px;
  background: white;
  border-radius: 50%;
  animation: bounce 0.6s infinite alternate;
}

.btn-loader span:nth-child(2) { animation-delay: 0.15s; }
.btn-loader span:nth-child(3) { animation-delay: 0.3s; }

@keyframes bounce {
  from { transform: translateY(0); opacity: 1; }
  to { transform: translateY(-6px); opacity: 0.5; }
}

.switch-link {
  text-align: center;
  font-size: 13.5px;
  color: #9ca3af;
}

.switch-link a {
  color: #0f5c44;
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.2s;
}

.switch-link a:hover {
  opacity: 0.75;
}

/* ===== 插图动画 ===== */
.float-slow {
  animation: floatSlow 5s ease-in-out infinite;
}

.float-mid {
  animation: floatMid 4s ease-in-out infinite 0.8s;
}

.float-fast {
  animation: floatFast 3.5s ease-in-out infinite 0.4s;
}

.pencil-float {
  animation: pencilDrift 5.5s ease-in-out infinite 0.3s;
  transform-origin: center;
}

.stars-twinkle > * {
  animation: twinkle 3s ease-in-out infinite;
}

.stars-twinkle > *:nth-child(2) { animation-delay: 0.5s; }
.stars-twinkle > *:nth-child(3) { animation-delay: 1s; }
.stars-twinkle > *:nth-child(4) { animation-delay: 1.5s; }
.stars-twinkle > *:nth-child(5) { animation-delay: 0.3s; }
.stars-twinkle > *:nth-child(6) { animation-delay: 0.9s; }
.stars-twinkle > *:nth-child(7) { animation-delay: 1.7s; }
.stars-twinkle > *:nth-child(8) { animation-delay: 2s; }
.stars-twinkle > *:nth-child(9) { animation-delay: 0.6s; }
.stars-twinkle > *:nth-child(10) { animation-delay: 1.2s; }

@keyframes floatSlow {
  0%, 100% { transform: translateY(0) rotate(-1deg); }
  50% { transform: translateY(-12px) rotate(1deg); }
}

@keyframes floatMid {
  0%, 100% { transform: translateY(0) rotate(1deg); }
  50% { transform: translateY(-16px) rotate(-1deg); }
}

@keyframes floatFast {
  0%, 100% { transform: translateY(0) rotate(-2deg); }
  50% { transform: translateY(-10px) rotate(1deg); }
}

@keyframes pencilDrift {
  0%, 100% { transform: translateY(0) translateX(0); }
  33% { transform: translateY(-14px) translateX(6px); }
  66% { transform: translateY(-8px) translateX(-4px); }
}

@keyframes twinkle {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.3; transform: scale(0.7); }
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .auth-page { flex-direction: column; }
  .panel-left {
    flex: 0 0 auto;
    padding: 28px 24px;
    min-height: 240px;
  }
  .illustration-wrap { max-height: 160px; }
  .left-tagline { display: none; }
  .panel-right {
    flex: 1;
    padding: 36px 24px;
  }
}
</style>
