from pathlib import Path
p=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
s=p.read_text()

def rep(old,new,n=1):
    global s
    assert old in s, old[:220]
    s=s.replace(old,new,n)

rep('if("Shorts".equals(selected)&&!currentProviderHasShorts())selected="Recomendações";',
    '/* 5.28.47: GreenShorts é catálogo global do YouTube, independente do provedor IPTV. */')
rep('if(!recommendations&&("Filmes".equals(selected)||"Séries".equals(selected)||"Shorts".equals(selected))&&!catalogTabReady(selected)){prepareCatalogTabAtomic(selected);return;}',
    'if(!recommendations&&("Filmes".equals(selected)||"Séries".equals(selected))&&!catalogTabReady(selected)){prepareCatalogTabAtomic(selected);return;}')
rep('if("Shorts".equals(selected)){JSONArray featured=featuredForShorts(12);if(featured.length()>0)featureCarousel(featured);loadShortsCategorySections(gen);return;}',
    'if("Shorts".equals(selected)){loadShortsCategorySections(gen);return;}')
rep('boolean catalogTabReady(String tab){JSONObject c=readHomeCache();if(c==null)return false;if("Filmes".equals(tab))return c.optInt("movie_first_pages_complete",0)==1;if("Séries".equals(tab))return c.optInt("series_first_pages_complete",0)==1;if("Shorts".equals(tab)){if(hasShortsSections(c))return true;return c.optInt("shorts_checked",0)==1;}return true;}',
    'boolean catalogTabReady(String tab){if("Shorts".equals(tab))return true;JSONObject c=readHomeCache();if(c==null)return false;if("Filmes".equals(tab))return c.optInt("movie_first_pages_complete",0)==1;if("Séries".equals(tab))return c.optInt("series_first_pages_complete",0)==1;return true;}')
rep('if(currentProviderHasShorts())addHomeTopMediaTab(tabs,R.drawable.top_shorts,"Shorts",selected);',
    'addHomeTopMediaTab(tabs,R.drawable.top_shorts,"Shorts",selected);')

old=''' void loadShortsCategorySections(final int gen){
  final LinearLayout host=body;if(host==null)return;JSONObject prepared=readHomeCache();JSONArray secs=prepared==null?null:prepared.optJSONArray("result");JSONArray loose=collectShortsLooseItems(secs);
  if(loose.length()>0){grid(loose);return;}
  TextView empty=t("Nenhum GreenShorts encontrado nesta fonte.",14);empty.setTextColor(0xff9da7a2);empty.setGravity(Gravity.CENTER);host.addView(empty,new LinearLayout.LayoutParams(-1,dp(72)));
 }'''
new=''' void loadShortsCategorySections(final int gen){
  final LinearLayout host=body;if(host==null)return;final TextView loading=t("Carregando GreenShorts…",14);loading.setTextColor(0xff9da7a2);loading.setGravity(Gravity.CENTER);host.addView(loading,new LinearLayout.LayoutParams(-1,dp(72)));
  fetchYoutubeShortsPage(1,0,new JSONArray(),new java.util.HashSet<String>(),gen,host,loading);
 }
 void fetchYoutubeShortsPage(final int page,final int offset,final JSONArray acc,final java.util.HashSet<String> seen,final int gen,final LinearLayout host,final TextView loading){
  if(!hostValid(gen,host))return;Api.post("greenshorts",Api.m("user_id",uid,"page_no",String.valueOf(page),"page",String.valueOf(page),"offset",String.valueOf(offset),"limit","120","per_page","120"),new Api.CB(){public void ok(JSONObject j){
   if(!hostValid(gen,host))return;JSONArray rows=j.optJSONArray("result");int added=0;if(rows!=null)for(int i=0;i<rows.length();i++){JSONObject x=rows.optJSONObject(i);if(x==null)continue;String y=x.optString("youtube_id","").trim();if(y.isEmpty())continue;String k="yt|"+y;if(seen.add(k)){acc.put(x);added++;}}
   boolean more=j.optBoolean("more_page",false);if(more&&rows!=null&&rows.length()>0&&added>0){fetchYoutubeShortsPage(page+1,offset+rows.length(),acc,seen,gen,host,loading);return;}
   if(loading.getParent()!=null)host.removeView(loading);if(acc.length()==0){TextView empty=t("Nenhum GreenShorts disponível no momento.",14);empty.setTextColor(0xff9da7a2);empty.setGravity(Gravity.CENTER);host.addView(empty,new LinearLayout.LayoutParams(-1,dp(72)));return;}JSONArray hero=new JSONArray();for(int i=0;i<Math.min(12,acc.length());i++){JSONObject x=acc.optJSONObject(i);if(x!=null)hero.put(x);}if(hero.length()>0)featureCarousel(hero);grid(acc);
  }public void err(String e){if(!hostValid(gen,host))return;if(loading.getParent()!=null)host.removeView(loading);TextView empty=t("Não foi possível carregar o GreenShorts.",14);empty.setTextColor(0xff9da7a2);empty.setGravity(Gravity.CENTER);host.addView(empty,new LinearLayout.LayoutParams(-1,dp(72)));}});
 }'''
