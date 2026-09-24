from pathlib import Path
import re

p=Path("work/app/src/main/java/fun/greenplay/app/SecretStrings.java")
s=p.read_text(encoding="utf-8")
s,n=re.subn(
    r'(?m)^\s*static String apiBase\(\).*?$',
    ' static String apiBase(){return "https://yellyplay.online/api/dtlive/";}',
    s,
    count=1
)
if n != 1:
    raise SystemExit("apiBase line not found")
p.write_text(s,encoding="utf-8")
print("YELLY_SECRET_FIX_OK")
