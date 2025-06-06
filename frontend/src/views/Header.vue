
<template>
    <header class="bg-gray-900 text-white py-3 px-6 flex items-center justify-between shadow-md">
      
      <div class="flex items-center space-x-3">
        <img src="../assets/Logo_IFC_vertical_Blumenau.png"
            alt="Logo AuraIA"
            class="h-12 w-auto object-contain" />
        <h1 class="text-lg font-semibold">AuraIA</h1>
      </div>

     
  
      
      <div class="flex items-center space-x-6">
       
        <div class="text-right">
          <p class="font-medium">{{ user.name }}</p>
          <p class="text-sm text-gray-300">{{ user.email }}</p>
        </div>
        
       
        <div class="relative flex items-center bg-gray-800 rounded-lg p-1">
          <button @click="setTheme('light')" :class="theme === 'light' ? 'bg-gray-600' : ''" class="p-2 rounded-lg">
            ☀️
          </button>
          <button @click="setTheme('dark')" :class="theme === 'dark' ? 'bg-gray-600' : ''" class="p-2 rounded-lg">
            🌙
          </button>
          <button @click="setTheme('system')" :class="theme === 'system' ? 'bg-gray-600' : ''" class="p-2 rounded-lg">
            🖥️
          </button>
        </div>
        
        
        <button @click="logout" class="text-red-400 hover:text-red-300">Sair</button>
      </div>
    </header>
  </template> 
  
  <script setup>
  import { ref, onMounted } from 'vue';

  console.log("🔍 Header.vue está sendo carregado!");
  
  const user = ref({
    name: "Paulo Rodacki", // Substituir pelo dado real do backend
    email: "rodacki@gmail.com"
  });
  
  const theme = ref(localStorage.getItem('theme') || 'system');
  
  const setTheme = (newTheme) => {
    theme.value = newTheme;
    localStorage.setItem('theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };
  
  const logout = () => {
    console.log("Usuário deslogado");
    // Aqui você pode redirecionar para a página de login ou limpar o estado de autenticação
  };
  
  onMounted(() => {
    setTheme(theme.value);
    console.log("✅ Header.vue foi montado com sucesso!");
  });
  </script>
  
  <style>
  [data-theme='dark'] {
    background-color: #1a202c;
    color: white;
  }
  [data-theme='light'] {
    background-color: #f9fafb;
    color: black;
  }
  </style>
  