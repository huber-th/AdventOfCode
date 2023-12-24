""" filesystem paths module """
from pathlib import Path
import sympy.geometry as gm
from itertools import combinations


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        lines = f.read().strip().split('\n')
        data = []
        for l in lines:
            point, velocity = l.split(' @ ')
            px,py,pz = point.replace(' ','').split(',')
            vx,vy,vz = velocity.replace(' ','').split(',')
            data.append(((int(px),int(py),int(pz)),(int(vx),int(vy),int(vz))))
    return data


if __name__ == '__main__':
    data = load_data('input')
    min_area = 200000000000000
    max_area = 400000000000000
    # print(data)

    combos = list(combinations(data, 2))
    print('Part one:')
    res = 0
    for c in combos:
        ax = c[0][0][0]
        ay = c[0][0][1]
        avx = c[0][1][0]
        avy = c[0][1][1]
        bx = c[1][0][0]
        by = c[1][0][1]
        bvx = c[1][1][0]
        bvy = c[1][1][1]
        line1=gm.Line(gm.Point(ax,ay),gm.Point((ax+avx, ay+avy)))
        line2=gm.Line(gm.Point(bx,by),gm.Point((bx+bvx, by+bvy)))
        intersection=line1.intersection(line2)
        if len(intersection) > 0:
            ix = intersection[0].evalf().x
            iy = intersection[0].evalf().y
            if (ix >= min_area and ix <= max_area and 
                iy >= min_area and iy <= max_area):
                axf = ayf = bxf = byf = False
                if ix < ax and avx < 0 or ix >= ax and avx >= 0:
                    axf = True
                if iy < ay and avy < 0 or iy >= ay and avy >= 0:
                    ayf = True
                if ix < bx and bvx < 0 or ix >= bx and bvx >= 0:
                    bxf = True
                if iy < by and bvy < 0 or iy >= by and bvy >= 0:
                    byf = True
                if axf and ayf and bxf and byf:
                    res += 1
    print(res)

    print('Part two:')
