<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTestStore } from '../store/testStore'
import { Line } from 'vue-chartjs'
import { 
  Chart as ChartJS, 
  Title, 
  Tooltip, 
  Legend, 
  LineElement, 
  LinearScale, 
  PointElement, 
  CategoryScale 
} from 'chart.js'
import { Home, Trash2, ArrowLeft } from '@lucide/vue'

ChartJS.register(
  Title, 
  Tooltip, 
  Legend, 
  LineElement, 
  LinearScale, 
  PointElement, 
  CategoryScale
)

const router = useRouter()
const store = useTestStore()

const history = computed(() => store.history)

const chartData = computed(() => {
  const sortedHistory = [...history.value].sort((a, b) => new Date(a.date) - new Date(b.date))
  const isDark = store.theme === 'dark'
  const primaryColor = isDark ? '#60a5fa' : '#2563eb'
  const areaColor = isDark ? 'rgba(96, 165, 250, 0.1)' : 'rgba(37, 99, 235, 0.1)'
  
  return {
    labels: sortedHistory.map(h => new Date(h.date).toLocaleDateString('id-ID', { day: '2-digit', month: 'short' })),
    datasets: [
      {
        label: 'Total Skor',
        borderColor: primaryColor,
        backgroundColor: areaColor,
        data: sortedHistory.map(h => h.totalScore),
        fill: true,
        tension: 0.4
      }
    ]
  }
})

const chartOptions = computed(() => {
  const isDark = store.theme === 'dark'
  const textColor = isDark ? '#94a3b8' : '#64748b'
  const gridColor = isDark ? '#334155' : '#e2e8f0'

  return {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        suggestedMax: 600,
        grid: { color: gridColor },
        ticks: { color: textColor }
      },
      x: {
        grid: { display: false },
        ticks: { color: textColor }
      }
    },
    plugins: {
      legend: {
        labels: { color: textColor }
      }
    }
  }
})

const clearHistory = () => {
  if (confirm('Apakah Anda yakin ingin menghapus semua riwayat statistik?')) {
    localStorage.removeItem('learning_agility_history')
    store.history = []
  }
}

const goHome = () => {
  router.push('/')
}
</script>

<template>
  <div class="container animate-fade-in">
    <div class="card">
      <div class="header">
        <button @click="goHome" class="btn-back">
          <ArrowLeft :size="20" />
          Kembali
        </button>
        <h2>Statistik Latihan</h2>
      </div>

      <div v-if="history.length > 0">
        <p>Grafik di bawah menunjukkan tren perkembangan skor total Anda dari waktu ke waktu.</p>
        
        <div class="chart-container">
          <Line :data="chartData" :options="chartOptions" />
        </div>

        <div class="stats-footer">
          <button @click="clearHistory" class="btn-clear">
            <Trash2 :size="16" />
            Hapus Riwayat
          </button>
        </div>
      </div>

      <div v-else class="empty-state">
        <div class="empty-icon">📈</div>
        <h3>Belum Ada Riwayat</h3>
        <p>Selesaikan setidaknya satu tes untuk melihat statistik latihan Anda di sini.</p>
        <button @click="router.push('/instruction/1')" class="btn btn-primary">
          Mulai Tes Pertama
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.btn-back {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 50%;
  transition: background 0.2s;
}

.btn-back:hover {
  background: var(--border);
  color: var(--primary);
}

.header h2 {
  margin-bottom: 0;
}

.chart-container {
  height: 300px;
  margin: 2rem 0;
}

.stats-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn-clear {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 0.875rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem;
  border-radius: var(--radius);
  transition: all 0.2s;
}

.btn-clear:hover {
  color: var(--danger);
  background: rgba(239, 68, 68, 0.1);
}

.empty-state {
  text-align: center;
  padding: 3rem 0;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin-bottom: 0.5rem;
}
</style>
