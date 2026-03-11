# ADR-004: Multi-part Data Upload Strategy using SAS Tokens

## Status
Accepted

## Context
Connected vehicles need to upload large binary files (up to 2GB) to the cloud. Routing these files through a central API gateway (like APIM) would create significant performance bottlenecks, increase costs due to double-buffering, and limit the maximum file size.

## Decision
We will implement a **decoupled ingestion strategy** using **Shared Access Signature (SAS) tokens**.

Implementation:
1.  **Handshake**: The vehicle requests an upload URL from the Vehicle-Facing (VF) API.
2.  **Token Issuance**: The VF API verifies the vehicle's JWT and generates a time-limited, scoped SAS token for a specific blob path in ADLS Gen2.
3.  **Direct Upload**: The vehicle performs a multi-part PUT request directly to Azure Blob Storage using the SAS token.
4.  **Completion**: Once all parts are uploaded, the vehicle notifies the VF API, which then commits the blob and triggers the processing pipeline via Event Grid.

## Consequences
### Positive
- **High Scalability**: Offloads the heavy lifting of data transfer to the cloud's native storage backbone.
- **Lower Latency**: Reduces network hops.
- **Cost Reduction**: Eliminates the need for expensive API gateway instances scaled for data throughput.

### Negative
- Requires more complex client-side logic in the vehicle for multi-part upload and retry handling.
- SAS token lifecycle must be strictly managed to prevent security leaks.

### Risks
- If SAS tokens are leaked, they provide direct access to the storage path until they expire.
- Network instability during direct upload requires robust resumable upload implementations on the device.
