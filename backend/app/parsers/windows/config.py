from app.parsers.base.transformer_config import TransformerConfig
from app.parsers.windows.mappings import WINDOWS_CONFIG_DICT

windows_transformer_config = TransformerConfig.load_from_dict(WINDOWS_CONFIG_DICT)
