from svgwrite import Drawing
from svgwrite.path import Path
from svgwrite.container import Group
from json import loads, dumps


class RulerGenerator:
    def __init__(self):
        with open('generators/svgData.json', 'r') as data:
            data = loads(data.read())
            self.size = (data['width'], data['height'])
            self.viewBox = data['viewBox']
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

        outline = self.getPath(self.rulerOutline, 0, style=self.styles[docType]['rulerOutline'])
        document.add(outline)

        text = self.parseSpecimenNumber(specimenNumber) + self.rulerTotal
        text = self.textToPaths(text, docType=docType, pathType=pathType)
        text['transform'] = 'translate(12.5, 20.5)'
        document.add(text)

        # document.save(pretty=True)
        return document.tostring()

    def getSVGDocument(self, specimenNumber):
        return Drawing(
            'light-nanosecond_ruler{}.svg'.format(specimenNumber),
            size=self.size,
            viewBox=self.viewBox,
            profile='tiny',
        )

    def getPath(self, points, xTranslation, style={}):
        parts = ['M {}{}'.format(round(startXPoint + xTranslation, 7), rest)
                 for startXPoint, rest in points]
        return Path(d=' '.join(parts), **style)

    def parseSpecimenNumber(self, specimenNumber):
        text = str(specimenNumber)
        splittedText = [text[(i-3 if i-3 > 0 else 0):i]
                        for i in range(len(text), -1, -3)]
        return " ".join(reversed(splittedText))

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


rulerGenerator = RulerGenerator()
