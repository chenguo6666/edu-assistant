<template>
  <!-- 弹窗遮罩 -->
  <Teleport to="body">
    <div class="quiz-overlay" @click.self="$emit('close')">
      <div class="quiz-modal">
        <!-- 弹窗头部 -->
        <div class="modal-header">
          <span class="quiz-badge">📝 练习题（共 {{ questions.length }} 题）</span>
          <div class="header-right">
            <span v-if="submitted" class="quiz-score">
              得分：{{ correctCount }}/{{ questions.length }}
            </span>
            <button class="close-btn" @click="$emit('close')">✕</button>
          </div>
        </div>

        <!-- 题目列表 -->
        <div class="modal-body">
          <div v-for="(q, qi) in questions" :key="qi" class="quiz-question" :class="{ submitted }">
            <div class="question-title">
              <span class="question-num">{{ qi + 1 }}.</span>
              <span v-html="renderInline(q.title)"></span>
              <span v-if="submitted" class="result-icon">
                {{ q.isCorrect ? '✅' : '❌' }}
              </span>
            </div>

            <!-- 选择题 -->
            <div v-if="q.type === 'choice'" class="options-list">
              <label
                v-for="opt in q.options"
                :key="opt.key"
                class="option-item"
                :class="{
                  selected: answers[qi] === opt.key,
                  correct: submitted && opt.key === q.answer,
                  wrong: submitted && answers[qi] === opt.key && opt.key !== q.answer,
                }"
              >
                <input
                  type="radio"
                  :name="'q' + qi"
                  :value="opt.key"
                  v-model="answers[qi]"
                  :disabled="submitted"
                />
                <span class="option-key">{{ opt.key }}</span>
                <span class="option-text">{{ opt.text }}</span>
              </label>
            </div>

            <!-- 填空题 -->
            <div v-else-if="q.type === 'fill'" class="fill-area">
              <input
                v-for="(_, fi) in q.blanks"
                :key="fi"
                type="text"
                class="fill-input"
                :class="{ correct: submitted && q.blankResults?.[fi], wrong: submitted && q.blankResults !== undefined && !q.blankResults?.[fi] }"
                :placeholder="'填写第 ' + (fi + 1) + ' 空'"
                v-model="fillAnswers[qi + '-' + fi]"
                :disabled="submitted"
              />
            </div>

            <!-- 简答题 -->
            <div v-else class="short-answer-area">
              <textarea
                class="short-input"
                placeholder="请输入你的答案..."
                v-model="shortAnswers[qi]"
                :disabled="submitted"
                rows="3"
              />
            </div>

            <!-- 提交后显示参考答案 -->
            <div v-if="submitted && q.explanation" class="answer-explanation">
              <strong>参考答案：</strong>
              <span v-html="renderInline(q.explanation)"></span>
            </div>
          </div>
        </div>

        <!-- 底部操作 -->
        <div class="modal-footer">
          <button v-if="!submitted" class="submit-btn" @click="handleSubmit" :disabled="!canSubmit">
            提交答案
          </button>
          <template v-else>
            <button class="submit-btn retry" @click="handleRetry">重新作答</button>
            <button class="submit-btn close-after" @click="$emit('close')">关闭</button>
          </template>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import MarkdownIt from 'markdown-it'

interface QuizOption {
  key: string
  text: string
}

interface QuizQuestion {
  type: 'choice' | 'fill' | 'short'
  title: string
  options?: QuizOption[]
  blanks?: number
  answer?: string
  answers?: string[]
  explanation?: string
  isCorrect?: boolean
  blankResults?: boolean[]
}

const props = defineProps<{
  content: string  // generate_quiz 工具的输出文本（纯题目）
}>()

const emit = defineEmits<{
  close: []
  submitAnswers: [formatted: string]
}>()

const mdInline = new MarkdownIt({ html: false, linkify: false, breaks: false })

function renderInline(text: string) {
  return mdInline.renderInline(text || '')
}

const questions = computed<QuizQuestion[]>(() => parseQuiz(props.content))

const answers = reactive<Record<number, string>>({})
const fillAnswers = reactive<Record<string, string>>({})
const shortAnswers = reactive<Record<number, string>>({})
const submitted = ref(false)
const correctCount = ref(0)

