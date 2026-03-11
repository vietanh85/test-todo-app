# ADR-004: Scalability and Storage Strategy for NOA OutCAR DataOps

## Status
Proposed

## Context
The NOA OutCAR DataOps platform is projected to support 6.5 million vehicles by 2040. Initial estimates of "65TB total storage" were found to be inconsistent with the scale of high-resolution image and video data collection. Assuming a conservative 10MB upload per vehicle per day, the system would ingest ~65TB **per day**, leading to ~23PB per year. A robust strategy is needed to handle this scale while managing costs.

## Decision
We will implement a **Multi-Tiered Exabyte-Scale Storage Strategy** leveraging Azure Data Lake Storage (ADLS) Gen2 and automated lifecycle management.

Key components:
1.  **Ingestion Scale**: Design for a peak ingestion rate of 65,000 requests per second (RPS) and ~100TB/day throughput.
2.  **Tiered Lifecycle**:
    *   **Hot Tier (Bronze/Silver)**: Data retained for 30 days for active training and processing.
    *   **Cool Tier (Gold)**: Curated datasets retained for 1 year for model iteration.
    *   **Archive Tier (Raw/Cold)**: Long-term retention (7+ years) for regulatory compliance and historical re-training, using Azure Archive Storage (Offline).
3.  **Partitioning Strategy**: Data will be partitioned by `Region / Year / Month / Day / VehicleID` to optimize query performance and data deletion (GDPR/APPI).
4.  **Storage Format**: Use **Apache Parquet** for metadata and **H.265/AV1** for video to maximize compression ratios.

## Consequences
### Positive
- Ensures the system can scale to 6.5M+ vehicles without architectural re-design.
- Reduces storage costs by up to 90% through aggressive archiving.
- Simplifies compliance with "Right to be Forgotten" requests through partitioning.

### Negative
- Increased complexity in data retrieval from Archive tier (latency of hours to days).
- Higher management overhead for lifecycle policies.

### Risks
- **Egress Costs**: Transferring data out of the archive for massive re-training could be expensive. 
- **Mitigation**: Perform re-training in the same region as the data lake.
