// lib/models/fabric.dart
class Fabric {
  final String id;
  final String name;
  final String? description;
  final String? imageUrl;
  final double basePrice;
  
  Fabric({
    required this.id,
    required this.name,
    this.description,
    this.imageUrl,
    required this.basePrice,
  });
  
  factory Fabric.fromJson(Map<String, dynamic> json) {
    return Fabric(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      imageUrl: json['image_url'],
      basePrice: (json['base_price'] as num).toDouble(),
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'image_url': imageUrl,
      'base_price': basePrice,
    };
  }
}
