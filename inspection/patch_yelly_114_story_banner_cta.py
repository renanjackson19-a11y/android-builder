from pathlib import Path
root=Path('work')
stories=root/'app/src/main/java/fun/greenplay/app/StoriesActivity.java'
yt=root/'app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java'
grad=root/'app/build.gradle'

def one(s,old,new,label):
    n=s.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 got {n}')
    return s.replace(old,new,1)

s=stories.read_text(encoding='utf-8')
s=one(s,
'FrameLayout root;WebView web;ImageView poster;View shade,swipe;LinearLayout info,actions;TextView title,meta,fav,comments,back,hint;ProgressBar progress;',
'FrameLayout root;WebView web;ImageView poster,logoTop;View shade,swipe,topMask,bottomMask;LinearLayout info,actions;TextView title,meta,fav,comments,back,hint;ProgressBar progress;',
'fields')

s=one(s,
'void build(){root=new FrameLayout(this);root.setBackgroundColor(Color.BLACK);poster=new ImageView(this);poster.setScaleType(ImageView.ScaleType.CENTER_CROP);poster.setBackgroundColor(Color.BLACK);poster.setAlpha(0f);root.addView(poster,new FrameLayout.LayoutParams(-1,-1));',
'void build(){root=new FrameLayout(this);root.setBackgroundColor(Color.BLACK);poster=new ImageView(this);poster.setScaleType(ImageView.ScaleType.CENTER_CROP);poster.setBackgroundColor(Color.BLACK);poster.setImageResource(R.drawable.story_banner_bg);poster.setAlpha(1f);root.addView(poster,new FrameLayout.LayoutParams(-1,-1));',
'banner background')

s=one(s,
'root.addView(web,new FrameLayout.LayoutParams(-1,-1));\n  shade=new View(this);',
'root.addView(web,new FrameLayout.LayoutParams(-1,-1));\n  topMask=new View(this);topMask.setBackgroundColor(0xee10070f);FrameLayout.LayoutParams tmp=new FrameLayout.LayoutParams(-1,dp(74),Gravity.TOP);tmp.setMargins(dp(2),dp(84),dp(2),0);root.addView(topMask,tmp);\n  bottomMask=new View(this);bottomMask.setBackgroundColor(0xee10070f);FrameLayout.LayoutParams bmp=new FrameLayout.LayoutParams(-1,dp(94),Gravity.BOTTOM);bmp.setMargins(dp(2),0,dp(2),dp(158));root.addView(bottomMask,bmp);\n  shade=new View(this);',
'youtube masks')

s=one(s,
'root.addView(back,bp);\n  info=new LinearLayout(this);',
'root.addView(back,bp);\n  logoTop=new ImageView(this);logoTop.setImageResource(R.drawable.yelly_logo);logoTop.setScaleType(ImageView.ScaleType.FIT_CENTER);FrameLayout.LayoutParams lpLogo=new FrameLayout.LayoutParams(dp(92),dp(42),Gravity.TOP|Gravity.RIGHT);lpLogo.setMargins(0,dp(96),dp(12),0);root.addView(logoTop,lpLogo);\n  info=new LinearLayout(this);',
'logo top right')

