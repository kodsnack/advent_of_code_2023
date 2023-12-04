import 'dart:math';

import '../util/linepos.dart';
import '../util/util.dart';

// const String inputFile = 'day3/example.txt';
const String inputFile = 'day3/input.txt';

Future<void> main(List<String> args) async {
  var input = await readInputAsString(inputFile);

  print('Part 1:');
  final resultP1 = calcResultP1(input);
  print(resultP1);

  print('Part 2:');
  final resultP2 = calcResultP2(input);
  print(resultP2);
}

class MaybePartNumber {
  LinePos start;
  int len;
  int number;
  bool isPartNumber = false;
  MaybePartNumber(this.start, this.len, this.number);
}

class Symbol {
  LinePos pos;
  String sym;
  List<int> neighbourNumbers = [];
  Symbol(this.pos, this.sym);
}

calcResultP1(String input) {
  int lineNo = 0;
  List<MaybePartNumber> numberPositions = [];
  List<LinePos> symbolPositions = [];

  final numberRegex = RegExp(r'\d+');
  final symbolRegex = RegExp(r'[^\d\.]');

  final lines = input.split('\n');

  int width = lines[0].length;
  int height = lines.length;

  for (final line in lines) {
    final numberMatches = numberRegex.allMatches(line);
    numberMatches.forEach((element) {
      int start = element.start;
      int len = element.end - start;
      numberPositions.add(MaybePartNumber(
          LinePos(start, lineNo), len, int.parse(element.group(0)!)));
    });

    final symbolMatches = symbolRegex.allMatches(line);
    symbolMatches.forEach((element) {
      symbolPositions.add(LinePos(element.start, lineNo));
    });
    lineNo++;
  }

  int sum = 0;

  for (final numPos in numberPositions) {
    // Get the adjacent positions
    final neighbours = getNeighbours(numPos, width, height);
    // If any neigbour has a symbol
    if (symbolPositions.any((element) => neighbours.contains(element))) {
      sum += numPos.number;
    }
  }
  return sum;
}

calcResultP2(String input) {
  int lineNo = 0;
  List<MaybePartNumber> numbers = [];
  List<Symbol> symbols = [];

  final numberRegex = RegExp(r'\d+');
  final symbolRegex = RegExp(r'[^\d\.]');

  final lines = input.split('\n');

  int width = lines[0].length;
  int height = lines.length;

  for (final line in lines) {
    final numberMatches = numberRegex.allMatches(line);
    numberMatches.forEach((element) {
      int start = element.start;
      int len = element.end - start;
      numbers.add(MaybePartNumber(
          LinePos(start, lineNo), len, int.parse(element.group(0)!)));
    });

    final symbolMatches = symbolRegex.allMatches(line);
    symbolMatches.forEach((element) {
      symbols.add(Symbol(LinePos(element.start, lineNo), element.group(0)!));
    });
    lineNo++;
  }

  for (final numPos in numbers) {
    // Get the adjacent positions
    final neighbours = getNeighbours(numPos, width, height);
    // If any neighbour has a symbol, add the number to the symbols neighbour
    // number list.
    for (final neighbour in neighbours) {
      for (final symbol in symbols) {
        if (neighbour == symbol.pos) {
          symbol.neighbourNumbers.add(numPos.number);
        }
      }
    }
  }

  int sum = 0;
  // Check all '*' symbols that has exactly two neighbouring numbers
  for (final symbol in symbols) {
    if (symbol.sym == '*' && symbol.neighbourNumbers.length == 2) {
      sum += symbol.neighbourNumbers[0] * symbol.neighbourNumbers[1];
    }
  }

  return sum;
}

List<LinePos> getNeighbours(MaybePartNumber numPos, int width, int height) {
  List<LinePos> neighbours = [];
  // Adjacent to the left
  int startCol = numPos.start.col;
  int startRow = numPos.start.row;
  if (startCol > 0) neighbours.add(LinePos(startCol - 1, startRow));

  // Adjacent to the right
  int endCol = startCol + numPos.len - 1;
  if (endCol < width - 1) neighbours.add(LinePos(endCol + 1, startRow));

  // The row above
  if (startRow > 0) {
    for (int col = max(0, startCol - 1); col <= min(width, endCol + 1); col++) {
      neighbours.add(LinePos(col, startRow - 1));
    }
  }

  // The row below
  if (startRow < height) {
    for (int col = max(0, startCol - 1); col <= min(width, endCol + 1); col++) {
      neighbours.add(LinePos(col, startRow + 1));
    }
  }
  return neighbours;
}
