import '../util/linepos.dart';
import '../util/util.dart';

// const String inputFile = 'day21/example.txt';
const String inputFile = 'day21/input.txt';

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
  board.printBoard();
  const int noOfSteps = 64;
  for (int step = 0; step < noOfSteps; step++) {
    board.doStep();
  }
  board.printBoard();
  return board.elfPos.length;
}

/* 
 Boards 
                    ---------  
                     | 25  |
               -------------------- 
            9  |  10 | 11  | 12  | 13
          -----------------------------
         |  24 |  1  |  2  |  3  | 14 |
    -----|----------------------------------
    | 28 |  23 |  8  |  0  |  4  | 15 | 26 |
      ---|----------------------------------
         |  22 |  7  |  6  |  5  | 16 |
          -----------------------------
            21 |  20 | 19  | 18  | 17
               -------------------
                     | 27  |
                     -------


*/

int calcResultP2(String input) {
  final lines = input.split('\n');

  // Find out the sequence in which the different kinds of boards fills

  Map<int, List<int>> boardFillSequences = {};
  for (int boardNo = 0; boardNo <= 32; boardNo++) {
    boardFillSequences[boardNo] = [];
  }
  Board board = Board(lines);
  int step = 0;
  int n = 2;
  int noOfSteps = 65 + n * 131;
  while (step < noOfSteps) {
    // Continue until the outer diagonal boards are filled.
    // break;
    step++;
    board.doStep();
    // print(step);
    for (int boardNo = 0; boardNo <= 32; boardNo++) {
      int noOfElfsInBoard = board.countElfsInBaseBoard(boardNo);
      boardFillSequences[boardNo]!.add(noOfElfsInBoard);
    }
  }
  int totalElfs = board.countElfsInBoard(extend: 6);

  print('After $step steps. Board has $totalElfs reachable plots ');

  // Analyzing data collected above shows that the boards starts to fill in
  // the following order:

  // Board 0 ( The center starting board) fills in 129 steps and reaches all
  // edges in 65 steps. After filled it is 7325 elfs on EVEN steps and 7265
  // on odd steps

  // Boards  2,4,6 and 8 gets their first elf after 66 steps. Filled after 261
  // steps (195 steps later..?) contains
  // 7325 elfs on ODD steps and 7265 on even.
  print('Boards 2,4,6 and 8 gets their first elf after 66 steps');
  for (int i in [2, 4, 6, 8]) {
    int first = boardFillSequences[i]!.indexWhere((element) => element > 0);
    print('Board $i gets first elf after ${first + 1} steps');
  }

  // Boards 1,3,5 and 7 gets their first elf after 132 steps. Filled contains
  // 7325 elfs on EVEN steps and 7265 on odd
  print('Boards 1,3,5 and 7 gets their first elf after 132 steps.');
  for (int i in [1, 3, 5, 7]) {
    int first = boardFillSequences[i]!.indexWhere((element) => element > 0);
    print('Board $i gets first elf after ${first + 1} steps');
  }

  // Boards 11,15,19 and 23 gets their first elf after 197 steps.
  // 65 steps after 1,3,5 and 7 or 131 steps after 2,4,6 and 8. Filled contains
  // 7325 elfs on EVEN steps and 7265 on odd
  print(
      'Boards 11,15,19 and 23 gets their first elf after 197 steps. (65 steps after 1,3,5 and 7)');
  for (int i in [11, 15, 19, 23]) {
    int first = boardFillSequences[i]!.indexWhere((element) => element > 0);
    print('Board $i gets first elf after ${first + 1} steps');
  }

  // Boards 10,12,14,16,18,20,22 and 24 gets their first elf after 263 steps.
  // 65 steps after 1,3,5 and 7 or 131 steps after 2, 4, 6 and 8. Filled contains
  // 7325 elfs on ODD steps and 7265 on even
  print(
      'Boards 10,12,14,16,18,20,22 and 24 gets their first elf after 263 steps.');
  print('131 steps after 1,3,5 and 7)');
  for (int i in [10, 12, 14, 16, 18, 20, 22, 24]) {
    int first = boardFillSequences[i]!.indexWhere((element) => element > 0);
    print('Board $i gets first elf after ${first + 1} steps');
  }

  // Boards 25-28  gets their first elf after 328 steps.
  // 131 steps after 11, 15, 19 and 23. Filled after 523 steps and contains
  // 7325 elfs on ODD steps and 7265 on even
  print(
      'Boards 10,12,14,16,18,20,22 and 24 gets their first elf after 263 steps.');
  print('131 steps after 1,3,5 and 7)');
  for (int i in [10, 12, 14, 16, 18, 20, 22, 24]) {
    int first = boardFillSequences[i]!.indexWhere((element) => element > 0);
    print('Board $i gets first elf after ${first + 1} steps');
  }
  // Seems that we have a diamond fill pattern with two kinds of boards. One
  // kind (type A) has 7325 elfs on odd steps and another (type B) with 7265
  // elfs on even steps. Since the total no of steps is odd, those are the
  // most interesting numbers
  int totalSteps = 26501365;

  int typeAFilled = boardFillSequences[4]!.last;
  int typeBFilled = boardFillSequences[0]!.last;

  // No of tiles that has been reached after totalsteps except for tile 0:
  int reachedHorizontalTiles = (totalSteps - 65) ~/ 131;

  // No of A filled horisontally

  int noOfBHorizontal = (reachedHorizontalTiles - 1) ~/ 2;
  int noOfAHorizontal = reachedHorizontalTiles - 1 - noOfBHorizontal;

  int noOfFilledTilesInQuarter =
      (reachedHorizontalTiles - 1) * reachedHorizontalTiles ~/ 2;

  int noOfSmallDiagonalTiles = reachedHorizontalTiles;
  int noOfLargeDiagonalTiles = reachedHorizontalTiles - 1;

  int noOfTypeATiles = noOfAHorizontal * noOfAHorizontal;
  int noOfTypeBTiles = noOfFilledTilesInQuarter - noOfTypeATiles;

  int noOfElfsInFilledTiles =
      4 * (noOfTypeATiles * typeAFilled + noOfTypeBTiles * typeBFilled);

  int noOfElfsInDiamondTipTiles = boardFillSequences[15]!.last +
      boardFillSequences[11]!.last +
      boardFillSequences[23]!.last +
      boardFillSequences[19]!.last;

  int noOfElfsInLargeDiagonalEdgeTiles = noOfLargeDiagonalTiles *
      (boardFillSequences[3]!.last +
          boardFillSequences[1]!.last +
          boardFillSequences[5]!.last +
          boardFillSequences[7]!.last);

  int noOfElfsInSmallDiagonalEdgeTiles = noOfSmallDiagonalTiles *
      (boardFillSequences[14]!.last +
          boardFillSequences[10]!.last +
          boardFillSequences[20]!.last +
          boardFillSequences[16]!.last);

  int totalElfsByCalculation = typeBFilled + // Center tile
      noOfElfsInFilledTiles + // Elfs in filled tiles. A and B
      noOfElfsInDiamondTipTiles + // Elfs in the tip of the diamond
      noOfElfsInSmallDiagonalEdgeTiles +
      noOfElfsInLargeDiagonalEdgeTiles; // Elfs on the diagonal edges

  // Steps after the last tiles has been reached
  int remainingSteps = totalSteps - reachedHorizontalTiles * 131;
  assert(remainingSteps == 65);

  return totalElfsByCalculation;
}

