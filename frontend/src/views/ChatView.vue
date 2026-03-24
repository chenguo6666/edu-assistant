<template>
  <div class="chat-page">
    <!-- 顶部导航 -->
    <header class="chat-header">
      <div class="header-left">
        <h2>EduAssistant</h2>
      </div>
      <div class="header-center">
        <n-tabs v-model:value="currentTab" type="segment" size="small" @update:value="handleTabChange">
          <n-tab name="edu">教育助手</n-tab>
          <n-tab name="admission">保研助手</n-tab>
        </n-tabs>
      </div>
      <div class="header-right">
        <span class="username-tag" v-if="authStore.user">{{ authStore.user.username }}</span>
        <n-dropdown :options="userMenuOptions" @select="handleUserMenu">
          <n-button quaternary circle>
            <n-icon size="20"><UserIcon /></n-icon>
          </n-button>
        </n-dropdown>
      </div>
    </header>

    <!-- 主体区域 -->
    <div class="chat-body">
      <!-- 左侧对话列表 -->
      <aside class="chat-sidebar">
        <n-button block type="primary" @click="handleNewChat" style="margin-bottom: 12px">
          + 新建对话
        </n-button>
        <div class="conversation-list">
          <div
            v-for="conv in filteredConversations"
            :key="conv.id"
            class="conversation-item"
            :class="{ active: conv.id === conversationStore.currentId }"
            @click="conversationStore.selectConversation(conv.id)"
          >
            <span class="conv-mode-badge" :class="conv.mode">
              {{ conv.mode === 'edu' ? '学' : '研' }}
            </span>
            <span class="conv-title">{{ conv.title }}</span>
            <n-button quaternary circle size="tiny" style="flex-shrink:0"
              @click.stop="conversationStore.removeConversation(conv.id)">
              ×
            </n-button>
          </div>
          <n-empty v-if="filteredConversations.length === 0"
            :description="currentTab === 'edu' ? '暂无教育对话' : '暂无保研对话'" size="small" />
        </div>

        <!-- 教育模式下显示文件上传 -->
        <div v-if="currentTab === 'edu'" class="sidebar-section">
          <n-divider title-placement="left">
            <span style="font-size:12px;color:#999">我的文档</span>
          </n-divider>
          <FileUpload />
        </div>
      </aside>

      <!-- 右侧聊天区域 -->
      <main class="chat-main">
        <div class="chat-placeholder" v-if="!conversationStore.currentId">
          <n-empty :description="currentTab === 'edu' ? '开始一次学习对话' : '开始一次保研咨询'">
            <template #extra>
              <n-button type="primary" @click="handleNewChat">新建对话</n-button>
            </template>
          </n-empty>
        </div>
        <ChatWindow v-else :conversation-id="conversationStore.currentId" />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NTabs, NTab, NButton, NIcon, NDropdown, NEmpty, NDivider } from 'naive-ui'
import { PersonCircleOutline as UserIcon } from '@vicons/ionicons5'
import { useAuthStore } from '../stores/auth'
import { useConversationStore } from '../stores/conversation'
import ChatWindow from '../components/chat/ChatWindow.vue'
import FileUpload from '../components/knowledge/FileUpload.vue'

const router = useRouter()
const authStore = useAuthStore()
const conversationStore = useConversationStore()

// Tab 独立管理，不直接绑定 store.currentMode（避免切换对话时 Tab 乱跳）
const currentTab = ref<'edu' | 'admission'>('edu')

// 按当前 Tab 过滤对话列表
const filteredConversations = computed(() =>
  conversationStore.conversations.filter((c) => c.mode === currentTab.value),
)

const userMenuOptions = [
  { label: `用户中心${authStore.user?.grade ? `（${authStore.user.grade}）` : ''}`, key: 'profile' },
  { label: '退出登录', key: 'logout' },
]

async function handleTabChange(mode: string) {
  currentTab.value = mode as 'edu' | 'admission'
  conversationStore.currentMode = mode as 'edu' | 'admission'
  // 切换到该模式最近的对话，没有则清空
  const latest = filteredConversations.value[0]
  if (latest) {
    await conversationStore.selectConversation(latest.id)
  } else {
    conversationStore.currentId = null
    conversationStore.messages = []
  }
}

function handleUserMenu(key: string) {
  if (key === 'profile') router.push('/profile')
  if (key === 'logout') {
    authStore.logout()
    router.push('/login')
  }
}

async function handleNewChat() {
  await conversationStore.createConversation(currentTab.value)
}

onMounted(async () => {
  await authStore.fetchUser()
  await conversationStore.loadConversations()
  // 默认选中最近的对话
  const latest = filteredConversations.value[0]
  if (latest) await conversationStore.selectConversation(latest.id)
})
</script>

<style scoped>
.chat-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 56px;
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
  flex-shrink: 0;
}

.header-left h2 {
  font-size: 18px;
  font-weight: 600;
  color: #667eea;
}

.header-center { width: 240px; }

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username-tag {
  font-size: 13px;
  color: #666;
}

.chat-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.chat-sidebar {
  width: 260px;
  background: #fff;
  border-right: 1px solid #e8e8e8;
  padding: 12px;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  overflow: hidden;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}

.conversation-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 10px;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 4px;
  transition: background 0.2s;
}

.conversation-item:hover { background: #f0f0f0; }
.conversation-item.active { background: #e8e8ff; }

.conv-mode-badge {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

.conv-mode-badge.edu { background: #e0e7ff; color: #5b21b6; }
.conv-mode-badge.admission { background: #fef3c7; color: #92400e; }

.conv-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13px;
  color: #333;
}

.sidebar-section { flex-shrink: 0; }

.chat-main {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.chat-placeholder {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
