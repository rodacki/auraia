import 'tailwindcss/tailwind-config'

declare module 'tailwindcss/tailwind-config' {
  interface UserConfig {
    daisyui?: {
      themes?: string[] | Record<string, unknown>[]
      darkTheme?: string
      // Você pode adicionar outras propriedades conforme necessário
    }
  }
}
