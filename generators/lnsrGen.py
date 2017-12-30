from svgwrite import Drawing
from svgwrite.shapes import Polyline, Polygon, Rect
from svgwrite.path import Path
from svgwrite.container import Group
# from svgpathtools import Path, Line as Path_tool, Line

class Ruler:
    def __init__(self):
        self.w = 2.25
        self.space = 1.75
        self.dpi = 72
        self.px = self.dpi / 25.4
        # Generate base points's position for each characters
        self.chars = self.convert_characters()
        # Generate the ruler's shape
        self.shape = self.get_ruler_shape()
        # Generate the ruler's total number string
        self.total = self.get_nbmax_str()

    def generate(self, n):
        doc = Drawing('lnsr.svg', profile='tiny',
                      size=('900px', '95px'), viewBox='0 0 900 95')
        main = Group(fill='none', stroke='black', stroke_linejoin='round',
                     stroke_width=str(self.w) + 'px', stroke_linecap='round')

        number, length = self.get_number_str(n)
        number['transform'] = 'translate({},{})'.format(
            13 * self.px, 22.5 * self.px - 2 * self.w)

        total = self.total
        total['transform'] = 'translate({})'.format(length)
        number.add(total)

        main.add(number)
        main.add(self.shape)
        main['transform'] = 'translate({},{})'.format(1.125, 1.125)
        doc.add(main)

        return doc

    def test(self, n):
        doc = Drawing('lnsrTest.svg', profile='tiny',
                      size=('200px', '200px'), viewBox='0 0 50 50')
        main = Group(fill='none', stroke='black', stroke_linejoin='round',
                     stroke_width=str(self.w) + 'px', stroke_linecap='round')

        main.add(self.get_path(n, 0))
        main['transform'] = 'translate({},{})'.format(10, 10)
        doc.add(main)

        return doc

    def draw(self, n):
        return self.generate(n).tostring()

    def generate_file(self, n):
        return self.test(n).save(pretty=True)

    def get_polyline(self, char, x):
        polyline = Polyline()
        for point in self.chars[char]:
            polyline.points.append((point[0] + x, point[1]))
        return polyline

    def get_path(self, char, x):
        points = self.chars[str(char)]
        a, b = points.pop(0)
        d = 'M{},{}L'.format(a + x, b)
        for p in points:
            a, b = p
            d += '{},{} '.format(a + x, b)

        return Path(d=d)

    def get_number_str(self, n):
        x = 0
        text = str(n)
        remove = len(text) % 3
        sequence = []
        if remove is not 0:
            sequence.append(text[0:remove])
        sequence += [text[i:i+3] for i in range(remove, len(text), 3)]

        formated = Group()
        for group in sequence:
            for char in group:
                formated.add(self.get_polyline(char, x))
                x += self.w * 3 + self.space
            x += self.w * 2 + (self.w - self.space)

        return formated, x - self.w

    def get_nbmax_str(self):
        x = 0
        text = '/31 557 600 000 000 000 lns'

        formated = Group()
        for char in text:
            if char is not ' ':
                formated.add(self.get_polyline(char, x))
                if char is '/': x += self.w * 5
                elif char is 'l': x += self.w * 3
                else: x += self.w * 4
            else: x += self.w * 2

        return formated

    def get_ruler_shape(self):
        px = self.px
        width = 299.792458 * px
        margin = 5 * px
        height = 30 * px

        points = [
            (0,0), (width, 0),
            (width, 10.5 * px), (width + margin, 7.5 * px),
            (width + margin, 22.5 * px), (width, 19.5 * px),
            (width, height), (0, height),
            (0, 19.5 * px), (margin, 22.5 * px),
            (margin, 7.5 * px), (0, 10.5 * px)
        ]

        return Polygon(points=points)

    def convert_characters(self):
        # Convert a grid like object into x,y positions

        def get_pos(pos):
            pos = [int(p) * self.w for p in pos]
            pos = [round(p) if round(p) == p else p for p in pos ]
            return pos

        chars = {
            '0': 'b4a3a1b0c1c3b4',
            '1': 'c4a4b4b0a1',
            '2': 'c4a4a3c1b0a0',
            '3': 'a4b4c3b2c1b0a0',
            '4': 'c0c4c3b3a2a1',
            '5': 'a4b4c3a1a0c0',
            '6': 'b0a1a3b4c3b2a3',
            '7': 'b4b2c1c0a0',
            '8': 'b4a3c1b0a1c3b4',
            '9': 'c4c1b0a1b2',
            '/': 'a4b3b1c0',
            'l': 'b4a3a0',
            'n': 'a4a2b2c3c4',
            's': 'a4b4b2c2'
        }

        for char in chars:
            trad = chars[char].replace('a', '0').replace('b', '1').replace('c', '2')
            trad = [trad[i:i+2] for i in range(0, len(trad), 2)]
            chars[char] = [get_pos(elem) for elem in trad]

        return chars

ruler = Ruler()

ruler.generate_file(1)
