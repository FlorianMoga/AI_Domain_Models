import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:untitled/new_template.dart';
import 'package:toast/toast.dart';
import 'package:http/http.dart' as http;
import 'package:webview_flutter/webview_flutter.dart';


import 'existing_template.dart';

final Color backgroundColor = Color(0xFF4A4A58);

class MenuDashboardPage extends StatefulWidget {
  @override
  _MenuDashboardPageState createState() => _MenuDashboardPageState();
}

class _MenuDashboardPageState extends State<MenuDashboardPage> with SingleTickerProviderStateMixin {
  bool isCollapsed = true;
  late double screenWidth, screenHeight;
  final Duration duration = const Duration(milliseconds: 300);
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  late Animation<double> _menuScaleAnimation;
  late Animation<Offset> _slideAnimation;
  String link = '';
  String token = '';
  String domainModel = '';
  final _formKey = GlobalKey<FormState>();
  int currentPage = 1;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: duration);
    _scaleAnimation = Tween<double>(begin: 1, end: 0.8).animate(_controller);
    _menuScaleAnimation = Tween<double>(begin: 0.5, end: 1).animate(_controller);
    _slideAnimation = Tween<Offset>(begin: Offset(-1, 0), end: Offset(0, 0)).animate(_controller);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    ToastContext().init(context);
    Size size = MediaQuery.of(context).size;
    screenHeight = size.height;
    screenWidth = size.width;

    return Scaffold(
      backgroundColor: backgroundColor,
      body: Stack(
        children: <Widget>[
          menu(context),
          currentPage == 1 ? dashboard1(context) : currentPage == 3 ? dashboard3(context) : dashboard2(context),
        ],
      ),
    );
  }

  Widget menu(context) {
    return SlideTransition(
      position: _slideAnimation,
      child: ScaleTransition(
        scale: _menuScaleAnimation,
        child: Padding(
          padding: const EdgeInsets.only(left: 16.0),
          child: Align(
            alignment: Alignment.centerLeft,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                GestureDetector(
                  onTap: () {
                  currentPage = 1;
                  setState(() {});
                },
                  child: Text("Home", style: TextStyle(color: Colors.white, fontSize: 22)),
                ),
                SizedBox(height: 10),
                GestureDetector(
                  onTap: () {
                    currentPage = 2;
                    setState(() {});
                  },
                  child: Text("Domain Models", style: TextStyle(color: Colors.white, fontSize: 22)),
                ),
                SizedBox(height: 10),
                GestureDetector(
                  onTap: () {
                    currentPage = 3;
                    setState(() {});
                  },
                  child: Text("Initialize", style: TextStyle(color: Colors.white, fontSize: 22)),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget dashboard1(context) {
    print(currentPage);
    return AnimatedPositioned(
      duration: duration,
      top: 0,
      bottom: 0,
      left: isCollapsed ? 0 : 0.6 * screenWidth,
      right: isCollapsed ? 0 : -0.2 * screenWidth,
      child: ScaleTransition(
        scale: _scaleAnimation,
        child: Material(
          animationDuration: duration,
          borderRadius: BorderRadius.all(Radius.circular(40)),
          elevation: 8,
          color: backgroundColor,
          child: SingleChildScrollView(
            scrollDirection: Axis.vertical,
            physics: ClampingScrollPhysics(),
            child: Container(
              padding: const EdgeInsets.only(left: 16, right: 16, top: 48),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Row(
                    // mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    mainAxisSize: MainAxisSize.max,
                    children: [
                      InkWell(
                        child: Icon(Icons.menu, color: Colors.white),
                        onTap: () {
                          setState(() {
                            if (isCollapsed)
                              _controller.forward();
                            else
                              _controller.reverse();

                            isCollapsed = !isCollapsed;
                          });
                        },
                      ),
                      SizedBox(width: 100,),
                      Image.asset('assets/gep_logo.png')
                    ],
                  ),
                  SizedBox(height: 50),
                  Text("Invoices:", style: TextStyle(color: Colors.white, fontSize: 20),),
                  SizedBox(height: 20),
                  Container(
                    height: 600,
                    child: PageView(
                      controller: PageController(viewportFraction: 0.8),
                      scrollDirection: Axis.horizontal,
                      pageSnapping: true,
                      children: <Widget>[
                        Container(
                          margin: const EdgeInsets.symmetric(horizontal: 8),
                          width: 110,
                            decoration: BoxDecoration(
                              border: Border.all(
                                color: Color(0xff30598e),
                                  width: 3,
                              ),
                            ),
                          child: new NewTemplate(link:this.link)
                        ),
                        Container(
                          margin: const EdgeInsets.symmetric(horizontal: 8),
                          width: 100,
                            decoration: BoxDecoration(
                              border: Border.all(
                                color: Color(0xff30598e),
                                width: 3,
                              ),
                            ),
                          child: new ExistingTemplate(link:this.link, template_image:"invoice.png")
                        ),
                        Container(
                          margin: const EdgeInsets.symmetric(horizontal: 8),
                            decoration: BoxDecoration(
                              border: Border.all(
                                color: Color(0xff30598e),
                                width: 3,
                              ),
                            ),
                          width: 100,
                          child: new ExistingTemplate(link: this.link, template_image: "img.png")
                        ),
                      ],
                    ),
                  ),
                  SizedBox(height: 20)
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget dashboard2(context) {
    print(currentPage);
    return AnimatedPositioned(
      duration: duration,
      top: 0,
      bottom: 0,
      left: isCollapsed ? 0 : 0.6 * screenWidth,
      right: isCollapsed ? 0 : -0.2 * screenWidth,
      child: ScaleTransition(
        scale: _scaleAnimation,
        child: Material(
          animationDuration: duration,
          borderRadius: BorderRadius.all(Radius.circular(40)),
          elevation: 8,
          color: backgroundColor,
          child: SingleChildScrollView(
            scrollDirection: Axis.vertical,
            physics: ClampingScrollPhysics(),
            child: Container(
              padding: const EdgeInsets.only(left: 16, right: 16, top: 48),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Row(
                    // mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    mainAxisSize: MainAxisSize.max,
                    children: [
                      InkWell(
                        child: Icon(Icons.menu, color: Colors.white),
                        onTap: () {
                          setState(() {
                            if (isCollapsed)
                              _controller.forward();
                            else
                              _controller.reverse();

                            isCollapsed = !isCollapsed;
                          });
                        },
                      ),
                      SizedBox(width: 100,),
                      Image.asset('assets/gep_logo.png')
                    ],
                  ),
                  SizedBox(height: 50),
                  Container(
                    height: 600,
                    child: PageView(
                      controller: PageController(viewportFraction: 0.8),
                      scrollDirection: Axis.horizontal,
                      pageSnapping: true,
                      children: <Widget>[
                        Scaffold(
                          appBar: AppBar(
                            title: const Text('Domain Model:', textAlign: TextAlign.center),
                            backgroundColor: backgroundColor,
                            toolbarHeight: 20,
                          ),
                          body: WebView(
                            initialUrl: this.domainModel,
                            javascriptMode: JavascriptMode.unrestricted,
                          ),
                        )
                      ],
                    ),
                  ),
                  SizedBox(height: 20)
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget dashboard3(context) {
    print(currentPage);
    return AnimatedPositioned(
      duration: duration,
      top: 0,
      bottom: 0,
      left: isCollapsed ? 0 : 0.6 * screenWidth,
      right: isCollapsed ? 0 : -0.2 * screenWidth,
      child: ScaleTransition(
        scale: _scaleAnimation,
        child: Material(
          animationDuration: duration,
          borderRadius: BorderRadius.all(Radius.circular(40)),
          elevation: 8,
          color: backgroundColor,
          child: SingleChildScrollView(
            scrollDirection: Axis.vertical,
            physics: ClampingScrollPhysics(),
            child: Container(
              padding: const EdgeInsets.only(left: 16, right: 16, top: 48),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Row(
                    // mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    mainAxisSize: MainAxisSize.max,
                    children: [
                      InkWell(
                        child: const Icon(Icons.menu, color: Colors.white),
                        onTap: () {
                          setState(() {
                            if (isCollapsed)
                              _controller.forward();
                            else
                              _controller.reverse();

                            isCollapsed = !isCollapsed;
                          });
                        },
                      ),
                      const SizedBox(width: 100,),
                      Image.asset('assets/gep_logo.png')
                    ],
                  ),
                  const SizedBox(height: 50),
                  SizedBox(
                    height: 600,
                    child: PageView(
                      controller: PageController(viewportFraction: 0.8),
                      scrollDirection: Axis.horizontal,
                      pageSnapping: true,
                      children: <Widget>[
                        Form(
                          key: _formKey,
                          child:Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                                TextFormField(
                                    style: TextStyle(color: Colors.white),
                                    initialValue: this.link,
                                    decoration: const InputDecoration(
                                        labelText: "Api Url",
                                        labelStyle: TextStyle(fontSize: 18, color: Colors.white),
                                        enabledBorder: OutlineInputBorder(
                                          borderSide: BorderSide(color: Colors.white, width: 2),
                                        ),
                                      prefixIcon: Icon(Icons.backup, color: Colors.white), iconColor: Colors.white),
                                  onSaved: (String? value) {
                                  link = value!;
                                }
                                ),
                                const SizedBox(height: 50),
                                TextFormField(
                                    style: TextStyle(color: Colors.white),
                                    initialValue: this.token,
                                    decoration: const InputDecoration(
                                          labelText: "Token",
                                          labelStyle: TextStyle(fontSize: 18, color: Colors.white),
                                          enabledBorder: OutlineInputBorder(
                                            borderSide: BorderSide(color: Colors.white, width: 2),
                                          ),
                                        prefixIcon: Icon(Icons.vpn_lock, color: Colors.white), iconColor: Colors.white),
                                    onSaved: (String? value) {
                                      token = value!;
                                    }
                                ),
                                const SizedBox(height: 50),
                                TextFormField(
                                    style: TextStyle(color: Colors.white),
                                    initialValue: this.domainModel,
                                    decoration: const InputDecoration(
                                        labelText: "Domain Model Link",
                                        labelStyle: TextStyle(fontSize: 18, color: Colors.white),
                                        enabledBorder: OutlineInputBorder(
                                          borderSide: BorderSide(color: Colors.white, width: 2),
                                        ),
                                        prefixIcon: Icon(Icons.assessment, color: Colors.white), iconColor: Colors.white),
                                    onSaved: (String? value) {
                                      domainModel = value!;
                                    }
                                ),
                              const SizedBox(height: 80),
                              SizedBox(
                                width: 400, // <-- Your width
                                height: 50,
                                child:ElevatedButton(
                                    style: ButtonStyle(
                                      backgroundColor: MaterialStateProperty.all(Color(0xff30598e)),
                                    ) ,
                                    onPressed: () {
                                      _formKey.currentState!.save();
                                      print(link);
                                      print(token);
                                      print(domainModel);

                                      try{
                                        uploadToken();
                                        Toast.show('Configuration Saved', duration: Toast.lengthLong, gravity: Toast.bottom);
                                      }catch(e){
                                        Toast.show('Error: $e', duration: Toast.lengthLong, gravity: Toast.bottom);
                                      }
                                    },
                                    child: Text('Submit', style: TextStyle(fontSize: 20),))
                              )
                            ],
                          )
                        )
                    ]
                    ),
                  ),
                  const SizedBox(height: 20)
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }


  Future<http.Response> uploadToken () async {
    Map data = {'token': token};
    //encode Map to JSON
    var body = json.encode(data);

    var response = await http.post(Uri.parse(link+"/token"),
        headers: {"Content-Type": "application/json"},
        body: body
    );
    print("${response.statusCode}");
    print("${response.body}");
    return response;
  }
}
