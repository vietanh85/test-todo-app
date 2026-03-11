# ADR-001: Selection of Microsoft Azure as the Primary Cloud Platform

## Status
Accepted

## Context
The NOA DataOps platform requires a robust cloud infrastructure to handle massive-scale video data ingestion, high-performance AI processing, and integration with existing enterprise systems. The selection was between AWS, Google Cloud, and Microsoft Azure.

## Decision
We have decided to select **Microsoft Azure** as the primary cloud platform for Phase 1 and Phase 2 of the NOA DataOps project.

Key drivers for this decision:
1.  **Databricks Synergy**: Azure Databricks provides a first-class managed service for the Lakehouse architecture, which is central to our data processing strategy.
2.  **AI Vision Capabilities**: Azure AI Vision and GPU-accelerated batch processing are highly optimized for the image/video processing workloads required for ADAS.
3.  **Integration with Snowflake/Internal Systems**: Strong existing ecosystem connectivity with Snowflake and Power BI.
4.  **Governance**: Microsoft Purview offers advanced, enterprise-grade data cataloging and governance that aligns with Honda's compliance requirements.
5.  **Cost Efficiency**: Better cost-performance ratio for large-scale GPU workloads and data transfer within the Azure ecosystem.

## Consequences
### Positive
- Accelerated development using mature managed services (AKS, Databricks, ADF).
- Simplified compliance with global privacy laws through built-in governance tools.
- Stronger alignment with enterprise BI and data warehousing standards.

### Negative
- Initial dependency on Azure-specific APIs (mitigated by using K8s and Terraform for Cloud-agnostic design).

### Risks
- Vendor lock-in if cloud-native services are used without abstraction layers.
