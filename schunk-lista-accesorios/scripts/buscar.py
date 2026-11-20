#!/usr/bin/env python3
"""Consulta de productos SCHUNK y accesorios compatibles.

Uso:
  python3 buscar.py producto "<ID o denominación>"     # identificar producto(s)
  python3 buscar.py accesorios "<ID o denominación>"   # accesorios compatibles agrupados
  python3 buscar.py lista --base <ID> [--xlsx ruta.xlsx]   (el Excel se genera siempre) [--partidas ruta.json] "ID:cant" ...
      # tabla final de cotización; --partidas exporta las líneas para la diapositiva de precio
  python3 buscar.py sistema "<mesa, ID o medidas p. ej. 430 x 430>" --voltaje <220|400/460> [--vero-s] [--xlsx ruta] [--partidas ruta]
      # MAGNOS: arma mesa + control + cable + botonera + extensiones de polo

Los datos viven en ../data/productos.csv y ../data/compatibilidad.csv.
"""
import csv, os, re, sys
from collections import defaultdict

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
PROD = list(csv.DictReader(open(os.path.join(BASE, 'productos.csv'), encoding='utf-8')))
COMP = list(csv.DictReader(open(os.path.join(BASE, 'compatibilidad.csv'), encoding='utf-8')))
BY_ID = {p['id']: p for p in PROD}

ORDEN_CAT = ['mordaza_sistema', 'mordaza_bruto', 'mordaza_portadora', 'mordaza_superior',
             'barra_posicionamiento', 'placa_giratoria', 'placa_adaptadora', 'placa_base', 'consola',
             'set_montaje', 'torquimetro', 'dado', 'palanca', 'tope', 'soporte', 'medicion',
             'lubricacion', 'pin_sujecion', 'antirrotacion', 'brida', 'tapon', 'fijacion_mesa', 'repuesto']


def norm(s):
    return re.sub(r'[\s\-/._]', '', s.upper())


def resolver(q):
    """Devuelve (lista_de_coincidencias, exacta: bool)."""
    q = q.strip()
    if re.fullmatch(r'\d{5,8}', q):
        p = BY_ID.get(q.zfill(7))
        return ([p] if p else []), True
    nq = norm(q)
    exact = [p for p in PROD if norm(p['denominacion']) == nq]
    if exact:
        return exact, True
    parcial = [p for p in PROD if nq in norm(p['denominacion'])]
    return parcial, False


def linea(p):
    extra = f" | interfaz {p['interfaz']}" if p['interfaz'] else ''
    datos = f" | {p['datos']}" if p['datos'] else ''
    return f"{p['id']}  {p['denominacion']}  – {p['descripcion']}{extra}{datos}"


def cmd_producto(q):
    res, exacta = resolver(q)
    if not res:
        print(f'SIN COINCIDENCIAS para "{q}". No inventes un ID: indícalo al usuario.')
        return
    print(('COINCIDENCIA EXACTA' if exacta else f'{len(res)} COINCIDENCIAS PARCIALES (confirmar con el usuario)') + ':')
    for p in res[:40]:
        print('  ' + linea(p))
    if len(res) > 40:
        print(f'  ... {len(res) - 40} más; afina la búsqueda.')


def familias(p):
    return [f for f in p['familia'].split('|') if f]


