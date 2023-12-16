import '../util/util.dart';

// const String inputFile = 'day14/example.txt';
const String inputFile = 'day14/input.txt';

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
  List<List<String>> grid = [];

  for (final line in lines) {
    grid.add(line.split(''));
  }

  rollNorth(grid);
  int result = calculateValue(grid);

  return result;
}

// 100492 too low
// 100531 correct. Checked the value at 961 instead of 960.
// I ran the rotating 1000 times. Analyzing data shows that my cycle
// length is 39.
// 999 999 999 - 960 is divisible by 39 so we should have the same
// load at 1000 000 000 as we have at cycle 961 and since the first
// cycle no is 0 we find it at cycleNo 960
int calcResultP2(String input) {
  final lines = input.split('\n');
  List<List<String>> grid = [];

  for (final line in lines) {
    grid.add(line.split(''));
  }

  // printGrid(grid);

  int noOfCycles = 1000;
  Map<String, List<int>> existing = {};
  for (var rollCycleNo = 0; rollCycleNo < noOfCycles; rollCycleNo++) {
    rollNorth(grid);
    rollWest(grid);
    rollSouth(grid);
    rollEast(grid);
    // printGrid(grid);
    String hash = getHash(grid);
    if (existing.containsKey(hash)) {
      existing[hash]!.add(rollCycleNo);
      if (existing[hash]!.length > 1) {
        int cycleLength = existing[hash]![1] - existing[hash]![0];
        if ((999999999 - rollCycleNo) % cycleLength == 0) break;
      }
    } else {
      existing[hash] = [rollCycleNo];
    }
  }

  int result = calculateValue(grid);
  return result;
}

String getHash(List<List<String>> grid) {
  String hash = '';
  for (int i = 0; i < grid.length; i++) {
    hash += grid[i].join();
  }
  return hash;
}

void printGrid(List<List<String>> grid) {
  for (int row = 0; row < grid.length; row++) {
    String line = '';
    for (int col = 0; col < grid.length; col++) {
      line += grid[row][col];
    }
    print(line);
  }
  print('');
}

int calculateValue(List<List<String>> grid) {
  int value = 0;
  for (int row = 0; row < grid.length; row++) {
    int lineNo = grid.length - row;
    for (int col = 0; col < grid.length; col++) {
      if (grid[row][col] == 'O') value += lineNo;
    }
  }
  return value;
}

void rollNorth(List<List<String>> grid) {
  for (int col = 0; col < grid[0].length; col++) {
    List<String> column =
        List.generate(grid.length, (index) => grid[index][col]);
    column = rollLeft(column);

    for (int row = 0; row < column.length; row++) {
      grid[row][col] = column[row];
    }
  }
}

void rollSouth(List<List<String>> grid) {
  for (int col = 0; col < grid[0].length; col++) {
    List<String> column = List.generate(
        grid.length, (index) => grid[grid.length - index - 1][col]);
    column = rollLeft(column);

    for (int row = 0; row < column.length; row++) {
      grid[row][col] = column[column.length - row - 1];
    }
  }
}

void rollEast(List<List<String>> grid) {
  for (int row = 0; row < grid.length; row++) {
    List<String> column = List.generate(
        grid.length, (index) => grid[row][grid.length - index - 1]);
    column = rollLeft(column);

    for (int col = 0; col < column.length; col++) {
      grid[row][col] = column[column.length - col - 1];
    }
  }
}

void rollWest(List<List<String>> grid) {
  for (int row = 0; row < grid.length; row++) {
    List<String> column =
        List.generate(grid.length, (index) => grid[row][index]);
    column = rollLeft(column);

    for (int col = 0; col < column.length; col++) {
      grid[row][col] = column[col];
    }
  }
}

List<String> rollLeft(List<String> column) {
  int limit = 0;
  while (limit < column.length) {
    if (column[limit] == '.') {
      // Empty space. Find next rock
      int idxOfRock = column.indexWhere((element) => element != '.', limit);
      if (idxOfRock < 0) {
        break; // No rocks found. We are ready
      }
      if (column[idxOfRock] == '#') {
        // Cube shape rock which cannot move. Set limit to next pos
        limit = idxOfRock + 1;
      } else {
        // Round rock. Should move
        column[idxOfRock] = '.';
        column[limit] = 'O';
      }
    } else {
      limit++;
    }
  }
  return column;
}
