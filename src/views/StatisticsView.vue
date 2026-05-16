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
  
  return {
    labels: sortedHistory.map(h => new Date(h.date).toLocaleDateString('id-ID', { day: '2-digit', month: 'short' })),
    datasets: [
      {
        label: 'Total Skor',
        borderColor: '#2563eb',
        backgroundColor: 'rgba(37, 99, 235, 0.1)',
        data: sortedHistory.map(h => h.totalScore),
        fill: true,
        tension: 0.4
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      suggestedMax: 600
    }
  }
}

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
  background: #f1f5f9;
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
  color: #94a3b8;
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
  background: #fef2f2;
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
