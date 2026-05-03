import 'auth_service.dart';

class MockAuthService implements AuthService {
  @override
  Future<String> signInWithProvider(String provider) async {
    await Future<void>.delayed(const Duration(milliseconds: 250));
    return 'mock-token-$provider';
  }

  @override
  Future<void> signOut() async {
    await Future<void>.delayed(const Duration(milliseconds: 100));
  }
}
