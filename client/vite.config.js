import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: process.env.NODE_ENV === 'production' 
          ? 'https://soko-safi-brvc.onrender.com'
          : 'http://127.0.0.1:5001',
        changeOrigin: true,
        secure: process.env.NODE_ENV === 'production',
        rewrite: (path) => path,
      }
    }
  }
})