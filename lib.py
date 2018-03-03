import yaml

def load_configs(path):
    # Load configurations.yaml file
    CONFS = yaml.load(open(path))
    return CONFS

def get_conf(conf_name, path):
    # Load specific configuration from configurations file
    return load_configs(path)[conf_name]