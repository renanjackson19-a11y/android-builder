from pathlib import Path

root=Path('work')
stories=root/'app/src/main/java/fun/greenplay/app/StoriesActivity.java'
yt=root/'app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java'
grad=root/'app/build.gradle'

def one(text, old, new, label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 got {n}')
    return text.replace(old,new,1)

s=stories.read_text(encoding='utf-8')

s=one(s,
'''FrameLayout root;WebView web;ImageView poster,topCoverMask,bottomCoverMask;View shade,swipe;LinearLayout info,actions;TextView title,meta,fav,comments,back,hint;ProgressBar progress;JSONArray items=new JSONArray();java.util.HashSet<String> seen=new java.util.HashSet<>();int index=0,page=1,totalRows=0;boolean loading=false,more=true,tvMode=false,playing=true,dragging=false,swipeAnimating=false;''',
'''FrameLayout root;WebView web;ImageView poster;View shade,swipe;LinearLayout info,actions;TextView title,meta,fav,comments,back,hint;ProgressBar progress;JSONArray items=new JSONArray();java.util.HashSet<String> seen=new java.util.HashSet<>();int index=0,page=1,totalRows=0;boolean loading=false,more=true,tvMode=false,playing=true,dragging=false,swipeAnimating=false,storyReady=false;''',
'story fields')

s=one(s,
'''void build(){root=new FrameLayout(this);root.setBackgroundColor(Color.BLACK);poster=new ImageView(this);poster.setScaleType(ImageView.ScaleType.FIT_CENTER);poster.setBackgroundColor(Color.BLACK);root.addView(poster,new FrameLayout.LayoutParams(-1,-1));''',
'''void build(){root=new FrameLayout(this);root.setBackgroundColor(Color.BLACK);poster=new ImageView(this);poster.setScaleType(ImageView.ScaleType.CENTER_CROP);poster.setBackgroundColor(Color.BLACK);poster.setAlpha(0f);root.addView(poster,new FrameLayout.LayoutParams(-1,-1));''',
'full screen single story backdrop')

s=one(s,
'''web=new WebView(this);web.setBackgroundColor(Color.BLACK);SecurityGuard.hardenWebView();WebSettings ws=web.getSettings();ws.setJavaScriptEnabled(true);ws.setDomStorageEnabled(true);ws.setMediaPlaybackRequiresUserGesture(false);ws.setAllowFileAccess(false);ws.setAllowContentAccess(false);if(Build.VERSION.SDK_INT>=21)ws.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);web.setWebChromeClient(new WebChromeClient());web.setWebViewClient(new WebViewClient());web.addJavascriptInterface(new Object(){@android.webkit.JavascriptInterface public void ready(){runOnUiThread(()->{if(web!=null&&!dragging&&!swipeAnimating){web.setTranslationY(0f);web.animate().alpha(1f).setDuration(110).start();}});}},"StoryBridge");try{web.setLayerType(View.LAYER_TYPE_HARDWARE,null);}catch(Exception ignored){}root.addView(web,new FrameLayout.LayoutParams(-1,-1));
  if(!tvMode){topCoverMask=new ImageView(this);topCoverMask.setScaleType(ImageView.ScaleType.CENTER_CROP);topCoverMask.setBackgroundColor(Color.BLACK);topCoverMask.setAlpha(.82f);FrameLayout.LayoutParams ytm=new FrameLayout.LayoutParams(-1,dp(86),Gravity.TOP);root.addView(topCoverMask,ytm);bottomCoverMask=new ImageView(this);bottomCoverMask.setScaleType(ImageView.ScaleType.CENTER_CROP);bottomCoverMask.setBackgroundColor(Color.BLACK);bottomCoverMask.setAlpha(.82f);FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(-1,dp(108),Gravity.BOTTOM);root.addView(bottomCoverMask,ybm);}''',
'''web=new WebView(this);web.setBackgroundColor(Color.TRANSPARENT);SecurityGuard.hardenWebView();WebSettings ws=web.getSettings();ws.setJavaScriptEnabled(true);ws.setDomStorageEnabled(true);ws.setMediaPlaybackRequiresUserGesture(false);ws.setAllowFileAccess(false);ws.setAllowContentAccess(false);if(Build.VERSION.SDK_INT>=21)ws.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);web.setWebChromeClient(new WebChromeClient());web.setWebViewClient(new WebViewClient());web.addJavascriptInterface(new Object(){@android.webkit.JavascriptInterface public void ready(){runOnUiThread(()->{storyReady=true;if(web!=null&&!dragging&&!swipeAnimating)revealStory();});}@android.webkit.JavascriptInterface public void previewEnded(){runOnUiThread(()->{if(!dragging&&!swipeAnimating&&items.length()>0)animateStorySwap(true);});}},"StoryBridge");try{web.setLayerType(View.LAYER_TYPE_HARDWARE,null);}catch(Exception ignored){}root.addView(web,new FrameLayout.LayoutParams(-1,-1));''',
'remove repeated story cover strips')

s=one(s,
'''info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(18),dp(10),dp(94),dp(24));title=t("Carregando Stories…",19);title.setGravity(Gravity.LEFT);title.setTypeface(null,1);title.setMaxLines(3);title.setEllipsize(android.text.TextUtils.TruncateAt.END);info.addView(title,new LinearLayout.LayoutParams(-1,-2));meta=t("Yelly Doramas",12);meta.setGravity(Gravity.LEFT);meta.setTextColor(0xffffb7d8);meta.setPadding(0,dp(6),0,0);info.addView(meta,new LinearLayout.LayoutParams(-1,-2));FrameLayout.LayoutParams ip=new FrameLayout.LayoutParams(-1,dp(170),Gravity.BOTTOM);root.addView(info,ip);''',
'''info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(18),dp(10),dp(94),dp(10));title=t("Carregando Stories…",19);title.setGravity(Gravity.LEFT);title.setTypeface(null,1);title.setMaxLines(3);title.setEllipsize(android.text.TextUtils.TruncateAt.END);info.addView(title,new LinearLayout.LayoutParams(-1,-2));meta=t("Yelly Doramas",13);meta.setGravity(Gravity.LEFT);meta.setTypeface(null,1);meta.setTextColor(0xffff9ccc);meta.setPadding(0,dp(6),0,0);info.addView(meta,new LinearLayout.LayoutParams(-1,-2));FrameLayout.LayoutParams ip=new FrameLayout.LayoutParams(-1,dp(188),Gravity.BOTTOM);ip.setMargins(0,0,0,dp(34));root.addView(info,ip);''',
'move yelly label up')

old_methods='''void setSwipeOffset(float y){float lim=Math.max(1,root.getHeight());float v=Math.max(-lim,Math.min(lim,y));if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(poster!=null)poster.setTranslationY(v);if(shade!=null)shade.setTranslationY(v);if(info!=null)info.setTranslationY(v);if(actions!=null)actions.setTranslationY(v);}
 void animateSwipeBack(){if(root==null)return;swipeAnimating=true;animateSwipeViews(0,120,()->{swipeAnimating=false;if(web!=null)web.animate().alpha(1f).setDuration(90).start();});}
 void animateStorySwap(boolean forward){if(forward&&index+1>=items.length()){if(more)fetch();animateSwipeBack();return;}if(!forward&&index<=0){animateSwipeBack();return;}swipeAnimating=true;float h=Math.max(1,root.getHeight());float out=forward?-h:h;float incoming=forward?h:-h;animateSwipeViews(out,125,()->{int ni=forward?index+1:index-1;show(ni);setSwipeOffset(incoming);animateSwipeViews(0,155,()->swipeAnimating=false);});}
 void animateSwipeViews(float y,long ms,Runnable end){if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(poster!=null)poster.animate().translationY(y).setDuration(ms).start();if(shade!=null)shade.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)actions.animate().translationY(y).setDuration(ms).withEndAction(end).start();else if(end!=null)end.run();}'''
new_methods='''void revealStory(){if(web!=null){web.animate().cancel();web.setTranslationY(0f);web.animate().alpha(1f).setDuration(110).start();}if(poster!=null){poster.animate().cancel();poster.setTranslationY(0f);poster.animate().alpha(.36f).setDuration(130).start();}}
 void setSwipeOffset(float y){float lim=Math.max(1,root.getHeight());float v=Math.max(-lim,Math.min(lim,y));if(poster!=null){poster.animate().cancel();poster.setAlpha(0f);poster.setTranslationY(0f);}if(web!=null){web.animate().cancel();web.setAlpha(storyReady?1f:0f);web.setTranslationY(v);}if(shade!=null)shade.setTranslationY(v);if(info!=null)info.setTranslationY(v);if(actions!=null)actions.setTranslationY(v);}
 void animateSwipeBack(){if(root==null)return;swipeAnimating=true;animateSwipeViews(0,120,()->{swipeAnimating=false;if(storyReady)revealStory();});}
 void setIncomingOffset(float y){if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(poster!=null){poster.animate().cancel();poster.setAlpha(0f);poster.setTranslationY(0f);}if(shade!=null)shade.setTranslationY(y);if(info!=null)info.setTranslationY(y);if(actions!=null)actions.setTranslationY(y);}
 void animateIncomingViews(float y,long ms,Runnable end){if(shade!=null)shade.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)actions.animate().translationY(y).setDuration(ms).withEndAction(end).start();else if(end!=null)end.run();}
 void animateStorySwap(boolean forward){if(forward&&index+1>=items.length()){if(more)fetch();animateSwipeBack();return;}if(!forward&&index<=0){animateSwipeBack();return;}swipeAnimating=true;float h=Math.max(1,root.getHeight());float out=forward?-h:h;float incoming=forward?h:-h;animateSwipeViews(out,125,()->{int ni=forward?index+1:index-1;show(ni);setIncomingOffset(incoming);animateIncomingViews(0,155,()->{swipeAnimating=false;if(storyReady)revealStory();});});}
 void animateSwipeViews(float y,long ms,Runnable end){if(poster!=null){poster.animate().cancel();poster.setAlpha(0f);poster.setTranslationY(0f);}if(web!=null)web.animate().translationY(y).setDuration(ms).start();if(shade!=null)shade.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)actions.animate().translationY(y).setDuration(ms).withEndAction(end).start();else if(end!=null)end.run();}'''
s=one(s,old_methods,new_methods,'smooth swipe without cover flash')

s=one(s,
'''void show(int i){if(items.length()==0)return;index=Math.max(0,Math.min(items.length()-1,i));JSONObject x=items.optJSONObject(index);if(x==null)return;final int token=++storyToken;String id=x.optString("youtube_id","").replaceAll("[^A-Za-z0-9_-]","");String nm=cleanTitle(x.optString("name",x.optString("title","Yelly Doramas")));title.setText(nm);meta.setText("Yelly Doramas");if(progress!=null)progress.setProgress(0);fav.setText(isFav(x)?"♥\\nFavorito":"♡\\nFavoritar");String img=x.optString("portrait_img",x.optString("thumbnail",""));if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(!img.isEmpty()){Img.loadVisible(poster,img);if(topCoverMask!=null)Img.loadVisible(topCoverMask,img);if(bottomCoverMask!=null)Img.loadVisible(bottomCoverMask,img);}play(id);enrich(x,token);if(more&&index>=items.length()-20)fetch();}''',
'''void show(int i){if(items.length()==0)return;index=Math.max(0,Math.min(items.length()-1,i));JSONObject x=items.optJSONObject(index);if(x==null)return;storyReady=false;final int token=++storyToken;String id=x.optString("youtube_id","").replaceAll("[^A-Za-z0-9_-]","");String nm=cleanTitle(x.optString("name",x.optString("title","Yelly Doramas")));title.setText(nm);meta.setText("Yelly Doramas");if(progress!=null)progress.setProgress(0);fav.setText(isFav(x)?"♥\\nFavorito":"♡\\nFavoritar");String img=x.optString("portrait_img",x.optString("thumbnail",""));if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(poster!=null){poster.animate().cancel();poster.setAlpha(0f);poster.setTranslationY(0f);}if(!img.isEmpty())Img.loadVisible(poster,img);play(id);enrich(x,token);if(more&&index>=items.length()-20)fetch();}''',
'story show single backdrop')

old_play='''void play(String id){if(web==null||id==null||id.isEmpty())return;String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'><style>html,body{margin:0;width:100%;height:100%;background:#000;overflow:hidden}#p{position:absolute;left:0;top:0;width:100vw;height:100vh;border:0;background:#000}</style><script src='https://www.youtube.com/iframe_api'></script></head><body><div id='p'></div><script>var player;function onYouTubeIframeAPIReady(){player=new YT.Player('p',{videoId:'"+id+"',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,playsinline:1,rel:0,modestbranding:1,iv_load_policy:3,origin:'https://yellyplay.online'},events:{onReady:function(e){e.target.playVideo();try{StoryBridge.ready();}catch(x){}}}});}function gpToggle(){if(!player)return;var s=player.getPlayerState();if(s==1)player.pauseVideo();else player.playVideo();}function gpProgress(){try{var d=player&&player.getDuration?player.getDuration():0;if(!d)return 0;return Math.round((player.getCurrentTime()/d)*1000)}catch(e){return 0}}</script></body></html>";web.loadDataWithBaseURL("https://yellyplay.online/",html,"text/html","UTF-8",null);playing=true;progressHandler.removeCallbacks(progressTick);progressHandler.postDelayed(progressTick,450);}'''
new_play='''void play(String id){if(web==null||id==null||id.isEmpty())return;String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'><style>html,body{margin:0;width:100%;height:100%;background:transparent;overflow:hidden}#p{position:absolute;left:50%;top:50%;border:0;background:#000;transform:translate(-50%,-50%)}</style><script src='https://www.youtube.com/iframe_api'></script></head><body><div id='p'></div><script>var player,previewSent=false,previewLimit=120,tv="+(tvMode?"true":"false")+";function sizeP(){var p=document.getElementById('p');if(!p)return;var iw=window.innerWidth,ih=window.innerHeight,w=iw,h=ih;if(!tv){h=Math.min(ih,iw*16/9);w=Math.min(iw,h*9/16);}p.style.width=w+'px';p.style.height=h+'px';}sizeP();window.addEventListener('resize',sizeP);function finishPreview(){if(previewSent)return;previewSent=true;try{if(player)player.pauseVideo();StoryBridge.previewEnded();}catch(x){}}function onYouTubeIframeAPIReady(){player=new YT.Player('p',{videoId:'"+id+"',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,playsinline:1,rel:0,modestbranding:1,iv_load_policy:3,origin:'https://yellyplay.online'},events:{onReady:function(e){e.target.playVideo();try{StoryBridge.ready();}catch(x){}},onStateChange:function(e){if(e.data==0)finishPreview();}}});}function gpToggle(){if(!player)return;var s=player.getPlayerState();if(s==1)player.pauseVideo();else player.playVideo();}function gpProgress(){try{var d=player&&player.getDuration?player.getDuration():0,c=player&&player.getCurrentTime?player.getCurrentTime():0;if(!d)return 0;var lim=Math.min(d,previewLimit);if(c>=lim-.15)finishPreview();return Math.round((Math.min(c,lim)/lim)*1000)}catch(e){return 0}}</script></body></html>";web.loadDataWithBaseURL("https://yellyplay.online/",html,"text/html","UTF-8",null);playing=true;progressHandler.removeCallbacks(progressTick);progressHandler.postDelayed(progressTick,450);}'''
s=one(s,old_play,new_play,'two minute story preview and fitted player')

s=one(s,
'''String p=d.optString("portrait_img",d.optString("thumbnail",""));if(!p.isEmpty()){x.put("portrait_img",p);x.put("thumbnail",p);Img.loadVisible(poster,p);if(topCoverMask!=null)Img.loadVisible(topCoverMask,p);if(bottomCoverMask!=null)Img.loadVisible(bottomCoverMask,p);}''',
'''String p=d.optString("portrait_img",d.optString("thumbnail",""));if(!p.isEmpty()){x.put("portrait_img",p);x.put("thumbnail",p);Img.loadVisible(poster,p);}''',
'enrich single backdrop')

stories.write_text(s,encoding='utf-8')

y=yt.read_text(encoding='utf-8')

y=one(y,
'''ImageView playerBackdrop,topPosterMask,bottomPosterMask,brandPosterMask;''',
'''ImageView playerBackdrop;''',
'full player fields')

y=one(y,
'''playerBackdrop=new ImageView(this);playerBackdrop.setScaleType(ImageView.ScaleType.CENTER_CROP);playerBackdrop.setBackgroundColor(Color.BLACK);playerBackdrop.setAlpha(.52f);if(videoPoster!=null&&!videoPoster.trim().isEmpty())Img.loadVisible(playerBackdrop,videoPoster);root.addView(playerBackdrop,new FrameLayout.LayoutParams(-1,-1));''',
'''playerBackdrop=new ImageView(this);playerBackdrop.setScaleType(ImageView.ScaleType.CENTER_CROP);playerBackdrop.setBackgroundColor(Color.BLACK);playerBackdrop.setAlpha(.40f);if(videoPoster!=null&&!videoPoster.trim().isEmpty())Img.loadVisible(playerBackdrop,videoPoster);root.addView(playerBackdrop,new FrameLayout.LayoutParams(-1,-1));''',
'full player one backdrop')

old_masks='''root.addView(web,new FrameLayout.LayoutParams(-1,-1));
        brandPosterMask=new ImageView(this);brandPosterMask.setScaleType(ImageView.ScaleType.CENTER_CROP);brandPosterMask.setBackgroundColor(Color.BLACK);brandPosterMask.setAlpha(.90f);if(videoPoster!=null&&!videoPoster.trim().isEmpty())Img.loadVisible(brandPosterMask,videoPoster);FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(dp(148),dp(58),Gravity.RIGHT|Gravity.BOTTOM);ybm.setMargins(0,0,dp(2),dp(2));root.addView(brandPosterMask,ybm);

        if(!tvMode){
            int screenH=getResources().getDisplayMetrics().heightPixels;
            int topMaskH=Math.max(dp(48),Math.min(dp(82),(int)(screenH*0.09f)));
            int bottomMaskH=Math.max(dp(64),Math.min(dp(110),(int)(screenH*0.11f)));
            topPosterMask=new ImageView(this);topPosterMask.setScaleType(ImageView.ScaleType.CENTER_CROP);topPosterMask.setBackgroundColor(Color.BLACK);topPosterMask.setAlpha(.90f);if(videoPoster!=null&&!videoPoster.trim().isEmpty())Img.loadVisible(topPosterMask,videoPoster);
            FrameLayout.LayoutParams topMaskLp=new FrameLayout.LayoutParams(-1,topMaskH,Gravity.TOP);root.addView(topPosterMask,topMaskLp);
            bottomPosterMask=new ImageView(this);bottomPosterMask.setScaleType(ImageView.ScaleType.CENTER_CROP);bottomPosterMask.setBackgroundColor(Color.BLACK);bottomPosterMask.setAlpha(.90f);if(videoPoster!=null&&!videoPoster.trim().isEmpty())Img.loadVisible(bottomPosterMask,videoPoster);
            FrameLayout.LayoutParams bottomMaskLp=new FrameLayout.LayoutParams(-1,bottomMaskH,Gravity.BOTTOM);root.addView(bottomPosterMask,bottomMaskLp);
        }'''
new_masks='''root.addView(web,new FrameLayout.LayoutParams(-1,-1));
        View ytBrandMask=new View(this);ytBrandMask.setBackground(bg(0xcc0a0709,12));FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(dp(102),dp(36),Gravity.RIGHT|Gravity.BOTTOM);ybm.setMargins(0,0,dp(5),dp(5));root.addView(ytBrandMask,ybm);'''
y=one(y,old_masks,new_masks,'remove repeated full player poster strips')

old_html='''String tvCss=tvMode?"transform:scale(1.48);transform-origin:50% 50%;":"";
        String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'>"+
            "<style>html,body,#p{margin:0;padding:0;width:100%;height:100%;background:transparent;overflow:hidden}iframe{width:100%!important;height:100%!important;border:0;"+tvCss+"}</style>"+
            "<script src='https://www.youtube.com/iframe_api'></script></head><body><div id='p'></div><script>"+
            "var player,ready=false;function onYouTubeIframeAPIReady(){player=new YT.Player('p',{videoId:'"+videoId+"',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,iv_load_policy:3,cc_load_policy:0,playsinline:1,rel:0,modestbranding:1,origin:'https://yellyplay.online'},events:{onReady:function(e){ready=true;if("+resumeMs+">0)e.target.seekTo("+(resumeMs/1000.0)+",true);e.target.playVideo();AndroidBridge.playerReady();},onStateChange:function(e){if(e.data==0)AndroidBridge.completed();}}});}"+'''
new_html='''String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'>"+
            "<style>html,body{margin:0;padding:0;width:100%;height:100%;background:transparent;overflow:hidden}#p{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#000}iframe{width:100%!important;height:100%!important;border:0}</style>"+
            "<script src='https://www.youtube.com/iframe_api'></script></head><body><div id='p'></div><script>"+
            "var player,ready=false,tv="+(tvMode?"true":"false")+";function sizeP(){var p=document.getElementById('p');if(!p)return;var iw=window.innerWidth,ih=window.innerHeight,w=iw,h=ih;if(!tv){h=Math.min(ih,iw*16/9);w=Math.min(iw,h*9/16);}p.style.width=w+'px';p.style.height=h+'px';}sizeP();window.addEventListener('resize',sizeP);function onYouTubeIframeAPIReady(){player=new YT.Player('p',{videoId:'"+videoId+"',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,iv_load_policy:3,cc_load_policy:0,playsinline:1,rel:0,modestbranding:1,origin:'https://yellyplay.online'},events:{onReady:function(e){ready=true;if("+resumeMs+">0)e.target.seekTo("+(resumeMs/1000.0)+",true);e.target.playVideo();AndroidBridge.playerReady();},onStateChange:function(e){if(e.data==0)AndroidBridge.completed();}}});}"+'''
y=one(y,old_html,new_html,'full player fit with one backdrop')

yt.write_text(y,encoding='utf-8')

g=grad.read_text(encoding='utf-8')
if "versionCode 10012" not in g or "versionName '1.0.12'" not in g:
    raise SystemExit('expected Yelly 1.0.12 base')
g=g.replace('versionCode 10012','versionCode 10013',1).replace("versionName '1.0.12'","versionName '1.0.13'",1)
grad.write_text(g,encoding='utf-8')

(root/'app/RELEASE_NOTES.txt').write_text('''Yelly Doramas 1.0.13
Stories ajustados pelo vídeo de referência:
- Story vira um preview/rush de até 2 minutos; ao chegar ao limite passa automaticamente para o próximo.
- Botão Assistir continua abrindo o conteúdo completo.
- Swipe volta a acompanhar o dedo com o vídeo atual e não mostra a capa no meio da troca.
- Removidas as capas repetidas em cima e embaixo.
- Agora existe uma única capa em tela cheia como fundo atrás do vídeo, aparecendo apenas nas áreas livres do player.
- "Yelly Doramas" foi subido e destacado para não ficar escondido no rodapé.
Assistir:
- removidas as repetições da capa em faixas separadas;
- uma única capa preenche o fundo completo atrás do vídeo.
''',encoding='utf-8')
print('YELLY_113_RUSH_PREVIEW_BACKGROUND_OK')
