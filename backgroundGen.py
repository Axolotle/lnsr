from svgwrite import Drawing
from svgwrite.shapes import Line
from svgwrite.container import Group

from random import random, uniform, randint

doc = Drawing('lightSpeed.svg', profile='tiny')
group = Group(stroke='black')
current_x = 0
current_y = 0
max_x = 2000
max_y = 1000
while current_y < max_y:
    while current_x < max_x:
        print(current_x)
        rand = randint(5, 30) + current_x
        group.add(Line((current_x, current_y), (rand, current_y)))
        current_x = rand + randint(10, 500)
    current_x = randint(0, 500)
    current_y += 20

doc.add(group)
doc.save(pretty=True)
