// lib/services/api_service.dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import '../utils/app_config.dart';

/// Base API service configuration
class ApiService {
  // Use AppConfig for dynamic environment-based configuration
  static String get apiBaseUrl => AppConfig.apiUrl;
  
  final storage = const FlutterSecureStorage();
  
  /// Get authorization headers with JWT token
  Future<Map<String, String>> getAuthHeaders() async {
    final token = await storage.read(key: 'access_token');
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }
  
  /// Get base headers without authentication
  Map<String, String> getBaseHeaders() {
    return {
      'Content-Type': 'application/json',
    };
  }
  
  /// Handle API errors
  String handleError(http.Response response) {
    if (response.statusCode >= 400 && response.statusCode < 500) {
      return 'Client error: ${response.statusCode}';
    } else if (response.statusCode >= 500) {
      return 'Server error: ${response.statusCode}';
    }
    return 'Unknown error occurred';
  }
}
