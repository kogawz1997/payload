import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/models/scan_result.dart';
import '../state/scan_state.dart';

class ScanResultPage extends StatelessWidget {
  final ScanResult result;
  const ScanResultPage({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    final best = result.topPredictions.first;
    return Scaffold(
      appBar: AppBar(title: const Text('ผลการวิเคราะห์')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          ListTile(
            title: Text(best.thaiName),
            subtitle: Text('${best.englishName} • ${best.scientificName}'),
            trailing: Text('${(best.confidence * 100).toStringAsFixed(1)}%'),
          ),
          Card(
            child: ListTile(
              title: const Text('กินได้ไหม'),
              subtitle: Text(best.edible ? 'กินได้' : 'ไม่แนะนำให้กิน'),
            ),
          ),
          Card(
            child: ListTile(
              title: const Text('มีพิษไหม'),
              subtitle: Text(best.venomous ? 'มีพิษ' : 'ไม่พบพิษเด่นชัด'),
            ),
          ),
          if (result.uncertain)
            const ListTile(
              leading: Icon(Icons.warning_amber, color: Colors.orange),
              title: Text('AI ไม่มั่นใจ กรุณาถ่ายเพิ่มมุมหัว/หาง/ครีบ'),
            ),
          const SizedBox(height: 16),
          ElevatedButton.icon(
            onPressed: () {
              context.read<ScanState>().reportWrongAnswer(result);
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('ส่งรายงาน AI ตอบผิดแล้ว')),
              );
            },
            icon: const Icon(Icons.report),
            label: const Text('AI ตอบผิด'),
          ),
          OutlinedButton.icon(
            onPressed: () {
              context.read<ScanState>().requestExpertReview(result);
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('ส่งเคสให้ผู้เชี่ยวชาญตรวจแล้ว')),
              );
            },
            icon: const Icon(Icons.medical_services_outlined),
            label: const Text('ส่งให้ผู้เชี่ยวชาญตรวจ'),
          ),
        ],
      ),
    );
  }
}
