import platform
import sys

def detect(platform_name: str | None = None) -> dict:
    machine = platform.machine().lower()
    arch = {"arm64": "arm64", "aarch64": "arm64", "x86_64": "x86_64", "amd64": "x86_64"}.get(machine, machine)
    name = platform_name or f"{sys.platform}-{arch}"
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    return {
        "platform_string": f"{name}-python-{version}",
        "kind": "local",
        "os": {"darwin": "macos", "linux": "linux", "win32": "windows"}.get(sys.platform, sys.platform),
        "arch": arch,
        "runtime": "python",
        "runtime_version": version,
    }

def env_key(platform_name: str) -> str:
    info = detect(platform_name)
    return f"{platform_name}-python-{info['runtime_version']}"
