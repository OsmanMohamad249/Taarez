// lib/screens/designs/designer_dashboard_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/design_provider.dart';
import '../../providers/auth_provider.dart';
import '../../widgets/design_list_item.dart';
import 'add_design_screen.dart';
import '../auth/login_screen.dart';

class DesignerDashboardScreen extends ConsumerWidget {
  const DesignerDashboardScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final myDesignsAsync = ref.watch(myDesignsProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text('My Designs'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: () {
              ref.invalidate(myDesignsProvider);
            },
            tooltip: 'Refresh',
          ),
          IconButton(
            icon: Icon(Icons.logout),
            onPressed: () async {
              await ref.read(authStateProvider.notifier).logout();
              if (context.mounted) {
                Navigator.of(context).pushReplacement(
                  MaterialPageRoute(builder: (_) => LoginScreen()),
                );
              }
            },
            tooltip: 'Logout',
          ),
        ],
      ),
      body: myDesignsAsync.when(
        data: (designs) {
          if (designs.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.design_services_outlined,
                    size: 80,
                    color: Colors.grey.shade400,
                  ),
                  SizedBox(height: 24),
                  Text(
                    'You haven\'t added any designs yet.',
                    style: TextStyle(
                      fontSize: 18,
                      color: Colors.grey.shade600,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 8),
                  Text(
                    'Tap \'+\' to create your first one!',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.grey.shade500,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            );
          }
          
          return ListView.builder(
            padding: EdgeInsets.only(top: 8, bottom: 80),
            itemCount: designs.length,
            itemBuilder: (context, index) {
              return DesignListItem(design: designs[index]);
            },
          );
        },
        loading: () => Center(
          child: CircularProgressIndicator(),
        ),
        error: (error, stack) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.error_outline,
                size: 60,
                color: Colors.red.shade300,
              ),
              SizedBox(height: 16),
              Text(
                'Failed to load designs.',
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.red.shade700,
                ),
              ),
              SizedBox(height: 8),
              Text(
                'Please try again.',
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey.shade600,
                ),
              ),
              SizedBox(height: 16),
              ElevatedButton.icon(
                onPressed: () {
                  ref.invalidate(myDesignsProvider);
                },
                icon: Icon(Icons.refresh),
                label: Text('Retry'),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          final result = await Navigator.of(context).push(
            MaterialPageRoute(builder: (_) => AddDesignScreen()),
          );
          
          // Refresh the list if a design was added
          if (result == true) {
            ref.invalidate(myDesignsProvider);
          }
        },
        child: Icon(Icons.add),
        tooltip: 'Add Design',
      ),
    );
  }
}
