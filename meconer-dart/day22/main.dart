import 'dart:math';

import '../util/pos.dart';
import '../util/range.dart';
import '../util/util.dart';

// const String inputFile = 'day22/example.txt';
const String inputFile = 'day22/input.txt';

Future<void> main(List<String> args) async {
  var input = await readInputAsString(inputFile);

  Stopwatch swP1 = Stopwatch();
  swP1.start();
  print('Part 1:');
  final resultP1 = calcResultP1(input);
  print(resultP1);
  print('${swP1.elapsedMilliseconds} ms');

  // Stopwatch swP2 = Stopwatch();
  // swP2.start();
  // print('Part 2:');
  // final resultP2 = calcResultP2(input);
  // print(resultP2);
  // print('${swP2.elapsedMilliseconds} ms');
}

int calcResultP1(String input) {
  final lines = input.split('\n');
  Space space = Space(lines);
  space.dropCubes();
  space.calculateSupport();
  int result = space.countDisintigratableBricks();
  return result;
}

class Space {
  List<Cube> cubes = [];
  Range range = Range();
  Space(List<String> lines) {
    for (final line in lines) {
      // Add all the cubes
      cubes.add(Cube(line));
    }
    // Then find out the range in x,y
    for (final cube in cubes) {
      range.extend(Pos(cube.x1, cube.y1));
      range.extend(Pos(cube.x2, cube.y2));
    }
  }

  void dropCubes() {
    // Sort cubes by z1. z1 is less than or equal to z2
    cubes.sort(((a, b) => a.z1.compareTo(b.z1)));
    Map<Pos, int> floorLevel = {};
    for (int x = range.xMin; x <= range.xMax; x++) {
      for (int y = range.yMin; y <= range.yMax; y++) {
        floorLevel[Pos(x, y)] = 1;
      }
    }
    for (final cube in cubes) {
      int zHeight = cube.z2 - cube.z1 + 1;
      int highestLevelUnderCube = 0;
      for (int x = cube.x1; x <= cube.x2; x++) {
        for (int y = cube.y1; y <= cube.y2; y++) {
          highestLevelUnderCube =
              max(highestLevelUnderCube, floorLevel[Pos(x, y)]!);
        }
      }
      cube.z1 = highestLevelUnderCube;
      cube.z2 = highestLevelUnderCube + zHeight - 1;
      for (int x = cube.x1; x <= cube.x2; x++) {
        for (int y = cube.y1; y <= cube.y2; y++) {
          floorLevel[Pos(x, y)] = cube.z2 + 1;
        }
      }
    }
    // printCubes();
  }

  void printCubes() {
    for (int z = 0; z < 9; z++) {
      print('Layer $z');
      for (int x = range.xMin; x <= range.xMax; x++) {
        String printLine = '';
        for (int y = range.yMin; y <= range.yMax; y++) {
          String charToPrint = '.';
          for (final cube in cubes) {
            if (cube.isOnPos(x, y, z)) {
              assert(charToPrint == '.');
              charToPrint = cube.name;
            }
          }
          printLine += charToPrint;
        }
        print(printLine);
      }
      print('');
    }
  }

  void calculateSupport() {
    // Go through each cube
    for (final cube in cubes) {
      // Check which cube is under
      int z = cube.z1 - 1;
      for (int x = cube.x1; x <= cube.x2; x++) {
        for (int y = cube.y1; y <= cube.y2; y++) {
          for (final maybeSupportingCube in cubes) {
            if (maybeSupportingCube.isOnPos(x, y, z)) {
              maybeSupportingCube.isSupporting.add(cube);
              cube.isSupportedBy.add(maybeSupportingCube);
            }
          }
        }
      }
    }
  }

  int countDisintigratableBricks() {
    // A brick is disintigratable if it supports no bricks or
    // if a brick it is supporting has another supporting brick
    int count = 0;
    for (final cube in cubes) {
      if (cube.isSupporting.isEmpty) {
        count++;
        continue;
      }
      bool disintigratable = true;
      for (final supportedCube in cube.isSupporting) {
        if (supportedCube.isSupportedBy.length == 1) {
          disintigratable = false;
          break;
        }
      }
      if (disintigratable) count++;
    }
    return count;
  }
}

class Cube {
  late int x1, x2, y1, y2, z1, z2;

  late String name;
  static String nextName = 'A';

  Set<Cube> isSupporting = {};
  Set<Cube> isSupportedBy = {};

  Cube(String line) {
    name = nextName;
    nextName = String.fromCharCode(nextName.codeUnitAt(0) + 1);
    final first =
        line.split('~')[0].split(',').map((e) => int.parse(e)).toList();
    final second =
        line.split('~')[1].split(',').map((e) => int.parse(e)).toList();
    x1 = min(first[0], second[0]);
    x2 = max(first[0], second[0]);
    y1 = min(first[1], second[1]);
    y2 = max(first[1], second[1]);
    z1 = min(first[2], second[2]);
    z2 = max(first[2], second[2]);
  }

  bool isOnPos(int xP, int yP, int zP) {
    for (int z = z1; z <= z2; z++) {
      for (int x = x1; x <= x2; x++) {
        for (int y = y1; y <= y2; y++) {
          if (xP == x && yP == y && zP == z) return true;
        }
      }
    }
    return false;
  }
}
