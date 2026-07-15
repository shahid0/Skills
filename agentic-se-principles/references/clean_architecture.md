# Clean Architecture Guidelines

Clean Architecture is a software design philosophy that isolates core business logic from external frameworks, user interfaces, databases, and third-party tools.

---

## 1. Core Concept

The system is organized into concentric layers. The overriding rule in Clean Architecture is the **Dependency Rule**: source code dependencies can only point inward.
*   **Entities (Domain Models):** Core business objects and data structures.
*   **Use Cases (Services):** Orchestrate the flow of data to and from entities, executing business logic.
*   **Interface Adapters (ViewModels/Repositories):** Convert data from the format most convenient for use cases and entities to the format most convenient for external agencies (UI/Web/Database).
*   **Frameworks & Drivers (Views/DB/Network Clients):** The outermost layer containing concrete details like databases, UI frameworks, and HTTP clients.

---

## 2. Design Guidelines

*   **Inward Dependencies:** You MUST ensure dependencies only flow inward. Lower layers (e.g. Services, Entities) SHALL NOT import or depend on higher layers (e.g. ViewModels, Views, API clients).
*   **UI Independence:** The business logic (Services/Entities) MUST remain completely decoupled from the UI. You SHALL NOT import UI-related frameworks (SwiftUI, Jetpack Compose, Flutter material, React) into Domain or Use Case layers.
*   **Database & Network Independence:** Use Cases MUST NOT know where data is stored or fetched. You MUST abstract databases, local caching, and remote HTTP operations behind Repository interfaces.
*   **Model Isolation:** You MUST map database entities (SQL records, schemas) and API data transfer objects (DTOs) into clean, platform-agnostic domain models before passing them to the Use Case or Service layers.

---

## 3. Common Anti-Patterns

*   **Bleeding UI Frameworks:** Importing View models, View Controllers, or UI Widgets into a core Service.
*   **Direct Network Access from VMs:** ViewModels or controllers building HTTP requests or calling APIs directly instead of utilizing a Repository.
*   **Leaking SQL/DTO Types:** Passing raw database entity models (e.g., HiveObjects, Room Entities, SQLite Row structures) or raw JSON API response objects directly to Use Cases or Views.
*   **Circular Dependencies:** Having a Repository import a Service, or a Service import a ViewModel, creating tight import loops that break modular compilation.
