import '../util/util.dart';

// const String inputFile = 'day25/example.txt';
const String inputFile = 'day25/input.txt';

Future<void> main(List<String> args) async {
  var input = await readInputAsString(inputFile);

  Stopwatch swP1 = Stopwatch();
  swP1.start();
  print('Part 1:');
  final resultP1 = calcResultP1(input);
  print(resultP1);
  print('${swP1.elapsedMilliseconds} ms');

  // Stopwatch swP2 = Stopwatch();
  // swP2.start();
  // print('Part 2:');
  // final resultP2 = calcResultP2(input);
  // print(resultP2);
  // print('${swP2.elapsedMilliseconds} ms');
}

int calcResultP1(String input) {
  final lines = input.split('\n');
  Map<String, Set<String>> connections = {};
  Map<String, int> edgeCounts = {};
  Set<String> nodes = {};
  List<Edge> edges = [];
  for (final line in lines) {
    final comp1 = line.split(': ')[0];
    nodes.add(comp1);

    if (!edgeCounts.containsKey(comp1)) {
      edgeCounts[comp1] = 0;
    }

    final comps = line.split(': ')[1].split(' ');
    if (!connections.containsKey(comp1)) connections[comp1] = {};
    connections[comp1]!.addAll(comps.toSet());
    nodes.addAll(comps);

    edgeCounts[comp1] = edgeCounts[comp1]! + comps.length;

    for (final comp in comps) {
      if (!edges.contains(Edge(comp, comp1))) edges.add(Edge(comp1, comp));

      edgeCounts[comp] = (edgeCounts[comp] ?? 0) + 1;
    }

    for (final comp in comps) {
      if (!connections.containsKey(comp)) connections[comp] = {};
      connections[comp]!.add(comp1);
    }
  }

  Map<int, int> counts = {};
  int noOfNodesWithOddEdges = 0;
  for (final edgeCount in edgeCounts.values) {
    if (edgeCount % 2 != 0) {
      noOfNodesWithOddEdges++;
    }
    counts[edgeCount] = (counts[edgeCount] ?? 0) + 1;
  }

  List<String> outLines = [];
  for (final edge in edges) {
    outLines.add('${edge.node1},${edge.node2}');
  }
  printToFile('day25/outfile.csv', outLines);

  int remIdx1 = edges.indexWhere((edge) =>
      (edge.node1 == 'bmx' && edge.node2 == 'zlv') ||
      (edge.node1 == 'zlv' && edge.node2 == 'bmx'));
  int remIdx2 = edges.indexWhere((edge) =>
      (edge.node1 == 'xsl' && edge.node2 == 'tpb') ||
      (edge.node1 == 'tpb' && edge.node2 == 'xsl'));
  int remIdx3 = edges.indexWhere((edge) =>
      (edge.node1 == 'qpg' && edge.node2 == 'lrd') ||
      (edge.node1 == 'lrd' && edge.node2 == 'qpg'));
  final edgesToTest = [...edges];
  edgesToTest.removeAt(remIdx3);
  edgesToTest.removeAt(remIdx2);
  edgesToTest.removeAt(remIdx1);

  final (groupCount, result) = countGroups(edgesToTest);
  if (groupCount == 2) return result;

  return 0;
}

class Edge {
  String node1;
  String node2;
  Edge(this.node1, this.node2);
}

(int, int) countGroups(List<Edge> edges) {
  List<Set<String>> groups = [];

  int maxGroupLength = 0;
  for (final edge in edges) {
    int currGroupLength = groups.length;
    if (currGroupLength > maxGroupLength) {
      maxGroupLength = currGroupLength;
      print('Groups : ${currGroupLength}');
    }

    if (groups.isEmpty) {
      Set<String> group = {};
      group.add(edge.node1);
      group.add(edge.node2);
      groups.add(group);
      continue;
    }
    // There are existing groups. Check which group that this edge connects
    // belongs to
    int groupIdx1 = groups.indexWhere((group) => group.contains(edge.node1));

    int groupIdx2 = groups.indexWhere((group) => group.contains(edge.node2));

    switch ((groupIdx1, groupIdx2)) {
      case ((-1, -1)):
        // None of the nodes exist to a group so we create a new
        Set<String> group = {};
        // And add both nods to this group
        group.add(edge.node1);
        group.add(edge.node2);
        groups.add(group);

      case ((>= 0, -1)):
        // First node belongs to a group. Add the other
        // node to the same group
        groups[groupIdx1].add(edge.node2);

      case ((-1, >= 0)):
        // Second node belongs to a group. Add the other
        // node to the same group
        groups[groupIdx2].add(edge.node1);

      case ((>= 0, >= 0)):
        {
          // Both nodes belongs to a group. If they belong to different groups we
          // need to merge them as long as we dont get fewer groups than 2.
          if (groupIdx1 != groupIdx2) {
            groups[groupIdx1].addAll(groups[groupIdx2]);
            groups.removeAt(groupIdx2);
            print('${edge.node1} - ${edge.node2}');
          }
        }
    }
  }

  int result = 0;
  if (groups.length == 2) {
    result = groups[0].length * groups[1].length;
  }
  return (groups.length, result);
}
