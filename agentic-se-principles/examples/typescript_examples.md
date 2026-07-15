# TypeScript / Web - Agentic SE Principles Examples

This document demonstrates CUPID, DDD, Dependency Injection, Composition, and Observability-First design using TypeScript.

---

## 1. Domain-Driven Design: Value Object (Immutable Object)
Uses frozen objects and private properties to guarantee immutability and invariant checks.

```typescript
export class Money {
  // Invariant validation and read-only assignment
  readonly amount: number;
  readonly currency: string;

  constructor(amount: number, currency: string) {
    if (amount < 0) {
      throw new Error("Money amount cannot be negative.");
    }
    const cleanCurrency = currency.trim().toUpperCase();
    if (cleanCurrency.length !== 3) {
      throw new Error("Currency must be a 3-letter ISO code.");
    }

    this.amount = amount;
    this.currency = cleanCurrency;

    // Freeze object to prevent modifications at runtime
    Object.freeze(this);
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new Error("Cannot add money values with different currencies.");
    }
    return new Money(this.amount + other.amount, this.currency);
  }
}
```

---

## 2. Dependency Injection & Constructor-Based Composition
Programming to interfaces instead of concrete classes.

```typescript
export interface TokenStorage {
  saveToken(token: string): Promise<void>;
  getToken(): Promise<string | null>;
}

export class AuthenticationService {
  // Constructor injection targeting abstraction
  constructor(private readonly tokenStorage: TokenStorage) {}

  async authenticate(token: string): Promise<boolean> {
    if (!token) return false;
    await this.tokenStorage.saveToken(token);
    return true;
  }
}
```

---

## 3. Composition Over Inheritance (Strategy Pattern)
Abstracting encryption methods by composing strategy objects rather than creating subclasses for each algorithm.

```typescript
export interface EncryptionStrategy {
  encrypt(data: string): string;
  decrypt(data: string): string;
}

export class AesEncryption implements EncryptionStrategy {
  encrypt(data: string): string { return `aes_${data}`; }
  decrypt(data: string): string { return data.replace("aes_", ""); }
}

export class XorEncryption implements EncryptionStrategy {
  encrypt(data: string): string { return `xor_${data}`; }
  decrypt(data: string): string { return data.replace("xor_", ""); }
}

// Composed client class (Strategy is injected and can be changed at runtime)
export class VaultClient {
  constructor(private encryptionStrategy: EncryptionStrategy) {}

  setStrategy(strategy: EncryptionStrategy) {
    this.encryptionStrategy = strategy;
  }

  storeData(rawData: string): string {
    return this.encryptionStrategy.encrypt(rawData);
  }
}
```

---

## 4. Observability-First: Structured Logging & Distributing Traces
Using structured metadata context fields to coordinate tracing.

```typescript
import { Logger } from "winston";

export interface SpanContext {
  traceId: string;
  spanId: string;
}

export class BillingProcessor {
  constructor(private readonly logger: Logger) {}

  async processInvoice(invoiceId: string, context: SpanContext): Promise<void> {
    // Structured JSON log with trace-id correlation context
    this.logger.info("Initializing invoice processing transaction.", {
      invoice_id: invoiceId,
      trace_id: context.traceId,
      span_id: context.spanId,
    });

    try {
      await this.chargeCustomer(invoiceId);
      
      this.logger.info("Invoice transaction processed successfully.", {
        invoice_id: invoiceId,
        trace_id: context.traceId,
        span_id: context.spanId,
      });
    } catch (error) {
      this.logger.error("Invoice transaction failed.", {
        invoice_id: invoiceId,
        trace_id: context.traceId,
        span_id: context.spanId,
        error: error instanceof Error ? error.message : String(error),
      });
      throw error;
    }
  }

  private async chargeCustomer(invoiceId: string): Promise<void> {
    // Remote database or gateway operation...
  }
}
```
