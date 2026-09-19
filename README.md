# Open ClassPad

Open ClassPad is an independent, offline, desktop recreation of the touchscreen
worksheet workflow of the Casio ClassPad II. It is **not affiliated with or endorsed
by Casio** and contains no Casio firmware, ROM, binaries, fonts, or copied artwork.

## What works

* portrait application launcher and application switching;
* selectable, reusable Main worksheet history and multi-page soft keyboard;
* exact/decimal arithmetic, implicit multiplication, assignments and natural display;
* Interactive simplify, expand, factor, partial fractions, solve, differentiation,
  integration, substitution and approximation;
* Graph & Table with five functions, axes/grid, discontinuity-safe drawing, trace,
  roots, view window and generated tables;
* list statistics, one-variable summaries, linear regression, normal and binomial
  distributions;
* grid-like matrix entry with determinant, inverse and transpose;
* dedicated numerical equation solver;
* persistent settings, variables, graphs, lists and optional history.

See [FEATURE_MATRIX.md](FEATURE_MATRIX.md) and [LIMITATIONS.md](LIMITATIONS.md) for an
honest status. “Open ClassPad” is a descriptive project name; ClassPad and fx-CP400
are trademarks of their respective owner.

## Install and run from source

Install Python 3.11 or newer with Tk support, then:

```console
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py run.py
```

On Linux/macOS use `python3` and `source .venv/bin/activate`. The calculator does not
need internet access after dependencies are installed. Enter expressions in the Main
line and press **EXE** for exact output or **≈** for decimal output. Single-click an old
row to select it; double-click to reuse it. Toolbar calculus buttons apply to the
selection. Assignment is `x:=5`.

## Windows portable build

From a Windows command prompt with Python installed, run:

```bat
build.bat
```

The tested build pipeline runs tests and produces `dist\OpenClassPad.exe`, which embeds
Python and runtime libraries; end users do not need Python. The repository cannot
cross-compile or validate a Windows PE binary from its Linux CI container, so release
artifacts should be built and smoke-tested on clean Windows 10 and Windows 11 VMs.

## Tests

```console
python -m pytest
```

## Project documentation

* [research dossier](RESEARCH_DOSSIER.md) and [references](REFERENCES.md)
* [technology/architecture](ARCHITECTURE.md)
* [feature matrix](FEATURE_MATRIX.md)
* [test report](TEST_REPORT.md)
* [known limitations](LIMITATIONS.md) and [UI differences](UI_DIFFERENCES.md)

## Licence and acknowledgements

Code and original UI shapes are available under the [MIT licence](LICENSE). SymPy is
used under its own BSD licence. Research sources are acknowledged in `REFERENCES.md`.
