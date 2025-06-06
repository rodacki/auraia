import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Login from '../views/Login.vue'
console.log("Login Component:", Login); // 🔹 Adicione esta linha para depuração
import TurmaDashboard from '../views/TurmaDashboard.vue'
console.log("TurmaDashboard Component:", TurmaDashboard); // 🔹 Adicione esta linha para depuração
import ProfessorDashboard from '../views/ProfessorDashboard.vue'
console.log("Dashboard Component:", ProfessorDashboard); // 🔹 Adicione esta linha para depuração
import EvaluationCreate from '../views/EvaluationCreate.vue'
console.log("EvaluationCreate Component:", EvaluationCreate); // 🔹 Adicione esta linha para depuração
import EvaluationResult from "../views/EvaluationResult.vue";
console.log("EvaluationResult Component:", EvaluationResult); // 🔹 Adicione esta linha para depuração



const isAuthenticated = (): boolean => !!localStorage.getItem('token')

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'ProfessorDashboard',
    component: ProfessorDashboard,
    beforeEnter: (_to, _from, next) => {
      isAuthenticated() ? next() : next({ name: 'Login' })
    }
  },
  {
    path: '/turma/:courseId/avaliacao/criar',
    name: 'EvaluationCreate',
    component: EvaluationCreate,
    beforeEnter: (_to, _from, next) => {
      isAuthenticated() ? next() : next({ name: 'Login' })
    }
  },
  {
    path: '/evaluation-result/:evaluationId', 
    name: 'EvaluationResult',
    component: EvaluationResult,
    beforeEnter: (_to, _from, next) => {
      isAuthenticated() ? next() : next({ name: 'Login' });
    }
  },
  {
    path: "/turma/:courseId/dashboard",
    name: "TurmaDashboard",
    component: TurmaDashboard,
    beforeEnter: (_to, _from, next) => {
      isAuthenticated() ? next() : next({ name: "Login" });
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router