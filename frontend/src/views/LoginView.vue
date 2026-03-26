<template>
  <div class="auth-page">
    <!-- 左侧插图区 -->
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

      <!-- 主插图 SVG -->
      <div class="illustration-wrap">
        <svg viewBox="0 0 420 380" fill="none" xmlns="http://www.w3.org/2000/svg" class="main-svg">
          <!-- 背景装饰圆 -->
          <circle cx="210" cy="190" r="150" fill="white" fill-opacity="0.04"/>
          <circle cx="210" cy="190" r="110" fill="white" fill-opacity="0.04"/>

          <!-- 浮动书本 1（左下） -->
          <g class="float-slow">
            <rect x="48" y="220" width="88" height="115" rx="6" fill="rgba(255,255,255,0.1)" stroke="rgba(255,255,255,0.25)" stroke-width="1.5"/>
            <rect x="48" y="220" width="10" height="115" rx="5" fill="rgba(255,255,255,0.18)"/>
            <rect x="66" y="238" width="56" height="4" rx="2" fill="rgba(255,255,255,0.35)"/>
            <rect x="66" y="250" width="44" height="2.5" rx="1.25" fill="rgba(255,255,255,0.22)"/>
            <rect x="66" y="259" width="50" height="2.5" rx="1.25" fill="rgba(255,255,255,0.22)"/>
            <rect x="66" y="268" width="40" height="2.5" rx="1.25" fill="rgba(255,255,255,0.22)"/>
            <rect x="66" y="277" width="46" height="2.5" rx="1.25" fill="rgba(255,255,255,0.22)"/>
          </g>

          <!-- 浮动书本 2（右上） -->
          <g class="float-mid">
            <rect x="282" y="52" width="80" height="105" rx="6" fill="rgba(240,180,40,0.18)" stroke="rgba(240,180,40,0.4)" stroke-width="1.5"/>
            <rect x="282" y="52" width="10" height="105" rx="5" fill="rgba(240,180,40,0.3)"/>
            <rect x="300" y="70" width="48" height="4" rx="2" fill="rgba(255,255,255,0.4)"/>
            <rect x="300" y="82" width="38" height="2.5" rx="1.25" fill="rgba(255,255,255,0.25)"/>
            <rect x="300" y="91" width="44" height="2.5" rx="1.25" fill="rgba(255,255,255,0.25)"/>
            <rect x="300" y="100" width="34" height="2.5" rx="1.25" fill="rgba(255,255,255,0.25)"/>
          </g>

          <!-- 浮动书本 3（右下小） -->
          <g class="float-fast">
            <rect x="314" y="268" width="66" height="82" rx="5" fill="rgba(96,165,250,0.18)" stroke="rgba(96,165,250,0.4)" stroke-width="1.5"/>
            <rect x="314" y="268" width="8" height="82" rx="4" fill="rgba(96,165,250,0.28)"/>
            <rect x="328" y="282" width="38" height="3.5" rx="1.75" fill="rgba(255,255,255,0.35)"/>
            <rect x="328" y="292" width="30" height="2" rx="1" fill="rgba(255,255,255,0.2)"/>
            <rect x="328" y="299" width="34" height="2" rx="1" fill="rgba(255,255,255,0.2)"/>
          </g>

          <!-- 猫头鹰主体 -->
          <g class="owl-bounce">
            <!-- 书堆 -->
            <rect x="136" y="272" width="148" height="18" rx="4" fill="rgba(96,165,250,0.35)"/>
            <rect x="144" y="256" width="132" height="18" rx="4" fill="rgba(129,140,248,0.35)"/>
            <rect x="152" y="240" width="116" height="18" rx="4" fill="rgba(167,139,250,0.35)"/>

            <!-- 身体 -->
            <ellipse cx="210" cy="202" rx="42" ry="50" fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.4)" stroke-width="2"/>
            <!-- 腹部浅色 -->
            <ellipse cx="210" cy="214" rx="26" ry="30" fill="rgba(255,255,255,0.1)"/>

            <!-- 耳羽（角） -->
            <polygon points="192,156 183,138 200,154" fill="rgba(255,255,255,0.28)"/>
            <polygon points="228,156 237,138 220,154" fill="rgba(255,255,255,0.28)"/>

            <!-- 翅膀 -->
            <ellipse cx="172" cy="216" rx="20" ry="32" fill="rgba(255,255,255,0.12)" stroke="rgba(255,255,255,0.2)" stroke-width="1" transform="rotate(-12 172 216)"/>
            <ellipse cx="248" cy="216" rx="20" ry="32" fill="rgba(255,255,255,0.12)" stroke="rgba(255,255,255,0.2)" stroke-width="1" transform="rotate(12 248 216)"/>

            <!-- 眼眶 -->
            <circle cx="197" cy="191" r="14" fill="rgba(255,255,255,0.22)" stroke="rgba(255,255,255,0.4)" stroke-width="1.5"/>
            <circle cx="223" cy="191" r="14" fill="rgba(255,255,255,0.22)" stroke="rgba(255,255,255,0.4)" stroke-width="1.5"/>
            <!-- 眼球 -->
            <circle cx="197" cy="191" r="9" fill="rgba(255,255,255,0.35)"/>
            <circle cx="223" cy="191" r="9" fill="rgba(255,255,255,0.35)"/>
            <!-- 瞳孔 -->
            <circle cx="197" cy="191" r="5.5" fill="#0b3d2e"/>
            <circle cx="223" cy="191" r="5.5" fill="#0b3d2e"/>
            <!-- 高光 -->
            <circle cx="199" cy="189" r="2" fill="white"/>
            <circle cx="225" cy="189" r="2" fill="white"/>

            <!-- 喙 -->
            <polygon points="210,200 204,210 216,210" fill="rgba(240,180,40,0.85)"/>

            <!-- 学士帽 -->
            <rect x="186" y="149" width="48" height="10" rx="2.5" fill="rgba(255,255,255,0.6)"/>
            <polygon points="210,130 185,149 235,149" fill="rgba(255,255,255,0.48)"/>
            <!-- 流苏 -->
            <line x1="236" y1="149" x2="238" y2="167" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"/>
            <circle cx="238" cy="170" r="5" fill="rgba(240,180,40,0.8)"/>
          </g>

          <!-- 星星装饰 -->
          <g class="stars-twinkle">
            <!-- 4角星 -->
            <path d="M46 94 L48 88 L50 94 L56 96 L50 98 L48 104 L46 98 L40 96 Z" fill="rgba(240,180,40,0.6)"/>
            <path d="M356 166 L358 160 L360 166 L366 168 L360 170 L358 176 L356 170 L350 168 Z" fill="rgba(255,255,255,0.5)"/>
            <path d="M148 40 L150 34 L152 40 L158 42 L152 44 L150 50 L148 44 L142 42 Z" fill="rgba(255,255,255,0.4)"/>
            <path d="M294 320 L296 314 L298 320 L304 322 L298 324 L296 330 L294 324 L288 322 Z" fill="rgba(96,165,250,0.55)"/>
            <!-- 圆点 -->
            <circle cx="56" cy="168" r="4.5" fill="rgba(240,180,40,0.55)"/>
            <circle cx="366" cy="280" r="5" fill="rgba(240,180,40,0.5)"/>
            <circle cx="84" cy="330" r="3.5" fill="rgba(167,139,250,0.6)"/>
            <circle cx="380" cy="72" r="3" fill="rgba(255,255,255,0.5)"/>
            <circle cx="116" cy="58" r="3" fill="rgba(96,165,250,0.5)"/>
            <!-- 小亮点 -->
            <circle cx="110" cy="160" r="2.5" fill="rgba(255,255,255,0.45)"/>
            <circle cx="308" cy="196" r="2.5" fill="rgba(255,255,255,0.45)"/>
            <circle cx="290" cy="136" r="2" fill="rgba(240,180,40,0.5)"/>
            <circle cx="128" cy="290" r="2" fill="rgba(96,165,250,0.5)"/>
          </g>
        </svg>
      </div>

      <div class="left-tagline">
        <h2>开启智慧学习之旅</h2>
        <p>AI 驱动的个性化教育助手，陪伴每一步成长</p>
      </div>

      <div class="left-footer">© 2026 EduAssistant · 智能教育助手</div>
    </div>

    <!-- 右侧表单区 -->
    <div class="panel-right">
      <div class="form-box">
        <div class="form-header">
          <h1 class="form-title">欢迎回来！</h1>
          <p class="form-subtitle">请登录您的账号继续学习</p>
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
              @keyup.enter="handleLogin"
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
              autocomplete="current-password"
              @focus="focus.password = true"
              @blur="focus.password = false; validateField('password')"
              @keyup.enter="handleLogin"
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

        <button class="submit-btn" :disabled="loading" @click="handleLogin">
          <span v-if="!loading" class="btn-text">登 录</span>
          <span v-else class="btn-loader">
            <span></span><span></span><span></span>
          </span>
        </button>

        <p class="switch-link">
          还没有账号？
          <router-link to="/register">立即注册 →</router-link>
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

