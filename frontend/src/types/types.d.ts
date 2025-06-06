export interface QuestaoObjetiva {
    enunciado: string;
    alternativa_a: string;
    alternativa_b: string;
    alternativa_c: string;
    alternativa_d: string;
    alternativa_e: string;
    resposta_correta: "a" | "b" | "c" | "d" | "e";
}
export interface QuestaoVerdadeiroFalso {
    enunciado: string;
    resposta_correta: "V" | "F";
}
export interface QuestaoSubjetiva {
    enunciado: string;
    resposta_correta?: string;
}
export interface ConjuntoQuestoes {
    objetiva: QuestaoObjetiva;
    vf: QuestaoVerdadeiroFalso;
    subjetiva: QuestaoSubjetiva;
}
export interface Student {
    id: string;
    name: string;
    email?: string;
    photoUrl?: string;
}
export interface Attachment {
    id: string;
    name: string;
    fileUrl: string;
    mimeType?: string;
}
export interface StudentSubmission {
    id: string;
    studentId: string;
    courseworkId: string;
    submissionTime: string;
    attachments: Attachment[];
    status: string;
}
export interface Coursework {
    id: string;
    title: string;
    description?: string;
    topicId?: string;
    dueDate?: string;
    submissions: StudentSubmission[];
}
export interface Topic {
    id: string;
    name: string;
    courseId: string;
}
export interface Course {
    id: string;
    name: string;
    section?: string;
    description?: string;
    topics: Topic[];
    coursework: Coursework[];
}
export interface StudentExamQuestion {
    studentSubmissionId: string;
    sourceCode: string;
    subQuestions: ConjuntoQuestoes;
}
export interface StudentExam {
    studentId: string;
    questions: StudentExamQuestion[];
}
export interface Evaluation {
    id: string;
    course: Course;
    title: string;
    date: string;
    numQuestions: number;
    selectedCourseworks: string[];
    selectedStudents: Student[];
    studentExams: StudentExam[];
}
