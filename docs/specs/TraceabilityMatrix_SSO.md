# Requirements Traceability Matrix (RTM) - SSO

## 1. Overview
This matrix maps functional and non-functional requirements to their corresponding user stories and use cases to ensure full coverage and justification.

## 2. Traceability Matrix

| Req ID | Description | Priority | User Story | Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **FR-101** | Login via Google | Must | US-01 | UC-1 |
| **FR-102** | OIDC Protocol | Must | US-01 | UC-1 |
| **FR-103** | Logout | Must | US-03 | UC-2 |
| **FR-201** | JWT Session | Must | US-01, US-04 | UC-1, UC-4 |
| **FR-202** | Expired Token Handling | Should | US-04 | UC-4 |
| **FR-301** | Association with `user_id` | Must | US-02, US-05 | UC-3 |
| **FR-302** | Display owned items only | Must | US-02 | UC-3 |
| **FR-303** | Ownership restricted ops | Must | US-02 | UC-3 |
| **NFR-101** | JWT Validation | Must | US-01, US-02 | - |
| **NFR-102** | Secure Token Storage | Must | US-01, US-03 | - |
| **NFR-103** | HTTPS Encryption | Must | - | - |
| **NFR-201** | Performance (<2s) | Should | US-01 | UC-1 |
| **NFR-301** | IdP Reliability | Should | US-01 | UC-1 |

## 3. Validation Summary
- **Functional Coverage**: All functional requirements are mapped to at least one User Story and Use Case.
- **Security Coverage**: Non-functional requirements for security (NFR-101, NFR-102) are implicitly covered by the technical implementation of US-01 and US-03.
- **Priority Distribution**:
    - **Must Have**: 8
    - **Should Have**: 3
    - **Could Have**: 0
