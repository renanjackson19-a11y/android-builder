from pathlib import Path
import re

root=Path("work")

def one(s,old,new,label):
    n=s.count(old)
    if n!=1:
        raise SystemExit(f"{label}: expected 1 got {n}")
    return s.replace(old,new,1)

# Stories: restore the previous hidden-ID playback, while keeping current Yelly UI.
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")
s=one(s,
'FrameLayout root;WebView web;ImageView poster;View shade,swipe;LinearLayout info,actions;TextView title,meta,fav,comments,back,hint;ProgressBar progress;',
'FrameLayout root;WebView web;ImageView poster,logoTop;View shade,swipe,ytTopMask,ytBottomMask;LinearLayout info,actions;TextView title,meta,fav,comments,back,hint;ProgressBar progress;',
'story fields')
s=one(s,
'void build(){root=new FrameLayout(this);root.setBackgroundColor(Color.BLACK);poster=new ImageView(this);poster.setScaleType(ImageView.ScaleType.CENTER_CROP);poster.setBackgroundColor(Color.BLACK);poster.setAlpha(0f);root.addView(poster,new FrameLayout.LayoutParams(-1,-1));',
'void build(){root=new FrameLayout(this);root.setBackgroundColor(Color.BLACK);poster=new ImageView(this);poster.setScaleType(ImageView.ScaleType.CENTER_CROP);poster.setBackgroundColor(Color.BLACK);poster.setImageResource(R.drawable.story_banner_bg);poster.setAlpha(1f);root.addView(poster,new FrameLayout.LayoutParams(-1,-1));',
'fixed story banner')
old='''web.setWebChromeClient(new WebChromeClient());web.setWebViewClient(new WebViewClient());web.addJavascriptInterface(new Object(){@android.webkit.JavascriptInterface public void ready(){runOnUiThread(()->{storyReady=true;if(web!=null&&!dragging&&!swipeAnimating)revealStory();});}@android.webkit.JavascriptInterface public void previewEnded(){runOnUiThread(()->{if(!dragging&&!swipeAnimating&&items.length()>0)animateStorySwap(true);});}},"StoryBridge");try{web.setLayerType(View.LAYER_TYPE_HARDWARE,null);}catch(Exception ignored){}root.addView(web,new FrameLayout.LayoutParams(-1,-1));'''
new='''web.setWebChromeClient(new WebChromeClient());web.setWebViewClient(new WebViewClient());web.addJavascriptInterface(new Object(){@android.webkit.JavascriptInterface public void ready(){runOnUiThread(()->{storyReady=true;if(web!=null&&!dragging&&!swipeAnimating)revealStory();});}@android.webkit.JavascriptInterface public void previewEnded(){runOnUiThread(()->{if(!dragging&&!swipeAnimating&&items.length()>0)animateStorySwap(true);});}},"StoryBridge");try{web.setLayerType(View.LAYER_TYPE_HARDWARE,null);}catch(Exception ignored){}FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1);if(!tvMode)wp.setMargins(0,dp(64),0,dp(112));root.addView(web,wp);
  ytTopMask=new View(this);ytTopMask.setBackgroundColor(0xee14080f);FrameLayout.LayoutParams ytp=new FrameLayout.LayoutParams(-1,dp(76),Gravity.TOP);ytp.setMargins(0,dp(64),0,0);root.addView(ytTopMask,ytp);
  ytBottomMask=new View(this);ytBottomMask.setBackgroundColor(0xee14080f);FrameLayout.LayoutParams ybp=new FrameLayout.LayoutParams(-1,dp(64),Gravity.BOTTOM);ybp.setMargins(0,0,0,dp(112));root.addView(ytBottomMask,ybp);'''
