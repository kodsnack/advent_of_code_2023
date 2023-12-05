import '../util/util.dart';

// const String inputFile = 'day2/example.txt';
const String inputFile = 'day2/input.txt';

Future<void> main(List<String> args) async {
  var input = await readInputAsString(inputFile);

  print('Part 1:');
  final resultP1 = calcResultP1(input);
  print(resultP1);

  print('Part 2:');
  final resultP2 = calcResultP2(input);
  print(resultP2);
}

calcResultP1(String input) {
  int sum = 0;
  for (final line in input.split('\n')) {
    int gameId = int.parse(line.split(':')[0].trim().split(' ')[1]);
    bool isValid = true;
    for (final gameParts in line.split(':')[1].trim().split(';')) {
      for (final gamePart in gameParts.split(',')) {
        if (!isValidGame(gamePart)) {
          isValid = false;
          break;
        }
      }
    }
    if (isValid) sum += gameId;
  }
  return sum;
}

calcResultP2(String input) {
  int sum = 0;
  for (final line in input.split('\n')) {
    final minVals = getMinVals(line.split(':')[1].trim());
    final power = minVals.getPower();
    sum += power;
  }
  return sum;
}

bool isValidGame(String gamePart) {
  int redInBag = 12;
  int greenInBag = 13;
  int blueInBag = 14;
  final count = int.parse(gamePart.trim().split(' ')[0]);
  final color = gamePart.trim().split(' ')[1];
  if (color == 'red' && count > redInBag) return false;
  if (color == 'green' && count > greenInBag) return false;
  if (color == 'blue' && count > blueInBag) return false;
  return true;
}

RGB getMinVals(String gameLine) {
  RGB minVals = RGB(0, 0, 0);

  for (final gameParts in gameLine.trim().split(';')) {
    for (final gamePart in gameParts.split(',')) {
      final count = int.parse(gamePart.trim().split(' ')[0]);
      final color = gamePart.trim().split(' ')[1];
      minVals.extend(color, count);
    }
  }
  return minVals;
}

class RGB {
  int red;
  int green;
  int blue;
  RGB(this.red, this.green, this.blue);

  int getPower() {
    return red * green * blue;
  }

  void extend(String color, int value) {
    if (color == 'red' && value > red) red = value;
    if (color == 'green' && value > green) green = value;
    if (color == 'blue' && value > blue) blue = value;
  }
}
