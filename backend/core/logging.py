import logging
import sys
import contextvars
from pythonjsonlogger import jsonlogger

correlation_id: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id", default="-")

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['correlation_id'] = correlation_id.get()

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logHandler = logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(correlation_id)s %(message)s',
        rename_fields={"levelname": "level", "asctime": "timestamp"}
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    return logger

logger = setup_logging()
