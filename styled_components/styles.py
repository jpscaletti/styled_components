from pathlib import Path
import glob
import hashlib
import os
import re

import sass


__all__ = ("Styles",)

RX_EXT = re.compile(r"\.css$", re.IGNORECASE)


def get_hash(styles):
    return hashlib.md5(styles.encode("utf8")).hexdigest()


class CSS(object):

    __slots__ = ("class_name", "styles")

    def __init__(self, class_name, styles, output_style=None):
        self.class_name = class_name
        styles = f".{class_name} {{ {styles} }}"
        styles = sass.compile(string=styles, output_style=output_style)
        self.styles = styles.replace("\n\n", "\n")

    def __str__(self):
        return self.class_name

    def __repr__(self):
        return f"<CSS {self.class_name}>"


class Styles(object):

    css_objs = None

    def __init__(self, file_path=None, file_url="styles.css", output_style="compact"):
        self.file_path = RX_EXT.split(file_path)[0] if file_path else None
        self.file_url = RX_EXT.split(file_url.rstrip("/"))[0] if file_url else None
        self.css_objs = {}
        self.output_style = output_style

    def __call__(self, styles, prefix=None):
        hash_ = get_hash(styles)
        if prefix:
            prefix = prefix.replace(" ", "").replace(".", "")
            class_name = prefix + "--" + hash_
        else:
            class_name = hash_

        cssobj = self.css_objs.get(class_name)
        if cssobj is None:
            cssobj = CSS(class_name, styles, output_style=self.output_style)
            self.css_objs[class_name] = cssobj

        return cssobj

    def render(self):
        if self.file_path:
            self.save_stylesheet()
        else:
            return self.render_styles()

    def save_stylesheet(self):
        styles = "".join([css.styles for css in self.css_objs.values()])
        hash_ = get_hash(styles)
        final_path = Path(f"{self.file_path}--{self.hash_}.css")
        if final_path.exists():
            return self._link_tag(hash_)

        self._delete_old_stylesheets()
        final_path.write_text(styles)
        return self._link_tag(hash_)

    def _link_tag(self, hash_):
        return (
            f'<link rel="stylesheet" href="{self.file_url}--{hash_}'
            '.css" type="text/css">'
        )

    def _delete_old_stylesheets(self):
        files_list = glob.glob(f"{self.file_path}--*.css")
        for path in files_list:
            try:
                os.remove(path)
            except OSError:
                pass

    def render_styles(self):
        output = ["<style>\n"]
        output.extend([css.styles for css in self.css_objs.values()])
        output.append("</style>")
        return "".join(output)
