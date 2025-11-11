// lib/utils/app_config.dart
/// Application configuration and environment variables
class AppConfig {
  /// API Base URL
  /// - For Docker environment: http://backend:8000
  /// - For Android Emulator: http://10.0.2.2:8000
  /// - For iOS Simulator: http://localhost:8000
  /// - For Physical Device: http://YOUR_MACHINE_IP:8000
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://backend:8000',
  );
  
  /// API Version Prefix
  static const String apiV1Prefix = '/api/v1';
  
  /// Full API URL
  static String get apiUrl => '$apiBaseUrl$apiV1Prefix';
  
  /// App Environment (development, staging, production)
  static const String environment = String.fromEnvironment(
    'ENVIRONMENT',
    defaultValue: 'development',
  );
  
  /// Whether the app is in debug mode
  static bool get isDebug => environment == 'development';
  
  /// Whether the app is in production mode
  static bool get isProduction => environment == 'production';
}
