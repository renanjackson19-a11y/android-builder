from pathlib import Path

root=Path('work')
stories=root/'app/src/main/java/fun/greenplay/app/StoriesActivity.java'
grad=root/'app/build.gradle'

st=stories.read_text(encoding='utf-8')

def r1(old,new,label):
    global st
    n=st.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 got {n}')
    st=st.replace(old,new,1)

r1(
'FrameLayout root;WebView web;ImageView poster;TextView title,meta,fav,comments,back,hint;JSONArray items=new JSONArray();int index=0,page=1;boolean loading=false,more=true,tvMode=false,playing=true;float downY=0,downX=0;String uid="";int accent=Color.rgb(184,0,125);android.content.SharedPreferences sp;int storyToken=0;',
'''FrameLayout root;WebView web;ImageView poster;View shade,swipe;LinearLayout info,actions;TextView title,meta,fav,comments,back,hint;ProgressBar progress;JSONArray items=new JSONArray();java.util.HashSet<String> seen=new java.util.HashSet<>();int index=0,page=1,totalRows=0;boolean loading=false,more=true,tvMode=false,playing=true,dragging=false,swipeAnimating=false;float downY=0,downX=0;String uid="",feedSeed=Long.toString(System.nanoTime(),36);int accent=Color.rgb(184,0,125);android.content.SharedPreferences sp;int storyToken=0;Handler progressHandler=new Handler(Looper.getMainLooper());
 Runnable progressTick=new Runnable(){public void run(){if(web==null||isFinishing())return;try{web.evaluateJavascript("javascript:gpProgress()",v->{try{String z=v==null?"0":v.replaceAll("[^0-9]","");if(!z.isEmpty()&&progress!=null)progress.setProgress(Math.max(0,Math.min(1000,Integer.parseInt(z))));}catch(Exception ignored){}});}catch(Exception ignored){}progressHandler.postDelayed(this,350);}};''',
'stories fields')

r1(
'poster=new ImageView(this);poster.setScaleType(ImageView.ScaleType.CENTER_CROP);',
'poster=new ImageView(this);poster.setScaleType(ImageView.ScaleType.FIT_CENTER);poster.setBackgroundColor(Color.BLACK);',
'story poster contain')

r1('View shade=new View(this);GradientDrawable shadeBg=', 'shade=new View(this);GradientDrawable shadeBg=', 'shade field')

r1(
'View swipe=new View(this);swipe.setBackgroundColor(Color.TRANSPARENT);swipe.setOnTouchListener((v,e)->{if(e.getAction()==MotionEvent.ACTION_DOWN){downY=e.getY();downX=e.getX();return true;}if(e.getAction()==MotionEvent.ACTION_UP){float dy=e.getY()-downY,dx=e.getX()-downX;if(Math.abs(dy)>dp(65)&&Math.abs(dy)>Math.abs(dx)){if(dy<0)next();else prev();}else toggle();return true;}return true;});',
'''swipe=new View(this);swipe.setBackgroundColor(Color.TRANSPARENT);swipe.setOnTouchListener((v,e)->{if(swipeAnimating)return true;int a=e.getActionMasked();if(a==MotionEvent.ACTION_DOWN){downY=e.getY();downX=e.getX();dragging=false;return true;}if(a==MotionEvent.ACTION_MOVE){float dy=e.getY()-downY,dx=e.getX()-downX;if(Math.abs(dy)>dp(4)&&Math.abs(dy)>Math.abs(dx)){dragging=true;setSwipeOffset(dy);return true;}return true;}if(a==MotionEvent.ACTION_UP||a==MotionEvent.ACTION_CANCEL){float dy=e.getY()-downY,dx=e.getX()-downX;if(dragging&&Math.abs(dy)>dp(72)&&Math.abs(dy)>Math.abs(dx)){animateStorySwap(dy<0);}else{animateSwipeBack();if(!dragging)toggle();}dragging=false;return true;}return true;});''',
'live swipe')

r1('LinearLayout info=new LinearLayout(this);', 'info=new LinearLayout(this);', 'info field')
r1('LinearLayout actions=new LinearLayout(this);', 'actions=new LinearLayout(this);', 'actions field')

r1(
'hint=t(tvMode?"↑ ↓  trocar Story":"↑  deslize para o próximo",12);hint.setTextColor(0xffd4c4cc);FrameLayout.LayoutParams hp=new FrameLayout.LayoutParams(-2,dp(32),Gravity.TOP|Gravity.CENTER_HORIZONTAL);hp.setMargins(0,dp(16),0,0);root.addView(hint,hp);setContentView(root);}',
'''hint=t(tvMode?"↑ ↓  trocar Story":"↑  deslize para o próximo",12);hint.setTextColor(0xffd4c4cc);FrameLayout.LayoutParams hp=new FrameLayout.LayoutParams(-2,dp(32),Gravity.TOP|Gravity.CENTER_HORIZONTAL);hp.setMargins(0,dp(16),0,0);root.addView(hint,hp);
  progress=new ProgressBar(this,null,android.R.attr.progressBarStyleHorizontal);progress.setMax(1000);progress.setProgress(0);if(Build.VERSION.SDK_INT>=21){progress.setProgressTintList(android.content.res.ColorStateList.valueOf(accent));progress.setProgressBackgroundTintList(android.content.res.ColorStateList.valueOf(0x55ffffff));}FrameLayout.LayoutParams pg=new FrameLayout.LayoutParams(-1,dp(3),Gravity.TOP);pg.setMargins(dp(12),dp(4),dp(12),0);root.addView(progress,pg);setContentView(root);}''',
'progress bar')

