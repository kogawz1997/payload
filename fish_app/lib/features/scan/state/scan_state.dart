import 'package:flutter/foundation.dart';

import '../../../core/models/scan_result.dart';
import '../../../core/services/scan_service.dart';

class ScanState extends ChangeNotifier {
  final ScanService service;
  ScanState({required this.service});

  bool loading = false;
  String? error;
  ScanResult? lastResult;
  final List<ScanResult> history = [];

  Future<void> runScan(String imageId) async {
    loading = true;
    error = null;
    notifyListeners();

    try {
      final result = await service.predictFromImage(imageId);
      lastResult = result;
      history.insert(0, result);
    } catch (e) {
      error = e.toString();
    }

    loading = false;
    notifyListeners();
  }

  void reportWrongAnswer(ScanResult result) {
    debugPrint('Report wrong answer for image ${result.imageId}');
  }

  void requestExpertReview(ScanResult result) {
    debugPrint('Request expert review for image ${result.imageId}');
  }
}
