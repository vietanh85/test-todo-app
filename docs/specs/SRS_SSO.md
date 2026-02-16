# Software Requirements Specification (SRS) - Single Sign-On (SSO)

## 1. Introduction
This document outlines the functional and non-functional requirements for implementing Single Sign-On (SSO) in the Todo Application.

## 2. Business Requirements
- **BR-001**: The system must support multi-tenancy by isolating user data.
- **BR-002**: The system must leverage existing identity providers to reduce password management overhead for users.
- **BR-003**: The system must ensure secure access to user-specific todo items.

## 3. Functional Requirements

### 3.1 User Authentication
- **FR-101**: The system shall allow users to log in using Google OAuth 2.0.
  - **Acceptance Criteria**: User is redirected to Google login, and upon successful authentication, is redirected back to the application with a valid session.
  - **Priority**: Must have
- **FR-102**: The system shall support OIDC (OpenID Connect) protocol for authentication.
  - **Acceptance Criteria**: Authentication flow follows OIDC standards (Authorization Code Flow with PKCE).
  - **Priority**: Must have
- **FR-103**: The system shall allow users to log out.
  - **Acceptance Criteria**: User's session is invalidated on the client-side, and they are redirected to the landing page.
  - **Priority**: Must have

### 3.2 Session Management
- **FR-201**: The system shall maintain an authenticated session using JWT (JSON Web Tokens).
  - **Acceptance Criteria**: JWT is issued upon successful login and used for subsequent API requests.
  - **Priority**: Must have
- **FR-202**: The system shall handle expired tokens by prompting the user to re-authenticate or using refresh tokens (if implemented).
  - **Acceptance Criteria**: API returns 401 on expired token; frontend handles redirection to login.
  - **Priority**: Should have

### 3.3 User Data Isolation
- **FR-301**: The system shall associate every todo item with a unique `user_id`.
  - **Acceptance Criteria**: Database schema includes `user_id` in the `todos` table.
  - **Priority**: Must have
- **FR-302**: The system shall only display todo items belonging to the currently authenticated user.
  - **Acceptance Criteria**: `GET /todos` returns only items where `user_id` matches the authenticated subject.
  - **Priority**: Must have
- **FR-303**: The system shall restrict write/delete operations to the owner of the todo item.
  - **Acceptance Criteria**: `PUT/DELETE /todos/{id}` returns 404 or 403 if the item belongs to another user.
  - **Priority**: Must have

## 4. Non-Functional Requirements

### 4.1 Security
- **NFR-101**: JWT tokens must be validated on the backend for every protected request.
  - **Acceptance Criteria**: Signature, expiration, issuer, and audience are verified using IdP public keys.
  - **Priority**: Must have
- **NFR-102**: Sensitive user information must not be stored in local storage.
  - **Acceptance Criteria**: Tokens are stored in memory or secure HTTP-only cookies.
  - **Priority**: Must have
- **NFR-103**: All authentication traffic must be encrypted via HTTPS.
  - **Acceptance Criteria**: Application is only accessible via HTTPS in production.
  - **Priority**: Must have

### 4.2 Performance
- **NFR-201**: SSO authentication redirection should complete within 2 seconds (excluding IdP processing time).
  - **Acceptance Criteria**: Latency for local processing is minimal.
  - **Priority**: Should have

### 4.3 Reliability
- **NFR-301**: The system should gracefully handle IdP downtime.
  - **Acceptance Criteria**: Users are shown a clear error message if Google login is unavailable.
  - **Priority**: Should have

## 5. Stakeholders
- **Users**: Need a simple and secure way to access their private todos.
- **Developers**: Need a standard way to manage identities and secure APIs.
- **Security Officers**: Need to ensure data privacy and secure authentication mechanisms.
