import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
    hmr: {
      overlay: false,
    },
  },
  preview: {
    port: 3000,
  },
  optimizeDeps: {
    esbuildOptions: {
      logLevel: 'error',
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
