# Familia MAGNOS – Mesas magnéticas electropermanentes MFRS2

Fuentes: catálogo MFRS2 (2026-09-22) y MAGNOS_MASTER_v2.xlsx de Arturo (mesas y unidades de
control de 220 V, que el catálogo solo menciona "bajo consulta"). 106 productos, validados contra
ambos archivos.

## Cómo se pide

El usuario da el **voltaje** y la mesa de cualquiera de estas formas; el script las resuelve
todas, así que pásale el texto tal cual:

- Solo medidas: `430 x 430`, `430x430` (con serie opcional: `A2-050 430 x 430`).
- ID: `1663682`.
- Denominación del catálogo:
- Mesas 400/460 V: `MFRS2-A2-050 600 x 430` (denominación del catálogo).
- Mesas 220 V: el voltaje va en el nombre → `MFRS2-A2-050 600 x 430 220V`.
- Con interfaz VERO-S: `MFRS2-V-A1-050 …` (el usuario la pide "con interfaz VERO-S").

Series: A1-050, V-A1-050, A2-050 (polo 50) y A1-070, A2-070 (polo 70); además, una mesa de la
generación anterior MFRS (ver "Notas de datos"). A1 = altura 66 mm,
A2 = altura 86 mm (más fuerza con cámara de aire grande). 220 V solo existe en A2-050, en 8 tamaños.

Respuestas del script:
- `SELECCIONADA POR MEDIDAS` → solo hay una mesa con esas medidas y voltaje; continúa con ella.
- `VARIAS OPCIONES` → muestra la lista (ID, serie, polo, polos, altura, fuerza) y pregunta.
- `NO EXISTE` → la búsqueda ya revisó todas las mesas por medidas; dilo y ofrece la alternativa
  que indique el script.

**No hay voltaje por defecto.** Si falta, pregúntalo. Si la combinación no existe, dilo de
inmediato (solo cuando el script responda `NO EXISTE`) y remite a
clampingsolution@mx.schunk.com para requerimientos especiales.

## Sistema completo (siempre)

Cada mesa se cotiza con su propio sistema completo, de forma unitaria:

```
python3 scripts/buscar.py sistema "<denominación>" --voltaje <220|400/460> --xlsx … [--partidas …]
```

| Orden | Línea | Regla |
|---|---|---|
| 1 | Mesa | La pedida (Qty 1) |
| 2 | Unidad de control KEH plus | Mismo voltaje (460 V/60 Hz o 220 V/60 Hz) y mismos canales que la mesa |
| 3 | Cable de conexión (5 m) | 1 canal → VBK2-5 1x4P-1x4P 1CH; 2 canales 7 pines → VBK2-5 1xIL-1x7P 2CH |
| 4 | Botonera (sin HKR) | Según canales de la unidad: HABE KEH plus 01 / 02 |
| 5 | Extensiones de polo fijas | Siempre **3 piezas** |
| 6 | Extensiones de polo flexibles | **Polos de la mesa − 3** piezas (sin tope) |

Extensiones por defecto:

| Polo | Fija | Flexible |
|---|---|---|
| 50 x 50 | PVF 50-54 (0420091) | PVB 50-54 EASYTURN (0420092) |
| 70 x 70 | PVF 70-70 (0422997) | PVB 70-70 EASYTURN (0422996) |

Otras alturas (PVF 50-20, PVF 50-32, PVB 50-32, PVF 70-30, PVF 70-47, PVB 70-47) solo si el usuario
las pide; fijas y flexibles deben tener la misma altura.

## Mesas MFRS2-V con VERO-S

Si el usuario pide una mesa MFRS2-V "con VERO-S", agrega `--vero-s` al comando `sistema`: suma, desglosados,
la estación NSL3 indicada para esa mesa, 4× BRR 50 y los pernos SPA/SPB/SPC 40-K (no el paquete
promocional; ver `references/veros.md`). Ninguna otra mesa lleva VERO-S.

## Productos que existen solo a pedido

No se agregan al sistema, pero se cotizan si el usuario los pide explícitamente:
KEH plus 04 y 08, cables de 10 m, cables para varias mesas (2x/3x/4x), cable ILME/ILME y
cajas de conexiones VBB2. Botoneras HABE KEH plus 04 y 08 también quedan a pedido.

## Fuera de la skill (no se cotizan de momento)

Mesas redondas MFRR, unidades de control 400 V/50 Hz, botoneras con regulación de fuerza (HKR),
cambio rápido QCS, bloques y placas de polos (PEB/PVP), tope WSA, componentes PLC, juegos de
tornillos ASM, garras SPR y pines para la versión VERO-S (SPA/SPB/SPC 40-K, GFD-SP 40).
Si los piden, indica que por ahora no están en la skill.

## Descripciones y nomenclatura

- Voltaje de las mesas: "400/460 V" o "220 V". Unidades de control: "460 V/60 Hz" o "220 V/60 Hz".
- La descripción de la mesa incluye polo, imán, tamaño, voltaje, número de polos y fuerza máxima
  en kN y toneladas (t = kN / 9.80665, un decimal).
- Columna Use: Mesa magnética, Unidad de control, Cable de conexión, Control remoto manual,
  Extensiones de polo.

## Notas de datos

- **1416402 – MFRS-A2-050 1000 x 230 220V**: mesa de la generación anterior MFRS (no está en el
  catálogo MFRS2). Datos del usuario: 36 polos, 4 pines, 1 canal, altura 86 mm, fuerza igual a la
  MFRS2-A2-050 de 36 polos (141 kN). Peso no disponible. Lleva el mismo sistema que una A2-050 de 220 V.

- Mesas de 220 V: fuerza, polos y peso son los de su versión 400/460 V del mismo tamaño.
- En MAGNOS_MASTER_v2.xlsx, las mesas MFRS2-V-A1-050 aparecen con polo "70 x 70" y la 1594962
  con altura 50; el catálogo indica polo 50 x 50 y altura 66 (la skill usa el catálogo).
