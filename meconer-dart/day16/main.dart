import 'dart:math';

import '../util/linepos.dart';
import '../util/lprange.dart';
import '../util/util.dart';

// const String inputFile = 'day16/example.txt';
const String inputFile = 'day16/input.txt';

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

  Cave cave = Cave(lines);
  cave.calcBeamPath(LinePos(0, 0), 'R', {});
  // cave.printEnergized();
  return cave.countEnergized();
}

int calcResultP2(String input) {
  final lines = input.split('\n');

  Cave cave = Cave(lines);
  int maxCount = 0;
  for (int col = 0; col < cave.grid.length; col++) {
    cave.calcBeamPath(LinePos(col, 0), 'D', {});
    maxCount = max(maxCount, cave.countEnergized());
    cave.resetEnergized();
    cave.calcBeamPath(LinePos(col, cave.grid.length - 1), 'U', {});
    maxCount = max(maxCount, cave.countEnergized());
    cave.resetEnergized();
  }
  for (int row = 0; row < cave.grid[0].length; row++) {
    cave.calcBeamPath(LinePos(0, row), 'R', {});
    maxCount = max(maxCount, cave.countEnergized());
    cave.resetEnergized();
    cave.calcBeamPath(LinePos(cave.grid[0].length - 1, row), 'L', {});
    maxCount = max(maxCount, cave.countEnergized());
    cave.resetEnergized();
  }
  return maxCount;
}

class Cave {
  List<List<Tile>> grid = [];
  LPRange range = LPRange();

  Cave(List<String> lines) {
    for (final line in lines) {
      grid.add(line.split('').map((e) => Tile(e)).toList());
    }
    range.extend(LinePos(0, 0));
    range.extend(LinePos(lines[0].length - 1, lines.length - 1));
  }

  void calcBeamPath(
      LinePos pos, String direction, Set<(LinePos, String)> seen) {
    if (!range.contains(pos)) return;
    if (seen.contains((pos, direction))) return;

    seen.add((pos, direction));
    final tile = grid[pos.row][pos.col];
    tile.isEnergized = true;

    List<String> nextDirections = getNextMoves(direction, tile.tileChar);
    for (final direction in nextDirections) {
      calcBeamPath(pos.moveDirStr(direction), direction, seen);
    }
  }

  List<String> getNextMoves(String direction, String tileChar) {
    const Map<(String, String), List<String>> nextMoves = {
      ('R', '.'): ['R'],
      ('R', '-'): ['R'],
      ('R', '/'): ['U'],
      ('R', r'\'): ['D'],
      ('R', '|'): ['U', 'D'],
      ('D', '.'): ['D'],
      ('D', '-'): ['L', 'R'],
      ('D', '/'): ['L'],
      ('D', r'\'): ['R'],
      ('D', '|'): ['D'],
      ('L', '.'): ['L'],
      ('L', '-'): ['L'],
      ('L', '/'): ['D'],
      ('L', r'\'): ['U'],
      ('L', '|'): ['U', 'D'],
      ('U', '.'): ['U'],
      ('U', '-'): ['L', 'R'],
      ('U', '/'): ['R'],
      ('U', r'\'): ['L'],
      ('U', '|'): ['U'],
    };
    return nextMoves[(direction, tileChar)]!;
  }

  void printEnergized() {
    for (var row = 0; row < grid.length; row++) {
      String line = '';
      for (var col = 0; col < grid[0].length; col++) {
        line += grid[row][col].isEnergized ? '#' : '.';
      }
      print(line);
    }
    print('');
  }

  int countEnergized() {
    int count = 0;
    for (var row = 0; row < grid.length; row++) {
      for (var col = 0; col < grid[0].length; col++) {
        count += grid[row][col].isEnergized ? 1 : 0;
      }
    }
    return count;
  }

  void resetEnergized() {
    for (var row = 0; row < grid.length; row++) {
      for (var col = 0; col < grid[0].length; col++) {
        grid[row][col].isEnergized = false;
      }
    }
  }
}

class Tile {
  String tileChar;
  bool isEnergized = false;
  Tile(this.tileChar);
}
