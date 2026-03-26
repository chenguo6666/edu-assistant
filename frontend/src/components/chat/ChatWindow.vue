<template>
  <div class="chat-window">
    <!-- 消息列表 -->
    <div class="messages-area" ref="messagesAreaRef">
      <!-- 初始加载中 -->
      <div v-if="loadingHistory" class="empty-chat">
        <n-spin size="medium" />
      </div>

      <!-- 空状态：欢迎语 -->
      <div v-else-if="messages.length === 0 && !isThinking && !streamingContent" class="empty-chat">
        <p class="empty-title">你好，有什么可以帮你？</p>
        <p class="empty-subtitle">{{ modeSubtitle }}</p>
      </div>

      <!-- 历史消息 -->
      <MessageBubble
        v-for="(msg, idx) in messages"
        :key="msg.id"
        :message="msg"
        :is-last="msg.role === 'assistant' && idx === messages.length - 1"
        @regenerate="handleRegenerate"
        @send-message="handleSend"
      />

      <!-- 正在生成的 AI 消息 -->
      <div v-if="isThinking || streamingContent" class="message-bubble assistant">
        <div class="bubble-avatar">AI</div>
        <div class="bubble-content">
          <AgentSteps v-if="agentSteps.length > 0" :steps="agentSteps" />
          <div class="bubble-text thinking" v-if="isThinking && !streamingContent">
            <span class="dot-1">●</span><span class="dot-2">●</span><span class="dot-3">●</span>
          </div>
          <div class="bubble-text" v-else-if="streamingContent" v-html="renderedStreaming"></div>
        </div>
      </div>
    </div>

    <!-- 预设快捷按钮（常驻输入框上方） -->
    <div class="preset-bar">
      <button
        v-for="card in presetCards"
        :key="card.label"
        class="preset-chip"
        @click="fillPreset(card.text)"
      >
        <span class="chip-icon">{{ card.icon }}</span>
        <span class="chip-label">{{ card.label }}</span>
      </button>
    </div>

    <!-- 输入框 -->
    <MessageInput
      ref="messageInputRef"
      :disabled="isThinking || (!!streamingContent && !isDone)"
      @send="handleSend"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { NSpin } from 'naive-ui'
import MarkdownIt from 'markdown-it'
import type { Message } from '../../types'
import { useWebSocket } from '../../composables/useWebSocket'
import { useConversationStore } from '../../stores/conversation'
import MessageBubble from './MessageBubble.vue'
import MessageInput from './MessageInput.vue'
import AgentSteps from './AgentSteps.vue'

const props = defineProps<{ conversationId: number }>()
const conversationStore = useConversationStore()
const messagesAreaRef = ref<HTMLElement>()
const messageInputRef = ref<InstanceType<typeof MessageInput>>()
const loadingHistory = ref(false)

const md = new MarkdownIt({ html: false, linkify: true, breaks: true })

const {
  isThinking, isDone, currentTokens, agentSteps,
  connect, sendMessage, disconnect, resetStreamingState,
} = useWebSocket()

const messages = computed(() => conversationStore.messages)
const streamingContent = computed(() => currentTokens.value)
const renderedStreaming = computed(() => md.render(currentTokens.value))

// 各模式预设问题卡片
const EDU_PRESETS = [
  { icon: '📝', label: '总结课文', text: '请帮我总结以下内容，提取核心知识点：\n\n' },
  { icon: '❓', label: '生成练习题', text: '请根据以下内容生成5道选择题（每题附答案和解析）：\n\n' },
  { icon: '💡', label: '解释概念', text: '请用简单易懂的方式解释以下概念：\n\n' },
  { icon: '📅', label: '制定学习计划', text: '请帮我制定一个两周的学习计划，目标是：\n\n' },
  { icon: '🔍', label: '提取知识点', text: '请从以下内容中提取重要知识点并整理成结构化笔记：\n\n' },
  { icon: '📖', label: '推荐学习资源', text: '请推荐学习以下方向的优质资源和方法：\n\n' },
]

const ADMISSION_PRESETS = [
  { icon: '🏫', label: '查询保研条件', text: '清华大学计算机系保研需要什么条件？' },
  { icon: '📅', label: '预推免时间线', text: '2024年CS专业保研预推免的时间安排是什么？' },
  { icon: '📊', label: '院校横向对比', text: '请比较北京大学、清华大学、浙江大学的CS保研要求' },
  { icon: '✅', label: '条件自测匹配', text: '我是985本科，GPA 3.8，有一篇论文，适合申请哪些学校的CS保研？' },
  { icon: '💼', label: '面试备考指南', text: '如何准备CS保研面试？考察哪些方面，有哪些注意事项？' },
  { icon: '📝', label: '个人陈述写作', text: '请分析CS保研个人陈述应该包含哪些内容，如何突出亮点？' },
]

