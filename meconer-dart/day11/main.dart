import 'dart:math';

import '../util/linepos.dart';
import '../util/util.dart';

// const String inputFile = 'day11/example.txt';
const String inputFile = 'day11/input.txt';

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

  Grid grid = Grid(lines);
  return grid.solveP1();
}

int calcResultP2(String input) {
  final lines = input.split('\n');

  Grid grid = Grid(lines);
  return grid.solveP2(1000000);
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
  }

  int solveP1() {
    List<LinePos> galaxies = findGalaxies();
    List<int> emptyColumns = findEmptyColumns();
    List<int> emptyRows = findEmptyRows();
    int totalDist = 0;
    for (int idx1 = 0; idx1 < galaxies.length - 1; idx1++) {
      for (int idx2 = idx1 + 1; idx2 < galaxies.length; idx2++) {
        final pos1 = galaxies[idx1];
        final pos2 = galaxies[idx2];
        int maxCol = max(pos1.col, pos2.col);
        int minCol = min(pos1.col, pos2.col);
        int xDist = maxCol -
            minCol +
            emptyColumns.where((col) => col > minCol && col < maxCol).length;

        int maxRow = max(pos1.row, pos2.row);
        int minRow = min(pos1.row, pos2.row);
        int yDist = maxRow -
            minRow +
            emptyRows.where((row) => row > minRow && row < maxRow).length;
        totalDist += xDist + yDist;
      }
    }
    return totalDist;
  }

  int solveP2(int expansionFactor) {
    List<LinePos> galaxies = findGalaxies();
    List<int> emptyColumns = findEmptyColumns();
    List<int> emptyRows = findEmptyRows();
    int totalDist = 0;
    for (int idx1 = 0; idx1 < galaxies.length - 1; idx1++) {
      for (int idx2 = idx1 + 1; idx2 < galaxies.length; idx2++) {
        final pos1 = galaxies[idx1];
        final pos2 = galaxies[idx2];

        int maxCol = max(pos1.col, pos2.col);
        int minCol = min(pos1.col, pos2.col);
        int noOfEmptyCols =
            emptyColumns.where((col) => col > minCol && col < maxCol).length;
        int expandedCols = expansionFactor * noOfEmptyCols - noOfEmptyCols;

        int xDist = maxCol - minCol + expandedCols;

        int maxRow = max(pos1.row, pos2.row);
        int minRow = min(pos1.row, pos2.row);

        int noOfEmptyRows =
            emptyRows.where((row) => row > minRow && row < maxRow).length;
        int expandedRows = expansionFactor * noOfEmptyRows - noOfEmptyRows;
        int yDist = maxRow - minRow + expandedRows;
        totalDist += xDist + yDist;
      }
    }
    return totalDist;
  }

  List<LinePos> findGalaxies() {
    List<LinePos> galaxies = [];
    for (int row = 0; row < height; row++) {
      for (int col = 0; col < width; col++) {
        if (grid[LinePos(col, row)] == '#') {
          galaxies.add(LinePos(col, row));
        }
      }
    }
    return galaxies;
  }

  List<int> findEmptyColumns() {
    List<int> emptyColumns = [];
    for (int col = 0; col < width; col++) {
      bool foundGalaxy = false;
      for (int row = 0; row < height; row++) {
        if (grid[LinePos(col, row)] == '#') {
          foundGalaxy = true;
        }
      }
      if (!foundGalaxy) emptyColumns.add(col);
    }
    return emptyColumns;
  }

  List<int> findEmptyRows() {
    List<int> emptyRows = [];
    for (int row = 0; row < height; row++) {
      bool foundGalaxy = false;
      for (int col = 0; col < width; col++) {
        if (grid[LinePos(col, row)] == '#') {
          foundGalaxy = true;
        }
      }
      if (!foundGalaxy) emptyRows.add(row);
    }
    return emptyRows;
  }
}
