#!/usr/bin/env python3
"""Pruebas de regresión de la skill. Ejecutar después de cualquier cambio en datos o script:

    python3 scripts/probar.py

Cada caso es una petición real con el resultado que debe dar. Si alguno falla, no publiques
la versión hasta corregirlo.
"""
import os, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
BUSCAR = os.path.join(AQUI, 'buscar.py')
SALIDA = tempfile.mkdtemp(prefix='schunk_prueba_')

# (descripción, argumentos, textos que deben aparecer, textos que NO deben aparecer)
CASOS = [
    ('MAGNOS por medidas: 430 x 430 a 220 V (caso real: se declaró inexistente por error)',
     ['sistema', '430 x 430', '--voltaje', '220'],
     ['1663682', '0420655', '1610919', '0420180', '| 0420091 | 3 |', '| 0420092 | 33 |', 'Excel generado'],
     ['NO EXISTE']),
    ('MAGNOS por ID',
     ['sistema', '1663682', '--voltaje', '220'], ['SISTEMA MAGNOS: MFRS2-A2-050 430 x 430 220V'], ['NO EXISTE']),
    ('MAGNOS por denominación completa',
     ['sistema', 'MFRS2-A2-050 430 x 430', '--voltaje', '220'], ['1663682'], ['NO EXISTE']),
    ('MAGNOS medidas escritas pegadas y con voltaje en el texto',
     ['sistema', '430x430 220V', '--voltaje', '220'], ['1663682'], ['NO EXISTE']),
    ('MAGNOS medidas con varias opciones: debe listar, no elegir ni negar',
     ['sistema', '430 x 430', '--voltaje', '460'], ['VARIAS OPCIONES', '1594990', '1595029'],
     ['NO EXISTE', 'Excel generado']),
    ('MAGNOS combinación que de verdad no existe: ofrece la alternativa',
     ['sistema', 'A1-070 430 x 430', '--voltaje', '220'], ['NO EXISTE', '1663682'], ['Excel generado']),
    ('MAGNOS sin voltaje: debe preguntar',
     ['sistema', '430 x 430'], ['FALTA VOLTAJE'], ['Excel generado']),
    ('KSC3 normal no se confunde con la versión de vise automation',
     ['producto', 'KSC3 80-130'], ['1508857'], ['1623548']),
    ('Vise automation: lista con estación como base y Excel',
     ['lista', '--base', '1621657', '1621657', '1623548', '1623565', '1627791'],
     ['1623548', '1623565', 'Excel generado'], ['ALERTA', 'NO ENCONTRADOS']),
    ('Lista sin --xlsx: el Excel se genera igual',
     ['lista', '--base', '1382588', '1382588', '0402121'], ['Excel generado'], []),
]


def main():
    env = dict(os.environ, SCHUNK_SALIDA=SALIDA)
    fallas = 0
    for desc, args, si, no in CASOS:
        out = subprocess.run([sys.executable, BUSCAR] + args, capture_output=True, text=True, env=env)
        txt = out.stdout + out.stderr
        err = [f'falta "{t}"' for t in si if t not in txt] + [f'no debe aparecer "{t}"' for t in no if t in txt]
        if out.returncode not in (0,) and 'Traceback' in txt:
            err.append('el script falló (Traceback)')
        print(('OK   ' if not err else 'FALLA') + f'  {desc}')
        for e in err:
            print(f'         {e}')
        fallas += bool(err)
    xlsx = [f for f in os.listdir(SALIDA) if f.endswith('.xlsx')]
    print(f'\n{len(CASOS) - fallas}/{len(CASOS)} casos correctos; {len(xlsx)} Excel generados en {SALIDA}')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
