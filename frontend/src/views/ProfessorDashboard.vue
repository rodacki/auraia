
<template>
  <Header /> 


  <div class="p-4 max-w-3xl mx-auto">
  <!-- 🔹 Container flexível para alinhar h1 e botão na mesma linha -->
  <div class="flex items-center justify-between mb-4">
    <h1 class="text-3xl font-bold">Dashboard do Professor</h1>
    <button @click="fetchCourses(true)" class="btn btn-secondary">
      🔄 Atualizar Turmas
    </button>
  </div>

  <!-- <div class="p-4 max-w-3xl mx-auto">
    <h1 class="text-3xl font-bold mb-4">Dashboard do Professor</h1>

    <button @click="fetchCourses(true)" class="btn btn-secondary mt-4">
            🔄 Atualizar Turmas
          </button> -->

    <!-- Exibir mensagem de carregamento -->
    <div v-if="loading" class="flex justify-center items-center h-32">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <!-- Exibir erro caso ocorra -->
    <p v-else-if="error" class="text-red-500 text-center">Erro ao carregar turmas. Tente novamente.</p>

    <!-- Exibir lista de turmas -->
    <div v-else-if="courses.length > 0" class="space-y-4">  
      <div v-for="course in courses" :key="course.id" class="p-4 bg-white shadow-md rounded-lg border flex justify-between items-center">
        <!-- Nome da turma -->
        <h2 class="text-lg font-semibold text-gray-800">{{ course.name }}</h2>

        
        <div class="mt-4 flex justify-end space-x-2">
          <button @click="goToTurmaDashboard(course.id)" class="btn btn-primary">
            Entrar
          </button>
          
        </div>

        <!-- Botões de ação -->
        <!-- <div class="flex space-x-2">
          <button @click="goToEvaluations(course.id)" class="btn btn-primary">Entrar</button>
        </div> -->
      </div>
    </div>

    <!-- Caso não haja turmas -->
    <p v-else class="text-center text-gray-500">Nenhuma turma encontrada.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Header from "./Header.vue"; // 🔹 Importando o Header
import type { Course } from "../types/types";


export default defineComponent({
  name: "ProfessorDashboard",
  components: { Header }, // 🔹 Registrando o Header

  setup() {
    const courses = ref<Course[]>([]);
    const loading = ref<boolean>(false);
    const error = ref<boolean>(false);
    const router = useRouter();

    const UPDATE_INTERVAL_MS = 5 * 60 * 1000; // 🔹 5 minutos

    
    const loadCourses = async () => {
      const cachedCourses = localStorage.getItem("courses");

      if (cachedCourses) {
        console.log("📌 Carregando turmas do cache...");
        courses.value = JSON.parse(cachedCourses);
        loading.value = false;
        return;
      }

      console.log("🔍 Nenhuma turma salva. Buscando via API...");

      try {
        const token = localStorage.getItem("token");
        if (!token) {
          console.error("🚨 Token não encontrado.");
          error.value = true;
          loading.value = false;
          return;
        }

        const response = await fetch("http://localhost:8000/classroom/cursos", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          console.error(`🚨 Erro na API (${response.status}):`, await response.text());
          error.value = true;
          loading.value = false;
          return;
        }

        const data = await response.json();
        console.log("✅ Dados das turmas recebidos:", data);

        courses.value = data.cursos ?? [];

        // 🔹 Salvar no LocalStorage para acessos futuros
        localStorage.setItem("courses", JSON.stringify(courses.value));
        console.log("✅ Turmas salvas no LocalStorage.");
      } catch (err) {
        console.error("❌ Erro ao buscar turmas:", err);
        error.value = true;
      } finally {
        loading.value = false;
      }
    };

    
    const fetchCourses = async (forceUpdate = true) => {
    try {
        loading.value = true;
        error.value = false;

        const token = localStorage.getItem("token");
        if (!token) {
            console.error("🚨 Token não encontrado.");
            error.value = true;
            loading.value = false;
            return;
        }

        const storedCourses = localStorage.getItem("courses");
        const lastUpdated = localStorage.getItem("courses_last_updated");

        // 🔹 Converte o timestamp salvo para número
        const lastUpdatedTime = lastUpdated ? parseInt(lastUpdated, 10) : 0;
        const now = Date.now();
        const timeDiff = now - lastUpdatedTime;

        console.log(`📌 Última atualização salva: ${lastUpdatedTime} (${new Date(lastUpdatedTime).toLocaleString()})`);
        console.log(`⏳ Tempo decorrido desde última atualização: ${timeDiff / 1000} segundos`);

        // 🔹 Se os dados foram atualizados recentemente (menos de 5 minutos) e forceUpdate for true, usa localStorage
        if (storedCourses && timeDiff < UPDATE_INTERVAL_MS) {
            console.log("📌 Carregando turmas do localStorage, pois os dados ainda estão atualizados.");
            courses.value = JSON.parse(storedCourses);
            loading.value = false;
            return;
        }

        // 🔹 Se passaram mais de 5 minutos ou se não há dados salvos, buscar na API do Google Classroom
        console.log("🔄 Buscando turmas na API do Google Classroom...");
        const response = await fetch("http://localhost:8000/classroom/cursos", {
            headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
            console.error(`🚨 Erro na API (${response.status}):`, await response.text());
            error.value = true;
            loading.value = false;
            return;
        }

        const data = await response.json();
        const apiCourses = data.cursos ?? [];
        console.log("✅ Turmas recebidas da API:", apiCourses);

        // 🔹 Atualiza o localStorage e a variável reativa
        localStorage.setItem("courses", JSON.stringify(apiCourses));
        localStorage.setItem("courses_last_updated", now.toString());
        console.log(`📌 Turmas atualizadas e salvas no LocalStorage. Nova atualização em ${UPDATE_INTERVAL_MS / 60000} minutos.`);

        courses.value = apiCourses;
    } catch (err) {
        console.error("❌ Erro ao buscar turmas:", err);
        error.value = true;
    } finally {
        loading.value = false;
    }
};

    const goToTurmaDashboard = (courseId: string) => {
      router.push(`/turma/${courseId}/dashboard`);
    };

    onMounted(() => fetchCourses());

    return { courses, loading, error, goToTurmaDashboard, fetchCourses };
  },
});
</script>

