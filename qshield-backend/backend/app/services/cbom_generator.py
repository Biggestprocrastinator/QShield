def _algorithm_type_from_cipher(cipher):
    if not cipher:
        return "UNKNOWN"

    upper = cipher.upper()
    if "RSA" in upper:
        return "RSA"
    if "ECDHE" in upper or "ECDSA" in upper:
        return "ECC"
    return "UNKNOWN"


def _key_strength_from_cipher(cipher):
    if not cipher:
        return "MODERATE"

    upper = cipher.upper()
    if "AES" in upper or "CHACHA20" in upper:
        return "STRONG"
    if "CBC" in upper or "3DES" in upper:
        return "WEAK"
    return "MODERATE"


def generate_cbom(crypto_results):

    cbom = []

    for item in crypto_results:
        if "error" in item:
            cbom.append({
                "domain": item.get("domain"),
                "tls_version": item.get("tls_version") or "Unknown",
                "cipher": item.get("cipher") or "Unknown",
                "key_size": item.get("key_size"),
                "certificate_algo": item.get("certificate_algo"),
                "algorithm": item.get("algorithm"),
                "signature": item.get("signature"),
                "algorithm_type": "UNKNOWN",
                "key_strength": "WEAK",
                "quantum_vulnerable": True
            })
            continue

        tls_version = item.get("tls_version") or "Unknown"
        cipher = item.get("cipher") or "Unknown"
        key_strength = _key_strength_from_cipher(cipher)
        cert_algo = (item.get("certificate_algo") or "").strip().upper()

        algorithm_type = _algorithm_type_from_cipher(cipher)
        if cert_algo in {"ECC", "RSA"}:
            algorithm_type = cert_algo

        quantum_vulnerable = not (tls_version == "TLSv1.3" and key_strength == "STRONG")

        certificate = item.get("certificate", {"expiry_days": None, "expiry_date": "Unknown"})
        cbom.append({
            "domain": item.get("domain"),
            "ip": item.get("ip"),
            "tls_version": tls_version,
            "cipher": cipher,
            "key_size": item.get("key_size"),
            "certificate_algo": item.get("certificate_algo"),
            "algorithm": item.get("algorithm"),
            "signature": item.get("signature"),
            "algorithm_type": algorithm_type,
            "key_strength": key_strength,
            "quantum_vulnerable": quantum_vulnerable,
            "ports": item.get("ports", {"80": False, "443": False}),
            "security_headers": item.get("security_headers", {
                "hsts": False,
                "csp": False,
                "x_frame_options": False,
                "x_content_type_options": False,
            }),
            "certificate": certificate,
            "certificate_status": item.get("certificate_status", "UNKNOWN"),
            "services": item.get("services", []),
            "outdated_services": bool(item.get("outdated_services")),
            "type": (item.get("type") or "server"),
        })

    return cbom
