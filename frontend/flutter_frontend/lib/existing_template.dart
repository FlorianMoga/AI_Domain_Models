import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:modal_progress_hud_nsn/modal_progress_hud_nsn.dart';
import 'package:toast/toast.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:async';
import 'package:native_pdf_renderer/native_pdf_renderer.dart';

final Color backgroundColor = Color(0xFF4A4A58);

class ExistingTemplate extends StatefulWidget {
  final String link;
  final String template_image;

  const ExistingTemplate({Key? key, required this.link, required this.template_image}): super(key: key);

  @override
  State<ExistingTemplate> createState() => _ExistingTemplateState();
}

class _ExistingTemplateState extends State<ExistingTemplate> {
  File? selectedFile;
  String? message='';
  bool showSpinner = false;
  late PdfPageImage pageImage;

  uploadFile() async{
    setState(() {
      showSpinner = true;
    });
    try {
      print(widget.link);
      final request = http.MultipartRequest("POST", Uri.parse(widget.link+"/popupalte"));
      final headers = {
        "Content-type": "multipart/form-data"
      };

      request.fields['id'] = '${widget.template_image}';

      request.files.add(
          http.MultipartFile('file',selectedFile!.readAsBytes().asStream(), selectedFile!.lengthSync(), filename: selectedFile!.path.split('/').last)
      );

      request.headers.addAll(headers);

      final response = await request.send();
      http.Response res = await http.Response.fromStream(response).timeout(
          const Duration(seconds: 15));

      if (response.statusCode == 200) {
        message = 'file uploaded';
        Toast.show('image uploaded', duration: Toast.lengthLong,
            gravity: Toast.bottom);
      } else {
        Toast.show(
            'failed to upload', duration: Toast.lengthLong, gravity: Toast.bottom);
      }
    }on TimeoutException catch (e) {
      Toast.show('server not available', duration: Toast.lengthLong,
          gravity: Toast.bottom);
    } on Error catch (e) {
      Toast.show('error: $e', duration: Toast.lengthLong,
          gravity: Toast.bottom);
    }

    setState(() {
      showSpinner = false;
    });
  }

  Future getFile() async{
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      allowMultiple: false,
      type: FileType.custom,
      allowedExtensions: ['jpg', 'pdf', 'png'],
    );

    if (result != null) {
      selectedFile = File(result.files.single.path!);
      if(selectedFile?.path.split(".").last == 'pdf'){
        final document = await PdfDocument.openFile(result.files.single.path!);
        final page = await document.getPage(1);
        pageImage = (await page.render(width: page.width, height: page.height))!;
        await page.close();
      }
    }
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    ToastContext().init(context);
    return
      MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'Flutter Demo',
        theme: ThemeData(
          scaffoldBackgroundColor: backgroundColor,
          inputDecorationTheme: InputDecorationTheme(
            border: OutlineInputBorder(
                borderSide: BorderSide(color: Colors.white)
            ),
          ),
        ),
        home: ModalProgressHUD(
          inAsyncCall: showSpinner,
          child:Scaffold(
            body: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: <Widget>[
                  Text("Populate this Domain Model:", textAlign: TextAlign.center, style: TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 18),),
                  Image(image: AssetImage('assets/templates/'+widget.template_image),
                      height: MediaQuery.of(context).size.width * 0.65 * 1.41421, width: MediaQuery.of(context).size.width * 0.65, fit: BoxFit.cover),
                  selectedFile == null
                      ? Text("Please pick a file based on \n the displayed template", textAlign: TextAlign.center, style: TextStyle(color: Colors.white),)
                      : Text("File chosen✔", textAlign: TextAlign.center, style: TextStyle(color: Colors.white),),
                  SizedBox(height:20)
                ],
              ),
            ),
            floatingActionButton: Container(
                margin: const EdgeInsets.symmetric(horizontal: 8),
                width: 225,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,

                  children: [
                    FloatingActionButton(
                      child: Icon(
                          Icons.cloud_upload
                      ),
                      onPressed: uploadFile,
                      heroTag: null,
                    ),
                    FloatingActionButton(
                      child: Icon(
                          Icons.attach_file
                      ),
                      onPressed: getFile,
                      heroTag: null,
                    )
                  ]
            )
            )
          ),
        ),
      );
  }
}
