/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        neon: {
          blue: "#00f3ff",
          purple: "#9d00ff",
          pink: "#ff007f",
          cyan: "#0ff",
          green: "#0f0",
          orange: "#ffaa00",
        },
        dark: {
          bg: "#050510",
          panel: "rgba(10, 10, 20, 0.7)",
          border: "rgba(0, 243, 255, 0.2)",
        }
      },
      backgroundImage: {
        'glass-gradient': 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%)',
      }
    },
  },
  plugins: [],
}
