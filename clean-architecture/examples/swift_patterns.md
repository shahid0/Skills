# Swift/SwiftUI Clean Facade Architecture Examples

Concrete examples demonstrating Repository, Service, and SDK facades using Swift and SwiftUI.

---

## 1. Repository Facade
Encapsulates remote API requests and local CoreData/SwiftData storage behind a simple Swift protocol.

```swift
// 1. Domain Model
struct UserProfile: Identifiable {
    let id: String
    let email: String
}

// 2. Repository Interface
protocol UserRepository {
    func getUserProfile(id: String) async throws -> UserProfile
}

// 3. Concrete Repository Facade (Coordinates REST API client and SwiftData cache)
class UserRepositoryImpl: UserRepository {
    private let apiClient: UserApiClient
    private let localCache: UserCache
    
    init(apiClient: UserApiClient, localCache: UserCache) {
        self.apiClient = apiClient
        self.localCache = localCache
    }
    
    func getUserProfile(id: String) async throws -> UserProfile {
        if let cached = try? await localCache.fetch(id: id) {
            return cached
        }
        let rawDto = try await apiClient.fetchUserProfile(id: id)
        let domainModel = UserProfile(id: rawDto.id, email: rawDto.email)
        try? await localCache.save(domainModel)
        return domainModel
    }
}
```

---

## 2. Service Facade
Coordinates multiple Swift repositories to orchestrate business logic workflows.

```swift
// Service coordinating multiple repositories for a user onboarding workflow
class SwiftUIOnboardingService {
    private let authRepo: AuthRepository
    private let profileRepo: ProfileRepository
    private let tracker: AnalyticsTracker
    
    init(authRepo: AuthRepository, profileRepo: ProfileRepository, tracker: AnalyticsTracker) {
        self.authRepo = authRepo
        self.profileRepo = profileRepo
        self.tracker = tracker
    }
    
    func completeOnboarding(email: String, name: String) async throws -> String {
        let user = try await authRepo.registerUser(email: email)
        try await profileRepo.setupProfile(userId: user.id, name: name)
        tracker.trackEvent("swift_onboarding_completed", properties: ["user_id": user.id])
        return user.id
    }
}
```

---

## 3. Infrastructure SDK Facade
Wraps third-party iOS libraries (like Sentry or Firebase Analytics) behind custom protocols.

```swift
protocol AnalyticsTracker {
    func trackEvent(_ name: String, properties: [String: Any]?)
}

class FirebaseTrackerImpl: AnalyticsTracker {
    func trackEvent(_ name: String, properties: [String: Any]?) {
        // Under-the-hood Google Analytics/Firebase SDK call
        // Analytics.logEvent(name, parameters: properties)
    }
}
```
