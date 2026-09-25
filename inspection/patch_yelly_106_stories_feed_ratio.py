from pathlib import Path
root=Path('work')
main=root/'app/src/main/java/fun/greenplay/app/MainActivity.java'
stories=root/'app/src/main/java/fun/greenplay/app/StoriesActivity.java'
grad=root/'app/build.gradle'

s=main.read_text(encoding='utf-8')
def one(old,new,label):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 got {n}')
    s=s.replace(old,new,1)

one('final int contentW=Math.max(dp(300),getResources().getDisplayMetrics().widthPixels-dp(36));final int cardW=Math.min(dp(250),(int)(contentW*.68f));final int cardH=(int)(cardW*1.27f);final int gap=dp(12);',
    'final int contentW=Math.max(dp(300),getResources().getDisplayMetrics().widthPixels-dp(36));final int cardW=Math.min(dp(250),(int)(contentW*.68f));final int cardH="Shorts".equals(activeHomeTab)?Math.max(dp(138),(int)(cardW*9f/16f)):(int)(cardW*1.27f);final int gap=dp(12);',
    'shorts carousel ratio')

one('int available=Math.max(dp(900),getResources().getDisplayMetrics().widthPixels-dp(80));int visible=Math.max(6,Math.min(8,screenWidthDp()/165));int gap=dp(12);int cardW=Math.max(dp(128),Math.min(dp(166),(available-gap*(visible-1))/visible));int cardH=(int)(cardW*1.38f);',
    'int available=Math.max(dp(900),getResources().getDisplayMetrics().widthPixels-dp(80));int visible=Math.max(6,Math.min(8,screenWidthDp()/165));int gap=dp(12);int cardW=Math.max(dp(128),Math.min(dp(166),(available-gap*(visible-1))/visible));int cardH="Shorts".equals(activeHomeTab)?Math.max(dp(90),(int)(cardW*9f/16f)):(int)(cardW*1.38f);',
    'tv shorts carousel ratio')

one('int start=mobileCategoryNextIndex,len=mobileCategoryRows.length(),end=Math.min(len,start+48),h=dp(196);',
    'int start=mobileCategoryNextIndex,len=mobileCategoryRows.length(),end=Math.min(len,start+48),shortH=Math.max(dp(64),(int)(mobileCategoryCardW*9f/16f)),h="Shorts".equals(activeHomeTab)?shortH+dp(48):dp(196);',
    'mobile grid row height')
one('for(int i=start;i<end;i++){JSONObject x=mobileCategoryRows.optJSONObject(i);if(x==null)continue;LinearLayout c=card(x);GridLayout.LayoutParams lp=new GridLayout.LayoutParams();lp.width=mobileCategoryCardW;lp.height=h;',
    'for(int i=start;i<end;i++){JSONObject x=mobileCategoryRows.optJSONObject(i);if(x==null)continue;LinearLayout c=card(x);if("Shorts".equals(activeHomeTab)&&c.getChildCount()>0){View p=c.getChildAt(0);ViewGroup.LayoutParams pl=p.getLayoutParams();pl.height=shortH;p.setLayoutParams(pl);}GridLayout.LayoutParams lp=new GridLayout.LayoutParams();lp.width=mobileCategoryCardW;lp.height=h;',
    'mobile grid poster ratio')

one('if(gen!=viewGen||g==null||g.getParent()==null)return;int end=Math.min(a.length(),start+(wideTvUi()?24:12));int h=wideTvUi()?dp(246):dp(196);',
    'if(gen!=viewGen||g==null||g.getParent()==null)return;int end=Math.min(a.length(),start+(wideTvUi()?24:12));int shortH=Math.max(dp(64),(int)(w*9f/16f));int h="Shorts".equals(activeHomeTab)?shortH+dp(48):(wideTvUi()?dp(246):dp(196));',
    'grid chunk height')
one('for(int i=start;i<end;i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;LinearLayout c=card(x);GridLayout.LayoutParams lp=new GridLayout.LayoutParams();lp.width=w;lp.height=h;',
    'for(int i=start;i<end;i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;LinearLayout c=card(x);if("Shorts".equals(activeHomeTab)&&c.getChildCount()>0){View p=c.getChildAt(0);ViewGroup.LayoutParams pl=p.getLayoutParams();pl.height=shortH;p.setLayoutParams(pl);}GridLayout.LayoutParams lp=new GridLayout.LayoutParams();lp.width=w;lp.height=h;',
    'grid chunk poster ratio')

one('c.addView(poster,new LinearLayout.LayoutParams(-1,dp(158)));',
    'c.addView(poster,new LinearLayout.LayoutParams(-1,"Shorts".equals(activeHomeTab)?dp(72):dp(158)));',
    'short card default poster')

