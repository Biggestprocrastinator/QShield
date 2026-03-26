import logging
import socket
import subprocess
from pathlib import Path
from typing import Iterable, List, Tuple

MAX_ASSETS = 20
MAX_SUBDOMAINS = 50

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
    commands = [
        ["subfinder", "-d", domain, "-silent"],
        _locate_executable("subfinder", fallback="subfinder.exe") + ["-d", domain, "-silent"],
    ]

    for command in commands:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )

            if result.returncode != 0:
                logger.warning("Subfinder failed: %s", (result.stderr or "").strip())
                continue

            output = [
                normalize_domain(line)
                for line in result.stdout.splitlines()
                if normalize_domain(line)
            ]
            if output:
                return output

        except (subprocess.TimeoutExpired, OSError) as exc:
            logger.warning("Subfinder error: %s", exc)
            continue

    return []


def _filter_live_domains(domains: List[str]) -> Tuple[List[str], bool]:
    if not domains:
        return [], True

    cmd = _locate_executable("httpx") + ["-silent"]
    try:
        payload = "\n".join(domains)
        result = subprocess.run(
            cmd,
            input=payload,
            capture_output=True,
            text=True,
            timeout=25,
            check=False,
        )

        live = result.stdout.splitlines()
        if not live:
            live = domains

        print("HTTPX returned:", len(live))
        return live, True

    except (subprocess.TimeoutExpired, OSError):
        print("HTTPX returned: 0 (fallback)")
        return domains, False


def discover_assets(domain: str):
    subdomains = _run_subfinder(domain)
    subdomains = list(dict.fromkeys(subdomains))  # dedupe while keeping order
    subdomains = subdomains[:MAX_SUBDOMAINS]
    print("Subfinder count:", len(subdomains))
    print("Subdomains limited to:", len(subdomains))
    if not subdomains:
        fallback_subdomains = [
            f"www.{domain}",
            f"api.{domain}",
            f"mail.{domain}",
        ]
        print("Using fallback subdomains")
        subdomains.extend(fallback_subdomains)
    print("Subfinder count:", len(subdomains))
    all_domains = [
        normalize_domain(d)
        for d in [domain] + subdomains
        if isinstance(d, str) and d.strip()
    ]

    if not all_domains:
        logger.error("Subfinder returned no domains for %s", domain)
        all_domains = [normalize_domain(domain)]

    live_domains, httpx_success = _filter_live_domains(all_domains)
    domains = (live_domains if httpx_success else all_domains)[:MAX_ASSETS]
    print("Final domains count:", len(domains))

    assets = []
    for candidate in domains:
        assets.append(
            {
                "domain": candidate,
                "ip": _resolve_ip(candidate),
            }
        )

    return assets
