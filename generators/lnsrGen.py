from svgwrite import Drawing
from svgwrite.shapes import Polyline
from svgwrite.container import Group


w = 2.25

def convertCharacters():
    charas = {
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
    for chara in charas:
        trad = charas[chara].replace('a', '1').replace('b', '2').replace('c', '3')
        trad = [list(trad[i:i+2]) for i in range(0, len(trad), 2)]
        charas[chara] = [(int(pos[0]) * w, (int(pos[1]) + 1) * w) for pos in trad]

    return charas

def getPolyline(chara, x):
    polyline = Polyline()
    for point in characters[chara]:
        polyline.points.append((point[0] + x, point[1]))

    return polyline

def base():
    text = list('/31 557 600 000 000 000 lns')
    style = {
        'fill': 'none',
        'stroke': 'black',
        'stroke_width': str(w) + 'px',
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        #'stroke-miterlimit': str(w),
    }
    elements = Group(**style)
    x = 0
    for chara in text:
        if chara is not ' ':
            elements.add(getPolyline(chara, x))
            x += w * 4
        else: x += w * 2
    return elements


characters = convertCharacters()

doc = Drawing('lnsr.svg', profile='tiny',
              size=('500px', '500px'), viewBox='0 0 500 500')
doc.add(base())
doc.save(pretty=True)
