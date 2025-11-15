import 'dart:io';
import 'package:http/http.dart' as http;
import 'api_service.dart';

class MeasurementService extends ApiService {
  /// Fetch list of measurements
  Future<http.Response> listMeasurements() async {
    final headers = await getAuthHeaders();
    final uri = Uri.parse('${ApiService.apiBaseUrl}/api/v1/measurements');
    final resp = await http.get(uri, headers: headers);
    return resp;
  }

  /// Upload image file and return response
  Future<http.StreamedResponse> uploadImage(File file) async {
    final uri = Uri.parse('${ApiService.apiBaseUrl}/api/v1/measurements/upload-image');
    final request = http.MultipartRequest('POST', uri);
    final headers = await getAuthHeaders();
    request.headers.addAll(headers);
    final stream = http.ByteStream(file.openRead());
    final length = await file.length();
    final multipartFile = http.MultipartFile('file', stream, length, filename: file.path.split('/').last);
    request.files.add(multipartFile);
    final streamedResponse = await request.send();
    return streamedResponse;
  }

  /// Process measurements with four photos and user height/weight
  /// photos: map with keys 'front','back','left','right'
  Future<http.StreamedResponse> processMeasurements(Map<String, File> photos, double height, double weight, {int retries = 3}) async {
    final uri = Uri.parse('${ApiService.apiBaseUrl}/api/v1/measurements/process');
    int attempt = 0;
    while (true) {
      attempt += 1;
      try {
        final request = http.MultipartRequest('POST', uri);
        final headers = await getAuthHeaders();
        request.headers.addAll(headers);
        // Add form fields
        request.fields['height'] = height.toString();
        request.fields['weight'] = weight.toString();

        // Attach photos with expected field names
        for (final entry in photos.entries) {
          final key = entry.key; // expected 'front','back','left','right'
          final file = entry.value;
          final stream = http.ByteStream(file.openRead());
          final length = await file.length();
          final fieldName = 'photo_${key}';
          final multipartFile = http.MultipartFile(fieldName, stream, length, filename: file.path.split('/').last);
          request.files.add(multipartFile);
        }

        final streamedResponse = await request.send();
        // If server error, consider retrying
        if (streamedResponse.statusCode >= 500 && attempt < retries) {
          // exponential backoff
          await Future.delayed(Duration(seconds: 1 << (attempt - 1)));
          continue;
        }
        return streamedResponse;
      } catch (e) {
        if (attempt >= retries) rethrow;
        await Future.delayed(Duration(seconds: 1 << (attempt - 1)));
      }
    }
  }
}
