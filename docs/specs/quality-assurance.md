# Technical Specification: Code Quality and Linting

## 1. Overview
This document specifies the standards and tools for maintaining code quality, consistency, and type safety across the project.

## 2. Python Backend
### 2.1 Tools
- **Linter**: `Ruff` (replacement for Flake8, Isort, and more)
- **Type Checker**: `Pyright` or `mypy`
- **Formatter**: `Ruff` (format command)

### 2.2 Standards
- Strict type checking enabled.
- Maximum line length: 88 characters.
- Mandatory docstrings for public modules and classes.

## 3. TypeScript Frontend
### 3.1 Tools
- **Linter**: `ESLint`
- **Type Checker**: `TSC` (TypeScript Compiler)
- **Formatter**: `Prettier` (integrated with ESLint)

### 3.2 Standards
- `strict: true` in `tsconfig.json`.
- No `any` types allowed (except where absolutely necessary and documented).
- Functional components using arrow functions.
- Tailwind CSS class sorting via `prettier-plugin-tailwindcss`.

## 4. Git Hooks
- Use `Husky` and `lint-staged` to run linting and unit tests before every commit.
- Prevent commits that contain `console.log` or debug statements.

## 5. Documentation
- All architecture diagrams should be created using Mermaid.js syntax within markdown files.
- ADRs must be created for any significant architectural change.