class Board {
  Set<LinePos> rocks = {};
  Set<LinePos> elfPos = {};
  late LinePos startPos;
  late int width;
  late int height;
  Board(List<String> lines) {
    width = lines[0].length;
    height = lines.length;
    for (int row = 0; row < height; row++) {
      final line = lines[row];
      for (int col = 0; col < width; col++) {
        if (line[col] == '#') rocks.add(LinePos(col, row));
        if (line[col] == 'S') elfPos.add(LinePos(col, row));
      }
    }
  }

  void printBoard({int extend = 0}) {
    for (int row = -extend * width; row < height * (extend + 1); row++) {
      String lineToPrint = '';
      for (int col = -extend * height; col < width * (extend + 1); col++) {
        if (rocks.contains(infPos(col, row))) {
          lineToPrint += '#';
        } else if (elfPos.contains(LinePos(col, row))) {
          lineToPrint += 'O';
        } else {
          lineToPrint += '.';
        }
      }
      print(lineToPrint);
    }
    print('');
  }

  void doStep() {
    Set<LinePos> newElfPos = {};
    for (final pos in elfPos) {
      for (final neighbour in pos.getNeighbours()) {
        if (!rocks.contains(infPos(neighbour.col, neighbour.row)))
          newElfPos.add(neighbour);
      }
    }
    elfPos = newElfPos;
  }

  String getState() {
    String state = '';
    for (int row = 0; row < height; row++) {
      for (int col = 0; col < width; col++) {
        if (rocks.contains(LinePos(col, row))) {
          state += '#';
        } else if (elfPos.contains(LinePos(col, row))) {
          state += 'O';
        } else {
          state += '.';
        }
      }
    }
    return state;
  }

