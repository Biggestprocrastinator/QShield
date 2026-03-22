import json
import logging
import re
import shutil
import subprocess
import sys
from pathlib import Path


def _resolve_sslyze_command() -> list[str]:
    """
    Prefer a local Windows venv install, then fall back to PATH, then the
    current interpreter if SSLyze is installed in the active environment.
    """
    exe_name = "sslyze.exe" if sys.platform.startswith("win") else "sslyze"
    current_python = Path(sys.executable)

    candidates = [
        current_python.with_name(exe_name),
        Path.cwd() / "venv" / "Scripts" / exe_name,
        Path(__file__).resolve().parents[4] / "venv" / "Scripts" / exe_name,
    ]

    for candidate in candidates:
        if candidate.exists():
            return [str(candidate)]

    found = shutil.which(exe_name)
    if found:
        return [found]

    return [sys.executable, "-m", "sslyze"]


def _normalize_tls_version(version: str | None) -> str:
    if not version:
        return "Unknown"

    mapping = {
        "TLS_1_3": "TLSv1.3",
        "TLS_1_2": "TLSv1.2",
        "TLS_1_1": "TLSv1.1",
        "TLS_1": "TLSv1",
        "TLSV1_3": "TLSv1.3",
        "TLSV1_2": "TLSv1.2",
        "TLSV1_1": "TLSv1.1",
        "TLSV1": "TLSv1",
    }
    return mapping.get(version.upper(), version.replace("_", ".").replace("TLSV", "TLSv"))


def _extract_hostname(domain: str) -> str:
    return re.sub(r"^https?://", "", domain).split("/")[0].split(":")[0].strip()


def _cipher_rank(cipher_name: str, tls_version: str) -> tuple[int, int, int]:
    name = cipher_name.upper()
    is_tls13 = 1 if tls_version == "TLSv1.3" else 0
    is_chacha20 = 1 if "CHACHA20" in name else 0
    is_aes_gcm = 1 if "AES" in name and "GCM" in name else 0
    return is_tls13, is_chacha20 or is_aes_gcm, len(name)


def _select_best_cipher(results: dict) -> str:
    candidates: list[tuple[str, str]] = []

    connectivity = results.get("connectivity_result") or {}
    direct_cipher = connectivity.get("cipher_suite_supported")
    tls_version = _normalize_tls_version(connectivity.get("highest_tls_version_supported"))
    if direct_cipher:
        candidates.append((tls_version, direct_cipher))

    scan_result = results.get("scan_result") or {}
    for version_key in ("tls_1_3_cipher_suites", "tls_1_2_cipher_suites"):
        block = scan_result.get(version_key) or {}
        if block.get("status") != "COMPLETED":
            continue

        version = _normalize_tls_version(block.get("result", {}).get("tls_version_used"))
        accepted = block.get("result", {}).get("accepted_cipher_suites", [])
        for item in accepted:
            cipher = (item.get("cipher_suite") or {}).get("openssl_name") or (item.get("cipher_suite") or {}).get("name")
            if cipher:
                candidates.append((version, cipher))

    if not candidates:
        return "Unknown"

    candidates.sort(key=lambda item: _cipher_rank(item[1], item[0]), reverse=True)
    return candidates[0][1]


def _extract_certificate_details(results: dict) -> tuple[str | None, int | None]:
    scan_result = results.get("scan_result") or {}
    cert_block = scan_result.get("certificate_info") or {}
    if cert_block.get("status") != "COMPLETED":
        return None, None

    cert_result = cert_block.get("result") or {}
    deployments = cert_result.get("certificate_deployments") or []
    if not deployments:
        return None, None

    leaf = (deployments[0].get("received_certificate_chain") or [{}])[0]
    public_key = leaf.get("public_key") or {}

    algorithm = public_key.get("algorithm")
    if isinstance(algorithm, str):
        if "RSA" in algorithm.upper():
            certificate_algo = "RSA"
        elif "EC" in algorithm.upper() or "ECDSA" in algorithm.upper():
            certificate_algo = "ECC"
        else:
            certificate_algo = algorithm
    else:
        sig_oid_name = ((leaf.get("signature_algorithm_oid") or {}).get("name") or "").lower()
        if "rsa" in sig_oid_name:
            certificate_algo = "RSA"
        elif "ecdsa" in sig_oid_name or "ec" in sig_oid_name:
            certificate_algo = "ECC"
        else:
            certificate_algo = None

    key_size = public_key.get("key_size")
    if isinstance(key_size, int):
        return certificate_algo, key_size

    return certificate_algo, None


def _extract_error_message(result: subprocess.CompletedProcess[str]) -> str:
    message = (result.stderr or "").strip() or (result.stdout or "").strip()
    return message or f"SSLyze exited with code {result.returncode}"


logger = logging.getLogger(__name__)


def scan_tls(domain: str):
    hostname = _extract_hostname(domain)
    target = f"{hostname}:443"
    command = _resolve_sslyze_command()
    command += [
        "--json_out",
        "-",
        "--sni",
        hostname,
        "--certinfo",
        "--tlsv1_2",
        "--tlsv1_3",
        "--mozilla_config",
        "disable",
        target,
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=90,
            shell=False,
        )

        logger.info("scanning %s via %s", domain, command[0])
        logger.debug("sslyze command: %s", " ".join(command))
        if result.returncode != 0:
            return {
                "domain": domain,
                "tls_version": "Unknown",
                "cipher": "Unknown",
                "certificate_algo": None,
                "key_size": None,
                "error": _extract_error_message(result),
            }

        payload = (result.stdout or "").strip()
        if not payload:
            return {
                "domain": domain,
                "tls_version": "Unknown",
                "cipher": "Unknown",
                "certificate_algo": None,
                "key_size": None,
                "error": _extract_error_message(result),
            }

        logger.debug("sslyze output length=%d", len(payload))
        data = json.loads(payload)
        server_results = data.get("server_scan_results") or []
        if not server_results:
            return {
                "domain": domain,
                "tls_version": "Unknown",
                "cipher": "Unknown",
                "certificate_algo": None,
                "key_size": None,
                "error": "SSLyze returned no server scan results",
            }

        server = server_results[0]
        connectivity = server.get("connectivity_result") or {}
        tls_version = _normalize_tls_version(connectivity.get("highest_tls_version_supported"))

        cipher = _select_best_cipher(server)
        certificate_algo, key_size = _extract_certificate_details(server)
        logger.info("parsed tls=%s cipher=%s", tls_version, cipher)

        return {
            "domain": domain,
            "tls_version": tls_version,
            "cipher": cipher,
            "certificate_algo": certificate_algo,
            "key_size": key_size,
        }

    except (json.JSONDecodeError, OSError, subprocess.TimeoutExpired) as e:
        logger.error("sslyze error for %s: %s", domain, e)
        return {
            "domain": domain,
            "tls_version": "Unknown",
            "cipher": "Unknown",
            "certificate_algo": None,
            "key_size": None,
            "error": str(e),
        }
    except Exception as e:
        logger.error("unexpected error during scan of %s: %s", domain, e)
        return {
            "domain": domain,
            "tls_version": "Unknown",
            "cipher": "Unknown",
            "certificate_algo": None,
            "key_size": None,
            "error": str(e),
        }
