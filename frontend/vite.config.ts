import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  base: '/lra26/',
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icons/icon.svg', 'icons/icon-192.png', 'icons/icon-512.png'],
      manifest: {
        name: 'LRA-26 · Космический рейтинг',
        short_name: 'LRA-26',
        description: 'Рейтинг команд, задания и кабинет участника',
        theme_color: '#07091d',
        background_color: '#050611',
        display: 'standalone',
        orientation: 'portrait-primary',
        start_url: '/lra26/',
        scope: '/lra26/',
        icons: [
          { src: 'icons/icon-192.png', sizes: '192x192', type: 'image/png', purpose: 'any maskable' },
          { src: 'icons/icon-512.png', sizes: '512x512', type: 'image/png', purpose: 'any maskable' }
        ]
      },
      workbox: {
        navigateFallback: '/lra26/index.html',
        navigateFallbackDenylist: [/\/api\//, /\/ws\//],
        runtimeCaching: [
          {
            urlPattern: /\/lra26\/api\/leaderboard\/$/,
            handler: 'NetworkFirst',
            options: { cacheName: 'leaderboard', networkTimeoutSeconds: 3, expiration: { maxEntries: 1, maxAgeSeconds: 300 } }
          }
        ]
      }
    })
  ],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/lra26/api': { target: 'http://127.0.0.1:8000', changeOrigin: true, rewrite: path => path.replace(/^\/lra26/, '') },
      '/lra26/ws': { target: 'ws://127.0.0.1:8000', ws: true, rewrite: path => path.replace(/^\/lra26/, '') },
      '/lra26/control': { target: 'http://127.0.0.1:8000', changeOrigin: true, rewrite: path => path.replace(/^\/lra26/, '') },
      '/lra26/static': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/lra26/media': { target: 'http://127.0.0.1:8000', changeOrigin: true }
    }
  }
});
