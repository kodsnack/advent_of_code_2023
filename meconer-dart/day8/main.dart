import '../util/util.dart';

// const String inputFile = 'day8/example.txt';
const String inputFile = 'day8/input.txt';

Future<void> main(List<String> args) async {
  var input = await readInputAsString(inputFile);

  print('Part 1:');
  final resultP1 = calcResultP1(input);
  print(resultP1);

  Stopwatch sw = Stopwatch();
  sw.start();
  print('Part 2:');
  final resultP2 = calcResultP2(input);
  print(resultP2);
  print('${sw.elapsedMicroseconds} us');
}

int calcResultP1(String input) {
  final lines = input.split('\n');
  final instructions = lines[0].split('');

  final nodeMap = getNodes(lines.sublist(2));

  int count = 0;
  String node = 'AAA';
  while (node != 'ZZZ') {
    int instrIdx = count % instructions.length;
    String instr = instructions[instrIdx];
    node = nodeMap[node]![instr]!;
    count++;
  }

  return count;
}

int calcResultP2(String input) {
  final lines = input.split('\n');
  final instructions = lines[0].split('');

  final nodeMap = getNodes(lines.sublist(2));

  List<String> nodes = findAllMapsEndingWith('A', nodeMap);

  List<int> cycleLengths = [];
  for (int nodeNo = 0; nodeNo < nodes.length; nodeNo++) {
    cycleLengths.add(findDistToZ(nodes[nodeNo], nodeMap, instructions));
  }

  int interval = cycleLengths[0];
  int count = interval;
  for (int nodeIdx = 1; nodeIdx < nodes.length; nodeIdx++) {
    while (count % cycleLengths[nodeIdx] != 0) {
      count += interval;
    }
    interval = count;
  }
  return count;
}

int findDistToZ(String node, Map<String, Map<String, String>> nodeMap,
    List<String> instructions) {
  int count = 0;
  while (!node.endsWith('Z')) {
    int instrIdx = count % instructions.length;
    String instr = instructions[instrIdx];
    node = nodeMap[node]![instr]!;
    count++;
  }
  return count;
}

List<String> findAllMapsEndingWith(
    String endStr, Map<String, Map<String, String>> nodeMap) {
  List<String> nodeList = [];
  for (final node in nodeMap.keys) {
    if (node.endsWith(endStr)) {
      nodeList.add(node);
    }
  }
  return nodeList;
}

Map<String, Map<String, String>> getNodes(List<String> lines) {
  Map<String, Map<String, String>> nodeMap = {};
  for (final line in lines) {
    final thisNode = line.split(' =')[0];
    final leftNode = line.split(' = (')[1].split(',')[0];
    String rightNode = line.split(' = (')[1].split(', ')[1];
    rightNode = rightNode.substring(0, rightNode.length - 1);
    Map<String, String> nodes = {};
    nodes['L'] = leftNode;
    nodes['R'] = rightNode;
    nodeMap[thisNode] = nodes;
  }
  return nodeMap;
}
