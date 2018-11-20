from svgwrite import Drawing
from svgwrite.path import Path
from svgwrite.container import Group
from json import loads, dumps
from urllib.parse import quote_plus
from math import ceil
from time import strftime


class RulerGenerator:
    def __init__(self):
        with open('generators/svgData.json', 'r') as data:
            data = loads(data.read())
            self.margin = [data['marginX'], data['marginY']]
            self.width = round(data['width'] + self.margin[0] * 2, 7)
            self.height = round(data['height'] + self.margin[1] * 2, 7)
            self.viewBox = '0 0 {} {}'.format(self.width, self.height)

            self.glyphW = data['glyphWidth']
            self.glyphInnerSpaceW = data['glyphInnerSpaceWidth']
            self.spaceW = self.glyphW - self.glyphInnerSpaceW
            self.glyphSlashSpace = data['glyphSlashSpace']

            self.styles = data['styles']
            self.rulerOutline = data['rulerOutline']
            self.rulerTotal = data['rulerTotal']
            self.glyphs = data['glyphs']

    def generate_file(self, specimenNumber,
                      docType='screen', pathType='stroked'):
        document = self.getSVGDocument(specimenNumber)
        elements = Group()
        elements['transform'] = 'translate({}, {})'.format(*self.margin)
        document.add(elements)

        outline = self.getPath(self.rulerOutline, 0, style=self.styles[docType]['rulerOutline'])
        elements.add(outline)

        text = self.numberToString(specimenNumber) + self.rulerTotal
        text = self.textToPaths(text, docType=docType, pathType=pathType)
        text['transform'] = 'translate(12.5, 20.5)'
        elements.add(text)

        # document.save(pretty=True)
        return '<?xml version="1.0" encoding="UTF-8"?>' + document.tostring()

    def getSVGDocument(self, specimenNumber):
        return Drawing(
            'light-nanosecond_ruler{}.svg'.format(specimenNumber),
            size=(str(self.width) + 'mm', str(self.height) + 'mm'),
            viewBox=self.viewBox,
            profile='tiny',
        )

    def getPath(self, points, xTranslation, style={}):
        parts = ['M {}{}'.format(round(startXPoint + xTranslation, 7), rest)
                 for startXPoint, rest in points]
        return Path(d=' '.join(parts), **style)

    def numberToString(self, specimenNumber):
        text = str(specimenNumber)
        splittedText = [text[(i-3 if i-3 > 0 else 0):i]
                        for i in range(len(text), -1, -3)]
        return ' '.join(reversed(splittedText))

    def textToPaths(self, text, xTranslation=0, docType='screen', pathType='stroked'):
        glyphs = self.glyphs[pathType]
        glyphsPaths = Group(**self.styles[docType][pathType])
        textLen = len(text) - 1

        for i, glyph in enumerate(text):
            if glyph is not ' ':
                glyphsPaths.add(self.getPath(glyphs[glyph], round(xTranslation, 2)))
                if glyph is '/' or (i+1 <= textLen and text[i+1] is '/'):
                    xTranslation += self.glyphW + self.glyphSlashSpace
                elif glyph is 'l':
                    xTranslation += 1.6 + self.glyphInnerSpaceW
                else:
                    xTranslation += self.glyphW + self.glyphInnerSpaceW
            else:
                xTranslation += self.spaceW

        return glyphsPaths

    def getContentNumbers(self, specimenNumber):
        cardboard = ceil(specimenNumber/1328)
        return {
            'cardboard': self.numberToString(cardboard),
            'container': self.numberToString(ceil(cardboard/729)),
            'date': strftime('%d/%m/%y à %Hh%M')
        }


rulerGenerator = RulerGenerator()
