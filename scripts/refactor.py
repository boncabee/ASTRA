import os
import re

MODELS_DIR = r"d:\Project\ASTRA\backend\models"

def refactor_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Add Mapped and mapped_column imports if they don't exist
    if "from sqlalchemy.orm import Mapped, mapped_column" not in content:
        content = "from sqlalchemy.orm import Mapped, mapped_column\n" + content
    
    # Replace id = Column(...) -> id: Mapped[uuid.UUID] = mapped_column(...)
    # String -> Mapped[str]
    # Boolean -> Mapped[bool]
    # Integer -> Mapped[int]
    # DateTime -> Mapped[datetime]
    # JSON -> Mapped[dict]
    # SQLEnum(something) -> Mapped[something]
    # Uuid(as_uuid=True) -> Mapped[uuid.UUID]
    
    # We will do a generic replacement using regex
    # Regex to match: field_name = Column(Type, ...)
    
    lines = content.split("\n")
    new_lines = []
    
    for line in lines:
        match = re.match(r"^    ([a-zA-Z0-9_]+) = Column\((.*?)\)(.*)$", line)
        if match:
            field = match.group(1)
            args = match.group(2)
            rest = match.group(3)
            
            # Detect type
            py_type = "Any"
            if "String" in args:
                py_type = "str"
            elif "Boolean" in args:
                py_type = "bool"
            elif "Integer" in args:
                py_type = "int"
            elif "DateTime" in args:
                py_type = "datetime"
            elif "JSON" in args:
                py_type = "dict"
            elif "Uuid" in args:
                py_type = "uuid.UUID"
            elif "SQLEnum" in args:
                enum_match = re.search(r"SQLEnum\(([a-zA-Z0-9_]+)\)", args)
                if enum_match:
                    py_type = enum_match.group(1)
            
            # Check for nullable
            if "nullable=True" in args or "nullable=False" not in args and "primary_key" not in args:
                # SQLAlchemy defaults nullable=True unless primary_key=True
                # But let's be careful. If nullable=False is missing, we shouldn't assume Optional unless nullable=True is explicitly there.
                # Actually, in old Column, nullable is True by default.
                if "nullable=False" not in args and "primary_key=True" not in args:
                    py_type = f"str | None" if py_type == "str" else f"{py_type} | None"
            
            # Some manual cleanup needed, but let's try a simpler regex
            new_line = f"    {field}: Mapped[{py_type}] = mapped_column({args}){rest}"
            new_lines.append(new_line)
        else:
            new_lines.append(line)
            
    # Also fix imports for Any, datetime etc if needed, but easier to just let mypy tell us and fix.
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

for filename in os.listdir(MODELS_DIR):
    if filename.endswith(".py") and filename != "__init__.py":
        refactor_file(os.path.join(MODELS_DIR, filename))
        
print("Refactored models.")
