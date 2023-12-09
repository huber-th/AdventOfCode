from pathlib import Path

seeds = []
seed_to_soil = []
soil_to_fertilizer = []
fertilizer_to_water = []
water_to_light = []
light_to_temperature = []
temperature_to_humidity = []
humidity_to_location = []

def get_values(input):
    input = input.split('\n')
    input.pop(0)
    values = []
    for i in input:
        values.append(list(map(int, i.split(' '))))
    return values

p = Path(__file__).with_name('input')
with p.open('r') as f:
    s, sts, stf, ftw, wtl,ltt, tth, htl = f.read().split('\n\n')
    seeds = list(map(int, s.split(':')[1].strip().split(' ')))
    seed_to_soil = get_values(sts)
    soil_to_fertilizer = get_values(stf)
    fertilizer_to_water = get_values(ftw)
    water_to_light = get_values(wtl)
    light_to_temperature = get_values(ltt)
    temperature_to_humidity = get_values(tth)
    humidity_to_location = get_values(htl)


def mapped_value(input, needle) -> int:
    value = needle
    for e in input:
        if needle < e[1]:
            continue
        if needle > e[1] + e[2] - 1:
            continue
        value = e[0] + needle - e[1]
    return value

def find_location(seed: int) -> int | None:
    soil = mapped_value(seed_to_soil, seed)
    fertilizer = mapped_value(soil_to_fertilizer, soil)
    water = mapped_value(fertilizer_to_water, fertilizer)
    light = mapped_value(water_to_light, water)
    temperature = mapped_value(light_to_temperature, light)
    humidity = mapped_value(temperature_to_humidity, temperature)
    location = mapped_value(humidity_to_location, humidity)

    return location

print('Part one:')
min_location: int | None = None
for seed in seeds:
    location = find_location(seed)
    if min_location is None:
        min_location = location
    elif location is not None and location < min_location:
        min_location = location 
print(min_location)

print('Part two:')
min_location = None
min_seed = 0
for i,j in zip(seeds[0::2], seeds[1::2]):
    print('processing seeds {}...{}'.format(i,i+j))
    for s in range(i,i+j,1000):
        location = find_location(s)
        if min_location is None:
            min_location = location
            min_seed = s
        elif location is not None and location < min_location:
            min_location = location 
            min_seed = s
print('min_location for sampling is {} for seed {}'.format(min_location,min_seed))
min_location = None
for s in range(min_seed - 500, min_seed + 500):
    location = find_location(s)
    if min_location is None:
        min_location = location
        min_seed = s
    elif location is not None and location < min_location:
        min_location = location 
        min_seed = s
print('min_location overall is {}'.format(min_location))
