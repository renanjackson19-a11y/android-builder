from pathlib import Path
root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")

# Keep 1.0.36 exactly; only bring the top floral strip in front of the video.
anchor='''  ytBottomMask=new View(this);'''
if anchor not in s: raise SystemExit("mask anchor missing")
insert='''  storyFloralTop.bringToFront();
'''+anchor
s=s.replace(anchor,insert,1)

# Move only the existing Yelly logo slightly downward.
old='''lpLogo.setMargins(0,dp(12),dp(14),0);'''
new='''lpLogo.setMargins(0,dp(20),dp(14),0);'''
if old not in s: raise SystemExit("logo margin anchor missing")
s=s.replace(old,new,1)

p.write_text(s,encoding="utf-8")
g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10036" not in t or "versionName '1.0.36'" not in t: raise SystemExit("wrong 1.0.36 base")
t=t.replace("versionCode 10036","versionCode 10037",1).replace("versionName '1.0.36'","versionName '1.0.37'",1)
g.write_text(t,encoding="utf-8")
print("YELLY_137_TOP_FLORAL_LAYER_LOGO_DOWN_OK")
