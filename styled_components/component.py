import textwrap

from jinja2.sandbox import SandboxedEnvironment


# The default env options for jinja2
DEFAULT_ENV_OPTIONS = {
    "autoescape": False,
    "block_start_string": "[%",
    "block_end_string": "%]",
    "variable_start_string": "[[",
    "variable_end_string": "]]",
    "keep_trailing_newline": False,
}

jinja_env = SandboxedEnvironment(**DEFAULT_ENV_OPTIONS)


class Component(object):

    def __str__(self):
        src = self._get_template_src()
        return self._jinja_render(src)

    def _get_template_src(self):
        src = (self.render() or "").strip("\n")
        return textwrap.dedent(src)

    def _jinja_render(self, template_src):
        template = jinja_env.from_string(template_src)
        return template.render()
