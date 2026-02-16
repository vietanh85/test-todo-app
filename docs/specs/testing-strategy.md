# Testing Strategy and Architecture

## 1. Overview
This document defines the testing strategy for the Todo application, ensuring high code quality, reliability, and maintainability across both the backend (Python) and frontend (TypeScript/React).

## 2. Testing Levels

### 2.1 Unit Testing
- **Goal**: Verify individual functions, components, and logic in isolation.
- **Backend (Python)**:
    - Framework: `pytest`
    - Focus: Models, utility functions, and business logic.
- **Frontend (React)**:
    - Framework: `Vitest` + `React Testing Library`
    - Focus: UI components, custom hooks (`useTodos`), and utility functions.

### 2.2 Integration Testing
- **Goal**: Verify interactions between different parts of the system (e.g., API endpoints and Database).
- **Backend**:
    - Framework: `pytest` with `httpx` for client requests.
    - Focus: API endpoints, database interactions, and middleware.
- **Frontend**:
    - Focus: TanStack Query hooks integration with mock service worker (MSW).

### 2.3 End-to-End (E2E) Testing
- **Goal**: Verify the entire system from the user's perspective.
- **Framework**: `Playwright` or `Cypress`.
- **Focus**: Critical user flows (Create, Read, Update, Delete todos).

## 3. Test Data Management
- Use a dedicated test database (e.g., SQLite in-memory or a separate PostgreSQL container).
- Reset the database state before each test suite execution.
- Use factory patterns (e.g., `factory_boy` for Python) to generate test data.

## 4. CI/CD Integration
- Tests must run automatically on every Pull Request.
- Minimum code coverage requirement: 80%.
- Linting and type checking (Pyright/ESLint/TSC) must pass before tests run.

## 5. API Mocking
- **Frontend**: Use `Mock Service Worker (MSW)` to intercept API calls during development and testing.
- **Backend**: Use `unittest.mock` or `pytest-mock` to mock external services (if any).
