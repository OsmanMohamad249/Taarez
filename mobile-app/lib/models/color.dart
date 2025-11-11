// lib/models/color.dart
class ColorModel {
  final String id;
  final String name;
  final String hexCode;
  
  ColorModel({
    required this.id,
    required this.name,
    required this.hexCode,
  });
  
  factory ColorModel.fromJson(Map<String, dynamic> json) {
    return ColorModel(
      id: json['id'],
      name: json['name'],
      hexCode: json['hex_code'],
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'hex_code': hexCode,
    };
  }
}
