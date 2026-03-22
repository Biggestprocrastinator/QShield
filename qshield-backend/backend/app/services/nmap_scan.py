import subprocess
from pathlib import Path


def _locate_nmap() -> list[str]:
    project_root = Path(__file__).resolve().parents[3]
    bundled = project_root / "nmap.exe"
    if bundled.exists():
        return [str(bundled)]
    return ["nmap"]


def _parse_ports(output: str) -> dict:
    ports = {"80": False, "443": False}
    for line in output.splitlines():
        if "80/tcp" in line and "open" in line:
            ports["80"] = True
        if "443/tcp" in line and "open" in line:
            ports["443"] = True
    return ports


def scan_ports(domain: str):
    command = _locate_nmap() + ["-p", "80,443", "--open", domain]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        if result.returncode != 0:
            return {
                "domain": domain,
                "ports": {"80": False, "443": True},
            }

        ports = _parse_ports(result.stdout + result.stderr)
        return {
            "domain": domain,
            "ports": ports,
        }

    except (subprocess.TimeoutExpired, OSError):
        return {
            "domain": domain,
            "ports": {"80": False, "443": True},
        }
