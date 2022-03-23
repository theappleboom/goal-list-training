import 'dart:async';

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
  final _goalList = GoalList();

  void _pushListEditor() {
    Navigator.of(context).push(
      MaterialPageRoute(
          builder: (context) => GoalListInspector(goalList: _goalList)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
        actions: [
          IconButton(
              icon: const Icon(Icons.list),
              onPressed: _pushListEditor,
              tooltip: 'Inspect Goal List'),
        ],
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

class GoalListInspector extends StatefulWidget {
  const GoalListInspector({Key? key, required this.goalList}) : super(key: key);
  final GoalList goalList;

  @override
  State<GoalListInspector> createState() => _GoalListInspectorState();
}

class _GoalListInspectorState extends State<GoalListInspector> {
  var _itemList = <GoalListItem>[];

  void _pushItemAdder() {
    Navigator.of(context)
        .push(
      MaterialPageRoute(
          builder: (context) => ItemAdder(goalList: widget.goalList)),
    )
        .then((_) {
      // Updates the list after an item has been added
      setState(() {});
    });
  }

  void listUpdateCallback() {}

  @override
  void initState() {
    super.initState();
    _itemList = widget.goalList.listItems;
  }

  @override
  Widget build(BuildContext context) {
    final tiles = _itemList.map((listItem) {
      return ListTile(
        title: Text(
          listItem.name,
          style: const TextStyle(fontSize: 20.0),
        ),
      );
    });
    final divided = tiles.isNotEmpty
        ? ListTile.divideTiles(context: context, tiles: tiles).toList()
        : <Widget>[];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Current Goal List'),
      ),
      body: ListView(children: divided),
      floatingActionButton: FloatingActionButton(
          child: const Icon(Icons.add), onPressed: _pushItemAdder),
    );
  }
}

class ItemAdder extends StatefulWidget {
  const ItemAdder({Key? key, required this.goalList}) : super(key: key);
  final GoalList goalList;

  @override
  State<ItemAdder> createState() => _ItemAdderState();
}

class _ItemAdderState extends State<ItemAdder> {
  String _newItemName = "";
  String _newItemRarity = "Common";

  void _addNewItem() {
    int rarity = 0;

    if (_newItemName != "") {
      switch (_newItemRarity) {
        case "Common":
          rarity = 0;
          break;
        case "Uncommon":
          rarity = 1;
          break;
        case "Rare":
          rarity = 2;
          break;
      }
      widget.goalList.addListItem(_newItemName, rarity);
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add a New Item'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(24.0),
            child: TextFormField(
              onChanged: (newValue) {
                setState(() {
                  _newItemName = newValue.toString();
                });
              },
              decoration: const InputDecoration(
                labelText: 'New List Item',
              ),
            ),
          ),
          Container(
            alignment: AlignmentDirectional.topStart,
            padding: const EdgeInsets.all(24.0),
            child: DropdownButton<String>(
              hint: const Text('How often should this item show'),
              value: _newItemRarity,
              onChanged: (value) {
                setState(() {
                  _newItemRarity = value.toString();
                });
              },
              items: <String>["Common", "Uncommon", "Rare"].map((itemValue) {
                return DropdownMenuItem<String>(
                  value: itemValue,
                  child: Text(itemValue),
                );
              }).toList(),
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
          child: const Icon(Icons.check), onPressed: _addNewItem),
    );
  }
}

class GoalListItem {
  String name;
  int rarity;
  int weight;

  GoalListItem(this.name, this.rarity, this.weight);
}

class GoalList {
  List<GoalListItem> listItems;

  GoalList() : listItems = <GoalListItem>[];

  addListItem(String name, int rarity) {
    listItems.add(GoalListItem(name, rarity, 0));
  }
}
