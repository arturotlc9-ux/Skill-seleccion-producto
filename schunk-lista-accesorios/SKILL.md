---
name: "schunk-lista-accesorios"
description: Arma listas ID/Qty/Descripción de productos SCHUNK (prensas, mesas magnéticas, VERO-S) con sus accesorios compatibles. Úsala siempre que pidan números de parte o accesorios SCHUNK.
metadata:
  version: "1.0"
---

# Lista de accesorios SCHUNK

Convierte una petición como "KSP3-LH 100 con mordazas 5 ejes, adaptador estándar y grasa" en una
lista con el formato de cotización de SCHUNK México (ID, Qty, Description, Use, precios en blanco),
usando solo datos verificados del catálogo.

En una cotización, un ID equivocado cuesta más que uno faltante. Por eso todos los IDs salen del
script; nunca se escriben de memoria ni se deducen por patrón (los IDs de un mismo tipo no son
consecutivos entre tamaños).

## Familias cargadas

| Familia | Referencia | Fuente |
|---|---|---|
| KSP3 (KSP3, KSP3-LH, KSP3-F; tamaños 64–315) | `references/ksp3.md` | Catálogo KSP3, 2026-09-16 |
| KSC3 (KSC3, KSC3-S, KSC3 grip; modelos 80-130 a 160-480) | `references/ksc3.md` | Catálogo KSC3, 2026-08-21 |
| KSC-5X (prensa 5 ejes; longitudes 320–800, alturas 142/181/252) | `references/ksc5x.md` | Catálogo KSC-5X (NL) |
| VERO-S (estaciones NSL3/NST3 y paquetes promocionales "VERO-S NSL3 200/400/600/800") | `references/veros.md` | Catálogo NSL3 + volante promocional |
| MAGNOS (mesas magnéticas MFRS2, polo 50 y 70, 400/460 V y 220 V) | `references/magnos.md` | Catálogo MFRS2, 2026-09-22 + Excel MAGNOS_MASTER_v2 |
| Vise Automation (estación VERO-S 1 vía, KSC3 -VA, almacén, dedos y bridas PGN-plus-P 80) — **solo si mencionan "vise automation"** | `references/vise-automation.md` | Vise Automation Expert Training, 2026-03-10 |

Si piden una familia que no está en la tabla, dilo claramente y no inventes datos.
Para agregar una familia nueva, sigue `references/agregar-familia.md`.

## Flujo

**Mesas magnéticas MAGNOS:** el flujo es distinto. Lee `references/magnos.md` y usa
`scripts/buscar.py sistema "<mesa>" --voltaje <220|400/460> --xlsx …`, que arma el sistema completo
(mesa, control, cable, botonera y extensiones de polo) y detecta combinaciones inexistentes.
Si falta el voltaje o la mesa no existe, dilo antes de cualquier otra cosa. Si piden una mesa
MFRS2-V "con VERO-S", agrega `--vero-s`.

**Vise Automation:** solo cuando el usuario diga "vise automation". Lee
`references/vise-automation.md` y arma la lista con la estación como base (`--base 1621657` o
`--base 1662096`), no con una prensa.

**VERO-S:** "VERO-S NSL3 200/400/600/800" son paquetes promocionales con precio guardado; lee
`references/veros.md`. Si el script avisa que la promoción venció, pide precios actualizados.

Para prensas, sigue:

1. **Identifica la prensa.** El usuario siempre indica el modelo; úsalo tal cual, sin preguntar
   por variantes (-Z, -AS, -PM) ni agregar opciones que no nombró.
   `python3 scripts/buscar.py producto "<ID o denominación>"`
   Solo si no hay coincidencia exacta, muestra las opciones con su ID y pregunta.

2. **Lee la referencia de la familia de esa prensa** (`references/ksp3.md`, `references/ksc3.md`, `references/ksc5x.md`):
   contiene el glosario de términos del usuario, los valores por defecto, las cantidades y las
   dependencias. El glosario cambia entre familias: "mordazas" es KTR en KSP3 y SGWB-G3-B en KSC3 y
   KSC-5X; el torquímetro y el dado de KSC-5X no son los de KSC3 125.

3. **Consulta los accesorios compatibles.**
   `python3 scripts/buscar.py accesorios "<ID>"`

4. **Traduce cada cosa que pidió el usuario** con el glosario de la referencia.
   - Petición genérica ("con mordazas") → usa el valor por defecto de la referencia; no preguntes.
   - Si nombra un accesorio concreto, confirma que aparezca en el resultado de `accesorios`.
     El número en el nombre de una mordaza superior es su ancho, no el tamaño de la prensa
     (GBS-G5 160-… es W-160 y va en KSP3 315, no en KSP3 160). Si no aparece, no lo incluyas:
     explica por qué y ofrece el equivalente compatible.
   - Si pide algo que no existe o no se ofrece para esa prensa (p. ej. torquímetro en una KSP3
     neumática, grasa o mordazas 5 ejes en una KSC3), dilo en una línea y no lo incluyas.
     El script marca con "NO OFRECER" los productos que existen en el catálogo pero no se cotizan.
   - Incluye solo lo que pidió más las dependencias obligatorias de la referencia (p. ej. la
     mordaza portadora TBA-D de una mordaza superior), avisando que la agregaste. No sugieras
     ni agregues accesorios opcionales.

