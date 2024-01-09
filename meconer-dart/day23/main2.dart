import '../util/linepos.dart';
import '../util/util.dart';

// const String inputFile = 'day23/example.txt';
const String inputFile = 'day23/input.txt';

Future<void> main(List<String> args) async {
  var input = await readInputAsString(inputFile);

  Stopwatch swP1 = Stopwatch();
  swP1.start();
  print('Part 2:');
  final resultP2 = calcResult(input);
  print(resultP2);
  print('${swP1.elapsedMilliseconds} ms');
}

int calcResult(String input) {
  final lines = input.split('\n');
  Board board = Board.from(lines);
  int longestHike = board.findLongestHike();
  return longestHike;
}

class Board {
  List<String> grid = [];
  late int width;
  late int height;
  static int maxMaxDist = 0;

  Board.from(List<String> lines) {
    grid = [...lines];
    height = grid.length;
    width = grid[0].length;
  }

  Set<LinePos> createTrailPoints() {
    Set<LinePos> trailPoints = {};
    const trailChars = ['.', '<', '>', '^', 'v'];
    for (int row = 0; row < height; row++) {
      for (int col = 0; col < width; col++) {
        String char = grid[row][col];
        if (trailChars.contains(char)) trailPoints.add(LinePos(col, row));
      }
    }
    return trailPoints;
  }

  int findLongestHike() {
    LinePos startPos = LinePos(1, 0);
    LinePos targetPos = LinePos(grid[0].length - 2, grid.length - 1);

    // Create the trail
    final trailPoints = createTrailPoints();

    // Find the branches and make nodes
    Set<Node> nodes = {};
    nodes.add(Node(startPos));

    createNodes(
        trailPoints, nodes, LinePos(1, 1), targetPos, 'S', nodes.first, {});
    Set<Branch> branches = createBranches(nodes);
    calculateTopologicalDistToStart(nodes, startPos, branches);
    createBranchFile('day23/branches.csv', branches);
    Set<String> nodeNames = {};
    String startNodeName = 'A';
    String targetNodeName = '';
    for (final node in nodes) {
      if (node.pos == targetPos) targetNodeName = node.name;
      nodeNames.add(node.name);
    }

    // printBoard(trailPoints, LinePos(1, 0), nodes);

    final dist =
        findLongestPath(nodeNames, branches, startNodeName, targetNodeName);

    return dist;
  }

  List<String> getPossibleDirections(
      Set<LinePos> trailPoints, LinePos pos, String lastDirection) {
    List<String> possibledirections = ['N', 'E', 'S', 'W'];

    possibledirections = possibledirections
        .where((dir) => trailPoints.contains(pos.moveDirStr(dir)))
        .toList();
    possibledirections = possibledirections
        .where((dir) => dir != oppositeDirection[lastDirection]!)
        .toList();
    return possibledirections;
  }

  void printBoard(Set<LinePos> trailPoints, LinePos currPos, Set<Node> nodes) {
    for (int row = 0; row < height; row++) {
      String lineToPrint = '';
      for (int col = 0; col < width; col++) {
        final pos = LinePos(col, row);
        final node = nodes.where((element) => element.pos == pos).firstOrNull;
        String currChar = ' ';
        if (trailPoints.contains(pos)) {
          currChar = '.';
        }
        if (node != null) {
          currChar = node.name;
        }
        // if (pos == currPos) {
        //   currChar = 'X';
        // }
        lineToPrint += currChar;
      }
      print(lineToPrint);
    }
    print('');
  }

  static const oppositeDirection = {
    'N': 'S',
    'E': 'W',
    'S': 'N',
    'W': 'E',
  };

  void createNodes(
      Set<LinePos> trailPoints,
      Set<Node> nodes,
      LinePos pos,
      LinePos targetPos,
      String lastDirection,
      Node sourceNode,
      Set<LinePos> visited) {
    // printBoard(trailPoints, pos, nodes);
    var possibleDirections =
        getPossibleDirections(trailPoints, pos, lastDirection);

    // Count dist until we reach a branch where we have more than one possible
    // direction
    int dist = 1;
    while (possibleDirections.length == 1 && pos != targetPos) {
      String direction = possibleDirections.first;
      pos = pos.moveDirStr(direction);
      possibleDirections = getPossibleDirections(trailPoints, pos, direction);
      if (possibleDirections.length == 1) visited.add(pos);
      dist++;
    }

    // Found a branch or the target
    if (visited.contains(pos)) {
      // We have been here before
      // Update this node.
      Node thisNode = nodes.firstWhere((element) => element.pos == pos);
      thisNode.branches.addAll({sourceNode: dist});
      return;
    }
    visited.add(pos);

    if (pos == targetPos) {
      Node targetNode = Node(targetPos);
      nodes.add(targetNode);
      sourceNode.branches.addAll({targetNode: dist});
      return;
    }

    Node? node = nodes.where((n) => n.pos == pos).firstOrNull;
    if (node == null) {
      node = Node(pos);
      nodes.add(node);
    }
    node.branches.addAll({sourceNode: dist});

    for (final direction in possibleDirections) {
      createNodes(trailPoints, nodes, pos.moveDirStr(direction), targetPos,
          direction, node, visited);
    }
  }

