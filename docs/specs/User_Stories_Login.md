# User Stories: Authentication

## Overview
These user stories describe the login and authentication requirements from the perspective of different user types.

## User Stories

### US-001: User Login
**As a** registered user  
**I want to** log in with my credentials  
**So that** I can access my private todo list.

**Acceptance Criteria:**
- GIVEN the user is on the login page
- WHEN they enter valid email and password
- AND click "Login"
- THEN they are redirected to the Dashboard.
- GIVEN the user enters incorrect credentials
- WHEN they click "Login"
- THEN an error message "Invalid email or password" is displayed.

### US-002: Protected Routes
**As a** guest user  
**I want to** be prevented from seeing private data  
**So that** my data (or others' data) remains secure.

**Acceptance Criteria:**
- GIVEN a user is not logged in
- WHEN they try to navigate directly to `/dashboard`
- THEN they are redirected to the `/login` page.

### US-003: User Logout
**As a** logged-in user  
**I want to** log out of my account  
**So that** nobody else can access my account on this device.

**Acceptance Criteria:**
- GIVEN the user is logged in
- WHEN they click the "Logout" button
- THEN their session is destroyed
- AND they are redirected to the login page.

### US-004: Persistent Session
**As a** busy user  
**I want to** stay logged in between browser restarts  
**So that** I don't have to re-enter my credentials every time.

**Acceptance Criteria:**
- GIVEN the user has successfully logged in
- WHEN they close and reopen the browser
- THEN they should still be logged in (unless the session expired).

### US-005: Password Security Visibility
**As a** user entering a complex password  
**I want to** see what I'm typing  
**So that** I can correct typos before submitting.

**Acceptance Criteria:**
- GIVEN the user is typing in the password field
- WHEN they click the "eye" icon
- THEN the password text becomes visible.
- WHEN they click it again
- THEN it becomes masked again.
