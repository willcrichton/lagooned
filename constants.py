import yaml

C = {}    
files = ['writing.yml']
for path in files:
    with open(path) as stream:
        C.update(yaml.load(stream))
