import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../../services/measurement_service.dart';

class UploadImageScreen extends StatefulWidget {
  const UploadImageScreen({Key? key}) : super(key: key);

  @override
  _UploadImageScreenState createState() => _UploadImageScreenState();
}

class _UploadImageScreenState extends State<UploadImageScreen> {
  File? _file;
  bool _loading = false;
  final _service = MeasurementService();

  Future<void> _pickFile() async {
    final result = await FilePicker.platform.pickFiles(type: FileType.image);
    if (result != null && result.files.single.path != null) {
      setState(() {
        _file = File(result.files.single.path!);
      });
    }
  }

  Future<void> _upload() async {
    if (_file == null) return;
    setState(() => _loading = true);
    try {
      final resp = await _service.uploadImage(_file!);
      final status = resp.statusCode;
      if (!mounted) return;
      if (status == 200) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Upload successful')));
        Navigator.of(context).pop(true);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Upload failed: $status')));
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Upload Image')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            ElevatedButton.icon(
              onPressed: _pickFile,
              icon: Icon(Icons.photo_library),
              label: Text('Pick image'),
            ),
            SizedBox(height: 16),
            if (_file != null) ...[
              Text('Selected: ${_file!.path.split('/').last}'),
              SizedBox(height: 8),
              Image.file(_file!, height: 200),
            ],
            Spacer(),
            ElevatedButton(
              onPressed: _loading ? null : _upload,
              child: _loading ? CircularProgressIndicator(color: Colors.white) : Text('Upload and Process'),
            ),
          ],
        ),
      ),
    );
  }
}
