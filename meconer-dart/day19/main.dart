import '../util/util.dart';

// const String inputFile = 'day19/example.txt';
const String inputFile = 'day19/input.txt';

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

  // Read workflows
  Map<String, WorkFlow> workFlows = {};
  int lineNo = 0;
  while (lines[lineNo] != '') {
    String workFlowName = lines[lineNo].split('{')[0];
    workFlows[workFlowName] = getWorkFlowFromLine(lines[lineNo]);
    lineNo++;
  }
  lineNo++;
  // Read parts
  List<Part> parts = [];
  while (lineNo < lines.length) {
    Part part = Part(lines[lineNo]);
    parts.add(part);
    lineNo++;
  }

  int sum = 0;
  for (final part in parts) {
    bool ready = false;
    var workFlow = workFlows['in'];
    while (!ready) {
      String result = workFlow!.eval(part);

      if (result == 'A') {
        // Accepted
        sum += part.getAcceptedValue();
        ready = true;
        break;
      }
      if (result == 'R') {
        // Rejected
        ready = true;
        break;
      }
      workFlow = workFlows[result]!;
    }
  }

  return sum;
}

int calcResultP2(String input) {
  final lines = input.split('\n');

  // Read workflows
  Map<String, WorkFlow> workFlows = {};
  int lineNo = 0;
  while (lines[lineNo] != '') {
    String workFlowName = lines[lineNo].split('{')[0];
    workFlows[workFlowName] = getWorkFlowFromLine(lines[lineNo]);
    lineNo++;
  }

  int combinations = workFlows['in']!.countCombinations(workFlows, Ranges());
  return combinations;
}

class Part {
  late int x, m, a, s;
  Part(String line) {
    line = line.replaceAll('{', '');
    line = line.replaceAll('}', '');
    final lineParts = line.split(',');
    for (final linePart in lineParts) {
      String varName = linePart.split('=')[0];
      int value = int.parse(linePart.split('=')[1]);
      switch (varName) {
        case 'x':
          x = value;
          break;
        case 'm':
          m = value;
          break;
        case 'a':
          a = value;
          break;
        case 's':
          s = value;
          break;
      }
    }
  }

  int getVal(String varName) {
    switch (varName) {
      case 'x':
        return x;
      case 'm':
        return m;
      case 'a':
        return a;
      case 's':
        return s;
      default:
        return 0;
    }
  }

  int getAcceptedValue() {
    return x + m + s + a;
  }
}

WorkFlow getWorkFlowFromLine(String line) {
  WorkFlow workFlow = WorkFlow();

  String rulesPart = line.substring(line.indexOf('{') + 1);
  rulesPart = rulesPart.substring(0, rulesPart.length - 1);
  for (final rulePart in rulesPart.split(',')) {
    if (rulePart.contains(':')) {
      // A condition
      String conditionPart = rulePart.split(':')[0];
      Rule rule = Rule(conditionPart[0], conditionPart[1],
          int.parse(conditionPart.substring(2)), rulePart.split(':')[1]);
      workFlow.rules.add(rule);
    } else {
      // No condition. Only a consequence
      workFlow.rules.add(Rule('', '', 0, rulePart));
    }
  }
  return workFlow;
}

class Ranges {
  int xMin = 1;
  int xMax = 4000;
  int mMin = 1;
  int mMax = 4000;
  int aMin = 1;
  int aMax = 4000;
  int sMin = 1;
  int sMax = 4000;

  Ranges();

  Ranges.fromRanges(Ranges ranges) {
    xMin = ranges.xMin;
    xMax = ranges.xMax;
    mMin = ranges.mMin;
    mMax = ranges.mMax;
    aMin = ranges.aMin;
    aMax = ranges.aMax;
    sMin = ranges.sMin;
    sMax = ranges.sMax;
  }

  int countCombinations() {
    if (xMax < xMin || mMax < mMin || aMax < aMin || sMax < sMin) return 0;
    return (xMax - xMin + 1) *
        (mMax - mMin + 1) *
        (aMax - aMin + 1) *
        (sMax - sMin + 1);
  }