const canSubmit = computed(() => {
  return questions.value.some((q, i) => {
    if (q.type === 'choice') return !!answers[i]
    if (q.type === 'fill') {
      for (let f = 0; f < (q.blanks || 1); f++) {
        if (fillAnswers[i + '-' + f]?.trim()) return true
      }
    }
    if (q.type === 'short') return !!shortAnswers[i]?.trim()
    return false
  })
})

/** 预处理：去除 Markdown 标记，统一格式 */
function preprocessText(raw: string): string {
  let text = raw
  // 去除 Markdown 标题标记
  text = text.replace(/^#{1,6}\s+/gm, '')
  // 去除加粗标记
  text = text.replace(/\*\*(.+?)\*\*/g, '$1')
  // 去除分隔线
  text = text.replace(/^[\-\*]{3,}\s*$/gm, '')
  // 去除 emoji（段落标题前的📝等）
  text = text.replace(/[\u{1F000}-\u{1FFFF}]\s*/gu, '')
  // 去除列表标记前缀（* 、- 、· ），保留 A/B/C/D 选项内容
  text = text.replace(/^[\s]*[\*\-·•]\s+/gm, '')
  return text
}

/** 段落标题正则：匹配"一、选择题"、"选择题（共3题）"等 */
const SECTION_RE = /^(?:[一二三四五六七八九十][、．.]\s*)?(?:选择题|填空题|简答题|判断题|问答题).*$/

/** 从段落标题推断题型 */
function detectSectionType(header: string): 'choice' | 'fill' | 'short' | null {
  if (/选择题/.test(header)) return 'choice'
  if (/填空题/.test(header)) return 'fill'
  if (/简答题|问答题/.test(header)) return 'short'
  return null
}

/** 按题号分割一个段落内的题目 */
function splitQuestions(sectionText: string): string[] {
  return sectionText.split(/(?=(?:^|\n)\s*\d+[\.\、\)\）]\s*)/m).filter(s => s.trim())
}

/** 解析单道选择题 */
function parseChoiceQuestion(lines: string[]): QuizQuestion | null {
  const titleLines: string[] = []
  const options: QuizOption[] = []
  let answer = ''
  let explanation = ''

  for (const line of lines) {
    const optMatch = line.match(/^([A-D])[\.\、\)\）\s]\s*(.+)/)
    if (optMatch) {
      options.push({ key: optMatch[1], text: optMatch[2] })
    } else if (/(?:答案|正确|参考)[：:]\s*([A-D])/i.test(line)) {
      const am = line.match(/(?:答案|正确|参考)[：:]\s*([A-D])/i)
      if (am) answer = am[1]
      const after = line.replace(/.*(?:答案|正确|参考)[：:]\s*[A-D][\s,，]*/i, '').trim()
      if (after) explanation = after
    } else if (/解[析释说]|原因/i.test(line)) {
      explanation = line.replace(/^[解析释说]+[：:]?\s*/, '')
    } else if (options.length === 0) {
      titleLines.push(line)
    }
  }
  if (options.length < 2) return null
  return {
    type: 'choice',
    title: titleLines.join(' ').replace(/^\d+[\.\、\)\）]\s*/, ''),
    options,
    answer,
    explanation: explanation || (answer ? `正确答案：${answer}` : ''),
  }
}

/** 解析单道填空题 */
function parseFillQuestion(lines: string[]): QuizQuestion | null {
  const titleLine = lines[0] || ''
  const blankCount = (titleLine.match(/_{2,}/g) || []).length
  if (blankCount === 0) return null
  let answerText = ''
  for (const line of lines.slice(1)) {
    if (/答案|参考|正确/i.test(line)) {
      answerText = line.replace(/^.*?[：:]\s*/, '')
    }
  }
  return {
    type: 'fill',
    title: titleLine.replace(/^\d+[\.\、\)\）]\s*/, ''),
    blanks: blankCount,
    answer: answerText,
    answers: answerText.split(/[,，、;\s]+/).filter(Boolean),
    explanation: answerText ? `参考答案：${answerText}` : '',
  }
}

/** 解析单道简答题 */
function parseShortQuestion(lines: string[]): QuizQuestion {
  let answerText = ''
  const titleParts: string[] = []
  let collecting = false
  for (const line of lines) {
    if (/(?:参考)?答案[：:]|(?:参考)?解[析释][：:]/.test(line)) {
      collecting = true
      const extracted = line.replace(/^.*?[：:]\s*/, '').trim()
      if (extracted) answerText += extracted + '\n'
    } else if (collecting) {
      answerText += line + '\n'
    } else {
      titleParts.push(line)
    }
  }
  return {
    type: 'short',
    title: titleParts.join(' ').replace(/^\d+[\.\、\)\）]\s*/, ''),
    answer: answerText.trim(),
    explanation: answerText.trim() ? `参考答案：${answerText.trim()}` : '',
  }
}

