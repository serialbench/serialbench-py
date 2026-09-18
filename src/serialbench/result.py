import datetime as _dt

import yaml

from .adapters import xml, json, yaml as yaml_adapters, toml


def _serializers_information(fmt, registry):
    rows = []
    for cls in registry:
        adapter = cls()
        if not adapter.available:
            continue
        rows.append(
            {
                "name": adapter.name,
                "format": fmt,
                "version": str(adapter.version()),
                "features": adapter.features(),
            }
        )
    return rows


def write(path, fmt, platform_info, benchmark_result, benchmark_name):
    registry = {"xml": xml, "json": json, "yaml": yaml_adapters, "toml": toml}[fmt]
    document = {
        "platform": platform_info,
        "metadata": {
            "benchmark_config_path": f"serialbench-py/{benchmark_name}.yml",
            "environment_config_path": f"python-{platform_info['runtime_version']}",
            "tags": ["local", platform_info["os"], platform_info["arch"], f"python-{platform_info['runtime_version']}"],
        },
        "benchmark_config": {
            "name": benchmark_name,
            "formats": [fmt],
            "operations": ["parsing", "generation", "xpath", "xquery", "xslt", "xslt30", "validation", "streaming", "memory"],
        },
        "benchmark_result": {
            "serializers": _serializers_information(fmt, registry.REGISTER),
            **benchmark_result,
        },
    }
    with open(path, "w") as fh:
        yaml.safe_dump(document, fh, sort_keys=False, default_flow_style=False, allow_unicode=True)
