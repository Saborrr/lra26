/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'neon-green': '#00ff88',
        'neon-purple': '#ff00ff',
      },
      boxShadow: {
        'neon-green': '0 0 20px #00ff88',
      },
    },
  },
  plugins: [],
}