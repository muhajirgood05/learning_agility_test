<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTestStore } from '../store/testStore'
import { Radar } from 'vue-chartjs'
import { 
  Chart as ChartJS, 
  Title, 
  Tooltip, 
  Legend, 
  PointElement, 
  LineElement, 
  RadialLinearScale,
  Filler
} from 'chart.js'
import { RefreshCw, Home, Download } from '@lucide/vue'

ChartJS.register(
  Title, 
  Tooltip, 
  Legend, 
  PointElement, 
  LineElement, 
  RadialLinearScale,
  Filler
)

const router = useRouter()
const store = useTestStore()

const session = computed(() => store.currentSession)

const chartData = computed(() => ({
  labels: [
    'Subtes 1', 
    'Subtes 2', 
    'Subtes 3', 
    'Subtes 4', 
    'Subtes 5', 
    'Berhitung'
  ],
  datasets: [
    {
      label: 'Skor Anda',
      backgroundColor: 'rgba(37, 99, 235, 0.2)',
      borderColor: 'rgba(37, 99, 235, 1)',
      pointBackgroundColor: 'rgba(37, 99, 235, 1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(37, 99, 235, 1)',
      data: [
        session.value.scores.subtest1,
        session.value.scores.subtest2,
        session.value.scores.subtest3,
        session.value.scores.subtest4,
        session.value.scores.subtest5,
        session.value.scores.subtest6
      ]
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    r: {
      angleLines: { display: true },
      suggestedMin: 0,
      suggestedMax: 100,
      ticks: { stepSize: 20 }
    }
  },
  plugins: {
    legend: { display: false }
  }
}

const restart = () => {
  store.resetSession()
  router.push('/instruction/1')
}

const goHome = () => {
  router.push('/')
}
</script>

<template>
  <div class="container animate-fade-in">
    <div class="card text-center">
      <h1>Hasil Tes Anda</h1>
      <p>Selamat! Anda telah menyelesaikan seluruh rangkaian Learning Agility Test.</p>

      <div class="score-summary">
        <div class="score-item">
          <span class="label">Total Skor</span>
          <span class="value">{{ session.totalScore }}</span>
        </div>
        <div class="score-item">
          <span class="label">Rata-rata</span>
          <span class="value">{{ Math.round(session.totalScore / 6) }}</span>
        </div>
      </div>

      <div class="chart-container">
        <Radar :data="chartData" :options="chartOptions" />
      </div>

      <div class="actions">
        <button @click="restart" class="btn btn-primary">
          <RefreshCw :size="18" />
          Ulangi Tes
        </button>
        <button @click="goHome" class="btn btn-outline">
          <Home :size="18" />
          Menu Utama
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.text-center {
  text-align: center;
}

.score-summary {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
}

.score-item {
  display: flex;
  flex-direction: column;
}

.score-item .label {
  font-size: 0.875rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.score-item .value {
  font-size: 2rem;
  font-weight: 800;
  color: var(--primary);
}

.chart-container {
  height: 350px;
  margin-bottom: 2rem;
  position: relative;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

@media (max-width: 640px) {
  .actions {
    flex-direction: column;
  }
}
</style>
