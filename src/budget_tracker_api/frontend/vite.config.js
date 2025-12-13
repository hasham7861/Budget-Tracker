import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],

  // Build output configuration
  build: {
    outDir: '../app/public',
    emptyOutDir: true,
    rollupOptions: {
      output: {
        // Asset file naming
        assetFileNames: 'assets/[name]-[hash][extname]',
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
      }
    }
  },

  // Development server configuration
  server: {
    port: 5173,
    // Proxy API requests to FastAPI during development
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },

  // Base path for assets
  base: '/',
});