rep(old,new)

rep('LinearLayout card(JSONObject x){JSONObject merged=mergeDetailJson(x,readDetailCache(x));final JSONObject use=merged==null?x:merged;',
    'LinearLayout card(JSONObject x){JSONObject merged=isYoutubeShort(x)?x:mergeDetailJson(x,readDetailCache(x));final JSONObject use=merged==null?x:merged;')
rep('boolean detailNeedsEnrich(JSONObject d){if(d==null)return true;',
    'boolean detailNeedsEnrich(JSONObject d){if(d==null)return true;if(isYoutubeShort(d))return false;')
rep('String detailPlayUrl(JSONObject d){return detailValue(d,"video_1080","video_720","video_480","video_320","video_url","stream_url","url");}',
''' boolean isYoutubeShort(JSONObject x){return x!=null&&(!x.optString("youtube_id","").trim().isEmpty()||"youtube".equalsIgnoreCase(x.optString("source","")));}
 String youtubeVideoId(JSONObject x){if(x==null)return "";String id=x.optString("youtube_id","").trim();if(id.isEmpty()){String raw=x.optString("youtube_url","");try{Uri u=Uri.parse(raw);id=u.getQueryParameter("v");}catch(Exception ignored){}}return id==null?"":id.replaceAll("[^A-Za-z0-9_-]","");}
 void openYoutubeVideo(JSONObject source,String title){String id=youtubeVideoId(source);if(id.isEmpty()){Toast.makeText(this,"Vídeo do YouTube indisponível.",Toast.LENGTH_SHORT).show();return;}Intent in=new Intent(this,YouTubePlayerActivity.class);in.putExtra("youtube_id",id);in.putExtra("title",title==null?"GreenShorts":title);startActivity(in);}
 String detailPlayUrl(JSONObject d){return detailValue(d,"video_1080","video_720","video_480","video_320","video_url","stream_url","url");}''')
rep('int vt=d.optInt("video_type",source.optInt("video_type",source.optInt("type_id",1)));boolean isSeries=vt==2||"series".equalsIgnoreCase(d.optString("type",""));',
    'int vt=d.optInt("video_type",source.optInt("video_type",source.optInt("type_id",1)));boolean isSeries=vt==2||"series".equalsIgnoreCase(d.optString("type",""));final boolean isYoutube=isYoutubeShort(source)||isYoutubeShort(d);')
rep('String providerId=source.optString("id",d.optString("id",""));if(!providerId.isEmpty()){View idBadge=detailIdBadge("ID:  "+providerId);',
    'String providerId=source.optString("id",d.optString("id",""));if(!isYoutube&&!providerId.isEmpty()){View idBadge=detailIdBadge("ID:  "+providerId);')

old_movie='''  if(!isSeries){
   renderMovieResume(source,d,host,displayTitle);
   boolean canResume=movieResumePosition(source.optString("id",d.optString("id","")))>0;
   View play=detailPrimaryAction(canResume?"Continuar assistindo":"Assistir");LinearLayout.LayoutParams plp=new LinearLayout.LayoutParams(-1,dp(62));plp.setMargins(0,dp(8),0,dp(12));host.addView(play,plp);
   play.setOnClickListener(v->guardPlaybackAction(()->showMovieActions(source,d,displayTitle)));
  }'''
