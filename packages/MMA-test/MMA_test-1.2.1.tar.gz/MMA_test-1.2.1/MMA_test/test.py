import yaml

def readYaml(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.load(f, yaml.Loader)['featureClass']['glcm']