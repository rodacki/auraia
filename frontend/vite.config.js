// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'
// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [vue()],
// })
// import { defineConfig } from 'vite';
// import vue from '@vitejs/plugin-vue';
// import tailwindcss from '@tailwindcss/vite';
// // Exporta a configuração para Vite
// export default defineConfig({
//     plugins: [vue(),
//         tailwindcss(),
//     ],
//     server: {
//         port: 5173, // Altere a porta se necessário
//     },
// });

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import tailwindcss from '@tailwindcss/vite';

// Exporta a configuração para Vite
export default defineConfig({
  plugins: [vue(),
    tailwindcss(),
  ],
  server: {
    port: 5173, // Altere a porta se necessário
  },
});