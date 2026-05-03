import 'package:flutter/material.dart';

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: const [
        ListTile(title: Text('Profile / Privacy / Delete Account')),
        ListTile(title: Text('Notification Preferences')),
        ListTile(title: Text('Billing / Subscription')),
        ListTile(title: Text('Export My Data / Consent')),
      ],
    );
  }
}
