from __future__ import annotations

import json
from typing import Dict, Set


class TypescriptImports:
    def __init__(self):
        self.imports: Dict[str, Set[str]] = {}

    def add(self, module: str, declaration: str) -> None:
        self.imports.setdefault(module, set())
        self.imports[module].add(declaration)

    def merge(self, other_imports: TypescriptImports) -> None:
        for module, declarations in other_imports:
            for declaration in declarations:
                self.add(module, declaration)

    def __iter__(self):
        for module, declarations in self.imports.items():
            yield module, declarations

    def __bool__(self):
        return len(self.imports.keys()) > 0

    def render(self) -> str:
        if not self.imports:
            return ""
        out = ""
        for module, declarations in sorted(self):
            out += "// prettier-ignore\n"
            out += "import {"
            out += ", ".join(declarations)
            out += "} from "
            out += json.dumps(module)
            out += "\n"

        return out
