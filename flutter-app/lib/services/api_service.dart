import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io' show Platform;
import '../models/gesture_prediction.dart';

/// Service for communicating with the FastAPI backend
class ApiService {
  // Automatically detect the correct URL based on platform
  // For Android emulator: http://10.0.2.2:8000 (special IP that maps to host's localhost)
  // For iOS simulator: http://localhost:8000
  // For physical device: http://<your-computer-ip>:8000 (you'll need to set this manually)
  static String get baseUrl {
    if (Platform.isAndroid) {
      // Android emulator uses 10.0.2.2 to access host machine's localhost
      return 'http://10.0.2.2:8000';
    } else {
      // iOS simulator and other platforms can use localhost
      return 'http://localhost:8000';
    }
  }

  /// Predict gesture from image bytes
  Future<GesturePrediction> predictGesture(List<int> imageBytes) async {
    try {
      final uri = Uri.parse('$baseUrl/predict');
      final request = http.MultipartRequest('POST', uri);

      request.files.add(
        http.MultipartFile.fromBytes(
          'file',
          imageBytes,
          filename: 'gesture.jpg',
        ),
      );

      final response = await request.send();
      final responseBody = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        final json = jsonDecode(responseBody) as Map<String, dynamic>;
        return GesturePrediction.fromJson(json);
      } else {
        // Try to parse error message from response
        try {
          final errorJson = jsonDecode(responseBody) as Map<String, dynamic>;
          final errorDetail = errorJson['detail'] ?? 'Unknown error';
          throw Exception(errorDetail);
        } catch (_) {
          throw Exception(
              'Failed to predict gesture: ${response.statusCode} - $responseBody');
        }
      }
    } catch (e) {
      // Re-throw with more context
      if (e.toString().contains('Connection refused') ||
          e.toString().contains('Failed host lookup')) {
        throw Exception(
            'Cannot connect to backend server. Make sure the server is running on $baseUrl');
      }
      // Clean up nested error messages
      String errorMsg = e.toString();
      if (errorMsg.startsWith('Exception: ')) {
        errorMsg = errorMsg.substring(11);
      }
      if (errorMsg.startsWith('Error: ')) {
        errorMsg = errorMsg.substring(7);
      }
      // Remove duplicate "Exception:" prefixes
      while (errorMsg.startsWith('Exception: ')) {
        errorMsg = errorMsg.substring(11);
      }
      throw Exception(errorMsg);
    }
  }

  /// Get list of all supported gestures
  Future<List<GestureInfo>> getGestures() async {
    try {
      final uri = Uri.parse('$baseUrl/gestures');
      final response = await http.get(uri);

      if (response.statusCode == 200) {
        final json = jsonDecode(response.body) as Map<String, dynamic>;
        final gesturesList = json['gestures'] as List;
        return gesturesList
            .map((g) => GestureInfo.fromJson(g as Map<String, dynamic>))
            .toList();
      } else {
        throw Exception('Failed to get gestures: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching gestures: $e');
    }
  }

  /// Get information about a specific gesture
  Future<GestureInfo> getGestureInfo(String gestureLabel) async {
    try {
      final uri = Uri.parse('$baseUrl/gesture/$gestureLabel');
      final response = await http.get(uri);

      if (response.statusCode == 200) {
        final json = jsonDecode(response.body) as Map<String, dynamic>;
        return GestureInfo.fromJson(json);
      } else {
        throw Exception('Failed to get gesture info: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching gesture info: $e');
    }
  }

  /// Check if API is available
  Future<bool> checkHealth() async {
    try {
      final uri = Uri.parse('$baseUrl/health');
      final response = await http.get(uri);
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  /// Check if model is loaded on the backend
  Future<bool> checkModelStatus() async {
    try {
      final uri = Uri.parse('$baseUrl/health');
      final response = await http.get(uri);

      if (response.statusCode == 200) {
        final json = jsonDecode(response.body) as Map<String, dynamic>;
        return json['model_loaded'] as bool? ?? false;
      }
      return false;
    } catch (e) {
      return false;
    }
  }
}
