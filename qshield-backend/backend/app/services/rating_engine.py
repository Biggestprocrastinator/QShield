def calculate_rating(cbom):

    total_score = 0
    count = len(cbom)

    if count == 0:
        return {
            "score": 0,
            "rating": "Critical",
            "quantum_status": "High Risk",
            "classical_security": "Weak",
        }

    vuln_count = 0
    tls_versions = []
    for item in cbom:
        score = 0
        tls = (item.get("tls_version") or "").strip()
        cipher = (item.get("cipher") or "").upper()
        quantum = item.get("quantum_vulnerable")
        tls_versions.append(tls)

        if tls == "TLSv1.3":
            score += 40

        if "AES" in cipher or "CHACHA20" in cipher:
            score += 40

        if quantum is True:
            score -= 30
            vuln_count += 1
        elif quantum is False:
            score += 20

        total_score += max(score, 0)

    avg_score = max(total_score // count, 0)

    if avg_score >= 85:
        rating = "Elite"
    elif avg_score >= 70:
        rating = "Standard"
    elif avg_score >= 50:
        rating = "Legacy"
    else:
        rating = "Critical"

    vuln_ratio = vuln_count / count
    if vuln_ratio > 0.7:
        quantum_status = "High Risk"
    elif vuln_count > 0:
        quantum_status = "Vulnerable"
    else:
        quantum_status = "Safe"

    if all(version == "TLSv1.3" for version in tls_versions if version):
        classical_security = "Strong"
    elif any(version in {"TLSv1", "TLSv1.1"} for version in tls_versions):
        classical_security = "Weak"
    else:
        classical_security = "Moderate"

    return {
        "score": avg_score,
        "rating": rating,
        "quantum_status": quantum_status,
        "classical_security": classical_security,
    }
