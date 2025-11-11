// lib/features/auth/domain/auth_state.dart
import '../../../models/user.dart';

/// Base auth state class
abstract class AuthState {
  const AuthState();
  
  // Pattern matching methods
  T when<T>({
    required T Function() initial,
    required T Function() loading,
    required T Function(User user) authenticated,
    required T Function() unauthenticated,
    required T Function(String message) error,
  }) {
    if (this is AuthStateInitial) {
      return initial();
    } else if (this is AuthStateLoading) {
      return loading();
    } else if (this is AuthStateAuthenticated) {
      return authenticated((this as AuthStateAuthenticated).user);
    } else if (this is AuthStateUnauthenticated) {
      return unauthenticated();
    } else if (this is AuthStateError) {
      return error((this as AuthStateError).message);
    }
    throw Exception('Unknown auth state');
  }
  
  T? whenOrNull<T>({
    T Function()? initial,
    T Function()? loading,
    T Function(User user)? authenticated,
    T Function()? unauthenticated,
    T Function(String message)? error,
  }) {
    if (this is AuthStateInitial && initial != null) {
      return initial();
    } else if (this is AuthStateLoading && loading != null) {
      return loading();
    } else if (this is AuthStateAuthenticated && authenticated != null) {
      return authenticated((this as AuthStateAuthenticated).user);
    } else if (this is AuthStateUnauthenticated && unauthenticated != null) {
      return unauthenticated();
    } else if (this is AuthStateError && error != null) {
      return error((this as AuthStateError).message);
    }
    return null;
  }
  
  T maybeWhen<T>({
    T Function()? initial,
    T Function()? loading,
    T Function(User user)? authenticated,
    T Function()? unauthenticated,
    T Function(String message)? error,
    required T Function() orElse,
  }) {
    if (this is AuthStateInitial && initial != null) {
      return initial();
    } else if (this is AuthStateLoading && loading != null) {
      return loading();
    } else if (this is AuthStateAuthenticated && authenticated != null) {
      return authenticated((this as AuthStateAuthenticated).user);
    } else if (this is AuthStateUnauthenticated && unauthenticated != null) {
      return unauthenticated();
    } else if (this is AuthStateError && error != null) {
      return error((this as AuthStateError).message);
    }
    return orElse();
  }
}

class AuthStateInitial extends AuthState {
  const AuthStateInitial();
}

class AuthStateLoading extends AuthState {
  const AuthStateLoading();
}

class AuthStateAuthenticated extends AuthState {
  final User user;
  
  const AuthStateAuthenticated({required this.user});
}

class AuthStateUnauthenticated extends AuthState {
  const AuthStateUnauthenticated();
}

class AuthStateError extends AuthState {
  final String message;
  
  const AuthStateError({required this.message});
}

