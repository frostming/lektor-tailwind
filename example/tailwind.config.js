const colors = require("tailwindcss/colors");

module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        primary: colors.teal,
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