old_info='info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(18),dp(10),dp(94),dp(10));title=t("Carregando Stories…",19);title.setGravity(Gravity.LEFT);title.setTypeface(null,1);title.setMaxLines(3);title.setEllipsize(android.text.TextUtils.TruncateAt.END);info.addView(title,new LinearLayout.LayoutParams(-1,-2));meta=t("Yelly Doramas",13);meta.setGravity(Gravity.LEFT);meta.setTypeface(null,1);meta.setTextColor(0xffff9ccc);meta.setPadding(0,dp(6),0,0);info.addView(meta,new LinearLayout.LayoutParams(-1,-2));FrameLayout.LayoutParams ip=new FrameLayout.LayoutParams(-1,dp(188),Gravity.BOTTOM);ip.setMargins(0,0,0,dp(34));root.addView(info,ip);'
new_info='info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(18),dp(8),dp(94),dp(10));title=t("Carregando Stories…",19);title.setGravity(Gravity.LEFT);title.setTypeface(null,1);title.setMaxLines(3);title.setEllipsize(android.text.TextUtils.TruncateAt.END);info.addView(title,new LinearLayout.LayoutParams(-1,-2));meta=t("▶  Assistir agora",13);meta.setGravity(Gravity.CENTER);meta.setTypeface(null,1);meta.setTextColor(Color.WHITE);meta.setBackground(round(accent,16));meta.setPadding(dp(14),dp(8),dp(14),dp(8));meta.setOnClickListener(v->openFull());LinearLayout.LayoutParams mlp=new LinearLayout.LayoutParams(-2,dp(42));mlp.setMargins(0,dp(9),0,0);info.addView(meta,mlp);FrameLayout.LayoutParams ip=new FrameLayout.LayoutParams(-1,dp(190),Gravity.BOTTOM);ip.setMargins(0,0,0,dp(36));root.addView(info,ip);'
s=one(s,old_info,new_info,'assistir agora cta')

old_actions='actions=new LinearLayout(this);actions.setOrientation(LinearLayout.VERTICAL);actions.setGravity(Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);fav=action("♡\\nFavoritar");fav.setOnClickListener(v->toggleFav());actions.addView(fav,new LinearLayout.LayoutParams(dp(78),dp(74)));comments=action("💬\\nComentários");LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(dp(78),dp(74));cp.setMargins(0,dp(8),0,0);actions.addView(comments,cp);comments.setOnClickListener(v->openComments());TextView open=action("▶\\nAssistir");LinearLayout.LayoutParams op=new LinearLayout.LayoutParams(dp(78),dp(74));op.setMargins(0,dp(8),0,0);actions.addView(open,op);open.setOnClickListener(v->openFull());FrameLayout.LayoutParams ap=new FrameLayout.LayoutParams(dp(82),dp(258),Gravity.RIGHT|Gravity.BOTTOM);ap.setMargins(0,0,dp(7),dp(92));root.addView(actions,ap);'
new_actions='actions=new LinearLayout(this);actions.setOrientation(LinearLayout.VERTICAL);actions.setGravity(Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);fav=action("♡\\nFavoritar");fav.setOnClickListener(v->toggleFav());actions.addView(fav,new LinearLayout.LayoutParams(dp(78),dp(74)));comments=action("💬\\nComentários");LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(dp(78),dp(74));cp.setMargins(0,dp(8),0,0);actions.addView(comments,cp);comments.setOnClickListener(v->openComments());FrameLayout.LayoutParams ap=new FrameLayout.LayoutParams(dp(82),dp(176),Gravity.RIGHT|Gravity.BOTTOM);ap.setMargins(0,0,dp(7),dp(126));root.addView(actions,ap);'
s=one(s,old_actions,new_actions,'right actions')

s=one(s,
'void revealStory(){if(web!=null){web.animate().cancel();web.setTranslationY(0f);web.animate().alpha(1f).setDuration(110).start();}if(poster!=null){poster.animate().cancel();poster.setTranslationY(0f);poster.animate().alpha(.36f).setDuration(130).start();}}',
'void revealStory(){if(web!=null){web.animate().cancel();web.setTranslationY(0f);web.animate().alpha(1f).setDuration(110).start();}if(poster!=null){poster.animate().cancel();poster.setAlpha(1f);poster.setTranslationY(0f);}}',
'reveal fixed banner')

