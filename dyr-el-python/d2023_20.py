from aoc_prepare import PrepareAoc

from position import Pos2D
from collections import namedtuple, deque, Counter
from prio_queue import PrioQueue

class Machine:
    def __init__(self, name):
        self._name = name
        self._receivers = list()
        self._inputs = list()
    @property
    def name(self):
        return self._name
    def add_receiver(self, receiver):
        self._receivers.append(receiver)
    def add_input(self, sender):
        self._inputs.append(sender)
    @property
    def receivers(self):
        return self._receivers
    @property
    def senders(self):
        return self._inputs

class FlipFlop(Machine):
    def __init__(self, name):
        super().__init__(name)
        self._status = 0
    @property
    def status(self):
        return self._status
    def receive(self, signal):
        if signal == 0:
            self._status = 1 - self.status
            return self.receivers, self.status
        else:
            return [], self.status
    def __str__(self):
        if self.status == 1:
            return f"%{self.name}+"
        return f"%{self.name}-"
    def __repr__(self):
        return f"%{self.name}{self.status}"

class Conjuncion(Machine):
    def __init__(self, name):
        super().__init__(name)
    def receive(self, _):
        return self._receivers, self.status
    def __str__(self):
        return f"&{self.name}"
    def __repr__(self):
        return f"&{self.name}"
    @property
    def status(self):
        if all((input.status == 1 for input in self._inputs)):
            return 0
        return 1

class Source(Machine):
    def __init__(self, name):
        super().__init__(name)
    def receive(self, signal):
        return self.receivers, signal
    def __str__(self):
        return self.name
    def __repr__(self):
        return f"{self.name}->"

class Sink(Machine):
    def __init__(self, name):
        super().__init__(name)
        self._output = 0
    def receive(self, signal):
        if signal == 0:
            self._output = 1
        return [], 0
    @property
    def output(self):
        return self._output
    def __str__(self):
        return self.name
    def __repr__(self):
        return f"->{self.name}"


def parse(inp):
    source_types = {'%': FlipFlop, '&': Conjuncion}
    modules = dict()
    destinations = dict()
    for line in inp.splitlines():
        source, dests = line.split(' -> ')
        if source[0] in source_types:
            source_type = source_types[source[0]]
            source_name = source[1:]
        else:
            source_type = Source
            source_name = source
        modules[source_name] = source_type(source_name)
        if source_name not in destinations:
            destinations[source_name] = list()
        for dest in dests.split(', '):
            destinations[source_name].append(dest)
    for name, dests in destinations.items():
        for dest in dests:
            if dest not in modules:
                modules[dest] = Sink(dest)
            modules[name].add_receiver(modules[dest])
            modules[dest].add_input(modules[name])
    return modules


def part1(inp):
    modules = parse(inp)
    count = {0: 0, 1: 0}
    for i in range(1000):
        start_module = modules["broadcaster"]
        start_signal = 0
        q = deque([(start_module, start_signal)])
        while q:
            receiver, signal = q.popleft()
            count[signal] += 1
            receivers, signal = receiver.receive(signal)
            for r in receivers:
                q.append((r, signal))
    return count[0] * count[1]


from functools import reduce
from operator import mul
def part2(inp):
    modules = parse(inp)
    button_presses = 0
    cycles = {"kr": 0, "zb": 0, "sm": 0, "xd": 0}
    while True:
        button_presses += 1
        start_module = modules["broadcaster"]
        start_signal = 0
        q = deque([(start_module, start_signal)])
        while q:
            receiver, signal = q.popleft()
            receivers, signal = receiver.receive(signal)
            for r in receivers:
                q.append((r, signal))
        for module in cycles:
            if modules[module].status != button_presses % 2 and cycles[module] == 0:
                cycles[module] = button_presses
                if all((val > 0 for val in cycles.values())):
                    return reduce(mul, cycles.values())
        if modules["rx"].output == 1:
            break
    return button_presses


def test_1_1():
    assert 32000000 == part1("""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""")

def test_1_2():
    assert 11687500 == part1("""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""")


def test_1_2():
    pass


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 20)
    main(prep.get_content())