# ADR-004: Scalability Projections and Storage Strategy for 2040 Horizon

## Status
Proposed

## Context
The initial architecture for NOA OutCAR DataOps estimated a daily ingestion of 65TB for 6.5 million vehicles by 2040. A design review identified this as a significant understatement. Even if each vehicle only uploads 100MB of telemetry and high-value event-based video per day, 6.5 million vehicles would produce ~650TB/day. For full SDV (Software-Defined Vehicle) support, this could easily scale to several Petabytes (PB) per day.

We need a revised projection and a clear storage strategy to handle Exabyte-scale archives without cost spirals.

## Decision
We will design the system for **Exabyte-scale** total storage capacity and **Petabyte-scale** daily ingestion.

Key strategy components:
1. **Revised Scale (2040):**
   - **Active Fleet:** 6.5 Million Vehicles.
   - **Daily Ingestion Target:** 500TB - 2PB per day.
   - **Peak Ingress:** 100,000 requests per second (rps).
2. **Aggressive Edge Filtering:**
   - Vehicles will use local AI models to select only "high-value" frames/clips (e.g., edge cases, disengagements) to avoid uploading junk data.
   - Target reduction: 99% of raw vehicle sensor data discarded at the edge.
3. **Tiered Storage Architecture:**
   - **Hot (SSD/Premium):** First 7 days for immediate AI training and active validation.
   - **Cool:** Days 8-90 for long-term ETL and periodic re-training.
   - **Archive (LRS/ZRS):** 90+ days for regulatory compliance and historic data mining.
4. **Data Compaction:**
   - Use of efficient binary formats (Parquet/Avro for metadata, H.265/AV1 for video) to minimize footprint.
5. **Partitioning Strategy:**
   - Physical partitioning by `Year/Month/Day/Region/VehicleID` to ensure performant queries on massive datasets.

## Consequences
### Positive
- Future-proof architecture capable of handling the 2040 vision.
- Predictable cost model via tiered storage and edge pre-processing.
- High query performance for AI engineers through effective partitioning.

### Negative
- Increased complexity in edge software (requires sophisticated trigger logic).
- Significant infrastructure management overhead for massive K8s clusters and storage accounts.

### Risks
- **Egress/Ingress Costs:** Even with Azure's competitive pricing, Petabyte-scale movement is expensive.
  - *Mitigation:* Multi-region ingestion points (Edge Zones) to minimize long-distance transit.
- **Storage Limits:** Azure Storage account limits may be reached.
  - *Mitigation:* Implement a "Storage Account Sharding" pattern at the Gateway level.
