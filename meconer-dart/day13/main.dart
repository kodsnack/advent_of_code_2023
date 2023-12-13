import '../util/util.dart';

// const String inputFile = 'day13/example.txt';
const String inputFile = 'day13/input.txt';

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
  int sum = 0;
  List<String> gridLines = [];

  for (final line in lines) {
    if (line.isEmpty) {
      sum += getValueForGrid(gridLines);
      gridLines = [];
    } else {
      gridLines.add(line);
    }
  }

  sum += getValueForGrid(gridLines);
  return sum;
}

int calcResultP2(String input) {
  final lines = input.split('\n');
  int sum = 0;
  List<String> gridLines = [];

  for (final line in lines) {
    if (line.isEmpty) {
      sum += getValueForGridP2(gridLines);
      gridLines = [];
    } else {
      gridLines.add(line);
    }
  }

  sum += getValueForGridP2(gridLines);
  return sum;
}

int getValueForGrid(List<String> gridLines) {
  List<String> cols, rows;
  (rows, cols) = linesToGrid(gridLines);
  int rowsAboveHorizontalReflection = findReflection(rows);
  int colsToLeftOfVertical = findReflection(cols);
  return colsToLeftOfVertical + 100 * rowsAboveHorizontalReflection;
}

int getValueForGridP2(List<String> gridLines) {
  List<String> cols, rows;
  (rows, cols) = linesToGrid(gridLines);
  int rowsAboveHorizontalReflection = findReflection(rows, wantedSmudge: 1);

  int colsToLeftOfVertical = findReflection(cols, wantedSmudge: 1);
  return colsToLeftOfVertical + 100 * rowsAboveHorizontalReflection;
}

int getDiff(String s1, String s2) {
  assert(s1.length == s2.length);
  int count = 0;
  for (int idx = 0; idx < s1.length; idx++) {
    if (s1[idx] != s2[idx]) count++;
  }
  return count;
}

int findReflection(List<String> rows, {int wantedSmudge = 0}) {
  int reflectionRow = 1;

  while (reflectionRow < rows.length) {
    bool foundReflection = true;
    int rowAbove = reflectionRow - 1;
    int rowBelow = reflectionRow;
    int smudgeCount = 0;

    while (rowAbove >= 0 && rowBelow < rows.length) {
      int diffCount = getDiff(rows[rowAbove], rows[rowBelow]);
      if (diffCount + smudgeCount > wantedSmudge) {
        foundReflection = false;
        break;
      }
      smudgeCount += diffCount;
      rowAbove--;
      rowBelow++;
    }
    if (foundReflection && smudgeCount == wantedSmudge) return reflectionRow;
    reflectionRow++;
  }
  return 0;
}

(List<String>, List<String>) linesToGrid(List<String> gridLines) {
  List<String> rows = [...gridLines];
  List<String> cols = List.generate(rows[0].length, (_) => '');
  for (int colIdx = 0; colIdx < rows[0].length; colIdx++) {
    for (int rowIdx = 0; rowIdx < rows.length; rowIdx++) {
      cols[colIdx] += rows[rowIdx][colIdx];
    }
  }
  return (rows, cols);
}
