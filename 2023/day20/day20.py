""" filesystem paths module """
from pathlib import Path
from math import lcm


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n')
    # print(c)
    return c


class Signal():
    def __init__(self, value: int, source: str, target: str) -> None:
        self.value = value
        self.source = source
        self.target = target

    def __str__(self) -> str:
        return f'{self.value} from {self.source} to {self.target}'


class Module():
    def __init__(self, definition: str) -> None:
        name, t = definition.split(' -> ')
        targets = t.split(', ')
        if name == 'broadcaster':
            self.name = name
            self.module_type = 'b'
        else:
            self.name = name[1:]
            self.module_type = name[0]
        self.targets = targets
        self.value = False
        self.inputs = {}


    def __str__(self) -> str:
        if self.module_type == '&':
            return f'{self.name} of {self.module_type} with targets {[t for t in self.targets]} and inputs {self.inputs}'
        else:
            return f'{self.name} of {self.module_type} with targets {[t for t in self.targets]}'


    def add_input(self, input: str):
        """ Add a new input to the module with 0 as last value """
        if self.module_type != '&':
            raise Exception('Inputs only supported for conjunction modules')
        self.inputs[input] = 0


    def process(self, signal: Signal, i: int, part2: bool, zh_incoming: dict[str, int]):
        signals = []

        if part2 and self.name == 'zh' and signal.value == 1:
            if not zh_incoming.__contains__(signal.source):
                zh_incoming[signal.source] = i
            if len(zh_incoming) == len(self.inputs):
                res = 1
                for v in zh_incoming.values():
                    res = lcm(res, v)
                print(res)
                exit()
        if self.module_type == 'b':
            for target in self.targets:
                signals.append(Signal(signal.value, self.name, target))
        elif self.module_type == '%':
            # process low pulse and do nothing for high pulse
            if signal.value == 0:
                # flip state
                self.value = 1 if self.value == 0 else 0
                for target in self.targets:
                    signals.append(Signal(self.value, self.name, target))
        elif self.module_type == '&':
            # update memory for input
            self.inputs[signal.source] = signal.value
            signal_to_send = 1
            # if all inputs are remembered as high, send low
            if all(value == 1 for value in self.inputs.values()):
                signal_to_send = 0
            for target in self.targets:
                signals.append(Signal(signal_to_send, self.name, target))

        return signals



def push_button_and_process(modules: dict[str, Module], i: int, part2: bool, zh_incoming) -> list[Signal]:
    signals_processed = []
    signals_queue = [Signal(0, 'button', 'broadcaster')]


    while len(signals_queue) > 0:
        signal = signals_queue.pop(0)
        if modules.__contains__(signal.target):
            module = modules[signal.target]
            signals_queue.extend(module.process(signal, i, part2, zh_incoming))
        signals_processed.append(signal)

    return signals_processed


def load_modules():
    data = load_data('input')
    modules: dict[str,Module] = {} 
    for d in data:
        module = Module(d)
        modules[module.name] = module
    # find all inputs for conjunction modules
    for m in modules:
        module = modules[m]
        for target in module.targets:
            if modules.__contains__(target) and modules[target].module_type == '&':
                modules[target].add_input(module.name)
    return modules

if __name__ == '__main__':

    modules = load_modules()

    print('Part one:')
    signales_processed: list[Signal] = []
    for i in range(1,1001):
        signales_processed.extend(push_button_and_process(modules, i ,False, None))
    low: int = 0
    high: int = 0
    for signal in signales_processed:
        if signal.value == 0:
            low += 1
        if signal.value == 1:
            high += 1
    print(f'{low*high}')

    print('Part two:')
    modules = load_modules()
    iteration: int = 1
    # dict for part 2 to store incoming signal button count for zh
    zh_incoming = {}
    # Iterate until solution is found which will print the result and stop the program
    while True:
        push_button_and_process(modules, iteration, True, zh_incoming)
        iteration += 1

