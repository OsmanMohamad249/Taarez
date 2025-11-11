// lib/services/design_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/design.dart';
import 'api_service.dart';

class DesignService extends ApiService {
  /// Get all designs
  Future<Map<String, dynamic>> getDesigns({
    int skip = 0,
    int limit = 100,
  }) async {
    try {
      final headers = await getAuthHeaders();
      final response = await http.get(
        Uri.parse('${ApiService.apiBaseUrl}/designs?skip=$skip&limit=$limit'),
        headers: headers,
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final designs = (data as List)
            .map((item) => Design.fromJson(item))
            .toList();
        
        return {
          'success': true,
          'designs': designs,
        };
      } else {
        return {
          'success': false,
          'error': handleError(response),
        };
      }
    } catch (e) {
      return {
        'success': false,
        'error': 'Network error: ${e.toString()}',
      };
    }
  }
  
  /// Get my designs (designer's own designs)
  Future<List<Design>> getMyDesigns({
    int skip = 0,
    int limit = 100,
  }) async {
    try {
      final headers = await getAuthHeaders();
      final response = await http.get(
        Uri.parse('${ApiService.apiBaseUrl}/designs/me?skip=$skip&limit=$limit'),
        headers: headers,
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final designs = (data as List)
            .map((item) => Design.fromJson(item))
            .toList();
        return designs;
      } else {
        throw Exception(handleError(response));
      }
    } catch (e) {
      throw Exception('Failed to load designs: ${e.toString()}');
    }
  }
  
  /// Get design by ID
  Future<Map<String, dynamic>> getDesignById(String designId) async {
    try {
      final headers = await getAuthHeaders();
      final response = await http.get(
        Uri.parse('${ApiService.apiBaseUrl}/designs/$designId'),
        headers: headers,
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {
          'success': true,
          'design': Design.fromJson(data),
        };
      } else {
        return {
          'success': false,
          'error': handleError(response),
        };
      }
    } catch (e) {
      return {
        'success': false,
        'error': 'Network error: ${e.toString()}',
      };
    }
  }
  
  /// Create new design
  Future<Map<String, dynamic>> createDesign({
    required String name,
    required String description,
    required double basePrice,
    String? styleType,
    String? baseImageUrl,
    String? categoryId,
  }) async {
    try {
      final headers = await getAuthHeaders();
      final body = {
        'name': name,
        'description': description,
        'base_price': basePrice,
      };
      
      if (styleType != null) body['style_type'] = styleType;
      if (baseImageUrl != null) body['base_image_url'] = baseImageUrl;
      if (categoryId != null) body['category_id'] = categoryId;
      
      final response = await http.post(
        Uri.parse('${ApiService.apiBaseUrl}/designs'),
        headers: headers,
        body: jsonEncode(body),
      );
      
      if (response.statusCode == 201) {
        final data = jsonDecode(response.body);
        return {
          'success': true,
          'design': Design.fromJson(data),
        };
      } else {
        return {
          'success': false,
          'error': handleError(response),
        };
      }
    } catch (e) {
      return {
        'success': false,
        'error': 'Network error: ${e.toString()}',
      };
    }
  }
  
  /// Update design
  Future<Map<String, dynamic>> updateDesign({
    required String designId,
    String? name,
    String? description,
    String? styleType,
    double? basePrice,
    String? baseImageUrl,
    String? categoryId,
  }) async {
    try {
      final headers = await getAuthHeaders();
      final body = <String, dynamic>{};
      
      if (name != null) body['name'] = name;
      if (description != null) body['description'] = description;
      if (styleType != null) body['style_type'] = styleType;
      if (basePrice != null) body['base_price'] = basePrice;
      if (baseImageUrl != null) body['base_image_url'] = baseImageUrl;
      if (categoryId != null) body['category_id'] = categoryId;
      
      final response = await http.put(
        Uri.parse('${ApiService.apiBaseUrl}/designs/$designId'),
        headers: headers,
        body: jsonEncode(body),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {
          'success': true,
          'design': Design.fromJson(data),
        };
      } else {
        return {
          'success': false,
          'error': handleError(response),
        };
      }
    } catch (e) {
      return {
        'success': false,
        'error': 'Network error: ${e.toString()}',
      };
    }
  }
  
  /// Delete design
  Future<Map<String, dynamic>> deleteDesign(String designId) async {
    try {
      final headers = await getAuthHeaders();
      final response = await http.delete(
        Uri.parse('${ApiService.apiBaseUrl}/designs/$designId'),
        headers: headers,
      );
      
      if (response.statusCode == 204) {
        return {
          'success': true,
        };
      } else {
        return {
          'success': false,
          'error': handleError(response),
        };
      }
    } catch (e) {
      return {
        'success': false,
        'error': 'Network error: ${e.toString()}',
      };
    }
  }
}
