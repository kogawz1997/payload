class Prediction {
  final String thaiName;
  final String englishName;
  final String scientificName;
  final double confidence;
  final bool edible;
  final bool venomous;

  const Prediction({
    required this.thaiName,
    required this.englishName,
    required this.scientificName,
    required this.confidence,
    required this.edible,
    required this.venomous,
  });
}

class ScanResult {
  final String imageId;
  final List<Prediction> topPredictions;
  final bool uncertain;
  final DateTime createdAt;

  const ScanResult({
    required this.imageId,
    required this.topPredictions,
    required this.uncertain,
    required this.createdAt,
  });
}
