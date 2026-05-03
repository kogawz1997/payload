import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state/auth_state.dart';

import '../../community/presentation/community_page.dart';
import '../../farm/presentation/farm_page.dart';
import '../../history/presentation/history_page.dart';
import '../../market/presentation/market_page.dart';
import '../../scan/presentation/scan_page.dart';
import '../../settings/presentation/settings_page.dart';
import '../../wiki/presentation/wiki_page.dart';

class MobileShell extends StatefulWidget {
  final String authMode;
  const MobileShell({super.key, required this.authMode});

  @override
  State<MobileShell> createState() => _MobileShellState();
}

class _MobileShellState extends State<MobileShell> {
  int index = 0;

  @override
  Widget build(BuildContext context) {
    final pages = [
      const ScanPage(),
      const HistoryPage(),
      const WikiPage(),
      const CommunityPage(),
      const FarmPage(),
      const MarketPage(),
      const SettingsPage(),
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text('Fish Intelligence (${widget.authMode})'),
        actions: [
          IconButton(
            onPressed: () => Navigator.of(context).pushReplacement(
              MaterialPageRoute(builder: (_) => const _SignOutBridge()),
            ),
            icon: const Icon(Icons.logout),
          ),
        ],
      ),
      body: pages[index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: index,
        onDestinationSelected: (v) => setState(() => index = v),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.camera_alt), label: 'Scan'),
          NavigationDestination(icon: Icon(Icons.history), label: 'History'),
          NavigationDestination(icon: Icon(Icons.menu_book), label: 'Wiki'),
          NavigationDestination(icon: Icon(Icons.groups), label: 'Community'),
          NavigationDestination(icon: Icon(Icons.agriculture), label: 'Farm'),
          NavigationDestination(icon: Icon(Icons.storefront), label: 'Market'),
          NavigationDestination(icon: Icon(Icons.settings), label: 'Settings'),
        ],
      ),
    );
  }
}


class _SignOutBridge extends StatelessWidget {
  const _SignOutBridge();

  @override
  Widget build(BuildContext context) {
    Future.microtask(() async {
      await context.read<AuthState>().signOut();
      if (context.mounted) Navigator.of(context).pop();
    });
    return const Scaffold(body: Center(child: CircularProgressIndicator()));
  }
}
