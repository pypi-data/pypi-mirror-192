import yaml

def readYaml(file_path):
    with open('radiomics_features.yaml', 'r', encoding='utf-8') as f:
        return yaml.load(f, yaml.Loader)['featureClass']['glcm']