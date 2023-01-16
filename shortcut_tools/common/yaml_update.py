from ruamel import yaml
from shortcut_tools.common.set_path import CONFIG_FILE


class UpdateYaml:
    @staticmethod
    def up_yml(key, value):
        with open(CONFIG_FILE, 'r', encoding="utf-8") as f:
            content = yaml.load(f, Loader=yaml.Loader)
            # 修改yml文件中的参数
            content[key] = value
        with open(CONFIG_FILE, 'w', encoding="utf-8") as nf:
            yaml.dump(content, nf, Dumper=yaml.RoundTripDumper, allow_unicode=True)
