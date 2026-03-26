import socket
import ssl
from datetime import datetime, timezone


def get_certificate_expiry(domain: str, port_443_open: bool = True) -> dict:
    if not port_443_open:
        return {
            "expiry_days": None,
            "expiry_date": "Unknown",
            "certificate_status": "NO_TLS",
        }

    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

        not_after = cert.get("notAfter")
        if not not_after:
            return {
                "expiry_days": None,
                "expiry_date": "Unknown",
                "certificate_status": "NO_CERT",
            }

        expiry_dt = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
        expiry_dt = expiry_dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        days_left = (expiry_dt - now).days
        status = (
            "CRITICAL"
            if days_left < 15
            else "WARNING"
            if days_left < 30
            else "OK"
        )

        return {
            "expiry_days": days_left,
            "expiry_date": expiry_dt.date().isoformat(),
            "certificate_status": status,
        }
    except Exception:
        return {
            "expiry_days": None,
            "expiry_date": "Unknown",
            "certificate_status": "UNREACHABLE",
        }