def accesorios_de(p):
    """Devuelve (dict categoria -> lista de (producto, nota), tamaño)."""
    grupos = defaultdict(list)
    vistos = set()

    def add(acc_id, nota=''):
        if acc_id in vistos or acc_id not in BY_ID:
            return
        vistos.add(acc_id)
        a = BY_ID[acc_id]
        if a.get('restriccion'):
            nota = (nota + ' | ' if nota else '') + 'NO OFRECER: ' + a['restriccion']
        grupos[a['categoria']].append((a, nota))

    tam = p['tamano'] if p['tipo'] in ('prensa', 'mesa', 'estacion') else None
    fam = familias(p)[0]
    if tam:
        for c in COMP:
            if c['familia'] == fam and c['aplica_tipo'] == 'tamano' and c['aplica_valor'] == tam:
                add(c['id_accesorio'], c['nota'])
        # Mordazas superiores: por la interfaz de las mordazas/placas portadoras de este tamaño
        portadoras = defaultdict(list)
        for lst in list(grupos.values()):
            for a, _ in lst:
                if a['interfaz'] and not a.get('restriccion'):
                    for i in a['interfaz'].split('|'):
                        portadoras[i].append(a)
        interfaces = {}
        for i, lst in portadoras.items():
            nombres = [f"{a['denominacion']} ({a['id']})" for a in lst]
            union = ' + ' if i == 'W-38' else ' o '
            interfaces[i] = 'requiere ' + union.join(nombres)
        for c in COMP:
            if c['familia'] == fam and c['aplica_tipo'] == 'interfaz' and c['aplica_valor'] in interfaces:
                if c['id_accesorio'] in vistos:
                    continue
                add(c['id_accesorio'], interfaces[c['aplica_valor']])
    # Accesorios de accesorios (y accesorios directos de un accesorio consultado)
    base_ids = [p['id']] + [a['id'] for lst in grupos.values() for a, _ in lst]
    for b in base_ids:
        for c in COMP:
            if c['aplica_tipo'] == 'id' and c['aplica_valor'] == b:
                add(c['id_accesorio'], f"para {BY_ID[b]['denominacion']} ({b})")
    return grupos, tam


def cmd_accesorios(q):
    res, exacta = resolver(q)
    if len(res) != 1:
        print('Primero identifica un único producto:')
        cmd_producto(q)
        return
    p = res[0]
    print('PRODUCTO BASE: ' + linea(p))
    grupos, tam = accesorios_de(p)
    if not grupos:
        print('Sin accesorios registrados para este producto en los datos de la skill.')
        return
    cats = sorted(grupos, key=lambda c: ORDEN_CAT.index(c) if c in ORDEN_CAT else 99)
    for c in cats:
        print(f'\n[{c}]')
        for a, nota in grupos[c]:
            print('  ' + linea(a) + (f'  <<{nota}>>' if nota else ''))
    if p['tipo'] == 'prensa' and 'KSP3' in familias(p) and 'mordaza_portadora' not in grupos:
        print(f'\nNOTA: el tamaño {tam} no tiene mordaza portadora TBA-D, por lo que no lleva '
              'mordazas superiores GB*; solo mordazas de sistema y en bruto.')


def _precio(p):
    """Precio promocional guardado (solo paquetes); avisa si la promoción ya venció."""
    import datetime
    d = dict(x.split('=', 1) for x in p['datos'].split('; ')) if p.get('datos') else {}
    if 'precio_promo' not in d:
        return None
    vig = datetime.date.fromisoformat(d['vigencia'])
    if datetime.date.today() > vig:
        print(f"AVISO: la promoción de {p['denominacion']} venció el {vig:%d-%m-%Y}. "
              'Pide al usuario los precios actualizados; el precio queda en blanco.')
        return None
    print(f"PRECIO PROMOCIÓN {p['denominacion']}: ${float(d['precio_promo']):,.0f} USD "
          f"(lista ${float(d['precio_lista']):,.0f}, ahorro ${float(d['ahorro']):,.0f}; vigente al {vig:%d-%m-%Y})")
    return float(d['precio_promo'])


def _descripcion(p):
    d = f"{p['denominacion']} – {p['descripcion']}"
    uv = p.get('unidad_venta', '')
    if uv.startswith('set') or uv == 'juego':
        d += f' ({uv})'
    return d


def _carpeta_salida():
    """Carpeta del Excel si no se pasa --xlsx: $SCHUNK_SALIDA, /mnt/user-data/outputs o ./salida."""
    if os.environ.get('SCHUNK_SALIDA'):
        return os.environ['SCHUNK_SALIDA']
    if os.path.isdir('/mnt/user-data/outputs'):
        return '/mnt/user-data/outputs'
    return os.path.join(os.getcwd(), 'salida')


