<template>
  <div class="message-bubble" :class="message.role">
    <div class="bubble-avatar">
      {{ message.role === 'user' ? '你' : 'AI' }}
    </div>
    <div class="bubble-content">
      <!-- Agent 步骤展示（AI 消息且有步骤时） -->
      <AgentSteps v-if="message.role === 'assistant' && parsedSteps.length > 0" :steps="parsedSteps" />
      <!-- 消息正文 -->
      <div class="bubble-text" ref="bubbleTextRef" v-html="renderedContent"></div>
      <!-- 去答题按钮（检测到出题内容时显示） -->
      <button v-if="isQuizMessage" class="action-btn quiz-btn" @click="showQuizModal = true">
        📝 去答题
      </button>
      <!-- 答题弹窗 -->
      <QuizInteractive
        v-if="showQuizModal"
        :content="quizContent"
        @close="showQuizModal = false"
        @submit-answers="(text: string) => { showQuizModal = false; $emit('sendMessage', text) }"
      />
      <!-- AI 消息操作栏 -->
      <div v-if="message.role === 'assistant'" class="bubble-actions">
        <button class="action-btn" title="复制" @click="handleCopy">
          <span v-if="copied">✓ 已复制</span>
          <span v-else>📋 复制</span>
        </button>
        <button class="action-btn" title="朗读" @click="handleSpeak">
          <span v-if="speaking">⏹ 停止</span>
          <span v-else>🔊 朗读</span>
        </button>
        <button v-if="isLast" class="action-btn" title="重新回答" @click="$emit('regenerate')">
          🔄 重新回答
        </button>
        <button class="action-btn" title="导出" @click="showExport = !showExport">
          📥 导出
        </button>
        <div v-if="showExport" class="export-menu">
          <button class="export-option" @click="handleExport('md')">Markdown (.md)</button>
          <button class="export-option" @click="handleExport('pdf')">PDF (.pdf)</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'
import MarkdownIt from 'markdown-it'
import type { Message, AgentStep } from '../../types'
import AgentSteps from './AgentSteps.vue'
import QuizInteractive from './QuizInteractive.vue'

const props = defineProps<{
  message: Message
  isLast?: boolean
}>()

defineEmits<{ regenerate: [], sendMessage: [text: string] }>()

/** 检测 agent_steps 中是否有 generate_quiz 工具调用 */
const hasQuizTool = computed(() => {
  if (!props.message.agent_steps) return false
  try {
    const steps = JSON.parse(props.message.agent_steps)
    return steps.some((s: any) => s.tool === 'generate_quiz')
  } catch {
    return false
  }
})

/** 兜底检测：消息内容本身是否包含题目（选择题 A/B/C/D 选项模式） */
const hasQuizContent = computed(() => {
  if (props.message.role !== 'assistant') return false
  const text = props.message.content || ''
  // 至少包含两个 A/B/C/D 选项行，且包含"题"字
  const hasOptions = (text.match(/^[\s*\-]*[A-D][\.\、\)\）\s]/gm) || []).length >= 4
  const hasQuizKeyword = /选择题|练习题|习题|测试题|简答题|填空题/.test(text)
  return hasOptions && hasQuizKeyword
})

/** 是否显示"去答题"按钮 */
const isQuizMessage = computed(() => hasQuizTool.value || hasQuizContent.value)

