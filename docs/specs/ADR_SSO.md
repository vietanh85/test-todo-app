# ADR 005: Implementation of Single Sign-On (SSO)

## Status
Proposed

## Context
The current Todo application lacks authentication and authorization. All users share the same set of todos, and there is no identity management. To support multiple users and secure their data, we need a Single Sign-On (SSO) solution.

## Decision
We will implement SSO using **OpenID Connect (OIDC)** via **OAuth 2.0**.

### Selected IdP
Initially, we will support **Google OAuth 2.0** as the primary Identity Provider (IdP), as it is widely used and provides a simple integration path. The architecture will be designed to be IdP-agnostic to allow adding other providers (e.g., GitHub, Azure AD) in the future.

### Authentication Flow
We will use the **Authorization Code Flow with PKCE** (Proof Key for Code Exchange).
1.  **Frontend** initiates the login by redirecting the user to the IdP.
2.  **User** authenticates with the IdP.
3.  **IdP** redirects back to the Frontend with an authorization code.
4.  **Frontend** exchanges the code for tokens (Access Token, ID Token) via the IdP's token endpoint.
5.  **Frontend** sends the Access Token (JWT) in the `Authorization: Bearer <token>` header for all API requests.
6.  **Backend** validates the JWT using the IdP's public keys (JWKS).

### Technical Stack
- **Frontend**: `react-oidc-context` or `oidc-client-ts` for managing the OIDC flow.
- **Backend**: `fastapi-auth0` or custom middleware using `python-jose` and `httpx` to fetch and cache JWKS.

## Consequences
- **Security**: Todos will be isolated by user ID. JWT validation ensures only authenticated users can access the API.
- **User Experience**: Users can log in using their existing Google accounts without creating a new password for this app.
- **Complexity**: Adds complexity to both frontend and backend for token management and validation.
- **Dependencies**: The application will depend on the availability of the external IdP.
- **Database Changes**: The `todos` table must be updated to include a `user_id` field. A `users` table may be needed for profile storage.
