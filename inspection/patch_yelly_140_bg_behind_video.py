from pathlib import Path
root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")
# Remove the two foreground floral strips added in 1.0.36/1.0.37.
start=s.find('''  ImageView storyFloralTop=new ImageView(this);''')
end=s.find('''  int storyScreenH=getResources().getDisplayMetrics().heightPixels;''', start)
if start<0 or end<0: raise SystemExit("floral strip block missing")
s=s[:start]+s[end:]
s=s.replace('''  storyFloralTop.bringToFront();''','',1)
# Put the supplied floral image behind the video/root content, preserving aspect ratio.
anchor='''  WebView web=new WebView(this);'''
bg='''  ImageView storyBackground=new ImageView(this);storyBackground.setImageResource(R.drawable.yelly_story_bg);storyBackground.setScaleType(ImageView.ScaleType.FIT_CENTER);storyBackground.setBackgroundColor(Color.BLACK);root.addView(storyBackground,new FrameLayout.LayoutParams(-1,-1));
'''+anchor
if anchor not in s: raise SystemExit("web anchor missing")
s=s.replace(anchor,bg,1)
p.write_text(s,encoding="utf-8")
g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10037" not in t or "versionName '1.0.37'" not in t: raise SystemExit("wrong base")
t=t.replace("versionCode 10037","versionCode 10040",1).replace("versionName '1.0.37'","versionName '1.0.40'",1)
g.write_text(t,encoding="utf-8")
print("YELLY_140_BACKGROUND_BEHIND_VIDEO_NO_ZOOM_OK")
