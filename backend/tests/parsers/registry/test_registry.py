import pytest
from app.parsers.registry.registry import ParserRegistry
from app.parsers.registry.exceptions import (
    DuplicateParserError,
    ParserNotFoundError,
    InvalidParserError
)
from app.parsers.base.base_parser import BaseParser
from app.schemas.ces import CESEvent
from app.schemas.parser import RawLog

class MockParser(BaseParser):
    def parse(self, raw_log: RawLog) -> CESEvent:
        raise NotImplementedError()

class MockParser2(BaseParser):
    def parse(self, raw_log: RawLog) -> CESEvent:
        raise NotImplementedError()

class InvalidParser:
    pass

@pytest.fixture
def registry():
    reg = ParserRegistry()
    reg.clear()
    return reg

def test_register_parser_success(registry):
    registry.register_parser("mock", MockParser)
    assert registry.has_parser("mock")
    assert registry.get_parser("mock") is MockParser
    
def test_register_parser_duplicate(registry):
    registry.register_parser("mock", MockParser)
    with pytest.raises(DuplicateParserError):
        registry.register_parser("mock", MockParser2)

def test_register_empty_source_type(registry):
    with pytest.raises(ValueError):
        registry.register_parser("", MockParser)

def test_register_invalid_parser_class(registry):
    with pytest.raises(InvalidParserError):
        registry.register_parser("invalid", InvalidParser)
        
def test_register_not_a_class(registry):
    with pytest.raises(InvalidParserError):
        registry.register_parser("invalid", "not_a_class") # type: ignore

def test_get_parser_success(registry):
    registry.register_parser("mock", MockParser)
    assert registry.get_parser("mock") is MockParser
    
def test_get_parser_not_found(registry):
    with pytest.raises(ParserNotFoundError):
        registry.get_parser("nonexistent")

def test_has_parser(registry):
    assert not registry.has_parser("mock")
    registry.register_parser("mock", MockParser)
    assert registry.has_parser("mock")
    
def test_list_parsers(registry):
    registry.register_parser("mock1", MockParser)
    registry.register_parser("mock2", MockParser2)
    parsers = registry.list_parsers()
    assert len(parsers) == 2
    assert "mock1" in parsers
    assert "mock2" in parsers

def test_unregister_parser(registry):
    registry.register_parser("mock", MockParser)
    assert registry.has_parser("mock")
    registry.unregister_parser("mock")
    assert not registry.has_parser("mock")
    with pytest.raises(ParserNotFoundError):
        registry.get_parser("mock")

def test_unregister_nonexistent_parser(registry):
    registry.unregister_parser("nonexistent")

def test_metadata_defaults(registry):
    registry.register_parser("mock", MockParser)
    metadata = registry.get_metadata("mock")
    assert metadata["name"] == "mock"
    assert metadata["enabled"] is True
    assert metadata["version"] == "1.0"

def test_metadata_custom(registry):
    registry.register_parser("mock", MockParser, version="2.0", author="tester")
    metadata = registry.get_metadata("mock")
    assert metadata["version"] == "2.0"
    assert metadata["author"] == "tester"

def test_get_metadata_not_found(registry):
    with pytest.raises(ParserNotFoundError):
        registry.get_metadata("nonexistent")

def test_set_enabled(registry):
    registry.register_parser("mock", MockParser)
    assert registry.is_enabled("mock") is True
    registry.set_enabled("mock", False)
    assert registry.is_enabled("mock") is False

def test_set_enabled_not_found(registry):
    with pytest.raises(ParserNotFoundError):
        registry.set_enabled("nonexistent", False)

def test_is_enabled_not_found(registry):
    with pytest.raises(ParserNotFoundError):
        registry.is_enabled("nonexistent")

def test_singleton_behavior():
    reg1 = ParserRegistry()
    reg2 = ParserRegistry()
    assert reg1 is reg2
