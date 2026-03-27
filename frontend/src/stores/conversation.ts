/** 对话状态管理 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Conversation, Message } from '../types'
import {
  listConversationsApi,
  createConversationApi,
  getConversationApi,
  deleteConversationApi,
} from '../api/conversation'

export const useConversationStore = defineStore('conversation', () => {
  const conversations = ref<Conversation[]>([])
  const currentId = ref<number | null>(null)
  const messages = ref<Message[]>([])
  const currentMode = ref<'edu' | 'admission'>('edu')

  async function loadConversations() {
    const { data } = await listConversationsApi()
    conversations.value = data
  }

  async function createConversation(mode?: string) {
    const m = mode || currentMode.value
    const { data } = await createConversationApi(m)
    conversations.value.unshift(data)
    await selectConversation(data.id)
    return data
  }

  async function selectConversation(id: number) {
    currentId.value = id
    const { data } = await getConversationApi(id)
    messages.value = data.messages
    currentMode.value = data.mode as 'edu' | 'admission'
  }

  async function removeConversation(id: number) {
    await deleteConversationApi(id)
    conversations.value = conversations.value.filter((c) => c.id !== id)
    if (currentId.value === id) {
      currentId.value = null
      messages.value = []
    }
  }

  function addMessage(msg: Message) {
    messages.value.push(msg)
  }

  function updateLastAssistantMessage(content: string, agentSteps?: string) {
    const last = messages.value[messages.value.length - 1]
    if (last && last.role === 'assistant') {
      last.content = content
      if (agentSteps) last.agent_steps = agentSteps
    }
  }

  /** 重置所有状态（切换用户时调用） */
  function $reset() {
    conversations.value = []
    currentId.value = null
    messages.value = []
    currentMode.value = 'edu'
  }

  return {
    conversations, currentId, messages, currentMode,
    loadConversations, createConversation, selectConversation,
    removeConversation, addMessage, updateLastAssistantMessage, $reset,
  }
})
