import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/scan_result.dart';
import '../../features/auth/state/auth_state.dart';
import 'api_config.dart';
import 'scan_service.dart';

class HttpScanService implements ScanService {
  final http.Client client;
  final AuthState authState;
  HttpScanService({required this.client, required this.authState});

  @override
  Future<ScanResult> predictFromImage(String imageId) async {
    final uri = Uri.parse('${ApiConfig.baseUrl}/v1/scan/predict');
    final response = await client.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        if (authState.token != null) 'Authorization': 'Bearer ${authState.token}'
      },
      body: jsonEncode({'image_id': imageId}),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to predict: ${response.statusCode}');
    }

    final data = jsonDecode(response.body) as Map<String, dynamic>;
    final predictions = (data['predictions'] as List<dynamic>)
        .map(
          (raw) => Prediction(
            thaiName: raw['thai_name'] as String,
            englishName: raw['english_name'] as String,
            scientificName: raw['scientific_name'] as String,
            confidence: (raw['confidence'] as num).toDouble(),
            edible: raw['edible'] as bool,
            venomous: raw['venomous'] as bool,
          ),
        )
        .toList();

    return ScanResult(
      imageId: data['image_id'] as String,
      topPredictions: predictions,
      uncertain: data['uncertain'] as bool,
      createdAt: DateTime.parse(data['created_at'] as String),
    );
  }
}
