from pathlib import Path
root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")
old="iframe{position:absolute!important;left:0!important;top:-23%!important;width:100%!important;height:140%!important;border:0!important}"
new="iframe{position:absolute!important;left:0!important;top:-23%!important;width:100%!important;height:134%!important;border:0!important}"
if old not in s: raise SystemExit("1.0.32 crop anchor missing")
s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")
g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10032" not in t or "versionName '1.0.32'" not in t: raise SystemExit("wrong 1.0.32 base")
t=t.replace("versionCode 10032","versionCode 10033",1).replace("versionName '1.0.32'","versionName '1.0.33'",1)
g.write_text(t,encoding="utf-8")
print("YELLY_133_OK")
