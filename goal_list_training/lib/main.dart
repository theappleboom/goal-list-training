import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Goal List App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.white,
          foregroundColor: Colors.black,
        ),
      ),
      home: const MyHomePage(title: 'Goal List'),
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
  final _checkListItems = <String>[
    "Brush Teeth",
    "Comb Hair",
    "Eat Human",
    "Steal Honey",
    "Scratch on Tree",
  ];
  final _finished = <String>{};

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: ListView.builder(
            padding: const EdgeInsets.all(16.0),
            itemCount: 9,
            itemBuilder: (context, i) {
              if (i.isOdd) return const Divider();

              final index = i ~/ 2;

              final checkFinished = _finished.contains(_checkListItems[index]);
              return ListTile(
                  title: Text(
                    _checkListItems[index],
                    style: const TextStyle(fontSize: 20.0),
                  ),
                  trailing: Icon(
                    checkFinished
                        ? Icons.check_circle_outline
                        : Icons.radio_button_unchecked,
                    color: checkFinished
                        ? Colors.green
                        : const Color.fromARGB(255, 128, 79, 7),
                    semanticLabel:
                        checkFinished ? 'Remove from checked' : 'Checked',
                  ),
                  onTap: () {
                    setState(() {
                      if (checkFinished) {
                        _finished.remove(_checkListItems[index]);
                      } else {
                        _finished.add(_checkListItems[index]);
                      }
                    });
                  });
            }),
      ),
    );
  }
}
