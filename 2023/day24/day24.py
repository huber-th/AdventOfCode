""" filesystem paths module """
from pathlib import Path
from sympy import symbols, solve, geometry
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
        line1=geometry.Line(geometry.Point(ax,ay),geometry.Point((ax+avx, ay+avy)))
        line2=geometry.Line(geometry.Point(bx,by),geometry.Point((bx+bvx, by+bvy)))
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
    hails = data[:3]

    X1,V1 = hails[0]
    X2,V2 = hails[1]
    X3,V3 = hails[2]

    x1, y1, z1 = X1
    x2, y2, z2 = X2
    x3, y3, z3 = X3

    vx1, vy1, vz1 = V1
    vx2, vy2, vz2 = V2
    vx3, vy3, vz3 = V3

    x = symbols('x')
    y = symbols('y')
    z = symbols('z')
    vx = symbols('vx')
    vy = symbols('vy')
    vz = symbols('vz')

    equations = [
        (y1-y)*(vz1-vz)-(z1-z)*(vy1-vy),
        (z1-z)*(vx1-vx)-(x1-x)*(vz1-vz),
        (x1-x)*(vy1-vy)-(y1-y)*(vx1-vx),
        (y2-y)*(vz2-vz)-(z2-z)*(vy2-vy),
        (z2-z)*(vx2-vx)-(x2-x)*(vz2-vz),
        (x2-x)*(vy2-vy)-(y2-y)*(vx2-vx),
        (y3-y)*(vz3-vz)-(z3-z)*(vy3-vy),
        (z3-z)*(vx3-vx)-(x3-x)*(vz3-vz),
        (x3-x)*(vy3-vy)-(y3-y)*(vx3-vx)
    ]

    solution = solve(equations, [x, y, z, vx, vy, vz], dict=True)[0]
    print(solution[x] + solution[y] + solution[z])
