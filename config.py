import yaml

with open("config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
