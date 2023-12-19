enum Direction { Up, Right, Down, Left }

class LinePos {
  final int col, row;
  LinePos(this.col, this.row);

  LinePos moveUp() {
    return LinePos(col, row - 1);
  }

  LinePos moveDown() {
    return LinePos(col, row + 1);
  }

  LinePos moveLeft() {
    return LinePos(col - 1, row);
  }

  LinePos moveRight() {
    return LinePos(col + 1, row);
  }

  LinePos moveDirStr(String command) {
    switch (command.substring(0, 1)) {
      case 'U':
        return moveUp();
      case 'N':
        return moveUp();
      case 'D':
        return moveDown();
      case 'S':
        return moveDown();
      case 'L':
        return moveLeft();
      case 'W':
        return moveLeft();
      case 'R':
        return moveRight();
      case 'E':
        return moveRight();
      default:
        throw Exception('Wrong command');
    }
  }

  LinePos moveDir(Direction dir) {
    switch (dir) {
      case Direction.Up:
        return moveUp();
      case Direction.Down:
        return moveDown();
      case Direction.Left:
        return moveLeft();
      case Direction.Right:
        return moveRight();
    }
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is LinePos && (col == other.col && row == other.row);
  }

  int get hashCode => (col * 100000 + row);

  moveDirWithLimit(Direction dir, int colLimit, int rowLimit) {
    LinePos pos = moveDir(dir);
    if (pos.col < 0) return LinePos(0, pos.row);
    if (pos.col > colLimit) return LinePos(colLimit, pos.row);
    if (pos.row < 0) return LinePos(pos.col, 0);
    if (pos.row > rowLimit) return LinePos(pos.col, rowLimit);
    return pos;
  }

  int manhattanDistance(LinePos pos) {
    int xDist = (pos.col - col).abs();
    int yDist = (pos.row - row).abs();
    return xDist + yDist;
  }

  LinePos moveNW() {
    return moveUp().moveLeft();
  }

  LinePos moveNE() {
    return moveUp().moveRight();
  }

  LinePos moveSW() {
    return moveDown().moveLeft();
  }

  LinePos moveSE() {
    return moveDown().moveRight();
  }

  LinePos moveN() {
    return moveUp();
  }

  LinePos moveW() {
    return moveLeft();
  }

  LinePos moveS() {
    return moveDown();
  }

  LinePos moveE() {
    return moveRight();
  }

  List<LinePos> getNeighbours() {
    return [moveUp(), moveLeft(), moveDown(), moveRight()];
  }

  static String getOppositeDirection(String direction) {
    switch (direction) {
      case 'N':
        return 'S';
      case 'E':
        return 'W';
      case 'S':
        return 'N';
      case 'W':
        return 'E';
      case 'U':
        return 'D';
      case 'L':
        return 'R';
      case 'R':
        return 'L';
      case 'D':
        return 'U';
      default:
        return '';
    }
  }

  LinePos moveDist(int length, String directionStr) {
    switch (directionStr) {
      case 'U':
      case 'N':
        return LinePos(col, row - length);
      case 'E':
      case 'R':
        return LinePos(col + length, row);
      case 'S':
      case 'D':
        return LinePos(col, row + length);
      case 'W':
      case 'L':
        return LinePos(col - length, row);
      default:
        throw ArgumentError('Wrong direction str');
    }
  }
}
