# Technical Specification: Vehicle-Facing Gateway (VFG)

## 1. Overview
The Vehicle-Facing Gateway (VFG) is the primary entry point for all Honda vehicles connecting to the NOA DataOps platform. It acts as a security enforcement point, traffic manager, and protocol translator.

## 2. Technical Stack
- **Framework:** Java 21 with Spring Boot 3.x
- **Runtime:** Azure Kubernetes Service (AKS)
- **Communication:** mTLS for transport, REST for API, WebSockets (optional for Phase 2)
- **Database:** Redis (for session/token caching)
- **Integration:** Azure Key Vault (for certificate management)

## 3. Core Functions

### 3.1 Authentication & Authorization
- **mTLS Termination:** Terminate mTLS at the Azure Front Door / Application Gateway level; VFG validates the forwarded client certificate headers against the Managed PKI (See [ADR-006](./ADR-006-mTLS-and-Certificate-Management.md)).
- **JWT Issuance:** Exchange validated certificate details for a short-lived JWT (1 hour) via the Connected Auth Platform.
- **Token Validation:** Every subsequent request must contain the JWT in the `Authorization: Bearer` header.

### 3.2 File Distribution (Trigger & Provisioning)
As per the design review, a **Pull Model** is adopted for scalability.
- **Endpoint:** `GET /v1/trigger/{vehicle_id}`
- **Logic:**
  1. VFG checks Redis for the vehicle's assigned trigger group.
  2. If missing, queries the Master Data management system.
  3. Returns a signed URL to a JSON configuration file hosted on Azure Blob Storage (backed by CDN).
  4. Vehicles poll this endpoint every X minutes or upon significant events (e.g., ignition on).

### 3.3 Data Ingestion Management
- **Pre-signed URL Generation:** For files > 10MB, the VFG generates an Azure Storage SAS (Shared Access Signature) token with `Write-Only` permissions.
- **Direct Upload:** For metadata or small files (<= 10MB), VFG accepts the payload, performs basic validation/virus scanning, and writes directly to the `Landing` container.
- **Resumable Uploads:** Support for multipart upload protocols to handle flaky vehicle connectivity.

## 4. Scalability & Resilience
- **Autoscaling:** HPA (Horizontal Pod Autoscaler) based on CPU and Request Count. Target: < 200ms p95 latency.
- **Circuit Breaker:** Resilience4j implemented for downstream calls to the Auth Platform and Database.
- **Rate Limiting:** Per-vehicle and Per-IP rate limiting to prevent DDoS (intentional or accidental from buggy firmware).

## 5. Security Architecture
- **PII Protection:** VFG logs must NEVER contain PII (VINs are masked in logs).
- **Traffic Isolation:** VFG resides in a restricted Subnet with only Egress to required Azure Services (Event Hubs, Blob Storage).
- **Audit Logging:** Every authentication attempt and configuration retrieval is logged to Microsoft Sentinel for anomaly detection.

## 6. API Summary
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/auth/token` | mTLS-based token exchange |
| GET | `/v1/trigger` | Retrieve signed URL for trigger files |
| POST | `/v1/upload/init` | Request SAS URL for large uploads |
| POST | `/v1/upload/complete` | Notify system that upload is finished |
