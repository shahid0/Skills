# Observability-First Design Guidelines

Observability-First Design (also known as Observability-Driven Development) is a software development philosophy that treats telemetry instrumentation (logs, metrics, and traces) as a core functional requirement, ensuring system visibility is designed *before* code is deployed to production.

---

## 1. Core Concept

Systems are designed to generate high-fidelity, contextual data that enables engineers to understand the system's internal state solely from its external outputs:
*   **Structured Logging:** Exposing logs in standard, machine-readable formats (like JSON) containing key-value context metadata, rather than unstructured plain text.
*   **Traces & Context Propagation:** Tracking the request path across microservices or internal layers using unique trace and span IDs, allowing developers to reconstruct the call stack of a distributed transaction.
*   **Metrics:** Emitting numerical data (latency, error rate, throughput, CPU/Memory) to identify trends, bottleneck anomalies, and regression patterns.

---

## 2. Design Guidelines

*   **Design Telemetry Prior to Implementation:** You MUST define the logs, metrics, and trace boundaries (spans) during the design phase of a feature.
*   **Use Structured Contextual Logs:** You MUST emit logs in structured formats (e.g. JSON log entries). Every log statement MUST include contextual metadata (such as `user_id`, `transaction_id`, or `correlation_id`) so that related actions can be grouped.
*   **Propagate Trace Context:** You MUST propagate trace and span context across API boundaries, thread pool shifts, and architectural layers to maintain trace continuity.
*   **Instrument Critical Failure Paths:** You MUST ensure that all database queries, network operations, cache lookups, and business logic validation checkpoints are instrumented with latency metrics and error tracing.

---

## 3. Common Anti-Patterns

*   **Afterthought Instrumentation:** Writing the feature code entirely and then sprinkling `print()` or basic log statements right before merging, resulting in missing context.
*   **Unstructured Logs:** Writing logs as unstructured sentences (e.g., `logger.info("User logged in with email: " + email)`), which makes searching, querying, and parsing in log aggregators (ELK, Datadog) difficult.
*   **Leaking Secrets in Logs:** Emitting personally identifiable information (PII) like passwords, authorization tokens, credit card numbers, or full names in plaintext logs.
*   **Disconnected Pillars:** Emitting logs, traces, and metrics that cannot be correlated (e.g., a metric shows high latency, but there is no trace ID link to pinpoint the slow database query or log sequence).
