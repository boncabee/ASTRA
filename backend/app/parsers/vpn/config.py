from app.parsers.base.transformer_config import TransformerConfig
from app.parsers.vpn.mappings import VPN_CONFIG_DICT

# Instantiate the centralized configuration for the VPN parser
vpn_transformer_config = TransformerConfig.load_from_dict(VPN_CONFIG_DICT)
