# ADR 001: Selection of Testing Frameworks

## Status
Proposed

## Context
The project needs a robust testing infrastructure for both the Python FastAPI backend and the React TypeScript frontend. We need frameworks that are modern, well-supported, and integrate well with our existing stack.

## Decision
We will use the following frameworks:
1.  **Backend**: `pytest`
2.  **Frontend (Unit/Component)**: `Vitest` + `React Testing Library`
3.  **Frontend (E2E)**: `Playwright`
4.  **API Mocking**: `Mock Service Worker (MSW)`

## Consequences
- **pytest**: Highly extensible and widely used in the Python ecosystem. Easier to write tests compared to the built-in `unittest`.
- **Vitest**: Native support for Vite (which the frontend uses), resulting in faster test execution and easier configuration.
- **React Testing Library**: Encourages testing behavior rather than implementation details.
- **Playwright**: Offers better performance and more reliable selectors compared to Cypress.
- **MSW**: Allows for seamless API mocking at the network level, providing a more realistic testing environment.
