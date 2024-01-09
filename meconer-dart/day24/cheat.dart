import '../util/util.dart';

class Hailstone {
  final int px, py, pz, vx, vy, vz;

  Hailstone(this.px, this.py, this.pz, this.vx, this.vy, this.vz);
}

Map<int, List<int>> velocitiesX = {};
Map<int, List<int>> velocitiesY = {};
Map<int, List<int>> velocitiesZ = {};
List<Hailstone> hailstones = [];

int getRockVelocity(Map<int, List<int>> velocities) {
  var possibleV = List<int>.generate(2001, (i) => i - 1000);

  velocities.forEach((vel, values) {
    if (values.length < 2) {
      return;
    }

    var newPossibleV = <int>[];
    for (var possible in possibleV) {
      // Add a check to ensure that the denominator is not zero
      if (possible - vel != 0 &&
          (values[0] - values[1]) % (possible - vel) == 0) {
        newPossibleV.add(possible);
      }
    }

    possibleV = newPossibleV;
  });

  return possibleV[0];
}

Future<void> coordinatesOfInitialPosition() async {
  const String inputFile = 'day24/example.txt';
  // const String inputFile = 'day24/input.txt';
  var input = await readInputAsString(inputFile);
  final lines = input.split('\n');

  for (var line in lines) {
    final parts = line.split(' @ ');
    final positions = parts[0];
    final velocity = parts[1];

    final pos = positions.split(', ').map((n) => int.parse(n)).toList();
    final px = pos[0], py = pos[1], pz = pos[2];

    final vel = velocity.split(', ').map((n) => int.parse(n)).toList();
    final vx = vel[0], vy = vel[1], vz = vel[2];

    if (!velocitiesX.containsKey(vx)) {
      velocitiesX[vx] = [px];
    } else {
      velocitiesX[vx]!.add(px);
    }

    if (!velocitiesY.containsKey(vy)) {
      velocitiesY[vy] = [py];
    } else {
      velocitiesY[vy]!.add(py);
    }

    if (!velocitiesZ.containsKey(vz)) {
      velocitiesZ[vz] = [pz];
    } else {
      velocitiesZ[vz]!.add(pz);
    }

    hailstones.add(Hailstone(px, py, pz, vx, vy, vz));
  }

  // var possibleVX = List<int>.generate(2001, (i) => i - 1000);

  final rvx = getRockVelocity(velocitiesX);
  final rvy = getRockVelocity(velocitiesY);
  final rvz = getRockVelocity(velocitiesZ);

  var results = <int, int>{};
  for (var i = 0; i < hailstones.length; i++) {
    for (var j = i + 1; j < hailstones.length; j++) {
      final stoneA = hailstones[i];
      final stoneB = hailstones[j];

      final ma = (stoneA.vy - rvy) / (stoneA.vx - rvx);
      final mb = (stoneB.vy - rvy) / (stoneB.vx - rvx);

      final ca = stoneA.py - ma * stoneA.px;
      final cb = stoneB.py - mb * stoneB.px;

      final rpx = ((ma - mb) != 0) ? (cb - ca) ~/ (ma - mb) : 0;
      final rpy = ((ma - mb) != 0) ? (ma * rpx + ca).toInt() : 0;
      final time =
          ((stoneA.vx - rvx) != 0) ? (rpx - stoneA.px) ~/ (stoneA.vx - rvx) : 0;

      final rpz = stoneA.pz + (stoneA.vz - rvz) * time;

      final result = rpx + rpy + rpz;
      results[result] = results[result] == null ? 1 : results[result]! + 1;
    }
  }

  var keys = results.keys.toList()..sort((a, b) => results[b]! - results[a]!);
  print(keys[0]);
}

void main(List<String> args) {
  coordinatesOfInitialPosition();
}
