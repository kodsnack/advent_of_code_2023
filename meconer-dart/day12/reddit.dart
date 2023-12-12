import 'dart:convert';
import 'dart:io';

int sumOfPossibleArrangementCount() {
  try {
    var input = File('day12/input.txt').readAsStringSync();
    var recordsAndGroups = parse(input);
    var records = recordsAndGroups[0];
    var groups = recordsAndGroups[1];
    var res = 0;

    for (var i = 0; i < records.length; i++) {
      res += solve(unfoldRecord(records[i]), unfoldGroup(groups[i]));
    }

    print(res);
    return res;
  } catch (e) {
    print(e);
    return 0;
  }
}

String unfoldRecord(String record) {
  var res = StringBuffer();
  for (var i = 0; i < record.length * 5; i++) {
    if (i != 0 && i % record.length == 0) {
      res.write('?');
    }
    res.write(record[i % record.length]);
  }

  return res.toString();
}

List<int> unfoldGroup(List<int> group) {
  var res = <int>[];
  for (var i = 0; i < group.length * 5; i++) {
    res.add(group[i % group.length]);
  }

  return res;
}

int solve(String record, List<int> group) {
  var cache =
      List.generate(record.length, (i) => List.filled(group.length + 1, -1));

  return dp(0, 0, record, group, cache);
}

int dp(int i, int j, String record, List<int> group, List<List<int>> cache) {
  if (i >= record.length) {
    if (j < group.length) {
      return 0;
    }
    return 1;
  }

  if (cache[i][j] != -1) {
    return cache[i][j];
  }

  var res = 0;
  if (record[i] == '.') {
    res = dp(i + 1, j, record, group, cache);
  } else {
    if (record[i] == '?') {
      res += dp(i + 1, j, record, group, cache);
    }
    if (j < group.length) {
      var count = 0;
      for (var k = i; k < record.length; k++) {
        if (count > group[j] ||
            record[k] == '.' ||
            (count == group[j] && record[k] == '?')) {
          break;
        }
        count += 1;
      }

      if (count == group[j]) {
        if (i + count < record.length && record[i + count] != '#') {
          res += dp(i + count + 1, j + 1, record, group, cache);
        } else {
          res += dp(i + count, j + 1, record, group, cache);
        }
      }
    }
  }

  cache[i][j] = res;
  return res;
}

List<dynamic> parse(String input) {
  var records = <String>[];
  var groups = <List<int>>[];

  for (var line in LineSplitter.split(input.replaceAll('\r\n', '\n'))) {
    var parts = line.split(' ');
    records.add(parts[0]);
    var group = parts[1].split(',').map((num) => int.parse(num)).toList();
    groups.add(group);
  }

  return [records, groups];
}

void main() {
  sumOfPossibleArrangementCount();
}
