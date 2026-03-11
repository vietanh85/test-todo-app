# ADR-006: mTLS and Certificate Management Strategy for 1M+ Vehicles

## Status
Proposed

## Context
The NOA DataOps platform must securely authenticate and authorize over 1 million Honda vehicles (scaling to 6.5 million by 2040). Each vehicle must establish a secure communication channel to upload sensitive sensor and video data. Traditional username/password or simple API keys are insufficient due to the scale, security risks, and lack of strong device identity. We need a robust Public Key Infrastructure (PKI) and Mutual TLS (mTLS) strategy to ensure only authorized vehicles can communicate with the platform.

## Decision
We will implement a **Managed PKI with mTLS**, strategically reusing the existing **Connected Authentication Platform** for certificate issuance and JWT orchestration.

Key components of the decision:
1. **Reuse of Honda Connected Auth Platform:** To minimize architectural redundancy, the NOA DataOps platform will integrate with the established Connected Authentication Platform. The DataOps Vehicle-Facing Gateway will act as a PEP (Policy Enforcement Point), validating mTLS handshakes and proxying token requests.
2. **Tiered CA Hierarchy:**
   - **Root CA:** Offline, highly secure root of trust.
   - **Intermediate CA (Issuing CA):** Managed by the Connected Auth Platform, dedicated to vehicle identity.
2. **Device-Level Certificates:** Every vehicle will be provisioned with a unique X.509 certificate and private key stored in a Hardware Security Module (HSM) or Trusted Platform Module (TPM) during manufacturing or provisioning.
3. **mTLS at Ingress:** The Vehicle-Facing Gateway (AKS-based) will terminate mTLS connections. It will verify the vehicle certificate against the trusted Issuing CA.
4. **Certificate Revocation:** Implementation of Online Certificate Status Protocol (OCSP) stapling and short-lived certificates to minimize the impact of compromised keys, rather than relying solely on large Certificate Revocation Lists (CRLs).
5. **Auto-Renewal:** Vehicles will support an automated certificate renewal process (e.g., via EST or SCEP) to rotate keys without manual intervention.

## Consequences
### Positive
- **Strong Identity:** Cryptographic assurance of vehicle identity.
- **Encryption:** Automatic encryption of all data in transit via TLS.
- **Revocation:** Ability to instantly block compromised or decommissioned vehicles.
- **Compliance:** Meets industry standards for automotive cybersecurity (ISO/SAE 21434).

### Negative
- **Operational Complexity:** Managing a PKI for millions of devices requires significant operational overhead and specialized expertise.
- **Infrastructure Cost:** Cost of managed CA services and HSM-backed storage for root keys.
- **Provisioning Hurdles:** Requires integration with the vehicle manufacturing and provisioning process.

### Risks
- **Root CA Compromise:** If the Root CA is compromised, the entire fleet's security is invalidated.
- **OCSP Availability:** If the OCSP responder is down, mTLS handshakes may fail or revert to "insecure" if not handled carefully.
- **Certificate Expiry:** Large-scale "bricking" of vehicle communication if auto-renewal fails globally due to a bug.