/** 自动检测单道题的类型并解析 */
function autoParseQuestion(lines: string[]): QuizQuestion | null {
  // 有 A/B/C/D 选项 → 选择题
  if (lines.some(l => /^[A-D][\.\、\)\）\s]/.test(l))) {
    return parseChoiceQuestion(lines)
  }
  // 有 ____ → 填空题
  if (lines.some(l => /_{2,}/.test(l))) {
    return parseFillQuestion(lines)
  }
  // 其它 → 简答题
  return parseShortQuestion(lines)
}

/** 解析题目文本为结构化数据（两层分割：先按段落标题，再按题号） */
function parseQuiz(rawText: string): QuizQuestion[] {
  const text = preprocessText(rawText)
  const result: QuizQuestion[] = []
  const lines = text.split('\n')

  // 第一步：按段落标题拆成 sections
  interface Section { type: 'choice' | 'fill' | 'short' | null; body: string }
  const sections: Section[] = []
  let currentType: 'choice' | 'fill' | 'short' | null = null
  let currentLines: string[] = []

  for (const line of lines) {
    const trimmed = line.trim()
    if (SECTION_RE.test(trimmed)) {
      // 遇到新段落标题：保存上一段
      if (currentLines.length > 0) {
        sections.push({ type: currentType, body: currentLines.join('\n') })
      }
      currentType = detectSectionType(trimmed)
      currentLines = []
    } else {
      currentLines.push(line)
    }
  }
  if (currentLines.length > 0) {
    sections.push({ type: currentType, body: currentLines.join('\n') })
  }

  // 如果完全没有段落标题，把整段作为一个 section
  if (sections.length === 0) {
    sections.push({ type: null, body: text })
  }

  // 第二步：每个 section 按题号分割，逐题解析
  for (const section of sections) {
    const questionBlocks = splitQuestions(section.body)

    for (const block of questionBlocks) {
      const blockLines = block.split('\n').map(l => l.trim()).filter(Boolean)
      if (blockLines.length === 0) continue
      // 必须以题号开头
      if (!/^\d+[\.\、\)\）]/.test(blockLines[0])) continue
      // 过滤掉段落标题残留
      const cleanLines = blockLines.filter(l => !SECTION_RE.test(l))
      if (cleanLines.length === 0) continue

      let q: QuizQuestion | null = null
      if (section.type === 'choice') {
        q = parseChoiceQuestion(cleanLines) || autoParseQuestion(cleanLines)
      } else if (section.type === 'fill') {
        q = parseFillQuestion(cleanLines) || autoParseQuestion(cleanLines)
      } else if (section.type === 'short') {
        q = parseShortQuestion(cleanLines)
      } else {
        q = autoParseQuestion(cleanLines)
      }
      if (q) result.push(q)
    }
  }

  return result
}

/** 提交答案 */
function handleSubmit() {
  submitted.value = true
  let correct = 0
  const formattedParts: string[] = []

  for (let i = 0; i < questions.value.length; i++) {
    const q = questions.value[i]

    if (q.type === 'choice') {
      const userAnswer = answers[i] || '未作答'
      q.isCorrect = q.answer ? userAnswer === q.answer : false
      if (q.isCorrect) correct++
      formattedParts.push(`第${i + 1}题：${userAnswer}`)
    } else if (q.type === 'fill') {
      const blanks: string[] = []
      const blankRes: boolean[] = []
      for (let f = 0; f < (q.blanks || 1); f++) {
        const val = fillAnswers[i + '-' + f]?.trim() || '未作答'
        blanks.push(val)
        const refAnswer = q.answers?.[f] || ''
        blankRes.push(refAnswer ? val.includes(refAnswer) || refAnswer.includes(val) : false)
      }
      q.blankResults = blankRes
      q.isCorrect = blankRes.every(Boolean)
      if (q.isCorrect) correct++
      formattedParts.push(`第${i + 1}题：${blanks.join('、')}`)
    } else {
      const val = shortAnswers[i]?.trim() || '未作答'
      q.isCorrect = false
      formattedParts.push(`第${i + 1}题：${val}`)
    }
  }

  correctCount.value = correct

  const formatted = `请批改我的答案（共${questions.value.length}题）：\n\n${formattedParts.join('\n')}\n\n请逐题指出对错并给出解析。`
  emit('submitAnswers', formatted)
}

