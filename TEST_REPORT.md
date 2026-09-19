# Test report

Run date: 2026-09-19 (Linux development container, Python 3.14.4)

## Automated result

Command: `python -m pytest -q -ra`

* **15 tests passed** (parser, graph sampler/root, statistics, distributions and JSON
  persistence).
* **1 module skipped** (`tests/test_engine.py`, 12 SymPy-backed cases) because outbound
  package installation is blocked in this container and SymPy is not preinstalled.
* **0 failed**.

`python -m compileall -q classpad tests run.py` also completed successfully.

The skipped engine module covers arithmetic, fractions, radicals, trigonometry,
combinatorics, complex arithmetic, equations, integration and assignments and is
mandatory in the Windows build script after dependencies are installed.

## Reference workflow matrix

| Input/workflow | Documented target | Replica expectation | Automated |
|---|---|---|---|
| `1/2+1/3` EXE | `5/6` | `5/6` | Defined; dependency-blocked here |
| `sqrt(8)` EXE | `2√2` | `2√2` display | Defined; dependency-blocked here |
| `x^2-5x+6=0`, Interactive Solve | `x=2, x=3` | `[2, 3]` natural list | Defined; dependency-blocked here |
| `(x-6)^2`, Interactive Integrate | polynomial antiderivative | `x³/3−6x²+36x` | Defined; dependency-blocked here |
| graph `x^2-4`, Root | `(-2,0)`, `(2,0)` | both roots | Passed core test |
| list `1,2,3,4,5`, 1-Var | mean 3, σ≈1.4142, s≈1.5811 | matches | Passed |

## Manual/UI and packaging status

An X server and Windows host are unavailable in this container, so interactive visual
smoke testing, screenshot capture, DPI checks and the Windows PE build are not claimed.
Run `build.bat` on Windows; it deliberately gates packaging on the complete test suite.
