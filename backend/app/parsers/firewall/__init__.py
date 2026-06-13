from app.parsers.registry.registry import registry
from app.parsers.firewall.firewall_parser import FirewallParser

registry.register_parser("firewall", FirewallParser)

__all__ = ["FirewallParser"]
