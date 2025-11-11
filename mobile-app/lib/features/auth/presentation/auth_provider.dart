// lib/features/auth/presentation/auth_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../services/auth_service.dart';
import '../../../models/user.dart';
import '../domain/auth_state.dart';

// Auth service provider
final authServiceProvider = Provider((ref) => AuthService());

// Auth state provider
final authStateProvider = StateNotifierProvider<AuthStateNotifier, AuthState>((ref) {
  return AuthStateNotifier(ref.read(authServiceProvider));
});

// Auth state notifier
class AuthStateNotifier extends StateNotifier<AuthState> {
  final AuthService authService;
  
  AuthStateNotifier(this.authService) : super(const AuthState.initial());
  
  // Check authentication status
  Future<void> checkAuth() async {
    // Set loading state
    state = const AuthState.loading();
    
    try {
      final isLoggedIn = await authService.isLoggedIn();
      
      if (isLoggedIn) {
        final result = await authService.getCurrentUser();
        if (result['success']) {
          final user = User.fromJson(result['data']);
          state = AuthState.authenticated(user: user);
        } else {
          state = const AuthState.unauthenticated();
        }
      } else {
        state = const AuthState.unauthenticated();
      }
    } catch (e) {
      state = AuthState.error(message: e.toString());
    }
  }
  
  // Login
  Future<bool> login(String email, String password) async {
    state = const AuthState.loading();
    
    try {
      final result = await authService.login(
        email: email,
        password: password,
      );
      
      if (result['success']) {
        // Fetch user info
        final userResult = await authService.getCurrentUser();
        if (userResult['success']) {
          final user = User.fromJson(userResult['data']);
          state = AuthState.authenticated(user: user);
          return true;
        }
      }
      
      state = AuthState.error(message: result['error'] ?? 'Login failed');
      return false;
    } catch (e) {
      state = AuthState.error(message: e.toString());
      return false;
    }
  }
  
  // Register
  Future<bool> register({
    required String email,
    required String password,
    String? firstName,
    String? lastName,
  }) async {
    state = const AuthState.loading();
    
    try {
      final result = await authService.register(
        email: email,
        password: password,
        firstName: firstName,
        lastName: lastName,
      );
      
      if (result['success']) {
        state = const AuthState.unauthenticated();
        return true;
      } else {
        state = AuthState.error(message: result['error'] ?? 'Registration failed');
        return false;
      }
    } catch (e) {
      state = AuthState.error(message: e.toString());
      return false;
    }
  }
  
  // Logout
  Future<void> logout() async {
    await authService.logout();
    state = const AuthState.unauthenticated();
  }
}
