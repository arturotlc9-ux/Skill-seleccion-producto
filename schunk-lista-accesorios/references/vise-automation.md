# Vise Automation (familia VISE-AUTO)

Fuente: "Vise Automation | Machine Tending – Expert Training" (SCHUNK, 10.03.2026).

**Solo se usa cuando el usuario mencione "vise automation".** En cualquier otra lista no uses
estos productos: una "KSC3 80-130" normal sigue siendo 1508857 (familia KSC3), no la versión
VA 1623548. Los IDs de las prensas VA son distintos a los del catálogo KSC3.

## Concepto

Unidad de automatización para carga directa de prensas con robot pequeño:
1. Estación de sujeción VERO-S de 1 vía (punto cero), conexión inferior y lateral.
2. Prensas KONTEC KSC3 con interfaz para gripper y para almacén (80-130, 80-190, 125-160).
3. Gripper PGN-plus-P 80 con dedos estándar; el gripper PGN-plus-P 80-1-AS y su brida los
   suministra SCHUNK Hausen.

Peso de manipulación hasta 20 kg (prensa + pieza), cálculo a 2G con la interfaz de gripper de
20°. Repetibilidad de sujeción de las prensas: ±0.01 mm.

## Producto base

La lista se arma siempre con la estación como base:
- `--base 1621657` — estación VERO-S de 1 vía estándar (conexión inferior y lateral: abrir,
  turbo, monitoreo de corredera abierta, limpieza por el centro del módulo).
- `--base 1662096` — estación de 1 vía con control lateral vía robot (abrir, turbo); se usa con
  la unidad de gripper con transferencia de medios 1662100.

## Glosario y valores por defecto

| El usuario dice | Usar |
|---|---|
| "KSC3 80-130" (en contexto vise automation) | KSC3 80-130-VA 1623548 |
| "KSC3 grip …" | KSC3 grip …-VA (1640163 / 1640164 / 1640167) |
| "KSC3-K …" | KSC3-K …-VA (1629373 / 1629374 / 1629375) |
| "con dedos" (genérico) | FIN KSC3 80/125 1627791 (todas las versiones) |
| "dedos de 80" | FIN KSC3 80 1634882 (solo si todas las prensas son de 80 mm) |
| "con almacén" | Sistema de almacén 1662101 (para 20 prensas) |
| "pernos de almacén" | 1627792 (pieza) o 1634883 (set de 40 piezas) |
| "pin de sujeción" | SPA 40-K 0432369 |
| "indexador" / "antirrotación" | IXB V1-K 0432371 |
| "brida" del gripper | Preguntar la brida del robot; no elegir una (8 opciones AKO) |

## Dependencias obligatorias

- KSC3(-K) 80-130-VA y 80-190-VA → cubierta lateral de virutas 1623565, una por prensa
  (cubre el módulo VERO-S). Agrégala y avisa que la agregaste.
- Pin de sujeción e indexador solo si el usuario los pide.

## Pendientes de confirmar

- Descripción completa de la brida 30057476 (en la fuente aparece cortada).
- Unidad de venta de los dedos FIN KSC3 (se capturaron como pieza).
- Las descripciones en español de las bridas AKO se derivaron de su denominación.
