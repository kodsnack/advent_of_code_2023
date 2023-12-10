import '../util/linepos.dart';
import '../util/util.dart';

// const String inputFile = 'day10/example.txt';
const String inputFile = 'day10/input.txt';

Future<void> main(List<String> args) async {
  var input = await readInputAsString(inputFile);

  print('Part 1:');
  final resultP1 = calcResultP1(input);
  print(resultP1);

  print('Part 2:');
  final resultP2 = calcResultP2(input);
  print(resultP2);
}

int calcResultP1(String input) {
  final lines = input.split('\n');

  Grid grid = Grid(lines);
  return grid.solveP1();
}

int calcResultP2(String input) {
  final lines = input.split('\n');

  Grid grid = Grid(lines);
  return grid.solveP2();
}

class Grid {
  Map<LinePos, String> grid = {};
  late int width;
  late int height;

  Grid(List<String> lines) {
    for (int row = 0; row < lines.length; row++) {
      final line = lines[row];
      for (int col = 0; col < line.length; col++) {
        grid[LinePos(col, row)] = line.substring(col, col + 1);
      }
    }
    width = lines[0].length;
    height = lines.length;
    // Add extra points around the grid so we dont have to care about
    // limits
    for (int col = -1; col < width + 1; col++) {
      grid[LinePos(col, -1)] = '.';
      grid[LinePos(col, height)] = '.';
    }
    for (int row = -1; row < height + 1; row++) {
      grid[LinePos(-1, row)] = '.';
      grid[LinePos(width, row)] = '.';
    }
  }

  int solveP1() {
    LinePos? startPoint;
    grid.forEach((key, value) {
      if (value == 'S') {
        startPoint = LinePos(key.col, key.row);
      }
    });
    return findDistToFurthestPoint(startPoint!);
  }

  int solveP2() {
    LinePos? startPoint;
    grid.forEach((key, value) {
      if (value == 'S') {
        startPoint = LinePos(key.col, key.row);
      }
    });
    int count = countEnclosedPoints(startPoint!);
    return count;
  }

  int countEnclosedPoints(LinePos startPoint) {
    final loopPoints = getLoop(startPoint);
    int noOfEnclosedPoints = 0;

    for (int row = 0; row < height; row++) {
      int loopCrossingCount = 0;
      String lastCornerChar = '';
      for (int col = 0; col < width; col++) {
        final currPt = LinePos(col, row);
        final charAtCurrPt = grid[currPt]!;

        if (loopPoints.contains(currPt)) {
          switch (charAtCurrPt) {
            case '|':
              loopCrossingCount++;
              break;
            case 'L':
              lastCornerChar = 'L';
              break;
            case 'F':
              lastCornerChar = 'F';
              break;
            case '7':
              if (lastCornerChar == 'L') loopCrossingCount++;
              break;
            case 'J':
              if (lastCornerChar == 'F') loopCrossingCount++;
              break;
            default:
          }
        } else {
          if (loopCrossingCount % 2 != 0) {
            noOfEnclosedPoints++;
          }
        }
      }
    }
    return noOfEnclosedPoints;
  }

  Map<String, List<String>> connections = {
    '|': ['N', 'S'],
    '-': ['E', 'W'],
    'L': ['N', 'E'],
    'J': ['N', 'W'],
    '7': ['S', 'W'],
    'F': ['S', 'E'],
    'S': ['N', 'W', 'S', 'E'],
  };

  (LinePos, LinePos) findTwoDirections(LinePos point) {
    List<LinePos> connectingPoints = [];
    List<String> directionsToCheck = connections[grid[point]]!;

    for (final direction in directionsToCheck) {
      final pointToCheck = point.moveDirStr(direction);

      List<String>? conns = connections[grid[pointToCheck]];
      final oppositeDirection = LinePos.getOppositeDirection(direction);
      if (conns != null && conns.contains(oppositeDirection))
        connectingPoints.add(pointToCheck);
    }
    assert(connectingPoints.length == 2);
    return (connectingPoints[0], connectingPoints[1]);
  }

