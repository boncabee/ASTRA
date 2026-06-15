import threading
from typing import Dict, Type, Any, List

from app.parsers.base.base_parser import BaseParser
from app.parsers.registry.exceptions import (
    DuplicateParserError,
    ParserNotFoundError,
    InvalidParserError
)

class ParserRegistry:
    """
    Centralized registry for all ASTRA parsers.
    Manages parser registration, discovery, and lifecycle.
    Thread-safe for concurrent access.
    """
    _instance = None
    _lock = threading.Lock()
    _initialized: bool = False
    
    def __new__(cls) -> 'ParserRegistry':
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ParserRegistry, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self) -> None:
        with self._lock:
            if not self._initialized:
                self._parsers: Dict[str, Type[BaseParser]] = {}
                self._metadata: Dict[str, Dict[str, Any]] = {}
                self._initialized = True

    def register_parser(self, source_type: str, parser_class: Type[BaseParser], **kwargs) -> None:
        """
        Registers a new parser for a specific source type.
        """
        if not source_type:
            raise ValueError("source_type cannot be empty.")
            
        if not isinstance(parser_class, type) or not issubclass(parser_class, BaseParser):
            raise InvalidParserError(f"parser_class must be a subclass of BaseParser, got {parser_class}.")
            
        with self._lock:
            if source_type in self._parsers:
                raise DuplicateParserError(f"Parser for source_type '{source_type}' is already registered.")
            
            self._parsers[source_type] = parser_class
            
            # Default metadata with any provided overrides
            metadata = {
                "name": source_type,
                "enabled": True,
                "version": "1.0",
                **kwargs
            }
            self._metadata[source_type] = metadata

    def get_parser(self, source_type: str) -> Type[BaseParser]:
        """
        Retrieves the parser class for a specific source type.
        """
        with self._lock:
            if source_type not in self._parsers:
                raise ParserNotFoundError(f"No parser registered for source_type '{source_type}'.")
            return self._parsers[source_type]

    def has_parser(self, source_type: str) -> bool:
        """
        Checks if a parser is registered for the given source type.
        """
        with self._lock:
            return source_type in self._parsers

    def list_parsers(self) -> List[str]:
        """
        Returns a list of all registered source types.
        """
        with self._lock:
            return list(self._parsers.keys())

    def unregister_parser(self, source_type: str) -> None:
        """
        Removes a parser from the registry.
        """
        with self._lock:
            if source_type in self._parsers:
                del self._parsers[source_type]
            if source_type in self._metadata:
                del self._metadata[source_type]

    def get_metadata(self, source_type: str) -> Dict[str, Any]:
        """
        Retrieves metadata for a registered parser.
        """
        with self._lock:
            if source_type not in self._parsers:
                raise ParserNotFoundError(f"No parser registered for source_type '{source_type}'.")
            return dict(self._metadata[source_type])
            
    def set_enabled(self, source_type: str, enabled: bool) -> None:
        """
        Enables or disables a registered parser.
        """
        with self._lock:
            if source_type not in self._parsers:
                raise ParserNotFoundError(f"No parser registered for source_type '{source_type}'.")
            self._metadata[source_type]["enabled"] = enabled
            
    def is_enabled(self, source_type: str) -> bool:
        """
        Checks if a parser is enabled.
        """
        with self._lock:
            if source_type not in self._parsers:
                raise ParserNotFoundError(f"No parser registered for source_type '{source_type}'.")
            return self._metadata[source_type].get("enabled", True)
            
    def clear(self) -> None:
        """
        Clears all registered parsers. Mainly for testing.
        """
        with self._lock:
            self._parsers.clear()
            self._metadata.clear()

registry = ParserRegistry()
