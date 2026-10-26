"""Smoke test: ejecuta cada página del dashboard con Streamlit AppTest y reporta excepciones."""
import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
PAGES = [ROOT / "app.py"] + sorted((ROOT / "pages").glob("*.py"))

failures = []
for page in PAGES:
    print(f"▶  probando {page.relative_to(ROOT)} ... ", end="", flush=True)
    at = AppTest.from_file(str(page), default_timeout=120)
    at.run()
    errs = [e.value for e in at.exception]
    if errs:
        print("❌")
        for e in errs:
            print("   ", e.splitlines()[-1] if e else e)
        failures.append((page.name, errs))
    else:
        print(f"✅  ({len(at.markdown)} bloques markdown, {len(at.slider)} sliders)")

print("\n" + "=" * 60)
if failures:
    print(f"RESULTADO: {len(failures)} página(s) con errores")
    sys.exit(1)
print(f"RESULTADO: las {len(PAGES)} páginas cargan sin excepciones ✔")
