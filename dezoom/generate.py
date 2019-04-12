from lxml.etree import ElementTree, Element, tostring

from parse import yaml


def itering(items, container):
    for (tag, options) in items:
        children = options.pop('children', None)
        text = options.pop('content', None)
        elem = Element(tag, **refactorize_options(options, tag))
        elem.text = text
        if children:
            itering(children, elem)
        container.append(elem)

def refactorize_options(opts, tag):
    haddata = False
    options = {}
    classes = []
    for key, value in opts.items():
        if key == 'data':
            if 'scalename' not in opts['data'] or len(opts['data']) > 1:
                classes.append('data')
            for name, val in opts[key].items():
                options['data-' + name] = val
        elif key in ['c', 'r'] and type(value) == list:
            options[key + 'x'] = str(value[0])
            options[key + 'y'] = str(value[1])
        elif key == 'class':
            classes = [*classes, *opts[key].split(' ')]
        else:
            options[key] = str(value)

    if len(classes):
        options['class'] = ' '.join(classes)

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
