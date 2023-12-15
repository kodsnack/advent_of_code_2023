import '../util/util.dart';

// const String inputFile = 'day15/example.txt';
const String inputFile = 'day15/input.txt';

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
  int sum = 0;
  for (final linePart in input.split(',')) {
    sum += hashAlgo(linePart);
  }

  return sum;
}

int calcResultP2(String input) {
  List<Box> boxes = List.generate(256, (index) => Box());
  for (final linePart in input.split(',')) {
    if (linePart.contains('=')) {
      String label = linePart.split('=')[0];
      int focalLength = int.parse(linePart.split('=')[1]);
      Lens lens = Lens(label, focalLength);
      int boxNo = hashAlgo(label);
      int indexOfLensWithSameLabel =
          boxes[boxNo].lenses.indexWhere((lens) => lens.label == label);
      if (indexOfLensWithSameLabel < 0) {
        boxes[boxNo].lenses.add(lens);
      } else {
        boxes[boxNo].lenses[indexOfLensWithSameLabel] = lens;
      }
    } else {
      // operation must have a - at the end
      assert(linePart.endsWith('-'));
      String label = linePart.substring(0, linePart.length - 1);
      int boxNo = hashAlgo(label);
      int indexOfLensWithSameLabel =
          boxes[boxNo].lenses.indexWhere((lens) => lens.label == label);
      if (indexOfLensWithSameLabel >= 0) {
        boxes[boxNo].lenses.removeAt(indexOfLensWithSameLabel);
      }
    }
  }

  int sum = 0;
  for (int boxIdx = 0; boxIdx < 256; boxIdx++) {
    final box = boxes[boxIdx];
    for (int lensIdx = 0; lensIdx < box.lenses.length; lensIdx++) {
      sum += (boxIdx + 1) * (lensIdx + 1) * box.lenses[lensIdx].focalLength;
    }
  }
  return sum;
}

class Box {
  List<Lens> lenses = [];
}

class Lens {
  String label;
  int focalLength;
  Lens(this.label, this.focalLength);
}

int hashAlgo(String s) {
  int currVal = 0;
  for (final asciiCode in s.split('').map((e) => e.codeUnitAt(0))) {
    currVal += asciiCode;
    currVal *= 17;
    currVal %= 256;
  }
  return currVal;
}
