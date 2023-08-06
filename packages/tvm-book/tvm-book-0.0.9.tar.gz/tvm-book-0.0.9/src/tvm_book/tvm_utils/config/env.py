import toml
from ._env import set_tvm


def set_env(toml_path):
    """
    Args:
        toml_path: 存储 TVM 环境配置
    """
    with open(toml_path) as fp:
        config = toml.load(fp)
    set_tvm(config["TVM_ROOT"])
