from svgwrite import Drawing
from svgwrite.shapes import Line
from svgwrite.container import Group
from svgwrite.animate import AnimateTransform

from random import randint, sample

max_x = 3000
max_y = 1500
# longest = 0


def simple_gen():
    group = Group()
    duplicated_group = Group(transform='translate(3000)')
    global longest
    current_x = 0
    current_y = 0
    while current_y < max_y:
        while current_x < max_x:
            rand = randint(5, 30) + current_x
            line = Line((current_x, current_y), (rand, current_y))
            if current_x < 1500:
                duplicated_group.add(line)
            if rand > longest: longest = rand
            group.add(line)
            current_x = rand + randint(10, 500)
        current_x = randint(0, 500)
        current_y += 20
    return group, duplicated_group

def lines():
    groups = [Group(), Group()]
    longest = 0
    current_y = 10

    while current_y < max_y:
        line_quantity = randint(1, 8)
        lengths = [randint(5, 30) for l in range(line_quantity)]
        position = sample(range(max_x), line_quantity)
        for length, pos in zip(lengths, position):
            if pos + length > longest:
                longest = pos + length
            line = Line((pos, current_y), (pos + length, current_y))
            if pos < max_x:
                groups[1].add(line)
            groups[0].add(line)
        current_y += randint(1,5) * 10

    groups[1]['transform'] = 'translate({})'.format(longest)
    groups.append(animate(longest, 5))
    container = Group(stroke='black', stroke_width='5px')
    for g in groups:
        container.add(g)
    return container

def parallax_lines():
    groups = [Group() for i in range(3)]
    duplicated_groups = [Group() for i in range(3)]
    longest = [0 for i in range(3)]

    current_y = 10
    while current_y < max_y:
        line_quantity = randint(1, 9)
        lengths = [randint(5, 30) for l in range(line_quantity)]
        position = sample(range(max_x), line_quantity)
        for i, (length, pos) in enumerate(zip(lengths, position)):
            if i % 3 is 0 or i is 0: n = 2
            elif i % 2 is 0: n = 1
            else: n = 0
            if pos + length > longest[n]:
                longest[n] = pos + length
            line = Line((pos, current_y), (pos + length, current_y))
            if pos < max_y:
                duplicated_groups[n].add(line)
            groups[n].add(line)
        current_y += randint(1,5) * 10

    dur = 2
    containers = [Group() for i in range(3)]
    for c, g, dg, l in zip(containers, groups, duplicated_groups, longest):
        c.add(g)
        dg['transform'] = 'translate({})'.format(l)
        c.add(dg)
        c.add(animate(l, dur))
        dur += 0.5
    return containers

def structure():
    param = {
        'profile': 'tiny',
        'size': (str(max_y) + 'px', str(max_y) + 'px'),
        'viewBox': '0 0 {} {}'.format(max_y, max_y),
    }
    doc = Drawing('lightSpeed.svg', **param)
    return doc

def animate(longest, dur):
    anim = AnimateTransform('translate')
    anim.attribs = {
        'type': 'translate',
        'restart': 'always',
        'begin': '0s',
        'from': '0 0',
        'to': '-{} 0'.format(longest),
        'dur': '{}s'.format(dur),
        'calcMode': 'linear',
        'repeatCount': 'indefinite',
        'attributeName': 'transform'
    }
    return anim

def generate():
    doc = structure()
    doc.add(lines())
    return doc.tostring()
    # doc.save(pretty=True)

def generate_parallax():
    doc = structure()
    main = Group(stroke='#323232', stroke_width='5px')
    for g in parallax_lines():
        main.add(g)
    doc.add(main)

    return '<?xml version="1.0"?>' + doc.tostring()
    # doc.save(pretty=True)
