# Technical Specification: Vehicle-Facing Gateway (VFG)

## 1. Introduction
The Vehicle-Facing Gateway (VFG) is the secure entry point for all vehicle-to-cloud communications. It handles authentication, configuration distribution (provisioning/triggers), and initial data ingestion.

## 2. Technical Stack
- **Framework**: Java 21 / Spring Boot 3.x
- **Runtime**: Azure Kubernetes Service (AKS) with HPA (Horizontal Pod Autoscaler).
- **Communication Protocols**: 
    - HTTPS/REST for metadata and small uploads.
    - mTLS (Mutual TLS) for transport layer security.
- **Service Mesh**: Istio for mTLS termination and traffic management.

## 3. Core Functions

### 3.1 Authentication & Token Exchange
Vehicles use a factory-provisioned client certificate to initiate an mTLS connection.
- **Endpoint**: `POST /v1/auth/token`
- **Logic**: VFG validates the certificate against the Root CA. Upon success, it calls the *Connected Auth Platform* to issue a short-lived JWT.
- **Degraded Mode**: If the *Connected Auth Platform* is unreachable, the VFG enters a "Degraded Mode" where it allows "Critical Telemetry" uploads based solely on mTLS certificate validity, while pausing "Large Video Uploads" to protect system stability.

### 3.2 Configuration Distribution (Trigger Files)
"Trigger Files" define the logic for data collection (e.g., "Collect 10s of video if hard braking is detected at GPS X,Y").
- **Mechanism**: **Pull-based with CDN Caching**.
- **Endpoint**: `GET /v1/trigger`
- **Design**: VFG generates a signed URL for the latest trigger configuration stored in Blob Storage. Large-scale distribution is offloaded to **Azure Front Door (CDN)** to minimize VFG load.

### 3.3 Data Upload Orchestration
- **Multipart Upload (Files > 10MB)**:
    1. Vehicle calls `POST /v1/upload/init` with file metadata.
    2. VFG validates the request and generates a **Shared Access Signature (SAS)** URL for direct-to-blob upload.
    3. Vehicle uploads chunks directly to ADLS Gen2.
    4. Vehicle calls `POST /v1/upload/complete`. VFG then triggers the processing pipeline via Event Grid.
- **Direct Upload (Files <= 10MB)**:
    - Vehicle sends binary data in the request body to `POST /v1/upload/direct`.
    - VFG performs a quick virus scan and writes to the Landing Zone.

### 3.4 Storage Account Sharding
To overcome Azure Storage account IOPS and throughput limits at PB-scale, the VFG implements a sharding logic:
- **Mechanism**: Consistent hashing of the `vehicle_id`.
- **Logic**: `target_storage_account = shard_map[hash(vehicle_id) % total_shards]`
- **Implementation**: The VFG retrieves the shard map from the *Configuration Service* and generates the SAS URL pointing to the designated shard.

## 4. Scalability & Availability
- **Throughput**: Designed to handle 65,000+ RPS.
- **Global Distribution**: VFG instances deployed in multiple regions (Tokyo, Oregon). Azure Front Door routes vehicles to the nearest healthy instance.
- **Resiliency**: Circuit breaker pattern implemented for downstream calls to Auth and Database services.

## 5. Security
- **mTLS**: Required for all endpoints.
- **JWT**: Required for all endpoints except `/auth/token`.
- **Throttling**: Rate limiting applied per `vehicle_id` to prevent DDoS/misbehaving clients.
