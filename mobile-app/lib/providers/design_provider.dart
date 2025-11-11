// lib/providers/design_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/design_service.dart';
import '../models/design.dart';

// Design service provider
final designServiceProvider = Provider((ref) => DesignService());

// Provider for fetching designer's own designs
final myDesignsProvider = FutureProvider<List<Design>>((ref) async {
  final designService = ref.read(designServiceProvider);
  return designService.getMyDesigns();
});

// Provider to trigger refresh of designs
final designsRefreshProvider = StateProvider<int>((ref) => 0);
