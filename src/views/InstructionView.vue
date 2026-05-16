<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { SUBTESTS } from '../data/subtests'
import { ArrowRight, ChevronLeft } from '@lucide/vue'

const route = useRoute()
const router = useRouter()

const subtestId = computed(() => parseInt(route.params.id))
const subtest = computed(() => SUBTESTS.find(s => s.id === subtestId.value))

const startSubtest = () => {
  router.push(`/test/${subtestId.value}`)
}

const goBack = () => {
  if (subtestId.value > 1) {
    router.push(`/instruction/${subtestId.value - 1}`)
  } else {
    router.push('/')
  }
}

// Get image URL
const getImageUrl = (name) => {
  return new URL(`../assets/images/${name}`, import.meta.url).href
}
</script>

<template>
  <div class="container animate-fade-in" v-if="subtest">
    <div class="card">
      <div class="header">
        <button @click="goBack" class="btn-back">
          <ChevronLeft :size="20" />
          Kembali
        </button>
        <span class="step-indicator">Subtes {{ subtestId }} dari 6</span>
      </div>

      <h2>{{ subtest.title }}</h2>
      <p>{{ subtest.description }}</p>

      <div class="instruction-image-container">
        <img :src="getImageUrl(subtest.instructionImage)" :alt="subtest.title">
      </div>

      <div class="actions">
        <button @click="startSubtest" class="btn btn-primary w-full">
          Mulai Subtes
          <ArrowRight :size="20" />
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-weight: 500;
  transition: color 0.2s;
  padding: 0;
}

.btn-back:hover {
  color: var(--primary);
}

.step-indicator {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--primary);
  background: rgba(37, 99, 235, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 99px;
}

.w-full {
  width: 100%;
}

.actions {
  margin-top: 1rem;
}
</style>
