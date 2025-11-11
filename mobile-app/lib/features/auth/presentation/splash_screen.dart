// lib/features/auth/presentation/splash_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'auth_provider.dart';
import '../domain/auth_state.dart';
import 'login_screen.dart';
import 'home_screen.dart';
import '../../../screens/designs/designer_dashboard_screen.dart';

class SplashScreen extends ConsumerStatefulWidget {
  const SplashScreen({Key? key}) : super(key: key);

  @override
  _SplashScreenState createState() => _SplashScreenState();
}

class _SplashScreenState extends ConsumerState<SplashScreen> {
  @override
  void initState() {
    super.initState();
    // Check authentication on mount
    Future.microtask(() {
      ref.read(authStateProvider.notifier).checkAuth();
    });
  }
  
  @override
  Widget build(BuildContext context) {
    // Listen to auth state changes
    ref.listen<AuthState>(authStateProvider, (previous, next) {
      next.when(
        initial: () {
          // Do nothing, waiting for checkAuth to complete
        },
        loading: () {
          // Do nothing, show loading indicator
        },
        authenticated: (user) {
          // Navigate to appropriate screen based on user role
          if (user.isDesigner) {
            Navigator.of(context).pushReplacement(
              MaterialPageRoute(builder: (_) => DesignerDashboardScreen()),
            );
          } else {
            Navigator.of(context).pushReplacement(
              MaterialPageRoute(builder: (_) => const HomeScreen()),
            );
          }
        },
        unauthenticated: () {
          // Navigate to login screen
          Navigator.of(context).pushReplacement(
            MaterialPageRoute(builder: (_) => const LoginScreen()),
          );
        },
        error: (message) {
          // Navigate to login screen on error
          Navigator.of(context).pushReplacement(
            MaterialPageRoute(builder: (_) => const LoginScreen()),
          );
        },
      );
    });
    
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Tiraz',
              style: TextStyle(
                fontSize: 48,
                fontWeight: FontWeight.bold,
                color: Colors.blue,
              ),
            ),
            SizedBox(height: 20),
            CircularProgressIndicator(),
          ],
        ),
      ),
    );
  }
}
