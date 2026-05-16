<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useTestStore } from './store/testStore'
import { Sun, Moon } from '@lucide/vue'

const store = useTestStore()

onMounted(() => {
  store.initTheme()
})
</script>

<template>
  <main>
    <button @click="store.toggleTheme" class="theme-toggle" :title="store.theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
      <Sun v-if="store.theme === 'dark'" :size="20" />
      <Moon v-else :size="20" />
    </button>

    <RouterView v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </RouterView>
  </main>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

#app {
  width: 100%;
}

.theme-toggle {
  position: fixed;
  top: 1.5rem;
  right: 1.5rem;
  z-index: 100;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text-main);
  cursor: pointer;
  box-shadow: var(--shadow);
  transition: all 0.2s;
}

.theme-toggle:hover {
  transform: scale(1.1);
  background: var(--border);
}
</style>
