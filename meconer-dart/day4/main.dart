import 'dart:math';

import '../util/util.dart';

// const String inputFile = 'day4/example.txt';
const String inputFile = 'day4/input.txt';

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
  int sum = 0;
  final numberRegex = RegExp(r'\d+');
  for (final line in input.split('\n')) {
    final winningNumbers = Set.from(numberRegex
        .allMatches(line.split(':')[1].trim().split('|')[0])
        .map((e) => int.parse(e.group(0)!)));
    final numbers = Set.from(numberRegex
        .allMatches(line.split(':')[1].trim().split('|')[1])
        .map((e) => int.parse(e.group(0)!)));

    final matchingNumbers =
        numbers.where((element) => winningNumbers.contains(element));
    if (matchingNumbers.isNotEmpty) {
      final value = pow(2, matchingNumbers.length - 1);
      sum += value.toInt();
    }
  }
  return sum;
}

int calcResultP2(String input) {
  final numberRegex = RegExp(r'\d+');
  final lines = input.split('\n');
  List<int> counts = List.generate(lines.length + 1, (_) => 1);
  counts[0] = 0;

  for (int cardNo = 1; cardNo < counts.length; cardNo++) {
    final line = lines[cardNo - 1];

    final winningNumbers = Set.from(numberRegex
        .allMatches(line.split(':')[1].trim().split('|')[0])
        .map((e) => int.parse(e.group(0)!)));

    final numbers = Set.from(numberRegex
        .allMatches(line.split(':')[1].trim().split('|')[1])
        .map((e) => int.parse(e.group(0)!)));

    final matchingNumbers =
        numbers.where((element) => winningNumbers.contains(element));
    for (int i = 0; i < matchingNumbers.length; i++) {
      counts[cardNo + 1 + i] += counts[cardNo];
    }
  }
  return counts.reduce((v, e) => v + e);
}
