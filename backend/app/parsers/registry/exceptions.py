class ParserRegistryError(Exception):
    """Base exception for all ParserRegistry errors."""
    pass

class DuplicateParserError(ParserRegistryError):
    """Raised when attempting to register a parser with a source_type that is already registered."""
    pass

class ParserNotFoundError(ParserRegistryError):
    """Raised when attempting to look up a parser that is not registered."""
    pass

class InvalidParserError(ParserRegistryError):
    """Raised when attempting to register an invalid parser class (e.g., non-BaseParser implementation)."""
    pass
