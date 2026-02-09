/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2196F3',
        secondary: '#FFC107',
        success: '#4CAF50',
        error: '#F44336',
        warning: '#FF9800',
        info: '#00BCD4'
      }
    },
  },
  plugins: [],
}
