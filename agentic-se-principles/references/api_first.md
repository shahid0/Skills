# API-First Design Guidelines

API-First design is a development strategy that treats APIs as first-class citizens. It means designing the application's APIs around the user/client needs first, before implementing the underlying database schemas, UI layouts, or business workflows.

---

## 1. Core Concept

API-First ensures that the application's boundaries are clean, highly accessible, and standardized:
*   **APIs as the Core Product:** The API is treated as a product rather than a side effect of database schema design.
*   **Client-Centric Design:** Design APIs around how client devices (mobile apps, web apps, IoT devices, partner integrations) will consume the data, minimizing the number of network roundtrips.
*   **Integration Ease:** Ensures that the system is easily integrable and composable with other services from the outset.

---

## 2. Design Guidelines

*   **API Boundary Autonomy:** You MUST design your API endpoints and signatures based on the business requirements of the clients. You SHALL NOT expose database schemas or table keys directly through the API.
*   **Strict Documentation:** Every API endpoint MUST be documented using standard specifications (OpenAPI, AsyncAPI). The API documentation MUST be updated and published before development begins.
*   **Consumer-Driven Versioning:** You MUST design versioning strategies (e.g. URI versioning `/v1/`, header versioning) into the API from day one. You SHALL NOT introduce breaking changes to existing endpoints without deprecating old versions.
*   **Platform Neutrality:** APIs MUST be designed using platform-neutral protocols and data formats (JSON, Protobuf) to ensure any client stack can interact with them.

---

## 3. Common Anti-Patterns

*   **Database-Driven APIs:** Automatically exposing database tables as REST endpoints (e.g., exposing auto-incrementing integer IDs or internal foreign keys).
*   **Chatty APIs:** Designing APIs that force a client to make multiple sequential calls to display a single screen (e.g., call `/orders` then call `/order-items/{id}` ten times to get prices).
*   **Unversioned Endpoint Changes:** Modifying API response formats or renaming fields directly in production, breaking existing mobile app installations and third-party integrations.
*   **Lack of Error Standardization:** Exposing raw stack traces, database error messages, or using inconsistent HTTP status codes (e.g., returning HTTP 200 with an error message in the response body).
