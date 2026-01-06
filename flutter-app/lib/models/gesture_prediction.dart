/// Model for gesture prediction response from API
class GesturePrediction {
  final String gesture;
  final double confidence;
  final bool handDetected;
  final String message;

  GesturePrediction({
    required this.gesture,
    required this.confidence,
    required this.handDetected,
    required this.message,
  });

  factory GesturePrediction.fromJson(Map<String, dynamic> json) {
    return GesturePrediction(
      gesture: json['gesture'] ?? 'none',
      confidence: (json['confidence'] ?? 0.0).toDouble(),
      handDetected: json['hand_detected'] ?? false,
      message: json['message'] ?? '',
    );
  }

  bool get isCorrect => confidence >= 0.6 && handDetected;
}

/// Model for ASL gesture information
class GestureInfo {
  final String label;
  final String name;
  final String description;

  GestureInfo({
    required this.label,
    required this.name,
    required this.description,
  });

  factory GestureInfo.fromJson(Map<String, dynamic> json) {
    return GestureInfo(
      label: json['label'] ?? '',
      name: json['name'] ?? '',
      description: json['description'] ?? '',
    );
  }
}

/// Supported ASL gestures
enum ASLGesture {
  hello,
  thankYou,
  yes,
  no,
  iLoveYou,
  none;

  String get displayName {
    switch (this) {
      case ASLGesture.hello:
        return 'Hello';
      case ASLGesture.thankYou:
        return 'Thank You';
      case ASLGesture.yes:
        return 'Yes';
      case ASLGesture.no:
        return 'No';
      case ASLGesture.iLoveYou:
        return 'I Love You';
      case ASLGesture.none:
        return 'None';
    }
  }

  String get label {
    switch (this) {
      case ASLGesture.hello:
        return 'hello';
      case ASLGesture.thankYou:
        return 'thank_you';
      case ASLGesture.yes:
        return 'yes';
      case ASLGesture.no:
        return 'no';
      case ASLGesture.iLoveYou:
        return 'i_love_you';
      case ASLGesture.none:
        return 'none';
    }
  }

  static ASLGesture fromLabel(String label) {
    switch (label) {
      case 'hello':
        return ASLGesture.hello;
      case 'thank_you':
        return ASLGesture.thankYou;
      case 'yes':
        return ASLGesture.yes;
      case 'no':
        return ASLGesture.no;
      case 'i_love_you':
        return ASLGesture.iLoveYou;
      default:
        return ASLGesture.none;
    }
  }
}

