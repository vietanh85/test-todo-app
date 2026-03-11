# Design Review: NOA OutCAR DataOps - Architecture Design

**Reviewer:** Solution Architect (AI)
**Date:** 2026-03-11
**Status:** Detailed Review (Finalized)

## 1. Summary
The current architecture for NOA OutCAR DataOps is well-structured, leveraging a modern Medallion (Lakehouse) architecture on Azure. It correctly identifies key functional areas like vehicle authentication (mTLS), high-throughput ingestion, and anonymization. However, there are critical ambiguities regarding data volume projections and a contradiction between "Cloud Agnostic" goals and "Azure Native" implementation.

## 2. Key Observations & Recommendations

### 2.1 Scalability & Data Volume (Verified)
- **Observation:** The document now correctly identifies the scale for 2040.
- **Analysis:** Petabyte-scale ingestion (~500TB to 2PB/day) and Exabyte-scale total storage (65PB+) are realistic and world-class targets.
- **Recommendation:** Ensure "Storage Account Sharding" and "Edge Filtering" are prioritized in the implementation phase.

### 2.2 Cloud Agnostic vs. Azure Native (Strategic)
- **Observation:** Requirement 2.2 calls for "Cloud Agnostic Design," but the architecture uses specific Azure PaaS (Event Hubs, ADLS, Azure AI Vision).
- **Analysis:** While AKS and Terraform provide a base, the data services create significant lock-in.
- **Recommendation:** If cloud agnosticism is a priority, define an **Abstraction Layer** (e.g., using S3-compatible interfaces for storage, Kafka-compatible for messaging) or accept the lock-in as a strategic choice for Phase 1 (as noted in ADR-003).

### 2.3 Disaster Recovery (Verified)
- **Observation:** RPO (< 5-15 mins) and RTO (< 4-24 hours) targets have been defined.
- **Analysis:** These targets are appropriate for a non-mission-critical DataOps pipeline but provide strong guarantees for AI research continuity.
- **Recommendation:** Regularly test geo-failover via Azure Front Door to ensure the RTO can be met in practice.

### 2.4 Vehicle-Facing Gateway Details (Verified)
- **Observation:** The spec now details the "Pull Model" and SAS-based direct upload.
- **Analysis:** This design minimizes the compute load on the VFG and leverages Azure Blob Storage's native scalability.
- **Recommendation:** Implement a robust "Virus Scan" phase in the Landing zone before moving data to Bronze to prevent lateral movement of malicious payloads.

## 3. Remaining Gaps & Future Considerations
1. **FinOps & Cost Governance**: At Petabyte-scale, ingestion costs must be monitored in real-time. Recommend adding a "Cost Management" section to the architecture.
2. **Edge Trigger A/B Testing**: Support for canary deployments of trigger files to small subsets of the fleet for validation.
3. **Data Quality Framework**: Automated validation of image/video quality (e.g., lens obstruction detection) during the Bronze -> Silver transition.

## 4. Conclusion
The architecture is now robust, scalable, and follows industry best practices for high-volume DataOps. It is ready for the "Detailed Design" and "PoC" implementation phases.
