from abc import ABC, abstractmethod
from typing import Any, Dict
from app.schemas.ces import CESEvent
from app.transformers.exceptions import TransformationError, EventValidationError
from pydantic import ValidationError

class BaseTransformer(ABC):
    """
    Abstract base class for all CES transformers (parsers).
    Defines the contract for converting raw events into validated CESEvents.
    """
    
    @abstractmethod
    def parse(self, raw_event: Any) -> Dict[str, Any]:
        """
        Parses a raw event into a dictionary matching the CESEvent schema.
        Must be implemented by subclasses.
        """
        pass
        
    def transform(self, raw_event: Any) -> CESEvent:
        """
        Transforms a raw event into a validated CESEvent.
        Provides base exception handling and strict schema enforcement.
        """
        try:
            parsed_data = self.parse(raw_event)
        except Exception as e:
            if isinstance(e, TransformationError):
                raise
            raise TransformationError(f"Failed to parse raw event: {str(e)}", raw_event=raw_event) from e
            
        try:
            return CESEvent(**parsed_data)
        except ValidationError as e:
            raise EventValidationError(f"CES validation failed: {str(e)}", raw_event=raw_event) from e
