from abc import ABC, abstractmethod
import uuid
import logging
from typing import Any, Dict, Optional

from app.schemas.ces import CESEvent, SourceType, Severity
from app.schemas.parser import RawLog

logger = logging.getLogger(__name__)

class BaseParser(ABC):
    """
    Abstract base class for all ASTRA Parsers.
    Parsers are responsible for converting raw log strings into validated CESEvents.
    """

    @abstractmethod
    def parse(self, raw_log: RawLog) -> CESEvent:
        """
        Parses a RawLog into a standard CESEvent.
        Subclasses must implement this method. If parsing fails, they should raise an exception
        which can be handled, or return a custom/fallback CESEvent.
        """
        pass

    def parse_safe(self, raw_log: RawLog) -> CESEvent:
        """
        Wraps the parsing logic with error handling.
        If a log cannot be fully parsed due to missing data or an unknown format variant,
        outputs a fallback CESEvent categorized as 'custom' with the original raw_event intact.
        Logs must never be silently dropped.
        """
        try:
            return self.parse(raw_log)
        except Exception as e:
            logger.error(f"Failed to parse log: {str(e)}")
            return self._create_fallback_event(raw_log, str(e))

    def _create_fallback_event(self, raw_log: RawLog, error_msg: str, metadata: Optional[Dict[str, Any]] = None) -> CESEvent:
        """
        Creates a fallback CESEvent when parsing fails to ensure logs are never dropped.
        """
        from datetime import datetime, timezone

        meta = metadata or {}
        meta["parsing_error"] = error_msg
        
        return CESEvent(
            schema_version="1.0",
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            source_type=SourceType.custom,
            event_type="custom.parsing.failed",
            severity=Severity.info,
            raw_event=raw_log.raw_event,
            metadata=meta
        )
