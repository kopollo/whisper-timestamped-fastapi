import yaml

with open("setup_config/test_cpu_config.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