new_movie='''  if(!isSeries){
   if(!isYoutube)renderMovieResume(source,d,host,displayTitle);
   boolean canResume=!isYoutube&&movieResumePosition(source.optString("id",d.optString("id","")))>0;
   View play=detailPrimaryAction(isYoutube?"Assistir no YouTube":(canResume?"Continuar assistindo":"Assistir"));LinearLayout.LayoutParams plp=new LinearLayout.LayoutParams(-1,dp(62));plp.setMargins(0,dp(8),0,dp(12));host.addView(play,plp);
   play.setOnClickListener(v->guardPlaybackAction(()->{if(isYoutube)openYoutubeVideo(source,displayTitle);else showMovieActions(source,d,displayTitle);}));
  }'''
rep(old_movie,new_movie)

rep('String raw="catalog52845_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);',
    'String raw="catalog52847_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);')
p.write_text(s)

manifest=Path('work/app/src/main/AndroidManifest.xml')
ms=manifest.read_text()
needle='  <activity android:name=".PlayerActivity" android:screenOrientation="unspecified" android:configChanges="orientation|screenSize"/>'
assert needle in ms
ms=ms.replace(needle,needle+'\n  <activity android:name=".YouTubePlayerActivity" android:screenOrientation="unspecified" android:configChanges="orientation|screenSize"/>',1)
manifest.write_text(ms)

Path('work/app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java').write_text(r'''package fun.greenplay.app;
import android.app.*;import android.os.*;import android.graphics.Color;import android.view.*;import android.webkit.*;
public class YouTubePlayerActivity extends Activity{
 WebView web;
 @Override public void onCreate(Bundle b){super.onCreate(b);getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);getWindow().setStatusBarColor(Color.BLACK);getWindow().setNavigationBarColor(Color.BLACK);getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN|View.SYSTEM_UI_FLAG_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);String id=getIntent()==null?"":getIntent().getStringExtra("youtube_id");if(id==null)id="";id=id.replaceAll("[^A-Za-z0-9_-]","");if(id.isEmpty()){finish();return;}web=new WebView(this);web.setBackgroundColor(Color.BLACK);WebSettings s=web.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setMediaPlaybackRequiresUserGesture(false);s.setLoadsImagesAutomatically(true);s.setUseWideViewPort(true);s.setLoadWithOverviewMode(true);web.setWebChromeClient(new WebChromeClient());web.setWebViewClient(new WebViewClient());setContentView(web,new ViewGroup.LayoutParams(-1,-1));String src="https://www.youtube.com/embed/"+id+"?autoplay=1&playsinline=1&rel=0&origin=https%3A%2F%2Fgreenplay.fun";String html="<html><head><meta name=viewport content='width=device-width,initial-scale=1,maximum-scale=1'><style>html,body{margin:0;padding:0;width:100%;height:100%;background:#000;overflow:hidden}iframe{width:100%;height:100%;border:0}</style></head><body><iframe src='"+src+"' allow='autoplay; encrypted-media; picture-in-picture' allowfullscreen></iframe></body></html>";web.loadDataWithBaseURL("https://greenplay.fun/",html,"text/html","UTF-8",null);}
 @Override public void onBackPressed(){if(web!=null&&web.canGoBack())web.goBack();else super.onBackPressed();}
 @Override protected void onDestroy(){if(web!=null){try{web.stopLoading();web.loadUrl("about:blank");web.removeAllViews();web.destroy();}catch(Exception ignored){}web=null;}super.onDestroy();}
}
''')

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52845' in t and "versionName '5.28.45'" in t
t=t.replace('versionCode 52845','versionCode 52847',1).replace("versionName '5.28.45'","versionName '5.28.47'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52847.txt').write_text("""GreenPlay 5.28.47

- GreenShorts agora é um catálogo global do YouTube administrado pelo painel.
- Não usa mais ReelShort/Shorts dos provedores IPTV.
- Busca /api/dtlive/greenshorts e mostra somente vídeos sincronizados do YouTube.
- Canal inicial: Flor da Vida.
- Reprodução dentro do GreenPlay via player incorporado oficial do YouTube.
- Sem download/extracao de MP4 do YouTube.
- GreenShorts continua na barra superior em todos os provedores.
""")

out=p.read_text()
assert 'Api.post("greenshorts"' in out
assert 'YouTubePlayerActivity' in out
assert 'isYoutubeShort' in out
assert 'catalog52847_' in out
assert 'versionCode 52847' in b.read_text()
print('OK 5.28.47')
