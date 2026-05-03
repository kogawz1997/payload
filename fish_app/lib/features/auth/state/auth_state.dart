import 'package:flutter/foundation.dart';

import '../../../core/services/auth_service.dart';

class AuthState extends ChangeNotifier {
  final AuthService authService;
  AuthState({required this.authService});

  bool loading = false;
  String? token;
  String? mode;
  String? error;

  bool get isLoggedIn => token != null;

  Future<void> signIn(String provider) async {
    loading = true;
    error = null;
    notifyListeners();

    try {
      token = await authService.signInWithProvider(provider);
      mode = provider;
    } catch (e) {
      error = e.toString();
    }

    loading = false;
    notifyListeners();
  }

  Future<void> signOut() async {
    loading = true;
    notifyListeners();
    await authService.signOut();
    token = null;
    mode = null;
    loading = false;
    notifyListeners();
  }
}
