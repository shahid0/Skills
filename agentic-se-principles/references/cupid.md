# CUPID Design Principles Guide

CUPID is a design quality framework created by Dan North as an alternative to SOLID, focusing on code properties that make software a joy to work with.

---

## 1. Core Concept

CUPID focuses on qualities that code exhibits rather than rigid rules:
*   **C - Composable:** Code plays well with others; small components with minimal dependencies that fit together easily.
*   **U - Unix Philosophy:** Components do one thing and do it well, keeping scopes focused and simple.
*   **P - Predictable:** Code behaves exactly as expected; it is standard, deterministic, and free of surprises.
*   **I - Idiomatic:** Code uses the standard styles, tools, and idioms of the language and community.
*   **D - Domain-Driven:** Code models the domain in its structure and language rather than technical implementation details.

---

## 2. Design Guidelines

*   **Composable:** You MUST write modules/classes with clean input/output parameters. You SHALL NOT tightly couple business logic to specific framework components.
*   **Unix Philosophy:** You MUST keep your functions and classes small. A class or method MUST have a single, clear responsibility.
*   **Predictable:** You MUST write deterministic code. If a method is named `calculateTotal()`, it MUST NOT modify state or run asynchronous network requests.
*   **Idiomatic:** You MUST adhere to the target language's formatting and style guides (e.g., Swift's API design guidelines, Kotlin coding conventions, Dart lints, TypeScript ESLint rules).
*   **Domain-Driven:** You MUST use the vocabulary of the business (ubiquitous language) in your variable, class, and method names.

---

## 3. Common Anti-Patterns

*   **Mega-Components (Anti-Unix):** Classes or modules that handle UI, business rules, networking, and caching all at once.
*   **Surprising Side Effects (Anti-Predictable):** Calling a getter method that triggers network syncs, writes to a database, or raises exceptions.
*   **"Clever" Non-Standard Solutions (Anti-Idiomatic):** Reinventing custom list structures or custom async frameworks instead of using standard language APIs (e.g., using raw threads instead of async/await).
*   **Technical Language Leakage (Anti-Domain):** Naming domain entities after databases or tables (e.g. `SqlRowUserDtoManager` instead of `UserProfile`).
