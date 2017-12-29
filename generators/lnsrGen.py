from svgwrite import Drawing
from svgwrite.shapes import Polyline
from svgwrite.container import Group

class Ruler:
    def __init__(self):
        self.w = 2.25
        self.space = 1.75
        # Generate base points's position for each characters
        self.chars = self.convert_characters()
        # Generate
        self.total = self.get_nbmax_str()

    def generate(self, n):
        doc = Drawing('lnsr.svg', profile='tiny',
                      size=('500px', '500px'), viewBox='0 0 500 500')
        text, length = self.get_number_str(n)
        total = self.total
        total['transform'] = 'translate({})'.format(length)
        text.add(total)
        doc.add(text)

        return doc

    def draw(self, n):
        return self.generate(n).tostring()

    def generate_file(self, n):
        return self.generate(n).save(pretty=True)

    def get_polyline(self, char, x):
        polyline = Polyline()
        for point in self.chars[char]:
            polyline.points.append((point[0] + x, point[1]))

        return polyline

    def get_number_str(self, n):
        x = 0
        text = str(n)
        text = [text[i-3:i] or text[i-2:i] or text[i-1:i]
                for i in range(len(text), -1, -3)]

        formated = Group(
            fill='none',
            stroke='black',
            stroke_width=str(self.w) + 'px',
            stroke_linecap='round',
            stroke_linejoin='round',
            #stroke_miterlimit=str(w),
        )

        for group in reversed(text):
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

    def convert_characters(self):
        # Convert a grid like object into x,y positions
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
            trad = chars[char].replace('a', '1').replace('b', '2').replace('c', '3')
            trad = [list(trad[i:i+2]) for i in range(0, len(trad), 2)]
            chars[char] = [(int(pos[0]) * self.w, (int(pos[1]) + 1) * self.w)
                            for pos in trad]

        return chars

ruler = Ruler()

ruler.generate_file(31557600000000000)
