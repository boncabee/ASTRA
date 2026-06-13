from app.parsers.registry.registry import registry
from app.parsers.windows.windows_parser import WindowsParser

registry.register_parser("windows", WindowsParser)

__all__ = ["WindowsParser"]
