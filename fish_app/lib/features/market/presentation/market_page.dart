import 'package:flutter/material.dart';

class MarketPage extends StatelessWidget {
  const MarketPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: const [
        ListTile(title: Text('Seller Listing / Buyer Search')),
        ListTile(title: Text('Matching Engine')),
        ListTile(title: Text('Price Intelligence')),
        ListTile(title: Text('Delivery + Cold Chain')),
      ],
    );
  }
}