def _xlsx(filas, ruta):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook(); ws = wb.active; ws.title = 'Lista'
    azul, celeste, gris = '003B6F', 'C9E9F8', 'E7E6E6'
    blanco = Side(style='thin', color='FFFFFF')
    borde = Border(left=blanco, right=blanco, top=blanco, bottom=blanco)
    enc = ['ID', 'Qty', 'Description', 'Use', 'Unit price\n(USD)', 'Total (USD)']
    for c, t in enumerate(enc, 1):
        x = ws.cell(row=1, column=c, value=t)
        x.font = Font(name='Arial', bold=True, color='FFFFFF', size=11)
        x.fill = PatternFill('solid', fgColor=azul)
        x.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        x.border = borde
    moneda = '"$"#,##0.00'
    for r, (i, cant, desc, uso, precio) in enumerate(filas, 2):
        vals = [i, int(cant) if str(cant).isdigit() else cant, desc, uso, precio, f'=IF(E{r}="","",B{r}*E{r})']
        for c, v in enumerate(vals, 1):
            x = ws.cell(row=r, column=c, value=v)
            x.font = Font(name='Arial', size=10)
            x.fill = PatternFill('solid', fgColor=celeste)
            x.border = borde
            x.alignment = Alignment(vertical='center', wrap_text=True,
                                    horizontal='left' if c in (3, 4) else 'center')
            if c in (5, 6):
                x.number_format = moneda
        ws.cell(row=r, column=1).number_format = '@'
    t = len(filas) + 2
    lab = ws.cell(row=t, column=5, value='Grand\ntotal\n(USD):')
    lab.font = Font(name='Arial', bold=True, color='FFFFFF', size=11)
    lab.fill = PatternFill('solid', fgColor=azul)
    lab.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    tot = ws.cell(row=t, column=6, value=f'=SUM(F2:F{t - 1})')
    tot.font = Font(name='Arial', size=14)
    tot.fill = PatternFill('solid', fgColor=gris)
    tot.alignment = Alignment(horizontal='center', vertical='center')
    tot.number_format = moneda
    ws.row_dimensions[1].height = 32
    ws.row_dimensions[t].height = 48
    for col, w in zip('ABCDEF', (11, 7, 55, 24, 14, 16)):
        ws.column_dimensions[col].width = w
    for r in range(2, t):
        ws.row_dimensions[r].height = 36
    ws.freeze_panes = 'A2'
    ws.page_setup.orientation = 'landscape'
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_options.horizontalCentered = True
    wb.save(ruta)


