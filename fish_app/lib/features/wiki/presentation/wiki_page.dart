import 'package:flutter/material.dart';

class WikiPage extends StatelessWidget {
  const WikiPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: const [
        ListTile(title: Text('ค้นหาด้วยชื่อ/รูป/สี/รูปร่าง')),
        ListTile(title: Text('ข้อมูลปลา: ไทย/อังกฤษ/วิทยาศาสตร์')),
        ListTile(title: Text('ถิ่นอาศัย/ฤดู/กฎหมาย/อนุรักษ์')),
      ],
    );
  }
}
