import 'package:fish_app/core/app.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('app boots and shows login title', (tester) async {
    await tester.pumpWidget(const FishIntelligenceApp());
    expect(find.text('เข้าสู่ระบบ'), findsOneWidget);
  });
}
