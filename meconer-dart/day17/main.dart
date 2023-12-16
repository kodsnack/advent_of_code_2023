import '../util/util.dart';

const String inputFile = 'day17/example.txt';
// const String inputFile = 'day17/input.txt';

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

  return 0;
}
