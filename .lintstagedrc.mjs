export default {
  // TypeScript/JavaScript files in project directories - run ESLint
  "nedlia-front-end/**/*.{js,jsx,ts,tsx}": (filenames) => {
    if (filenames.length === 0) return [];
    return [
      `eslint --config tools/js/eslint.config.js --fix --max-warnings=0 ${filenames.join(" ")}`,
    ];
  },

  // Python files - run Ruff directly on staged files
  "*.py": (filenames) => {
    const files = filenames.filter(
      (f) => !f.includes(".venv") && !f.includes("__pycache__"),
    );
    if (files.length === 0) return [];
    return [
      `ruff check --fix ${files.join(" ")}`,
      `ruff format ${files.join(" ")}`,
    ];
  },

  // JSON files in project directories - run Prettier
  "{nedlia-front-end,nedlia-back-end,nedlia-sdk}/**/*.json": (filenames) => {
    if (filenames.length === 0) return [];
    return [
      `prettier --config tools/js/prettier.config.js --write ${filenames.join(" ")}`,
    ];
  },

  // Markdown files - run Prettier
  "*.md": (filenames) => {
    return [
      `prettier --config tools/js/prettier.config.js --write ${filenames.join(" ")}`,
    ];
  },
};
