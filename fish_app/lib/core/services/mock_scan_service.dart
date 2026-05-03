import '../models/scan_result.dart';
import 'scan_service.dart';

class MockScanService implements ScanService {
  @override
  Future<ScanResult> predictFromImage(String imageId) async {
    await Future<void>.delayed(const Duration(milliseconds: 300));

    const predictions = [
      Prediction(
        thaiName: 'ปลานิล',
        englishName: 'Nile tilapia',
        scientificName: 'Oreochromis niloticus',
        confidence: 0.86,
        edible: true,
        venomous: false,
      ),
      Prediction(
        thaiName: 'ปลาทับทิม',
        englishName: 'Red tilapia',
        scientificName: 'Oreochromis spp.',
        confidence: 0.63,
        edible: true,
        venomous: false,
      ),
      Prediction(
        thaiName: 'ปลาดุก',
        englishName: 'Walking catfish',
        scientificName: 'Clarias batrachus',
        confidence: 0.34,
        edible: true,
        venomous: false,
      ),
    ];

    return ScanResult(
      imageId: imageId,
      topPredictions: predictions,
      uncertain: predictions.first.confidence < 0.7,
      createdAt: DateTime.now(),
    );
  }
}
