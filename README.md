# Skills SCHUNK México

Versión actual: **1.0** (ver `CHANGELOG.md`)

## schunk-lista-accesorios

Arma listas de cotización (ID | Qty | Description | Use | precios) de productos SCHUNK con sus
accesorios compatibles, a partir de datos verificados del catálogo (`data/*.csv`).
Genera la tabla en markdown y un Excel con fórmulas.

Familias: KSP3, KSC3, KSC-5X, VERO-S, MAGNOS y Vise Automation (esta última solo se usa cuando
se menciona "vise automation").

> Contenido interno de SCHUNK. Mantener este repositorio privado.

## Instalación

Requiere Python 3 y `openpyxl` (`pip install openpyxl`).

| Herramienta | Carpeta |
|---|---|
| Claude Code | `~/.claude/skills/` o `.claude/skills/` del proyecto |
| GitHub Copilot (VS Code / CLI) | `.github/skills/` del proyecto |
| OpenAI Codex CLI | `~/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` |

```bash
git clone https://github.com/<usuario>/<repo>.git
cp -r <repo>/schunk-lista-accesorios <carpeta-de-skills>/
```

## Actualizar

```bash
cd <repo> && git pull
cp -r schunk-lista-accesorios <carpeta-de-skills>/
```

Revisa `CHANGELOG.md` para ver qué cambió. Si hay cambios de IDs, actualiza antes de cotizar.

## Proponer cambios

Abre un pull request con el cambio y la fuente (catálogo y fecha). Para una familia nueva sigue
`schunk-lista-accesorios/references/agregar-familia.md`.
