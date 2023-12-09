from pathlib import Path

p = Path(__file__).with_name('input')
with p.open('r') as f:
    c = f.read().strip()
    print(c)
    
    print('Part one:')

    print('Part two:')