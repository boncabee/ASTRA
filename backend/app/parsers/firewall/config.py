from app.parsers.base.transformer_config import TransformerConfig
from app.parsers.firewall.mappings import FIREWALL_CONFIG_DICT

firewall_transformer_config = TransformerConfig.load_from_dict(FIREWALL_CONFIG_DICT)
