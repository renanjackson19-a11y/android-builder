from pathlib import Path

root=Path("work")

def replace_method(text, marker, new_method):
    start=text.find(marker)
    if start<0:
        raise SystemExit("method marker not found: "+marker)
    brace=text.find("{", start)
    if brace<0:
        raise SystemExit("opening brace not found: "+marker)
    depth=0
    end=None
    for i in range(brace,len(text)):
        ch=text[i]
        if ch=="{": depth+=1
        elif ch=="}":
            depth-=1
            if depth==0:
                end=i+1
                break
    if end is None:
        raise SystemExit("method end not found: "+marker)
    return text[:start]+new_method+text[end:]

# Stories: use only the Yelly mini-series feed, never GreenPlay movie categories.
stories=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=stories.read_text(encoding="utf-8")
s=s.replace(
    "int index=0, accent=Color.rgb(184,0,125), storyToken=0, sourceIndex=0, fetchRound=0, pendingCategoryCalls=0;",
    "int index=0, accent=Color.rgb(184,0,125), storyToken=0, sourceIndex=0, fetchRound=0, pendingCategoryCalls=0, storyPage=1;",
    1
)

s=replace_method(s,"    void fetchCatalog()","""    void fetchCatalog(){fetchGreenShortsPage();}""")
s=replace_method(s,"    void fetchCategoryWave()","""    void fetchCategoryWave(){fetchGreenShortsPage();}""")
s=replace_method(s,"    void categoryDone()","""    void categoryDone(){}""")
s=replace_method(s,"    void appendCatalog(JSONArray a)","""    void appendGreenShorts(JSONArray a){if(a==null)return;for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;String y=x.optString("youtube_id","").trim();String id=x.optString("id",x.optString("video_id",y)).trim();String direct=playUrl(x);if(id.isEmpty()&&direct.isEmpty())continue;String k=!y.isEmpty()?"gs|"+y:"gs|"+id+"|"+direct;if(seen.add(k)){try{x.put("video_type",1);x.put("type_id",1);x.put("source","greenshorts");}catch(Exception ignored){}items.put(x);}}}""")

anchor="    void fetchCategoryWave(){fetchGreenShortsPage();}"
insert=anchor+"""

    void fetchGreenShortsPage(){
        if(loading)return;loading=true;if(items.length()==0)title.setText("Carregando minisséries…");
        final int page=Math.max(1,storyPage++);final int offset=(page-1)*120;final String seed=String.valueOf(System.nanoTime());
        Api.post("greenshorts",Api.m("user_id",uid,"page_no",String.valueOf(page),"page",String.valueOf(page),"offset",String.valueOf(offset),"limit","120","per_page","120","random","1","seed",seed),new Api.CB(){
            public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");int before=items.length();appendGreenShorts(a);loading=false;if(items.length()>0){if(before==0){shuffleArray(items);index=0;show(0);}}else if(page<4){fetchGreenShortsPage();}else title.setText("Nenhuma minissérie disponível agora.");}
            public void err(String e){loading=false;if(items.length()==0){if(page<4)fetchGreenShortsPage();else title.setText("Não foi possível carregar as minisséries.");}}
        });
    }"""
if anchor not in s:
    raise SystemExit("fetchCategoryWave insert anchor missing")
s=s.replace(anchor,insert,1)

s=replace_method(s,"    void resolveItem(JSONObject x,int token,boolean forFull)","""    void resolveItem(JSONObject x,int token,boolean forFull){
        String direct=playUrl(x);if(!direct.isEmpty()){currentResolved=x;if(forFull)launchFull(x);else startPreview(x,token);return;}
        String q=x.optString("original_title",x.optString("name",x.optString("title",""))).trim();
        if(q.isEmpty()){if(forFull)Toast.makeText(this,"Conteúdo indisponível.",Toast.LENGTH_SHORT).show();else advanceUnavailable();return;}
        Api.post("dorama_enrich",Api.m("title",q,"display_name",x.optString("name",x.optString("title","")),"thumbnail",x.optString("thumbnail",x.optString("portrait_img","")),"landscape",x.optString("landscape",x.optString("backdrop","")),"series_key",x.optString("series_key",""),"category_name",x.optString("category_name","Yelly Doramas"),"language","pt-BR","lang","pt-BR","locale","pt-BR"),new Api.CB(){
            public void ok(JSONObject j){if(token!=storyToken&&!forFull)return;JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;JSONObject merged=mergeJson(x,d);currentResolved=merged;if(playUrl(merged).isEmpty()){if(forFull)Toast.makeText(StoriesActivity.this,"Esta minissérie ainda não possui vídeo direto.",Toast.LENGTH_SHORT).show();else advanceUnavailable();return;}if(forFull)launchFull(merged);else startPreview(merged,token);}
            public void err(String e){if(forFull)Toast.makeText(StoriesActivity.this,"Não foi possível preparar esta minissérie.",Toast.LENGTH_SHORT).show();else advanceUnavailable();}
        });
    }""")

