import 'package:flutter/foundation.dart';
import '../models/gesture_prediction.dart';
import '../services/api_service.dart';
import '../services/camera_service.dart';

/// Provider for managing gesture recognition state
class GestureProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  final CameraService _cameraService = CameraService();

  GesturePrediction? _currentPrediction;
  bool _isProcessing = false;
  bool _isCameraInitialized = false;
  bool _isModelLoaded = false;
  String? _errorMessage;

  GesturePrediction? get currentPrediction => _currentPrediction;
  bool get isProcessing => _isProcessing;
  bool get isCameraInitialized => _isCameraInitialized;
  bool get isModelLoaded => _isModelLoaded;
  String? get errorMessage => _errorMessage;
  CameraService get cameraService => _cameraService;

  /// Initialize camera
  Future<void> initializeCamera() async {
    try {
      _errorMessage = null;
      await _cameraService.initialize();
      _isCameraInitialized = _cameraService.isInitialized;

      // Check model status when camera initializes
      await checkModelStatus();

      notifyListeners();
    } catch (e) {
      _errorMessage = 'Failed to initialize camera: $e';
      _isCameraInitialized = false;
      notifyListeners();
    }
  }

  /// Check model status on backend
  Future<void> checkModelStatus() async {
    try {
      _isModelLoaded = await _apiService.checkModelStatus();
      if (!_isModelLoaded && _errorMessage == null) {
        _errorMessage =
            'Model not loaded. Please train a model first. See TRAIN_MODEL_GUIDE.md for instructions.';
      } else if (_isModelLoaded) {
        // Clear error if model is now loaded
        if (_errorMessage?.contains('Model not loaded') ?? false) {
          _errorMessage = null;
        }
      }
      notifyListeners();
    } catch (e) {
      _isModelLoaded = false;
      if (_errorMessage == null) {
        _errorMessage =
            'Cannot check model status. Make sure the backend server is running.';
      }
      notifyListeners();
    }
  }

  /// Predict gesture from current camera frame
  Future<void> predictGesture() async {
    if (!_isCameraInitialized || _isProcessing) {
      return;
    }

    // Check model status before predicting
    if (!_isModelLoaded) {
      await checkModelStatus();
      if (!_isModelLoaded) {
        _errorMessage =
            'Model not loaded. Please train a model first. See TRAIN_MODEL_GUIDE.md for instructions.';
        notifyListeners();
        return;
      }
    }

    try {
      _isProcessing = true;
      _errorMessage = null;
      notifyListeners();

      // Capture image
      final imageBytes = await _cameraService.captureImage();

      // Send to API
      final prediction = await _apiService.predictGesture(imageBytes);

      _currentPrediction = prediction;
      _isProcessing = false;
      notifyListeners();
    } catch (e) {
      // Clean up error message
      String errorMsg = e.toString();
      if (errorMsg.contains('Model not loaded')) {
        _isModelLoaded = false;
        errorMsg =
            'Model not loaded. Please train a model first. See TRAIN_MODEL_GUIDE.md for instructions.';
      } else if (errorMsg.contains('Connection refused') ||
          errorMsg.contains('Failed host lookup')) {
        errorMsg =
            'Cannot connect to backend server. Make sure the server is running.';
      }
      _errorMessage = errorMsg;
      _isProcessing = false;
      _currentPrediction = null;
      notifyListeners();
    }
  }

  /// Clear current prediction
  void clearPrediction() {
    _currentPrediction = null;
    notifyListeners();
  }

  /// Clear error message
  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }

  /// Check API health
  Future<bool> checkApiHealth() async {
    return await _apiService.checkHealth();
  }

  /// Dispose resources
  @override
  void dispose() {
    _cameraService.dispose();
    super.dispose();
  }
}
