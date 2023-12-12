import '../util/util.dart';

// const String inputFile = 'day12/example.txt';
const String inputFile = 'day12/input.txt';

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

// 7084
int calcResultP1(String input) {
  final lines = input.split('\n');
  int sum = 0;
  for (final line in lines) {
    int count = countPossibilites(line);
    // print(count);
    sum += count;
  }
  return sum;
}

//8414003326821
int calcResultP2(String input) {
  final lines = input.split('\n');
  int sum = 0;
  int lineNo = 1;
  for (final line in lines) {
    int count = countPossibilitesP2(line);
    print('$lineNo: $count');
    lineNo++;
    sum += count;
  }
  return sum;
}

int countPossibilites(String line) {
  final groups =
      line.split(' ')[1].split(',').map((e) => int.parse(e)).toList();

  int count = matchCountP2(line.split(' ')[0], groups, {});
  // int count = matchCount(line.split(' ')[0], groups);
  return count;
}

int countPossibilitesP2(String line) {
  final groupPart =
      line.split(' ')[1].split(',').map((e) => int.parse(e)).toList();
  final linePart = line.split(' ')[0];
  List<int> groups = [];
  String lineToTest = '';
  for (int i = 0; i < 5; i++) {
    groups.addAll(groupPart);
  }
  for (int i = 0; i < 4; i++) {
    lineToTest += linePart;
    lineToTest += '?';
  }
  lineToTest += linePart;
  int count = matchCountP2(lineToTest, groups, {});
  return count;
}

int matchCount(String line, List<int> groupsToMatch) {
  if (!line.contains('?')) {
    // No more ?:s Check if we match the group count
    List<int> groups = getGrouping(line);

    // If the groups are different lengts there is no match
    if (groupsToMatch.length != groups.length) return 0;

    // Check if the groups count are similar
    for (int idx = 0; idx < groups.length; idx++) {
      if (groupsToMatch[idx] != groups[idx]) return 0;
    }

    // Groups are identical. We have 1 match
    return 1;
  } else {
    // We have ? chars left.
    // Try both '.' and '#'
    int count = matchCount(line.replaceFirst('?', '.'), groupsToMatch);
    count += matchCount(line.replaceFirst('?', '#'), groupsToMatch);
    return count;
  }
}

int matchCountP2(String line, List<int> groupsToMatch, Map<String, int> memo) {
  String key = line + ' ' + groupsToMatch.map((e) => e.toString()).join(',');
  if (memo.containsKey(key)) return memo[key]!;
  if (groupsToMatch.isEmpty) {
    if (line.contains('#')) {
      return 0;
    }
    return 1;
  }
  if (!line.contains('?')) {
    // No more ?:s Check if we match the group count
    List<int> groups = getGrouping(line);

    // If the groups are different lengts there is no match
    if (groupsToMatch.length != groups.length) {
      return 0;
    }

    // Check if the groups are equal
    for (int idx = 0; idx < groups.length; idx++) {
      if (groupsToMatch[idx] != groups[idx]) {
        return 0;
      }
    }

    // Groups are identical. We have 1 match
    return 1;
  }
  // We have ? chars left.
  // int neededLength =
  //     groupsToMatch.fold(0, (p, e) => p + e) + groupsToMatch.length - 1;
  // if (line.length <= neededLength) return 0;

  while (line.startsWith('.')) {
    line = line.substring(1);
  }
  if (line.startsWith('?')) {
    int count = matchCountP2(line.replaceFirst('?', '.'), groupsToMatch, memo);
    count += matchCountP2(line.replaceFirst('?', '#'), groupsToMatch, memo);
    String key = line + ' ' + groupsToMatch.map((e) => e.toString()).join(',');
    memo[key] = count;
    return count;
  }

  int nextGroupToMatch = groupsToMatch.first;

  if (nextGroupToMatch > line.length) return 0;

  final groupStr = line.substring(0, nextGroupToMatch);
  if (groupStr.contains('.')) {
    return 0;
  } else {
    if (line.length > nextGroupToMatch && line[nextGroupToMatch] == '#') {
      return 0;
    }
    String nextLine = line.substring(nextGroupToMatch);
    if (nextLine.isEmpty) {
      if (groupsToMatch.length == 1) {
        return 1;
      }
      return 0;
    }
    nextLine = '.' + nextLine.substring(1);
    final nextGroup = groupsToMatch.sublist(1);
    String key = nextLine + ' ' + nextGroup.map((e) => e.toString()).join(',');
    int count = matchCountP2(nextLine, groupsToMatch.sublist(1), memo);
    memo[key] = count;
    return matchCountP2(nextLine, groupsToMatch.sublist(1), memo);
  }
}

List<int> getGrouping(String line) {
  List<int> groups = [];
  int groupCount = 0;
  for (final char in line.split('')) {
    if (groupCount > 0) {
      // We are in a group
      if (char == '#') {
        groupCount++;
      } else {
        groups.add(groupCount);
        groupCount = 0;
      }
    }
    if (groupCount == 0 && char == '#') {
      groupCount++;
    }
  }
  if (groupCount > 0) groups.add(groupCount);
  return groups;
}
