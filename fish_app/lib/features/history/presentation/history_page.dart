import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../scan/presentation/scan_result_page.dart';
import '../../scan/state/scan_state.dart';

class HistoryPage extends StatelessWidget {
  const HistoryPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<ScanState>(
      builder: (_, state, __) {
        if (state.history.isEmpty) {
          return const Center(child: Text('ยังไม่มีประวัติการสแกน'));
        }

        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: state.history.length,
          itemBuilder: (_, index) {
            final item = state.history[index];
            final top = item.topPredictions.first;
            return Card(
              child: ListTile(
                title: Text(top.thaiName),
                subtitle: Text('Confidence ${(top.confidence * 100).toStringAsFixed(1)}%'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => Navigator.of(context).push(
                  MaterialPageRoute(builder: (_) => ScanResultPage(result: item)),
                ),
              ),
            );
          },
        );
      },
    );
  }
}
