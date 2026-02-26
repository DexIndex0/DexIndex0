import { defineConfig } from 'vite';

export default defineConfig({
  // Use relative base for GH Pages subfolder compatibility
  base: '/DexIndex0/',
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: './index.html',
        notFound: './404.html'
      }
    }
  }
});
