# -*- coding: utf-8 -*-
#
# BSD 2-Clause License
# Copyright (c) 2026 Riocloud
#
"""
URL validation — blocks SSRF attempts (private IPs, metadata endpoints, DNS rebinding).

Security fix based on x-reader: https://github.com/runesleo/x-reader/commit/733c913
"""

import ipaddress
import socket
from urllib.parse import urlparse

# Private/reserved networks that should never be accessed via user-supplied URLs
_BLOCKED_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),  # link-local + AWS metadata
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fd00::/8"),
]


def validate_url(url: str) -> str:
    """
    Validate a URL is safe to fetch (not targeting internal resources).

    Checks:
    1. Scheme must be http or https
    2. Hostname must exist
    3. Resolved IP must not be private/loopback/link-local

    Returns the validated URL. Raises ValueError if blocked.
    """
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Blocked: unsupported scheme '{parsed.scheme}'")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Blocked: no hostname in URL")

    # Resolve hostname to IP — catches DNS rebinding (evil.com → 127.0.0.1)
    try:
        resolved = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror:
        raise ValueError(f"Blocked: cannot resolve hostname '{hostname}'")

    for family, _, _, _, sockaddr in resolved:
        ip = ipaddress.ip_address(sockaddr[0])
        for network in _BLOCKED_NETWORKS:
            if ip in network:
                raise ValueError(
                    f"Blocked: '{hostname}' resolves to private address {ip}"
                )

    return url
