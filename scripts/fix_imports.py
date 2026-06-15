import os

MODELS_DIR = r"d:\Project\ASTRA\backend\models"

def fix_imports(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False
    
    if "from typing import Any" not in content and "Any" in content:
        content = "from typing import Any\n" + content
        changed = True
        
    if "from datetime import datetime" not in content and "datetime" in content:
        content = "from datetime import datetime\n" + content
        changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

for filename in os.listdir(MODELS_DIR):
    if filename.endswith(".py") and filename != "__init__.py":
        fix_imports(os.path.join(MODELS_DIR, filename))
        
print("Fixed imports.")
