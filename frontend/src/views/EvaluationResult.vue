<script lang="ts">
import { defineComponent, ref, onMounted, nextTick, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import Prism from "prismjs";
import "prismjs/themes/prism-tomorrow.css"; // Escolha o tema de destaque
import "prismjs/components/prism-python"; // Suporte para Python
import type { Evaluation } from "../types/types";
import Header from "./Header.vue"; // 🔹 Importando o Header

export default defineComponent({
    name: "EvaluationResult",
    components: { Header }, // 🔹 Registrando o Header
    setup() {
        const evaluation = ref<Evaluation | null>(null);
        const router = useRouter();
        const route = useRoute();
        const loading = ref(true);

    


        const loadEvaluation = async () => {
    const evaluationId = route.params.evaluationId as string;
    console.log("📌 Evaluation ID recebido:", evaluationId);

    const storedEvaluations = localStorage.getItem("evaluations");
    if (!storedEvaluations) {
        console.error("⚠️ Nenhuma avaliação encontrada no localStorage.");
        loading.value = false;
        return;
    }

    // 🔹 Recupera TODAS as avaliações e faz o parse do JSON
    const allEvaluations: Evaluation[] = JSON.parse(storedEvaluations);

    // 🔹 Busca a avaliação correta pelo ID
    const foundEvaluation = allEvaluations.find(ev => ev.id === evaluationId);

    if (!foundEvaluation) {
        console.error("⚠️ Avaliação não encontrada no localStorage.");
        loading.value = false;
        return;
    }

    evaluation.value = foundEvaluation;
    loading.value = false;

    console.log("✅ Avaliação carregada:", evaluation.value);

    // 🔹 Aguarda o DOM ser atualizado antes de aplicar Prism.js
    await nextTick();
    highlightCode();
};


        // -------------------------------------------
        // 🔹 Aplica o destaque de sintaxe ao código-fonte
        const highlightCode = () => {
            nextTick(() => {
                document.querySelectorAll("pre code").forEach((el) => {
                    Prism.highlightElement(el as HTMLElement);
                });
            });
        };

        // -------------------------------------------
        // 🔹 Monitora mudanças na `evaluation` para reaplicar Prism.js
        watch(evaluation, () => {
            nextTick(() => {
                highlightCode();
            });
        });


    

        const goBack = () => {
    if (evaluation.value?.course?.id) {
        console.log(`🔙 Retornando para /turma/${evaluation.value.course.id}/dashboard`);
        router.push(`/turma/${evaluation.value.course.id}/dashboard`);
    } else {
        console.warn("⚠️ Erro: ID da turma não encontrado, voltando ao dashboard principal.");
        router.push("/dashboard");
    }
};



const formatCode = (code) => {
  if (!code) return "Código-fonte não encontrado.";

  console.log(`Código antes da formatação:\n${code}`);

  // Tenta fazer o parsing da string para remover os escapes extras
  try {
    code = JSON.parse(code);
  } catch (e) {
    console.warn("Não foi possível fazer o parse da string. Usando o conteúdo original.");
  }

  // Remover aspas duplas extras no início e fim (caso existam)
  let cleanedCode = code.replace(/^"|"$/g, "");

  // Expressão regular para capturar strings delimitadas por aspas simples ou duplas
  const stringRegex = /(["'])(?:(?=(\\?))\2.)*?\1/g;
  let parts = [];
  let lastIndex = 0;
  let match;

  // Separa o código em partes: trechos que são strings e trechos que não são
  while ((match = stringRegex.exec(cleanedCode)) !== null) {
    // Parte que não é string
    parts.push({
      text: cleanedCode.slice(lastIndex, match.index),
      isString: false
    });
    // Parte que é string – deixa inalterada para preservar os escapes internos
    parts.push({
      text: match[0],
      isString: true
    });
    lastIndex = match.index + match[0].length;
  }
  // Adiciona a parte final, se houver
  parts.push({
    text: cleanedCode.slice(lastIndex),
    isString: false
  });

  // Processa somente as partes que NÃO são strings
  parts = parts.map(part => {
    if (!part.isString) {
      // Substituir representações de quebras de linha (fora de strings) por quebras reais
      return { ...part, text: part.text.replace(/\\r\\n|\\r|\\n|rn/g, "\n") };
    }
    return part;
  });

  // Reconstrói o código unindo todas as partes
  cleanedCode = parts.map(part => part.text).join("");

  // Dividir o código em linhas
  let lines = cleanedCode.split("\n");

  // Remover linhas vazias no início
  while (lines.length > 0 && lines[0].trim() === "") {
    lines.shift();
  }

  // Remover linhas vazias no final
  while (lines.length > 0 && lines[lines.length - 1].trim() === "") {
    lines.pop();
  }

  // Encontrar a menor indentação
  let minIndent = Math.min(
    ...lines
      .filter(line => line.trim() !== "")
      .map(line => line.match(/^(\s*)/)?.[0].length || 0)
  );

  // Remover a indentação mínima e espaços desnecessários no final de cada linha
  let formattedLines = lines.map(line => line.slice(minIndent).trimEnd());

  // Adicionar uma linha em branco no início (se necessário)
  formattedLines.unshift("");

  let finalCode = formattedLines.join("\n");
  console.log(`Código depois da formatação:\n${finalCode}`);

  return finalCode;
};
        // -------------------------------------------
        // 🔹 Retorna nome do aluno pelo ID
        const getStudentName = (studentId: string) => {
            const student = evaluation.value?.selectedStudents.find(s => s.id === studentId);
            return student ? student.name : "Nome não disponível";
        };


        onMounted(async () => {
            await loadEvaluation();
            //await nextTick();  // Aguarda o DOM ser atualizado
            highlightCode();
        });

        return {
            evaluation,
            goBack,
            loading,
            formatCode,
            getStudentName,
            
        };
    },
});
</script>


<template>
       <Header /> 

    <div class="p-6 max-w-4xl mx-auto">
        <div class="flex justify-between mb-4">
            <button @click="goBack"
                class="btn bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 transition">
                ← Voltar
            </button>
        </div>

        <div v-if="loading" class="text-center text-gray-500">Carregando...</div>
        <div v-else-if="!evaluation" class="text-center text-gray-500">Nenhuma avaliação encontrada.</div>

        <div v-else>
            <h2 class="text-2xl font-semibold text-base-content">{{ evaluation.title }}</h2>
            <p class="text-base-content">Data: {{ evaluation.date }}</p>

            <div v-for="studentExam in evaluation.studentExams" :key="studentExam.studentId"
                class="mt-6 p-5 bg-white shadow-md rounded-lg">
                <h3 class="text-lg font-semibold text-gray-900 border-b pb-2">Aluno: {{
                    getStudentName(studentExam.studentId) }}</h3>

                <div v-for="(question, index) in studentExam.questions" :key="index"
                    class="mt-4 p-4 bg-gray-100 rounded-md shadow-sm">
                    <h4 class="text-gray-800 font-medium">Questão {{ index + 1 }}:</h4>

                    <div class="mt-2">
                        <p class="text-gray-700 text-sm">Código Fonte:</p>


                        <pre
                            class="bg-gray-900 text-green-300 p-4 rounded-lg overflow-auto text-xs leading-tight shadow-sm">
                            <code class="language-python" ref="codeBlocks" v-html="formatCode(question.sourceCode)"></code>
                        </pre>
                    </div>

                    <p class="mt-4 text-gray-700 text-sm">
                        Considerando o código fonte acima, criado por você, responda:
                    </p>

                    <!-- Questão Objetiva -->
                    <div v-if="question.subQuestions.objetiva" class="mt-3">
                        <p class="text-gray-700 font-medium">{{ index + 1 }}.1 Objetiva:</p>
                        <p class="text-gray-700 text-sm">{{ question.subQuestions.objetiva.enunciado }}</p>
                        <div class="ml-4 text-gray-700 text-sm mt-2 space-y-1">
                            <p><strong>a)</strong> {{ question.subQuestions.objetiva.alternativa_a }}</p>
                            <p><strong>b)</strong> {{ question.subQuestions.objetiva.alternativa_b }}</p>
                            <p><strong>c)</strong> {{ question.subQuestions.objetiva.alternativa_c }}</p>
                            <p><strong>d)</strong> {{ question.subQuestions.objetiva.alternativa_d }}</p>
                            <p><strong>e)</strong> {{ question.subQuestions.objetiva.alternativa_e }}</p>
                        </div>
                    </div>

                    <!-- Questão Verdadeiro ou Falso -->
                    <div v-if="question.subQuestions.vf" class="mt-4">
                        <p class="text-gray-700 font-medium">{{ index + 1 }}.2 Verdadeiro ou Falso:</p>
                        <p class="text-gray-700 text-sm">{{ question.subQuestions.vf.enunciado }} (V ou F?)</p>
                    </div>

                    <!-- Questão Subjetiva -->
                    <div v-if="question.subQuestions.subjetiva" class="mt-4">
                        <p class="text-gray-700 font-medium">{{ index + 1 }}.3 Subjetiva:</p>
                        <p class="text-gray-700 text-sm">{{ question.subQuestions.subjetiva.enunciado }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>