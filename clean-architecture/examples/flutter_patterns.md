# Dart / Flutter Clean Facade Architecture Examples

Concrete examples demonstrating Repository, Service, and SDK facades using Dart and Flutter.

---

## 1. Repository Facade
Encapsulates HTTP Clients (like Dio or Http) and Local storage (like Hive, Isar, or Shared Preferences).

```dart
// 1. Domain Model
class Book {
  final String id;
  final String title;
  Book({required this.id, required this.title});
}

// 2. Repository Interface
abstract class BookRepository {
  Future<Book> getBook(String id);
}

// 3. Concrete Repository Facade (Coordinates Dio Client and Hive Storage)
class BookRepositoryImpl implements BookRepository {
  final BookApiClient _apiClient;
  final BookCache _localCache;

  BookRepositoryImpl(this._apiClient, this._localCache);

  @override
  Future<Book> getBook(String id) async {
    if (await _localCache.isCached(id)) {
      return _localCache.getCachedBook(id);
    }
    final rawDto = await _apiClient.fetchBook(id);
    final domainBook = Book(id: rawDto.id, title: rawDto.name);
    await _localCache.cacheBook(domainBook);
    return domainBook;
  }
}
```

---

## 2. Service Facade
Coordinates multiple Dart repositories to run business use cases.

```dart
// Coordinates multiple repositories for checkout operations
class PlaceOrderService {
  final PaymentRepository _paymentRepository;
  final InventoryRepository _inventoryRepository;
  final CartRepository _cartRepository;

  PlaceOrderService(
    this._paymentRepository,
    this._inventoryRepository,
    this._cartRepository,
  );

  Future<OrderStatus> executeCheckout(String userId) async {
    final cartItems = await _cartRepository.getItems(userId);
    if (cartItems.isEmpty) return OrderStatus.failed("Cart is empty");

    final hasStock = await _inventoryRepository.verifyStock(cartItems);
    if (!hasStock) return OrderStatus.failed("Item out of stock");

    final total = cartItems.fold(0.0, (sum, item) => sum + item.price);
    final charged = await _paymentRepository.charge(userId, total);
    if (!charged) return OrderStatus.failed("Payment declined");

    await _cartRepository.clear(userId);
    return OrderStatus.success();
  }
}
```

---

## 3. Infrastructure SDK Facade
Wraps third-party Flutter packages (like Firebase Messaging or Geolocator) under interface adapters.

```dart
abstract class NotificationManager {
  Future<void> initialize();
  Future<String?> getToken();
}

class FirebaseNotificationManagerImpl implements NotificationManager {
  @override
  Future<void> initialize() async {
    // Under-the-hood Firebase Messaging calls
    // await FirebaseMessaging.instance.requestPermission();
  }

  @override
  Future<String?> getToken() async {
    // return FirebaseMessaging.instance.getToken();
    return "mock_token";
  }
}
```
