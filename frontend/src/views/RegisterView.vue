<template>
  <div class="register-page">
    <n-card title="EduAssistant 注册" style="width: 400px">
      <n-form ref="formRef" :model="form" :rules="rules">
        <n-form-item label="用户名" path="username">
          <n-input v-model:value="form.username" placeholder="请输入用户名" />
        </n-form-item>
        <n-form-item label="密码" path="password">
          <n-input v-model:value="form.password" type="password" placeholder="请输入密码" />
        </n-form-item>
        <n-form-item label="确认密码" path="confirmPassword">
          <n-input v-model:value="form.confirmPassword" type="password" placeholder="请再次输入密码"
            @keyup.enter="handleRegister" />
        </n-form-item>
      </n-form>
      <n-button type="primary" block :loading="loading" @click="handleRegister">
        注册
      </n-button>
      <div style="margin-top: 12px; text-align: center">
        已有账号？<router-link to="/login">去登录</router-link>
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

const form = reactive({ username: '', password: '', confirmPassword: '' })
const rules = {
  username: { required: true, message: '请输入用户名', trigger: 'blur' },
  password: { required: true, message: '请输入密码', trigger: 'blur' },
  confirmPassword: { required: true, message: '请确认密码', trigger: 'blur' },
}

async function handleRegister() {
  if (!form.username || !form.password) return
  if (form.password !== form.confirmPassword) {
    message.error('两次输入的密码不一致')
    return
  }
  loading.value = true
  try {
    await authStore.register(form.username, form.password)
    message.success('注册成功')
    router.push('/')
  } catch (e: any) {
    message.error(e.response?.data?.detail || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
