from random import randint, sample

from svgwrite import Drawing
from svgwrite.shapes import Line
from svgwrite.container import Group
from svgwrite.animate import AnimateTransform

from .data import bg_anim_data as anim, bg_img_data as img


def get_background_anim():
    document = get_SVG_document(anim['width'], anim['height'],
        anim['viewBox'], anim['unitType'])
    for group in get_parallax_lines():
        document.add(group)

    return document.tostring()

def get_background_img():
    document = get_SVG_document(img['width'], img['height'],
        img['viewBox'], img['unitType'])
    document.add(get_lines())

    return document.tostring()

def get_SVG_document(width, height, viewBox, unitType):
    return Drawing(
        'lightSpeed.svg',
        size=(str(width) + unitType, str(height) + unitType),
        viewBox=viewBox,
        profile='tiny',
    )

def get_lines():
    group = Group(**img['style'])

    current_y = 6
    current_x = randint(-10 , 150)

    for y in range(0, img['verticalLines']):
        while current_x < img['width']:
            rand_x = randint(2, 6) + current_x
            line = Line((current_x, current_y), (rand_x, current_y))
            group.add(line)
            current_x = rand_x + randint(50, 150)
        current_x = randint(-10, 150)
        current_y = round(current_y + img['verticalInterval'], 1)

    return group

def get_parallax_lines():
    groups = [Group() for i in range(3)]
    duplicated_groups = [Group() for i in range(3)]
    longest = [0 for i in range(3)]

    current_y = anim['verticalInterval']
    while current_y < anim['height']:
        line_quantity = randint(1, 9)
        lengths = [randint(5, 30) for l in range(line_quantity)]
        position = sample(range(anim['width'] * 2), line_quantity)
        for i, (length, pos) in enumerate(zip(lengths, position)):
            if i % 3 is 0 or i is 0: n = 2
            elif i % 2 is 0: n = 1
            else: n = 0
            if pos + length > longest[n]:
                longest[n] = pos + length
            line = Line((pos, current_y), (pos + length, current_y))
            if pos < anim['height']:
                duplicated_groups[n].add(line)
            groups[n].add(line)
        current_y += randint(1,5) * anim['verticalInterval']

    dur = 2
    containers = [Group(**anim['style']) for i in range(3)]
    for c, g, dg, l in zip(containers, groups, duplicated_groups, longest):
        c.add(g)
        dg['transform'] = 'translate({}, 0)'.format(l)
        c.add(dg)
        c.add(animate(l, dur))
        dur += 0.5

    return containers

def animate(longest, dur):
    animation = AnimateTransform('translate')
    animation.attribs = { **anim['animationAttributes'] }
    animation.attribs['to'] = '-{} 0'.format(longest)
    animation.attribs['dur'] = '{}s'.format(dur)

    return animation