  Set<Branch> createBranches(Set<Node> nodes) {
    Set<Branch> branches = {};
    for (final node in nodes) {
      for (final nBranch in node.branches.entries) {
        String n1 = node.name;
        String n2 = nBranch.key.name;
        int dist = nBranch.value;
        final existingBranches = branches.where((br) =>
            (br.node1 == n1 && br.node2 == n2) ||
            (br.node1 == n2 && br.node2 == n1));
        if (existingBranches.isEmpty) {
          Branch branch = Branch(n1, n2, dist);
          print('$n1 - $n2  : d $dist');
          branches.add(branch);
        } else {
          if (dist > existingBranches.first.dist) {
            existingBranches.first.dist = dist;
          }
        }
      }
    }
    return branches;
  }

  List<String> getNeighboursFromBranches(Set<Branch> branches, String node) {
    List<String> neighbours = [];
    for (final branch in branches) {
      if (branch.node1 == node) neighbours.add(branch.node2);
      if (branch.node2 == node) neighbours.add(branch.node1);
    }
    return neighbours;
  }

  int findDistFromBranches(
      Set<Branch> branches, String node, String neighbour) {
    for (final branch in branches) {
      if (branch.node1 == node && branch.node2 == neighbour) return branch.dist;
      if (branch.node2 == node && branch.node1 == neighbour) return branch.dist;
    }
    return -1;
  }

  void createBranchFile(String fileName, Set<Branch> branches) {
    List<String> lines = [];
    lines.add('N1,N2,D');
    for (final branch in branches) {
      lines.add('${branch.node1},${branch.node2},${branch.dist}');
    }
    printToFile(fileName, lines);
  }

  void calculateTopologicalDistToStart(
      Set<Node> nodes, LinePos startPos, Set<Branch> branches) {
    Node startNode = nodes.firstWhere((n) => n.pos == startPos);
    startNode.topologicalDistToStart = 0;
    Set<String> visited = {};
    List<Node> queue = [startNode];
    while (queue.isNotEmpty) {
      Node node = queue.removeAt(0);
      final neighbourNames = getNeighboursFromBranches(branches, node.name);
      int currTopoDist = node.topologicalDistToStart;
      for (final neighbourName in neighbourNames) {
        if (visited.contains(neighbourName)) continue;
        final neighbourNode = nodes.firstWhere((n) => n.name == neighbourName);

        if (currTopoDist + 1 < neighbourNode.topologicalDistToStart) {
          neighbourNode.topologicalDistToStart = currTopoDist + 1;
        }
        queue.add(neighbourNode);
      }
      visited.add(node.name);
    }
  }

  int findLongestPath(Set<String> nodeNames, Set<Branch> branches,
      String startNodeName, String targetNodeName) {
    List<String> currentPath = [startNodeName];
    int maxDist = 0;
    Set<String> visited = {};

    void backtrack(
        String current, List<String> currentPath, int currentLength) {
      visited.add(current);

      if (current == targetNodeName) {
        if (currentLength > maxDist) {
          maxDist = currentLength;
          print('$maxDist - ${currentPath.length}');
          String lineToPrint = '';
          for (final n in currentPath) {
            lineToPrint += n;
          }
          print(lineToPrint);
        }
      } else {
        for (final neighbour in getNeighboursFromBranches(branches, current)) {
          if (!visited.contains(neighbour)) {
            currentPath.add(neighbour);
            backtrack(
                neighbour,
                currentPath,
                currentLength +
                    findDistFromBranches(branches, current, neighbour));
            currentPath.removeLast();
          }
        }
      }

      visited.remove(current);
    }

    backtrack(startNodeName, currentPath, 0);

    return maxDist;
  }
}

class Branch {
  String node1, node2;
  int dist;
  Branch(this.node1, this.node2, this.dist);
}

class Node {
  static String nextName = 'A';
  late String name;
  int topologicalDistToStart = veryLargeNumber;
  LinePos pos;
  Map<Node, int> branches = {};
  Node(this.pos) {
    name = nextName;
    nextName = String.fromCharCode(nextName.codeUnitAt(0) + 1);
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Node && other.pos == pos;
  }

  int get hashCode => pos.hashCode;
}
