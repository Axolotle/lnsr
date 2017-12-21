from svgwrite import Drawing
from svgwrite.shapes import Line
from svgwrite.container import Group

from random import random, uniform, randint, sample

max_x = 1500
max_y = 1500

doc = Drawing('lightSpeed.svg', profile='tiny')
doc['width'] = str(max_x) + 'px'
doc['height'] = str(max_y) + 'px'
group = Group(stroke='black', stroke_width='3px')

def simple_gen():
    current_x = 0
    current_y = 0
    while current_y < max_y:
        while current_x < max_x:
            print(current_x)
            rand = randint(5, 30) + current_x
            group.add(Line((current_x, current_y), (rand, current_y)))
            current_x = rand + randint(10, 500)
        current_x = randint(0, 500)
        current_y += 20
    return group

def test():
    current_x = 0
    current_y = 10
    while current_y < max_y:
        line_quantity = randint(1, 8)
        lines_len = [randint(5, 30) for l in range(line_quantity)]
        position = sorted(sample(range(max_x), line_quantity))
        for line, pos in zip(lines_len, position):
            group.add(Line((pos, current_y), (pos + line, current_y)))
        current_y += randint(1,5) * 10



test()
doc.add(group)
doc.save(pretty=True)
