# Composition Over Inheritance Guidelines

Composition Over Inheritance is a fundamental object-oriented design principle stating that classes should achieve polymorphic behavior and code reuse by containing references to other objects (composition) rather than extending a parent class (inheritance).

---

## 1. Core Concept

*   **Inheritance (Is-A relationship):** A class extends a parent class, inheriting all its behaviors and attributes. This creates a tight compile-time coupling and can lead to the "fragile base class problem."
*   **Composition (Has-A relationship):** A class contains instances of other helper classes as dependencies, delegating work to them. This allows flexible runtime behavior changes and cleaner unit testing.
*   **Polymorphism via Interfaces:** Use protocols or interfaces to define shared behaviors, and compose objects that implement these interfaces.

---

## 2. Design Guidelines

*   **Avoid Subclassing for Reuse:** You SHALL NOT create subclass hierarchies solely to share utility functions or minor behaviors. You MUST extract these behaviors into separate, composed helper classes.
*   **Use Protocols/Interfaces:** You MUST define behaviors using interfaces or protocols. Classes that exhibit this behavior MUST implement the interface and compose the required dependencies.
*   **Favor Flat Hierarchies:** You MUST limit class inheritance depth. Ideally, keep inheritance depth to 0 or 1.
*   **Delegate Tasks:** A class composed of dependencies MUST delegate tasks to those dependencies (e.g., instead of a `SecureRepository` extending a `BaseRepository`, the `SecureRepository` should implement `Repository` and compose a basic `Repository` instance inside it, delegating calls to it after performing security validation).

---

## 3. Common Anti-Patterns

*   **Fragile Base Class:** Modifying a method in a parent class (e.g., `BaseController`) inadvertently breaking behaviors in dozens of subclass controllers.
*   **Rigid Deep Hierarchies:** Creating deeply nested class chains (e.g., `AdminUserViewModel` extends `VerifiedUserViewModel` which extends `UserViewModel` which extends `BaseViewModel`).
*   **Utility Base Classes:** Creating general-purpose abstract parent classes (e.g. `BaseComponent`, `BaseService`) that contain dozens of unrelated utility helper methods.
*   **Inheriting to Overwrite:** Inheriting from a large class and overriding 90% of its methods to disable them, violating the Liskov Substitution Principle.
