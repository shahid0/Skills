# Dart / Flutter - Agentic SE Principles Examples

This document demonstrates CUPID, DDD, Dependency Injection, Composition, and Observability-First design using Dart and Flutter.

---

## 1. Domain-Driven Design: Value Object (Immutable class)
Utilizes Dart's `meta` library annotation `@immutable` and custom factories for invariant validation.

```dart
import 'package:meta/meta.dart';

@immutable
class UsPhoneNumber {
  final String rawValue;

  // Invariant validation inside factory constructor
  factory UsPhoneNumber.parse(String number) {
    // Stripping formatting characters
    final clean = number.replaceAll(RegExp(r'\D'), '');
    if (clean.length != 10) {
      throw ArgumentError('US Phone Number must contain exactly 10 digits.');
    }
    return UsPhoneNumber._(clean);
  }

  const UsPhoneNumber._(this.rawValue);

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is UsPhoneNumber &&
          runtimeType == other.runtimeType &&
          rawValue == other.rawValue;

  @override
  int get hashCode => rawValue.hashCode;
}
```

---

## 2. Dependency Injection & Constructor-Based Composition
Injecting abstractions rather than concrete subclasses.

```dart
abstract class LocationClient {
  Future<Coordinates> getCurrentLocation();
}

class WeatherService {
  final LocationClient _locationClient;
  final WeatherApiClient _weatherApi;

  // Constructor Injection
  WeatherService({
    required LocationClient locationClient,
    required WeatherApiClient weatherApi,
  })  : _locationClient = locationClient,
        _weatherApi = weatherApi;

  Future<WeatherData> getLocalWeather() async {
    final coords = await _locationClient.getCurrentLocation();
    return _weatherApi.fetchWeather(coords.lat, coords.lon);
  }
}
```

---

## 3. Composition Over Inheritance (Adapter Pattern)
Wrapping platform-specific operations in composed adapter objects.

```dart
abstract class StorageAdapter {
  Future<void> write(String key, String value);
  Future<String?> read(String key);
}

// 1. SharedPreferences implementation composed into storage facade
class PrefsStorageAdapter implements StorageAdapter {
  final SharedPreferences _prefs;
  
  PrefsStorageAdapter(this._prefs);

  @override
  Future<String?> read(String key) async => _prefs.getString(key);

  @override
  Future<void> write(String key, String value) async => _prefs.setString(key, value);
}

// 2. Encryption decorator (Composition instead of inheritance)
class SecureStorageAdapter implements StorageAdapter {
  final StorageAdapter _baseStorage;
  final CryptoHelper _crypto;

  SecureStorageAdapter(this._baseStorage, this._crypto);

  @override
  Future<void> write(String key, String value) async {
    final encrypted = _crypto.encrypt(value);
    await _baseStorage.write(key, encrypted);
  }

  @override
  Future<String?> read(String key) async {
    final encryptedValue = await _baseStorage.read(key);
    if (encryptedValue == null) return null;
    return _crypto.decrypt(encryptedValue);
  }
}
```

---

## 4. Observability-First: Structured Logging & Tracing
Using key-value maps inside structured log envelopes.

```dart
import 'dart:convert';
import 'package:logger/logger.dart';

class StructuredTelemetryLogger {
  final _logger = Logger(printer: SimplePrinter());

  void logTelemetry({
    required String message,
    required String level,
    required String traceId,
    required Map<String, dynamic> context,
  }) {
    final payload = {
      'timestamp': DateTime.now().toIso8601String(),
      'level': level.toUpperCase(),
      'message': message,
      'trace_id': traceId,
      'context': context,
    };
    
    // Output as structured JSON
    _logger.log(Level.info, jsonEncode(payload));
  }
}
```
