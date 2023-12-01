import '../util/util.dart';

// const String inputFile = 'day1/example.txt';
// const String inputFile = 'day1/example2.txt';
const String inputFile = 'day1/input.txt';

Future<void> main(List<String> args) async {
  var input = await readInputAsString(inputFile);

  // print('Part 1:');
  // final resultP1 = calcResultP1(input);
  // print(resultP1);

  print('Part 2:');
  final resultP2 = calcResultP2(input);
  print(resultP2);
}

calcResultP1(String input) {
  final re = RegExp(r'\d');

  int sum = 0;
  for (final line in input.split('\n')) {
    final list = line.split('');
    final firstDigit =
        int.parse(list.firstWhere((element) => re.hasMatch(element)));
    final lastDigit =
        int.parse(list.lastWhere((element) => re.hasMatch(element)));
    int lineValue = firstDigit * 10 + lastDigit;
    sum += lineValue;
  }
  return sum;
}

calcResultP2(String input) {
  const digitStrings = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine'
  ];

  List<String> digitStringsReversed =
      digitStrings.map((e) => e.split('').reversed.join()).toList();

  final regexStr = r'(\d|' + digitStrings.join('|') + ')';
  final regex = RegExp(regexStr);

  final regexStrReversed = r'(\d|' + digitStringsReversed.join('|') + ')';
  final regexReversed = RegExp(regexStrReversed);

  int sum = 0;

  for (final line in input.split('\n')) {
    final matches = regex.allMatches(line);
    final firstMatch = matches.first.group(0);
    int firstDigit = isDigit(firstMatch!, 0)
        ? int.parse(firstMatch)
        : digitStrings.indexWhere((element) => element == firstMatch) + 1;

    final reverseMatches =
        regexReversed.allMatches(line.split('').reversed.join());

    final lastMatch = reverseMatches.first.group(0);
    int lastDigit = isDigit(lastMatch!, 0)
        ? int.parse(lastMatch)
        : digitStringsReversed.indexWhere((element) => element == lastMatch) +
            1;

    int lineValue = firstDigit * 10 + lastDigit;
    sum += lineValue;
  }
  return sum;
}
