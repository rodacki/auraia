// ------------------------------------------------------
// Estruturas de dados
// ------------------------------------------------------


// Questão Objetiva (Múltipla Escolha)
export interface QuestaoObjetiva {
  enunciado: string;
  alternativa_a: string;
  alternativa_b: string;
  alternativa_c: string;
  alternativa_d: string;
  alternativa_e: string;
  resposta_correta: "a" | "b" | "c" | "d" | "e";
}

// Questão de Verdadeiro ou Falso
export interface QuestaoVerdadeiroFalso {
  enunciado: string;
  resposta_correta: "V" | "F";
}

// Questão Subjetiva (Discursiva)
export interface QuestaoSubjetiva {
  enunciado: string;
  resposta_correta?: string; // Opcional
}

// Conjunto de Questões Geradas para um Código-Fonte
export interface ConjuntoQuestoes {
  objetiva: QuestaoObjetiva;
  vf: QuestaoVerdadeiroFalso;
  subjetiva: QuestaoSubjetiva;
}

// Representa um aluno inscrito em um curso
export interface Student {
  id: string; // ID único do aluno no Google Classroom
  name: string; // Nome completo do aluno
  email?: string; // E-mail do aluno (opcional)
  photoUrl?: string; // URL da foto do aluno (opcional)
}

// Representa um arquivo submetido pelo aluno
export interface Attachment {
    id: string; // Identificador único do anexo (arquivo)
    name: string; // Nome do arquivo submetido
    fileUrl: string; // URL para recuperar o arquivo no Google Drive
    mimeType?: string; // Tipo MIME do arquivo (exemplo: "text/x-python", "application/pdf")
  }
  
  // Representa a submissão de um aluno em uma atividade prática (Coursework)
  export interface StudentSubmission {
    id: string; // Identificador único da submissão
    studentId: string; // Identificador único do aluno que fez a submissão
    courseworkId: string; // Identificador da atividade à qual essa submissão pertence
    submissionTime: string; // Data e hora em que a submissão foi realizada (ISO string)
    attachments: Attachment[]; // Lista de arquivos submetidos pelo aluno
    status: string; // Status da submissão ("TURNED_IN", "RETURNED", "DRAFT", etc.)
  }
  
  // Representa uma atividade prática dentro de um curso
  export interface Coursework {
    id: string; // Identificador único da atividade
    title: string; // Título da atividade
    description?: string; // Descrição opcional da atividade
    topicId?: string; // Identificador do tópico ao qual essa atividade pertence
    dueDate?: string; // Data de entrega (ISO string)
    submissions: StudentSubmission[]; // Lista de submissões feitas pelos alunos
  }
  
  // Representa um tópico dentro de um curso
  export interface Topic {
    id: string; // Identificador único do tópico
    name: string; // Nome do tópico
    courseId: string; // Identificador do curso ao qual este tópico pertence
  }
  
  // Representa um curso no Google Classroom
  export interface Course {
    id: string; // Identificador único do curso
    name: string; // Nome do curso
    section?: string; // Seção do curso (exemplo: "Turma A - 2024")
    description?: string; // Descrição opcional do curso
    topics: Topic[]; // Lista de tópicos do curso
    coursework: Coursework[]; // Lista de atividades do curso
  }
  
  // Representa uma questão gerada a partir da submissão do aluno
  export interface StudentExamQuestion {
    studentSubmissionId: string; // ID da submissão usada para gerar as questões
    sourceCode: string; // Código-fonte escolhido aleatoriamente
    subQuestions: ConjuntoQuestoes; // Objeto contendo as subquestões geradas
  }
  
  // Representa a prova completa de um estudante
  export interface StudentExam {
    studentId: string; // ID do estudante que realizará a prova
    questions: StudentExamQuestion[]; // Lista de questões da prova (tamanho = numQuestions da Evaluation)
  }
  
  // Representa uma avaliação criada pelo usuário
  export interface Evaluation {
    id: string; // Identificador único da avaliação (gerado pelo frontend)
    course: Course; // Curso ao qual essa avaliação pertence
    title: string; // Título da avaliação
    date: string; // Data da avaliação (formato ISO)
    numQuestions: number; // Número total de questões na avaliação
    selectedCourseworks: string[]; // Lista de IDs das atividades selecionadas
    selectedStudents: Student[]; // Lista de  alunos selecionados para a avaliacao
    studentExams: StudentExam[]; // Mapeamento de cada estudante para sua prova individual
  }