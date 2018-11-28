from json import loads
from random import randint, sample

from svgwrite import Drawing
from svgwrite.shapes import Line
from svgwrite.container import Group
from svgwrite.animate import AnimateTransform

class BackgroundGenerator:
    def __init__(self):
        with open('generators/backgroundData.json', 'r') as data:
            self.data = loads(data.read())

        for type in ['image', 'animation']:
            self.data[type]['verticalLines'] = round(self.data[type]['height'] / self.data[type]['verticalInterval'])
            self.data[type]['viewBox'] = '0 0 {} {}'.format(self.data[type]['width'], self.data[type]['height'])

    def generate_object(self, docType):
        document = self.get_SVG_document(docType)
        if docType is 'image':
            document.add(self.get_lines())
        else:
            for group in self.get_parallax():
                document.add(group)

        return document

    def generate_string(self, docType):
        return self.generate_object(docType).tostring()

    def get_SVG_document(self, docType):
        config = self.data[docType]
        return Drawing(
            'lightSpeed.svg',
            size=(str(config['width']) + config['unitType'],
                  str(config['height']) + config['unitType']),
            viewBox=config['viewBox'],
            profile='tiny',
        )

    def get_lines(self):
        config = self.data['image']
        group = Group(**config['style'])

        currentY = 6
        currentX = randint(-10 , 150)

        for y in range(0, config['verticalLines']):
            while currentX < config['width']:
                randX = randint(2, 6) + currentX
                line = Line((currentX, currentY), (randX, currentY))
                group.add(line)
                currentX = randX + randint(50, 150)
            currentX = randint(-10, 150)
            currentY = round(currentY + config['verticalInterval'], 1)

        return group

    def get_parallax(self):
        config = self.data['animation']

        groups = [Group() for i in range(3)]
        duplicated_groups = [Group() for i in range(3)]
        longest = [0 for i in range(3)]

        current_y = config['verticalInterval']
        while current_y < config['height']:
            line_quantity = randint(1, 9)
            lengths = [randint(5, 30) for l in range(line_quantity)]
            position = sample(range(config['width'] * 2), line_quantity)
            for i, (length, pos) in enumerate(zip(lengths, position)):
                if i % 3 is 0 or i is 0: n = 2
                elif i % 2 is 0: n = 1
                else: n = 0
                if pos + length > longest[n]:
                    longest[n] = pos + length
                line = Line((pos, current_y), (pos + length, current_y))
                if pos < config['height']:
                    duplicated_groups[n].add(line)
                groups[n].add(line)
            current_y += randint(1,5) * config['verticalInterval']

        dur = 2
        containers = [Group(**config['style']) for i in range(3)]
        for c, g, dg, l in zip(containers, groups, duplicated_groups, longest):
            c.add(g)
            dg['transform'] = 'translate({}, 0)'.format(l)
            c.add(dg)
            c.add(self.animate(l, dur))
            dur += 0.5
        return containers

    def animate(self, longest, dur):
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

background = BackgroundGenerator()