s=replace_method(s,"    String key(JSONObject x)","""    String key(JSONObject x){if(x==null)return "";String y=x.optString("youtube_id","").trim();if(!y.isEmpty())return "gs|"+y;return "gs|"+x.optString("id",x.optString("video_id",x.optString("name","")));}""")
s=replace_method(s,"    String commentId(JSONObject x)","""    String commentId(JSONObject x){if(x==null)return "";String y=x.optString("youtube_id","").trim();return !y.isEmpty()?y:x.optString("id",x.optString("video_id",""));}""")

s=s.replace('Api.post("add_comment",Api.m("user_id",uid,"youtube_id","","video_id",vid,',
            'Api.post("add_comment",Api.m("user_id",uid,"youtube_id",x.optString("youtube_id",""),"video_id",vid,',1)
s=s.replace('Api.post("get_comment",Api.m("user_id",uid,"youtube_id","","video_id",vid,"limit","80")',
            'Api.post("get_comment",Api.m("user_id",uid,"youtube_id",x.optString("youtube_id",""),"video_id",vid,"limit","80")',1)

listener='''            @Override public void onPlayerError(PlaybackException error){if(!tryNextSource())advanceUnavailable();}'''
listener_new='''            @Override public void onVideoSizeChanged(androidx.media3.common.VideoSize v){if(v!=null&&v.height>0){float par=v.pixelWidthHeightRatio<=0?1f:v.pixelWidthHeightRatio;fitStoryVideo((v.width*par)/(float)v.height);}}
            @Override public void onPlayerError(PlaybackException error){if(!tryNextSource())advanceUnavailable();}'''
if listener not in s:
    raise SystemExit("Stories player listener anchor missing")
s=s.replace(listener,listener_new,1)

start_preview='''    void startPreview(JSONObject x,int token){if(token!=storyToken||player==null)return;collectSources(x);if(sourceUrls.isEmpty()){advanceUnavailable();return;}setSource(sourceIndex);}'''
fit_method='''    void fitStoryVideo(float ar){if(tvMode||playerView==null||root==null||ar<=0)return;root.post(()->{int fw=root.getWidth(),fh=root.getHeight();if(fw<=0||fh<=0)return;int top=dp(64),bottom=dp(150),avail=Math.max(dp(220),fh-top-bottom);int w=fw,h=Math.max(1,Math.round(w/ar));if(h>avail){h=avail;w=Math.max(1,Math.round(h*ar));}FrameLayout.LayoutParams lp=new FrameLayout.LayoutParams(w,h,Gravity.TOP|Gravity.CENTER_HORIZONTAL);lp.topMargin=top+Math.max(0,(avail-h)/2);playerView.setLayoutParams(lp);});}

'''+start_preview
if start_preview not in s:
    raise SystemExit("startPreview anchor missing")
s=s.replace(start_preview,fit_method,1)
stories.write_text(s,encoding="utf-8")

# Home/catalog mini-series: never launch the YouTube player.
main=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
m=main.read_text(encoding="utf-8")
m=replace_method(m," void openYoutubeVideo(JSONObject source,String title,boolean restart)",""" void openYoutubeVideo(JSONObject source,String title,boolean restart){if(source==null)return;String direct=detailPlayUrl(source);if(!direct.isEmpty()){openPlayableUrl(source,title==null?"Yelly Doramas":title,false,direct);return;}Api.post("dorama_enrich",doramaEnrichArgs(source),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;JSONObject merged=mergeDetailJson(source,d);String u=detailPlayUrl(merged);if(u.isEmpty()){runOnUiThread(()->showAppNotice("Esta minissérie ainda não possui vídeo direto cadastrado.",true));return;}saveDetailCache(source,merged);runOnUiThread(()->openPlayableUrl(merged,title==null?"Yelly Doramas":title,false,u));}public void err(String e){runOnUiThread(()->showAppNotice("Não foi possível preparar esta minissérie.",true));}});}""")
m=replace_method(m," void renderGreenShortsResume(JSONObject source,LinearLayout host,String title)",""" void renderGreenShortsResume(JSONObject source,LinearLayout host,String title){}""")
m=replace_method(m," void showGreenShortsActions(JSONObject source,String title)",""" void showGreenShortsActions(JSONObject source,String title){openYoutubeVideo(source,title,false);}""")
m=m.replace('in.putExtra("force_portrait",!tvMode&&"Shorts".equals(activeHomeTab));',
            'in.putExtra("force_portrait",!tvMode&&("Shorts".equals(activeHomeTab)||isYoutubeShort(source)));',1)
main.write_text(m,encoding="utf-8")

