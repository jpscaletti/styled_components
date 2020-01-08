from styled_components import Component, Styles


class colors:
    back = "#fff"
    front = "#ff1010"


class fonts:
    default = '"Fira Sans", sans-serif'


css = Styles()


class Hint(Component):

    def __init__(self, text, action):
        self.text = text
        self.action = action

        self.s_wrapper = css(f"""
            font-family: {fonts.default};
            background-color: {colors.back};
            opacity: 0.5;
            border-radius: 3px;
            display: flex;
            justify-content: space-between;
            padding: 10px;

            @media screen and (max-width: 640px) {{
                font-size: 10px;
            }}
        """, "HintWrapper")

        self.s_span = css(f"""
            height: 16px;
            color: {colors.front};
            font-size: 12px;
            line-height: 16px;
        """, "HintHelp")

        self.s_button = css(f"""
            height: 14px;
            color: {colors.front};
            font-size: 12px;
            font-weight: bold;
            line-height: 14px;
            background: none;
            border: none;
            display: inline-flex;
            cursor: pointer;
            """, "HintButton")

    def template(self):
        return """
        <div class="{{ s_wrapper }}">
            <span class="{{ s_span }}">{{ text }}</span>
            <button class="{{ s_button }}">
                {{ action }}
            </button>
        </div>
        """


hint = Hint(text="Click the button", action="Be happy")
print(hint.render())
print("-" * 80)
print(css.render())
