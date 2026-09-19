# ClassPad II reconstruction dossier

## Scope and target

The primary behavioural target is the **fx-CP400 ClassPad II OS 3.10/3.20 family**.
ClassPad Manager is a secondary reference for window chrome and mouse operation.  This
project is an independent implementation: no firmware, ROM, executable, font, or icon
from Casio is included.

Research was performed before implementation on 19 September 2026. Network access in
the build container was blocked (the search service returned HTTP 401 and direct HTTPS
returned 403), so the implementation deliberately limits claims to observations that
can be traced to the official manuals listed in `REFERENCES.md`. Screenshot-level
measurements which could not be independently rechecked are marked approximate.

## Screen specifications

### Application launcher

| Attribute | Observation | Implementation note | Confidence |
|---|---|---|---|
| LCD | Portrait, 320 x 528 px on fx-CP400 | Fixed 320:528 logical canvas, scalable shell | High |
| Layout | Scrollable, labelled application icons in three columns | Original Unicode/shape icons; no copied artwork | High |
| Entries | Main, eActivity, Statistics, Spreadsheet, Graph & Table, 3D Graph, Geometry, Picture Plot, Interactive Differential Calculus, Conics, Physium, Numeric Solver, Sequence, Financial, Program, Communication, System | Unsupported applications are visibly labelled “not implemented” | High |
| Bottom | Persistent icon strip provides application/keyboard navigation | Home and keyboard controls retained | Medium |

### Main application

| Attribute | Observation | Implementation note | Confidence |
|---|---|---|---|
| Menus | File, Edit, Action, Interactive | Machine-readable definitions in `classpad/assets/menus.json` | High |
| Worksheet | Inputs are left aligned; evaluated outputs are right aligned; old rows remain selectable | List-backed history supports selection, reuse, copy and command application | High |
| Action vs Interactive | Action inserts command forms; Interactive applies a chosen transformation to the selected expression | Both routes use one command registry | High |
| Exact/decimal | EXE produces normal/exact evaluation; the decimal control requests an approximate result | Separate EXE and ≈ buttons | High |
| Soft keyboard | Pages include `mth`, `abc`, `cat` and `2D`; keyboard can be shown/hidden | `mth`, `abc`, and `cat` pages implemented; structural templates place the cursor | Medium |
| Status | Angle and calculation modes are visible | `Rad/Deg/Gra`, `Standard/Decimal`, and complex format shown | High |

Selection is modelled at expression-row granularity. Fine-grained two-dimensional
subexpression selection remains an explicitly documented difference.

### Graph & Table

| Attribute | Observation | Implementation note | Confidence |
|---|---|---|---|
| Editor | `y1`, `y2`, … function rows have selection/on-off controls | Ten editable rows | High |
| Window | Axes, scale, grid, zoom, pan, trace and G-Solve analysis | Custom Tk canvas, discontinuity segmentation, trace and roots | High |
| View Window | Xmin/Xmax/Xscale and Ymin/Ymax/Yscale | Persistent settings dialog | High |
| Table | Start/end/step produce x and enabled-y columns | Implemented as a real generated table | High |
| G-Solve | Root, Min, Max, Intersection and integral are offered | Numerical scanning/refinement backs the implemented analyses | Medium |

### Statistics

| Attribute | Observation | Implementation note | Confidence |
|---|---|---|---|
| Editor | Named list columns with spreadsheet-like cells | Three paste-friendly list columns | High |
| Calc | One-variable and paired/regression calculations | One-variable summary and linear regression implemented | High |
| Graph | Histogram, box plot, scatter and regression types | Histogram and scatter canvas rendering | Medium |
| Distribution | Normal, binomial and other families are grouped in distribution commands | Normal PDF/CDF/inverse and binomial PDF/CDF implemented | High |

Quartiles use the median-of-halves convention. Manuals do not completely prescribe
all small-sample quartile edge cases, so this is an approximation.

### System/settings

Calculation settings include Standard/Decimal, Rad/Deg/Gra, Real/Complex and display
precision. Graph settings include view bounds, axes and grid. Application state is
stored as JSON under the user's application-data directory. Variable and history
management are available from Main.

## Behaviour notes used by implementation

* Pressing EXE appends rather than replacing worksheet content.
* Selecting an old input or result and choosing an Interactive operation appends the
  operation's result, preserving the source row.
* Reuse copies a selected expression into the active entry line, where it can be
  edited before evaluation.
* Assignments use ClassPad's `:=` direction (`x:=5`); stored variables affect later
  evaluations and can be cleared through Variable Manager.
* Graph trace reports the active graph and an `(x,y)` coordinate; graph analysis
  returns coordinates rather than silently changing the expression editor.

## Approximation log

Exact icon pixels, toolbar spacing on every OS revision, partial-expression selection,
drag animation, graph cursor snapping, and a few menu order details could not be
validated in the offline build environment. They are isolated in data/style modules
so later comparisons can correct them without changing the maths engine.
