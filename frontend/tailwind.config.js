/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx, html}"],
  theme: {
    extend: {
      colors: {
        primary: "#4A2280",
        "primary-bg": "#D9CBE4",
      },
      fontFamily: { sans: ["Circular Std"] },
    },
  },
  plugins: [],
};
