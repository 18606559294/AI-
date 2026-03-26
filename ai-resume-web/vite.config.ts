import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd(), '');

  return {
    // 基础路径，用于部署
    base: env.VITE_BASE_URL || '/',

    plugins: [react()],

    resolve: {
      alias: {
        '@': resolve(__dirname, './src'),
      },
    },

    server: {
      port: 3000,
      strictPort: true,
      host: true,
      proxy: {
        '/api': {
          target: env.VITE_API_PROXY_TARGET || 'http://127.0.0.1:8000',
          changeOrigin: true,
        },
      },
      hmr: {
        overlay: false,
      },
    },

    preview: {
      port: 3000,
      host: true,
    },

    optimizeDeps: {
      esbuildOptions: {
        logLevel: 'error',
      },
    },

    build: {
      outDir: 'dist',
      sourcemap: mode === 'development',
      // 生产环境优化 - 使用 esbuild 避免额外依赖
      minify: 'esbuild',
      target: 'es2015',
      // 分包策略
      rollupOptions: {
        output: {
          manualChunks: {
            // 第三方库分包
            'vendor-react': ['react', 'react-dom', 'react-router-dom'],
            'vendor-query': ['@tanstack/react-query'],
            'vendor-ui': ['zustand'],
          },
        },
      },
      // 资源内联限制
      assetsInlineLimit: 4096,
    },
  };
});
