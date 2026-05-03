import 'package:flutter/material.dart';

class CommunityPage extends StatelessWidget {
  const CommunityPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: const [
        ListTile(title: Text('ส่งเคสให้ชุมชนโหวต')),
        ListTile(title: Text('Expert ยืนยันผล')),
        ListTile(title: Text('Reputation + Moderation')),
      ],
    );
  }
}
