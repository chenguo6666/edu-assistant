<template>
  <div class="login-page">
    <n-card title="EduAssistant 登录" style="width: 400px">
      <n-form ref="formRef" :model="form" :rules="rules">
        <n-form-item label="用户名" path="username">
          <n-input v-model:value="form.username" placeholder="请输入用户名" />
        </n-form-item>
        <n-form-item label="密码" path="password">
          <n-input v-model:value="form.password" type="password" placeholder="请输入密码"
            @keyup.enter="handleLogin" />
        </n-form-item>
      </n-form>
      <n-button type="primary" block :loading="loading" @click="handleLogin">
        登录
      </n-button>
      <div style="margin-top: 12px; text-align: center">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NForm, NFormItem, NInput, NButton, useMessage } from 'naive-ui'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()
const loading = ref(false)

const form = reactive({ username: '', password: '' })
const rules = {
  username: { required: true, message: '请输入用户名', trigger: 'blur' },
  password: { required: true, message: '请输入密码', trigger: 'blur' },
}

async function handleLogin() {
  if (!form.username || !form.password) return
  loading.value = true
  try {
    await authStore.login(form.username, form.password)
    message.success('登录成功')
    router.push('/')
  } catch (e: any) {
    message.error(e.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
