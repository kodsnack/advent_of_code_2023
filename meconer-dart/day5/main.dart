import 'dart:math';

import '../util/util.dart';

// const String inputFile = 'day5/example.txt';
const String inputFile = 'day5/input.txt';

Future<void> main(List<String> args) async {
  var input = await readInputAsString(inputFile);

  print('Part 1:');
  final resultP1 = calcResultP1(input);
  print(resultP1);

  Stopwatch stopwatch = Stopwatch();
  stopwatch.start();
  print('Part 2:');
  final resultP2 = calcResultP2(input);
  print(resultP2);
  stopwatch.stop();
  int mikros = stopwatch.elapsedMicroseconds;
  int millis = mikros ~/ 1000;
  mikros %= 1000;
  print('Time : $millis,$mikros ms');
}

int calcResultP1(String input) {
  final lines = input.split('\n');
  final digitRegexp = RegExp(r'\d');
  List<int> seeds = lines[0]
      .split(':')[1]
      .trim()
      .split(' ')
      .map((e) => int.parse(e))
      .toList();

  List<Conversion> conversions = [];
  int lineNo = 2;
  while (true) {
    final conversion = Conversion.from(lines[lineNo]);
    conversions.add(conversion);
    lineNo++;

    while (lines[lineNo].startsWith(digitRegexp)) {
      final convMap = ConversionMap.from(lines[lineNo]);
      conversion.conversionMaps.add(convMap);
      lineNo++;
      if (lineNo >= lines.length) break;
    }
    lineNo++;
    if (lineNo >= lines.length) break;
  }

  int minLocationNo = veryLargeNumber;
  for (final seed in seeds) {
    int locationNo = findLocation(seed, conversions);
    minLocationNo = min(minLocationNo, locationNo);
  }
  return minLocationNo;
}

int calcResultP2(String input) {
  final lines = input.split('\n');
  List<Range> ranges = getRanges(lines[0]);

  final conversions = getConversions(lines);

  List<Range> newRanges = [];
  for (final conversion in conversions) {
    for (final range in ranges) {
      List<Range> convertedRanges = conversion.splitAndConvertRange(range);
      newRanges.addAll(convertedRanges);
    }
    ranges = newRanges;
    newRanges = [];
  }

  int minLocationNo = veryLargeNumber;
  for (int rNo = 0; rNo < ranges.length; rNo++) {
    if (ranges[rNo].start < minLocationNo) {
      // print('$rNo : ${ranges[rNo].start}');
      minLocationNo = ranges[rNo].start;
    }
  }
  return minLocationNo;
}

List<Range> getRanges(String line) {
  List<Range> ranges = [];
  final linePart =
      line.split(':')[1].trim().split(' ').map((e) => int.parse(e)).toList();
  for (int i = 0; i < linePart.length; i++) {
    int start = linePart.removeAt(0);
    int length = linePart.removeAt(0);
    ranges.add(Range(start, length));
  }
  return ranges;
}

List<Conversion> getConversions(List<String> lines) {
  int lineNo = 2;
  final digitRegexp = RegExp(r'\d');
  List<Conversion> conversions = [];
  while (true) {
    final conversion = Conversion.from(lines[lineNo]);
    conversions.add(conversion);
    lineNo++;

    while (lines[lineNo].startsWith(digitRegexp)) {
      final convMap = ConversionMap.from(lines[lineNo]);
      conversion.conversionMaps.add(convMap);
      lineNo++;
      if (lineNo >= lines.length) break;
    }

    conversion.conversionMaps
        .sort((a, b) => a.sourceRangeStart.compareTo(b.sourceRangeStart));
    lineNo++;
    if (lineNo >= lines.length) break;
  }
  return conversions;
}

int findLocation(int seed, List<Conversion> conversions) {
  int nextValue = seed;
  for (final conversion in conversions) {
    nextValue = conversion.convert(nextValue);
  }
  return nextValue;
}

class ConversionMap {
  late int destRangeStart;
  late int sourceRangeStart;
  late int length;
  ConversionMap(this.destRangeStart, this.sourceRangeStart, this.length);

