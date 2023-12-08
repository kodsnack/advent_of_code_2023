import 'dart:math';

import '../util/util.dart';

// const String inputFile = 'day6/example.txt';
const String inputFile = 'day6/input.txt';

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
  final raceTimes = lines[0]
      .split(':')[1]
      .trim()
      .split(RegExp(' +'))
      .map((e) => int.parse(e))
      .toList();

  final recordDistances = lines[1]
      .split(':')[1]
      .trim()
      .split(RegExp(' +'))
      .map((e) => int.parse(e))
      .toList();

  int result = 1;
  for (int raceNo = 0; raceNo < raceTimes.length; raceNo++) {
    final (firstPushTimeToBeatRecord, lastPushTimeToBeatRecord) =
        getPushTimesToWin(raceTimes[raceNo], recordDistances[raceNo]);
    final numberOfWaysToBeatRecord =
        lastPushTimeToBeatRecord - firstPushTimeToBeatRecord + 1;
    result *= numberOfWaysToBeatRecord;
  }

  return result;
}

int calcResultP2(String input) {
  final lines = input.split('\n');
  final raceTime = int.parse(lines[0].split(':')[1].replaceAll(' ', ''));

  final recordDistance = int.parse(lines[1].split(':')[1].replaceAll(' ', ''));

  final (firstPushTimeToBeatRecord, lastPushTimeToBeatRecord) =
      getPushTimesToWin(raceTime, recordDistance);
  final numberOfWaysToBeatRecord =
      lastPushTimeToBeatRecord - firstPushTimeToBeatRecord + 1;

  return numberOfWaysToBeatRecord;
}

// Total time raceTime = pushTime + travelTime
// speed = pushTime
// travelTime = raceTime - pushTime
// distance = travelTime * speed
// distance = (raceTime - pushTime) * speed
// distance = (raceTime - pushTime) * pushTime
// distance = raceTime * pushTime - pushTime^2
// pushTime^2 - raceTime * pushTime + distance = 0;
// pushTime = raceTime / 2 +- sqrt( raceTime^2 / 4 - distance)
//
(int, int) getPushTimesToWin(int raceTime, int recordDistance) {
  double pushTime1 =
      raceTime / 2 + sqrt(raceTime * raceTime / 4 - recordDistance);
  double pushTime2 =
      raceTime / 2 - sqrt(raceTime * raceTime / 4 - recordDistance);
  print('$pushTime1 : $pushTime2');
  if (pushTime1.floor() == pushTime1.ceil()) {
    pushTime1 += 0.01;
  }
  if (pushTime2.floor() == pushTime2.ceil()) {
    pushTime1 -= 0.01;
  }
  final firstPushTimeToBeatRecord = pushTime2.ceil();
  final lastPushTimeToBeatRecord = pushTime1.floor();
  return (firstPushTimeToBeatRecord, lastPushTimeToBeatRecord);
}