/** 提取题目文本：合并所有 generate_quiz 工具输出，兜底用 message.content 的题目段落 */
const quizContent = computed(() => {
  if (props.message.agent_steps) {
    try {
      const steps = JSON.parse(props.message.agent_steps)
      // 合并所有 generate_quiz 调用的输出（可能分多次调用不同题型）
      const quizOutputs = steps
        .filter((s: any) => s.tool === 'generate_quiz' && s.output)
        .map((s: any) => s.output as string)
      if (quizOutputs.length > 0) return quizOutputs.join('\n\n')
    } catch { /* fallback */ }
  }
  // 兜底：从 message.content 中提取题目段落
  const text = props.message.content || ''
  const quizStart = text.search(/#{1,3}\s*.*?[练习测试]*题|[一二三四五六七八九十]、\s*选择题|[一二三四五六七八九十]、\s*填空题|[一二三四五六七八九十]、\s*简答题/)
  if (quizStart > 0) return text.slice(quizStart)
  return text
})

const bubbleTextRef = ref<HTMLElement>()
const showQuizModal = ref(false)
const copied = ref(false)
const speaking = ref(false)
const showExport = ref(false)
let copyTimer: ReturnType<typeof setTimeout> | null = null
let utterance: SpeechSynthesisUtterance | null = null

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

/** 复制消息内容（原始 Markdown） */
async function handleCopy() {
  try {
    await navigator.clipboard.writeText(props.message.content || '')
    copied.value = true
    if (copyTimer) clearTimeout(copyTimer)
    copyTimer = setTimeout(() => { copied.value = false }, 2000)
  } catch {
    // 降级：使用 textarea 方式
    const ta = document.createElement('textarea')
    ta.value = props.message.content || ''
    document.body.appendChild(ta)
    ta.select()
    document.execCommand('copy')
    document.body.removeChild(ta)
    copied.value = true
    copyTimer = setTimeout(() => { copied.value = false }, 2000)
  }
}

/** 朗读消息内容（Web Speech API） */
function handleSpeak() {
  if (speaking.value) {
    speechSynthesis.cancel()
    speaking.value = false
    return
  }
  // 去除 Markdown 标记，朗读纯文本
  const text = (props.message.content || '').replace(/[#*`_~\[\]()>|\\-]/g, '').trim()
  utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = 'zh-CN'
  utterance.rate = 1.0
  utterance.onend = () => { speaking.value = false }
  utterance.onerror = () => { speaking.value = false }
  speaking.value = true
  speechSynthesis.speak(utterance)
}

/** 导出单条消息 */
function handleExport(format: 'md' | 'pdf') {
  showExport.value = false
  const content = props.message.content || ''
  const timestamp = new Date(props.message.created_at).toLocaleString('zh-CN')
  const filename = `EduAssistant_${new Date().toISOString().slice(0, 10)}`

  if (format === 'md') {
    const mdContent = `# EduAssistant 导出\n\n> 导出时间：${timestamp}\n\n---\n\n${content}\n`
    downloadFile(`${filename}.md`, mdContent, 'text/markdown;charset=utf-8')
  } else {
    exportAsPdf(content, timestamp, filename)
  }
}

/** 下载文件工具函数 */
function downloadFile(name: string, content: string, type: string) {
  const blob = new Blob([content], { type })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = name
  a.click()
  URL.revokeObjectURL(url)
}

/** 导出为 PDF（利用浏览器打印功能） */
function exportAsPdf(content: string, timestamp: string, filename: string) {
  const html = md.render(content)
  const printWindow = window.open('', '_blank')
  if (!printWindow) return
  printWindow.document.write(`<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>${filename}</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 800px; margin: 0 auto; padding: 40px 20px; color: #333; line-height: 1.8; font-size: 14px; }
  h1, h2, h3 { color: #1a1a2e; }
  pre { background: #f5f5f5; padding: 12px; border-radius: 6px; overflow-x: auto; }
  code { font-family: Consolas, Monaco, monospace; }
  table { border-collapse: collapse; width: 100%; } th, td { border: 1px solid #ddd; padding: 8px; }
  .meta { color: #999; font-size: 12px; margin-bottom: 20px; }
</style></head><body>
<h1>EduAssistant 导出</h1>
<p class="meta">导出时间：${timestamp}</p>
<hr/>
${html}
</body></html>`)
  printWindow.document.close()
  // 等待渲染后自动弹出打印对话框
  printWindow.onload = () => { printWindow.print() }
}

onUnmounted(() => {
  if (copyTimer) clearTimeout(copyTimer)
  if (speaking.value) speechSynthesis.cancel()
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

/* 消息操作栏 */
.bubble-actions {
  display: flex;
  align-items: center;
  gap: 2px;
  margin-top: 4px;
  position: relative;
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  padding: 2px 8px;
  border: none;
  background: transparent;
  color: #999;
  font-size: 12px;
  cursor: pointer;
  border-radius: 4px;
  font-family: inherit;
  transition: color 0.15s, background 0.15s;
}

.action-btn:hover {
  color: #667eea;
  background: #f0f0ff;
}

/* 导出下拉菜单 */
.export-menu {
  position: absolute;
  bottom: 100%;
  left: 0;
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 4px;
  z-index: 10;
}

.export-option {
  display: block;
  width: 100%;
  padding: 6px 12px;
  border: none;
  background: none;
  font-size: 13px;
  color: #333;
  cursor: pointer;
  border-radius: 4px;
  text-align: left;
  white-space: nowrap;
  font-family: inherit;
}

.export-option:hover {
  background: #f0f0ff;
  color: #667eea;
}

/* 去答题按钮 */
.quiz-btn {
  margin-top: 6px;
  padding: 4px 14px !important;
  background: #667eea !important;
  color: #fff !important;
  border-radius: 6px !important;
  font-size: 13px !important;
  font-weight: 500;
  transition: opacity 0.15s !important;
}

.quiz-btn:hover {
  opacity: 0.9;
  background: #667eea !important;
  color: #fff !important;
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
