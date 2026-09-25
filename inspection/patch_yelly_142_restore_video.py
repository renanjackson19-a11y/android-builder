from pathlib import Path
root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")
# Restore the exact video/layout behavior of 1.0.37. Only remove the added floral strips.
start=s.find("  ImageView storyFloralTop=new ImageView(this);")
end=s.find("  int storyScreenH=getResources().getDisplayMetrics().heightPixels;", start)
if start<0 or end<0: raise SystemExit("floral block missing")
s=s[:start]+s[end:]
s=s.replace("  storyFloralTop.bringToFront();\n","",1)
p.write_text(s,encoding="utf-8")
g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10037" not in t or "versionName '1.0.37'" not in t: raise SystemExit("wrong base")
t=t.replace("versionCode 10037","versionCode 10042",1).replace("versionName '1.0.37'","versionName '1.0.42'",1)
g.write_text(t,encoding="utf-8")
print("YELLY_142_RESTORE_VIDEO_137_OK")
