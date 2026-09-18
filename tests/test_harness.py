import pathlib
import tempfile

from serialbench.adapters import xml, json, yaml, toml
from serialbench.runner import run_format
from serialbench.test_data import load

SMALL = {
    "xml": '<r><book id="1"><price>42</price></book></r>',
    "json": '{"a": 1, "b": [1, 2]}',
    "yaml": "a: 1\nb:\n  - x\n",
    "toml": "a = 1\n[b]\nc = 'x'\n",
}


def _registry(fmt):
    return {"xml": xml, "json": json, "yaml": yaml, "toml": toml}[fmt].REGISTER


def test_capability_protocol():
    etree = [c for c in xml.REGISTER if c.name == "elementtree"][0]
    assert etree().supports("generate")
    assert not etree().supports("xpath")

    tomllib = [c for c in toml.REGISTER if c.name == "tomllib"][0]
    assert tomllib().supports("parse")
    assert not tomllib().supports("generate")


def test_round_trips():
    for fmt in ("xml", "json", "yaml", "toml"):
        for cls in _registry(fmt):
            adapter = cls()
            if not adapter.available or not adapter.supports("generate"):
                continue
            assert adapter.parse(adapter.generate(adapter.parse(SMALL[fmt]))) is not None, fmt


def test_all_registered_adapters_parse():
    from serialbench.adapters import json, toml, xml, yaml

    registries = {"xml": xml, "json": json, "yaml": yaml, "toml": toml}
    docs = {"xml": "<a><b/></a>", "json": '{"a": [1]}', "yaml": "a: 1\nb:\n- x\n", "toml": "a = 1\n"}
    measured = 0
    for fmt, mod in registries.items():
        for cls in mod.REGISTER:
            adapter = cls()
            if not adapter.available:
                continue
            parsed = adapter.parse(docs[fmt])
            assert parsed is not None, fmt
            measured += 1
    assert measured >= 6, f"expected the core field to be measurable, got {measured}"


def test_xquery_xslt_ops_on_capable_adapters():
    from serialbench.runner import OPERATIONS

    data = {"small": {"xml": "<books><book id=\"1\"><price>42</price></book></books>"}}
    rows = run_format("xml", data, sizes=("small",))
    ops = {r["adapter"] for r in rows.get("xquery", [])}
    assert "leptris" in ops


def test_runner_produces_rows(tmp_path):
    data = {"small": {f: SMALL[f] for f in ("json",)}, "medium": {}, "large": {}}
    result = run_format("json", data, sizes=("small",))
    assert result["parsing"], "parsing rows missing"
    assert all(r["iterations_per_second"] > 0 for r in result["parsing"])
    assert result["memory"], "memory rows missing"