# Full native player: show the film art behind the video, without internal black letterbox taking the whole screen.
player=root/"app/src/main/java/fun/greenplay/app/PlayerActivity.java"
p=player.read_text(encoding="utf-8")
p=p.replace(
    'boolean live=false,prepared=false,switching=false,tickerStarted=false,episodeQueue=false,tvMode=false,forcePortrait=false,resumeAfterBackground=false,seekingTouch=false,shortsLandscapeCanvas=false;',
    'boolean live=false,prepared=false,switching=false,tickerStarted=false,episodeQueue=false,tvMode=false,forcePortrait=false,resumeAfterBackground=false,seekingTouch=false,shortsLandscapeCanvas=false; float lastVideoAspect=0f;',
    1
)
p=replace_method(p," void applyDisplayMode()",""" void applyDisplayMode(){
  if(playerView==null)return;
  playerView.setScaleX(1f);playerView.setScaleY(1f);
  if(forcePortrait&&!tvMode&&displayMode==3){
   playerView.setResizeMode(AspectRatioFrameLayout.RESIZE_MODE_FIT);
   if(lastVideoAspect>0)fitPortraitVideo(lastVideoAspect);
   if(displayModeButton!=null)displayModeButton.setText("▣ Tela");
   return;
  }
  playerView.setLayoutParams(new FrameLayout.LayoutParams(-1,-1,Gravity.CENTER));
  if(displayMode==1)playerView.setResizeMode(AspectRatioFrameLayout.RESIZE_MODE_ZOOM);
  else if(displayMode==2)playerView.setResizeMode(AspectRatioFrameLayout.RESIZE_MODE_FILL);
  else playerView.setResizeMode(AspectRatioFrameLayout.RESIZE_MODE_FIT);
  if(displayModeButton!=null)displayModeButton.setText(displayMode==1?"▣ Zoom":displayMode==2?"▣ Preencher":"▣ Completo");
  if(!forcePortrait)getSharedPreferences("gp",0).edit().putInt("player_display_mode",displayMode).apply();
 }""")
insert_after=''' void cycleDisplayMode(){if(forcePortrait&&!tvMode){displayMode=displayMode==3?0:(displayMode==0?1:3);}else displayMode=(displayMode+1)%3;applyDisplayMode();}'''
fit=''' void fitPortraitVideo(float ar){if(!forcePortrait||tvMode||playerView==null||frame==null||ar<=0)return;frame.post(()->{int fw=frame.getWidth(),fh=frame.getHeight();if(fw<=0||fh<=0)return;int top=dp(54),bottom=dp(118),avail=Math.max(dp(220),fh-top-bottom);int w=fw,h=Math.max(1,Math.round(w/ar));if(h>avail){h=avail;w=Math.max(1,Math.round(h*ar));}FrameLayout.LayoutParams lp=new FrameLayout.LayoutParams(w,h,Gravity.TOP|Gravity.CENTER_HORIZONTAL);lp.topMargin=top+Math.max(0,(avail-h)/2);playerView.setLayoutParams(lp);});}
'''+insert_after
if insert_after not in p:
    raise SystemExit("cycleDisplayMode anchor missing")
p=p.replace(insert_after,fit,1)

old_vs='''@Override public void onVideoSizeChanged(VideoSize v){if(forcePortrait&&!tvMode&&v!=null&&v.height>0){float par=v.pixelWidthHeightRatio<=0?1f:v.pixelWidthHeightRatio;float ar=(v.width*par)/(float)v.height;shortsLandscapeCanvas=ar>1.15f;if(displayMode==3)applyDisplayMode();}}'''
new_vs='''@Override public void onVideoSizeChanged(VideoSize v){if(v!=null&&v.height>0){float par=v.pixelWidthHeightRatio<=0?1f:v.pixelWidthHeightRatio;float ar=(v.width*par)/(float)v.height;lastVideoAspect=ar;shortsLandscapeCanvas=ar>1.15f;if(forcePortrait&&!tvMode&&displayMode==3)fitPortraitVideo(ar);}}'''
if old_vs not in p:
    raise SystemExit("Player video size anchor missing")
p=p.replace(old_vs,new_vs,1)
player.write_text(p,encoding="utf-8")

manifest=root/"app/src/main/AndroidManifest.xml"
x=manifest.read_text(encoding="utf-8")
x=x.replace('  <activity android:name=".YouTubePlayerActivity" android:exported="false" android:screenOrientation="unspecified" android:configChanges="orientation|screenSize"/>\n','',1)
manifest.write_text(x,encoding="utf-8")

grad=root/"app/build.gradle"
g=grad.read_text(encoding="utf-8")
if "versionCode 10015" not in g or "versionName '1.0.15'" not in g:
    raise SystemExit("wrong 1.0.15 base")
g=g.replace("versionCode 10015","versionCode 10016",1).replace("versionName '1.0.15'","versionName '1.0.16'",1)
grad.write_text(g,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.16
- Stories voltaram para a fonte correta de minisséries do Yelly (greenshorts), sem puxar filmes do catálogo GreenPlay.
- Reprodução dos Stories e das minisséries do catálogo não abre mais o player do YouTube.
- Só usa URLs diretas autorizadas retornadas pelo catálogo/enriquecimento; itens sem vídeo direto são ignorados/avisados em vez de abrir YouTube.
- Banner fixo enviado pelo usuário permanece como fundo dos Stories.
- Player completo usa a capa/backdrop do próprio conteúdo atrás do vídeo e o vídeo é dimensionado para deixar esse fundo visível nas áreas livres.
- Mantidos Favoritar, Comentários, Assistir agora e preview de até 2 minutos.
""",encoding="utf-8")
print("YELLY_116_FIXED")
