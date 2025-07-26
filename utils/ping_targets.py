# utils/ping_targets.py

DEFAULT_TARGETS = {
    "Google DNS": "8.8.8.8",
    "Cloudflare DNS": "1.1.1.1",
    "OpenDNS": "208.67.222.222"
}

def get_ping_targets(config: dict | None = None) -> dict:
    """
    Returns a dict of name: IP/hostname to ping.
    Uses config["ping_targets"] if available, otherwise falls back to DEFAULT_TARGETS.
    """
    if config and isinstance(config.get("ping_targets"), dict):
        return config["ping_targets"]
    return DEFAULT_TARGETS
