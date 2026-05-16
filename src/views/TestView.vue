<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { SUBTESTS } from '../data/subtests'
import { QUESTIONS } from '../data/questions'
import { useTestStore } from '../store/testStore'
import { Timer, CheckCircle } from '@lucide/vue'

const route = useRoute()
const router = useRouter()
const store = useTestStore()

const subtestId = computed(() => parseInt(route.params.id))
const subtest = computed(() => SUBTESTS.find(s => s.id === subtestId.value))
const questions = computed(() => QUESTIONS[subtestId.value] || [])

const timeLeft = ref(60) // 60 seconds per subtest
let timerInterval = null

// Navigation state
const currentIndex = ref(0)
const currentQuestion = computed(() => questions.value[currentIndex.value])
const progress = computed(() => ((currentIndex.value + 1) / questions.value.length) * 100)

// Store user answers: { [questionId]: selectedOptionIndex }
const userAnswers = ref({})

const startTimer = () => {
  clearInterval(timerInterval)
  timeLeft.value = 60 // Reset timer for each subtest
  timerInterval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      completeSubtest()
    }
  }, 1000)
}

const completeSubtest = () => {
  clearInterval(timerInterval)
  
  // Calculate score
  let correctCount = 0
  questions.value.forEach(q => {
    if (userAnswers.value[q.id] === q.answer) {
      correctCount++
    }
  })
  
  const totalQuestions = questions.value.length
  // Score is percentage (0-100)
  const score = totalQuestions > 0 ? Math.round((correctCount / totalQuestions) * 100) : 0
  
  store.setScore(subtestId.value, score)

  if (subtestId.value < 6) {
    router.push(`/instruction/${subtestId.value + 1}`)
  } else {
    store.finishSession()
    router.push('/result')
  }
}

const selectAnswer = (questionId, optionIndex) => {
  userAnswers.value[questionId] = optionIndex
}

const nextQuestion = () => {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
  } else {
    completeSubtest()
  }
}

const prevQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

// Watch for route changes to reset timer and answers
watch(() => route.params.id, (newId, oldId) => {
  if (newId !== oldId) {
    userAnswers.value = {}
    currentIndex.value = 0
    startTimer()
  }
})

onMounted(() => {
  startTimer()
})

onUnmounted(() => {
  clearInterval(timerInterval)
})

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}
</script>

<template>
  <div class="container animate-fade-in" v-if="subtest">
    <div class="card">
      <div class="test-header">
        <h2>{{ subtest.title }}</h2>
        <div class="timer-badge" :class="{ 'warning': timeLeft < 10 }">
          <Timer :size="18" />
          {{ formatTime(timeLeft) }}
        </div>
      </div>

      <div class="progress-container">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
        <span class="progress-text">Soal {{ currentIndex + 1 }} dari {{ questions.length }}</span>
      </div>

      <div class="question-container" v-if="currentQuestion">
        <div class="question-item animate-slide-up" :key="currentQuestion.id">
          <div class="question-number">Nomor {{ currentIndex + 1 }}</div>
          
          <!-- Type: Text (Logic/Math) -->
          <p v-if="currentQuestion.type === 'text'" class="question-text whitespace-pre-wrap">{{ currentQuestion.question }}</p>

          <!-- Type: Matching (Letters/Symbols) -->
          <div v-if="currentQuestion.type === 'matching'" class="matching-container">
            <p class="question-text">Berapa banyak karakter di baris bawah yang merupakan pasangan karakter di baris atas?</p>
            <div class="matching-rows">
              <div class="row top-row">
                <span v-for="(char, cIdx) in currentQuestion.topRow" :key="'t'+cIdx" class="char-box">{{ char }}</span>
              </div>
              <div class="row bottom-row">
                <span v-for="(char, cIdx) in currentQuestion.bottomRow" :key="'b'+cIdx" class="char-box">{{ char }}</span>
              </div>
            </div>
          </div>

          <!-- Type: Sequence (Memory/Pattern) -->
          <div v-if="currentQuestion.type === 'sequence'" class="sequence-container">
            <p class="question-text">{{ currentQuestion.question }}</p>
            <div class="sequence-cards">
              <button 
                v-for="(item, sIdx) in currentQuestion.sequence" 
                :key="sIdx" 
                class="seq-card"
                :class="{ 'selected': userAnswers[currentQuestion.id] === sIdx }"
                @click="selectAnswer(currentQuestion.id, sIdx)"
              >
                {{ item }}
              </button>
            </div>
          </div>

          <div v-if="currentQuestion.type !== 'sequence'" class="options-grid" :class="{'options-inline': currentQuestion.type === 'matching'}">
            <button 
              v-for="(opt, oIndex) in currentQuestion.options" 
              :key="oIndex"
              class="option-btn"
              :class="{ 'selected': userAnswers[currentQuestion.id] === oIndex }"
              @click="selectAnswer(currentQuestion.id, oIndex)"
            >
              {{ opt }}
            </button>
          </div>
        </div>
      </div>

      <div class="navigation-actions">
        <button @click="prevQuestion" class="btn btn-outline" :disabled="currentIndex === 0">
          Kembali
        </button>
        <button 
          @click="nextQuestion" 
          class="btn btn-primary"
          :disabled="userAnswers[currentQuestion.id] === undefined"
        >
          {{ currentIndex === questions.length - 1 ? 'Selesai Subtes' : 'Selanjutnya' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.test-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.timer-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--border);
  padding: 0.5rem 1rem;
  border-radius: 99px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  color: var(--text-main);
}

