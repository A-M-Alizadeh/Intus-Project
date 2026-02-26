import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [vue()],
    // Set VITE_BASE_PATH for GitHub Pages project sites (e.g. /my-repo/).
    base: env.VITE_BASE_PATH || '/',
  }
})
