# `verification/falsifiers/` — Батарея T1–T7 и генератор контрпримеров Stage 2 (R2 `#1156`)

- `battery_t1_t7.py` — исполнимая батарея из 7 канонических экземпляров точности/неточности аффинных правил (`T1`–`T7`, эссе `2026-10-20` + первоисточники `corpus/`), решаемая точным рациональным симплексом (`Fraction`) и `SymPy` без чисел с плавающей точкой.
- `sympy_counterexample_template.py` — шаблон Stage 2 (`Falsify-First`) для поиска контрпримеров по точным рациональным сеткам с жёстким запретом пустых сеток (`grids: []` → `EmptyGridError`).
- `tests/test_falsifiers.py` — unit-тесты для `exact_lp`, батареи `T1–T7`, `evaluate_conjecture` и шаблона контрпримеров.
