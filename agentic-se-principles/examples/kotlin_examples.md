# Kotlin / Jetpack Compose / KMP - Agentic SE Principles Examples

This document demonstrates CUPID, DDD, Dependency Injection, Composition, and Observability-First design using Kotlin.

---

## 1. Domain-Driven Design: Value Object (Immutable Data Class)
Enforces invariants during instantiation.

```kotlin
import java.util.regex.Pattern

@JvmInline
value class Password private constructor(val raw: String) {
    
    companion object {
        private val PASSWORD_PATTERN = Pattern.compile("^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,}$")
        
        fun create(password: String): Result<Password> {
            return if (PASSWORD_PATTERN.matcher(password).matches()) {
                Result.success(Password(password))
            } else {
                Result.failure(IllegalArgumentException("Password must contain at least 8 characters, one digit, and one uppercase letter."))
            }
        }
    }
}
```

---

## 2. Dependency Injection & Constructor-Based Composition
Abstracts concrete classes behind interface parameters.

```kotlin
interface NotificationChannel {
    suspend fun send(title: String, message: String)
}

class AlertService(
    private val notificationChannel: NotificationChannel,
    private val userPrefs: UserPreferences
) {
    suspend fun raiseAlert(userId: String, systemMessage: String) {
        val userEnabledAlerts = userPrefs.getAlertStatus(userId)
        if (userEnabledAlerts) {
            notificationChannel.send(
                title = "Critical Security Alert",
                message = systemMessage
            )
        }
    }
}
```

---

## 3. Composition Over Inheritance (Delegation Pattern)
Using Kotlin's `by` keyword for clean composition delegation.

```kotlin
interface ArticleStorage {
    fun saveArticle(id: String, content: String)
    fun fetchArticle(id: String): String?
}

class LocalDatabaseStorage : ArticleStorage {
    override fun saveArticle(id: String, content: String) { /* Database insert */ }
    override fun fetchArticle(id: String): String? = "Article Content"
}

// Composition via Class Delegation - Logging behavior added without inheritance
class EncryptedLoggingStorage(
    private val baseStorage: ArticleStorage,
    private val crypto: EncryptionHelper,
    private val logger: StructuredLogger
) : ArticleStorage by baseStorage {
    
    override fun saveArticle(id: String, content: String) {
        logger.info("Encrypting article: $id")
        val encryptedContent = crypto.encrypt(content)
        baseStorage.saveArticle(id, encryptedContent)
        logger.info("Encrypted article successfully saved.")
    }
}
```

---

## 4. Observability-First: Structured Logging & Tracing Context
Correlating trace and span context inside Kotlin Coroutines.

```kotlin
import kotlinx.coroutines.withContext
import org.slf4j.MDC
import org.slf4j.LoggerFactory

class OrderProcessor {
    private val logger = LoggerFactory.getLogger(OrderProcessor::class.java)
    
    suspend fun processOrder(orderId: String, traceId: String) {
        // MDCCloseable safely manages thread context boundaries
        MDC.put("trace_id", traceId)
        MDC.put("order_id", orderId)
        
        try {
            logger.info("Processing transaction sequence started.")
            validateOrder(orderId)
            chargeCard(orderId)
            logger.info("Transaction sequence successfully completed.")
        } catch (e: Exception) {
            logger.error("Failed to process transaction.", e)
        } finally {
            MDC.clear()
        }
    }
    
    private suspend fun validateOrder(orderId: String) { /* Business check */ }
    private suspend fun chargeCard(orderId: String) { /* Gateway call */ }
}
```
