<template>
  <div class="message-bubble" :class="message.role">
    <div class="bubble-avatar">
      {{ message.role === 'user' ? '你' : 'AI' }}
    </div>
    <div class="bubble-content">
      <!-- Agent 步骤展示（AI 消息且有步骤时） -->
      <AgentSteps v-if="message.role === 'assistant' && parsedSteps.length > 0" :steps="parsedSteps" />
      <!-- 消息正文 -->
      <div class="bubble-text" v-html="renderedContent"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import type { Message, AgentStep } from '../../types'
import AgentSteps from './AgentSteps.vue'

const props = defineProps<{ message: Message }>()

const md = new MarkdownIt({
  html: false,
  linkify: true,
  breaks: true,
})

const renderedContent = computed(() => {
  return md.render(props.message.content || '')
})

const parsedSteps = computed<AgentStep[]>(() => {
  if (!props.message.agent_steps) return []
  try {
    const raw = JSON.parse(props.message.agent_steps)
    return raw.map((s: any, i: number) => ({
      step_number: i + 1,
      description: `调用 ${s.tool}`,
      tool_name: s.tool,
      input: s.input,
      output: s.output,
      status: 'done' as const,
    }))
  } catch {
    return []
  }
})
</script>

<style scoped>
.message-bubble {
  display: flex;
  gap: 12px;
  padding: 12px 20px;
  max-width: 100%;
}

.message-bubble.user {
  flex-direction: row-reverse;
}

.bubble-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
}

.user .bubble-avatar {
  background: #667eea;
  color: #fff;
}

.assistant .bubble-avatar {
  background: #e8e8e8;
  color: #333;
}

.bubble-content {
  max-width: 75%;
  min-width: 0;
}

.bubble-text {
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  word-break: break-word;
}

.user .bubble-text {
  background: #667eea;
  color: #fff;
  border-bottom-right-radius: 4px;
}

.assistant .bubble-text {
  background: #f0f0f0;
  color: #333;
  border-bottom-left-radius: 4px;
}

.bubble-text :deep(p) {
  margin: 0 0 8px;
}

.bubble-text :deep(p:last-child) {
  margin-bottom: 0;
}

.bubble-text :deep(pre) {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 13px;
}

.bubble-text :deep(code) {
  font-family: 'Consolas', 'Monaco', monospace;
}

.bubble-text :deep(ul), .bubble-text :deep(ol) {
  padding-left: 20px;
  margin: 4px 0;
}
</style>
