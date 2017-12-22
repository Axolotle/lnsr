from svgwrite import Drawing
from svgwrite.shapes import Line
from svgwrite.container import Group
from svgwrite.animate import AnimateTransform

from random import randint, sample

max_x = 3000
max_y = 1500
longest = 0


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

def generate_lines():
    group = Group()
    duplicated_group = Group(transform='translate(3000)')
    global longest
    current_y = 10
    while current_y < max_y:
        line_quantity = randint(1, 8)
        lengths = [randint(5, 30) for l in range(line_quantity)]
        position = sorted(sample(range(max_x), line_quantity))
        for length, pos in zip(lengths, position):
            if pos + length > longest:
                longest = pos + length
            line = Line((pos, current_y), (pos + length, current_y))
            if pos < 1500:
                duplicated_group.add(line)
            group.add(line)
        current_y += randint(1,5) * 10
    return group, duplicated_group

def generate():
    doc = Drawing('lightSpeed.svg', profile='tiny')
    doc['width'] = str(max_y) + 'px'
    doc['height'] = str(max_y) + 'px'
    doc['viewBox'] = '0 0 {} {}'.format(max_y, max_y)
    main = Group(stroke='black', stroke_width='5px')

    group, duplicated_group = generate_lines()
    main.add(group)
    main.add(duplicated_group)
    anim = AnimateTransform('translate')
    anim.attribs = {
        'type': 'translate',
        'restart': 'always',
        'begin': '0s',
        'from': '0 0',
        'to': '-{} 0'.format(longest),
        'dur': '2.5s',
        'calcMode': 'linear',
        'repeatCount': 'indefinite',
        'attributeName': 'transform'
    }

    main.add(anim)
    doc.add(main)

    return doc.tostring()
    # doc.save(pretty=True)
# doc.save()
