import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state/auth_state.dart';
import 'mobile_shell.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<AuthState>(
      builder: (_, authState, __) {
        if (authState.isLoggedIn) {
          return MobileShell(authMode: authState.mode ?? 'Unknown');
        }

        return Scaffold(
          appBar: AppBar(title: const Text('เข้าสู่ระบบ')),
          body: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Text('Fish Intelligence Platform', textAlign: TextAlign.center),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: authState.loading ? null : () => authState.signIn('Google'),
                  child: const Text('Login with Google'),
                ),
                ElevatedButton(
                  onPressed: authState.loading ? null : () => authState.signIn('Apple'),
                  child: const Text('Login with Apple'),
                ),
                ElevatedButton(
                  onPressed: authState.loading ? null : () => authState.signIn('Phone'),
                  child: const Text('Login with Phone'),
                ),
                OutlinedButton(
                  onPressed: authState.loading ? null : () => authState.signIn('Guest'),
                  child: const Text('Guest Mode'),
                ),
                const SizedBox(height: 20),
                if (authState.error != null)
                  Text(authState.error!, style: const TextStyle(color: Colors.red)),
              ],
            ),
          ),
        );
      },
    );
  }
}
