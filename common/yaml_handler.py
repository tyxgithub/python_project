import yaml
from config import config


# YAML读取
def read_yaml(file, method="r"):
    with open(file, method) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data


# YAML文件写入
def write_yaml(file, data, method="a+"):
    with open(file, method) as f:
        yaml.dump(data, f, encoding="utf-8", allow_unicode=True)
    return "数据写入成功"


if __name__ == '__main__':
    excel_path = config.CON_PATH + "\config.yaml"
    print(read_yaml(excel_path))