  Ranges limitRange(String varName, String condition, int val) {
    Ranges newRange = Ranges.fromRanges(this);
    switch (varName) {
      case 'x':
        if (condition == '<') newRange.xMax = val - 1;
        if (condition == '>') newRange.xMin = val + 1;
      case 'm':
        if (condition == '<') newRange.mMax = val - 1;
        if (condition == '>') newRange.mMin = val + 1;
      case 'a':
        if (condition == '<') newRange.aMax = val - 1;
        if (condition == '>') newRange.aMin = val + 1;
      case 's':
        if (condition == '<') newRange.sMax = val - 1;
        if (condition == '>') newRange.sMin = val + 1;
    }
    return newRange;
  }

  Ranges oppositeRange(String varName, String condition, int value) {
    Ranges newRange = Ranges.fromRanges(this);
    String oppositeCond = condition == '<' ? '>' : '<';
    int val = (oppositeCond == '<') ? value + 1 : value - 1;

    switch (varName) {
      case 'x':
        if (oppositeCond == '<') newRange.xMax = val - 1;
        if (oppositeCond == '>') newRange.xMin = val + 1;
      case 'm':
        if (oppositeCond == '<') newRange.mMax = val - 1;
        if (oppositeCond == '>') newRange.mMin = val + 1;
      case 'a':
        if (oppositeCond == '<') newRange.aMax = val - 1;
        if (oppositeCond == '>') newRange.aMin = val + 1;
      case 's':
        if (oppositeCond == '<') newRange.sMax = val - 1;
        if (oppositeCond == '>') newRange.sMin = val + 1;
    }
    return newRange;
  }
}

class WorkFlow {
  List<Rule> rules = [];

  String eval(Part part) {
    for (final rule in rules) {
      if (rule.condition == '') return rule.consequence;
      if (rule.condition == '<') {
        if (part.getVal(rule.category) < rule.value) return rule.consequence;
      }
      if (rule.condition == '>') {
        if (part.getVal(rule.category) > rule.value) return rule.consequence;
      }
    }
    return 'Error!';
  }

  int countCombinations(Map<String, WorkFlow> workFlows, Ranges ranges) {
    int count = 0;

    // condition can be '<', '>' or nothing ''
    for (final rule in rules) {
      if (rule.condition == '') {
        // No condition. We can have A, R or a subflow
        if (rule.consequence == 'A') {
          count += ranges.countCombinations();
        } else if (rule.consequence != 'R') {
          // Count the number of combinations for the sub flow
          int partCount =
              workFlows[rule.consequence]!.countCombinations(workFlows, ranges);
          count += partCount;
          break; // Sub workFlows never return
        }
        // We do nothing for the rejection
      }

      if (rule.condition == '<') {
        final remainingRanges =
            ranges.oppositeRange(rule.category, rule.condition, rule.value);
        ranges = ranges.limitRange(rule.category, rule.condition, rule.value);
        if (rule.consequence == 'A') {
          // This many parts is accepted
          count += ranges.countCombinations();
          // The remaining range is left
          ranges = remainingRanges;
        } else if (rule.consequence == 'R') {
          // Remaining ranges is left
          ranges = remainingRanges;
        } else {
          // There is a sub workflow
          int partCount =
              workFlows[rule.consequence]!.countCombinations(workFlows, ranges);
          count += partCount;
          // Remaining ranges is left
          ranges = remainingRanges;
        }
      }

      if (rule.condition == '>') {
        final remainingRanges =
            ranges.oppositeRange(rule.category, rule.condition, rule.value);
        ranges = ranges.limitRange(rule.category, rule.condition, rule.value);
        if (rule.consequence == 'A') {
          // This many parts is accepted
          count += ranges.countCombinations();
          // The remaining range is left
          ranges = remainingRanges;
        } else if (rule.consequence == 'R') {
          // Remaining ranges is left
          ranges = remainingRanges;
        } else {
          int partCount =
              workFlows[rule.consequence]!.countCombinations(workFlows, ranges);
          count += partCount;
          // Remaining ranges is left
          ranges = remainingRanges;
        }
      }
    }
    return count;
  }
}

class Rule {
  String category;
  String condition;
  int value;
  String consequence;
  Rule(this.category, this.condition, this.value, this.consequence);
}
