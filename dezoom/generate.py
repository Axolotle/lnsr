from lxml.etree import ElementTree, Element, tostring

from parse import yaml


with open('dezoom.yaml', 'r') as input:
    data = yaml.load(input)

children = data['svg'].pop('children')
NSMAP = data['svg'].pop('ns')
root = Element('svg', attrib=data['svg'], nsmap=NSMAP)
document = ElementTree(root)

with open('../templates/svgs/dezoom.svg', 'w') as output:
    input = tostring(document, encoding='utf-8', xml_declaration=True, pretty_print=True)
    output.write(input.decode())
