# TypeScript / Web Clean Facade Architecture Examples

Concrete examples demonstrating Repository, Service, and SDK facades using TypeScript (React, Vue, Next.js, or NestJS).

---

## 1. Repository Facade
Encapsulates Axios/Fetch API requests and local storage caching (e.g. IndexedDB, LocalStorage, or state cache).

```typescript
// 1. Domain Model
export interface User {
  id: string;
  name: string;
}

// 2. Repository Interface
export interface UserRepository {
  getUser(id: string): Promise<User>;
}

// API Response DTO
interface UserDto {
  id: string;
  display_name: string;
}

// 3. Repository Facade Implementation (Coordinates Fetch API and LocalStorage cache)
export class UserRepositoryImpl implements UserRepository {
  constructor(
    private readonly baseUrl: string,
    private readonly cache: Storage
  ) {}

  async getUser(id: string): Promise<User> {
    // 1. Read from facade local storage cache
    const cachedData = this.cache.getItem(`user_${id}`);
    if (cachedData) {
      return JSON.parse(cachedData) as User;
    }

    // 2. Call remote REST client
    const response = await fetch(`${this.baseUrl}/users/${id}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch user: ${response.statusText}`);
    }
    const rawDto: UserDto = await response.json();

    // 3. Map DTO to domain model
    const user: User = {
      id: rawDto.id,
      name: rawDto.display_name,
    };

    // 4. Update facade cache
    this.cache.setItem(`user_${id}`, JSON.stringify(user));
    return user;
  }
}
```

---

## 2. Service Facade
Coordinates multiple TypeScript repositories or stores to execute business workflows.

```typescript
// Coordinates shopping checkout operations across several repositories
export class CheckoutService {
  constructor(
    private readonly cartRepo: CartRepository,
    private readonly paymentRepo: PaymentRepository,
    private readonly inventoryRepo: InventoryRepository
  ) {}

  async checkout(userId: string): Promise<CheckoutResult> {
    const items = await this.cartRepo.getItems(userId);
    if (items.length === 0) {
      return { success: false, reason: "Cart is empty" };
    }

    const isAvailable = await this.inventoryRepo.verifyStock(items);
    if (!isAvailable) {
      return { success: false, reason: "Some items are out of stock" };
    }

    const total = items.reduce((sum, item) => sum + item.price, 0);
    const paymentProcessed = await this.paymentRepo.processCharge(userId, total);
    if (!paymentProcessed) {
      return { success: false, reason: "Payment failed" };
    }

    await this.cartRepo.clearCart(userId);
    return { success: true };
  }
}
```

---

## 3. Infrastructure SDK Facade
Wraps browser APIs or third-party web SDKs (e.g. Firebase Analytics, Amplitude, Datadog) behind standard interfaces.

```typescript
// Shared Logger Interface
export interface TelemetryTracker {
  logEvent(event: string, parameters?: Record<string, any>): void;
}

// Amplitude Implementation Facade
export class AmplitudeTracker implements TelemetryTracker {
  logEvent(event: string, parameters?: Record<string, any>): void {
    // Under-the-hood Amplitude SDK call
    // amplitude.getInstance().logEvent(event, parameters);
    console.log(`[Amplitude Event]: ${event}`, parameters);
  }
}
```
