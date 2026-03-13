# ADR-002: Eventual Consistency for Pre-Checkout Inventory Availability

## Status
Accepted

## Context
The shopping cart must dynamically display real-time pickup availability (e.g., Apple Marunouchi, March 22, 2026) and home delivery dates (e.g., zip 102-0091, March 20-22, 2026) while viewing items in the cart. However, locking physical inventory in the relational database the moment an item is added to the cart leads to severe inventory starvation and database contention, especially during high-demand product launches (e.g., M5 Pro MacBook Pro).

## Decision
We will adopt an **Eventually Consistent** model for inventory reads during the browsing and cart-building phases, and transition to **Strong Consistency** only at the final checkout transaction.
- The frontend client will query a high-performance Redis cluster (Inventory Read Model) that is updated via asynchronous domain events (Kafka) from the core Inventory Database.
- The cache will store "Available to Promise" (ATP) quantities and fulfillment dates per SKU per store/warehouse location.
- When the user clicks "Apple Payで注文手続きを行う" (Proceed to Checkout), a synchronous, strongly consistent transaction will execute against the primary Inventory DB (PostgreSQL) to soft-allocate the item, followed by a hard allocation upon payment success.

## Consequences
### Positive
- Massive reduction in database lock contention and connection pooling exhaustion during high-traffic events.
- Sub-10ms read latency for displaying pickup/delivery dates in the cart UI, enhancing user experience.
- Improves overall system scalability, fault tolerance, and resilience by effectively decoupling the read and write paths (implementing the CQRS pattern for inventory).

### Negative
- Introduces the potential for "overselling" at the UI level: A user may see an item as "Available" in the cart, but it could sell out before they complete checkout, leading to a negative user experience ("Sorry, this item is no longer available").
- Increased architectural complexity due to the introduction of Kafka event streams and eventual consistency reconciliation logic.

### Risks
- **Replication/Processing Lag**: If the asynchronous event stream processing lags, the Redis cache becomes stale, increasing the false-positive availability rate.
  - *Mitigation*: Setting aggressive TTLs on high-velocity SKUs, implementing real-time Kafka consumer lag monitoring, and dynamically scaling the consumer group based on the backlog.