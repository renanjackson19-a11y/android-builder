from pathlib import Path

root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")

old='''  int storyTopMaskH=Math.max(dp(64),Math.min(dp(118),(int)(storyScreenH*0.125f)));'''
new='''  int storyTopMaskH=(int)(storyScreenH*0.23f);'''
if old not in s: raise SystemExit("storyTopMaskH anchor missing")
s=s.replace(old,new,1)

p.write_text(s,encoding="utf-8")

g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10028" not in t or "versionName '1.0.28'" not in t: raise SystemExit("wrong base")
t=t.replace("versionCode 10028","versionCode 10029",1).replace("versionName '1.0.28'","versionName '1.0.29'",1)
g.write_text(t,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.29
- Stories: área preta superior aumentada para ficar com a mesma altura visual da reprodução do catálogo.
- O vídeo continua em tela cheia por trás, sem reduzir nem dar zoom nos atores.
- Mantidos swipe, Favoritar, Comentários, Assistir agora e catálogo inicial aleatório.
- Nenhuma alteração no GreenPlay.
""",encoding="utf-8")
print("YELLY_129_STORIES_TOP_BLACK_MATCH_CATALOG_OK")
