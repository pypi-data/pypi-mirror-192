from abc import ABC, abstractmethod
from pathlib import Path

from pygments.lexers import get_lexer_by_name, get_lexer_for_filename

from dmte.token import Token


class Lexer(ABC):
    @abstractmethod
    def get_tokens(self, text: str):
        pass


class LexerSelector(ABC):
    lexer_name: str = None
    lexer: Lexer = None

    @abstractmethod
    def autoselect_lexer(self, filename: Path):
        pass

    def __init__(self):
        pass

    @abstractmethod
    def _get_lexer(self):
        pass

    def select_lexer(self, lexer_name: str):
        self.lexer_name = lexer_name
        self._get_lexer()


class PygmentsLexerSelector(LexerSelector):
    def __init__(self):
        super().__init__()

    def _get_lexer(self):
        self.lexer = get_lexer_by_name(self.lexer_name)

    def autoselect_lexer(self, filename: Path):
        self.lexer = get_lexer_for_filename(filename)

    def get_tokens(self, text: str):
        if self.lexer:
            return self.lexer.get_tokens(text)


if __name__ == "__main__":
    path = Path(r"C:\Users\Dmatryus\Downloads\Documents\calc_stats.py")
    with open(path) as f:
        text = "\n".join(f.readlines())
    pls = PygmentsLexerSelector()
    pls.autoselect_lexer(path)
    print(pls.lexer)
    tokens = pls.get_tokens(text)
    print([str(token) for token in tokens])
