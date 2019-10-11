from .constants import colors, fonts
from .manager import Component


class Hint(Component):

    def __init__(self, content, action, onAction):
        self.content = content
        self.action = action
        self.onAction = onAction

        self.div_styles = self.css(f"""
            background-color: {colors.back};
            opacity: 0.5;
            border-radius: 3px;
            display: flex;
            justify-content: space-between;
            padding: 10px;
        """)

        self.span_styles = self.css(f"""
            height: 16px;
            color: {colors.front};
            font-family: {fonts.default};
            font-size: 12px;
            line-height: 16px;
        """)

        self.button_styles = self.css(f"""
            height: 14px;
            color: {colors.front};
            font-family: {fonts.default};
            font-size: 12px;
            font-weight: bold;
            line-height: 14px;
            background: none;
            border: none;
            display: inline-flex;
            cursor: pointer;
            """)

    def render(self):
        return f"""
        <div class="{self.div_styles}">
            <span class="{self.span_styles}">{self.text}</span>
            <button class="{self.button_styles}" onClick={self.onAction}>
                {self.action}
            </button>
        </div>
        """
