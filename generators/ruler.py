from json import loads

from svgwrite import Drawing
from svgwrite.path import Path
from svgwrite.container import Group

from .helpers import number_to_string
from .data import ruler_data as data


class RulerGenerator:
    def __init__(self):
        self.width = data['width']
        self.height = data['height']

        self.glyph_width = data['glyphWidth']
        self.inner_space = data['glyphInnerSpaceWidth']
        self.space = self.glyph_width - self.inner_space
        self.slash_space = data['glyphSlashSpace']

        self.styles = data['styles']
        self.ruler_outline = data['rulerOutline']
        self.ruler_total = data['rulerTotal']
        self.glyphs = data['glyphs']

    def generate_object(self, specimen_number, doc_type):
        style = self.styles[doc_type]
        width = round(self.width + style['margin'] * 2, 7)
        height = round(self.height + style['margin'] * 2, 7)

        document = self.get_SVG_document(specimen_number, width, height)
        elements = Group()
        elements['transform'] = 'translate({}, {})'.format(style['margin'], style['margin'])
        document.add(elements)

        outline = self.get_path(self.ruler_outline, 0, style=style['outlineStyle'])
        elements.add(outline)

        text = number_to_string(specimen_number) + self.ruler_total
        text = self.text_to_paths(text, style['numbersPathType'], style['numbersStyle'])
        text['transform'] = 'translate(12.5, 20.5)'
        elements.add(text)

        return document

    def generate_string(self, specimen_number, doc_type):
        return self.generate_object(specimen_number, doc_type).tostring()

    def generate_file(self, specimen_number, doc_type, folder):
        filename = '{}light-nanosecond_ruler{}.svg'.format(folder, specimen_number)
        return self.generate_object(specimen_number, doc_type).saveas(filename)

    def get_SVG_document(self, specimen_number, width, height):
        return Drawing(
            'light-nanosecond_ruler{}.svg'.format(specimen_number),
            size=(str(width) + 'mm', str(height) + 'mm'),
            viewBox='0 0 {} {}'.format(width, height),
            profile='tiny',
        )

    def get_path(self, points, translate_x, style={}):
        parts = ['M {}{}'.format(round(start_x + translate_x, 7), rest)
                 for start_x, rest in points]
        return Path(d=' '.join(parts), **style)


    def text_to_paths(self, text, path_type, style, translate_x=0):
        glyphs = self.glyphs[path_type]
        glyphs_paths = Group(**style)
        text_len = len(text) - 1

        for i, glyph in enumerate(text):
            if glyph is not ' ':
                glyphs_paths.add(self.get_path(glyphs[glyph], round(translate_x, 2)))
                if glyph is '/' or (i+1 <= text_len and text[i+1] is '/'):
                    translate_x += self.glyph_width + self.slash_space
                elif glyph is 'l':
                    translate_x += 1.6 + self.inner_space
                else:
                    translate_x += self.glyph_width + self.inner_space
            else:
                translate_x += self.space

        return glyphs_paths


ruler = RulerGenerator()