const form = reactive({ username: '', password: '' })
const errors = reactive({ username: '', password: '' })
const focus = reactive({ username: false, password: false })

function validateField(field: 'username' | 'password') {
  if (field === 'username') {
    errors.username = form.username.trim() ? '' : '请输入用户名'
  } else {
    errors.password = form.password ? '' : '请输入密码'
  }
}

async function handleLogin() {
  validateField('username')
  validateField('password')
  if (errors.username || errors.password) return

  loading.value = true
  try {
    await authStore.login(form.username, form.password)
    message.success('登录成功，欢迎回来！')
    router.push('/')
  } catch (e: any) {
    message.error(e.response?.data?.detail || '用户名或密码错误')
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

/* 背景纹理 */
.panel-left::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(circle at 20% 20%, rgba(255,255,255,0.04) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(240,180,40,0.06) 0%, transparent 50%);
  pointer-events: none;
}

/* 品牌标识 */
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

/* 插图区 */
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

/* 左侧标语 */
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

/* 底部版权 */
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
  margin-bottom: 36px;
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
  margin-bottom: 20px;
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

/* ===== 登录按钮 ===== */
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
  margin-top: 28px;
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

/* 加载动画 */
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

/* ===== 切换链接 ===== */
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
  transform-origin: center;
}

.float-mid {
  animation: floatMid 4s ease-in-out infinite 0.8s;
  transform-origin: center;
}

.float-fast {
  animation: floatFast 3.5s ease-in-out infinite 0.4s;
  transform-origin: center;
}

.owl-bounce {
  animation: owlFloat 4.5s ease-in-out infinite 0.2s;
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

@keyframes floatSlow {
  0%, 100% { transform: translateY(0px) rotate(-1deg); }
  50% { transform: translateY(-12px) rotate(1deg); }
}

@keyframes floatMid {
  0%, 100% { transform: translateY(0px) rotate(2deg); }
  50% { transform: translateY(-16px) rotate(-1deg); }
}

@keyframes floatFast {
  0%, 100% { transform: translateY(0px) rotate(-2deg); }
  50% { transform: translateY(-10px) rotate(1deg); }
}

@keyframes owlFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

@keyframes twinkle {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.35; transform: scale(0.75); }
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .auth-page { flex-direction: column; }
  .panel-left {
    flex: 0 0 auto;
    padding: 28px 24px;
    min-height: 260px;
  }
  .illustration-wrap { max-height: 180px; }
  .left-tagline { display: none; }
  .panel-right {
    flex: 1;
    padding: 36px 24px;
  }
}
</style>
