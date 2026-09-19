# Architecture and technology decision

## Choice

The application uses **Python 3.11+, Tk 8.6, SymPy, and Pillow**, packaged with
**PyInstaller**. Tk provides a native, DPI-scalable desktop window with no browser or
local server. SymPy is hidden behind `ClassPadEngine`; user input never reaches Python
`eval`. Pillow is used only for original generated assets and export. PyInstaller can
create a one-file Windows executable containing the interpreter and dependencies.

This stack favours a small, auditable desktop implementation and mature CAS behaviour.
The compatibility boundary means a future renderer or CAS can be substituted.

## Layers

```text
Tk shell/applications -> command registry -> worksheet/session models
                                      |-> safe parser -> ClassPadEngine (SymPy)
                                      |-> formatter -> natural text/Unicode display
                                      |-> graph sampler / statistics / distributions
settings store <----------------------------------------------- all applications
```

`classpad/ui` owns presentation only. `classpad/core` owns syntax, CAS, formatting,
history and persistence. `classpad/applications` contains isolated application frames.
The parser passes a fixed local dictionary to SymPy transformations, rejects unknown
function calls and limits expression size/depth; unrestricted `eval` is never used.
