from pathlib import Path
root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")
# Start from the good 1.0.37. Keep player and all controls untouched.
# Only remove the floral foreground strips; use floral artwork on the existing top/bottom masks.
start=s.find("  ImageView storyFloralTop=new ImageView(this);")
end=s.find("  int storyScreenH=getResources().getDisplayMetrics().heightPixels;", start)
if start<0 or end<0: raise SystemExit("floral block missing")
s=s[:start]+s[end:]
s=s.replace("  storyFloralTop.bringToFront();\n","",1)
# Existing masks already occupy only the spare top/bottom areas; give them the supplied image.
old='''ytTopMask.setBackgroundColor(Color.TRANSPARENT);'''
new='''ytTopMask.setBackgroundResource(R.drawable.yelly_story_bg);'''
if old not in s: raise SystemExit("top mask anchor missing")
s=s.replace(old,new,1)
old='''ytBottomMask.setBackgroundColor(Color.TRANSPARENT);'''
new='''ytBottomMask.setBackgroundResource(R.drawable.yelly_story_bg);'''
if old not in s: raise SystemExit("bottom mask anchor missing")
s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")
g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10037" not in t or "versionName '1.0.37'" not in t: raise SystemExit("wrong base")
t=t.replace("versionCode 10037","versionCode 10041",1).replace("versionName '1.0.37'","versionName '1.0.41'",1)
g.write_text(t,encoding="utf-8")
print("YELLY_141_PLAYER_UNTOUCHED_FLORAL_MASKS_OK")
