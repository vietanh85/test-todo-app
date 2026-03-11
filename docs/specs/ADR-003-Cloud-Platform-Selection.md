# ADR-003: Selection of Azure as the Primary Cloud Platform for NOA DataOps

## Status
Accepted

## Context
The NOA DataOps platform requires high-throughput data ingestion, large-scale media (video/image) processing with GPU acceleration, and seamless integration with existing data ecosystems (Snowflake). We evaluated AWS, Azure, and Google Cloud Platform (GCP) against these requirements, focusing on scalability, cost-efficiency, and technical compatibility with ADAS training workflows.

## Decision
We have selected **Microsoft Azure** as the primary cloud platform for the NOA DataOps system development (Phase 1).

Key reasons for this decision include:
1. **Media Processing:** Azure provides high-performance GPU instances (Azure Batch GPU) that are well-suited for the intensive video/image processing and "Natural Anonymization" tasks required.
2. **Databricks Integration:** Azure Databricks offers a first-class, natively integrated experience on Azure, which is the cornerstone of our medallion-based Lakehouse architecture.
3. **Cost Efficiency:** Comparative analysis showed that Azure offers more competitive pricing for large-scale GPU workloads and tiered storage (ADLS Gen2) compared to AWS for this specific use case.
4. **Governance:** Azure Purview and Microsoft Sentinel provide integrated governance and security logging that meet Honda's strict compliance requirements for PII and data lineage.
5. **Existing Ecosystem:** Azure provides superior connectivity and lower egress costs for integration with enterprise systems like Snowflake.

## Consequences
### Positive
- Accelerated development using native Azure integrations (Event Grid, Azure Data Factory).
- Enhanced security via Azure Defender for Cloud and Microsoft Entra ID.
- Up to 85% cost reduction in storage through automated lifecycle management policies.

### Negative
- Potential vendor lock-in for certain managed services (e.g., Azure AI Vision), though mitigated by a container-first deployment strategy.

### Risks
- Regional service availability differences between Tokyo and Oregon, requiring careful Terraform orchestration.
- Integration complexity with non-Azure authentication platforms (mitigated by using mTLS and standardized JWTs).
