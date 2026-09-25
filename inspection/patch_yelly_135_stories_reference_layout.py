from pathlib import Path
root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")

old='''web.addJavascriptInterface(new Object(){@android.webkit.JavascriptInterface public void ready(){runOnUiThread(()->{storyReady=true;if(web!=null&&!dragging&&!swipeAnimating)revealStory();});}@android.webkit.JavascriptInterface public void previewEnded(){runOnUiThread(()->{if(!dragging&&!swipeAnimating&&items.length()>0)animateStorySwap(true);});}},"StoryBridge");try{web.setLayerType(View.LAYER_TYPE_HARDWARE,null);}catch(Exception ignored){}FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1);root.addView(web,wp);
  int storyScreenH=getResources().getDisplayMetrics().heightPixels;'''
new='''web.addJavascriptInterface(new Object(){@android.webkit.JavascriptInterface public void ready(){runOnUiThread(()->{storyReady=true;if(web!=null&&!dragging&&!swipeAnimating)revealStory();});}@android.webkit.JavascriptInterface public void previewEnded(){runOnUiThread(()->{if(!dragging&&!swipeAnimating&&items.length()>0)animateStorySwap(true);});}},"StoryBridge");try{web.setLayerType(View.LAYER_TYPE_HARDWARE,null);}catch(Exception ignored){}
  int storyScreenH=getResources().getDisplayMetrics().heightPixels;
  FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1);wp.setMargins(0,(int)(storyScreenH*0.10f),0,(int)(storyScreenH*0.10f));root.addView(web,wp);'''
if old not in s: raise SystemExit("Stories web frame anchor missing")
s=s.replace(old,new,1)

# Keep the same logo, but place it over the floral/video composition instead of the old black header area.
old='''logoTop=new ImageView(this);logoTop.setImageResource(R.drawable.yelly_logo);logoTop.setScaleType(ImageView.ScaleType.FIT_CENTER);FrameLayout.LayoutParams lpLogo=new FrameLayout.LayoutParams(dp(100),dp(46),Gravity.TOP|Gravity.RIGHT);lpLogo.setMargins(0,dp(12),dp(14),0);root.addView(logoTop,lpLogo);'''
new='''logoTop=new ImageView(this);logoTop.setImageResource(R.drawable.yelly_logo);logoTop.setScaleType(ImageView.ScaleType.FIT_CENTER);FrameLayout.LayoutParams lpLogo=new FrameLayout.LayoutParams(dp(112),dp(54),Gravity.TOP|Gravity.RIGHT);lpLogo.setMargins(0,dp(34),dp(14),0);root.addView(logoTop,lpLogo);'''
if old not in s: raise SystemExit("Stories logo anchor missing")
s=s.replace(old,new,1)

p.write_text(s,encoding="utf-8")

g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10034" not in t or "versionName '1.0.34'" not in t: raise SystemExit("wrong 1.0.34 base")
t=t.replace("versionCode 10034","versionCode 10035",1).replace("versionName '1.0.34'","versionName '1.0.35'",1)
g.write_text(t,encoding="utf-8")
print("YELLY_135_STORIES_REFERENCE_LAYOUT_OK")
