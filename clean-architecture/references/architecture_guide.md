# Multiplatform Clean Facade Architecture - Reference Guide

This document contains the detailed architectural specifications, layer responsibilities, and directory layouts for the **Feature-Based Clean Architecture** and **Facade Pattern**.

---

## 1. High-Level Dependency Flow

Dependencies only flow downward. Lower layers must never depend on higher layers.

```
View (UI Layer)
    ↓
ViewModel (Presentation State)
    ↓
Service / Use Case (Business Logic & Service Facades)
    ↓
Repository (Data Facades & Cache Control)
    ↓
API Client / Local Storage (Data Sources)
    ↓
Core Infrastructure (Shared Utils & SDK Facades)
```

---

## 2. Layer Responsibilities & Constraints

### View (UI Presentation)
* **Responsibility:** Renders the user interface and forwards user interactions to the ViewModel.
* **Constraints:** MUST NOT build network requests, read databases, execute business logic, or handle raw HTTP/REST responses.

### ViewModel / Presenter
* **Responsibility:** Holds presentation state, maps business models to UI-friendly formats, and triggers Services.
* **Constraints:** MUST NOT execute network operations, access persistence layers, or contain core business validation rules.

### Service / Use Case
* **Responsibility:** Houses platform-agnostic business logic (validation, workflow rules, calculations). Serves as a **Service Facade** when coordinating multiple repositories.
* **Constraints:** MUST remain decoupled from UI frameworks (SwiftUI, Jetpack Compose, Flutter, React). MUST NOT call networking/database clients directly.

### Repository
* **Responsibility:** Abstracts data access. Decides whether to retrieve remote (API) or local (DB/Cache) data. Exposes domain models to Services.
* **Constraints:** MUST serve as a **Data Facade**. Consumers (Services) should never know the underlying source of the data.

### API Client
* **Responsibility:** Interfaces with remote HTTP, GraphQL, or WebSocket APIs.
* **Constraints:** MUST expose strongly typed, simple functions (e.g. `getUser(id)`). MUST NOT expose raw URL building, JSON encoding, or HTTP methods to higher layers.

### Local Storage
* **Responsibility:** Manages data persistence (caching, SQLite, Realm, Hive, secure preferences).
* **Constraints:** MUST NOT contain core business logic. Must only perform CRUD operations.

### Core Infrastructure
* **Responsibility:** Handles shared, cross-cutting concerns (analytics, networking clients, logger engines, feature flag controls).
* **Constraints:** MUST NOT depend on or import feature-specific code. Use **Infrastructure Facades** to encapsulate third-party libraries.

---

## 3. Standard Directory Structures

### Feature Structure
Keep features isolated to maximize code reusability, easy exploration, and safe refactoring.

```text
Features/
  [FeatureName]/
    Models/         # Domain models and Data Transfer Objects (DTOs)
    Views/          # UI Components, Screens, Widgets, SwiftUI/Compose
    ViewModels/     # Presentation state controllers
    Services/       # Feature-specific business logic / Service Facades
    Repository/     # Repository interfaces and implementations
    API/            # Typed endpoints specifically for this feature
    Components/     # Shared feature-level sub-views
    Utilities/      # Feature-local helpers
```

### Core Structure
Only highly reusable, platform-agnostic code lives here:

```text
Core/
    Networking/     # HTTP/Websocket engine configurations, interceptors
    Storage/        # DB drivers, keychain, local cache drivers
    Logging/        # Application-wide logger configurations
    Analytics/      # Shared event tracking interfaces
    Configuration/  # Global constants, feature flags, environments
    Utilities/      # General utilities (date formatters, extensions)
```
