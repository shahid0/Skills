# Domain-Driven Design (DDD) Guidelines

Domain-Driven Design is an approach to software development that centers the design on a highly structured model of the business domain and its rules.

---

## 1. Core Concept

DDD aligns the codebase structure with the business model using a set of tactical patterns:
*   **Ubiquitous Language:** Common, shared terminology used consistently by both domain experts (business) and developers in conversation and code.
*   **Entities:** Objects with a distinct, persistent identity that remains consistent across attribute changes (e.g. `User`, `Order`).
*   **Value Objects:** Immutable objects defined solely by their attributes, with no conceptual identity (e.g. `Money`, `Address`, `EmailAddress`). Two value objects with identical attributes are considered equal.
*   **Aggregates:** A cluster of associated objects treated as a single transactional unit. The **Aggregate Root** is the only gatekeeper through which external objects can interact with the aggregate.
*   **Repositories:** Provide access to Aggregate Roots, abstracting persistence mechanisms.
*   **Domain Services:** House business logic that doesn't naturally fit inside a single Entity or Value Object.

---

## 2. Design Guidelines

*   **Ubiquitous Language:** You MUST name classes, methods, and variables using domain terminology. Avoid technical suffixes in domain logic (e.g., use `Account` instead of `AccountModel` or `AccountTable`).
*   **Value Object Immutability:** Value Objects MUST be immutable (e.g., in Swift, use read-only structs; in Kotlin, use read-only data classes; in Dart, use `@immutable` classes). You SHALL NOT expose setters on a Value Object.
*   **Aggregate Boundary Integrity:** External objects MUST NOT reference or modify internal entities within an Aggregate. External objects MUST only reference the **Aggregate Root** (e.g., you can load an `Order`, but you cannot modify an `OrderItem` directly without going through the `Order` root).
*   **Encapsulated Domain Logic:** Entities and Value Objects MUST enforce their own invariants (rules). Validation MUST happen inside the constructors or creation methods (factory patterns) of these objects to prevent invalid state (e.g., an `EmailAddress` constructor MUST throw/return an error if the email format is invalid).

---

## 3. Common Anti-Patterns

*   **Anemic Domain Model:** Entities that are simple data bags containing only getters and setters, while all business logic is placed in bloated Service classes.
*   **Mutable Value Objects:** Modifying properties of value objects (like changing the currency or amount of a `Money` instance) rather than instantiating a new instance.
*   **Direct Sub-Entity Queries:** Allowing repository clients to query and save nested entities (like retrieving a `LineItem` directly from the database) instead of accessing them via their Aggregate Root (`Order`).
*   **Leaking Infrastructure into DDD:** Importing database libraries, network clients, or serialization logic (like JSON parsing keys) directly into Domain Entities or Value Objects.
