from pathlib import Path
import hashlib
import re
import subprocess

import sass


__all__ = ("Styles",)


RX_EXTRA_SPACES = re.compile(r"^\s+|\s+$")
RX_EXTRA_SPACES2 = re.compile(r"\n\s+")
RX_EXTRA_LINEJUMPS = re.compile(r"\n\n+")


def normalize_styles(styles):
    styles = RX_EXTRA_SPACES.sub("", styles)
    styles = RX_EXTRA_SPACES2.sub("\n", styles)
    styles = RX_EXTRA_LINEJUMPS.sub("\n", styles)
    return styles


def get_hash(styles):
    return hashlib.md5(styles.encode("utf8")).hexdigest()


class CSS(object):

    __slots__ = ("class_name", "styles")

    def __init__(self, class_name, styles, output_style=None):
        self.class_name = class_name
        styles = f".{class_name} {{ {styles} }}"
        self.styles = sass.compile(string=styles, output_style=output_style)

    def __str__(self):
        return self.class_name


class Styles(object):

    css_objs = None

    def __init__(
        self, file_path=None, file_url=None, autoprefix=True, output_style="expanded"
    ):
        if file_path:
            file_path = Path(file_path)
            assert file_path.exists()
            assert file_path.isdir()
        self.file_path = file_path
        self.file_url = file_url
        self.css_objs = {}
        self.autoprefix = autoprefix
        self.output_style = output_style

    def __call__(self, styles, prefix=None):
        styles = normalize_styles(styles)
        postfix = get_hash(styles)
        if prefix:
            class_name = prefix.replace(" ", "") + "--" + postfix
        else:
            class_name = postfix

        cssobj = CSS(class_name, styles, output_style=self.output_style)
        self.css_objs[class_name] = cssobj
        return cssobj

    def save_styles(self):
        if self.file_path:
            return self._save_styles_to_file()
        return self._render_styles()

    def _save_styles_to_file(self):
        with open(self.file_path, "rt") as sfile:
            for class_name, css in self.css_objs.items():
                sfile.write(css.styles)

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
        output = ["<style>\n"]
        output.extend([css.styles for css in self.css_objs.values()])
        output.append("</style>")
        return "".join(output)