r1(
'void fetch(){if(loading||!more)return;loading=true;final int p=page;Api.post("greenshorts",Api.m("user_id",uid,"page_no",String.valueOf(p),"page",String.valueOf(p),"offset",String.valueOf((p-1)*60),"limit","60","per_page","60"),new Api.CB(){public void ok(JSONObject j){loading=false;JSONArray a=j.optJSONArray("result");if(a!=null)for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x!=null&&!x.optString("youtube_id","").trim().isEmpty())items.put(x);}more=j.optBoolean("more_page",a!=null&&a.length()>=60);if(more)page=p+1;if(items.length()>0&&p==1)show(0);else if(items.length()==0)title.setText("Nenhum Story disponível agora.");}public void err(String e){loading=false;if(page<=1&&loadSeedFallback())return;title.setText("Não foi possível carregar os Stories.");}});}',
'''void fetch(){if(loading||!more)return;loading=true;final int p=page;final int size=60;Api.post("greenshorts",Api.m("user_id",uid,"random","1","seed",feedSeed,"page_no",String.valueOf(p),"page",String.valueOf(p),"offset",String.valueOf((p-1)*size),"limit",String.valueOf(size),"per_page",String.valueOf(size)),new Api.CB(){public void ok(JSONObject j){loading=false;totalRows=j.optInt("total_rows",j.optInt("total",totalRows));JSONArray a=j.optJSONArray("result");if(a!=null)for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;String y=x.optString("youtube_id","").trim();if(!y.isEmpty()&&seen.add(y))items.put(x);}if(totalRows<items.length())totalRows=items.length();if(j.has("more_page"))more=j.optBoolean("more_page");else more=a!=null&&a.length()>0&&(totalRows<=0||items.length()<totalRows);if(more)page=p+1;if(items.length()>0&&p==1){shuffleItems();show(0);}else if(items.length()==0)title.setText("Nenhum Story disponível agora.");}public void err(String e){loading=false;if(page<=1&&loadSeedFallback())return;title.setText("Não foi possível carregar os Stories.");}});}''',
'random full pagination')

r1(
'more=true;page=2;if(items.length()>0){show(0);return true;}',
'shuffleItems();more=true;page=2;totalRows=Math.max(items.length(),totalRows);if(items.length()>0){show(0);return true;}',
'fallback shuffle')

anchor=' String cleanTitle(String s){'
helpers=''' void shuffleItems(){try{java.util.ArrayList<JSONObject> list=new java.util.ArrayList<>();for(int i=0;i<items.length();i++){JSONObject x=items.optJSONObject(i);if(x!=null){String y=x.optString("youtube_id","").trim();if(!y.isEmpty())seen.add(y);list.add(x);}}java.util.Collections.shuffle(list,new java.util.Random(System.nanoTime()));items=new JSONArray();for(JSONObject x:list)items.put(x);}catch(Exception ignored){}}
 void setSwipeOffset(float y){float lim=Math.max(1,root.getHeight());float v=Math.max(-lim,Math.min(lim,y));if(poster!=null)poster.setTranslationY(v);if(web!=null)web.setTranslationY(v);if(shade!=null)shade.setTranslationY(v);if(info!=null)info.setTranslationY(v);if(actions!=null)actions.setTranslationY(v);}
 void animateSwipeBack(){if(root==null)return;swipeAnimating=true;animateSwipeViews(0,120,()->swipeAnimating=false);}
 void animateStorySwap(boolean forward){if(forward&&index+1>=items.length()){if(more)fetch();animateSwipeBack();return;}if(!forward&&index<=0){animateSwipeBack();return;}swipeAnimating=true;float h=Math.max(1,root.getHeight());float out=forward?-h:h;float incoming=forward?h:-h;animateSwipeViews(out,125,()->{int ni=forward?index+1:index-1;show(ni);setSwipeOffset(incoming);animateSwipeViews(0,155,()->swipeAnimating=false);});}
 void animateSwipeViews(float y,long ms,Runnable end){if(poster!=null)poster.animate().translationY(y).setDuration(ms).start();if(web!=null)web.animate().translationY(y).setDuration(ms).start();if(shade!=null)shade.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)actions.animate().translationY(y).setDuration(ms).withEndAction(end).start();else if(end!=null)end.run();}
'''
if anchor not in st:
    raise SystemExit('helper anchor missing')
st=st.replace(anchor,helpers+anchor,1)

r1(
'meta.setText("Yelly Doramas  •  "+(index+1)+" / "+items.length());',
'meta.setText("Yelly Doramas  •  "+(index+1)+" / "+(totalRows>0?totalRows:items.length()));if(progress!=null)progress.setProgress(0);',
'story total display')

