// import type { Config } from 'tailwindcss'
// import daisyui from 'daisyui'

// export default <Config>{
//   content: [
//     "./index.html",
//     "./src/**/*.{vue,js,ts,jsx,tsx}",
//   ],
//   theme: {
//     extend: {},
//   },
//   plugins: [daisyui],
//   daisyui: {
//     themes: ["dark", "light"],
//     darkTheme: "dark",
//   },
// }

// /** @type {import('tailwindcss').Config} */
// const daisyui = require('daisyui');

// module.exports = {
//   content: [
//     "./index.html",
//     "./src/**/*.{vue,js,ts,jsx,tsx}",
//   ],
//   theme: {
//     extend: {},
//   },
//   plugins: [daisyui],
//   daisyui: {
//     themes: ["dark", "light"],
//     darkTheme: "dark",
//   },
// };

// import type { Config } from 'tailwindcss';
// import daisyui from 'daisyui';

// const config: Config = {
//   content: [
//     "./index.html",
//     "./src/**/*.{vue,js,ts,jsx,tsx}",
//   ],
//   theme: {
//     extend: {},
//   },
//   plugins: [daisyui],
//   daisyui: {
//     themes: ["dark", "light"],
//     darkTheme: "dark",
//   },
// };

// export default config;


// import type { Config } from 'tailwindcss';
// import daisyui from 'daisyui';

// const config: Config = {
//   content: [
//     "./index.html",
//     "./src/**/*.{vue,js,ts,jsx,tsx}",
//   ],
//   theme: {
//     extend: {},
//   },
//   plugins: [daisyui], // DaisyUI já está nos plugins
// };

// // Adicionamos um `export` separado para evitar erros de tipagem do TypeScript
// export default {
//   ...config, 
//   daisyui: {
//     themes: ["dark", "light"],
//     darkTheme: "dark",
//   },
// } satisfies Config; // ✅ Isso garante que TypeScript aceite a configuração extra


/** @type {import('tailwindcss').Config} */
const daisyui = require('daisyui');

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [daisyui],
  daisyui: {
    themes: ["dark", "light"],
    darkTheme: "dark",
  },
};