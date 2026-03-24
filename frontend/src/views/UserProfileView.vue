<template>
  <div class="profile-page">
    <n-card class="profile-card">
      <template #header>
        <div class="card-header">
          <n-button quaternary circle @click="router.push('/')">
            <n-icon><ArrowBackIcon /></n-icon>
          </n-button>
          <span>用户中心</span>
        </div>
      </template>

      <n-form :model="form" label-placement="left" label-width="90px">
        <n-form-item label="用户名">
          <n-input :value="authStore.user?.username" disabled />
        </n-form-item>

        <n-divider title-placement="left">
          <span style="font-size: 12px; color: #999">个人信息（影响 AI 个性化回答）</span>
        </n-divider>

        <n-form-item label="年级">
          <n-select
            v-model:value="form.grade"
            :options="gradeOptions"
            placeholder="选择年级"
            clearable
          />
        </n-form-item>

        <n-form-item label="专业">
          <n-input v-model:value="form.major" placeholder="如：计算机科学与技术" clearable />
        </n-form-item>

        <n-form-item label="GPA">
          <n-input-number
            v-model:value="form.gpa"
            :min="0" :max="5" :step="0.01" :precision="2"
            placeholder="如：3.50"
            style="width: 160px"
          />
        </n-form-item>

        <n-form-item label="感兴趣学科">
          <div class="subjects-input">
            <n-dynamic-tags v-model:value="form.subjects" />
            <div class="subjects-hint">按 Enter 添加学科标签，如「机器学习」「算法」</div>
          </div>
        </n-form-item>
      </n-form>

      <div class="form-actions">
        <n-button type="primary" @click="handleSave" :loading="loading" style="width: 120px">
          保存
        </n-button>
        <n-button @click="router.push('/')">返回聊天</n-button>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  NCard, NForm, NFormItem, NInput, NInputNumber, NButton, NIcon,
  NSelect, NDivider, NDynamicTags, useMessage,
} from 'naive-ui'
import { ArrowBackOutline as ArrowBackIcon } from '@vicons/ionicons5'
import { useAuthStore } from '../stores/auth'
import api from '../api/index'

const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()
const loading = ref(false)

const gradeOptions = [
  { label: '大一', value: '大一' },
  { label: '大二', value: '大二' },
  { label: '大三', value: '大三' },
  { label: '大四', value: '大四' },
  { label: '研一', value: '研一' },
  { label: '研二', value: '研二' },
  { label: '研三', value: '研三' },
]

const form = reactive({
  grade: '' as string | null,
  major: '',
  gpa: null as number | null,
  subjects: [] as string[],
})

onMounted(async () => {
  await authStore.fetchUser()
  if (authStore.user) {
    form.grade = authStore.user.grade || null
    form.major = authStore.user.major || ''
    form.gpa = authStore.user.gpa ?? null
    form.subjects = authStore.user.subjects || []
  }
})

async function handleSave() {
  loading.value = true
  try {
    await api.put('/user/profile', {
      grade: form.grade || null,
      major: form.major || null,
      gpa: form.gpa,
      subjects: form.subjects.length > 0 ? form.subjects : null,
    })
    await authStore.fetchUser()
    message.success('保存成功，AI 回答将基于你的信息个性化')
  } catch {
    message.error('保存失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.profile-page {
  min-height: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 40px 20px;
  background: #f5f5f5;
}

.profile-card {
  width: 100%;
  max-width: 520px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
}

.subjects-input {
  width: 100%;
}

.subjects-hint {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}
</style>
