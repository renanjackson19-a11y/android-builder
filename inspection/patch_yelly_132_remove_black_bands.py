from pathlib import Path

root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")

# Remove only the two black Stories covers. Keep all controls/layout unchanged.
s=s.replace("ytTopMask.setBackgroundColor(Color.BLACK);","ytTopMask.setBackgroundColor(Color.TRANSPARENT);",1)
s=s.replace("ytBottomMask.setBackgroundColor(Color.BLACK);","ytBottomMask.setBackgroundColor(Color.TRANSPARENT);",1)

# Crop the embedded player behind the same areas instead of covering them in black.
# This keeps the video large and pushes the external top/bottom chrome outside the viewport.
old="iframe{width:100%!important;height:100%!important;border:0}"
new="iframe{position:absolute!important;left:0!important;top:-23%!important;width:100%!important;height:140%!important;border:0!important}"
if old not in s: raise SystemExit("iframe crop anchor missing")
s=s.replace(old,new,1)

p.write_text(s,encoding="utf-8")

g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10030" not in t or "versionName '1.0.30'" not in t: raise SystemExit("wrong 1.0.30 base")
t=t.replace("versionCode 10030","versionCode 10032",1).replace("versionName '1.0.30'","versionName '1.0.32'",1)
g.write_text(t,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.32
- Stories: removidas somente as duas faixas pretas marcadas.
- O player ocupa essas áreas por recorte, mantendo o vídeo grande.
- Nenhum outro elemento do aplicativo foi alterado.
""",encoding="utf-8")
print("YELLY_132_ONLY_REMOVE_BLACK_BANDS_OK")
