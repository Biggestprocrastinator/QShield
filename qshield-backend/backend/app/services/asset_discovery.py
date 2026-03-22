import logging
import socket
import subprocess
from pathlib import Path
from typing import Iterable, List, Tuple

MAX_ASSETS = 20

logger = logging.getLogger(__name__)


def _resolve_ip(domain: str):
    try:
        return socket.gethostbyname(domain)
    except Exception:
        return None


def normalize_domain(url: str) -> str:
    if not url:
        return ""

    stripped = url.strip()
    if stripped.startswith("http://"):
        stripped = stripped[len("http://") :]
    elif stripped.startswith("https://"):
        stripped = stripped[len("https://") :]

    stripped = stripped.rstrip("/").strip()
    stripped = stripped.split("/")[0]
    return stripped


def _locate_executable(name: str, fallback: str | None = None) -> List[str]:
    command = [name]
    if fallback:
        project_root = Path(__file__).resolve().parents[3]
        candidate = project_root / fallback
        if candidate.exists():
            command = [str(candidate)]
    return command


def _run_subfinder(domain: str) -> Iterable[str]:
    command = _locate_executable("subfinder", fallback="subfinder.exe") + ["-d", domain, "-silent"]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=25,
            check=False,
        )

        if result.returncode != 0:
            return []

        return [
            normalize_domain(line)
            for line in result.stdout.splitlines()
            if normalize_domain(line)
        ]

    except (subprocess.TimeoutExpired, OSError):
        return []


def _filter_live_domains(domains: List[str]) -> Tuple[List[str], bool]:
    if not domains:
        return [], True

    command = _locate_executable("httpx") + ["-silent"]
    try:
        payload = "\n".join(domains) + "\n"
        result = subprocess.run(
            command,
            input=payload,
            capture_output=True,
            text=True,
            timeout=25,
            check=False,
        )

        if result.returncode != 0:
            return domains, False

        live = [
            normalize_domain(line)
            for line in result.stdout.splitlines()
            if normalize_domain(line)
        ]

        return live, True

    except (subprocess.TimeoutExpired, OSError):
        return domains, False


def discover_assets(domain: str):
    raw_domains = [normalize_domain(domain)]
    raw_domains.extend(_run_subfinder(domain))

    seen = set()
    deduped = []
    for candidate in raw_domains:
        normalized = normalize_domain(candidate)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(normalized)

    if not deduped:
        logger.error("Subfinder returned no domains for %s", domain)
        deduped = [normalize_domain(domain)]

    print("Subfinder domains:", deduped)

    live_domains, httpx_success = _filter_live_domains(deduped)
    target_domains = (live_domains if httpx_success else deduped)[:MAX_ASSETS]

    assets = []
    for candidate in target_domains:
        assets.append(
            {
                "domain": candidate,
                "ip": _resolve_ip(candidate),
            }
        )

    return assets
