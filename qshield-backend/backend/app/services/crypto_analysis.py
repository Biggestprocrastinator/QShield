import ssl
import socket

def analyze_crypto(domain: str):
    try:
        context = ssl.create_default_context()

        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:

                cert = ssock.getpeercert()
                tls_version = ssock.version()
                cipher = ssock.cipher()

                return {
                    "domain": domain,
                    "tls_version": tls_version,
                    "cipher": cipher[0] if cipher else None,
                    "issuer": dict(x[0] for x in cert.get("issuer", [])),
                    "subject": dict(x[0] for x in cert.get("subject", [])),
                }

    except Exception as e:
        return {
            "domain": domain,
            "error": str(e)
        }