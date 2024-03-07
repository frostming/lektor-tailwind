const colors = require("tailwindcss/colors");

module.exports = {
  content: ["./**/*.html"],
  theme: {
    extend: {
      colors: {
        primary: colors.teal,
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
