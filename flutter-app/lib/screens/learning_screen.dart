import 'package:flutter/material.dart';
import '../models/gesture_prediction.dart';
import '../services/api_service.dart';

/// Screen for learning ASL gestures (non-ML mode)
class LearningScreen extends StatefulWidget {
  const LearningScreen({Key? key}) : super(key: key);

  @override
  State<LearningScreen> createState() => _LearningScreenState();
}

class _LearningScreenState extends State<LearningScreen> {
  final ApiService _apiService = ApiService();
  List<GestureInfo> _gestures = [];
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadGestures();
  }

  Future<void> _loadGestures() async {
    try {
      setState(() {
        _isLoading = true;
        _errorMessage = null;
      });

      final gestures = await _apiService.getGestures();
      setState(() {
        _gestures = gestures;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'Failed to load gestures: $e';
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Learn ASL'),
        backgroundColor: Colors.blue.shade700,
        foregroundColor: Colors.white,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _errorMessage != null
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.error_outline,
                          size: 64, color: Colors.red),
                      const SizedBox(height: 16),
                      Text(
                        _errorMessage!,
                        textAlign: TextAlign.center,
                        style: const TextStyle(fontSize: 16),
                      ),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: _loadGestures,
                        child: const Text('Retry'),
                      ),
                    ],
                  ),
                )
              : _gestures.isEmpty
                  ? const Center(
                      child: Text('No gestures available'),
                    )
                  : ListView.builder(
                      padding: const EdgeInsets.all(16),
                      itemCount: _gestures.length,
                      itemBuilder: (context, index) {
                        final gesture = _gestures[index];
                        return _GestureCard(gesture: gesture);
                      },
                    ),
    );
  }
}

/// Card widget for displaying gesture information
class _GestureCard extends StatelessWidget {
  final GestureInfo gesture;

  const _GestureCard({required this.gesture});

  IconData _getGestureIcon(String label) {
    switch (label) {
      case 'hello':
        return Icons.waving_hand;
      case 'thank_you':
        return Icons.favorite;
      case 'yes':
        return Icons.thumb_up;
      case 'no':
        return Icons.thumb_down;
      case 'i_love_you':
        return Icons.favorite_border;
      default:
        return Icons.gesture;
    }
  }

  Color _getGestureColor(String label) {
    switch (label) {
      case 'hello':
        return Colors.blue;
      case 'thank_you':
        return Colors.green;
      case 'yes':
        return Colors.orange;
      case 'no':
        return Colors.red;
      case 'i_love_you':
        return Colors.pink;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: _getGestureColor(gesture.label).withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    _getGestureIcon(gesture.label),
                    color: _getGestureColor(gesture.label),
                    size: 32,
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        gesture.name,
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Text(
                        gesture.label.replaceAll('_', ' ').toUpperCase(),
                        style: TextStyle(
                          fontSize: 12,
                          color: Colors.grey.shade600,
                          letterSpacing: 1,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.grey.shade100,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                children: [
                  Icon(Icons.info_outline, color: Colors.grey.shade700),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      gesture.description,
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey.shade800,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
