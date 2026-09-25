from pathlib import Path
root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")
# Keep 1.0.37 layout untouched. Only correct how the floral artwork is rendered:
# preserve aspect ratio (no stretch) and let a small floral edge overlap the video.
old='''storyFloralTop.setScaleType(ImageView.ScaleType.CENTER_CROP);FrameLayout.LayoutParams sftp=new FrameLayout.LayoutParams(-1,(int)(getResources().getDisplayMetrics().heightPixels*0.10f),Gravity.TOP);'''
new='''storyFloralTop.setScaleType(ImageView.ScaleType.CENTER_CROP);storyFloralTop.setAdjustViewBounds(true);FrameLayout.LayoutParams sftp=new FrameLayout.LayoutParams(-1,(int)(getResources().getDisplayMetrics().heightPixels*0.115f),Gravity.TOP);'''
if old not in s: raise SystemExit("top anchor missing")
s=s.replace(old,new,1)
old='''storyFloralBottom.setScaleType(ImageView.ScaleType.CENTER_CROP);FrameLayout.LayoutParams sfbp=new FrameLayout.LayoutParams(-1,(int)(getResources().getDisplayMetrics().heightPixels*0.10f),Gravity.BOTTOM);'''
new='''storyFloralBottom.setScaleType(ImageView.ScaleType.CENTER_CROP);storyFloralBottom.setAdjustViewBounds(true);FrameLayout.LayoutParams sfbp=new FrameLayout.LayoutParams(-1,(int)(getResources().getDisplayMetrics().heightPixels*0.115f),Gravity.BOTTOM);'''
if old not in s: raise SystemExit("bottom anchor missing")
s=s.replace(old,new,1)
# Both artwork edges stay above the video; controls remain above them as in 1.0.37.
old='''storyFloralTop.bringToFront();'''
new='''storyFloralTop.bringToFront();storyFloralBottom.bringToFront();'''
if old not in s: raise SystemExit("layer anchor missing")
s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")
g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10037" not in t or "versionName '1.0.37'" not in t: raise SystemExit("wrong base")
t=t.replace("versionCode 10037","versionCode 10039",1).replace("versionName '1.0.37'","versionName '1.0.39'",1)
g.write_text(t,encoding="utf-8")
print("YELLY_139_FLORAL_NO_STRETCH_OK")
