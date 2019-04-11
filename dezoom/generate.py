from parse import yaml

with open('dezoom.yaml', 'r') as input:
    data = yaml.load(input)
    print(data)
