import '../util/util.dart';

// const String inputFile = 'day20/example.txt';
const String inputFile = 'day20/input.txt';

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

  // Create modules list
  Map<String, Module> modules = {};
  for (final line in lines) {
    final module = Module.from(line);
    modules[module.name] = module;
  }
  // Set the inputs for the conjunction modules
  for (final module in modules.values) {
    for (final dest in module.destinations) {
      final receiverModule = modules[dest];
      if (receiverModule != null) {
        receiverModule.rememberedSignalType[module.name] = SignalType.low;
      }
    }
  }

  const int numberOfTimeToPushButton = 1000;
  List<Signal> signalsQueue = [];
  int lowPulseCount = 0;
  int highPulseCount = 0;
  for (int pressNo = 0; pressNo < numberOfTimeToPushButton; pressNo++) {
    // Push button.
    signalsQueue.add(Signal('broadcaster', 'button', SignalType.low));
    while (signalsQueue.isNotEmpty) {
      final signal = signalsQueue.removeAt(0);
      if (signal.signalType == SignalType.low) {
        lowPulseCount++;
      } else {
        highPulseCount++;
      }
      final receiverModule = modules[signal.destination];
      receiverModule?.handleSignal(signal, signalsQueue);
    }
  }
  return lowPulseCount * highPulseCount;
}

int calcResultP2(String input) {
  final lines = input.split('\n');
  List<String> inputThatNeedsToBeHigh = [];

  // Create modules list
  Map<String, Module> modules = {};
  for (final line in lines) {
    final module = Module.from(line);
    modules[module.name] = module;
    if (module.destinations.contains('vr')) {
      inputThatNeedsToBeHigh.add(module.name);
    }
  }
  // Set the inputs for the conjunction modules
  for (final module in modules.values) {
    for (final dest in module.destinations) {
      final receiverModule = modules[dest];
      if (receiverModule != null) {
        receiverModule.rememberedSignalType[module.name] = SignalType.low;
      }
    }
  }

  List<Signal> signalsQueue = [];
  int pressNo = 0;
  Map<String, int> cycleCountsForHighSignal = {};
  for (final inp in inputThatNeedsToBeHigh) {
    cycleCountsForHighSignal[inp] = 0;
  }

  bool foundCycles = false;

  while (!foundCycles) {
    pressNo++;
    // Push button.
    signalsQueue.add(Signal('broadcaster', 'button', SignalType.low));
    while (signalsQueue.isNotEmpty) {
      final signal = signalsQueue.removeAt(0);
      if (inputThatNeedsToBeHigh.contains(signal.source) &&
          signal.signalType == SignalType.high) {
        print('Module: ${signal.source} sends high after $pressNo cycles');
        cycleCountsForHighSignal[signal.source] = pressNo;
        if (!cycleCountsForHighSignal.values.any((element) => element == 0)) {
          foundCycles = true;
          break;
        }
      }
      final receiverModule = modules[signal.destination];
      receiverModule?.handleSignal(signal, signalsQueue);
    }
  }

  int n = 1;
  for (int i = 0; i < 4; i++) {
    int c = cycleCountsForHighSignal[inputThatNeedsToBeHigh[i]]!;
    assert(isPrime(c) == true);

    n = n * c;
  }
  print(n);
  return 0;
}

class State {
  late String stateStr;
  State(Map<String, Module> modules) {
    stateStr = '';
    for (final module in modules.values) {
      stateStr += module.name;
      stateStr += module.flipFlopState == FlipFlopState.on ? '1' : '0';
      for (final mem in module.rememberedSignalType.values) {
        stateStr += mem == SignalType.high ? '0' : '1';
      }
      stateStr += ' ';
    }
  }

  @override
  operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is State && stateStr == other.stateStr;
  }

  int get hashCode => stateStr.hashCode;
}

int countPushes(Map<String, List<String>> tree, String rootName,
    Map<String, Module> modules) {
  int pushCount = 0;
  final module = modules[rootName];
  if (module == null) {
    // Unregistered. Probably the output
    for (final name in tree[rootName]!) {
      pushCount += countPushes(tree, name, modules);
    }
    return pushCount;
  }
  switch (module.moduleType) {
    case ModuleType.flipflop:
      pushCount = 2 * countPushes(tree, tree[module.name]![0], modules);
    case ModuleType.broadcaster:
      pushCount = 1;
    case ModuleType.conjunction:
      int factor = 1;
      for (final name in module.rememberedSignalType.keys) {
        pushCount += factor * countPushes(tree, name, modules);
        factor++;
      }
  }
  return pushCount;
}

class Signal {
  SignalType signalType;
  String destination;
  String source;
  Signal(this.destination, this.source, this.signalType);
}

enum ModuleType { flipflop, broadcaster, conjunction }

enum SignalType { low, high }

enum FlipFlopState { on, off }

class Module {
  late String name;
  late ModuleType moduleType;
  List<String> destinations = [];

  // Only for conjunction type
  Map<String, SignalType> rememberedSignalType = {};

  // Only for flipflops
  FlipFlopState flipFlopState = FlipFlopState.off;

  Module(this.name, this.moduleType);

  Module.from(String line) {
    final namePart = line.split(' -> ')[0];
    if (namePart == 'broadcaster') {
      name = namePart;
      moduleType = ModuleType.broadcaster;
    } else {
      name = namePart.substring(1);
      if (namePart[0] == '%') {
        moduleType = ModuleType.flipflop;
      } else {
        moduleType = ModuleType.conjunction;
      }
    }
    final destPart = line.split('-> ')[1];
    final destStrs = destPart.split(', ');
    for (final destStr in destStrs) {
      destinations.add(destStr.trim());
    }
  }

  void handleSignal(Signal signal, List<Signal> signalsQueue) {
    switch (moduleType) {
      case ModuleType.broadcaster:
        for (final dest in destinations) {
          signalsQueue.add(Signal(dest, name, signal.signalType));
        }
      case ModuleType.flipflop:
        if (signal.signalType == SignalType.low) {
          // Flipflops only reacts on low signals

          SignalType signalTypeToSend;
          if (flipFlopState == FlipFlopState.off) {
            flipFlopState = FlipFlopState.on;
            signalTypeToSend = SignalType.high;
          } else {
            flipFlopState = FlipFlopState.off;
            signalTypeToSend = SignalType.low;
          }
          for (final dest in destinations) {
            signalsQueue.add(Signal(dest, name, signalTypeToSend));
          }
        }
      case ModuleType.conjunction:
        rememberedSignalType[signal.source] = signal.signalType;

        // If this conjunction module remembers high for all inputs
        // it sends a low signal
        SignalType signalTypeToSend = SignalType.low;
        // But if any remembered input is low it sends a high pulse
        for (final rememberedType in rememberedSignalType.values) {
          if (rememberedType == SignalType.low)
            signalTypeToSend = SignalType.high;
        }
        for (final dest in destinations) {
          signalsQueue.add(Signal(dest, name, signalTypeToSend));
        }
    }
  }
}
