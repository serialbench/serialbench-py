# serialbench-py

The Python harness of the serialbench benchmark family. Measures the canonical
byte-identical fixtures from [serialbench/fixtures](https://github.com/serialbench/fixtures)
against Python serialization libraries, and pushes results to
[serialbench/data](https://github.com/serialbench/data) in the shared schema —
which is what makes numbers comparable across the Ruby, Python, and C harnesses.

## Architecture (ports the Ruby harness)

- **Capability set** per adapter (`capabilities: frozenset`) — one source of
  truth; features derive from it; unavailable adapters are probe-skipped and
  log their reason (never silent).
- **OPERATIONS table** — parsing / generation / xpath / streaming (+ memory
  profiling via `tracemalloc`; labeled python-heap, since C-extension
  allocations are invisible to it — time is the cross-runtime metric).
- **Same iteration discipline** — warmup 3, then small:10 / medium:3 / large:1.

## Run

```sh
pip install -e '.[adapters,tris]'
git clone --depth 1 https://github.com/serialbench/fixtures.git fixtures
serialbench run --format xml --platform-name macos-26 --out results/xml/results.yaml
```