main.write_text(s,encoding='utf-8')

st=stories.read_text(encoding='utf-8')
def r1(old,new,label):
    global st
    n=st.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 got {n}')
    st=st.replace(old,new,1)

r1('FrameLayout root;WebView web;ImageView poster;TextView title,meta,fav,comments,back,hint;JSONArray items=new JSONArray();int index=0,page=1;boolean loading=false,more=true,tvMode=false,playing=true;float downY=0,downX=0;String uid="";int accent=Color.rgb(184,0,125);android.content.SharedPreferences sp;int storyToken=0;',
'''FrameLayout root;WebView web;ImageView poster;View shade,swipe;LinearLayout info,actions;TextView title,meta,fav,comments,back,hint;ProgressBar progress;JSONArray items=new JSONArray();int index=0,page=1,totalRows=0;boolean loading=false,more=true,tvMode=false,playing=true,dragging=false,swipeAnimating=false;float downY=0,downX=0;String uid="",feedSeed=Long.toString(System.nanoTime(),36);int accent=Color.rgb(184,0,125);android.content.SharedPreferences sp;int storyToken=0;Handler progressHandler=new Handler(Looper.getMainLooper());
 Runnable progressTick=new Runnable(){public void run(){if(web==null||isFinishing())return;try{web.evaluateJavascript("javascript:gpProgress()",v->{try{String z=v==null?"":v.replace("\\\"","").replace("\"","");String[] p=z.split("\\|");if(p.length==2){double cur=Double.parseDouble(p[0]),dur=Double.parseDouble(p[1]);if(dur>0&&progress!=null)progress.setProgress((int)Math.max(0,Math.min(1000,(cur/dur)*1000)));}}catch(Exception ignored){}});}catch(Exception ignored){}progressHandler.postDelayed(this,350);}};''',
'stories fields')

r1('poster=new ImageView(this);poster.setScaleType(ImageView.ScaleType.CENTER_CROP);',
   'poster=new ImageView(this);poster.setScaleType(ImageView.ScaleType.FIT_CENTER);poster.setBackgroundColor(Color.BLACK);',
   'story poster fit')

r1('View shade=new View(this);GradientDrawable shadeBg=', 'shade=new View(this);GradientDrawable shadeBg=', 'shade field')
r1('View swipe=new View(this);swipe.setBackgroundColor(Color.TRANSPARENT);swipe.setOnTouchListener((v,e)->{if(e.getAction()==MotionEvent.ACTION_DOWN){downY=e.getY();downX=e.getX();return true;}if(e.getAction()==MotionEvent.ACTION_UP){float dy=e.getY()-downY,dx=e.getX()-downX;if(Math.abs(dy)>dp(65)&&Math.abs(dy)>Math.abs(dx)){if(dy<0)next();else prev();}else toggle();return true;}return true;});',
'''swipe=new View(this);swipe.setBackgroundColor(Color.TRANSPARENT);swipe.setOnTouchListener((v,e)->{if(swipeAnimating)return true;int a=e.getActionMasked();if(a==MotionEvent.ACTION_DOWN){downY=e.getY();downX=e.getX();dragging=false;return true;}if(a==MotionEvent.ACTION_MOVE){float dy=e.getY()-downY,dx=e.getX()-downX;if(Math.abs(dy)>dp(6)&&Math.abs(dy)>Math.abs(dx)){dragging=true;setSwipeOffset(dy);return true;}return true;}if(a==MotionEvent.ACTION_UP||a==MotionEvent.ACTION_CANCEL){float dy=e.getY()-downY,dx=e.getX()-downX;if(dragging&&Math.abs(dy)>dp(78)&&Math.abs(dy)>Math.abs(dx)){animateStorySwap(dy<0);}else{animateSwipeBack();if(!dragging)toggle();}dragging=false;return true;}return true;});''',
'live swipe')

r1('LinearLayout info=new LinearLayout(this);', 'info=new LinearLayout(this);', 'info field')
r1('LinearLayout actions=new LinearLayout(this);', 'actions=new LinearLayout(this);', 'actions field')

