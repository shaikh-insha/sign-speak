import 'dart:typed_data';
import 'package:camera/camera.dart';
import 'package:image/image.dart' as img;

/// Service for managing camera operations
class CameraService {
  CameraController? _controller;
  List<CameraDescription>? _cameras;
  bool _isInitialized = false;

  CameraController? get controller => _controller;
  bool get isInitialized => _isInitialized;
  bool get isInitializing => _controller?.value.isInitialized == false;

  /// Initialize camera
  Future<void> initialize() async {
    try {
      _cameras = await availableCameras();
      if (_cameras == null || _cameras!.isEmpty) {
        throw Exception('No cameras available');
      }

      // Use front camera by default (better for selfie-style ASL practice)
      _controller = CameraController(
        _cameras![0],
        ResolutionPreset.medium, // Balance between quality and performance
        enableAudio: false,
      );

      await _controller!.initialize();
      _isInitialized = true;
    } catch (e) {
      _isInitialized = false;
      throw Exception('Failed to initialize camera: $e');
    }
  }

  /// Capture image and convert to bytes
  Future<Uint8List> captureImage() async {
    if (_controller == null || !_controller!.value.isInitialized) {
      throw Exception('Camera not initialized');
    }

    try {
      final XFile imageFile = await _controller!.takePicture();
      final Uint8List imageBytes = await imageFile.readAsBytes();

      // Convert to JPEG format for API
      final img.Image? image = img.decodeImage(imageBytes);
      if (image == null) {
        throw Exception('Failed to decode image');
      }

      // Convert to JPEG with quality 85
      final Uint8List jpegBytes = Uint8List.fromList(
        img.encodeJpg(image, quality: 85),
      );

      return jpegBytes;
    } catch (e) {
      throw Exception('Failed to capture image: $e');
    }
  }

  /// Dispose camera resources
  Future<void> dispose() async {
    await _controller?.dispose();
    _controller = null;
    _isInitialized = false;
  }

  /// Switch between front and back camera
  Future<void> switchCamera() async {
    if (_cameras == null || _cameras!.length < 2) {
      return; // Only one camera available
    }

    final currentIndex = _cameras!.indexOf(_controller!.description);
    final newIndex = (currentIndex + 1) % _cameras!.length;

    await _controller?.dispose();
    _controller = CameraController(
      _cameras![newIndex],
      ResolutionPreset.medium,
      enableAudio: false,
    );

    await _controller!.initialize();
  }
}
