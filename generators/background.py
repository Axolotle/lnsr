from json import loads
from random import randint, sample
from svgwrite import Drawing
from svgwrite.shapes import Line
from svgwrite.container import Group

class BackgroundGenerator:
    def __init__(self):
        with open('generators/backgroundData.json', 'r') as data:
            data = loads(data.read())
            self.width = data['width']
            self.height = data['height']
            self.style = data['style']
            self.verticalInterval = data['verticalInterval']

        self.verticalLines = round(self.height / self.verticalInterval)
        self.viewBox = '0 0 {} {}'.format(self.width, self.height)

    def generateObject(self):
        document = self.getSVGDocument()
        elements = self.getLines()
        print(self.verticalLines)
        document.add(elements)

        return document

    def generateString(self):
        return self.generateObject().tostring()

    def getSVGDocument(self):
        return Drawing(
            'background.svg',
            size=(str(self.width) + "mm", str(self.height) + "mm"),
            viewBox=self.viewBox,
            profile='tiny',
        )

    def getLines(self):
        group = Group(**self.style)

        currentY = 6
        currentX = randint(-10 , 150)

        for y in range(0, self.verticalLines):
            while currentX < self.width:
                randX = randint(2, 6) + currentX
                line = Line((currentX, currentY), (randX, currentY))
                group.add(line)
                currentX = randX + randint(50, 150)
            currentX = randint(-10, 150)
            currentY = round(currentY + self.verticalInterval, 1)

        return group

background = BackgroundGenerator()
