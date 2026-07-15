# Swift / SwiftUI - Agentic SE Principles Examples

This document demonstrates CUPID, DDD, Dependency Injection, Composition, and Observability-First design using Swift.

---

## 1. Domain-Driven Design: Value Object (Immutable Struct)
Enforces its own invariants upon creation (cannot represent invalid state).

```swift
import Foundation

struct EmailAddress: Hashable, Codable {
    let rawValue: String
    
    enum ValueError: Error {
        case invalidFormat
    }
    
    // Invariant Enforcement
    init(rawValue: String) throws {
        let emailRegex = #"^[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,64}$"#
        let predicate = NSPredicate(format:"SELF MATCHES %@", emailRegex)
        guard predicate.evaluate(with: rawValue) else {
            throw ValueError.invalidFormat
        }
        self.rawValue = rawValue.lowercased()
    }
}
```

---

## 2. Dependency Injection & Constructor-Based Composition
Programming to abstractions. Dependencies are injected via the constructor rather than instantiated inside.

```swift
protocol PaymentGateway {
    func processPayment(amount: Double) async throws -> Bool
}

class CheckoutService {
    private let paymentGateway: PaymentGateway
    private let cartRepository: CartRepository
    
    // Constructor Injection
    init(paymentGateway: PaymentGateway, cartRepository: CartRepository) {
        self.paymentGateway = paymentGateway
        self.cartRepository = cartRepository
    }
    
    func checkout(userId: String) async throws -> Bool {
        let total = try await cartRepository.fetchTotal(for: userId)
        return try await paymentGateway.processPayment(amount: total)
    }
}
```

---

## 3. Composition Over Inheritance (Decorator Pattern)
Adding logging behavior to a repository without subclassing or modifying the base implementation.

```swift
protocol BookRepository {
    func getBook(id: String) async throws -> Book
}

// 1. Base Implementation
class BookRepositoryImpl: BookRepository {
    func getBook(id: String) async throws -> Book {
        // Fetch from API...
        return Book(id: id, title: "Clean Code")
    }
}

// 2. Composed Decorator (No inheritance from BookRepositoryImpl)
class LoggingBookRepository: BookRepository {
    private let decorated: BookRepository
    private let logger: AppLogger
    
    init(decorated: BookRepository, logger: AppLogger) {
        self.decorated = decorated
        self.logger = logger
    }
    
    func getBook(id: String) async throws -> Book {
        logger.logInfo("Fetching book with ID: \(id)")
        do {
            let book = try await decorated.getBook(id: id)
            logger.logInfo("Successfully fetched book: \(book.title)")
            return book
        } catch {
            logger.logError("Failed to fetch book \(id)", error: error)
            throw error
        }
    }
}
```

---

## 4. Observability-First: Structured Logging & Tracing Spans
Logging with context tags and tracing asynchronous operations.

```swift
import OSLog

struct LogContext {
    let traceId: String
    let userId: String
}

class UserService {
    private let logger = Logger(subsystem: "com.app.user", category: "UserService")
    
    func updateUserProfile(userId: String, context: LogContext) async {
        // Structured Logging using OSLog interpolation and context metadata
        logger.info("Starting profile update for user: \(userId, privacy: .public) [TraceID: \(context.traceId)]")
        
        do {
            // Asynchronous tracking span
            try await saveProfileData(userId: userId)
            logger.info("Successfully updated profile for user: \(userId, privacy: .public) [TraceID: \(context.traceId)]")
        } catch {
            logger.error("Failed profile update for user: \(userId, privacy: .public) [TraceID: \(context.traceId)] - Error: \(error.localizedDescription)")
        }
    }
    
    private func saveProfileData(userId: String) async throws {
        // Save database rules...
    }
}
```
