from pathlib import Path

root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java"
s=p.read_text(encoding="utf-8")
old='int topMaskH=Math.max(dp(48),Math.min(dp(82),(int)(screenH*0.09f)));'
new='int topMaskH=Math.max(dp(64),Math.min(dp(118),(int)(screenH*0.125f)));'
if old not in s: raise SystemExit("top mask anchor missing")
s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")

g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10024" not in t or "versionName '1.0.24'" not in t: raise SystemExit("wrong base")
t=t.replace("versionCode 10024","versionCode 10025",1).replace("versionName '1.0.24'","versionName '1.0.25'",1)
g.write_text(t,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.25
- A faixa preta superior do player foi aumentada.
- Agora ela desce um pouco mais, cobrindo também a área logo abaixo do aviso IA.
- Restante do player mantido igual à 1.0.24.
""",encoding="utf-8")
print("YELLY_125_TOP_MASK_LOWER_OK")
