import uuid
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.schemas.ces import CESEvent, SourceType, Severity
from app.schemas.parser import RawLog
from app.parsers.fallback.exceptions import RecoveryFailureError
from app.parsers.fallback.fallback_event import ConfidenceLevel, FALLBACK_EVENT_TYPE

logger = logging.getLogger(__name__)

class FallbackMapper:
    """
    Standardized fallback mechanism that guarantees unknown or unsupported
    events are handled safely and consistently without data loss.
    """

    @staticmethod
    def _create_fallback_event(
        raw_log: RawLog,
        reason: str,
        confidence: ConfidenceLevel,
        original_source: Optional[str] = None,
        partial_data: Optional[Dict[str, Any]] = None,
        timestamp: Optional[str] = None
    ) -> CESEvent:
        """
        Core internal method to generate a compliant fallback CESEvent.
        """
        try:
            now_iso = datetime.now(timezone.utc).isoformat()
            event_timestamp = timestamp if timestamp else now_iso
            
            # Ensure timestamp is valid ISO-8601, else fallback to now
            try:
                datetime.fromisoformat(event_timestamp.replace('Z', '+00:00'))
            except ValueError:
                event_timestamp = now_iso

            # Resolve source type safely
            source_type = SourceType.custom
            if original_source:
                try:
                    source_type = SourceType(original_source.lower())
                except ValueError:
                    source_type = SourceType.custom

            metadata: Dict[str, Any] = {
                "fallback_reason": reason,
                "fallback_timestamp": now_iso,
                "original_source_type": original_source or "unknown",
                "confidence_score": confidence.value
            }

            if partial_data:
                metadata["partial_data"] = partial_data

            event = CESEvent(
                schema_version="1.0",
                event_id=str(uuid.uuid4()),
                timestamp=event_timestamp,
                source_type=source_type,
                event_type=FALLBACK_EVENT_TYPE,
                severity=Severity.low,
                raw_event=raw_log.raw_event,
                metadata=metadata
            )
            return event
        except Exception as e:
            logger.error(f"Critical failure during fallback mapping: {e}")
            raise RecoveryFailureError(f"Failed to create fallback event: {e}")

    @classmethod
    def handle_unknown_event(cls, raw_log: RawLog, original_source: str) -> CESEvent:
        """
        Input: unknown event
        Output: valid fallback CESEvent
        """
        return cls._create_fallback_event(
            raw_log=raw_log,
            reason="unknown_event",
            confidence=ConfidenceLevel.LOW,
            original_source=original_source
        )

    @classmethod
    def handle_unknown_vendor(cls, raw_log: RawLog, vendor_name: str) -> CESEvent:
        """
        Input: vendor not registered
        Output: generic normalized CESEvent
        """
        return cls._create_fallback_event(
            raw_log=raw_log,
            reason="unknown_vendor",
            confidence=ConfidenceLevel.LOW,
            original_source=vendor_name
        )

    @classmethod
    def handle_parser_failure(cls, raw_log: RawLog, exception: Exception, original_source: str) -> CESEvent:
        """
        Input: parser exception
        Output: fallback CESEvent
        """
        return cls._create_fallback_event(
            raw_log=raw_log,
            reason="parser_failure",
            confidence=ConfidenceLevel.LOW,
            original_source=original_source,
            partial_data={"error_message": str(exception)}
        )

    @classmethod
    def handle_partial_recovery(cls, raw_log: RawLog, partial_data: Dict[str, Any], original_source: str, timestamp: Optional[str] = None) -> CESEvent:
        """
        Input: missing fields
        Output: best-effort CESEvent
        """
        return cls._create_fallback_event(
            raw_log=raw_log,
            reason="partial_mapping",
            confidence=ConfidenceLevel.MEDIUM,
            original_source=original_source,
            partial_data=partial_data,
            timestamp=timestamp
        )
