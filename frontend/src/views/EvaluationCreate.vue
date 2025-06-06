<template>
     <Header /> 

  <div class="p-6 max-w-2xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">
      Cadastro de Avaliação - Turma {{ courseName || "Carregando..." }}
    </h1>

    <!-- Formulário -->
    <form @submit.prevent="createEvaluation" class="space-y-4">
      <!-- Título da Avaliação -->
      <div class="form-control">
        <label class="label">Título da Avaliação</label>
        <input v-model="evaluation.title" type="text" class="input input-bordered w-full" required>
      </div>

      <!-- Linha com dois campos lado a lado -->
      <div class="grid grid-cols-2 gap-4">
        <!-- Data -->
        <div class="form-control">
          <label class="label">Data</label>
          <input v-model="evaluation.date" type="date" class="input input-bordered w-full" required>
        </div>

        <!-- Número de Questões -->
        <div class="form-control">
          <label class="label">Número de Questões</label>
          <input v-model.number="evaluation.numQuestions" type="number" class="input input-bordered w-full" required>
        </div>
      </div>

      <!-- Seção: Exercícios -->
      <div class="form-control">
        <label class="label">Selecione os Exercícios:</label>
        <div v-if="loadingCourseworks" class="flex justify-center">
          <span class="loading loading-spinner loading-md"></span>
        </div>
        <div v-else-if="courseworks.length" class="grid grid-cols-1 gap-2">
          <label v-for="cw in courseworks" :key="cw.id" class="flex items-center gap-2 p-2 bg-base-200 rounded">
            <input type="checkbox" :value="cw.id" v-model="evaluation.selectedCourseworks"
              class="checkbox checkbox-primary">
            <span>{{ cw.title }}</span>
          </label>
        </div>
        <p v-else class="text-gray-500">Nenhum exercício encontrado.</p>
      </div>

      <!-- Lista de Alunos -->
      <div class="form-control">
        <label class="label">Selecione os Alunos:</label>
        <div class="flex items-center mb-2">
          <input type="checkbox" :checked="isAllSelected" @change="toggleSelectAllStudents"
            class="checkbox checkbox-primary mr-2" />
          <span>Selecionar Todos</span>
        </div>
        <div v-if="loadingStudents" class="flex justify-center">
          <span class="loading loading-spinner loading-md"></span>
        </div>
        <div v-else-if="students.length" class="grid grid-cols-1 gap-2">
          <div v-for="student in students" :key="student.id" class="flex items-center">
            <input type="checkbox" :value="student.id" v-model="evaluation.selectedStudents" class="mr-2">
            <span>{{ student.name }}</span>
          </div>
        </div>
        <p v-else class="text-gray-500">Nenhum aluno encontrado.</p>
      </div>

      <!-- Botões -->
      <div class="flex justify-between">
        <button @click="$router.push(`/turma/${courseId}/dashboard`)" type="button"
          class="btn bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 transition">
          ← Voltar
        </button>
        <button type="submit" class="btn btn-primary w-auto">
          Criar Avaliação
        </button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import Header from "./Header.vue"; // 🔹 Importando o Header
import type { Evaluation, 
              Course, 
              Coursework, 
              Student,
              StudentExam, 
              StudentExamQuestion, 
              ConjuntoQuestoes } from "../types/types"; // Importando os tipos corretos


