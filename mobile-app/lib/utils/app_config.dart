// lib/utils/app_config.dart
/// Application configuration and environment variables
class AppConfig {
  /// API Base URL
  /// - For Docker environment: http://backend:8000
  /// - For Android Emulator: http://10.0.2.2:8000
  /// - For iOS Simulator: http://localhost:8000
  /// - For Physical Device: http://YOUR_MACHINE_IP:8000
  /// - For GitHub Codespaces: Auto-constructed from current host
  static String get apiBaseUrl {
    const envUrl = String.fromEnvironment('API_BASE_URL', defaultValue: '');
    
    if (envUrl.isNotEmpty) {
      return envUrl;
    }
    
    // For web builds, auto-detect the backend URL
    // If running in Codespaces (*.app.github.dev), construct backend URL
    // This uses the flutter web app's URL to infer the backend URL
    try {
      // In web environment, we can detect the current host
      // For Codespaces: if frontend is on xxx-8080.app.github.dev
      // then backend is on xxx-8000.app.github.dev
      final currentUrl = Uri.base.toString();
      
      if (currentUrl.contains('.app.github.dev')) {
        // GitHub Codespaces pattern: replace port 8080 with 8000
        final backendUrl = currentUrl.replaceAll('-8080.app.github.dev', '-8000.app.github.dev');
        // Remove any path components and ensure it's just the base URL
        final uri = Uri.parse(backendUrl);
        return '${uri.scheme}://${uri.host}';
      }
    } catch (e) {
      // If detection fails, fall back to default
    }
    
    // Default for local Docker development
    return 'http://backend:8000';
  }
  
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