  int findDistToFurthestPoint(LinePos startPoint) {
    Set<LinePos> visited = {};
    // Find two directions
    visited.add(startPoint);
    LinePos nextPoint1, nextPoint2;
    (nextPoint1, nextPoint2) = findTwoDirections(startPoint);
    int dist = 0;
    while (nextPoint1 != nextPoint2 &&
        !(visited.contains(nextPoint1) && visited.contains(nextPoint2))) {
      dist++;
      visited.add(nextPoint1);
      nextPoint1 = moveOneStep(nextPoint1, visited);
      visited.add(nextPoint2);
      nextPoint2 = moveOneStep(nextPoint2, visited);
    }
    // If both points are visited we found the place furthest away
    return dist + 1;
  }

  Set<LinePos> getLoop(LinePos startPoint) {
    Set<LinePos> visited = {};
    // Find two directions
    visited.add(startPoint);

    LinePos nextPoint1, nextPoint2;
    (nextPoint1, nextPoint2) = findTwoDirections(startPoint);
    replaceStartPointCharacter(startPoint, nextPoint1, nextPoint2);
    // If both points are visited we found the place furthest away
    while (true) {
      if (nextPoint1 == nextPoint2) {
        visited.add(nextPoint1);
        // drawVisited(visited);
        break;
      }
      if (visited.contains(nextPoint1) && visited.contains(nextPoint2)) break;
      visited.add(nextPoint1);
      nextPoint1 = moveOneStep(nextPoint1, visited);
      visited.add(nextPoint2);
      nextPoint2 = moveOneStep(nextPoint2, visited);
      // drawVisited(visited);
    }
    return visited;
  }

  LinePos moveOneStep(LinePos point, Set<LinePos> visited) {
    LinePos nextPoint1, nextPoint2;
    (nextPoint1, nextPoint2) = findTwoDirections(point);
    return visited.contains(nextPoint1) ? nextPoint2 : nextPoint1;
  }

  void drawVisited(Set<LinePos> visited) {
    for (int row = 0; row < height; row++) {
      String lineToPrint = '';
      for (int col = 0; col < width; col++) {
        if (visited.contains(LinePos(col, row))) {
          lineToPrint += '#';
        } else {
          lineToPrint += grid[LinePos(col, row)]!;
        }
      }
      print(lineToPrint);
    }
    print('');
  }

  void replaceStartPointCharacter(
      LinePos startPoint, LinePos nextPoint1, LinePos nextPoint2) {
    if (nextPoint1 == startPoint.moveN()) {
      if (nextPoint2 == startPoint.moveE()) {
        grid[startPoint] = 'L';
      }
      if (nextPoint2 == startPoint.moveS()) {
        grid[startPoint] = '|';
      }
      if (nextPoint2 == startPoint.moveW()) {
        grid[startPoint] = 'J';
      }
    }
    if (nextPoint1 == startPoint.moveE()) {
      if (nextPoint2 == startPoint.moveN()) {
        grid[startPoint] = 'L';
      }
      if (nextPoint2 == startPoint.moveS()) {
        grid[startPoint] = '|';
      }
      if (nextPoint2 == startPoint.moveW()) {
        grid[startPoint] = '-';
      }
    }
    if (nextPoint1 == startPoint.moveS()) {
      if (nextPoint2 == startPoint.moveN()) {
        grid[startPoint] = '|';
      }
      if (nextPoint2 == startPoint.moveE()) {
        grid[startPoint] = 'F';
      }
      if (nextPoint2 == startPoint.moveW()) {
        grid[startPoint] = '7';
      }
    }
    if (nextPoint1 == startPoint.moveW()) {
      if (nextPoint2 == startPoint.moveN()) {
        grid[startPoint] = 'J';
      }
      if (nextPoint2 == startPoint.moveE()) {
        grid[startPoint] = '-';
      }
      if (nextPoint2 == startPoint.moveS()) {
        grid[startPoint] = '7';
      }
    }
  }
}
