
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);


  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'Image Upload'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  File? selectedImage;
  String? message='';

  uploadImage() async{
    final request = http.MultipartRequest("POST", Uri.parse(" https://b6db-89-34-73-154.eu.ngrok.io/upload"));
    final headers = {
      "Content-type": "multipart/form-data"
    };
    request.files.add(
      http.MultipartFile('image',selectedImage!.readAsBytes().asStream(), selectedImage!.lengthSync(), filename: selectedImage!.path.split('/').last)
    );
    request.headers.addAll(headers);
    final response = await request.send();
    http.Response res = await http.Response.fromStream(response);
    final resJson = jsonDecode(res.body);
    message = resJson['message'];
    setState(() {});
  }

  Future getImage() async{
    final pickedImage = await ImagePicker().getImage(source: ImageSource.gallery);
    selectedImage = File(pickedImage!.path);
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(


        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            selectedImage == null
                ? Text("Please pick an image")
                : Image.file(File(selectedImage!.path).absolute,
                  height: 100, width: 100, fit: BoxFit.cover),
            TextButton.icon(
              style: ButtonStyle(
                backgroundColor: MaterialStateProperty.all(Colors.blue),
              ) ,
                onPressed: uploadImage,
                icon: Icon(Icons.upload_file, color: Colors.white),
                label: Text("Upload image", style: TextStyle(color: Colors.white),))
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(onPressed: getImage, child: Icon(Icons.add_a_photo),),
    );
  }
}