  int countElfsInBoard({int extend = 0}) {
    int count = 0;
    for (int row = -extend * height; row < height * (extend + 1); row++) {
      for (int col = -extend * width; col < width * (extend + 1); col++) {
        if (elfPos.contains(LinePos(col, row))) {
          count++;
        }
      }
    }
    return count;
  }

  LinePos infPos(int col, int row) {
    return LinePos(col % width, row % height);
  }

  int findboardCountAtOddStep(int boardNo) {
    int step = 1;
    int noOfSteps = width * 3;
    assert(noOfSteps % 2 == 1); // Check that it is odd
    while (step < noOfSteps) {
      doStep();
      step++;
    }
    return countElfsInBaseBoard(boardNo);
  }

  int countElfsInBaseBoard(int boardNo) {
    if (boardNo == 0) {
      // Center board
      return countElfsInBoard();
    }

    // Range factors for board no  rmin, rmax, cmin, cmax
    Map<int, List<int>> rangeFactors = {
      1: [-1, 0, -1, 0],
      2: [-1, 0, 0, 1],
      3: [-1, 0, 1, 2],
      4: [0, 1, 1, 2],
      5: [1, 2, 1, 2],
      6: [1, 2, 0, 1],
      7: [1, 2, -1, 0],
      8: [0, 1, -1, 0],
      9: [-2, -1, -2, -1],
      10: [-2, -1, -1, 0],
      11: [-2, -1, 0, 1],
      12: [-2, -1, 1, 2],
      13: [-2, -1, 2, 3],
      14: [-1, 0, 2, 3],
      15: [0, 1, 2, 3],
      16: [1, 2, 2, 3],
      17: [2, 3, 2, 3],
      18: [2, 3, 1, 2],
      19: [2, 3, 0, 1],
      20: [2, 3, -1, 0],
      21: [2, 3, -2, -1],
      22: [1, 2, -2, -1],
      23: [0, 1, -2, -1],
      24: [-1, 0, -2, -1],
      25: [-3, -2, 0, 1],
      26: [0, 1, 3, 4],
      27: [3, 4, 0, 1],
      28: [0, 1, -3, -2],
      29: [0, 1, 4, 5],
      30: [0, 1, 5, 6],
      31: [0, 1, 6, 7],
      32: [0, 1, 7, 8],
    };

    return countElfsInRange(
        height * rangeFactors[boardNo]![0],
        height * rangeFactors[boardNo]![1],
        width * rangeFactors[boardNo]![2],
        width * rangeFactors[boardNo]![3]);
    // if (boardNo == 1) {
    //   // NW board
    //   return countElfsInRange(-height, 0, -width, 0);
    // }
    // if (boardNo == 2) {
    //   //North board
    //   return countElfsInRange(-height, 0, 0, width);
    // }
    // if (boardNo == 3) {
    //   // NE board
    //   return countElfsInRange(-height, 0, width, 2 * width);
    // }
    // if (boardNo == 4) {
    //   // E board
    //   return countElfsInRange(0, height, width, 2 * width);
    // }
    // if (boardNo == 5) {
    //   // SE board
    //   return countElfsInRange(height, 2 * height, width, 2 * width);
    // }
    // if (boardNo == 6) {
    //   // S board
    //   return countElfsInRange(height, 2 * height, 0, width);
    // }
    // if (boardNo == 7) {
    //   // SW board
    //   return countElfsInRange(height, 2 * height, -width, 0);
    // }
    // if (boardNo == 8) {
    //   // W board
    //   return countElfsInRange(0, height, -width, 0);
    // }
    // return 0;
  }

  int countElfsInRange(int rMin, int rMax, int cMin, int cMax) {
    int count = 0;
    for (int row = rMin; row < rMax; row++) {
      for (int col = cMin; col < cMax; col++) {
        if (elfPos.contains(LinePos(col, row))) {
          count++;
        }
      }
    }
    return count;
  }

  // List<int> findFillSequence(int boardNo, int noOfStepsToFillBoard) {
  //   List<int> fillSequence = [];
  //   for (int step = 0; step < startStep; step++) {
  //     doStep();
  //   }
  //   fillSequence.add(countElfsInBaseBoard(boardNo));
  //   for (int step = startStep;
  //       step <= startStep + noOfStepsToFillBoard;
  //       step++) {
  //     doStep();
  //     fillSequence.add(countElfsInBaseBoard(boardNo));
  //   }
  //   return fillSequence;
  // }

  int findStepsUntilBoardGetsFirstElf(int boardNo) {
    int step = 1;
    doStep();
    while (countElfsInBaseBoard(boardNo) == 0) {
      print(step);
      printBoard();
      doStep();
      step++;
    }
    return step;
  }
}
