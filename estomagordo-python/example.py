from dataclasses import dataclass


@dataclass
class A:
    b: 'B'
    foo: str

    def __str__(self):
        return f'b: {self.b} foo: {self.foo}'


@dataclass
class B:
    bar: str

    def __str__(self):
        return f'bar: {self.bar}'