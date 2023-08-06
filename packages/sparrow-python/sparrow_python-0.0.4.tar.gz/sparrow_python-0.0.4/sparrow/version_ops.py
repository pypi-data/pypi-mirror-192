import os
from .io import yaml_load, yaml_dump, rm
from .string.ops import string_add


class VersionControl:
    def __init__(
            self,
            pkgname,
            pkgdir,
            version=None,
            filename="version-config.yaml",
    ):

        # self.config = None
        self._pkgname = pkgname
        self._config_path = os.path.join(pkgdir, filename)
        if version is None:
            try:
                self.get_config()
            except:
                print(f"{filename} was not exist, created now.")
                self.gen_config("0.0.0")
        else:
            self.gen_config(version)

    def gen_config(self, version="0.0.0"):
        config = {"name": self._pkgname, "version": version}
        self.config = config
        yaml_dump(self._config_path, config, rel_path=False)

    def get_config(self):
        config = yaml_load(self._config_path, rel_path=False)
        self.config = config
        return config

    def set_version(self, version):
        self.config["version"] = version

    def save_config(self):
        yaml_dump(self._config_path, self.config, rel_path=False)

    def update_version(self, version_step=1):
        self.config["version"] = string_add(self.config["version"], version_step)
        self.update_pyproject()
        yaml_dump(self._config_path, self.config, rel_path=False)

    def clean_config_file(self):
        os.remove(self._config_path)

    def update_pyproject(self):
        pyproject_path = "pyproject.toml"
        # import toml
        # pyproject = toml.load(pyproject_path)
        # pyproject['tool']['poetry']['version'] = self.config["version"]
        # pyproject['tool']['poetry']['version'] = 0.9
        # with open(pyproject_path, "w", encoding="utf8") as f:
        #     toml.dump(pyproject, f)
        with open(pyproject_path, "r", encoding="UTF-8") as fr:
            pyproject_list = fr.readlines()
        for idx, line in enumerate(pyproject_list[:10]):
            if "version" in line:
                new_line = f"""version = "{self.config['version']}"
"""
                pyproject_list[idx] = new_line
        with open(pyproject_path, 'w', encoding="UTF-8") as fw:
            fw.writelines(pyproject_list)

    def update_readme(
            self,
            readme_path="README.md",
            license="MIT",
            author="kunyuan",
            replace_flag=19 * "-",
    ):
        with open(readme_path, "r", encoding="UTF-8") as fr:
            readme = fr.read()
        replace_begin = f"""\
# {self._pkgname}
[![image](https://img.shields.io/badge/Pypi-{self.config['version']}-green.svg)](https://pypi.org/project/{self._pkgname})
[![image](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![image](https://img.shields.io/badge/license-{license}-blue.svg)](LICENSE)
[![image](https://img.shields.io/badge/author-{author}-orange.svg?style=flat-square&logo=appveyor)](https://github.com/beidongjiedeguang)


"""
        readme_list = readme.split(replace_flag)
        readme_list[0] = replace_begin
        new_readme = replace_flag.join(readme_list)

        with open(readme_path, "w", encoding="UTF-8") as fo:
            fo.write(new_readme)

    def upload_pypi(self):
        pkgname = self._pkgname
        rm("build", "dist", "eggs", f"{pkgname}.egg-info")
        os.system("python -m build")
        os.system("twine upload dist/*")
        rm("build", "dist", "eggs", f"{pkgname}.egg-info")

    def install(self):
        pkgname = self._pkgname
        rm("build", "dist", "eggs", f"{pkgname}.egg-info")
        os.system(f"pip uninstall {pkgname} -y && python setup.py install")
        rm("build", "dist", "eggs", f"{pkgname}.egg-info")

    @staticmethod
    def build():
        os.system(f"pythom -m build")