  ConversionMap.from(String line) {
    final parts = line.split(' ');
    destRangeStart = int.parse(parts[0]);
    sourceRangeStart = int.parse(parts[1]);
    length = int.parse(parts[2]);
  }

  bool inSourceRange(int value) {
    return (value >= sourceRangeStart && value < sourceRangeStart + length);
  }

  bool rangeContained(Range range) {
    return inSourceRange(range.start) &&
        inSourceRange(range.start + range.length - 1);
  }

  int convert(int value) {
    // Get the offset from range start
    int offset = value - sourceRangeStart;
    return destRangeStart + offset;
  }

  bool overlapAtStart(Range range) {
    int end = range.start + range.length - 1;
    int sourceEnd = sourceRangeStart + length;
    return range.start < sourceRangeStart &&
        end >= sourceRangeStart &&
        end < sourceEnd;
  }

  bool overlapAtEnd(Range range) {
    int end = range.start + range.length - 1;
    int sourceEnd = sourceRangeStart + length;
    return range.start >= sourceRangeStart &&
        range.start < sourceEnd &&
        end > sourceEnd;
  }

  bool isInside(Range range) {
    int end = range.start + range.length - 1;
    int sourceEnd = sourceRangeStart + length;
    return range.start < sourceRangeStart && end > sourceEnd;
  }
}

class Conversion {
  late String source;
  late String destination;
  List<ConversionMap> conversionMaps = [];

  Conversion(this.source, this.destination);

  Conversion.from(String line) {
    final parts = line.split(' ')[0].split('-');
    source = parts[0];
    destination = parts[2];
  }

  int convert(int value) {
    for (final convMap in conversionMaps) {
      if (convMap.inSourceRange(value)) {
        return convMap.convert(value);
      }
    }
    // If we get here there is no conversion
    return value;
  }

  List<Range> splitAndConvertRange(Range range) {
    List<Range> finishedRanges = [];
    int start = range.start;
    int end = range.start + range.length - 1;
    bool finished = false; // Flag to see if we used the entire range
    for (final convMap in conversionMaps) {
      if (finished) break;
      // Conversion maps are sorted on source range start.

      if (end < convMap.sourceRangeStart) {
        // Entire range is below this convmap
        finishedRanges.add(Range(start, end - start + 1));
        finished = true;
      } else if (start <= convMap.sourceRangeStart &&
          convMap.inSourceRange(end)) {
        // Overlap to the left
        finishedRanges.add(Range(start, convMap.sourceRangeStart - start));
        finishedRanges.add(
            Range(convMap.destRangeStart, end - convMap.sourceRangeStart + 1));
        finished = true;
      } else if (start < convMap.sourceRangeStart &&
          !convMap.inSourceRange(end)) {
        // Overlap both ends

        // Range before
        finishedRanges.add(Range(start, convMap.sourceRangeStart - start));
        // Range inside map
        finishedRanges.add(Range(convMap.destRangeStart, convMap.length));
        // And put back the part to the right
        start = convMap.sourceRangeStart + convMap.length;
      } else if (convMap.inSourceRange(start) && convMap.inSourceRange(end)) {
        // Range is completely inside.
        int offset = convMap.destRangeStart - convMap.sourceRangeStart;
        finishedRanges.add(Range(start + offset, range.length));
        finished = true;
      } else if (convMap.inSourceRange(start) &&
          end > convMap.sourceRangeStart + convMap.length) {
        // Range overlaps to the right
        int offset = convMap.destRangeStart - convMap.sourceRangeStart;
        int length = convMap.sourceRangeStart + convMap.length - start;
        // The part inside the range
        finishedRanges.add(Range(start + offset, length));
        // And then put back the part to the right
        start = convMap.sourceRangeStart + convMap.length;
      }
    }
    if (!finished) {
      // We have a range left that will be unchanged
      finishedRanges.add(Range(start, end - start + 1));
    }
    return finishedRanges;
  }
}

class Range {
  int start;
  int length;
  Range(this.start, this.length);
}
