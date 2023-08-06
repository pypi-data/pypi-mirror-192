from abc import ABC
from enum import Enum
from typing import Dict

from colour import Color
from pygments.styles import get_style_by_name
from pygments.style import Style as PygmentsStyle

from dmte.token import Token


class FontFormat(Enum):
    NORMAL = "normal"
    ITALIC = "italic"
    UNDERLINE = "underline"
    BOLD = "bold"
    MONOSPACE = "monospace"
    STRIKETHROUGH = "strikethrough"


class TokenStyle:
    def __init__(self, color: Color = None, font_style: FontFormat = FontFormat.NORMAL):
        self.color = color
        self.font_style = font_style


class Style(ABC):
    def __init__(
        self,
        background_color: Color = Color("#ffffff"),
        highlight_color: Color = Color("#ffffcc"),
        line_number_color: Color = Color("#555555"),
        line_number_background_color: Color = Color("#777777"),
        line_number_special_color: Color = Color("#000000"),
        line_number_special_background_color: Color = Color("#ffffc0"),
        token_styles: Dict[Token, TokenStyle] = None,
    ):
        self.background_color = background_color
        self.highlight_color = highlight_color
        self.line_number_color = line_number_color
        self.line_number_background_color = line_number_background_color
        self.line_number_special_color = line_number_special_color
        self.line_number_special_background_color = line_number_special_background_color
        self.token_styles = token_styles


def get_pygments_style(style_name: str) -> PygmentsStyle:
    return get_style_by_name(style_name)


if __name__ == "__main__":
    style = get_style_by_name("colorful")
    keys = tuple(get_style_by_name("colorful").styles.keys())
    print(style.style_for_token(keys[4]))
    print(Color(f"#{style.style_for_token(keys[4])['color']}"))
    print(Color("#eee").rgb)
