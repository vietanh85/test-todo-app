# ADR-003: Use of Open Table Formats (Delta Lake) for the Data Lakehouse

## Status
Accepted

## Context
Storing massive amounts of unstructured and semi-structured data in a standard object store (ADLS Gen2) makes it difficult to perform reliable updates, handle schema evolution, and provide high-performance querying for multiple downstream consumers (AI servers, BI tools).

## Decision
We will adopt the **Lakehouse Architecture** using **Delta Lake** as the primary storage format for the Silver and Gold layers.

Key drivers:
1.  **ACID Transactions**: Ensures data reliability during large-scale concurrent writes and deletes.
2.  **Schema Enforcement/Evolution**: Prevents data corruption by ensuring incoming data matches the defined schema.
3.  **Time Travel**: Enables auditability and the ability to reproduce AI training runs using historical snapshots of the data.
4.  **Multi-cloud Readiness**: Delta Lake is an open standard supported by major cloud providers and engines (Databricks, Spark, Trino), facilitating a future multi-cloud transition.

## Consequences
### Positive
- Improved data quality and governance.
- High-performance metadata handling for billions of files.
- Seamless integration with Databricks and Synapse.

### Negative
- Slight storage overhead for transaction logs and historical versions (mitigated by vacuum policies).
- Requires Spark-based engines for complex operations.

### Risks
- Evolution of the Delta Lake protocol vs. competitors like Apache Iceberg.
