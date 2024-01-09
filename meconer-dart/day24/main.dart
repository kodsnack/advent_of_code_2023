import '../util/util.dart';

const String inputFile = 'day24/example.txt';
// const String inputFile = 'day24/input.txt';

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
  List<HailStone> hailStones = [];
  for (final line in lines) {
    Point p;
    Vector v;
    (p, v) = getValsFromLine(line);
    hailStones.add(HailStone(p, v));
  }

  int minXY = 7;
  int maxXY = 27;
  // int minXY = 200000000000000;
  // int maxXY = 400000000000000;

  int count = 0;
  for (int i = 0; i < hailStones.length - 1; i++) {
    for (int j = i + 1; j < hailStones.length; j++) {
      final intersection = getFutureXYIntersection(
          hailStones[i].p, hailStones[i].v, hailStones[j].p, hailStones[j].v);
      if (intersection == null) continue;
      if (intersection.px >= minXY &&
          intersection.px <= maxXY &&
          intersection.py >= minXY &&
          intersection.py <= maxXY) count++;
    }
  }
  return count;
}

int calcResultP2(String input) {
  final lines = input.split('\n');
  List<HailStone> hailStones = [];
  for (final line in lines) {
    Point p;
    Vector v;
    (p, v) = getValsFromLine(line);
    hailStones.add(HailStone(p, v));
  }

  Point pRock = Point(0, 0, 0);
  Vector vRock = Vector(0, 0, 0);

  return 0;
}

Point? getFutureXYIntersection(Point p1, Vector v1, Point p2, Vector v2) {
  // Calculate the determinant
  double det = v1.vx * v2.vy - v1.vy * v2.vx;

  // Check if the lines are parallel (det == 0)
  if (det == 0) {
    // Lines are parallel, no intersection
    return null;
  }

  // Calculate the intersection point
  double t1 = ((p2.px - p1.px) * v2.vy - (p2.py - p1.py) * v2.vx) / det;
  if (t1 <= 0) return null;
  double t2 = ((p2.px - p1.px) * v1.vy - (p2.py - p1.py) * v1.vx) / det;
  if (t2 <= 0) return null;
  double x = p1.px + t1 * v1.vx;
  double y = p1.py + t1 * v1.vy;

  return Point(x, y, 0);
}

getValsFromLine(String line) {
  final posStr = line.split(' @ ')[0];
  final velStr = line.split(' @ ')[1];
  final posList = posStr.split(', ').map((e) => double.parse(e)).toList();
  final velList = velStr.split(', ').map((e) => double.parse(e)).toList();
  return (
    Point(
      posList[0],
      posList[1],
      posList[2],
    ),
    Vector(
      velList[0],
      velList[1],
      velList[2],
    )
  );
}

class Point {
  double px, py, pz;
  Point(this.px, this.py, this.pz);

  Point add(Vector v) {
    return Point(px + v.vx, py + v.vy, pz + v.vz);
  }
}

class Vector {
  double vx, vy, vz;
  Vector(this.vx, this.vy, this.vz);

  Vector mul(int s) {
    return Vector(vx * s, vy * s, vz * s);
  }
}

class HailStone {
  Point p;
  Vector v;
  HailStone(this.p, this.v);

  Point getPointAt(int time) {
    return p.add(v.mul(time));
  }
}
