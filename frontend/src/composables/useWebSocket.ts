/** WebSocket 通信组合式函数 */
import { ref } from 'vue'
import type { AgentStep, WSMessage } from '../types'

export function useWebSocket() {
  const ws = ref<WebSocket | null>(null)
  const isConnected = ref(false)
  const isThinking = ref(false)
  const isDone = ref(false)          // done 事件触发后置 true，供外部监听重载对话
  const hasError = ref(false)
  const currentTokens = ref('')
  const agentSteps = ref<AgentStep[]>([])

  function connect(conversationId: number) {
    const token = localStorage.getItem('token')
    if (!token) return

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const url = `${protocol}//${host}/api/chat/ws/${conversationId}?token=${token}`

    ws.value = new WebSocket(url)

    ws.value.onopen = () => { isConnected.value = true }

    ws.value.onclose = () => {
      isConnected.value = false
      isThinking.value = false
    }

    ws.value.onerror = () => {
      isConnected.value = false
      isThinking.value = false
    }

    ws.value.onmessage = (event) => {
      handleMessage(JSON.parse(event.data) as WSMessage)
    }
  }

  function handleMessage(data: WSMessage) {
    switch (data.type) {
      case 'thinking_start':
        isThinking.value = true
        isDone.value = false
        hasError.value = false
        currentTokens.value = ''
        agentSteps.value = []
        break

      case 'tool_call': {
        const d = data.data as Record<string, unknown>
        agentSteps.value.push({
          step_number: d.step_number as number,
          description: `调用 ${d.tool_name}`,
          tool_name: d.tool_name as string,
          input: d.input as string,
          status: 'running',
        })
        break
      }

      case 'tool_result': {
        const d = data.data as Record<string, unknown>
        const step = agentSteps.value.find((s) => s.step_number === (d.step_number as number))
        if (step) {
          step.output = d.output as string
          step.status = (d.status as string) === 'error' ? 'error' : 'done'
        }
        break
      }

      case 'token':
        isThinking.value = false
        currentTokens.value += data.content || ''
        break

      case 'done':
        isThinking.value = false
        if (data.content) currentTokens.value = data.content
        isDone.value = true  // 触发外部监听，重载对话消息
        break

      case 'error':
        isThinking.value = false
        hasError.value = true
        currentTokens.value = `⚠️ ${data.content || '处理失败，请重试'}`
        isDone.value = true
        break
    }
  }

  function sendMessage(content: string) {
    if (ws.value && ws.value.readyState === WebSocket.OPEN) {
      currentTokens.value = ''
      agentSteps.value = []
      isDone.value = false
      hasError.value = false
      isThinking.value = true
      ws.value.send(JSON.stringify({ type: 'message', content }))
    }
  }

  function disconnect() {
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }
    isConnected.value = false
    isThinking.value = false
  }

  // 对话完成后清除流式状态，避免与历史消息重复显示
  function resetStreamingState() {
    currentTokens.value = ''
    agentSteps.value = []
    isDone.value = false
  }

  return {
    isConnected, isThinking, isDone, hasError,
    currentTokens, agentSteps,
    connect, sendMessage, disconnect, resetStreamingState,
  }
}
