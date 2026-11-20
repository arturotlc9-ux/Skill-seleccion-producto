# Familia KSP3 – Prensas de sujeción neumáticas TANDEM KSP3

Fuente: catálogo "KSP3 Baureihe", sección en español, fecha 2026-09-16 (322 IDs, todos validados contra el PDF).

## Cómo leer la denominación

`<serie> <tamaño>[-Z][-AS][-PM]`

| Parte | Significado |
|---|---|
| KSP3 | Carrera estándar, movimiento sincronizado al centro |
| KSP3-LH | Carrera larga, movimiento sincronizado al centro |
| KSP3-F | Con mordaza fija (la fuerza mueve hacia la mordaza fija) |
| Tamaños | 64, 100, 140, 160, 200, 250, 315 |
| -Z | Orificios de posicionamiento con plantilla (±0,01 mm al centro) |
| -AS | Amplificación de fuerza por resortes en sujeción externa |
| -PM | Detección neumática de posición + transferencia de aire a la mordaza |

Cada tamaño tiene 24 variantes (3 series × 8 combinaciones de opciones).
El usuario siempre indica el modelo exacto: úsalo tal cual y no preguntes por variantes.

## Glosario del usuario (términos → producto)

| Lo que pide el usuario | Producto |
|---|---|
| Mordazas (genérico, sin especificar) | **KTR** del tamaño (valor por defecto) |
| Mordazas tongue and groove blandas | KTR |
| Mordazas tongue and groove blandas altas | KTR-H |
| Mordazas serración blandas | STR |
| Mordazas serración blandas altas | STR-H |
| Mordazas para 5 ejes | S5A-G5 |
| Mordazas péndulo | Kit: 1× KTP 160 + 1× KTA 160 + 4× GBG-6W 38-38-18 (solo KSP3 160) |
| Adaptador estándar | KSL3 del tamaño (placa de consola; existe de 64 a 200) |
| Grasa | Cartucho LP 410 |
| Grasera / pistola de grasa | Pistola de engrase (la prensa ya trae su grasera integrada) |

"Alta" o "de mayor altura" indica la versión H (STR-H, KTR-H). STR-H no existe en tamaño 140:
si la piden para 140, dilo y ofrece STR 140 o KTR-H 140.

Mordazas péndulo en otro tamaño que no sea 160: no existen en el catálogo; dilo.
Adaptador estándar para 250 o 315: no hay KSL3 en esos tamaños; dilo (no sustituyas por
ABP-h plus sin que el usuario lo pida).

## Compatibilidad por tamaño

El catálogo indica los accesorios como "Indicado para KSP3 <tamaño>". Esa compatibilidad aplica
a las tres series (KSP3, KSP3-LH, KSP3-F) y a todas las opciones del mismo tamaño, sin
excepciones (confirmado por el usuario).

## Dependencias entre accesorios

- **Mordazas superiores GB\*, GFA, GFB, GBN-P, GVA, GPE, GPL** se montan sobre la mordaza
  portadora **TBA-D** del tamaño (la interfaz W-xx debe coincidir). Si el usuario pide una
  mordaza superior, incluye también la TBA-D del tamaño y avísalo.

  | Tamaño | TBA-D | Interfaz para mordazas superiores |
  |---|---|---|
  | 64 | No existe | — (solo mordazas de sistema y en bruto) |
  | 100 | TBA-D 100 (0402294) | W-65-1 |
  | 140 | TBA-D 140 (1349715) | W-90-1 / W-100-1 |
  | 160 | TBA-D 160 (0402295) | W-100-1 |
  | 200 | TBA-D 200 (1498197) | W-100-1 |
  | 250 | TBA-D 250 (0402296) | W-125-1 |
  | 315 | TBA-D 315 (1498198) | W-160 |

- **Ojo con la denominación de mordazas superiores**: `GBS-G5 160-50-13.5` = ancho 160 mm,
  interfaz W-160 → solo KSP3 315. No confundir con el tamaño de la prensa.
- **Mordazas reversibles de 6 vías (W-38)**: solo KSP3 160, con placa giratoria KTP 160 y
  placa adaptadora KTA 160 (ambas). Es el sistema péndulo: 1 KTP + 1 KTA + 4 mordazas
  GBG-6W 38-38-18, contadas por pieza.
- **Mordazas con ranura en T (GBS-Gx-T)**: la barra de posicionamiento GPL es opcional; inclúyela
  solo si el usuario la pide.
- **Placas de consola KSL3 / placas base ABP-h plus**: pueden requerir pines SPx, perno IXB V1 o
  brida BRR 50 según el montaje (el script los lista como accesorios de la placa).
  Agrégalos solo si el usuario indica el tipo de montaje.
- **GFB 100/125/160 (repuestos)**: resortes de repuesto para las mordazas de tracción GFA; no
  confundir con las mordazas GFB 100-34-10 / GFB 125-39-10.

## Mordazas de sistema (montaje directo en la prensa)

S3A-G5, S5A-G5, STR, STR-H, KTR, KTR-H, STR-S: se eligen por tamaño y no necesitan portadora.

- **Sufijo H = mayor altura** (STR-H, KTR-H). Usa la versión estándar (STR, KTR) salvo que el
  usuario pida mordazas altas o de mayor altura; en ese caso usa la versión H.
- "Tongue and groove" / lengüeta y ranura / soft jaws con ranura y espiga → KTR (o KTR-H si son altas).

## Lubricación

- Grasa correcta para KSP3: **Cartucho LP 410 (0184213)**; la pistola de engrase (9900543) es opcional.
- **LINOMAX plus (1342585)** aparece en el catálogo pero es para chucks de torno y lunetas: no
  la ofrezcas para KSP3.

## Lo que NO existe en esta familia

KSP3 es de accionamiento neumático: el catálogo no incluye torquímetro, dado, llave ni
manivela. Si los piden, indícalo y pregunta si se refieren a otro producto (p. ej. una prensa
mecánica).

## Advertencias del catálogo

- KSP3 64: no existe TBA-D (confirmado), así que no lleva mordazas superiores. Las mordazas
  65-xx (W-65-1) son para TBA-D 100.
- STR-H no existe en tamaño 140.
- Mordazas con interfaz "W-90" (GBC/GBP/GBW/GBG 90-35-xx) son compatibles con la portadora
  TBA-D 140 "W-90-1" (confirmado); el catálogo usa las dos notaciones.
- 1409319 aparece en el catálogo como "KSP3-LH 200-AS-Z"; en los datos está como "KSP3-LH 200-Z-AS".
- KSP3 315-AS y 315-AS-PM no tienen la marca de "AS" en la tabla del catálogo; la
  denominación y la fuerza por resorte indican que sí la llevan.
- GBC 65-22-8 y GBP 65-22-7.7 indican ancho 64 mm en la tabla (posible errata).