s=one(s,old,new,'story hidden embed masks')
s=one(s,
'root.addView(back,bp);\n  info=new LinearLayout(this);',
'''root.addView(back,bp);
  logoTop=new ImageView(this);logoTop.setImageResource(R.drawable.yelly_logo);logoTop.setScaleType(ImageView.ScaleType.FIT_CENTER);FrameLayout.LayoutParams lpLogo=new FrameLayout.LayoutParams(dp(100),dp(46),Gravity.TOP|Gravity.RIGHT);lpLogo.setMargins(0,dp(12),dp(14),0);root.addView(logoTop,lpLogo);
  info=new LinearLayout(this);''',
'story yelly logo')
old_info='''info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(18),dp(10),dp(94),dp(10));title=t("Carregando Stories…",19);title.setGravity(Gravity.LEFT);title.setTypeface(null,1);title.setMaxLines(3);title.setEllipsize(android.text.TextUtils.TruncateAt.END);info.addView(title,new LinearLayout.LayoutParams(-1,-2));meta=t("Yelly Doramas",13);meta.setGravity(Gravity.LEFT);meta.setTypeface(null,1);meta.setTextColor(0xffff9ccc);meta.setPadding(0,dp(6),0,0);info.addView(meta,new LinearLayout.LayoutParams(-1,-2));FrameLayout.LayoutParams ip=new FrameLayout.LayoutParams(-1,dp(188),Gravity.BOTTOM);ip.setMargins(0,0,0,dp(34));root.addView(info,ip);'''
new_info='''info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(18),dp(10),dp(98),dp(10));title=t("Carregando Stories…",19);title.setGravity(Gravity.LEFT);title.setTypeface(null,1);title.setMaxLines(3);title.setEllipsize(android.text.TextUtils.TruncateAt.END);info.addView(title,new LinearLayout.LayoutParams(-1,-2));meta=t("▶  Assistir agora",13);meta.setGravity(Gravity.CENTER);meta.setTypeface(null,1);meta.setTextColor(Color.WHITE);meta.setBackground(round(accent,16));meta.setPadding(dp(14),dp(8),dp(14),dp(8));meta.setOnClickListener(v->openFull());LinearLayout.LayoutParams mlp=new LinearLayout.LayoutParams(-2,dp(42));mlp.setMargins(0,dp(9),0,0);info.addView(meta,mlp);FrameLayout.LayoutParams ip=new FrameLayout.LayoutParams(-1,dp(188),Gravity.BOTTOM);ip.setMargins(0,0,0,dp(34));root.addView(info,ip);'''
s=one(s,old_info,new_info,'story assistir agora')
new_actions='''actions=new LinearLayout(this);actions.setOrientation(LinearLayout.VERTICAL);actions.setGravity(Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);fav=action("♡\\nFavoritar");fav.setOnClickListener(v->toggleFav());actions.addView(fav,new LinearLayout.LayoutParams(dp(78),dp(74)));comments=action("💬\\nComentários");LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(dp(78),dp(74));cp.setMargins(0,dp(8),0,0);actions.addView(comments,cp);comments.setOnClickListener(v->openComments());FrameLayout.LayoutParams ap=new FrameLayout.LayoutParams(dp(82),dp(176),Gravity.RIGHT|Gravity.BOTTOM);ap.setMargins(0,0,dp(7),dp(126));root.addView(actions,ap);'''
s,n=re.subn(r'actions=new LinearLayout\(this\);actions\.setOrientation\(LinearLayout\.VERTICAL\);actions\.setGravity\(Gravity\.BOTTOM\|Gravity\.CENTER_HORIZONTAL\);.*?root\.addView\(actions,ap\);',new_actions,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f"story right actions: expected 1 got {n}")
s=one(s,
'void revealStory(){if(web!=null){web.animate().cancel();web.setTranslationY(0f);web.animate().alpha(1f).setDuration(110).start();}if(poster!=null){poster.animate().cancel();poster.setTranslationY(0f);poster.animate().alpha(.36f).setDuration(130).start();}}',
'void revealStory(){if(web!=null){web.animate().cancel();web.setTranslationY(0f);web.postDelayed(()->{if(web!=null&&!dragging&&!swipeAnimating)web.animate().alpha(1f).setDuration(120).start();},650);}if(poster!=null){poster.setAlpha(1f);poster.setTranslationY(0f);}}',
'story reveal')
# Banner stays fixed while video/UI swipes.
s=s.replace('if(poster!=null){poster.animate().cancel();poster.setAlpha(0f);poster.setTranslationY(0f);}','',3)
old_show='''void show(int i){if(items.length()==0)return;index=Math.max(0,Math.min(items.length()-1,i));JSONObject x=items.optJSONObject(index);if(x==null)return;storyReady=false;final int token=++storyToken;String id=x.optString("youtube_id","").replaceAll("[^A-Za-z0-9_-]","");String nm=cleanTitle(x.optString("name",x.optString("title","Yelly Doramas")));title.setText(nm);meta.setText("Yelly Doramas");if(progress!=null)progress.setProgress(0);fav.setText(isFav(x)?"♥\nFavorito":"♡\nFavoritar");String img=x.optString("portrait_img",x.optString("thumbnail",""));if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(poster!=null){poster.animate().cancel();poster.setAlpha(0f);poster.setTranslationY(0f);}if(!img.isEmpty())Img.loadVisible(poster,img);play(id);enrich(x,token);if(more&&index>=items.length()-20)fetch();}'''
new_show='''void show(int i){if(items.length()==0)return;index=Math.max(0,Math.min(items.length()-1,i));JSONObject x=items.optJSONObject(index);if(x==null)return;storyReady=false;final int token=++storyToken;String id=x.optString("youtube_id","").replaceAll("[^A-Za-z0-9_-]","");String nm=cleanTitle(x.optString("name",x.optString("title","Yelly Doramas")));title.setText(nm);meta.setText("▶  Assistir agora");if(progress!=null)progress.setProgress(0);fav.setText(isFav(x)?"♥\nFavorito":"♡\nFavoritar");if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(poster!=null){poster.setImageResource(R.drawable.story_banner_bg);poster.setAlpha(1f);poster.setTranslationY(0f);}play(id);enrich(x,token);if(more&&index>=items.length()-20)fetch();}'''
s=one(s,old_show,new_show,'story show')
s=one(s,
'if(!p.isEmpty()){x.put("portrait_img",p);x.put("thumbnail",p);Img.loadVisible(poster,p);}',
'if(!p.isEmpty()){x.put("portrait_img",p);x.put("thumbnail",p);}',
'story enrich poster')
s=s.replace("playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,playsinline:1,rel:0,modestbranding:1,iv_load_policy:3,origin:'https://yellyplay.online'}",
            "playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,playsinline:1,rel:0,modestbranding:1,iv_load_policy:3,cc_load_policy:0,origin:'https://yellyplay.online'}",1)
