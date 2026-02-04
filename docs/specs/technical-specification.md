# Technical Specification: Todo Frontend

## 1. Overview
This document outlines the technical implementation details for the Todo application frontend.

## 2. Component Hierarchy
The application will be composed of the following main components:

- `App`: Root component containing providers (`AuthProvider`, `QueryClient`, `ThemeProvider`).
- `LoginPage`: Form for user authentication.
- `AuthGuard`: Wrapper component to protect routes.
- `Layout`: Main wrapper with header and navigation.
    - `UserMenu`: Displays user info and "Logout" button.
- `Dashboard`: Main view containing:
    - `TodoStats`: Summary of active and completed tasks.
    - `AddTodoForm`: Input field and button to create new todos.
    - `TodoList`: Container for the list of todos.
        - `TodoItem`: Individual todo item with edit/delete/complete actions.
    - `TodoFilters`: Tabs to switch between "All", "Active", and "Completed".

## 3. State Management
### Auth State (Context API)
- `useAuth()`: Hook to access user object, login/logout functions, and loading state.

### Server State (TanStack Query)
- `useLogin()`: Mutation to perform authentication.
- `useTodos()`: Fetch user-specific todos (requires auth).
- `useCreateTodo()`: Mutation to add a new todo (requires auth).
- `useUpdateTodo()`: Mutation to toggle completion or edit title/description.
- `useDeleteTodo()`: Mutation to remove a todo.

## 4. Data Flow
1. User interacts with UI (e.g., submits Login form).
2. `useLogin` mutation is triggered.
3. On success, JWT is stored in `localStorage` and `AuthContext` is updated.
4. User is redirected to `Dashboard`.
5. Subsequent API calls automatically include the `Authorization: Bearer <token>` header via an Axios interceptor.
6. On 401 response, `AuthContext` clears token and redirects to `/login`.

## 5. Error Handling
- Global error boundary to catch unexpected crashes.
- Toast notifications (using `sonner` or `react-hot-toast`) for API errors and success confirmations.
- Inline validation errors for the "Add Todo" form.

## 6. Responsive Design
- Mobile-first approach.
- Single column layout for mobile.
- Centered container with max-width for desktop.