.timer-badge.warning {
  background: #fee2e2;
  color: var(--danger);
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.progress-container {
  margin-bottom: 2rem;
  background: var(--border);
  border-radius: 99px;
  height: 0.5rem;
  position: relative;
}

.progress-bar {
  height: 100%;
  background: var(--primary);
  border-radius: 99px;
  transition: width 0.3s ease;
}

.progress-text {
  position: absolute;
  right: 0;
  top: -1.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-light);
}

.question-container {
  min-height: 400px;
}

.question-item {
  background: var(--surface);
  padding: 2rem;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
}

.navigation-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
  gap: 1rem;
}

.navigation-actions button {
  flex: 1;
}

.question-text {
  font-size: 1.1rem;
  color: var(--text-main);
  margin-bottom: 1rem;
}

.options-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
}

@media (min-width: 640px) {
  .options-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.option-btn {
  padding: 1rem;
  border: 2px solid var(--border);
  background: var(--surface);
  border-radius: var(--radius);
  cursor: pointer;
  text-align: left;
  font-size: 1rem;
  transition: all 0.2s;
  color: var(--text-main);
}

.option-btn:hover {
  border-color: var(--primary);
  background: var(--border);
}

.option-btn.selected {
  border-color: var(--primary);
  background: rgba(37, 99, 235, 0.05);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
}

.w-full {
  width: 100%;
}

.mt-4 {
  margin-top: 1rem;
}

/* Custom Question Types Styling */
.question-number {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.whitespace-pre-wrap {
  white-space: pre-wrap;
  line-height: 1.6;
}

.matching-container {
  margin-bottom: 1.5rem;
}

.matching-rows {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  background: var(--background);
  padding: 1.5rem;
  border-radius: var(--radius);
  border: 1px dashed var(--border);
}

.row {
  display: flex;
  gap: 1rem;
}

.char-box {
  font-size: 2rem;
  font-weight: 700;
  width: 3.5rem;
  text-align: center;
  font-family: 'Courier New', Courier, monospace;
}

.bottom-row {
  margin-top: 0.5rem;
}

.sequence-container {
  margin-bottom: 1.5rem;
}

.sequence-cards {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.seq-card {
  font-size: 1.5rem;
  font-weight: 700;
  background: var(--surface);
  border: 2px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.5rem;
  box-shadow: var(--shadow);
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-main);
}

.seq-card:hover {
  border-color: var(--primary);
  background: var(--border);
  transform: translateY(-2px);
}

.seq-card.selected {
  border-color: var(--primary);
  background: rgba(37, 99, 235, 0.05);
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.2);
}

.options-inline {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.options-inline .option-btn {
  text-align: center;
  min-width: 4rem;
}
</style>
