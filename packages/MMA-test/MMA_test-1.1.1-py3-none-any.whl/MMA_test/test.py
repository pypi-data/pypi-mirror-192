import yaml

def readYaml():
    with open('./radiomics_features.yaml', 'r', encoding='utf-8') as f:
        return yaml.load(f, yaml.Loader)['featureClass']['glcm']