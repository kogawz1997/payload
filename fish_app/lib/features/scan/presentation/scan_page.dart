import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../scan/state/scan_state.dart';
import 'scan_result_page.dart';

class ScanPage extends StatelessWidget {
  const ScanPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<ScanState>(
      builder: (_, state, __) {
        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            const ListTile(title: Text('ถ่ายรูปจากกล้อง')),
            const ListTile(title: Text('อัปโหลดรูปหลายมุม')),
            const ListTile(title: Text('Quality Gate: เบลอ/แสง')),
            ElevatedButton.icon(
              onPressed: state.loading ? null : () => state.runScan('local-image'),
              icon: const Icon(Icons.auto_awesome),
              label: Text(state.loading ? 'กำลังวิเคราะห์...' : 'ลอง AI Scan (Mock)'),
            ),
            const SizedBox(height: 12),
            if (state.error != null)
              ListTile(
                leading: const Icon(Icons.error, color: Colors.red),
                title: Text(state.error!),
              ),
            if (state.lastResult != null) ...[
              Text('Top Predictions', style: Theme.of(context).textTheme.titleMedium),
              ...state.lastResult!.topPredictions.map(
                (p) => Card(
                  child: ListTile(
                    title: Text('${p.thaiName} (${p.scientificName})'),
                    subtitle: Text('Confidence: ${(p.confidence * 100).toStringAsFixed(1)}%'),
                  ),
                ),
              ),
              ElevatedButton(
                onPressed: () => Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (_) => ScanResultPage(result: state.lastResult!),
                  ),
                ),
                child: const Text('ดูผลลัพธ์แบบละเอียด'),
              ),
            ],
          ],
        );
      },
    );
  }
}