r1('hint=t(tvMode?"↑ ↓  trocar Story":"↑  deslize para o próximo",12);hint.setTextColor(0xffd4c4cc);FrameLayout.LayoutParams hp=new FrameLayout.LayoutParams(-2,dp(32),Gravity.TOP|Gravity.CENTER_HORIZONTAL);hp.setMargins(0,dp(16),0,0);root.addView(hint,hp);setContentView(root);}',
'''hint=t(tvMode?"↑ ↓  trocar Story":"↑  deslize para o próximo",12);hint.setTextColor(0xffd4c4cc);FrameLayout.LayoutParams hp=new FrameLayout.LayoutParams(-2,dp(32),Gravity.TOP|Gravity.CENTER_HORIZONTAL);hp.setMargins(0,dp(16),0,0);root.addView(hint,hp);
  progress=new ProgressBar(this,null,android.R.attr.progressBarStyleHorizontal);progress.setMax(1000);progress.setProgress(0);if(Build.VERSION.SDK_INT>=21){progress.setProgressTintList(android.content.res.ColorStateList.valueOf(accent));progress.setProgressBackgroundTintList(android.content.res.ColorStateList.valueOf(0x55ffffff));}FrameLayout.LayoutParams pg=new FrameLayout.LayoutParams(-1,dp(3),Gravity.TOP);pg.setMargins(dp(12),dp(4),dp(12),0);root.addView(progress,pg);setContentView(root);}''',
'progress bar')

r1('void fetch(){if(loading||!more)return;loading=true;final int p=page;Api.post("greenshorts",Api.m("user_id",uid,"page_no",String.valueOf(p),"page",String.valueOf(p),"offset",String.valueOf((p-1)*60),"limit","60","per_page","60"),new Api.CB(){public void ok(JSONObject j){loading=false;JSONArray a=j.optJSONArray("result");if(a!=null)for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x!=null&&!x.optString("youtube_id","").trim().isEmpty())items.put(x);}more=j.optBoolean("more_page",a!=null&&a.length()>=60);if(more)page=p+1;if(items.length()>0&&p==1)show(0);else if(items.length()==0)title.setText("Nenhum Story disponível agora.");}public void err(String e){loading=false;if(page<=1&&loadSeedFallback())return;title.setText("Não foi possível carregar os Stories.");}});}',
'''void fetch(){if(loading||!more)return;loading=true;final int p=page;final int size=120;Api.post("greenshorts",Api.m("user_id",uid,"random","1","seed",feedSeed,"page_no",String.valueOf(p),"page",String.valueOf(p),"offset",String.valueOf((p-1)*size),"limit",String.valueOf(size),"per_page",String.valueOf(size)),new Api.CB(){public void ok(JSONObject j){loading=false;totalRows=j.optInt("total_rows",totalRows);JSONArray a=j.optJSONArray("result");if(a!=null)for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x!=null&&!x.optString("youtube_id","").trim().isEmpty())items.put(x);}more=j.optBoolean("more_page",a!=null&&a.length()>=size);if(more)page=p+1;if(items.length()>0&&p==1)show(0);else if(items.length()==0)title.setText("Nenhum Story disponível agora.");}public void err(String e){loading=false;if(page<=1&&loadSeedFallback())return;title.setText("Não foi possível carregar os Stories.");}});}''',
'random full pagination')

r1('more=true;page=2;if(items.length()>0){show(0);return true;}',
   'shuffleItems();more=true;page=2;totalRows=Math.max(items.length(),totalRows);if(items.length()>0){show(0);return true;}',
   'fallback shuffle')

anchor=' String cleanTitle(String s){'
helpers=''' void shuffleItems(){try{java.util.ArrayList<JSONObject> list=new java.util.ArrayList<>();for(int i=0;i<items.length();i++){JSONObject x=items.optJSONObject(i);if(x!=null)list.add(x);}java.util.Collections.shuffle(list,new java.util.Random(System.nanoTime()));items=new JSONArray();for(JSONObject x:list)items.put(x);}catch(Exception ignored){}}
 void setSwipeOffset(float y){float v=Math.max(-root.getHeight(),Math.min(root.getHeight(),y));if(poster!=null)poster.setTranslationY(v);if(web!=null)web.setTranslationY(v);if(shade!=null)shade.setTranslationY(v);if(info!=null)info.setTranslationY(v);if(actions!=null)actions.setTranslationY(v);}
 void animateSwipeBack(){if(root==null)return;swipeAnimating=true;animateSwipeViews(0,130,()->swipeAnimating=false);}
 void animateStorySwap(boolean forward){if(forward&&index+1>=items.length()){if(more)fetch();animateSwipeBack();return;}if(!forward&&index<=0){animateSwipeBack();return;}swipeAnimating=true;float target=forward?-root.getHeight():root.getHeight();animateSwipeViews(target,145,()->{int ni=forward?index+1:index-1;setSwipeOffset(0);show(ni);swipeAnimating=false;});}
 void animateSwipeViews(float y,long ms,Runnable end){if(poster!=null)poster.animate().translationY(y).setDuration(ms).withEndAction(end).start();if(web!=null)web.animate().translationY(y).setDuration(ms).start();if(shade!=null)shade.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)actions.animate().translationY(y).setDuration(ms).start();}
'''
if anchor not in st: raise SystemExit('helper anchor')
st=st.replace(anchor,helpers+anchor,1)

