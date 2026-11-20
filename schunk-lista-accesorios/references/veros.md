# Familia VERO-S – Estaciones de sujeción NSL3/NST3 y paquetes promocionales

Fuentes: catálogo NSL3 (inglés, 40 IDs validados; descripciones traducidas) y volante promocional
SCHUNK México con 4 paquetes (vigentes al 31-dic-2026).

## Paquetes promocionales (prioridad cuando el usuario dice "VERO-S NSL3 …")

Cada paquete = **1× starter kit** + **4× BRR 50** (0470020) + **1× kit de conversión G1/8" a NPT
Parker** (1700927). El starter kit contiene la estación, los pernos y la regleta ASL 1-G1/8.

| Pide el usuario | Paquete | Starter kit | Contenido del kit | Lista | Promoción | Ahorro |
|---|---|---|---|---|---|---|
| VERO-S NSL3 200 | 1687252 | 1333465 | NSL3 200 + 5× SPA 40 + 5× SPB 40 + ASL 1-G1/8 | $5,206 | $3,610 | $1,596 |
| VERO-S NSL3 400 | 1687254 | 1333481 | NSL3 400 + 5× SPA + 5× SPB + 10× SPC 40 + ASL | $9,730 | $6,784 | $2,946 |
| VERO-S NSL3 600 | 1687255 | 1333488 | NSL3 600 + 5× SPA + 5× SPB + 15× SPC 40 + ASL | $13,102 | $9,134 | $3,968 |
| VERO-S NSL3 800 | 1687257 | 1584087 | NSL3 800 + 5× SPA + 5× SPB + 20× SPC 40 + ASL | $16,869 | $11,760 | $5,109 |

- Se cotizan en **una sola línea** (ID del paquete, Qty 1); la descripción resume el kit con su ID,
  las 4 BRR 50 y el kit de conversión.
- Los starter kits ("KIT VERO-S NSL3 200", etc.) también se pueden cotizar solos a pedido, sin precio.
- Son los únicos productos con precio guardado: el script llena el precio de promoción en la
  tabla y el Excel, y muestra lista y ahorro para mencionarlos en las notas.
- **Vigencia:** después del 31-12-2026 el script avisa que la promoción venció y deja el precio en
  blanco. En ese caso, pide al usuario los precios actualizados antes de entregar.
- Correcciones del volante confirmadas por el usuario: lista del paquete 4 = $16,869 (el volante
  dice $10,869); "SOC" = SPC; la regleta es la ASL 1-G1/8 del catálogo.
- Composición confirmada por el usuario para el paquete NSL3 200; los de 400, 600 y 800 siguen la
  misma estructura.

## Estaciones del catálogo (a pedido, sin precio)

NSL3 150-V1, 150-V1-T, 150-V4-T, 200, 200-V1-T, 400, 600, 800 y torres NST3 400-250, 500-300.
Se entregan sin pernos. Accesorios compatibles por estación con `accesorios`: pernos SPA/SPB/SPC 40
y 40-16 (SPB desde NSL3 200; SPC desde NSL3 400), antirrotación IXB V1/V1-K/V4 (solo versiones V),
extensiones SP-VL, sello KVS 40, monitoreo AFS3, regletas ASL 1-G1/8 (200–800) y ASL 2-G1/8
(200-V1-T y NST3), acoplamiento VSK, transferencia de medios MDN 3-2 y brida BRR 50.

## Estación sola

"Estación NSL3 400" (o el nombre de cualquier estación del catálogo) = la estación sola, sin pernos
ni regleta (p. ej. 1323572), sin precio. "VERO-S NSL3 400" = el paquete promocional.

## Relación con MAGNOS (MFRS2-V con VERO-S)

Solo las mesas **MFRS2-V** (interfaz VERO-S) se cotizan con VERO-S, y solo si el usuario lo pide.
En ese caso **no se usa el paquete**: se cotizan los componentes individuales, desglosados, con
`sistema … --vero-s`:

| Mesa MFRS2-V | Estación | BRR 50 | SPA 40-K | SPB 40-K | SPC 40-K |
|---|---|---|---|---|---|
| 315 x 315, 430 x 315 | NSL3 200 (1323569), 2 módulos | 4 | 1 | 1 | – |
| 430 x 430 | NSL3 400 (1323572), 4 módulos | 4 | 1 | 1 | 2 |
| 600 x 430, 800 x 600 | NSL3 600 (1323574), 6 módulos | 4 | 1 | 1 | 4 |

Regla de pernos: 1 SPA (referencia), 1 SPB (orientación) y SPC en los demás módulos. Se usan los
pernos **-K** (tornillo acortado) que el catálogo MFRS2 indica para estas mesas.
Con cualquier otra mesa, el script responde que no aplica.
