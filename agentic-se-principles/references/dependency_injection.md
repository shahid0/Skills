# Dependency Injection Guidelines

Dependency Injection (DI) is a software design pattern where an object receives its dependencies from an external source (injector) rather than creating them itself.

---

## 1. Core Concept

*   **Dependency Inversion Principle:** High-level modules should not depend on low-level modules; both should depend on abstractions.
*   **Inversion of Control (IoC):** The control of creating and linking dependencies is shifted from the class itself to the system framework or composition root.
*   **DI Types:**
    *   **Constructor Injection:** Passing dependencies via the class constructor (preferred).
    *   **Method Injection:** Passing dependencies as parameters to specific methods.
    *   **Property Injection:** Setting dependencies via public properties (to be used sparingly).

---

## 2. Design Guidelines

*   **Constructor Injection:** You MUST use constructor injection as the default mechanism for providing dependencies.
*   **Program to Abstractions:** You MUST inject interface/protocol types rather than concrete implementations (e.g. inject `BookRepository` rather than `BookRepositoryImpl`).
*   **Composition Root:** You MUST configure and instantiate your dependencies in a single centralized location (the **Composition Root**, such as a Main class, a DI container module, or a routing coordinator).
*   **Decoupled Creation:** Classes SHALL NOT instantiate their dependencies using the `new` keyword (or platform equivalent) within their methods or constructors.

---

## 3. Common Anti-Patterns

*   **Hardcoded Dependencies:** Instantiating helper classes directly inside constructors (e.g., `init() { self.apiClient = RealApiClient() }`). This makes unit testing with mock dependencies impossible.
*   **Service Locator (Anti-Pattern):** Injecting a dependency container or locator directly into a class so the class can query for its own dependencies (e.g., `init(container: DIContainer) { self.api = container.resolve(ArticleApi.self) }`). This hides the class's true dependencies.
*   **Monolithic Initializers:** Classes with too many constructor dependencies, indicating they have too many responsibilities and violate the Single Responsibility Principle.
*   **Global Singletons:** Relying on global, shared singletons (e.g., `ApiClient.shared.fetch()`) instead of injecting the dependency, which creates hidden couplings and state pollution.
