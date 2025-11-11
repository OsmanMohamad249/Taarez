// lib/models/design.dart
class Design {
  final String id;
  final String name;
  final String? description;
  final String? styleType;
  final double basePrice;
  final String? baseImageUrl;
  final String ownerId;
  final String? categoryId;
  final bool isActive;
  final DateTime createdAt;
  final Map<String, dynamic>? customizationRules;
  
  Design({
    required this.id,
    required this.name,
    this.description,
    this.styleType,
    required this.basePrice,
    this.baseImageUrl,
    required this.ownerId,
    this.categoryId,
    required this.isActive,
    required this.createdAt,
    this.customizationRules,
  });
  
  factory Design.fromJson(Map<String, dynamic> json) {
    return Design(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      styleType: json['style_type'],
      basePrice: (json['base_price'] as num).toDouble(),
      baseImageUrl: json['base_image_url'],
      ownerId: json['owner_id'],
      categoryId: json['category_id'],
      isActive: json['is_active'] ?? true,
      createdAt: DateTime.parse(json['created_at']),
      customizationRules: json['customization_rules'],
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'style_type': styleType,
      'base_price': basePrice,
      'base_image_url': baseImageUrl,
      'owner_id': ownerId,
      'category_id': categoryId,
      'is_active': isActive,
      'created_at': createdAt.toIso8601String(),
      'customization_rules': customizationRules,
    };
  }
  
  // Convenience getters for backward compatibility
  String get title => name;
  double get price => basePrice;
  String get imageUrl => baseImageUrl ?? '';
  String get designerId => ownerId;
}
