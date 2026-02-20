# ADR 002: Removal of Single Sign-On (SSO) Authentication

## Status
Proposed

## Context
The application currently implements Single Sign-On (SSO) using OpenID Connect (OIDC). This was implemented to support multi-user environments and secure access. However, the project requirements have changed, and the complexity of maintaining SSO (including managing IdP configurations, token validation, and user synchronization) is no longer justified for the current use case.

The current implementation:
- Uses `fastapi-auth0` style validation with JWKS.
- Requires `OIDC_ISSUER`, `OIDC_AUDIENCE`, and `JWKS_URL` environment variables.
- Synchronizes users to a local database.
- Associates all Todos with a `user_id`.

## Decision
We will remove the SSO authentication layer from the application. 

Specifically:
1.  **Backend**: Remove the `HTTPBearer` security dependency from all API endpoints.
2.  **Authentication Logic**: Deprecate `auth.py` and its `get_current_user` dependency.
3.  **User Model**: Transition from a dynamic user synchronization model to a simplified model.
4.  **Database**: Keep the `user_id` column in the `todos` table for potential future use or local multi-user support, but default it to a constant "default-user" if no authentication is provided.
5.  **Frontend**: Remove any OIDC client libraries and logic that handles redirection to the IdP or inclusion of Bearer tokens in API requests.

## Consequences
- **Security**: The application will no longer have built-in authentication. It is expected to be run in a trusted environment or behind a separate authentication proxy (e.g., Authelia, Nginx Basic Auth) if security is required.
- **Complexity**: Significantly reduced. No more dependency on external Identity Providers.
- **Development Speed**: Faster local development as no IdP setup is required.
- **User Experience**: Immediate access to the application without a login redirect.
- **Data Integrity**: Existing todos associated with specific `user_id`s will remain, but new todos will be associated with the "default-user" unless a simplified local mechanism is introduced.
