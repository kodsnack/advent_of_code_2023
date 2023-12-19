import 'dart:math';

import '../util/linepos.dart';
import '../util/lprange.dart';
import '../util/util.dart';

// const String inputFile = 'day18/example.txt';
const String inputFile = 'day18/input.txt';

Future<void> main(List<String> args) async {
  var input = await readInputAsString(inputFile);

  Stopwatch swP1 = Stopwatch();
  swP1.start();
  print('Part 1:');
  final resultP1 = calcResultP1(input);
  print(resultP1);
  print('${swP1.elapsedMilliseconds} ms');

  Stopwatch swP2 = Stopwatch();
  swP2.start();
  print('Part 2:');
  final resultP2 = calcResultP2(input);
  print(resultP2);
  print('${swP2.elapsedMilliseconds} ms');
}

int calcResultP1(String input) {
  final lines = input.split('\n');
  Board board = Board(lines);
  // board.printBoard();

  int lavaVolume = board.getLavaVolumeWithShoelaceFormula();
  return lavaVolume;
}

int calcResultP2(String input) {
  final lines = input.split('\n');
  Board board = Board(lines, part2: true);
  // board.printBoard();

  int lavaVolume = board.getLavaVolumeWithShoelaceFormula();
  return lavaVolume;
}

class Board {
  List<Line> lines = [];
  LPRange range = LPRange();

  Board(List<String> inputLines, {bool part2 = false}) {
    Map<String, String> dirs = {
      '0': 'R',
      '1': 'D',
      '2': 'L',
      '3': 'U',
    };
    LinePos pos = LinePos(0, 0);
    range.extend(pos);
    for (final inputLine in inputLines) {
      int l;
      String dirStr;
      if (part2) {
        String hex = inputLine.split(' (#')[1];
        String lengthInHex = hex.substring(0, 5);
        String dirVal = hex.substring(5, 6);
        l = int.parse(lengthInHex, radix: 16);
        dirStr = dirs[dirVal]!;
      } else {
        dirStr = inputLine.split(' ')[0];
        l = int.parse(inputLine.split(' ')[1]);
      }
      LinePos end = pos.moveDist(l, dirStr);
      lines.add(Line(pos, end));
      pos = end;
      range.extend(end);
    }
    // Add an empty border around polygon
    range.extend(LinePos(range.colMin - 1, range.rowMin - 1));
    range.extend(LinePos(range.colMax + 1, range.rowMax + 1));
  }

  int getLavaVolume() {
    // Count points outside polygon. Start at one corner
    int outsideCount =
        countPointsOutsidePolygon(LinePos(range.colMin, range.rowMin));

    return range.getArea() - outsideCount;
  }

  int getLavaVolumeWithShoelaceFormula() {
    double area = 0;
    int lineLength = 0;
    for (final line in lines) {
      area +=
          (line.start.row + line.end.row) * (line.start.col - line.end.col) / 2;
      lineLength += line.getLength();
    }
    area += lineLength / 2 + 1; // Add the width of the trench on one side
    return area.toInt();
  }

  List<String> getBoardLines() {
    List<String> boardLines = [];
    for (int row = range.rowMin; row <= range.rowMax; row++) {
      String boardLine = '';

      for (int col = range.colMin; col <= range.colMax; col++) {
        String ch = '.';
        for (final line in lines) {
          if (line.touches(LinePos(col, row))) {
            ch = '#';
            // break;
          }
        }
        boardLine += ch;
      }
      boardLines.add(boardLine);
    }
    return boardLines;
  }

  void printBoard() {
    for (final lineToPrint in getBoardLines()) {
      print(lineToPrint);
    }
    print('');
  }

  int countPointsOutsidePolygon(LinePos startPos) {
    List<LinePos> pointsToCount = [];
    Set<LinePos> counted = {};

    pointsToCount.add(startPos);
    int count = 0;
    while (pointsToCount.isNotEmpty) {
      final point = pointsToCount.removeAt(0);
      bool isOnLine = false;
      for (final line in lines) {
        if (line.touches(point)) {
          isOnLine = true;
          break;
        }
      }
      if (isOnLine) continue;
      if (counted.contains(point)) continue;
      counted.add(point);
      count++;
      for (final neighbour in point.getNeighbours()) {
        if (range.contains(neighbour)) pointsToCount.add(neighbour);
      }
    }
    return count;
  }
}

class Line {
  LinePos start;
  LinePos end;
  Line(this.start, this.end);

  bool touches(LinePos pos) {
    if (start.col == end.col) {
      // Vertical line
      if (pos.col != start.col) return false;
      if (pos.row <= max(start.row, end.row) &&
          pos.row >= min(start.row, end.row)) return true;
    } else {
      // Horizontal line
      if (pos.row != start.row) return false;
      if (pos.col <= max(start.col, end.col) &&
          pos.col >= min(start.col, end.col)) return true;
    }
    return false;
  }

  int getLength() {
    if (start.col == end.col) {
      // Vertical line
      return (start.row - end.row).abs();
    } else {
      return (start.col - end.col).abs();
    }
  }
}
