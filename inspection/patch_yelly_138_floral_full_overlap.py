from pathlib import Path
root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")
old='''storyFloralTop.setScaleType(ImageView.ScaleType.CENTER_CROP);FrameLayout.LayoutParams sftp=new FrameLayout.LayoutParams(-1,(int)(getResources().getDisplayMetrics().heightPixels*0.10f),Gravity.TOP);'''
new='''storyFloralTop.setScaleType(ImageView.ScaleType.FIT_XY);FrameLayout.LayoutParams sftp=new FrameLayout.LayoutParams(-1,(int)(getResources().getDisplayMetrics().heightPixels*0.125f),Gravity.TOP);'''
if old not in s: raise SystemExit("top floral anchor missing")
s=s.replace(old,new,1)
old='''storyFloralBottom.setScaleType(ImageView.ScaleType.CENTER_CROP);FrameLayout.LayoutParams sfbp=new FrameLayout.LayoutParams(-1,(int)(getResources().getDisplayMetrics().heightPixels*0.10f),Gravity.BOTTOM);'''
new='''storyFloralBottom.setScaleType(ImageView.ScaleType.FIT_XY);FrameLayout.LayoutParams sfbp=new FrameLayout.LayoutParams(-1,(int)(getResources().getDisplayMetrics().heightPixels*0.125f),Gravity.BOTTOM);'''
if old not in s: raise SystemExit("bottom floral anchor missing")
s=s.replace(old,new,1)
# Keep both floral layers in front so their edge extends slightly over the video.
old='''storyFloralTop.bringToFront();'''
new='''storyFloralTop.bringToFront();storyFloralBottom.bringToFront();'''
if old not in s: raise SystemExit("front layer anchor missing")
s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")
g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10037" not in t or "versionName '1.0.37'" not in t: raise SystemExit("wrong 1.0.37 base")
t=t.replace("versionCode 10037","versionCode 10038",1).replace("versionName '1.0.37'","versionName '1.0.38'",1)
g.write_text(t,encoding="utf-8")
print("YELLY_138_FLORAL_FULL_NO_ZOOM_OVERLAP_OK")
