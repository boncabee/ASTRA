from app.parsers.registry.registry import registry
from app.parsers.vpn.vpn_parser import VPNParser

registry.register_parser("vpn", VPNParser)

__all__ = ["VPNParser"]