p.write_text(s,encoding="utf-8")

# Full miniseries player: URL/ID remains internal; only Yelly chrome is visible.
p=root/"app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java"
y=p.read_text(encoding="utf-8")
y=one(y,'ImageView playerBackdrop;\n    View touchShield;','ImageView playerBackdrop,logoTop;\n    View touchShield,ytTopMask,ytBottomMask,ytBrandMask;','full fields')
y=one(y,'playerBackdrop.setAlpha(.40f);','playerBackdrop.setAlpha(1f);','full backdrop')
old='''root.addView(web,new FrameLayout.LayoutParams(-1,-1));
        View ytBrandMask=new View(this);ytBrandMask.setBackground(bg(0xcc0a0709,12));FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(dp(102),dp(36),Gravity.RIGHT|Gravity.BOTTOM);ybm.setMargins(0,0,dp(5),dp(5));root.addView(ytBrandMask,ybm);'''
new='''FrameLayout.LayoutParams wlp=new FrameLayout.LayoutParams(-1,-1);if(!tvMode)wlp.setMargins(0,dp(68),0,dp(106));root.addView(web,wlp);
        if(!tvMode){
            ytTopMask=new View(this);ytTopMask.setBackground(bg(0xee14080f,0));FrameLayout.LayoutParams tlp=new FrameLayout.LayoutParams(-1,dp(74),Gravity.TOP);tlp.setMargins(0,dp(68),0,0);root.addView(ytTopMask,tlp);
            ytBottomMask=new View(this);ytBottomMask.setBackground(bg(0xee14080f,0));FrameLayout.LayoutParams blp=new FrameLayout.LayoutParams(-1,dp(62),Gravity.BOTTOM);blp.setMargins(0,0,0,dp(106));root.addView(ytBottomMask,blp);
            ytBrandMask=new View(this);ytBrandMask.setBackground(bg(0xee14080f,12));FrameLayout.LayoutParams brp=new FrameLayout.LayoutParams(dp(124),dp(48),Gravity.RIGHT|Gravity.BOTTOM);brp.setMargins(0,0,dp(2),dp(106));root.addView(ytBrandMask,brp);
        }'''
