# Use Cases and Workflows - SORA

## Use Case 1: The "4:50 PM Clean Slate"
**Actor:** Office Worker  
**Pre-condition:** User is logged in and it is 4:50 PM on a workday.

**Main Success Scenario:**
1. **Trigger:** System detects time is 4:50 PM.
2. **Notification:** SORA sends a desktop notification: "Time to wrap up! Ready for your Clean Slate ritual?"
3. **Task Review:** SORA displays tasks completed today (synced from Jira/Linear).
4. **Log Wins:** User types in one major achievement.
5. **Next Day Planning:** SORA suggests 3 tasks for tomorrow based on deadlines.
6. **Confirmation:** User clicks "Done for today".
7. **Action:** SORA sets Slack status to "Out of Office" and silences work emails on mobile.

---

## Use Case 2: Lunch Group Voting
**Actor:** Group Organizer / Team Member

**Workflow:**
1. **Initiation (11:15 AM):** SORA checks if today is a "Team Lunch" day.
2. **Polling:** SORA sends a message to the team channel: "Hungry? Here are today's top 3 nearby options based on your preferences."
3. **Voting:** Team members click buttons for: 
    - [Option A: Sushi]
    - [Option B: Deli/Salad]
    - [Option C: Pho]
4. **Decision (11:45 AM):** SORA announces the winner and provides a Google Maps link to the location.
5. **Calendar Sync:** Adds a 1-hour "Lunch with Team" block to participants' calendars to prevent late meetings.

---

## Requirements Traceability Matrix (Draft)

| Req ID | User Story | Use Case | Status |
|:---|:---|:---|:---|
| FR-001 | US-01 | Morning Briefing Flow | Defined |
| FR-002 | US-02 | Focus Mode Trigger | Defined |
| FR-003 | - | Use Case 2 (Lunch) | Defined |
| FR-004 | US-03 | Use Case 1 (Clean Slate) | Defined |
