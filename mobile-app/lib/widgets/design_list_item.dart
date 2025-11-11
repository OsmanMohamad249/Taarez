// lib/widgets/design_list_item.dart
import 'package:flutter/material.dart';
import '../models/design.dart';
import '../utils/helpers.dart';

class DesignListItem extends StatelessWidget {
  final Design design;
  
  const DesignListItem({Key? key, required this.design}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
      ),
      child: ListTile(
        leading: Container(
          width: 50,
          height: 50,
          decoration: BoxDecoration(
            color: Colors.blue.shade50,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(
            Icons.checkroom,
            color: Colors.blue.shade700,
            size: 30,
          ),
        ),
        title: Text(
          design.name,
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
        subtitle: Text(
          'Starts at ${Helpers.formatCurrency(design.basePrice, symbol: 'SAR ')}',
          style: TextStyle(
            color: Colors.green.shade700,
            fontWeight: FontWeight.w500,
          ),
        ),
        trailing: Icon(
          Icons.chevron_right,
          color: Colors.grey.shade400,
        ),
        onTap: () {
          // TODO: Navigate to detail screen in the future
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Design: ${design.name}')),
          );
        },
      ),
    );
  }
}
