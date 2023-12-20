import '../util/linepos.dart';
import '../util/lprange.dart';
import '../util/util.dart';

const String inputFile = 'day17/example.txt';
// const String inputFile = 'day17/input.txt';

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
  Board board = Board(lines);
  int minHeatLoss = board.getMinHeatLoss();
  return minHeatLoss;
}

int calcResultP2(String input) {
  final lines = input.split('\n');
  Board board = Board(lines);
  int minHeatLoss = board.getMinHeatLoss(part2: true);
  return minHeatLoss;
}

class Board {
  List<List<int>> blocks = [];
  late int width, height;
  LPRange range = LPRange();

  Board(List<String> lines) {
    blocks = [];
    for (final line in lines) {
      blocks.add(line.split('').map((e) => int.parse(e)).toList());
    }
    width = lines[0].length;
    height = lines.length;
    range.extend(LinePos(0, 0));
    range.extend(LinePos(width - 1, height - 1));
  }

  int getMinHeatLoss({bool part2 = false}) {
    final targetPos = LinePos(width - 1, height - 1);

    Set<Node> nodes = {};

    Set<Node> visited = {};
    List<Node> queue = [];

    // Start nodes

    Node startNode = Node(LinePos(0, 0), '', 0);
    startNode.heatLoss = 0;
    queue.add(startNode);
    nodes.add(startNode);

    while (queue.isNotEmpty) {
      final node = queue.removeAt(0);

      int l = visited.length;
      if (l % 1000 == 0) print(l);

      if (node.pos == targetPos) return node.heatLoss;
      if (visited.contains(node)) continue;

      for (final heading in ['E', 'S', 'W', 'N']) {
        final nextPos = node.pos.moveDirStr(heading);

        if (!range.contains(nextPos)) continue; // Out of range
        if (node.heading != '') {
          if (heading == oppositeHeading(node.heading))
            continue; // Cannot turn 180 deg
        }

        if (part2) {
          if (heading == node.heading && node.distInThisDirection > 9)
            continue; // Max 10 straight steps
          if (node.distInThisDirection < 4) {
            if (heading != node.heading && node.heading != '') {
              continue; // We need at least 4 straight steps before we can turn
            }
          }
        } else {
          if (heading == node.heading && node.distInThisDirection > 2)
            continue; // Max 3 straight steps
        }

        int distInThisDir = 1;
        if (heading == node.heading)
          distInThisDir = node.distInThisDirection + 1;

        Node nextNode = Node(nextPos, heading, distInThisDir);
        if (nodes.contains(Node(nextPos, heading, distInThisDir))) {
          nextNode = nodes.firstWhere((stNode) =>
              stNode.pos == nextPos &&
              stNode.heading == heading &&
              stNode.distInThisDirection == distInThisDir);
          nodes.remove(nextNode);
        }

        if (!visited.contains(nextNode)) {
          int heatLoss = node.heatLoss + blocks[nextPos.row][nextPos.col];
          if (heatLoss < nextNode.heatLoss) {
            nextNode.heatLoss = heatLoss;
            nextNode.prevNode = node;
            nodes.add(nextNode);
            insertIntoQueue(queue, nextNode);
          }
        }
      }
      visited.add(node);
    }
    return 0;
  }

  void insertIntoQueue(List<Node> queue, Node node) {
    int indexToInsertBefore =
        queue.indexWhere((element) => element.heatLoss > node.heatLoss);
    if (indexToInsertBefore < 0) {
      queue.add(node);
    } else {
      queue.insert(indexToInsertBefore, node);
    }
  }

  // int getIndexOfNodeWithLowestDist(List<Node> queue) {
  //   int bestLoss = veryLargeNumber * 10;
  //   int indexOfNodeWithLowestDist = -1;
  //   for (int idx = 0; idx < queue.length; idx++) {
  //     Node node = queue[idx];
  //     if (node.heatLoss < bestLoss) {
  //       bestLoss = node.heatLoss;
  //       indexOfNodeWithLowestDist = idx;
  //     }
  //     if (idx == queue.length - 1 && indexOfNodeWithLowestDist == -1) {
  //       print('Wtf?');
  //     }
  //   }
  //   return indexOfNodeWithLowestDist;
  // }
}

String oppositeHeading(String heading) {
  switch (heading) {
    case 'N':
      return 'S';
    case 'E':
      return 'W';
    case 'S':
      return 'N';
    case 'W':
      return 'E';
    default:
      throw ArgumentError('Non existing heading');
  }
}

class Node {
  LinePos pos;
  Node? prevNode;
  String heading;
  int distInThisDirection = 1;
  int heatLoss = veryLargeNumber;
  Node(
    this.pos,
    this.heading,
    this.distInThisDirection,
  );

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Node &&
        pos == other.pos &&
        heading == other.heading &&
        distInThisDirection == other.distInThisDirection;
  }

  int get hashCode {
    String s = pos.toString() + heading + distInThisDirection.toString();
    return s.hashCode;
  }
}