const presetCards = computed(() =>
  conversationStore.currentMode === 'edu' ? EDU_PRESETS : ADMISSION_PRESETS,
)

const modeSubtitle = computed(() =>
  conversationStore.currentMode === 'edu'
    ? '选择下方卡片快速提问，或直接输入你的问题'
    : '选择下方卡片了解保研信息，或直接输入你的问题',
)

function fillPreset(text: string) {
  messageInputRef.value?.fill(text)
}

function handleSend(content: string) {
  // 临时显示用户消息
  const tempMsg: Message = {
    id: Date.now(),
    role: 'user',
    content,
    created_at: new Date().toISOString(),
  }
  conversationStore.addMessage(tempMsg)
  scrollToBottom()
  sendMessage(content)
}

/** 重新回答：找到最后一个用户消息，重新发送 */
function handleRegenerate() {
  const lastUserMsg = [...messages.value].reverse().find((m) => m.role === 'user')
  if (!lastUserMsg) return
  sendMessage(lastUserMsg.content)
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesAreaRef.value) {
      messagesAreaRef.value.scrollTop = messagesAreaRef.value.scrollHeight
    }
  })
}

// 流式内容和步骤变化时滚动
watch([currentTokens, () => agentSteps.value.length], scrollToBottom)

// done 信号触发后重载对话消息：先加载历史，再清空流式状态，避免重复显示
watch(isDone, async (val) => {
  if (val) {
    await conversationStore.selectConversation(props.conversationId)
    conversationStore.loadConversations()
    resetStreamingState()
  }
})

// 对话切换时重连 WebSocket 并重置状态
watch(
  () => props.conversationId,
  async (newId, oldId) => {
    if (newId !== oldId) {
      disconnect()
      connect(newId)
      loadingHistory.value = true
      await conversationStore.selectConversation(newId)
      loadingHistory.value = false
      scrollToBottom()
    }
  },
)

onMounted(() => {
  connect(props.conversationId)
  scrollToBottom()
})

onUnmounted(() => {
  disconnect()
})
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 16px 0;
  min-height: 0;
}

/* 空状态 */
.empty-chat {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 0 24px;
}

.empty-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.empty-subtitle {
  font-size: 13px;
  color: #999;
}

/* 预设快捷按钮栏（常驻输入框上方） */
.preset-bar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
  padding: 6px 20px;
  flex-shrink: 0;
}

.preset-chip {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 10px;
  background: #f7f7f8;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  cursor: pointer;
  font-family: inherit;
  transition: border-color 0.15s, background 0.15s;
  white-space: nowrap;
  overflow: hidden;
}

.preset-chip:hover {
  border-color: #667eea;
  background: #f0f0ff;
}

.chip-icon {
  font-size: 14px;
  line-height: 1;
  flex-shrink: 0;
}

.chip-label {
  font-size: 12px;
  color: #555;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 正在生成的气泡（与 MessageBubble 保持一致） */
.message-bubble {
  display: flex;
  gap: 12px;
  padding: 12px 20px;
}

.bubble-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #e8e8e8;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
}

.bubble-content {
  max-width: 75%;
  min-width: 0;
}

.bubble-text {
  padding: 10px 14px;
  border-radius: 12px;
  border-bottom-left-radius: 4px;
  font-size: 14px;
  line-height: 1.6;
  background: #f0f0f0;
  color: #333;
  word-break: break-word;
}

/* 三点动画 */
.bubble-text.thinking {
  display: flex;
  gap: 4px;
  align-items: center;
  padding: 12px 16px;
}

.bubble-text.thinking span {
  font-size: 18px;
  color: #999;
  animation: blink 1.4s infinite;
}
.dot-2 { animation-delay: 0.2s !important; }
.dot-3 { animation-delay: 0.4s !important; }

@keyframes blink {
  0%, 80%, 100% { opacity: 0.2; }
  40% { opacity: 1; }
}

.bubble-text :deep(p) { margin: 0 0 8px; }
.bubble-text :deep(p:last-child) { margin-bottom: 0; }
.bubble-text :deep(pre) {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 13px;
}
.bubble-text :deep(code) { font-family: 'Consolas', 'Monaco', monospace; }
.bubble-text :deep(ul), .bubble-text :deep(ol) { padding-left: 20px; margin: 4px 0; }
.bubble-text :deep(table) { border-collapse: collapse; width: 100%; margin: 8px 0; }
.bubble-text :deep(th), .bubble-text :deep(td) {
  border: 1px solid #ddd;
  padding: 6px 10px;
  font-size: 13px;
}
.bubble-text :deep(th) { background: #f5f5f5; font-weight: 600; }
</style>