s=one(s,
'void setSwipeOffset(float y){float lim=Math.max(1,root.getHeight());float v=Math.max(-lim,Math.min(lim,y));if(poster!=null){poster.animate().cancel();poster.setAlpha(0f);poster.setTranslationY(0f);}if(web!=null){web.animate().cancel();web.setAlpha(storyReady?1f:0f);web.setTranslationY(v);}if(shade!=null)shade.setTranslationY(v);if(info!=null)info.setTranslationY(v);if(actions!=null)actions.setTranslationY(v);}',
'void setSwipeOffset(float y){float lim=Math.max(1,root.getHeight());float v=Math.max(-lim,Math.min(lim,y));if(web!=null){web.animate().cancel();web.setAlpha(storyReady?1f:0f);web.setTranslationY(v);}if(shade!=null)shade.setTranslationY(v);if(info!=null)info.setTranslationY(v);if(actions!=null)actions.setTranslationY(v);}',
'fixed banner during drag')

s=one(s,
'void setIncomingOffset(float y){if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(poster!=null){poster.animate().cancel();poster.setAlpha(0f);poster.setTranslationY(0f);}if(shade!=null)shade.setTranslationY(y);if(info!=null)info.setTranslationY(y);if(actions!=null)actions.setTranslationY(y);}',
'void setIncomingOffset(float y){if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(shade!=null)shade.setTranslationY(y);if(info!=null)info.setTranslationY(y);if(actions!=null)actions.setTranslationY(y);}',
'fixed incoming banner')

s=one(s,
'void animateSwipeViews(float y,long ms,Runnable end){if(poster!=null){poster.animate().cancel();poster.setAlpha(0f);poster.setTranslationY(0f);}if(web!=null)web.animate().translationY(y).setDuration(ms).start();if(shade!=null)shade.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)actions.animate().translationY(y).setDuration(ms).withEndAction(end).start();else if(end!=null)end.run();}',
'void animateSwipeViews(float y,long ms,Runnable end){if(web!=null)web.animate().translationY(y).setDuration(ms).start();if(shade!=null)shade.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)actions.animate().translationY(y).setDuration(ms).withEndAction(end).start();else if(end!=null)end.run();}',
'fixed banner animation')

old_show='void show(int i){if(items.length()==0)return;index=Math.max(0,Math.min(items.length()-1,i));JSONObject x=items.optJSONObject(index);if(x==null)return;storyReady=false;final int token=++storyToken;String id=x.optString("youtube_id","").replaceAll("[^A-Za-z0-9_-]","");String nm=cleanTitle(x.optString("name",x.optString("title","Yelly Doramas")));title.setText(nm);meta.setText("Yelly Doramas");if(progress!=null)progress.setProgress(0);fav.setText(isFav(x)?"♥\\nFavorito":"♡\\nFavoritar");String img=x.optString("portrait_img",x.optString("thumbnail",""));if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(poster!=null){poster.animate().cancel();poster.setAlpha(0f);poster.setTranslationY(0f);}if(!img.isEmpty())Img.loadVisible(poster,img);play(id);enrich(x,token);if(more&&index>=items.length()-20)fetch();}'
new_show='void show(int i){if(items.length()==0)return;index=Math.max(0,Math.min(items.length()-1,i));JSONObject x=items.optJSONObject(index);if(x==null)return;storyReady=false;final int token=++storyToken;String id=x.optString("youtube_id","").replaceAll("[^A-Za-z0-9_-]","");String nm=cleanTitle(x.optString("name",x.optString("title","Yelly Doramas")));title.setText(nm);meta.setText("▶  Assistir agora");if(progress!=null)progress.setProgress(0);fav.setText(isFav(x)?"♥\\nFavorito":"♡\\nFavoritar");if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(poster!=null){poster.animate().cancel();poster.setAlpha(1f);poster.setTranslationY(0f);poster.setImageResource(R.drawable.story_banner_bg);}play(id);enrich(x,token);if(more&&index>=items.length()-20)fetch();}'
s=one(s,old_show,new_show,'show fixed banner')

