from lxml.etree import ElementTree, Element, tostring

from parse import yaml


def itering(items, container):
    for (tag, options) in items:
        children = options.pop('children', None)
        elem = Element(tag, **refactorize_options(options))
        if children:
            itering(children, elem)
        container.append(elem)

def refactorize_options(opts):
    haddata = False
    options = {}
    for key, value in opts.items():
        if key == 'data':
            for name, val in opts[key].items():
                options['data-' + name] = val
                if name != 'scalename':
                    haddata = True
        else:
            options[key] = str(value)

    if haddata:
        if 'class' in options:
            options['class'] += ' data'
        else:
            options['class'] = 'data'

    return options

if __name__ == "__main__":
    with open('dezoom.yaml', 'r') as input:
        data = yaml.load(input)

    children = data['svg'].pop('children')
    NSMAP = data['svg'].pop('ns')
    root = Element('svg', attrib=data['svg'], nsmap=NSMAP)
    document = ElementTree(root)

    itering(children, root)

    with open('../templates/svgs/dezoom.svg', 'w') as output:
        input = tostring(document, encoding='utf-8', xml_declaration=True, pretty_print=True)
        output.write(input.decode())
