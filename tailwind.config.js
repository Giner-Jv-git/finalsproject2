/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './ems/templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
} 