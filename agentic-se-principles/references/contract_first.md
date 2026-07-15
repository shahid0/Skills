# Contract-First Design Guidelines

Contract-First design is a methodology where developers define the interface agreements (contracts) between services, client-server applications, or internal modules *before* writing any code.

---

## 1. Core Concept

In Contract-First design, the contract is the source of truth:
*   **The Interface Contract:** A machine-readable, declarative schema (e.g. OpenAPI/Swagger for HTTP, Protocol Buffers for gRPC, JSON Schema, GraphQL schemas) defining exactly what data is exchanged, query parameters, types, headers, and error codes.
*   **Decoupled Development:** Once the contract is finalized, frontend and backend teams (or different service teams) can work in parallel using mock servers generated directly from the contract.
*   **Codegen Integration:** Code generators (e.g. OpenAPI Generator, Protoc) translate the contract into strongly typed client SDKs, models, and server stubs, ensuring type safety.

---

## 2. Design Guidelines

*   **Contract Isolation:** You MUST define the interface schema (e.g., OpenAPI YAML, protobuf `.proto` files) before writing any API endpoints, clients, or database tables.
*   **Single Source of Truth:** The contract MUST remain the authoritative source of truth. You SHALL NOT modify generated code by hand. If an API signature needs to change, you MUST edit the contract first and regenerate the code.
*   **Strict Type Enforcement:** You MUST specify types, validation constraints (e.g. ranges, patterns), required fields, and nullability options in the contract.
*   **Mock Verification:** You MUST set up API mock servers based directly on the contract during development, allowing client-side views and viewmodels to be tested before backend endpoints are built.

---

## 3. Common Anti-Patterns

*   **Implementation-First (Code-First):** Writing backend controllers and database tables first, and then using a library to generate the Swagger docs from the code. This causes client teams to block on implementation and leads to fragile API shapes.
*   **Manual Generated Code Edits:** Modifying regenerated files (like API models or network clients) directly. These edits are lost the next time code is regenerated from the contract.
*   **Vague Contract Schemas:** Defining parameters or responses as untyped blobs (e.g., `object`, `any`, `Map<String, Any>`) instead of declaring explicit schemas.
*   **Drift between Code and Contract:** Allowing the API contract and the running code to drift, leading to runtime failures due to mismatched parameters or response shapes.
