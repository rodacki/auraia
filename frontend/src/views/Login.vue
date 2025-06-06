

<template>
  <div class="flex items-center justify-center h-screen bg-base-200">
    <div class="card w-96 bg-base-100 shadow-xl p-6">
      <h1 class="text-2xl font-bold text-center mb-4">Login com Google</h1>
      <button 
        @click="login"
        :disabled="isLoading"
        class="btn btn-primary w-full"
      >
        {{ isLoading ? "Entrando..." : "Entrar com Google" }}
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'Login',
  setup() {
    const router = useRouter()
    const isLoading = ref(false)

    const login = async () => {
      if (isLoading.value) return // Evita chamadas múltiplas

      isLoading.value = true
      try {
        const response = await fetch('http://localhost:8000/auth/login')
        const data = await response.json()
        localStorage.setItem('token', data.token)
        router.push({ name: 'ProfessorDashboard' })
      } catch (error) {
        console.error("Erro no login:", error)
      } finally {
        isLoading.value = false
      }
    }

    return { login, isLoading }
  }
})
</script>