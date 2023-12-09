import '../util/util.dart';

// const String inputFile = 'day9/example.txt';
const String inputFile = 'day9/input.txt';

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

  int result = 0;
  for (final line in lines) {
    result += getResultFromLine(line);
  }

  return result;
}

int calcResultP2(String input) {
  final lines = input.split('\n');

  int result = 0;
  for (final line in lines) {
    result += getResultFromLineP2(line);
  }

  return result;
}

int getResultFromLine(String line) {
  List<List<int>> numbers = [];
  numbers.add(line.split(' ').map((e) => int.parse(e)).toList());
  int diffCount = 1;
  while (numbers[diffCount - 1].any((element) => element != 0)) {
    numbers.add([]);
    for (int idx = 0; idx < numbers[diffCount - 1].length - 1; idx++) {
      numbers[diffCount]
          .add(numbers[diffCount - 1][idx + 1] - numbers[diffCount - 1][idx]);
    }
    diffCount++;
  }
  int result = 0;
  for (int diffIdx = diffCount - 1; diffIdx >= 0; diffIdx--) {
    result += numbers[diffIdx].last;
  }
  return result;
}

int getResultFromLineP2(String line) {
  List<List<int>> numbers = [];
  numbers.add(line.split(' ').map((e) => int.parse(e)).toList());
  int diffCount = 1;
  while (numbers[diffCount - 1].any((element) => element != 0)) {
    numbers.add([]);
    for (int idx = 0; idx < numbers[diffCount - 1].length - 1; idx++) {
      numbers[diffCount]
          .add(numbers[diffCount - 1][idx + 1] - numbers[diffCount - 1][idx]);
    }
    diffCount++;
  }
  int diff = 0;
  for (int diffIdx = diffCount - 1; diffIdx >= 0; diffIdx--) {
    diff = numbers[diffIdx].first - diff;
  }
  return diff;
}
