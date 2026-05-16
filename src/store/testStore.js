import { defineStore } from 'pinia'

export const useTestStore = defineStore('test', {
  state: () => ({
    currentSession: {
      date: null,
      scores: {
        subtest1: 0,
        subtest2: 0,
        subtest3: 0,
        subtest4: 0,
        subtest5: 0,
        subtest6: 0
      },
      totalScore: 0
    },
    history: JSON.parse(localStorage.getItem('learning_agility_history') || '[]')
  }),
  actions: {
    setScore(subtestId, score) {
      this.currentSession.scores[`subtest${subtestId}`] = score
    },
    finishSession() {
      this.currentSession.date = new Date().toISOString()
      this.currentSession.totalScore = Object.values(this.currentSession.scores).reduce((a, b) => a + b, 0)
      
      this.history.push({ ...this.currentSession })
      localStorage.setItem('learning_agility_history', JSON.stringify(this.history))
    },
    resetSession() {
      this.currentSession = {
        date: null,
        scores: {
          subtest1: 0,
          subtest2: 0,
          subtest3: 0,
          subtest4: 0,
          subtest5: 0,
          subtest6: 0
        },
        totalScore: 0
      }
    }
  }
})
