from pathlib import Path
root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")
start=s.find("  ImageView storyFloralTop=new ImageView(this);")
end=s.find("  int storyScreenH=getResources().getDisplayMetrics().heightPixels;", start)
if start<0 or end<0: raise SystemExit("floral strip block missing")
# Reuse the already-loaded supplied drawable as one full-screen background behind the video.
bg='''  ImageView storyBackground=new ImageView(this);storyBackground.setImageResource(R.drawable.yelly_story_bg);storyBackground.setScaleType(ImageView.ScaleType.FIT_CENTER);storyBackground.setBackgroundColor(Color.BLACK);root.addView(storyBackground,new FrameLayout.LayoutParams(-1,-1));\n'''
s=s[:start]+bg+s[end:]
s=s.replace("  storyFloralTop.bringToFront();\n","",1)
p.write_text(s,encoding="utf-8")
g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10037" not in t or "versionName '1.0.37'" not in t: raise SystemExit("wrong base")
t=t.replace("versionCode 10037","versionCode 10040",1).replace("versionName '1.0.37'","versionName '1.0.40'",1)
g.write_text(t,encoding="utf-8")
print("YELLY_140_BACKGROUND_BEHIND_VIDEO_NO_ZOOM_OK")
