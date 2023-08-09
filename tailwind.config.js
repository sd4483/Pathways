/** @type {import('tailwindcss').Config} */
module.exports = {
  important: true,
  content: [
    './templates/**/*.html',
    './users/templates/**/*.html',
    './pathways/templates/**/*.html',
    './pathways/forms.py',
],
  theme: {
    extend: {
      colors :{
        'card': '#E3CCAE',
        'brownish': '#473C33',
        'light-brownish': '#9c8979',
        'lighter-brownish': '#baa593',
      }
    },
  },
  plugins: [],
}

