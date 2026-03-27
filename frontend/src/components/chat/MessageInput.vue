<template>
  <div class="message-input">
    <n-input
      v-model:value="inputText"
      type="textarea"
      placeholder="输入你的问题..."
      :autosize="{ minRows: 1, maxRows: 4 }"
      :disabled="disabled"
      @keydown.enter.exact.prevent="handleSend"
    />
    <n-button
      type="primary"
      :disabled="!inputText.trim() || disabled"
      @click="handleSend"
    >
      发送
    </n-button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NInput, NButton } from 'naive-ui'

const props = defineProps<{ disabled?: boolean }>()
const emit = defineEmits<{ send: [content: string] }>()
const inputText = ref('')

function handleSend() {
  const text = inputText.value.trim()
  if (!text || props.disabled) return
  emit('send', text)
  inputText.value = ''
}

// 供外部填入预设问题
defineExpose({ fill: (text: string) => { inputText.value = text } })
</script>

<style scoped>
.message-input {
  display: flex;
  gap: 10px;
  padding: 16px 20px;
  border-top: 1px solid #e8e8e8;
  background: #fff;
  align-items: flex-end;
}
</style>
