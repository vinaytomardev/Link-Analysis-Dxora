import ipaddress
import socket
from urllib.parse import urlparse

def validate_public_http_url(url: str) -> str:
    """Allow only public HTTP(S) destinations; helps reduce SSRF risk."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Only valid HTTP or HTTPS URLs are allowed.")
    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not allowed.")

    try:
        addresses = socket.getaddrinfo(parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80))
        for item in addresses:
            ip = ipaddress.ip_address(item[4][0])
            if not ip.is_global:
                raise ValueError("The URL must resolve to a public IP address.")
    except socket.gaierror:
        raise ValueError("The website hostname could not be resolved.")
    return url