/** 重新作答 */
function handleRetry() {
  submitted.value = false
  correctCount.value = 0
  for (const key in answers) delete answers[key]
  for (const key in fillAnswers) delete fillAnswers[key]
  for (const key in shortAnswers) delete shortAnswers[key]
  questions.value.forEach((q) => {
    q.isCorrect = undefined
    q.blankResults = undefined
  })
}
</script>

<style scoped>
/* 遮罩层 */
.quiz-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

/* 弹窗主体 */
.quiz-modal {
  background: #fff;
  border-radius: 14px;
  width: 100%;
  max-width: 640px;
  max-height: 82vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.18);
  overflow: hidden;
}

/* 头部 */
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  background: #f0f0ff;
  border-bottom: 1px solid #e0e0ff;
  flex-shrink: 0;
}

.quiz-badge {
  font-size: 14px;
  font-weight: 600;
  color: #667eea;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.quiz-score {
  font-size: 14px;
  font-weight: 600;
  color: #52c41a;
}

.close-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: #999;
  font-size: 16px;
  cursor: pointer;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, color 0.15s;
  font-family: inherit;
}

.close-btn:hover {
  background: #e8e8e8;
  color: #333;
}

/* 题目区（可滚动） */
.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 4px 0;
}

/* 每道题 */
.quiz-question {
  padding: 14px 18px;
  border-bottom: 1px solid #f0f0f0;
}

.quiz-question:last-child {
  border-bottom: none;
}

.question-title {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 10px;
  line-height: 1.6;
}

.question-num {
  color: #667eea;
  font-weight: 600;
  margin-right: 4px;
}

.result-icon {
  margin-left: 6px;
}

/* 选择题 */
.options-list {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 12px;
  border-radius: 7px;
  cursor: pointer;
  transition: background 0.15s;
  font-size: 14px;
  border: 1px solid transparent;
}

.option-item:hover:not(.submitted .option-item) {
  background: #f0f0ff;
}

.option-item.selected {
  background: #e8e8ff;
  border-color: #c5c5f5;
}

.option-item.correct {
  background: #f0fff0;
  border-color: #b7eb8f;
}

.option-item.wrong {
  background: #fff2f0;
  border-color: #ffccc7;
}

.option-item input[type="radio"] {
  accent-color: #667eea;
}

.option-key {
  font-weight: 600;
  color: #667eea;
  min-width: 18px;
}

.option-text {
  color: #333;
}

/* 填空题 */
.fill-area {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.fill-input {
  padding: 6px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 7px;
  font-size: 14px;
  width: 180px;
  outline: none;
  transition: border-color 0.15s;
  font-family: inherit;
}

.fill-input:focus {
  border-color: #667eea;
}

.fill-input.correct {
  border-color: #52c41a;
  background: #f6ffed;
}

.fill-input.wrong {
  border-color: #ff4d4f;
  background: #fff2f0;
}

/* 简答题 */
.short-answer-area {
  width: 100%;
}

.short-input {
  width: 100%;
  box-sizing: border-box;
  padding: 8px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 7px;
  font-size: 14px;
  outline: none;
  resize: vertical;
  font-family: inherit;
  transition: border-color 0.15s;
}

.short-input:focus {
  border-color: #667eea;
}

/* 参考答案 */
.answer-explanation {
  margin-top: 8px;
  padding: 7px 12px;
  background: #fffbe6;
  border-radius: 7px;
  font-size: 13px;
  color: #666;
  line-height: 1.5;
}

/* 底部按钮 */
.modal-footer {
  padding: 12px 18px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-shrink: 0;
}

.submit-btn {
  padding: 8px 32px;
  border: none;
  background: #667eea;
  color: #fff;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  font-family: inherit;
  font-weight: 500;
  transition: opacity 0.15s;
}

.submit-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.submit-btn:hover:not(:disabled) {
  opacity: 0.88;
}

.submit-btn.retry {
  background: #888;
}

.submit-btn.close-after {
  background: transparent;
  color: #667eea;
  border: 1px solid #667eea;
}

.submit-btn.close-after:hover {
  background: #f0f0ff;
  opacity: 1;
}
</style>
