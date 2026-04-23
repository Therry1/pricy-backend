#!/usr/bin/env python3
"""Scaffold : génère un nouveau module dans app/services/"""

import os
import sys

TEMPLATES = {
    "handler.py": '"""Handlers du module {name}."""\n',
    "helper.py": '"""Helpers du module {name}."""\n',
    "schemas.py": '"""Schémas Pydantic du module {name}."""\n',
    "router.py": (
        '"""Router du module {name}."""\n'
        "from fastapi import APIRouter\n\n"
        "router = APIRouter(prefix=\"/{name}\", tags=[\"{name}\"])\n"
    ),
    "dependencies.py": '"""Dépendances du module {name}."""\n',
    "constants.py": '"""Constantes du module {name}."""\n',
    "__init__.py": '"""Module {name}."""\n',
}

def scaffold(name: str) -> None:
    path = os.path.join("app", "services", name)
    if os.path.exists(path):
        print(f"❌ Le module '{name}' existe déjà.")
        sys.exit(1)

    os.makedirs(path)
    for filename, content in TEMPLATES.items():
        filepath = os.path.join(path, filename)
        with open(filepath, "w") as f:
            f.write(content.format(name=name))
        print(f"  ✅ {filepath}")

    print(f"\n🚀 Module '{name}' créé avec succès dans app/services/{name}/")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python scaffold.py <nom_du_module>")
        sys.exit(1)
    scaffold(sys.argv[1])