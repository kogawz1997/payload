import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';

import '../features/auth/presentation/login_page.dart';
import '../features/auth/state/auth_state.dart';
import '../features/scan/state/scan_state.dart';
import 'services/auth_service.dart';
import 'services/http_scan_service.dart';
import 'services/mock_auth_service.dart';
import 'services/mock_scan_service.dart';
import 'services/scan_service.dart';

class FishIntelligenceApp extends StatelessWidget {
  const FishIntelligenceApp({super.key});

  @override
  Widget build(BuildContext context) {
    const useMock = bool.fromEnvironment('USE_MOCK_SCAN', defaultValue: true);
    final authService = MockAuthService();

    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => AuthState(authService: authService),
        ),
        ChangeNotifierProxyProvider<AuthState, ScanState>(
          create: (_) => ScanState(service: MockScanService()),
          update: (_, authState, __) {
            final ScanService service = useMock
                ? MockScanService()
                : HttpScanService(client: http.Client(), authState: authState);
            return ScanState(service: service);
          },
        ),
      ],
      child: MaterialApp(
        title: 'Fish Intelligence Platform',
        theme: ThemeData(colorSchemeSeed: Colors.teal, useMaterial3: true),
        home: const LoginPage(),
      ),
    );
  }
}
