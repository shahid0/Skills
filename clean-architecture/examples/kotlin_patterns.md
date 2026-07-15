# Kotlin / Jetpack Compose / KMP Clean Facade Architecture Examples

Concrete examples demonstrating Repository, Service, and SDK facades using Kotlin and Kotlin Multiplatform (KMP).

---

## 1. Repository Facade
Encapsulates Ktor HTTP clients and SQLDelight cache.

```kotlin
// 1. Domain Model
data class Article(val id: String, val title: String)

// 2. Repository Interface
interface ArticleRepository {
    suspend fun getArticle(id: String): Article
}

// 3. Concrete Repository Facade (Coordinates Ktor Client and Local SQL Database)
class ArticleRepositoryImpl(
    private val api: ArticleApi,
    private val database: ArticleDb
) : ArticleRepository {
    
    override suspend fun getArticle(id: String): Article {
        val cached = database.selectById(id)
        if (cached != null) {
            return Article(id = cached.id, title = cached.title)
        }
        
        val dto = api.fetchArticle(id)
        val domainArticle = Article(id = dto.id, title = dto.title)
        database.insert(domainArticle)
        return domainArticle
    }
}
```

---

## 2. Service Facade
Coordinates multiple Kotlin repositories for complex business operations.

```kotlin
// Service coordinating multiple repositories for a shopping checkout workflow
class PurchaseService(
    private val cartRepo: CartRepository,
    private val paymentRepo: PaymentRepository,
    private val inventoryRepo: InventoryRepository
) {
    suspend fun checkout(userId: String): PurchaseResult {
        val items = cartRepo.getCartItems(userId)
        if (items.isEmpty()) return PurchaseResult.EmptyCart
        
        val stockAvailable = inventoryRepo.checkInventory(items)
        if (!stockAvailable) return PurchaseResult.OutOfStock
        
        val charged = paymentRepo.processPayment(userId, items.sumOf { it.price })
        if (!charged) return PurchaseResult.PaymentFailed
        
        cartRepo.clear(userId)
        return PurchaseResult.Success
    }
}
```

---

## 3. Infrastructure SDK Facade
Wraps third-party Kotlin/KMP libraries (like Kable Bluetooth, Firebase, or DataStore) behind clear interfaces.

```kotlin
interface SharedKeyValueStore {
    fun getString(key: String): String?
    fun setString(key: String, value: String)
}

class AndroidPreferencesStore(private val context: Context) : SharedKeyValueStore {
    private val prefs = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
    
    override fun getString(key: String): String? = prefs.getString(key, null)
    
    override fun setString(key: String, value: String) {
        prefs.edit().putString(key, value).apply()
    }
}
```
