# Shryftoriz merch — 3D models

Parametric CadQuery models for Shryftoriz merch, ready for production.

| Item | Script | Outputs | Made by |
|---|---|---|---|
| Pendant 23.5 × 14.5 × 1.0 mm, D-profile bail Ø1.8 hole, 1.5 mm walls | `pendant/src/build_pendant.py` | `pendant_d18.step/.stl` + outline DXF in `pendant/out/` | metal 3D print (JLC3DP SLM/BJ 316L) |
| Bottle-opener tag 90 × 139 × 2 mm, logo cut through | `tag/src/build_tag.py 27 6` | STEP, STL, DXF, PNG in `tag/out/` | laser cut 2 mm stainless sheet |

`source/` holds the original 32 mm pendant model the scripts start from.

## Setup (macOS / Linux)
```
python3 -m venv .venv && .venv/bin/pip install cadquery matplotlib
.venv/bin/python pendant/src/build_pendant.py      # run from repo root
.venv/bin/python tag/src/build_tag.py 27 6         # cap gap mm, margin mm
```
Open the STEP files in FreeCAD (free) to inspect or edit.

## Production rules (JLC3DP, metal)
- Walls ≥ 1.5 mm (2.0 mm optimal); fine tips below ~1 mm may print soft.
- Upload STL for 3D print; DXF for laser cut; STEP for CAD/casting factories.

## Live 3D previews (agtc)
- Pendant brief (EN/PT/UK): https://agtc.app/artifacts/1f8c94a7-79e3-43dd-bf47-12b4db3e2e90
- Pendant 3D: https://agtc.app/artifacts/545fb77b-3e1a-4285-911c-688a95e0984f
- Opener tag 3D: https://agtc.app/artifacts/7d5f19d5-31b9-47ec-81ac-5350504724f1

## Галерея локально

```bash
git clone https://github.com/asukhariev/3d-merch && cd 3d-merch && python3 -m http.server 8000
```

Відкрити http://localhost:8000 — усі моделі в 3D. Нова модель = один рядок у `MODELS` в `index.html`.
