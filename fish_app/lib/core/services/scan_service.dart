import '../models/scan_result.dart';

abstract class ScanService {
  Future<ScanResult> predictFromImage(String imageId);
}
