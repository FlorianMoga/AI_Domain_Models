import 'package:flutter/material.dart';
import 'menu_dashboard_layout.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget{
  @override
  Widget build(BuildContext context){
    return MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'Flutter App',
    theme: ThemeData(
      primarySwatch: Colors.blue
    ),
    home: MenuDashboardPage()
    );
  }
}