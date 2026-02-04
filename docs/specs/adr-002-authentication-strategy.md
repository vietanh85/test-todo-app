# ADR 002: Authentication and Authorization Strategy

## Status
Proposed

## Context
The Todo application requires a secure method to authenticate users and authorize access to their personal data. We need to decide on the authentication mechanism (Session vs. Token) and where to store authentication state.

## Decision
We will implement **JWT (JSON Web Token) based authentication** with the following specifics:

1.  **Token Generation**: The backend (FastAPI) will generate a JWT upon successful login containing the user's ID and an expiration timestamp.
2.  **Transport**: Tokens will be returned in the response body for the initial login, but we will evaluate moving to **HttpOnly, Secure Cookies** for subsequent implementations to mitigate XSS risks.
3.  **Client-Side Storage**: Initially, the frontend will store the JWT in `localStorage` for ease of implementation, with an `AuthContext` to manage the user state.
4.  **Authorization Header**: The client will include the JWT in the `Authorization: Bearer <token>` header for all protected API requests.
5.  **Interceptors**: An Axios interceptor will be used to automatically attach the token to outgoing requests and handle 401 (Unauthorized) responses by redirecting the user to the login page.

## Alternatives Considered
- **Session-based Authentication**:
    - *Pros*: More secure (no tokens exposed to JS), easier logout (server-side).
    - *Cons*: Requires stateful backend or distributed session store (Redis) if scaling horizontally.
- **OAuth2 / OpenID Connect (OIDC)**:
    - *Pros*: Offloads security to specialized providers (Auth0, Google).
    - *Cons*: Higher complexity for a simple internal todo application.

## Consequences
- **Pros**:
    - Stateless backend (easier to scale).
    - Works well across different domains or mobile clients in the future.
    - Decouples authentication from session management.
- **Cons**:
    - Token storage in `localStorage` is vulnerable to XSS (must ensure strict input sanitization).
    - Revoking tokens before expiration is difficult without a blacklist.
