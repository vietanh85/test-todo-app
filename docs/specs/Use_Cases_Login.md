# Use Cases and Workflows: Login Functionality

## 1. Use Case Diagram

```mermaid
useCaseDiagram
    User -> (Login)
    User -> (Logout)
    User -> (Request Password Reset)
    (Login) ..> (Validate Credentials) : include
    (Login) ..> (Show Dashboard) : secondary
```

## 2. Login Workflow (Sequence Diagram)

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Database

    User->>Frontend: Enter credentials & click Login
    Frontend->>Backend: POST /api/auth/login {email, password}
    Backend->>Database: Query user by email
    Database-->>Backend: User object (with hashed password)
    Backend->>Backend: Verify password hash
    alt Credentials Valid
        Backend-->>Frontend: 200 OK + JWT Token
        Frontend->>Frontend: Store token in LocalStorage/Cookies
        Frontend->>User: Redirect to Dashboard
    else Credentials Invalid
        Backend-->>Frontend: 401 Unauthorized
        Frontend->>User: Display error message
    end
```

## 3. Logout Workflow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend

    User->>Frontend: Click Logout
    Frontend->>Frontend: Clear LocalStorage/Cookies
    Frontend-->>User: Redirect to Login Page
    Note over Frontend,Backend: Optional: Notify backend to blacklist token
    Frontend->>Backend: POST /api/auth/logout
    Backend-->>Frontend: 200 OK
```

## 4. Protected Route Guard Workflow

```mermaid
graph TD
    A[User requests /dashboard] --> B{Is Authenticated?}
    B -- Yes --> C[Render Dashboard]
    B -- No --> D[Redirect to /login]
    D --> E[User logs in]
    E --> C
```
