import 'dart:math';

import '../util/linepos.dart';
import '../util/util.dart';

// const String inputFile = 'day23/example.txt';
const String inputFile = 'day23/input.txt';

Future<void> main(List<String> args) async {
  var input = await readInputAsString(inputFile);

  Stopwatch swP1 = Stopwatch();
  swP1.start();
  print('Part 1:');
  final resultP1 = calcResult(input);
  print(resultP1);
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

  Board.from(List<String> lines) {
    grid = [...lines];
    height = grid.length;
    width = grid[0].length;
  }

  Map<LinePos, String> createTrailNodes() {
    Map<LinePos, String> trailNodes = {};
    const trailChars = ['.', '<', '>', '^', 'v'];
    for (int row = 0; row < height; row++) {
      for (int col = 0; col < width; col++) {
        String char = grid[row][col];
        if (trailChars.contains(char)) trailNodes[LinePos(col, row)] = char;
      }
    }
    return trailNodes;
  }

  int findLongestHike() {
    LinePos pos = LinePos(1, 0);
    LinePos target = LinePos(grid[0].length - 2, grid.length - 1);

    // Create the nodes
    final trailNodes = createTrailNodes();

    // Put a 'v' in the start position so we can only move into the maze
    // and set its distance to zero
    trailNodes[pos] = 'v';

    int dist = findLongestDistToTarget(pos, LinePos(1, -1), trailNodes, target);

    return dist;
  }

  int findLongestDistToTarget(LinePos pos, LinePos lastPos,
      Map<LinePos, String> trailNodes, LinePos target) {
    if (pos == target) return 0;

    int skipDist = 0;
    List<String> possibledirections =
        getPossibleDirections(trailNodes, pos, lastPos);
    while (possibledirections.length == 1 && pos != target) {
      lastPos = pos;
      pos = pos.moveDirStr(possibledirections.first);
      skipDist++;
      possibledirections = getPossibleDirections(trailNodes, pos, lastPos);
    }
    if (pos == target) return skipDist;

    int maxDist = 0;
    for (final direction in possibledirections) {
      int dist = skipDist +
          1 +
          findLongestDistToTarget(
              pos.moveDirStr(direction), pos, trailNodes, target);
      maxDist = max(maxDist, dist);
    }
    return maxDist;
  }

  List<String> getPossibleDirections(
      Map<LinePos, String> trailNodes, LinePos pos, LinePos lastPos) {
    const slopeChars = {
      '<': 'W',
      '>': 'E',
      '^': 'N',
      'v': 'S',
    };

    String currChar = trailNodes[pos]!;

    List<String> possibledirections;
    if (slopeChars.keys.contains(currChar)) {
      possibledirections = [slopeChars[currChar]!];
    } else {
      possibledirections = [...slopeChars.values];
    }

    possibledirections = possibledirections
        .where((dir) => trailNodes.keys.contains(pos.moveDirStr(dir)))
        .toList();
    possibledirections = possibledirections
        .where((dir) => pos.moveDirStr(dir) != lastPos)
        .toList();
    return possibledirections;
  }

  void printBoard(
      Map<LinePos, String> trailNodes, LinePos currPos, LinePos lastPos) {
    for (int row = 0; row < height; row++) {
      String lineToPrint = '';
      for (int col = 0; col < width; col++) {
        final pos = LinePos(col, row);
        String currChar = '#';
        if (trailNodes.containsKey(pos)) {
          currChar = trailNodes[pos]!;
        }
        if (pos == lastPos) {
          currChar = 'O';
        }
        if (pos == currPos) {
          currChar = 'X';
        }
        lineToPrint += currChar;
      }
      print(lineToPrint);
    }
    print('');
  }
}
