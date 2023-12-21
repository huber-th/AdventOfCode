""" filesystem paths module """
from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n')
    print(c)
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


    def process(self, signal: Signal):
        # print(f'{self.name} received {signal}')
        signals = []

        if self.module_type == 'b':
            for target in self.targets:
                print(f'{signal} is forwarded to {target}')
                signals.append(Signal(signal.value, self.name, target))
        elif self.module_type == '%':
            # process low pulse and do nothing for high pulse
            if signal.value == 0:
                # flip state
                self.value = 1 if self.value == 0 else 0
                # print(f'{self.name} changed state to {self.value} because of signal {signal.value} from {signal.source}')
                for target in self.targets:
                    print(f'{self.name} sends {self.value} to {target}')
                    signals.append(Signal(self.value, self.name, target))
            # else:
            #     print(f'{self.name} ignores {signal}')
        elif self.module_type == '&':
            # update memory for input
            self.inputs[signal.source] = signal.value
            signal_to_send = 1
            # if all inputs are remembered as high, send low
            if all(value == 1 for value in self.inputs.values()):
                signal_to_send = 0
            for target in self.targets:
                print(f'{self.name} sends {signal_to_send} to {target}')
                signals.append(Signal(signal_to_send, self.name, target))

        return signals



def push_button_and_process(modules: dict[str, Module]) -> list[Signal]:
    signals_processed = []
    signals_queue = [Signal(0, 'button', 'broadcaster')]

    print(signals_queue[0])
    while len(signals_queue) > 0:
        signal = signals_queue.pop(0)
        # print(f'processing signal {signal}')
        if modules.__contains__(signal.target):
            module = modules[signal.target]
            signals_queue.extend(module.process(signal))
        signals_processed.append(signal)

    return signals_processed


if __name__ == '__main__':
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

    print(str.join("\n",[str(modules[m]) for m in modules]))


    print('Part one:')
    signales_processed: list[Signal] = []
    for i in range(1,1001):
        print(f'--- button {i} ---')
        signales_processed.extend(push_button_and_process(modules))
    low: int = 0
    high: int = 0
    for signal in signales_processed:
        if signal.value == 0:
            low += 1
        if signal.value == 1:
            high += 1
    print(f'low: {low}')
    print(f'high: {high}')
    print(f'answer: {low*high}')

    print('Part two:')
