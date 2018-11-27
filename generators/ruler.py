from json import loads, dumps
from math import ceil
from time import strftime

from svgwrite import Drawing
from svgwrite.path import Path
from svgwrite.container import Group


class RulerGenerator:
    def __init__(self):
        with open('generators/svgData.json', 'r') as data:
            data = loads(data.read())
            self.width = data['width']
            self.height = data['height']
            self.viewBox = '0 0 {} {}'.format(self.width, self.height)

            self.glyphW = data['glyphWidth']
            self.glyphInnerSpaceW = data['glyphInnerSpaceWidth']
            self.spaceW = self.glyphW - self.glyphInnerSpaceW
            self.glyphSlashSpace = data['glyphSlashSpace']

            self.styles = data['styles']
            self.rulerOutline = data['rulerOutline']
            self.rulerTotal = data['rulerTotal']
            self.glyphs = data['glyphs']

    def generateObject(self, specimenNumber, docType):
        style = self.styles[docType]
        width = round(self.width + style['margin'] * 2, 7)
        height = round(self.height + style['margin'] * 2, 7)

        document = self.getSVGDocument(specimenNumber, width, height)
        elements = Group()
        elements['transform'] = 'translate({}, {})'.format(style['margin'], style['margin'])
        document.add(elements)

        outline = self.getPath(self.rulerOutline, 0, style=style['outlineStyle'])
        elements.add(outline)

        text = self.numberToString(specimenNumber) + self.rulerTotal
        text = self.textToPaths(text, style['numbersPathType'], style['numbersStyle'])
        text['transform'] = 'translate(12.5, 20.5)'
        elements.add(text)

        return document

    def generateString(self, specimenNumber, docType):
        return self.generateObject(specimenNumber, docType).tostring()

    def generateFile(self, specimenNumber, docType, folder):
        filename = '{}light-nanosecond_ruler{}.svg'.format(folder, specimenNumber)
        return self.generateObject(specimenNumber, docType).saveas(filename)

    def getSVGDocument(self, specimenNumber, width, height):
        return Drawing(
            'light-nanosecond_ruler{}.svg'.format(specimenNumber),
            size=(str(width) + 'mm', str(height) + 'mm'),
            viewBox='0 0 {} {}'.format(width, height),
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

    def textToPaths(self, text, pathType, style, xTranslation=0):
        glyphs = self.glyphs[pathType]
        glyphsPaths = Group(**style)
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


ruler = RulerGenerator()
