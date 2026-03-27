/** 知识库相关 API */
import api from './index'

export interface DocumentItem {
  id: number
  filename: string
  file_type: string
  chunk_count: number
  created_at: string
}

export function uploadDocumentApi(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  return api.post<DocumentItem>('/knowledge/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 60000,
  })
}

export function listDocumentsApi() {
  return api.get<DocumentItem[]>('/knowledge/documents')
}

export function deleteDocumentApi(id: number) {
  return api.delete(`/knowledge/documents/${id}`)
}
