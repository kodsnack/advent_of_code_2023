import '../util/util.dart';

const String inputFile = 'day24/example.txt';
// const String inputFile = 'day24/input.txt';

Future<void> main(List<String> args) async {
  var input = await readInputAsString(inputFile);

  int n = 1;
  List<String> lines = [];
  for (final line in input.split('\n')) {
    Point p;
    Vector v;
    (p, v) = getValsFromLine(line);
    // final p2 = p.add(v.mul(1000000000000));
    final p2 = p.add(v.mul(10));

    String s =
        'line$n = Part.makeLine( (${p.px},${p.py},${p.pz}), (${p2.px},${p2.py},${p2.pz}) )';
    lines.add(s);
    print(s);

    s = 'Part.show(line$n)';
    lines.add(s);
    print(s);

    // s = 'sph$n = Part.makeSphere( 1000, FreeCAD.Vector(${p.px},${p.py},${p.pz}) )';
    // lines.add(s);
    // print(s);

    // s = 'Part.show(sph$n)';
    // lines.add(s);
    // print(s);

    n++;
  }
  printToFile('test.py', lines);
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
