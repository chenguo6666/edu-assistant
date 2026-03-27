/** 通用类型定义 */

/** 用户信息 */
export interface User {
  id: number
  username: string
  grade?: string
  major?: string
  subjects?: string[]
  gpa?: number
}

/** 登录/注册响应 */
export interface TokenResponse {
  access_token: string
  token_type: string
  user: User
}

/** 对话 */
export interface Conversation {
  id: number
  title: string
  mode: 'edu' | 'admission'
  created_at: string
  updated_at: string
}

/** 消息 */
export interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  agent_steps?: string
  created_at: string
}

/** 对话详情（含消息） */
export interface ConversationDetail extends Conversation {
  messages: Message[]
}

/** Agent 步骤（前端解析用） */
export interface AgentStep {
  step_number: number
  description: string
  tool_name: string
  input?: string
  output?: string
  status: 'running' | 'done' | 'error'
}

/** WebSocket 推送消息 */
export interface WSMessage {
  type: 'thinking_start' | 'step' | 'tool_call' | 'tool_result' | 'token' | 'done' | 'error'
  content?: string
  data?: Record<string, unknown>
  message_id?: string
}