// ------------------------------------------------------
// defineComponent
// ------------------------------------------------------
export default defineComponent({
  name: "EvaluationCreate",
  components: { Header }, // 🔹 Registrando o Header
  setup() {
    const route = useRoute();
    const router = useRouter();
    const courseId = route.params.courseId as string;
    const courseName = ref<string | null>(null);
    const courseworks = ref<Coursework[]>([]);
    const students = ref<Student[]>([]);
    const loadingCourseworks = ref<boolean>(true);
    const loadingStudents = ref<boolean>(true);
    const selectAllStudents = ref<boolean>(false);

    const evaluation = ref<Evaluation>({
      id: "", // ID gerado no backend
      course: {} as Course, // Curso será preenchido ao buscar os dados
      title: "",
      date: new Date().toISOString().split("T")[0], // Data atual como padrão
      numQuestions: 1,
      selectedCourseworks: [],
      selectedStudents: [],
      studentExams: [],
    });

    const theme = ref(localStorage.getItem("theme") || "system");

const themeClass = computed(() => {
  const currentTheme = theme.value === "system"
    ? (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light")
    : theme.value;

  return currentTheme === "dark" ? "bg-gray-900 text-white" : "bg-gray-100 text-black";
});



// 🔹 Função para carregar os dados do localStorage ou da API
const loadCourseData = async () => {
      const storedData = localStorage.getItem(`turma_${courseId}`);
      
      if (storedData) {
        console.log(`📌 Dados da turma ${courseId} carregados do localStorage.`);
        const parsedData = JSON.parse(storedData);
        courseworks.value = parsedData.courseworks || [];
        students.value = parsedData.students || [];
        courseName.value = parsedData.courseName || "Nome não disponível";
        loadingCourseworks.value = false;
        loadingStudents.value = false;
      } else {
        console.log(`🔍 Nenhum dado salvo para turma ${courseId}. Buscando via API...`);
        await fetchCourseDetails();
        await fetchCourseworks();
        await fetchStudents();

        // 🔹 Salvar os dados no localStorage para acessos futuros
        localStorage.setItem(`turma_${courseId}`, JSON.stringify({
          courseworks: courseworks.value,
          students: students.value,
          courseName: courseName.value
        }));
        console.log(`✅ Dados da turma ${courseId} salvos no localStorage.`);
      }
    };


    // ------------------------------------------------------
    // 🔹 Função principal: Criar a avaliação e gerar as provas dos alunos
    const createEvaluation = async () => {
      console.log("🟡 Criando avaliação...");

      if (evaluation.value.numQuestions < 1) {
        alert("O número de questões deve ser maior que 0.");
        return;
      }

      if (evaluation.value.selectedCourseworks.length === 0) {
        alert("Selecione pelo menos um exercício.");
        return;
      }

      if (evaluation.value.selectedStudents.length === 0) {
        alert("Selecione pelo menos um aluno.");
        return;
      }

       
      // ✅ Atualiza `selectedStudents` para armazenar objetos `Student`, não apenas IDs
      const selectedStudentIds = evaluation.value.selectedStudents as unknown as string[];
        evaluation.value.selectedStudents = students.value.filter((student: Student) =>
          selectedStudentIds.includes(student.id) // Comparando os IDs
        );

      // 🔹 Gerar as provas dos alunos
      try {
          evaluation.value.studentExams = await generateStudentExams();
          if (!evaluation.value.studentExams || evaluation.value.studentExams.length === 0) {
              throw new Error("Erro ao gerar as provas dos alunos.");
          }
      } catch (error) {
          console.error("❌ Erro ao gerar provas:", error);
          alert("Ocorreu um erro ao gerar as provas dos alunos. Tente novamente.");
          return;
      }

      // 🔹 Criar um identificador único para a avaliação
      const evaluationId = `eval-${new Date().getTime()}`;

       // 🔹 Garante que `course` está preenchido corretamente
    if (!evaluation.value.course || !evaluation.value.course.id) {
        console.warn("⚠️ Curso não está definido corretamente. Adicionando manualmente...");
        evaluation.value.course = {
            id: courseId,
            name: courseName.value || "Curso Indefinido",
            section: "",
            description: "",
            topics: [],
            coursework: [],
        };
    }

      // 🔹 Criar objeto da avaliação final
    const finalEvaluation = {
        id: evaluationId, 
        course: evaluation.value.course,
        title: evaluation.value.title,
        date: evaluation.value.date,
        numQuestions: evaluation.value.numQuestions,
        selectedCourseworks: evaluation.value.selectedCourseworks,
        selectedStudents: evaluation.value.selectedStudents,
        studentExams: evaluation.value.studentExams,  // 🔹 Provas geradas para cada aluno
    };

      console.log("✅ Avaliação final antes de salvar:", finalEvaluation);

       // 🔹 Recuperar avaliações existentes no localStorage
      const existingEvaluations = JSON.parse(localStorage.getItem("evaluations") || "[]");

      // 🔹 Adicionar a nova avaliação à lista
      localStorage.setItem("evaluations", JSON.stringify([...existingEvaluations, finalEvaluation]));


      //localStorage.setItem("evaluationData", JSON.stringify(finalEvaluation));
      router.push(`/evaluation-result/${evaluationId}`);
    };

    // ------------------------------------------------------
// 🔹 Gera as provas de cada estudante
const generateStudentExams = async (): Promise<StudentExam[]> => {
  const studentExams: StudentExam[] = [];

  for (const student of evaluation.value.selectedStudents as Student[]) {
    const studentExam: StudentExam = { 
      studentId: student.id, // ✅ Armazena o ID do estudante
      questions: [] 
    };

    for (let i = 0; i < evaluation.value.numQuestions; i++) {
      const question = await generateStudentExamQuestion(student.id); // ✅ Passa o ID corretamente
      if (question) studentExam.questions.push(question);
    }

    studentExams.push(studentExam);
  }

  return studentExams;
};

    // ------------------------------------------------------
    // 🔹 Gera uma questão para o aluno
    const generateStudentExamQuestion = async (studentId: string): Promise<StudentExamQuestion | null> => {
      console.info(`🔹 Gerando questão para aluno ${studentId}`);

      
      const randomCourseworkId =
        evaluation.value.selectedCourseworks[
        Math.floor(Math.random() * evaluation.value.selectedCourseworks.length)
        ];

        console.info(`📌 Coursework selecionado: ${randomCourseworkId}`);

      const submissionId = await fetchSubmissionId(courseId, randomCourseworkId, studentId);
      if (!submissionId) {
        console.warn(`⚠️ Nenhuma submissão encontrada para aluno ${studentId} em coursework ${randomCourseworkId}`);
        return null;
      }

      console.info(`📥 Submissão encontrada: ${submissionId}`);

      const sourceCode = await fetchRandomSourceCode(courseId, randomCourseworkId, submissionId, studentId);
      const subQuestions = await generateSubQuestions(sourceCode);


      console.info(`✅ Questão gerada para aluno ${studentId}`);
      return {
        studentSubmissionId: submissionId,
        sourceCode,
        subQuestions,
      };
    };

    // ------------------------------------------------------
    // 🔹 Obtém o submissionId do aluno
    const fetchSubmissionId = async (courseId: string, courseworkId: string, studentId: string): Promise<string | null> => {
      const token = localStorage.getItem("token");
      const response = await fetch(
        `http://localhost:8000/classroom/curso/${courseId}/trabalho/${courseworkId}/submissoes`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (!response.ok) return null;
      const data = await response.json();
      const submission = data.submissoes.find((s: any) => s.userId === studentId);
      return submission ? submission.id : null;
    };


    // ------------------------------------------------------
// 🔹 Obtém um código-fonte aleatório dos anexos de uma submissão
const fetchRandomSourceCode = async (
  courseId: string,
  courseworkId: string,
  submissionId: string,
  studentId: string
): Promise<string> => {
  console.log(`🔍 Buscando código-fonte para submissão ID: ${submissionId}`);

  try {
    const token = localStorage.getItem("token");

    // 🔹 1. Buscar os anexos da submissão
    const response = await fetch(
      `http://localhost:8000/classroom/curso/${courseId}/trabalho/${courseworkId}/submissao/${submissionId}/arquivos`,
      { headers: { Authorization: `Bearer ${token}` } }
    );

    if (!response.ok) {
      console.warn(`⚠️ Erro ao buscar anexos para submissão ${submissionId}`);
      return "Erro ao obter código-fonte";
    }

    const attachments = await response.json();

    if (!attachments || attachments.length === 0) {
      console.warn(`⚠️ Nenhum anexo encontrado para submissão ${submissionId}`);
      return "Erro ao obter código-fonte";
    }

    // 🔹 2. Escolher um arquivo aleatório entre os anexos disponíveis
    const randomAttachment = attachments[Math.floor(Math.random() * attachments.length)];
    console.log(`📥 Arquivo selecionado: ${randomAttachment.name} (ID: ${randomAttachment.id})`);

    // 🔹 3. Baixar o conteúdo do arquivo pelo backend
    return await fetchFileContent(randomAttachment.id);
  } catch (error) {
    console.error("❌ Erro ao buscar código-fonte:", error);
    return "Erro ao obter código-fonte";
  }
};

// ------------------------------------------------------
// 🔹 Função para buscar o conteúdo do arquivo via backend
const fetchFileContent = async (fileId: string): Promise<string> => {
  try {
    const token = localStorage.getItem("token");
    
    const response = await fetch(
      `http://localhost:8000/classroom/arquivo/${fileId}/conteudo`,
      { headers: { Authorization: `Bearer ${token}` } }
    );

    if (!response.ok) {
      console.warn(`⚠️ Erro ao baixar conteúdo do arquivo ID: ${fileId}`);
      return "Erro ao obter código-fonte";
    }

    const content = await response.text();
    console.log(`✅ Conteúdo do arquivo (${fileId}) recebido com sucesso.`);
    return content;
  } catch (error) {
    console.error("❌ Erro ao baixar conteúdo do arquivo:", error);
    return "Erro ao obter código-fonte";
  }
};

    // ------------------------------------------------------ 
    const fetchSourceCode = async (fileId: string, token: string): Promise<string> => {
  try {
    // ✅ Construindo URL correta para baixar o arquivo diretamente do Google Drive
    const fileUrl = `https://www.googleapis.com/drive/v3/files/${fileId}?alt=media`;

    const response = await fetch(fileUrl, {
      headers: { Authorization: `Bearer ${token}` }, // ✅ Adiciona o token do Google Drive
    });

    if (!response.ok) {
      console.warn(`⚠️ Erro ao baixar código-fonte do arquivo ${fileId}`);
      return "Erro ao obter código-fonte";
    }

    const textContent = await response.text(); // ✅ Pegamos o conteúdo UMA VEZ
    console.log(`📄 Conteúdo do arquivo baixado:\n${textContent}`);

    return textContent;
  } catch (error) {
    console.error("❌ Erro ao buscar código-fonte:", error);
    return "Erro ao obter código-fonte";
  }
};

    // ------------------------------------------------------
// 🔹 Envia o código-fonte para OpenAI e gera as subquestões
const generateSubQuestions = async (sourceCode: string): Promise<ConjuntoQuestoes> => {
  try {
    const response = await fetch("http://localhost:8000/questions/gerar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sourceCode }),
    });

    if (!response.ok) {
      console.error("❌ Erro ao gerar subquestões:", await response.text());
      throw new Error("Falha ao gerar subquestões.");
    }

    // ✅ O backend já retorna um objeto estruturado, então apenas fazemos o parsing corretamente
    const subQuestions: ConjuntoQuestoes = await response.json();

    console.log("✅ Subquestões geradas:", subQuestions);
    return subQuestions;
  } catch (error) {
    console.error("❌ Erro ao gerar subquestões:", error);
    return {
      objetiva: {
        enunciado: "",
        alternativa_a: "",
        alternativa_b: "",
        alternativa_c: "",
        alternativa_d: "",
        alternativa_e: "",
        resposta_correta: "a",
      },
      vf: {
        enunciado: "",
        resposta_correta: "V",
      },
      subjetiva: {
        enunciado: "",
        resposta_correta: "",
      },
    };
  }
};

// ------------------------------------------------------
    // Busca os informacoes do curso.
    const fetchCourseDetails = async () => {
  try {
    const token = localStorage.getItem("token");
    const response = await fetch(`http://localhost:8000/classroom/curso/${courseId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) {
      throw new Error(`Erro ao buscar detalhes do curso: ${response.statusText}`);
    }

    const data = await response.json();
    
    evaluation.value.course = {
      id: data.id,
      name: data.name,
      section: data.section,
      description: data.description,
      topics: data.topics ?? [], // Garante que sempre seja um array
      coursework: data.coursework ?? [] // Garante que sempre seja um array
    };

    courseName.value = data.name; // Atualiza o nome para exibição
  } catch (error) {
    console.error("❌ Erro ao buscar detalhes do curso:", error);
  }
};

    // ------------------------------------------------------
    // Busca os exercícios (trabalhos) do curso.
    const fetchCourseworks = async () => {
      const token = localStorage.getItem("token");
      const response = await fetch(`http://localhost:8000/classroom/curso/${courseId}/trabalhos`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      courseworks.value = data.trabalhos ?? [];
      loadingCourseworks.value = false;
    };

 // ------------------------------------------------------
    // Busca os alunos do curso.
   // ------------------------------------------------------
// 🔹 Busca os alunos do curso
const fetchStudents = async () => {
  try {
    const token = localStorage.getItem("token");
    const response = await fetch(`http://localhost:8000/classroom/curso/${courseId}/alunos`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) {
      throw new Error(`Erro na requisição: ${response.statusText}`);
    }

    const data = await response.json();
    
    // ✅ Agora acessamos corretamente `data.alunos`
    if (!Array.isArray(data.alunos)) {
      throw new Error("Resposta inesperada do backend: 'alunos' não é um array.");
    }

    students.value = data.alunos
      .map((s: any) => ({
        id: s.id,  // ✅ Agora usamos `id`, conforme o backend
        name: s.name,  // ✅ Nome atualizado para refletir o backend
        email: s.email, 
        photoUrl: s.foto_url, 
      }))
      .sort((a, b) => a.name.localeCompare(b.name, "pt-BR")); // 🔹 Ordenação alfabética;

    loadingStudents.value = false;
  } catch (error) {
    console.error("❌ Erro ao buscar alunos:", error);
    loadingStudents.value = false;
  }
};


    const isAllSelected = computed(() => {
      return students.value.length > 0 && 
            evaluation.value.selectedStudents.length === students.value.length;
    });

    const toggleSelectAllStudents = () => {
      selectAllStudents.value = !selectAllStudents.value;
      evaluation.value.selectedStudents = selectAllStudents.value 
        ? [...students.value]  // ✅ Agora armazena os objetos completos, não apenas IDs
        : [];
    };

    // ------------------------------------------------------
    onMounted(() => {
      loadCourseData();
      // fetchCourseDetails();
      // fetchCourseworks();
      // fetchStudents();
    });


    return {
      courseId,
      courseName,
      courseworks,
      students,
      loadingCourseworks,
      loadingStudents,
      evaluation,
      createEvaluation,
      isAllSelected,
      toggleSelectAllStudents,
      themeClass,
    };
  },
});

</script>
