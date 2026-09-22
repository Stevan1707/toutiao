// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'

// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [vue()],
// })


import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    // 让 Vite 自身也识别 .mjs 扩展名
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue'],
  },
  optimizeDeps: {
    // 强制预构建 vant 和 axios，避免它们被当作源码直接加载
    include: ['vant', 'axios'],
    esbuildOptions: {
      // 关键：让 esbuild 支持现代 ESM 语法，并解析 .mjs
      target: 'esnext',
      resolveExtensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json'],
    },
  },
  build: {
    // 构建目标也设为 esnext，保持一致
    target: 'esnext',
  },
})