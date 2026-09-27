from pathlib import Path

root = Path("work")
api = root / "app/src/main/java/fun/greenplay/app/Api.java"
gradle = root / "app/build.gradle"
notes = root / "app/RELEASE_NOTES.txt"

s = api.read_text(encoding="utf-8")
if '"X-CineTV Super-Key"' not in s:
    raise SystemExit("Invalid CineTV header marker not found in 1.0.0 source")
s = s.replace('"X-CineTV Super-Key"', '"X-CineTV-Super-Key"')
api.write_text(s, encoding="utf-8")

g = gradle.read_text(encoding="utf-8")
if "versionCode 100" not in g or "versionName '1.0.0'" not in g:
    raise SystemExit("CineTV 1.0.0 version markers not found")
g = g.replace("versionCode 100", "versionCode 101", 1)
g = g.replace("versionName '1.0.0'", "versionName '1.0.1'", 1)
gradle.write_text(g, encoding="utf-8")

notes.write_text("""CineTV Super 1.0.1
Correção do login e cadastro de teste grátis.
Corrigido o cabeçalho HTTP usado pelo aplicativo ao acessar a API CineTV Super.
Mantidos domínio, identidade visual, catálogo integrado e suporte a celular, Android TV e TV Box.
""", encoding="utf-8")

check = api.read_text(encoding="utf-8")
if '"X-CineTV Super-Key"' in check:
    raise SystemExit("Invalid HTTP header still present")
if '"X-CineTV-Super-Key"' not in check or '"Api-Token"' not in check:
    raise SystemExit("Expected API headers missing")
print("CineTV Super 1.0.1 login/network patch applied")
