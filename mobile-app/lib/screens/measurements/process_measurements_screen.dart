import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../../services/measurement_service.dart';

class ProcessMeasurementsScreen extends StatefulWidget {
  const ProcessMeasurementsScreen({Key? key}) : super(key: key);

  @override
  _ProcessMeasurementsScreenState createState() => _ProcessMeasurementsScreenState();
}

class _ProcessMeasurementsScreenState extends State<ProcessMeasurementsScreen> {
  final Map<String, File?> _photos = {
    'front': null,
    'back': null,
    'left': null,
    'right': null,
  };
  final _heightController = TextEditingController();
  final _weightController = TextEditingController();
  bool _loading = false;
  final _service = MeasurementService();

  Future<void> _pickPhoto(String key) async {
    final result = await FilePicker.platform.pickFiles(type: FileType.image);
    if (result != null && result.files.single.path != null) {
      setState(() {
        _photos[key] = File(result.files.single.path!);
      });
    }
  }

  Future<void> _process() async {
    // Validate
    if (_photos.values.any((f) => f == null)) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Please select all 4 photos')));
      return;
    }
    final height = double.tryParse(_heightController.text);
    final weight = double.tryParse(_weightController.text);
    if (height == null || weight == null) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Please enter valid height and weight')));
      return;
    }
    setState(() => _loading = true);
    try {
      final photos = <String, File>{};
      _photos.forEach((k, v) {
        if (v != null) photos[k] = v;
      });

      // Attempt to process with retries handled in service
      final resp = await _service.processMeasurements(photos, height, weight);
      final status = resp.statusCode;
      final body = await resp.stream.bytesToString();
      if (!mounted) return;

      if (status == 200) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Processing successful')));
        // Parse JSON result and render nicely
        try {
          final data = json.decode(body);
          final measurements = data['measurements'] ?? data['data']?['measurements'] ?? {};
          final confidence = data['confidence'] ?? data['data']?['confidence'] ?? data['data']?['confidence_score'] ?? null;

          // Show parsed measurements in a dialog with retry option
          await showDialog(
            context: context,
            builder: (_) => AlertDialog(
              title: Text('Measurements Result'),
              content: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (measurements is Map && measurements.isNotEmpty)
                      ...measurements.entries.map<Widget>((e) => Padding(
                            padding: const EdgeInsets.symmetric(vertical: 4.0),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [Text(e.key), Text(e.value.toString())],
                            ),
                          ))
                    else
                      Text('No measurement values returned'),
                    if (confidence != null) ...[
                      SizedBox(height: 12),
                      Text('Confidence: ${confidence.toString()}'),
                    ],
                  ],
                ),
              ),
              actions: [
                TextButton(onPressed: () => Navigator.of(context).pop(), child: Text('Close')),
              ],
            ),
          );

          if (!mounted) return;
          Navigator.of(context).pop(true);
        } catch (e) {
          // JSON parse error — show raw body with retry option
          await showDialog(
            context: context,
            builder: (_) => AlertDialog(
              title: Text('Processing Result'),
              content: SingleChildScrollView(child: Text(body)),
              actions: [
                TextButton(onPressed: () => Navigator.of(context).pop(), child: Text('Close')),
              ],
            ),
          );
        }
      } else if (status >= 500) {
        // Server error — offer retry
        final retry = await showDialog<bool>(
          context: context,
          builder: (_) => AlertDialog(
            title: Text('Server error'),
            content: Text('Processing failed with status $status. Do you want to retry?'),
            actions: [
              TextButton(onPressed: () => Navigator.of(context).pop(false), child: Text('Cancel')),
              TextButton(onPressed: () => Navigator.of(context).pop(true), child: Text('Retry')),
            ],
          ),
        );
        if (retry == true) {
          await _process();
          return;
        }
      } else {
        // Client error or validation error — show details and do not retry automatically
        await showDialog(
          context: context,
          builder: (_) => AlertDialog(
            title: Text('Processing failed'),
            content: SingleChildScrollView(child: Text(body)),
            actions: [TextButton(onPressed: () => Navigator.of(context).pop(), child: Text('Close'))],
          ),
        );
      }
    } catch (e) {
      final retry = await showDialog<bool>(
        context: context,
        builder: (_) => AlertDialog(
          title: Text('Error'),
          content: Text('An error occurred: $e. Retry?'),
          actions: [
            TextButton(onPressed: () => Navigator.of(context).pop(false), child: Text('Cancel')),
            TextButton(onPressed: () => Navigator.of(context).pop(true), child: Text('Retry')),
          ],
        ),
      );
      if (retry == true) {
        await _process();
        return;
      }
    } finally {
      setState(() => _loading = false);
    }
  }

  Widget _photoTile(String key) {
    final file = _photos[key];
    return GestureDetector(
      onTap: () => _pickPhoto(key),
      child: Container(
        width: 80,
        height: 80,
        color: Colors.grey[200],
        child: file == null
            ? Center(child: Text(key.toUpperCase()))
            : Image.file(file, fit: BoxFit.cover),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Process Measurements')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text('Select 4 photos (front, back, left, right)'),
            SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _photoTile('front'),
                _photoTile('back'),
                _photoTile('left'),
                _photoTile('right'),
              ],
            ),
            SizedBox(height: 16),
            TextField(controller: _heightController, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: 'Height (cm)')),
            SizedBox(height: 8),
            TextField(controller: _weightController, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: 'Weight (kg)')),
            Spacer(),
            ElevatedButton(onPressed: _loading ? null : _process, child: _loading ? CircularProgressIndicator(color: Colors.white) : Text('Process')),
          ],
        ),
      ),
    );
  }
}
