# Known limitations

This is an iterative reconstruction, not Casio software. The following differences are
intentional disclosures, not hidden placeholder features.

* History rows are selectable as whole expressions. Arbitrary two-dimensional
  subexpression selection and animated drag/drop are not yet available; double-click
  and the reuse toolbar button provide the supported workflow.
* The entry line is a calculator-aware linear editor. Results use natural Unicode
  notation, but stacked fractions, radicals with vincula, and cursor movement through
  nested two-dimensional templates need a future structured editor.
* Degree/grad mode is persisted and displayed but not yet applied to symbolic trig
  input. Radian mode is the validated calculation mode.
* Graph intersection, extrema and bounded integral algorithms are not exposed yet.
  Root, trace, table, view window, pan-ready canvas sampling and discontinuity breaks
  are functional.
* Statistics has one-variable summaries and linear regression. Other regressions,
  inferential tests, distribution families, histogram and boxplot UI remain future work.
* Spreadsheet, Geometry, Conics, 3D Graph, Sequence and Financial are honest launcher
  entries that state they are unavailable rather than presenting fake controls.
* Matrix editing is a paste-friendly row grid, not the exact ClassPad cell editor.
* Fine menu order and graph trace snapping vary by ClassPad OS release and require
  side-by-side hardware validation.
* A reproducible PyInstaller configuration is supplied, but this Linux environment
  cannot create or clean-machine-test the required Windows executable.
