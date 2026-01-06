import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/gesture_provider.dart';

/// Widget for displaying gesture recognition feedback
class GestureFeedbackWidget extends StatelessWidget {
  const GestureFeedbackWidget({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Consumer<GestureProvider>(
      builder: (context, gestureProvider, child) {
        final prediction = gestureProvider.currentPrediction;

        if (prediction == null) {
          return const SizedBox.shrink();
        }

        final isCorrect = prediction.isCorrect;
        final color = isCorrect ? Colors.green : Colors.orange;
        final icon = isCorrect ? Icons.check_circle : Icons.info;

        return Container(
          margin: const EdgeInsets.all(16),
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: color.withOpacity(0.9),
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.2),
                blurRadius: 8,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, color: Colors.white, size: 32),
              const SizedBox(width: 12),
              Flexible(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      prediction.message,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    if (prediction.handDetected)
                      Text(
                        'Confidence: ${(prediction.confidence * 100).toStringAsFixed(1)}%',
                        style: const TextStyle(
                          color: Colors.white70,
                          fontSize: 12,
                        ),
                      ),
                  ],
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