old_play='void play(String id){if(web==null||id==null||id.isEmpty())return;String html="<!doctype html><html><head><meta name=\'viewport\' content=\'width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no\'><style>html,body{margin:0;width:100%;height:100%;background:transparent;overflow:hidden}#p{position:absolute;left:50%;top:50%;border:0;background:#000;transform:translate(-50%,-50%)}</style><script src=\'https://www.youtube.com/iframe_api\'></script></head><body><div id=\'p\'></div><script>var player,previewSent=false,previewLimit=120,tv="+(tvMode?"true":"false")+";function sizeP(){var p=document.getElementById(\'p\');if(!p)return;var iw=window.innerWidth,ih=window.innerHeight,w=iw,h=ih;if(!tv){h=Math.min(ih,iw*16/9);w=Math.min(iw,h*9/16);}p.style.width=w+\'px\';p.style.height=h+\'px\';}sizeP();window.addEventListener(\'resize\',sizeP);function finishPreview(){if(previewSent)return;previewSent=true;try{if(player)player.pauseVideo();StoryBridge.previewEnded();}catch(x){}}function onYouTubeIframeAPIReady(){player=new YT.Player(\'p\',{videoId:\'"+id+"\',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,playsinline:1,rel:0,modestbranding:1,iv_load_policy:3,origin:\'https://yellyplay.online\'},events:{onReady:function(e){e.target.playVideo();try{StoryBridge.ready();}catch(x){}},onStateChange:function(e){if(e.data==0)finishPreview();}}});}function gpToggle(){if(!player)return;var s=player.getPlayerState();if(s==1)player.pauseVideo();else player.playVideo();}function gpProgress(){try{var d=player&&player.getDuration?player.getDuration():0,c=player&&player.getCurrentTime?player.getCurrentTime():0;if(!d)return 0;var lim=Math.min(d,previewLimit);if(c>=lim-.15)finishPreview();return Math.round((Math.min(c,lim)/lim)*1000)}catch(e){return 0}}</script></body></html>";web.loadDataWithBaseURL("https://yellyplay.online/",html,"text/html","UTF-8",null);playing=true;progressHandler.removeCallbacks(progressTick);progressHandler.postDelayed(progressTick,450);}'
new_play='void play(String id){if(web==null||id==null||id.isEmpty())return;String html="<!doctype html><html><head><meta name=\'viewport\' content=\'width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no\'><style>html,body{margin:0;width:100%;height:100%;background:transparent;overflow:hidden}#p{position:absolute;left:50%;border:0;background:#000;transform:translate(-50%,-50%);overflow:hidden}</style><script src=\'https://www.youtube.com/iframe_api\'></script></head><body><div id=\'p\'></div><script>var player,previewSent=false,previewLimit=120,tv="+(tvMode?"true":"false")+";function sizeP(){var p=document.getElementById(\'p\');if(!p)return;var iw=window.innerWidth,ih=window.innerHeight,w=iw,h=ih;if(!tv){var top=84,bottom=158,avail=Math.max(320,ih-top-bottom);h=Math.min(avail,iw*16/9);w=Math.min(iw*.96,h*9/16);p.style.top=(top+avail/2)+\'px\';}else{p.style.top=\'50%\';}p.style.width=w+\'px\';p.style.height=h+\'px\';}sizeP();window.addEventListener(\'resize\',sizeP);function finishPreview(){if(previewSent)return;previewSent=true;try{if(player)player.pauseVideo();StoryBridge.previewEnded();}catch(x){}}function onYouTubeIframeAPIReady(){player=new YT.Player(\'p\',{videoId:\'"+id+"\',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,playsinline:1,rel:0,modestbranding:1,iv_load_policy:3,origin:\'https://yellyplay.online\'},events:{onReady:function(e){e.target.playVideo();try{StoryBridge.ready();}catch(x){}},onStateChange:function(e){if(e.data==0)finishPreview();}}});}function gpToggle(){if(!player)return;var s=player.getPlayerState();if(s==1)player.pauseVideo();else player.playVideo();}function gpProgress(){try{var d=player&&player.getDuration?player.getDuration():0,c=player&&player.getCurrentTime?player.getCurrentTime():0;if(!d)return 0;var lim=Math.min(d,previewLimit);if(c>=lim-.15)finishPreview();return Math.round((Math.min(c,lim)/lim)*1000)}catch(e){return 0}}</script></body></html>";web.loadDataWithBaseURL("https://yellyplay.online/",html,"text/html","UTF-8",null);playing=true;progressHandler.removeCallbacks(progressTick);progressHandler.postDelayed(progressTick,450);}'
s=one(s,old_play,new_play,'story player layout')

