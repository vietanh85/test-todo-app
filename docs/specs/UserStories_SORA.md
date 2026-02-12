# User Stories & Acceptance Criteria - SORA

## US-01: Morning Preparation
**As a** busy office worker,  
**I want** to receive a consolidated briefing before I start my commute,  
**So that** I am mentally prepared for my day without checking multiple apps.

### Acceptance Criteria
- **AC1:** System pulls data from Calendar, Weather API, and Traffic API.
- **AC2:** Delivery occurs at a user-defined time (default 30 mins before first meeting).
- **AC3:** Briefing includes: Next meeting time, expected travel time, and a "High/Low" temperature alert.

---

## US-02: Protecting Focus Time
**As a** developer or analyst,  
**I want** the system to automatically block my status when I have a free slot,  
**So that** I don't get interrupted by ad-hoc "quick chat" requests.

### Acceptance Criteria
- **AC1:** Detects gaps in calendar >= 1 hour.
- **AC2:** Changes status on Slack/Microsoft Teams to "Focus Mode - DnD".
- **AC3:** User must be able to override or "End Focus Early" via a single click.

---

## US-03: End-of-Day Mental Disconnect
**As a** 9-to-5 worker who struggles to "stop" thinking about work,  
**I want** a guided ritual to close my tasks at 4:50 PM,  
**So that** I can enjoy my evening without lingering work anxiety.

### Acceptance Criteria
- **AC1:** Trigger a notification 10 minutes before the end of the shift.
- **AC2:** Provide a text input for "Wins of the Day".
- **AC3:** Auto-create a "Top 3 for Tomorrow" list based on uncompleted tasks.
- **AC4:** Automatically close or minimize all non-essential browser tabs/apps (optional user setting).