r1(
'if(more&&index>=items.length()-8)fetch();',
'if(more&&index>=items.length()-20)fetch();',
'early pagination')

old_play='void play(String id){if(web==null||id==null||id.isEmpty())return;String html="<!doctype html><html><head><meta name=\\'viewport\\' content=\\'width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no\\'><style>html,body{margin:0;width:100%;height:100%;background:#000;overflow:hidden}#p{position:absolute;left:50%;top:50%;width:177.78vh;height:100vh;transform:translate(-50%,-50%);border:0;background:#000}@media (min-aspect-ratio:1/1){#p{width:100vw;height:56.25vw}}</style><script src=\\'https://www.youtube.com/iframe_api\\'></script></head><body><div id=\\'p\\'></div><script>var player;function onYouTubeIframeAPIReady(){player=new YT.Player(\\'p\\',{videoId:\\'"+id+"\\',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,playsinline:1,rel:0,modestbranding:1,iv_load_policy:3,origin:\\'https://yellyplay.online\\'},events:{onReady:function(e){e.target.playVideo();}}});}function gpToggle(){if(!player)return;var s=player.getPlayerState();if(s==1)player.pauseVideo();else player.playVideo();}</script></body></html>";web.loadDataWithBaseURL("https://yellyplay.online/",html,"text/html","UTF-8",null);playing=true;}'
new_play='''void play(String id){if(web==null||id==null||id.isEmpty())return;String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'><style>html,body{margin:0;width:100%;height:100%;background:#000;overflow:hidden}#p{position:absolute;left:0;top:0;width:100vw;height:100vh;border:0;background:#000}</style><script src='https://www.youtube.com/iframe_api'></script></head><body><div id='p'></div><script>var player;function onYouTubeIframeAPIReady(){player=new YT.Player('p',{videoId:'"+id+"',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,playsinline:1,rel:0,modestbranding:1,iv_load_policy:3,origin:'https://yellyplay.online'},events:{onReady:function(e){e.target.playVideo();}}});}function gpToggle(){if(!player)return;var s=player.getPlayerState();if(s==1)player.pauseVideo();else player.playVideo();}function gpProgress(){try{var d=player&&player.getDuration?player.getDuration():0;if(!d)return 0;return Math.round((player.getCurrentTime()/d)*1000)}catch(e){return 0}}</script></body></html>";web.loadDataWithBaseURL("https://yellyplay.online/",html,"text/html","UTF-8",null);playing=true;progressHandler.removeCallbacks(progressTick);progressHandler.postDelayed(progressTick,450);}'''
r1(old_play,new_play,'contain video and progress')

r1(
'@Override protected void onPause(){if(web!=null)web.evaluateJavascript("javascript:if(player)player.pauseVideo()",null);super.onPause();}@Override protected void onDestroy(){if(web!=null){try{web.stopLoading();web.loadUrl("about:blank");web.destroy();}catch(Exception ignored){}web=null;}super.onDestroy();}',
'''@Override protected void onPause(){progressHandler.removeCallbacks(progressTick);if(web!=null)web.evaluateJavascript("javascript:if(player)player.pauseVideo()",null);super.onPause();}@Override protected void onResume(){super.onResume();if(web!=null)progressHandler.postDelayed(progressTick,450);}@Override protected void onDestroy(){progressHandler.removeCallbacksAndMessages(null);if(web!=null){try{web.stopLoading();web.loadUrl("about:blank");web.destroy();}catch(Exception ignored){}web=null;}super.onDestroy();}''',
'progress lifecycle')

stories.write_text(st,encoding='utf-8')

g=grad.read_text(encoding='utf-8')
if "versionCode 10005" not in g or "versionName '1.0.5'" not in g:
    raise SystemExit('expected clean 1.0.5 base')
g=g.replace('versionCode 10005','versionCode 10006',1).replace("versionName '1.0.5'","versionName '1.0.6'",1)
grad.write_text(g,encoding='utf-8')

(root/'app/RELEASE_NOTES.txt').write_text('''Yelly Doramas 1.0.6 corrigida
Base limpa: Yelly Doramas 1.0.5.
Home preservada exatamente no layout vertical da 1.0.5, sem aplicar a tentativa horizontal anterior.
Stories com vídeo inteiro dentro da tela, sem zoom/corte do conteúdo.
Swipe vertical acompanha o dedo e anima a troca como feed de vídeos curtos.
Feed pede ordem aleatória por sessão, pagina continuamente em lotes de 60 e evita duplicatas.
Contador mostra posição / total do catálogo quando a API informa total_rows.
Barra superior mostra o progresso do tempo do vídeo.
Favoritar, Comentários e Assistir permanecem; comentários e respostas do painel são mantidos da base 1.0.5.
Mantidos títulos em português, sinopse pré-carregada, login corrigido, identidade do painel, botão sair e paleta Yelly.
''',encoding='utf-8')
print('YELLY_106_CORRECTED_PATCH_OK')
