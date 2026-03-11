# ADR-001: Automated Metadata-Driven Ingestion Strategy

## Status
Proposed

## Context
American Honda Motor Co., Inc. (AHM) currently faces challenges with fragmented data ingestion processes, leading to high AWS infrastructure costs and a lack of automation. The Proof-of-Concept (POC) requires a scalable, cost-effective solution that ensures <1% ingestion error rate and 100% schema compliance.

## Decision
We propose the implementation of an **Automated Metadata-Driven Ingestion Framework**. 

Key components of this decision include:
1. **AWS Glue for ETL:** Using serverless ETL to handle transformation and schema mapping dynamically.
2. **Infrastructure as Code (Terraform):** All environments (A-DASH NA) and resources (S3, Redshift, RDS) will be managed via Terraform to ensure consistency and ease of deployment.
3. **Automated Quality Checks:** Integrating a validation layer within the pipeline to enforce schema compliance before loading into the data warehouse (Redshift).

## Consequences

### Positive
- **Cost Efficiency:** Serverless scaling and optimized resource utilization are expected to meet the 10% cost reduction target.
- **Reliability:** Automated validation reduces manual errors and ensures high technical quality.
- **Consistency:** Terraform-managed infrastructure ensures alignment across development, staging, and production environments.

### Negative
- **Initial Complexity:** Designing a flexible metadata-driven framework requires more upfront effort than hard-coded pipelines.
- **AWS Glue Costs:** While serverless, poorly optimized Glue jobs can incur significant costs if not monitored correctly.

### Risks
- **Knowledge Transfer:** The FPT team needs to ensure the AHM internal team is fully trained to manage the metadata-driven architecture post-POC.
- **Tooling Constraints:** Reliance on specific AWS services (Redshift, Glue) creates a tighter coupling with the AWS ecosystem.
