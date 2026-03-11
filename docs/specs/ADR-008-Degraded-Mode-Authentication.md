# ADR-008: Degraded Mode Authentication for Vehicle-Facing Gateway

## Status
Proposed

## Context
The Vehicle-Facing Gateway (VFG) currently relies on a centralized "Connected Auth Platform" to validate vehicle identity and issue JWT tokens. If this platform becomes unreachable (e.g., due to regional outage or service failure), all vehicle communications across the fleet would be blocked. This includes not only large video uploads but also critical telemetry and heartbeat signals which are vital for fleet monitoring.

## Decision
We will implement a **Degraded Mode** in the Vehicle-Facing Gateway to ensure high availability for critical communications during authentication service outages.

Key implementation details:
1. **Local mTLS Validation:** The VFG already terminates mTLS connections. In Degraded Mode, the VFG will accept the validity of the mTLS client certificate (verified against the Root CA) as a sufficient proof of identity for a limited set of operations.
2. **Feature Flags / Throttling:** When in Degraded Mode:
   - **Allowed:** Small telemetry payloads, heartbeat signals, and critical error logs.
   - **Paused:** Large file uploads (Multipart upload initialization will return 503 with a "Retry-After" header).
   - **Token Bypass:** The requirement for a valid JWT is temporarily relaxed for allowed endpoints, falling back to mTLS-based identity.
3. **Automated Trigger:** The VFG will enter Degraded Mode automatically after a configurable number of consecutive failures (e.g., 5) from the Connected Auth Platform, using a circuit breaker pattern.
4. **Manual Override:** SREs can manually trigger or disable Degraded Mode via the management console.

## Consequences
### Positive
- **High Availability:** Critical fleet telemetry continues even during major authentication outages.
- **Resilience:** Prevents "retry storms" from vehicles trying to re-authenticate simultaneously when the service returns.
- **Safety:** Ensures that critical vehicle status data is not lost.

### Negative
- **Reduced Security Granularity:** While mTLS is still secure, the additional layer of JWT-based authorization (which may contain specific session-level claims) is bypassed.
- **Complexity:** Increased complexity in the VFG logic to handle state transitions and conditional authorization.

### Risks
- **Identity Sprawl:** If a certificate is revoked but the CRL (Certificate Revocation List) is not updated, a "revoked" vehicle could still upload telemetry during Degraded Mode.
- **Abuse:** Potential for malicious actors to exploit the reduced authorization layer if the Degraded Mode is active for prolonged periods.
