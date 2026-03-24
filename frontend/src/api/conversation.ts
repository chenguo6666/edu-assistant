/** 对话相关 API */
import api from './index'
import type { Conversation, ConversationDetail } from '../types'

export function listConversationsApi() {
  return api.get<Conversation[]>('/conversations')
}

export function createConversationApi(mode: string) {
  return api.post<Conversation>('/conversations', { mode })
}

export function getConversationApi(id: number) {
  return api.get<ConversationDetail>(`/conversations/${id}`)
}

export function updateConversationApi(id: number, title: string) {
  return api.put<Conversation>(`/conversations/${id}`, { title })
}

export function deleteConversationApi(id: number) {
  return api.delete(`/conversations/${id}`)
}