y=one(y,old,new,'full hidden embed masks')
y=one(y,
'''bp.setMargins(dp(14),dp(14),0,0);root.addView(back,bp);
        back.bringToFront();''',
'''bp.setMargins(dp(14),dp(14),0,0);root.addView(back,bp);
        logoTop=new ImageView(this);logoTop.setImageResource(R.drawable.yelly_logo);logoTop.setScaleType(ImageView.ScaleType.FIT_CENTER);FrameLayout.LayoutParams llp=new FrameLayout.LayoutParams(dp(100),dp(46),Gravity.TOP|Gravity.RIGHT);llp.setMargins(0,dp(14),dp(14),0);root.addView(logoTop,llp);
        back.bringToFront();logoTop.bringToFront();''',
'full yelly logo')
y=one(y,
'if(web!=null){web.setTranslationX(0f);web.setTranslationY(0f);web.animate().alpha(1f).setDuration(120).start();}',
'if(web!=null){web.setTranslationX(0f);web.setTranslationY(0f);web.postDelayed(()->{if(web!=null)web.animate().alpha(1f).setDuration(140).start();},700);}',
'full delayed reveal')
p.write_text(y,encoding="utf-8")

# Current app catalog: restore the hidden internal youtube_id route instead of showing "no direct video".
p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
m=p.read_text(encoding="utf-8")
pat=r' void openYoutubeVideo\(JSONObject source,String title,boolean restart\)\{.*?\n void renderGreenShortsResume'
mm=re.search(pat,m,re.S)
if not mm:
    raise SystemExit("MainActivity openYoutubeVideo anchor not found")
replacement=''' void openYoutubeVideo(JSONObject source,String title,boolean restart){String id=youtubeVideoId(source);if(id.isEmpty()){Toast.makeText(this,"Vídeo indisponível.",Toast.LENGTH_SHORT).show();return;}if(restart)clearGreenShortResume(source);Intent in=new Intent(this,YouTubePlayerActivity.class);in.putExtra("youtube_id",id);in.putExtra("greenshorts_id",id);in.putExtra("title",title==null?"Yelly Doramas":title);in.putExtra("poster",detailValue(source,"thumbnail","portrait_img","poster","image"));in.putExtra("tv_mode",tvMode);int resume=restart?0:greenShortResumePosition(source);if(resume>0)in.putExtra("resume_ms",resume);startActivity(in);}
 void renderGreenShortsResume'''
m=m[:mm.start()]+replacement+m[mm.end():]
p.write_text(m,encoding="utf-8")

# Re-register the hidden player.
p=root/"app/src/main/AndroidManifest.xml"
x=p.read_text(encoding="utf-8")
if '.YouTubePlayerActivity' not in x:
    idx=x.find('<activity')
    if idx<0:
        raise SystemExit("manifest activity anchor not found")
    x=x[:idx]+'<activity android:name=".YouTubePlayerActivity" android:exported="false" android:screenOrientation="unspecified" android:configChanges="orientation|screenSize"/>\n        '+x[idx:]
p.write_text(x,encoding="utf-8")

# Version.
p=root/"app/build.gradle"
g=p.read_text(encoding="utf-8")
if "versionCode 10016" not in g or "versionName '1.0.16'" not in g:
    raise SystemExit("wrong 1.0.16 base")
g=g.replace("versionCode 10016","versionCode 10017",1).replace("versionName '1.0.16'","versionName '1.0.17'",1)
p.write_text(g,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.17
- Volta ao comportamento anterior: youtube_id/URL ficam somente internamente e não aparecem na interface.
- Stories usam novamente o feed correto de minisséries e reproduzem pelo player embutido com controles do Yelly.
- Mantido preview de até 2 minutos, Favoritar, Comentários e Assistir agora.
- Banner fixo do Yelly fica no fundo do Story e logo Yelly no topo direito.
- Camadas do app cobrem cabeçalho, canal/compartilhar e marca no rodapé do player embutido.
- Tela Assistir mantém a capa como fundo único e controles próprios do Yelly.
""",encoding="utf-8")
print("YELLY_117_RESTORED_HIDDEN_IDS_OK")
