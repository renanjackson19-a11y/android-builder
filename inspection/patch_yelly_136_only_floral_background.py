from pathlib import Path
root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")
anchor='''  int storyScreenH=getResources().getDisplayMetrics().heightPixels;'''
insert='''  ImageView storyFloralTop=new ImageView(this);storyFloralTop.setImageResource(R.drawable.yelly_story_bg);storyFloralTop.setScaleType(ImageView.ScaleType.CENTER_CROP);FrameLayout.LayoutParams sftp=new FrameLayout.LayoutParams(-1,(int)(getResources().getDisplayMetrics().heightPixels*0.10f),Gravity.TOP);root.addView(storyFloralTop,sftp);
  ImageView storyFloralBottom=new ImageView(this);storyFloralBottom.setImageResource(R.drawable.yelly_story_bg);storyFloralBottom.setScaleType(ImageView.ScaleType.CENTER_CROP);FrameLayout.LayoutParams sfbp=new FrameLayout.LayoutParams(-1,(int)(getResources().getDisplayMetrics().heightPixels*0.10f),Gravity.BOTTOM);root.addView(storyFloralBottom,sfbp);
'''+anchor
if anchor not in s: raise SystemExit("Stories anchor missing")
s=s.replace(anchor,insert,1)
p.write_text(s,encoding="utf-8")
g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10034" not in t or "versionName '1.0.34'" not in t: raise SystemExit("wrong base")
t=t.replace("versionCode 10034","versionCode 10036",1).replace("versionName '1.0.34'","versionName '1.0.36'",1)
g.write_text(t,encoding="utf-8")
print("YELLY_136_ONLY_FLORAL_BACKGROUND_OK")