s=one(s,
'String p=d.optString("portrait_img",d.optString("thumbnail",""));if(!p.isEmpty()){x.put("portrait_img",p);x.put("thumbnail",p);Img.loadVisible(poster,p);}String desc=d.optString("description",d.optString("overview",""));',
'String p=d.optString("portrait_img",d.optString("thumbnail",""));if(!p.isEmpty()){x.put("portrait_img",p);x.put("thumbnail",p);}String desc=d.optString("description",d.optString("overview",""));',
'do not replace banner')

stories.write_text(s,encoding='utf-8')

y=yt.read_text(encoding='utf-8')
y=one(y,
'playerBackdrop=new ImageView(this);playerBackdrop.setScaleType(ImageView.ScaleType.CENTER_CROP);playerBackdrop.setBackgroundColor(Color.BLACK);playerBackdrop.setAlpha(.40f);if(videoPoster!=null&&!videoPoster.trim().isEmpty())Img.loadVisible(playerBackdrop,videoPoster);root.addView(playerBackdrop,new FrameLayout.LayoutParams(-1,-1));',
'playerBackdrop=new ImageView(this);playerBackdrop.setScaleType(ImageView.ScaleType.CENTER_CROP);playerBackdrop.setBackgroundColor(Color.BLACK);playerBackdrop.setAlpha(1f);if(videoPoster!=null&&!videoPoster.trim().isEmpty())Img.loadVisible(playerBackdrop,videoPoster);root.addView(playerBackdrop,new FrameLayout.LayoutParams(-1,-1));View backdropShade=new View(this);backdropShade.setBackgroundColor(0x66000000);root.addView(backdropShade,new FrameLayout.LayoutParams(-1,-1));',
'full player cover background')

y=one(y,
'View ytBrandMask=new View(this);ytBrandMask.setBackground(bg(0xcc0a0709,12));FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(dp(102),dp(36),Gravity.RIGHT|Gravity.BOTTOM);ybm.setMargins(0,0,dp(5),dp(5));root.addView(ytBrandMask,ybm);',
'View ytBrandMask=new View(this);ytBrandMask.setBackground(bg(0xee10070f,12));FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(dp(112),dp(40),Gravity.RIGHT|Gravity.BOTTOM);ybm.setMargins(0,0,dp(5),dp(106));root.addView(ytBrandMask,ybm);',
'full player youtube brand mask')

y=one(y,
'bp.setMargins(dp(14),dp(14),0,0);root.addView(back,bp);\n        back.bringToFront();',
'bp.setMargins(dp(14),dp(14),0,0);root.addView(back,bp);\n        ImageView logoTop=new ImageView(this);logoTop.setImageResource(R.drawable.yelly_logo);logoTop.setScaleType(ImageView.ScaleType.FIT_CENTER);FrameLayout.LayoutParams lpp=new FrameLayout.LayoutParams(dp(92),dp(42),Gravity.TOP|Gravity.RIGHT);lpp.setMargins(0,dp(18),dp(12),0);root.addView(logoTop,lpp);\n        back.bringToFront();',
'full player logo')

yt.write_text(y,encoding='utf-8')

g=grad.read_text(encoding='utf-8')
if "versionCode 10013" not in g or "versionName '1.0.13'" not in g: raise SystemExit('wrong base')
g=g.replace('versionCode 10013','versionCode 10014',1).replace("versionName '1.0.13'","versionName '1.0.14'",1)
grad.write_text(g,encoding='utf-8')
print('PATCH114_OK')
