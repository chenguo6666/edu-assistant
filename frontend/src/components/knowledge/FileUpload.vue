<template>
  <div class="file-upload">
    <!-- 上传区域 -->
    <n-upload
      :custom-request="handleUpload"
      :accept="'.pdf,.txt,.md,.docx'"
      :show-file-list="false"
      :disabled="uploading"
    >
      <n-upload-dragger class="upload-dragger">
        <n-icon size="32" color="#667eea"><CloudUploadIcon /></n-icon>
        <p class="upload-hint">点击或拖拽上传文档</p>
        <p class="upload-sub">支持 PDF / TXT / MD / DOCX，最大 10MB</p>
      </n-upload-dragger>
    </n-upload>

    <!-- 上传进度 -->
    <div v-if="uploading" class="uploading-tip">
      <n-spin size="small" /> <span>正在处理文档...</span>
    </div>

    <!-- 已上传文档列表 -->
    <div v-if="documents.length > 0" class="doc-list">
      <div class="doc-list-title">已上传文档（{{ documents.length }}）</div>
      <div v-for="doc in documents" :key="doc.id" class="doc-item">
        <n-icon size="16" color="#667eea"><DocumentIcon /></n-icon>
        <span class="doc-name">{{ doc.filename }}</span>
        <span class="doc-chunks">{{ doc.chunk_count }} 段</span>
        <n-button quaternary circle size="tiny" @click="handleDelete(doc.id)">
          <n-icon><TrashIcon /></n-icon>
        </n-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NUpload, NUploadDragger, NIcon, NSpin, NButton, useMessage } from 'naive-ui'
import {
  CloudUploadOutline as CloudUploadIcon,
  DocumentTextOutline as DocumentIcon,
  TrashOutline as TrashIcon,
} from '@vicons/ionicons5'
import { uploadDocumentApi, listDocumentsApi, deleteDocumentApi } from '../../api/knowledge'
import type { DocumentItem } from '../../api/knowledge'

const message = useMessage()
const uploading = ref(false)
const documents = ref<DocumentItem[]>([])

async function loadDocuments() {
  try {
    const { data } = await listDocumentsApi()
    documents.value = data
  } catch {
    // 静默失败
  }
}

async function handleUpload({ file }: { file: { file: File } }) {
  uploading.value = true
  try {
    await uploadDocumentApi(file.file)
    message.success('文档上传成功，已加入知识库')
    await loadDocuments()
  } catch (e: any) {
    message.error(e.response?.data?.detail || '上传失败')
  } finally {
    uploading.value = false
  }
}

async function handleDelete(id: number) {
  try {
    await deleteDocumentApi(id)
    documents.value = documents.value.filter((d) => d.id !== id)
    message.success('文档已删除')
  } catch {
    message.error('删除失败')
  }
}

onMounted(loadDocuments)
</script>

<style scoped>
.file-upload {
  padding: 12px;
}

.upload-dragger {
  padding: 20px;
  text-align: center;
}

.upload-hint {
  margin: 8px 0 4px;
  font-size: 14px;
  color: #333;
}

.upload-sub {
  font-size: 12px;
  color: #999;
}

.uploading-tip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  font-size: 13px;
  color: #666;
}

.doc-list {
  margin-top: 12px;
}

.doc-list-title {
  font-size: 13px;
  font-weight: 500;
  color: #666;
  margin-bottom: 6px;
}

.doc-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 4px;
  border-radius: 6px;
  font-size: 13px;
}

.doc-item:hover {
  background: #f0f0f0;
}

.doc-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #333;
}

.doc-chunks {
  font-size: 11px;
  color: #999;
  flex-shrink: 0;
}
</style>
