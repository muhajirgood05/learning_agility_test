<script setup>
import { useRouter } from 'vue-router'
import { Play, BarChart2 } from '@lucide/vue'

const router = useRouter()

const startTest = () => {
  router.push('/instruction/1')
}

const viewStats = () => {
  router.push('/statistics')
}
</script>

<template>
  <div class="container animate-fade-in">
    <div class="card text-center">
      <div class="hero-section">
        <div class="logo-container">
          <div class="logo-circle">
            <Play :size="32" color="white" fill="white" />
          </div>
        </div>
        <h1>Learning Agility Test</h1>
        <p>Tingkatkan kelincahan belajar Anda melalui latihan psikotes terstruktur. Pantau perkembangan Anda dengan statistik yang mendalam.</p>
      </div>

      <div class="actions">
        <button @click="startTest" class="btn btn-primary">
          <Play :size="20" />
          Mulai Latihan
        </button>
        <button @click="viewStats" class="btn btn-outline">
          <BarChart2 :size="20" />
          Lihat Statistik
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.text-center {
  text-align: center;
}

.hero-section {
  margin-bottom: 3rem;
}

.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.logo-circle {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, var(--primary), #4f46e5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 25px rgba(37, 99, 235, 0.4);
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 300px;
  margin: 0 auto;
}

@media (min-width: 640px) {
  .actions {
    flex-direction: row;
    max-width: none;
    justify-content: center;
  }
}
</style>