r1('meta.setText("Yelly Doramas  •  "+(index+1)+" / "+items.length());',
   'meta.setText("Yelly Doramas  •  "+(index+1)+" / "+(totalRows>0?totalRows:items.length()));if(progress!=null)progress.setProgress(0);',
   'story total display')

r1('if(more&&index>=items.length()-8)fetch();',
   'if(more&&index>=items.length()-24)fetch();',
   'early pagination')

old_play='void play(String id){if(web==null||id==null||id.isEmpty())return;String html="<!doctype html><html><head><meta name=\'viewport\' content=\'width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no\'><style>html,body{margin:0;width:100%;height:100%;background:#000;overflow:hidden}#p{position:absolute;left:50%;top:50%;width:177.78vh;height:100vh;transform:translate(-50%,-50%);border:0;background:#000}@media (min-aspect-ratio:1/1){#p{width:100vw;height:56.25vw}}</style><script src=\'https://www.youtube.com/iframe_api\'></script></head><body><div id=\'p\'></div><script>var player;function onYouTubeIframeAPIReady(){player=new YT.Player(\'p\',{videoId:\'"+id+"\',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,playsinline:1,rel:0,modestbranding:1,iv_load_policy:3,origin:\'https://yellyplay.online\'},events:{onReady:function(e){e.target.playVideo();}}});}function gpToggle(){if(!player)return;var s=player.getPlayerState();if(s==1)player.pauseVideo();else player.playVideo();}</script></body></html>";web.loadDataWithBaseURL("https://yellyplay.online/",html,"text/html","UTF-8",null);playing=true;}'
new_play='''void play(String id){if(web==null||id==null||id.isEmpty())return;String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'><style>html,body{margin:0;width:100%;height:100%;background:#000;overflow:hidden}#p{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border:0;background:#000}</style><script src='https://www.youtube.com/iframe_api'></script></head><body><div id='p'></div><script>var player;function fit(){var w=innerWidth,h=innerHeight,p=document.getElementById('p'),pw=w,ph=w*9/16;if(ph>h){ph=h;pw=h*16/9}p.style.width=pw+'px';p.style.height=ph+'px'}addEventListener('resize',fit);fit();function onYouTubeIframeAPIReady(){player=new YT.Player('p',{videoId:'"+id+"',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,playsinline:1,rel:0,modestbranding:1,iv_load_policy:3,origin:'https://yellyplay.online'},events:{onReady:function(e){fit();e.target.playVideo();}}});}function gpToggle(){if(!player)return;var s=player.getPlayerState();if(s==1)player.pauseVideo();else player.playVideo();}function gpProgress(){try{return player.getCurrentTime()+'|'+player.getDuration()}catch(e){return '0|0'}}</script></body></html>";web.loadDataWithBaseURL("https://yellyplay.online/",html,"text/html","UTF-8",null);playing=true;progressHandler.removeCallbacks(progressTick);progressHandler.postDelayed(progressTick,500);}'''
r1(old_play,new_play,'fit video and progress')

r1('@Override protected void onPause(){if(web!=null)web.evaluateJavascript("javascript:if(player)player.pauseVideo()",null);super.onPause();}@Override protected void onDestroy(){if(web!=null){try{web.stopLoading();web.loadUrl("about:blank");web.destroy();}catch(Exception ignored){}web=null;}super.onDestroy();}',
'''@Override protected void onPause(){progressHandler.removeCallbacks(progressTick);if(web!=null)web.evaluateJavascript("javascript:if(player)player.pauseVideo()",null);super.onPause();}@Override protected void onResume(){super.onResume();if(web!=null)progressHandler.postDelayed(progressTick,450);}@Override protected void onDestroy(){progressHandler.removeCallbacksAndMessages(null);if(web!=null){try{web.stopLoading();web.loadUrl("about:blank");web.destroy();}catch(Exception ignored){}web=null;}super.onDestroy();}''',
'progress lifecycle')

stories.write_text(st,encoding='utf-8')

g=grad.read_text(encoding='utf-8').replace('versionCode 10005','versionCode 10006').replace("versionName '1.0.5'","versionName '1.0.6'")
grad.write_text(g,encoding='utf-8')
(root/'app/RELEASE_NOTES.txt').write_text('''Yelly Doramas 1.0.6
Stories preservam a proporção original do player, sem zoom/corte.
Swipe vertical acompanha o dedo durante o movimento e anima a troca.
Feed de Stories usa sequência aleatória por sessão e pagina até o catálogo inteiro.
Páginas de 120 itens e pré-carregamento antes do fim evitam parar em 60.
Barra superior mostra o progresso do vídeo.
Cards e carrossel de Doramas usam proporção horizontal do material original, sem blocos pretos altos.
''',encoding='utf-8')
print('YELLY_106_PATCH_OK')
