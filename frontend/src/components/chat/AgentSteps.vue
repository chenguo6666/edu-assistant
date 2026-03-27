<template>
  <div class="agent-steps" v-if="steps.length > 0">
    <div class="steps-header" @click="expanded = !expanded">
      <n-icon size="14" :style="{ transform: expanded ? 'rotate(90deg)' : 'rotate(0)', transition: 'transform 0.2s' }">
        <ChevronIcon />
      </n-icon>
      <span>{{ expanded ? '收起' : '查看' }}工具调用（{{ steps.length }} 步）</span>
      <span class="steps-summary" v-if="!expanded">
        {{ steps.map(s => s.tool_name).join(' → ') }}
      </span>
    </div>
    <div class="steps-list" v-show="expanded">
      <div
        v-for="step in steps"
        :key="step.step_number"
        class="step-item"
        :class="step.status"
      >
        <div class="step-header">
          <span class="step-badge">{{ step.step_number }}</span>
          <span class="step-tool">{{ step.tool_name }}</span>
          <span class="step-status">
          <template v-if="step.status === 'running'">
              <n-spin size="tiny" style="margin-right:4px" />执行中
            </template>
            <template v-else-if="step.status === 'done'">完成</template>
            <template v-else>失败</template>
          </span>
        </div>
        <div class="step-detail" v-if="step.output">
          <div class="step-output">{{ step.output }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NIcon, NSpin } from 'naive-ui'
import { ChevronForwardOutline as ChevronIcon } from '@vicons/ionicons5'
import type { AgentStep } from '../../types'

defineProps<{ steps: AgentStep[] }>()
const expanded = ref(false)
</script>

<style scoped>
.agent-steps {
  margin-bottom: 8px;
  font-size: 13px;
}

.steps-header {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  color: #888;
  padding: 4px 0;
  user-select: none;
}

.steps-summary {
  margin-left: 6px;
  color: #aaa;
  font-size: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 200px;
}

.steps-list {
  border-left: 2px solid #e0e0e0;
  margin-left: 6px;
  padding-left: 12px;
}

.step-item {
  margin: 8px 0;
  padding: 8px 10px;
  border-radius: 6px;
  background: #fafafa;
}

.step-item.error {
  background: #fff2f0;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.step-badge {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #667eea;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  flex-shrink: 0;
}

.step-tool {
  font-weight: 500;
  color: #333;
}

.step-status {
  margin-left: auto;
  color: #999;
  font-size: 12px;
}

.step-item.done .step-status {
  color: #52c41a;
}

.step-item.error .step-status {
  color: #ff4d4f;
}

.step-detail {
  margin-top: 6px;
}

.step-output {
  color: #666;
  font-size: 12px;
  max-height: 100px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
