from ruamel.yaml import YAML
from ruamel.yaml.constructor import SafeConstructor
from elements import elements


def construct_yaml_map(self, node):
    # Turns every svg elements keys/values into tuples to allow
    # duplicates keys in yaml files.
    # Adapted from https://stackoverflow.com/a/44906713

    for key_node, value_node in node.value:
        key = self.construct_object(key_node, deep=True)
        if key in elements and key != 'svg':
            break
    else:
        data = {}  # type: Dict[Any, Any]
        yield data
        value = self.construct_mapping(node)
        data.update(value)
        return


    data = []
    yield data
    for key_node, value_node in node.value:
        key = self.construct_object(key_node, deep=True)
        val = self.construct_object(value_node, deep=True)
        data.append((key, val))


SafeConstructor.add_constructor(u'tag:yaml.org,2002:map', construct_yaml_map)
yaml = YAML(typ='safe')
