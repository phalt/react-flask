from __future__ import annotations

from collections import OrderedDict


class TypescriptInterfaces:
    def __init__(self):
        self.imports = OrderedDict()

    def add(self, name: str, declaration: str) -> None:
        self.imports[name] = declaration

    def merge(self, other_imports: TypescriptInterfaces) -> None:
        for name, declaration in other_imports:
            self.add(name, declaration)

    def __iter__(self):
        for name, declaration in self.imports.items():
            yield name, declaration

    def __bool__(self):
        return len(self.imports.keys()) > 0

    def render(self) -> str:
        out = ""
        for _, declaration in self:
            out += "// prettier-ignore\n"
            out += "export "
            out += declaration
            out += "\n\n"

        return out
