# Agregar una familia nueva

## Esquema de datos

`data/productos.csv`

| Columna | Contenido |
|---|---|
| id | ID SCHUNK de 7 dígitos, con ceros a la izquierda |
| denominacion | Como aparece en el catálogo |
| familia | Familias que lo usan, separadas por barra vertical (KSP3, KSP3/KSC3 compartido…); un ID aparece una sola vez |
| tipo | `prensa` / `chuck` / `accesorio` |
| categoria | mordaza_sistema, mordaza_superior, placa_base, lubricacion, … |
| tamano | Tamaño del producto o tamaños que cubre (separados por barra vertical) |
| interfaz | Interfaz de montaje si aplica (W-100-1, …) |
| descripcion | Descripción corta en español, usada en la lista final |
| unidad_venta | pieza / set de 2 piezas / set de 4 piezas / juego |
| cantidad_defecto | Cantidad por prensa si el usuario no la indica |
| restriccion | Texto si el producto existe pero no se ofrece (el script lo marca NO OFRECER) |
| datos | Datos técnicos clave (`clave=valor; …`) |
| fuente | Catálogo y fecha |

`data/compatibilidad.csv`

| Columna | Contenido |
|---|---|
| id_accesorio | ID del accesorio |
| aplica_tipo | `tamano` (productos base de ese tamaño/modelo en la familia), `id` (un producto concreto, también accesorios de accesorios), `interfaz` (vía cualquier accesorio del tamaño con esa interfaz: portadora, mordaza de sistema o placa) |
| aplica_valor | El tamaño, ID o interfaz |
| familia | Familia a la que aplica la relación |
| nota | Dependencias o advertencias |

## Pasos

1. Capturar productos y relaciones desde el catálogo.
2. Validar: cada ID capturado debe existir en el PDF y cada ID del PDF debe estar capturado.
3. Verificar el emparejamiento denominación–ID.
4. Crear `references/<familia>.md` con denominaciones, dependencias y advertencias.
5. Agregar la familia a la tabla de SKILL.md.
6. Si la familia usa un tipo de producto base nuevo (p. ej. `chuck`), revisar `accesorios_de()`
   en `scripts/buscar.py`: hoy la compatibilidad por tamaño se resuelve para `tipo == prensa`.