5. **Genera la lista con el script**, siempre con `--base` y `--xlsx`:
   `python3 scripts/buscar.py lista --base <ID_prensa> --xlsx <carpeta de salida>/Lista_<modelo>.xlsx "<ID>:<qty>" ...`
   (en Claude la carpeta de salida es `/mnt/user-data/outputs`; en otras herramientas, una carpeta
   `salida/` del proyecto; en `<modelo>` usa guiones bajos en lugar de espacios, p. ej. `Lista_KSP3-LH_100.xlsx`).
   Si omites `:qty`, el script usa la cantidad por defecto del producto (p. ej. 2 piezas en las
   mordazas de sistema KSC3). Si el script lanza ALERTA, corrige la lista y vuelve a generarla
   antes de entregar.

## Formato de salida

1. La tabla en markdown que imprime el script, con las columnas
   `ID | Qty | Description | Use | Unit price (USD) | Total (USD)` y la fila
   "Grand total (USD)". Los precios van en blanco, salvo los paquetes VERO-S con promoción vigente.
2. El archivo Excel generado, presentado al usuario. Tiene el mismo diseño de la cotización
   (encabezado azul, filas celestes, total en gris) y fórmulas: Total = Qty × Unit price y
   Grand total = suma, para que se calculen al llenar los precios.
3. Debajo, solo si aplica, notas breves: dependencias agregadas, elementos no encontrados y
   alertas del script.

Orden de las filas: prensa primero, luego mordazas, placas, medición, lubricación y accesorios
de accesorios. Descripciones en español, salvo que el usuario pida otro idioma; en ese caso
traduce las columnas Description y Use al generar la respuesta y avisa que el Excel conserva
las descripciones del script en español.

**Ejemplo**

Petición: "KSP3 100 con mordazas y grasa"

| ID | Qty | Description | Use | Unit price (USD) | Total (USD) |
|---|---|---|---|---|---|
| 1382588 | 1 | KSP3 100 – Prensa neumática TANDEM KSP3, carrera estándar | Prensa de sujeción neumática |  |  |
| 0402121 | 1 | KTR 100 – Mordaza superior en bruto con ranura, espigas y agujeros de fijación (set de 2 piezas) | Mordazas blandas |  |  |
| 0184213 | 1 | Cartucho LP 410 – Grasa de alto rendimiento LP 410 (estándar para prensas TANDEM) | Lubricación |  |  |
|  |  |  |  | **Grand total (USD):** |  |

## Pasar la lista a una presentación SCHUNK

Si el usuario pide agregar la lista a una presentación, genera las partidas con el mismo script
(agrega `--partidas partidas.json` al comando `lista`) y sigue la skill
`schunk-presentaciones` (número de investigación y portada primero). Usa ese JSON tal cual como
`partidas` de la diapositiva `precio`, con `"alcance": []` y `"servicios_ampliados": []` para
productos de catálogo. Los precios van vacíos (`precio_unitario: null`) y quedan en blanco
en la diapositiva.

## Cantidades

- Por defecto, 1 por línea y por cada prensa pedida (2 prensas → prensa 2 y cada accesorio por
  prensa 2). Accesorios de uso general (medidor IFT, pistola de engrase) van en 1 aunque haya
  varias prensas, salvo que el usuario diga otra cosa.
- Mordazas: la unidad de venta depende del producto y la indica la referencia de la familia.
  KSP3: el ID es un set de 2 piezas → 1 por prensa. KSC3: las mordazas de sistema van por pieza
  → 2 por prensa. Las mordazas W-38 del péndulo van por pieza (4). El script agrega la unidad
  ("set de 2 piezas", "set de 4 piezas", "juego") a la descripción cuando aplica.
- Si el usuario da cantidades, respétalas.

## Reglas generales

- Los IDs tienen 7 dígitos con ceros a la izquierda (0402294); consérvalos así. Algunos IDs de
  SCHUNK tienen 8 dígitos: el script los acepta sin modificarlos.
- No mezcles familias sin que la compatibilidad esté registrada en los datos.
- Si el script marca algo como "POR CONFIRMAR", no lo presentes como compatible seguro.
- Si el usuario reporta una diferencia con la página de SCHUNK, gana la información más
  reciente: avísale que hay que actualizar los datos de la skill.
