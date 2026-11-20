# Changelog

## 1.1 — 2026-11-20

- **Corrección MAGNOS:** el script declaraba "NO EXISTE" cuando la mesa se pedía solo por medidas
  (p. ej. "430 x 430" a 220 V, que sí existe: 1663682). Ahora `sistema` acepta medidas, ID o
  denominación; si hay una sola opción la usa, si hay varias las lista, y solo responde
  NO EXISTE después de buscar por medidas en todas las series (ofrece alternativas).
- **Excel obligatorio:** `lista` y `sistema` generan siempre el Excel; sin `--xlsx` se guarda en
  `$SCHUNK_SALIDA`, `/mnt/user-data/outputs` o `./salida`.
- Reglas obligatorias en SKILL.md para cualquier modelo de IA: todo sale del script, "no existe"
  solo si el script lo dice, búsqueda por ID, Excel siempre.
- Pruebas de regresión: `python3 scripts/probar.py` (10 casos).

## 1.0 — 2026-11-20

Primera versión publicada de `schunk-lista-accesorios`.

- Familias: KSP3, KSC3, KSC-5X, VERO-S (NSL3/NST3 y paquetes promocionales) y MAGNOS MFRS2.
- Nueva familia **Vise Automation** (VISE-AUTO, 27 IDs): estaciones VERO-S de 1 vía,
  prensas KSC3 / KSC3 grip / KSC3-K -VA, cubierta lateral, almacén, dedos FIN KSC3 y bridas
  PGN-plus-P 80. Solo se usa cuando se menciona "vise automation".
  Fuente: Vise Automation Expert Training, 2026-03-10.
- Rutas de salida genéricas para usar la skill fuera de Claude.
