def _normalize_tls(packet):
    if not packet:
        return "UNKNOWN"

    value = packet.strip().upper().replace(".", "").replace("_", "")
    return value


def assess_pqc_risk(cbom):
    overall_risk = "Low"
    risk_order = {"Low": 0, "Medium": 1, "High": 2}

    for item in cbom:
        raw_tls = item.get("tls_version")
        tls = _normalize_tls(raw_tls)
        algorithm = (item.get("algorithm_type") or "").strip().upper()
        key_strength = (item.get("key_strength") or "").strip().upper()
        cipher = (item.get("cipher") or "").strip()

        if raw_tls == "Unknown" or cipher == "Unknown":
            quantum_vulnerable = None
            risk_level = "High"
        else:
            quantum_vulnerable = algorithm in {"RSA", "ECC"}
            if tls in {"TLSV1", "TLSV11", "TLSV12", "UNKNOWN"}:
                risk_level = "High"
            elif tls == "TLSV13" and key_strength == "STRONG":
                risk_level = "Low"
            else:
                risk_level = "Medium"

        item["quantum_vulnerable"] = quantum_vulnerable
        item["risk_level"] = risk_level

        if risk_order[risk_level] > risk_order[overall_risk]:
            overall_risk = risk_level

    return cbom, overall_risk
