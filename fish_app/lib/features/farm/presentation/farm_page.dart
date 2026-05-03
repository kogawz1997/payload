import 'package:flutter/material.dart';

class FarmPage extends StatelessWidget {
  const FarmPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: const [
        ListTile(title: Text('Pond Management')),
        ListTile(title: Text('Feeding + FCR')),
        ListTile(title: Text('Water Quality + Alert')),
        ListTile(title: Text('Fish Health + Finance')),
      ],
    );
  }
}
