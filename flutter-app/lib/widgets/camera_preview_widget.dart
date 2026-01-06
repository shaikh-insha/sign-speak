import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:provider/provider.dart';
import '../providers/gesture_provider.dart';

/// Widget for displaying camera preview with overlay
class CameraPreviewWidget extends StatelessWidget {
  final Widget? overlay;
  final bool showLandmarks;

  const CameraPreviewWidget({
    Key? key,
    this.overlay,
    this.showLandmarks = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Consumer<GestureProvider>(
      builder: (context, gestureProvider, child) {
        final cameraService = gestureProvider.cameraService;

        if (!gestureProvider.isCameraInitialized) {
          return const Center(
            child: CircularProgressIndicator(),
          );
        }

        final controller = cameraService.controller;
        if (controller == null) {
          return const Center(
            child: Text('Camera not available'),
          );
        }

        return Stack(
          fit: StackFit.expand,
          children: [
            // Camera preview
            CameraPreview(controller),
            // Overlay (for landmarks, feedback, etc.)
            if (overlay != null) overlay!,
          ],
        );
      },
    );
  }
}
