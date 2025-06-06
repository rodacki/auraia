<template>
  <router-view />
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'

export default defineComponent({
  name: 'App',
  setup() {
    const isDark = ref(false)

    const toggleTheme = () => {
      isDark.value = !isDark.value
      const newTheme = isDark.value ? 'dark' : 'light'
      document.documentElement.setAttribute('data-theme', newTheme)
      localStorage.setItem('theme', newTheme)
      console.log("🔄 Tema alterado para:", newTheme)
    }

    onMounted(() => {
      let savedTheme = localStorage.getItem('theme')

      if (!savedTheme) {
        // Detecta se o sistema operacional está no modo escuro
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches
        savedTheme = prefersDark ? 'dark' : 'light'
        localStorage.setItem('theme', savedTheme)
        console.log("💻 Tema do sistema operacional detectado:", savedTheme)
      }

      isDark.value = savedTheme === 'dark'
      document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')

      console.log("🌓 Tema carregado do localStorage:", savedTheme)
      console.log("🎨 Tema aplicado no document:", document.documentElement.getAttribute('data-theme'))
    })

    return { isDark, toggleTheme }
  }
})
</script>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
