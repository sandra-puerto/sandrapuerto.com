# ============================================================================
# LANDING-SGPT - (version_assets.py)
# Stratum Consumer Pattern
# ============================================================================
#
# Component ......... landing-sgpt
# Function .......... Cache busting por huella de contenido (content hash).
# Pattern ........... Equivalente ligero a `vite build` / `mix-manifest` de
#                     Laravel: cada asset referenciado en HTML recibe
#                     `?v=<sha256[:10]>` de su contenido actual.
#
# Por qué existe:
#   Nginx sirve CSS/JS con `Cache-Control: immutable` (7 días) y Cloudflare
#   los cachea en el edge. Sin una URL nueva por versión, navegador y CDN
#   siguen sirviendo la copia vieja aunque el archivo cambie en el servidor.
#
# Garantías:
#   - NO destructivo: solo reescribe el valor de `?v=` en los HTML.
#     Las fuentes CSS/JS permanecen legibles (gzip de Nginx comprime).
#   - Idempotente: si el contenido no cambió, el hash no cambia y el HTML
#     queda byte a byte igual.
#   - Modo --check para CI / pre-commit: sale con código 1 si algún hash
#     está desactualizado.
#
# Uso:
#   python scripts/version_assets.py          # actualiza hashes
#   python scripts/version_assets.py --check  # valida sin escribir
# ============================================================================

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

# HTML que referencian assets locales versionables
HTML_FILES = [
    PUBLIC / "index.html",
    ROOT / "templates" / "404.html",
    ROOT / "templates" / "maintenance.html",
]

# Coincide con href/src a /css/*.css o /js/*.js con o sin ?v= previo
ASSET_RE = re.compile(
    r'(?P<attr>(?:href|src)=")(?P<path>/(?:css|js)/[\w.\-/]+\.(?:css|js))(?:\?v=[\w\-]*)?(?P<end>")'
)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:10]


def process(html_path: Path, check: bool) -> bool:
    """Devuelve True si el archivo está (o quedó) al día."""
    if not html_path.exists():
        return True

    original = html_path.read_text(encoding="utf-8")
    missing = []

    def repl(m: re.Match) -> str:
        asset = PUBLIC / m.group("path").lstrip("/")
        if not asset.exists():
            missing.append(m.group("path"))
            return m.group(0)
        return f'{m.group("attr")}{m.group("path")}?v={file_hash(asset)}{m.group("end")}'

    updated = ASSET_RE.sub(repl, original)

    for p in missing:
        print(f"  [WARN] {html_path.name}: asset no encontrado {p}")

    rel = html_path.relative_to(ROOT)
    if updated == original:
        print(f"  [OK]   {rel}")
        return True
    if check:
        print(f"  [STALE] {rel} (ejecuta: python scripts/version_assets.py)")
        return False

    # newline="" preserva los finales de línea originales (CRLF/LF)
    with open(html_path, "w", encoding="utf-8", newline="") as f:
        f.write(updated)
    print(f"  [UPD]  {rel}")
    return True


def main() -> int:
    check = "--check" in sys.argv
    results = [process(p, check) for p in HTML_FILES]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
