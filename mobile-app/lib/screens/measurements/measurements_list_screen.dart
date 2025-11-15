import 'dart:convert';
import 'package:flutter/material.dart';
import '../../services/measurement_service.dart';
import 'upload_image_screen.dart';
import 'process_measurements_screen.dart';

class MeasurementsListScreen extends StatefulWidget {
  const MeasurementsListScreen({Key? key}) : super(key: key);

  @override
  _MeasurementsListScreenState createState() => _MeasurementsListScreenState();
}

class _MeasurementsListScreenState extends State<MeasurementsListScreen> {
  final _service = MeasurementService();
  late Future<List<dynamic>> _future;

  @override
  void initState() {
    super.initState();
    _future = _loadMeasurements();
  }

  Future<List<dynamic>> _loadMeasurements() async {
    final resp = await _service.listMeasurements();
    if (resp.statusCode == 200) {
      return json.decode(resp.body) as List<dynamic>;
    }
    throw Exception('Failed to load measurements (${resp.statusCode})');
  }

  void _openUpload() async {
    final result = await Navigator.of(context).push(MaterialPageRoute(builder: (_) => UploadImageScreen()));
    if (result == true) {
      setState(() {
        _future = _loadMeasurements();
      });
    }
  }

  void _openProcess() async {
    final result = await Navigator.of(context).push(MaterialPageRoute(builder: (_) => ProcessMeasurementsScreen()));
    if (result == true) {
      setState(() {
        _future = _loadMeasurements();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Measurements')),
      body: FutureBuilder<List<dynamic>>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) return Center(child: CircularProgressIndicator());
          if (snapshot.hasError) return Center(child: Text('Error: ${snapshot.error}'));
          final items = snapshot.data ?? [];
          if (items.isEmpty) return Center(child: Text('No measurements yet'));
          return ListView.separated(
            itemCount: items.length,
            separatorBuilder: (_, __) => Divider(height: 1),
            itemBuilder: (context, index) {
              final m = items[index];
              return ListTile(
                title: Text('Measurement ${m['id'] ?? index}'),
                subtitle: Text(m['measurements']?.toString() ?? ''),
                onTap: () {},
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _openUpload,
        child: Icon(Icons.upload_file),
        tooltip: 'Upload image',
      ),
      persistentFooterButtons: [
        ElevatedButton.icon(onPressed: _openProcess, icon: Icon(Icons.camera_alt), label: Text('Process photos'))
      ],
    );
  }
}
