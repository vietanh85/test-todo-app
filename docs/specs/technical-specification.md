# Technical Specification: Todo Frontend

## 1. Overview
This document outlines the technical implementation details for the Todo application frontend.

## 2. Component Hierarchy
The application will be composed of the following main components:

- `App`: Root component containing providers (QueryClient, ThemeProvider).
- `Layout`: Main wrapper with header and navigation.
- `Dashboard`: Main view containing:
    - `TodoStats`: Summary of active and completed tasks.
    - `AddTodoForm`: Input field and button to create new todos.
    - `TodoList`: Container for the list of todos.
        - `TodoItem`: Individual todo item with edit/delete/complete actions.
    - `TodoFilters`: Tabs to switch between "All", "Active", and "Completed".

## 3. State Management
### Server State (TanStack Query)
- `useTodos()`: Fetch all todos.
- `useCreateTodo()`: Mutation to add a new todo.
- `useUpdateTodo()`: Mutation to toggle completion or edit title/description.
- `useDeleteTodo()`: Mutation to remove a todo.

### Client State
- UI state (e.g., current filter, theme) will be managed using React `useState` or a lightweight store like `Zustand` if complexity increases.

## 4. Data Flow
1. User interacts with UI (e.g., clicks "Complete").
2. Component triggers a mutation via React Query.
3. React Query sends a PUT request to the backend.
4. On success, React Query invalidates the `todos` cache.
5. UI automatically re-refetches and updates with the latest data.

## 5. Error Handling
- Global error boundary to catch unexpected crashes.
- Toast notifications (using `sonner` or `react-hot-toast`) for API errors and success confirmations.
- Inline validation errors for the "Add Todo" form.

## 6. Responsive Design
- Mobile-first approach.
- Single column layout for mobile.
- Centered container with max-width for desktop.
