# ADR-001: Integration with Third-Party Financing Provider (Paidy)

## Status
Accepted

## Context
The e-commerce platform needs to support 0% interest, 24-month installment plans for high-value SKUs (e.g., the M5 Pro 16-inch MacBook Pro, priced at 569,800 JPY). Building an in-house financing, real-time credit-check, and installment collection system requires significant regulatory compliance, financial risk management, and operational overhead, specifically within the Japanese market. We need a way to offer seamless split payments without taking on the underlying credit risk or debt management.

## Decision
We will integrate with Paidy via their API to handle all installment-based payments ("ペイディあと払いプランApple専用"). 
* The **Pricing & Tax Service** will calculate the monthly display value (Total / 24 = 23,741 JPY/mo) dynamically for the frontend UI.
* The frontend will utilize the Paidy SDK/redirect flow upon checkout initiation.
* The **Cart/Order Service** will rely on a synchronous webhook or API callback from Paidy to confirm the authorized amount before finalizing the order state and allocating inventory.

## Consequences
### Positive
- Offloads all consumer credit risk, fraud liability, and debt collection processes to a specialized third party (Paidy).
- Drastically reduces PCI and local Japanese financial regulatory compliance scope for the core commerce platform.
- Faster time-to-market compared to building a proprietary financing and ledger backend.
- Potentially higher conversion rates due to Paidy's existing, verified user base in Japan.

### Negative
- Introduces a hard dependency on a third-party API for a critical path (checkout completion).
- Requires complex UX edge-case handling (e.g., if a user is rejected for credit by Paidy mid-checkout, or if their cart contains mixed eligible/ineligible items).
- Adds network latency to the final checkout step during the synchronous authorization call.

### Risks
- **Third-Party Downtime**: If the Paidy API is down or degraded, customers cannot complete financed purchases. *Mitigation*: Gracefully degrade the UI by hiding the installment option or clearly falling back to standard Apple Pay/Credit Card payment methods.
- **Data Synchronization**: Potential discrepancies between our calculated order total and the amount authorized by Paidy. *Mitigation*: Strict implementation of idempotency keys, robust amount validation in the webhook handler, and automated reconciliation reports.