def cmd_lista(items):
    filas, errores = [], []
    compatibles, base, ruta_xlsx = None, None, None
    ruta_json = None
    if '--xlsx' in items:
        k = items.index('--xlsx'); ruta_xlsx = items[k + 1]; items = items[:k] + items[k + 2:]
    if '--partidas' in items:
        k = items.index('--partidas'); ruta_json = items[k + 1]; items = items[:k] + items[k + 2:]
    if items and items[0] == '--base':
        base = BY_ID.get(items[1].zfill(7))
        items = items[2:]
        if base:
            g, _ = accesorios_de(base)
            compatibles = {a['id']: n for lst in g.values() for a, n in lst}
            compatibles[base['id']] = ''
    for it in items:
        if ':' in it:
            i, cant = it.split(':', 1)
        else:
            i, cant = it, None
        i = i.strip()
        i = i if len(i) > 7 else i.zfill(7)
        p = BY_ID.get(i)
        if not p:
            errores.append(i)
            continue
        cant = (cant or p.get('cantidad_defecto') or '1').strip()
        filas.append((p['id'], cant, _descripcion(p), p.get('uso', ''), _precio(p)))
        if p.get('restriccion'):
            print(f"ALERTA: {p['id']} {p['denominacion']} – NO OFRECER: {p['restriccion']}. Quítalo de la lista.")
        if compatibles is not None and p['id'] != base['id']:
            if p['id'] not in compatibles and not p.get('restriccion'):
                print(f"ALERTA: {p['id']} {p['denominacion']} NO es compatible con {base['denominacion']} "
                      f"según los datos. No lo incluyas; ofrece la alternativa compatible.")
            elif 'NO OFRECER' in compatibles[p['id']] and not p.get('restriccion'):
                print(f"ALERTA: {p['id']} {p['denominacion']} – {compatibles[p['id']]}. Quítalo de la lista.")
            elif compatibles[p['id']].startswith('POR CONFIRMAR'):
                print(f"AVISO: {p['id']} {p['denominacion']}: {compatibles[p['id']]}")
    if errores:
        print('IDs NO ENCONTRADOS (no incluir en la lista): ' + ', '.join(errores))
    print('| ID | Qty | Description | Use | Unit price (USD) | Total (USD) |')
    print('|---|---|---|---|---|---|')
    for i, cant, desc, uso, precio in filas:
        pu = f'${precio:,.2f}' if precio else ''
        tot = f'${precio * int(cant):,.2f}' if precio and str(cant).isdigit() else ''
        print(f'| {i} | {cant} | {desc} | {uso} | {pu} | {tot} |')
    gt = sum(pr * int(c) for _, c, _, _, pr in filas if pr and str(c).isdigit())
    print(f"|  |  |  |  | **Grand total (USD):** | {f'${gt:,.2f}' if gt else ''} |")
    if filas:
        if not ruta_xlsx:
            nombre = re.sub(r'[^\w\-]+', '_', (base or BY_ID[filas[0][0]])['denominacion']).strip('_')
            ruta_xlsx = os.path.join(_carpeta_salida(), f'Lista_{nombre}.xlsx')
        os.makedirs(os.path.dirname(os.path.abspath(ruta_xlsx)), exist_ok=True)
        _xlsx(filas, ruta_xlsx)
        print(f'\nExcel generado (entregarlo siempre al usuario): {os.path.abspath(ruta_xlsx)}')
    if ruta_json:
        import json
        partidas = [{'cantidad': int(c) if str(c).isdigit() else c, 'id': i, 'descripcion': d,
                     'uso': u, 'precio_unitario': pr} for i, c, d, u, pr in filas]
        json.dump(partidas, open(ruta_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'Partidas para presentación: {ruta_json}')


# --------------------------------------------------------------------------
# MAGNOS: sistema completo de una mesa magnética
# --------------------------------------------------------------------------
def _datos(p):
    return dict(x.split('=', 1) for x in p['datos'].split('; ')) if p.get('datos') else {}


def _norm_volt(v):
    v = v.upper().replace('V', '').replace(' ', '')
    if v in ('220', '230'):
        return '220'
    if v in ('400/460', '400', '440', '460', '460/400'):
        return '400/460'
    return None


def _medidas(txt):
    """'430 x 430', '430x430', '430 × 430' → ('430', '430') en orden mayor-menor, o None."""
    m = re.search(r'(\d{3,4})\s*[xX×*]\s*(\d{3,4})', txt)
    if not m:
        return None
    a, b = sorted((int(m.group(1)), int(m.group(2))), reverse=True)
    return str(a), str(b)


def _buscar_mesa(q, volt):
    """Encuentra la mesa por ID, denominación completa o por medidas (+ serie opcional).
    Solo declara NO EXISTE después de buscar por medidas en todas las mesas del catálogo."""
    mesas = [p for p in PROD if p['tipo'] == 'mesa']
    vol = lambda p: _datos(p).get('voltaje')
    # 1) ID directo
    if re.fullmatch(r'\d{7,8}', q.strip()):
        p = BY_ID.get(q.strip())
        if not p or p['tipo'] != 'mesa':
            print(f'NO ENCONTRADO: el ID {q} no es una mesa MAGNOS en los datos. Verifica el ID.')
            return None
        if vol(p) != volt:
            print(f'AVISO: el ID {q} ({p["denominacion"]}) es de {vol(p)} V, no de {volt} V. Confírmalo con el usuario.')
            return None
        return p
    # 2) Denominación completa
    base = lambda p: re.sub(r'\s*220V$', '', p['denominacion'])
    mismo = [p for p in mesas if norm(base(p)) == norm(q)]
    if mismo:
        m = [p for p in mismo if vol(p) == volt]
        if m:
            return m[0]
        otros = sorted({vol(p) for p in mismo})
        print(f'NO EXISTE: la mesa "{q}" no existe a {volt} V; sí existe a {", ".join(v + " V" for v in otros)}.')
        print('  Avísalo al usuario. Requerimientos especiales: clampingsolution@mx.schunk.com')
        return None
    # 3) Por medidas, con filtros opcionales de serie (A1/A2, 050/070, V)
    med = _medidas(q)
    if not med:
        print(f'SIN MEDIDAS: no se reconoce "{q}". Pide la denominación, el ID o las medidas (p. ej. 430 x 430).')
        return None
    tam = f'{med[0]} x {med[1]}'
    filtro = re.sub(r'\d{3,4}\s*[xX×*]\s*\d{3,4}|\b\d{3}\s*V\b', '', q).strip()
    alcance = f'serie {filtro}' if filtro else 'todas las series'
    cand = [p for p in mesas if re.search(rf'\b{med[0]} x {med[1]}\b', p['denominacion'])]
    nq = norm(re.sub(r'\d{3,4}\s*[xX×*]\s*\d{3,4}', '', q))
    for tok in ('A1', 'A2', '050', '070'):
        if tok in nq:
            cand = [p for p in cand if tok in norm(p['denominacion'])]
    if 'MFRS2V' in nq or 'VEROS' in nq:
        cand = [p for p in cand if '-V-' in p['denominacion']]
    m = [p for p in cand if vol(p) == volt]
    if len(m) == 1:
        print(f'SELECCIONADA POR MEDIDAS: {tam} a {volt} V → {m[0]["id"]} {m[0]["denominacion"]} (única opción).')
        return m[0]
    if len(m) > 1:
        print(f'VARIAS OPCIONES: {tam} a {volt} V existe en {len(m)} mesas. Muestra estas opciones y pregunta cuál:')
        for p in m:
            d = _datos(p)
            print(f'  {p["id"]}  {p["denominacion"]} | polo {d["polo"]} | {d["polos"]} polos | '
                  f'altura {d["altura"]} | fuerza: {p["descripcion"].split("fuerza máx. de sujeción ")[-1]}')
        return None
    if cand:
        otros = sorted({vol(p) for p in cand})
        print(f'NO EXISTE: no hay mesa {tam} a {volt} V (buscado por medidas en {alcance}). '
              f'Sí existe a: {", ".join(v + " V" for v in otros)}.')
    else:
        print(f'NO EXISTE: ninguna mesa MAGNOS mide {tam} en ningún voltaje (buscado por medidas en {alcance}).')
    if filtro:
        otras = [p for p in mesas if re.search(rf'\b{med[0]} x {med[1]}\b', p['denominacion']) and vol(p) == volt]
        for p in otras:
            print(f'  A {volt} V sí existe en otra serie: {p["id"]} {p["denominacion"]}. Ofrécela como alternativa.')
    print('  Avísalo al usuario. Requerimientos especiales: clampingsolution@mx.schunk.com')
    return None


def cmd_sistema(args):
    """sistema "<denominación de la mesa>" --voltaje <220|400/460> [--xlsx ruta] [--partidas ruta]"""
    extra = []
    for flag in ('--xlsx', '--partidas'):
        if flag in args:
            k = args.index(flag); extra += args[k:k + 2]; args = args[:k] + args[k + 2:]
    vero = '--vero-s' in args
    args = [a for a in args if a != '--vero-s']
    volt = None
    if '--voltaje' in args:
        k = args.index('--voltaje'); volt = _norm_volt(args[k + 1]); args = args[:k] + args[k + 2:]
    q = ' '.join(args)
    q = re.sub(r'\b(220|230|400/460|440|460)\s*V\b', '', q, flags=re.I).strip()
    if not volt:
        print('FALTA VOLTAJE: el usuario debe indicar 220 V o 400/460 V; no hay valor por defecto. Pregúntalo.')
        return
    mesa = _buscar_mesa(q, volt)
    if not mesa:
        return
    d = _datos(mesa)
    can, pines, polos, polo = int(d['canales']), int(d['pines']), int(d['polos']), d['polo']
    # 1) Unidad de control: mismo voltaje y canales
    keh = [p for p in PROD if p['categoria'] == 'unidad_control'
           and _datos(p)['voltaje'] == volt and int(_datos(p)['canales']) == can]
    # 2) Cable de 5 m según la unidad de control (4-PIN directo o ILME) y los pines de la mesa
    if can == 1:
        cable = '1610919'                      # VBK2-5 1x4P-1x4P 1CH (KEH plus 01)
    elif pines == 7:
        cable = '1611043'                      # VBK2-5 1xIL-1x7P 2CH
    else:
        cable = '1610941'                      # VBK2-5 1xIL-1x4P 1CH
    # 3) Botonera sin HKR según los canales de la unidad de control
    botonera = {1: '0420180', 2: '0420666', 4: '0420668', 8: '0420672'}[can]
    # 4) Extensiones de polo: 3 fijas + (polos - 3) flexibles, altura por defecto según el polo
    fija, flex = ('0420091', '0420092') if polo == '50' else ('0422997', '0422996')
    items = [f"{mesa['id']}:1", f"{keh[0]['id']}:1", f'{cable}:1', f'{botonera}:1',
             f'{fija}:3', f'{flex}:{polos - 3}']
    if vero:
        # MFRS2-V con VERO-S: componentes individuales (no el paquete promocional)
        nsl = {'315 x 315': '1323569', '430 x 315': '1323569', '430 x 430': '1323572',
               '600 x 430': '1323574', '800 x 600': '1323574'}          # NSL3 200 / 400 / 600
        if not mesa['denominacion'].startswith('MFRS2-V-'):
            print('NO APLICA: solo las mesas MFRS2-V (interfaz VERO-S) se cotizan con VERO-S. Avísalo al usuario.')
            return
        tam = re.search(r'(\d+ x \d+)', mesa['denominacion']).group(1)
        est = BY_ID[nsl[tam]]
        mod = int(_datos(est)['modulos'])
        BRR_QTY = 4                                   # bridas cilíndricas por estación
        items += [f"{est['id']}:1", f'0470020:{BRR_QTY}',      # estación NSL3 + BRR 50
                  '0432369:1', '0432370:1']                       # SPA 40-K (referencia) + SPB 40-K
        if mod > 2:
            items.append(f'1327450:{mod - 2}')                    # SPC 40-K en los demás módulos
        print(f"VERO-S (desglosado): la mesa está indicada para {est['denominacion']} ({mod} módulos) → "
              f"estación + {BRR_QTY}× BRR 50 + 1× SPA 40-K + 1× SPB 40-K" + (f" + {mod - 2}× SPC 40-K" if mod > 2 else ''))
    print(f"SISTEMA MAGNOS: {mesa['denominacion']} | {volt} V | {polos} polos, {can} canal(es), {pines} pines\n")
    cmd_lista(['--base', mesa['id']] + extra + items)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'producto':
        cmd_producto(' '.join(args))
    elif cmd == 'accesorios':
        cmd_accesorios(' '.join(args))
    elif cmd == 'lista':
        cmd_lista(args)
    elif cmd == 'sistema':
        cmd_sistema(args)
    else:
        print(__doc__)
