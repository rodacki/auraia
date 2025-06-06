import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./index.css"; // Certifique-se de que este caminho está correto

createApp(App)
    .use(router)
    .mount("#app");