<template>
    <Header />
  
    <div class="p-6 max-w-4xl mx-auto">
      <div class="flex justify-between mb-4">
        <!-- 🔹 Botão Voltar -->
        <button @click="goBack" class="btn bg-gray-200  text-gray-700">
          ← Voltar
        </button>
      </div>
  
      <!-- 🔹 Exibir mensagens de erro ou carregamento -->
      <div v-if="loading" class="text-center text-gray-800">Carregando...</div>
      <div v-else-if="!course" class="text-center text-gray-800">Turma não encontrada.</div>
  
      <div v-else>
        <!-- 🔹 Exibir dados da turma -->
        <h2 class="text-2xl font-semibold text-base-content">{{ course.name }}</h2>
        <!-- <p class="text-gray-600">Seção: {{ course.section || "Sem seção" }}</p> -->
  
        <!-- 🔹 Botão para Criar Nova Avaliação -->
        <div class="mt-4">
          <button @click="goToCreateEvaluation(course.id)" class="btn btn-primary">
            Criar Nova Avaliação
          </button>
        </div>
  
        <!-- 🔹 Lista de avaliações -->
        <h3 class="text-lg font-semibold mt-6">Avaliações Criadas</h3>
        <div v-if="evaluations.length === 0" class="text-gray-500 mt-2">
          Nenhuma avaliação encontrada.
        </div>
  
        <ul v-else class="mt-4 space-y-4">
          <li v-for="evaluation in evaluations" :key="evaluation.id"
              class="p-4 bg-gray-200 shadow-md rounded-lg flex justify-between items-center">
            <div>
              <h4 class="text-gray-900 font-medium">{{ evaluation.title }}</h4>
              <p class="text-gray-600 text-sm">Data: {{ evaluation.date }}</p>
            </div>
            <div class="flex space-x-2">
              <button @click="viewEvaluation(evaluation.id)" class="btn btn-secondary">Ver</button>
              <button @click="deleteEvaluation(evaluation.id)" class="btn btn-error">Excluir</button>
            </div>
          </li>

      

        </ul>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted, computed } from "vue";
  import { useRouter, useRoute } from "vue-router";
  import type { Evaluation, Course } from "../types/types";
  import Header from "./Header.vue";
  
  export default defineComponent({
    name: "TurmaDashboard",
    components: { Header },
    setup() {
      const router = useRouter();
      const route = useRoute();
      const loading = ref(true);
      const course = ref<Course | null>(null);
      const evaluations = ref<Evaluation[]>([]);
    const theme = ref(localStorage.getItem("theme") || "light");
  

    const loadData = () => {
    const courseId = route.params.courseId as string;
    console.log("📌 courseId recebido da URL:", courseId);

    // Recuperar cursos do localStorage
    const storedCourses = localStorage.getItem("courses");
    console.log("📌 Cursos no localStorage:", storedCourses ? JSON.parse(storedCourses) : "Nenhum curso salvo");

    if (storedCourses) {
        const courses: Course[] = JSON.parse(storedCourses);
        course.value = courses.find(c => c.id === courseId) || null;
    }

    if (!course.value) {
        console.warn("⚠️ Turma não encontrada. Verifique se courseId corresponde a um ID válido.");
        loading.value = false;
        return;
    }

    console.log("✅ Turma carregada corretamente:", course.value);

    // Recuperar avaliações do localStorage
    const storedEvaluations = localStorage.getItem("evaluations");
    if (storedEvaluations) {
        const allEvaluations: Evaluation[] = JSON.parse(storedEvaluations);
        evaluations.value = allEvaluations.filter(e => e.course.id === courseId);
    }

    console.log("📌 Avaliações carregadas:", evaluations.value);
    loading.value = false;
};

// 🔹 Função para remover uma avaliação do localStorage
const deleteEvaluation = (evaluationId: string) => {
    if (!confirm("Tem certeza que deseja excluir esta avaliação?")) return;

    const storedEvaluations = localStorage.getItem("evaluations");
    if (storedEvaluations) {
        let allEvaluations: Evaluation[] = JSON.parse(storedEvaluations);
        allEvaluations = allEvaluations.filter(e => e.id !== evaluationId);
        localStorage.setItem("evaluations", JSON.stringify(allEvaluations));

        // Atualiza a lista de avaliações na UI
        evaluations.value = allEvaluations.filter(e => e.course.id === course.value?.id);
    }
};
  
      // 🔹 Função para visualizar uma avaliação
      const viewEvaluation = (evaluationId: string) => {
        router.push(`/evaluation-result/${evaluationId}`);
      };
  
      // 🔹 Função para criar uma nova avaliação
      const goToCreateEvaluation = (courseId: string) => {
        router.push(`/turma/${courseId}/avaliacao/criar`);
      };
  
      // 🔹 Função para voltar ao dashboard do professor
      const goBack = () => {
        router.push("/dashboard");
      };
  
      onMounted(() => {
        loadData();
      });
  
      return {
        loading,
        course,
        evaluations,
        deleteEvaluation,
        viewEvaluation,
        goToCreateEvaluation,
        goBack
      };
    }
  });
  </script>