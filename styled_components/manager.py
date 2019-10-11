from pathlib import Path
import random
import string
import subprocess

from .component import Component as _Component


def random_postfix(len=9):
    letters = string.ascii_lowercase + string.digits
    return "".join(random.choices(letters, k=len))


class CSS(object):

    __slots__ = ("class_name", "styles")

    def __init__(self, class_name, styles):
        self.class_name = class_name
        self.styles = styles

    def __str__(self):
        return self.class_name


class Manager(object):

    styles = None

    def __init__(manager, file_path=None, file_url=None, autoprefix=True):
        file_path = Path(file_path)
        assert file_path.exists()
        assert file_path.isdir()
        manager.file_path = file_path
        manager.file_url = file_url
        manager.styles = {}

        class Component(_Component):
            def css(self, styles):
                class_name = self.get_class_name()
                cssobj = CSS(class_name, styles)
                manager.styles[class_name] = cssobj
                return cssobj

            def _get_class_name(self):
                return f"{self.__class__.__name__}--{random_postfix()}"

        manager.Component = Component

    def save_styles(self):
        if self.file_path:
            return self._save_styles_to_file()
        return self._render_styles()

    def _save_styles_to_file(self):
        with open(self.file_path, "rt") as sfile:
            for class_name, styles in self.styles.items():
                sfile.write(f".{class_name} {{")
                sfile.write(styles)
                sfile.write("}")
        if self.autoprefix:
            subprocess.call(
                [
                    "npx",
                    "postcss",
                    self.file_path,
                    "--use autoprefixer",
                    "-o",
                    self.file_path,
                ]
            )
        return f'<link rel="stylesheet" href="{self.file_url}" type="text/css">'

    def _render_styles(self):
        output = ["<style>"]
        for class_name, styles in self.styles.items():
            output.append(f".{class_name} {{")
            output.append(styles)
            output.append("}")
        output.append("</style>")
        return "\n".join(output)
