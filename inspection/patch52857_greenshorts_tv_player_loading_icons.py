from pathlib import Path

gradle=Path("work/app/build.gradle")
g=gradle.read_text()
assert "versionCode 52856" in g
assert "versionName '5.28.56'" in g
g=g.replace("versionCode 52856","versionCode 52857",1)
g=g.replace("versionName '5.28.56'","versionName '5.28.57'",1)
gradle.write_text(g)

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

old='''int tvChannelListGeneration=0,tvBrowserGridGeneration=0; Runnable tvChannelRefreshTask=null; boolean tvChannelChunkPending=false; ScrollView tvCatalogGridScroll=null; GridLayout tvCatalogGrid=null;'''
new='''int tvChannelListGeneration=0,tvBrowserGridGeneration=0; Runnable tvChannelRefreshTask=null; boolean tvChannelChunkPending=false; GridLayout tvShortsGrid=null; int tvShortsCardW=0,tvShortsGridGen=0; ScrollView tvCatalogGridScroll=null; GridLayout tvCatalogGrid=null;'''
assert old in s
s=s.replace(old,new,1)

old='''mobileCategoryGreenShorts=false;mobileCategorySeen.clear();mobileCategoryLoadingFooter=null;mobileCategoryLoadingText=null;mobileCategoryLoadingProgress=null;if(body!=null)'''
new='''mobileCategoryGreenShorts=false;mobileCategorySeen.clear();mobileCategoryLoadingFooter=null;mobileCategoryLoadingText=null;mobileCategoryLoadingProgress=null;tvShortsGrid=null;tvShortsCardW=0;tvShortsGridGen=0;if(body!=null)'''
assert old in s
s=s.replace(old,new,1)

old='''if(currentProviderHasLive()){navTv=tvHeroNavAction("TV",()->tvNavigate(2));uiTextSize(navTv,16);menu.addView(navTv,new LinearLayout.LayoutParams(dp(54),dp(58)));}else navTv=null;'''
new='''if(currentProviderHasLive()){navTv=tvHeroNavAction("",()->tvNavigate(2));navTv.setContentDescription("TV");try{Drawable tvIcon=getResources().getDrawable(R.drawable.top_tv);tvIcon.setBounds(0,0,dp(58),dp(32));navTv.setCompoundDrawables(tvIcon,null,null,null);navTv.setCompoundDrawablePadding(0);}catch(Exception ignored){navTv.setText("TV");uiTextSize(navTv,16);}menu.addView(navTv,new LinearLayout.LayoutParams(dp(66),dp(58)));}else navTv=null;'''
assert old in s
s=s.replace(old,new,1)

old='''navMovies=tvHeroNavAction("Filmes",()->{if(tvMode)openTvCatalogBrowser(1,"Filmes",false);else{if(detailOpen)closeDetails();homeTab("Filmes");}});uiTextSize(navMovies,16);menu.addView(navMovies,new LinearLayout.LayoutParams(dp(78),dp(58)));'''
new='''navMovies=tvHeroNavAction("",()->{if(tvMode)openTvCatalogBrowser(1,"Filmes",false);else{if(detailOpen)closeDetails();homeTab("Filmes");}});navMovies.setContentDescription("Filmes");try{Drawable movieIcon=getResources().getDrawable(R.drawable.top_filmes);movieIcon.setBounds(0,0,dp(82),dp(30));navMovies.setCompoundDrawables(movieIcon,null,null,null);navMovies.setCompoundDrawablePadding(0);}catch(Exception ignored){navMovies.setText("Filmes");uiTextSize(navMovies,16);}menu.addView(navMovies,new LinearLayout.LayoutParams(dp(90),dp(58)));'''
assert old in s
s=s.replace(old,new,1)

old='''navSeries=tvHeroNavAction("Séries",()->{if(tvMode)openTvCatalogBrowser(2,"Séries",false);else{if(detailOpen)closeDetails();homeTab("Séries");}});uiTextSize(navSeries,16);menu.addView(navSeries,new LinearLayout.LayoutParams(dp(78),dp(58)));'''
new='''navSeries=tvHeroNavAction("",()->{if(tvMode)openTvCatalogBrowser(2,"Séries",false);else{if(detailOpen)closeDetails();homeTab("Séries");}});navSeries.setContentDescription("Séries");try{Drawable seriesIcon=getResources().getDrawable(R.drawable.top_series);seriesIcon.setBounds(0,0,dp(82),dp(30));navSeries.setCompoundDrawables(seriesIcon,null,null,null);navSeries.setCompoundDrawablePadding(0);}catch(Exception ignored){navSeries.setText("Séries");uiTextSize(navSeries,16);}menu.addView(navSeries,new LinearLayout.LayoutParams(dp(90),dp(58)));'''
assert old in s
s=s.replace(old,new,1)

old='''void loadShortsCategorySections(final int gen){
  final LinearLayout host=body;if(host==null)return;
  if(wideTvUi()){
   final TextView loading=t("Carregando mais conteúdo…",14);loading.setTextColor(0xff9da7a2);loading.setGravity(Gravity.CENTER);host.addView(loading,new LinearLayout.LayoutParams(-1,dp(56)));
   fetchYoutubeShortsPage(1,0,new JSONArray(),new java.util.HashSet<String>(),gen,host,loading);return;
  }
  JSONArray seed=readGreenShortsSeedCache();
  if(seed.length()>0)featureCarousel(seed);
  grid(seed);
  startGreenShortsPaging(seed,gen);
 }'''
new='''void loadShortsCategorySections(final int gen){
  final LinearLayout host=body;if(host==null)return;
  JSONArray seed=readGreenShortsSeedCache();
  if(wideTvUi()){
   final java.util.HashSet<String> seen=new java.util.HashSet<>();
   for(int i=0;i<seed.length();i++){JSONObject x=seed.optJSONObject(i);if(x==null)continue;String y=x.optString("youtube_id","").trim();String k=!y.isEmpty()?"yt|"+y:itemKey(x);if(k!=null&&!k.trim().isEmpty())seen.add(k);}
   if(seed.length()>0)grid(seed);
   fetchYoutubeShortsTvProgressive(1,0,seen,gen,host);
   return;
  }
  if(seed.length()>0)featureCarousel(seed);
  grid(seed);
  startGreenShortsPaging(seed,gen);
 }'''
assert old in s
s=s.replace(old,new,1)

marker=''' void fetchYoutubeShortsPage(final int page,final int offset,final JSONArray acc,final java.util.HashSet<String> seen,final int gen,final LinearLayout host,final TextView loading){'''
assert marker in s
insert=''' void fetchYoutubeShortsTvProgressive(final int page,final int offset,final java.util.HashSet<String> seen,final int gen,final LinearLayout host){
  if(!hostValid(gen,host)||!wideTvUi()||gen!=viewGen)return;
  Api.post("greenshorts",Api.m("user_id",uid,"page_no",String.valueOf(page),"page",String.valueOf(page),"offset",String.valueOf(offset),"limit","120","per_page","120"),new Api.CB(){public void ok(JSONObject j){
   if(!hostValid(gen,host)||gen!=viewGen)return;
   JSONArray rows=j.optJSONArray("result");JSONArray fresh=new JSONArray();if(rows!=null)for(int i=0;i<rows.length();i++){JSONObject x=rows.optJSONObject(i);if(x==null)continue;String y=x.optString("youtube_id","").trim();String k=!y.isEmpty()?"yt|"+y:itemKey(x);if(k==null||k.trim().isEmpty())continue;if(seen.add(k))fresh.put(x);}
   if(page==1&&rows!=null&&rows.length()>0)saveGreenShortsSeedCache(rows);
   if(tvShortsGrid==null||tvShortsGridGen!=gen){if(fresh.length()>0)grid(fresh);}else if(fresh.length()>0&&tvShortsCardW>0){addGridChunk(tvShortsGrid,fresh,0,tvShortsCardW,gen);}
   boolean more=j.optBoolean("more_page",rows!=null&&rows.length()>=120);
   if(more&&rows!=null&&rows.length()>0)host.postDelayed(()->fetchYoutubeShortsTvProgressive(page+1,offset+rows.length(),seen,gen,host),35);
   else if(tvShortsGrid==null&&fresh.length()==0){TextView empty=t("Nenhum GreenShorts disponível no momento.",14);empty.setTextColor(0xff9da7a2);empty.setGravity(Gravity.CENTER);host.addView(empty,new LinearLayout.LayoutParams(-1,dp(72)));}
  }public void err(String e){if(!hostValid(gen,host)||gen!=viewGen)return;if(tvShortsGrid==null){TextView empty=t("Não foi possível carregar o GreenShorts.",14);empty.setTextColor(0xff9da7a2);empty.setGravity(Gravity.CENTER);host.addView(empty,new LinearLayout.LayoutParams(-1,dp(72)));}}});
 }
'''
s=s.replace(marker,insert+marker,1)

old='''if(wideTvUi()){if(a!=null&&a.length()>0)addGridChunk(g,a,0,w,gen);return;}'''
new='''if(wideTvUi()){if("Shorts".equals(activeHomeTab)){tvShortsGrid=g;tvShortsCardW=w;tvShortsGridGen=gen;}if(a!=null&&a.length()>0)addGridChunk(g,a,0,w,gen);return;}'''
assert old in s
s=s.replace(old,new,1)

old='''in.putExtra("poster",detailValue(source,"thumbnail","portrait_img","poster","image"));int resume=restart?0:greenShortResumePosition(source);'''
new='''in.putExtra("poster",detailValue(source,"thumbnail","portrait_img","poster","image"));in.putExtra("tv_mode",tvMode);int resume=restart?0:greenShortResumePosition(source);'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

yp=Path("work/app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java")
y=yp.read_text()
old='''import android.content.res.ColorStateList;'''
new='''import android.content.res.ColorStateList;
import android.content.pm.ActivityInfo;'''
assert old in y
y=y.replace(old,new,1)

old='''tvMode=DeviceCompat.isTelevisionDevice(this);
        getWindow().setFlags'''
new='''tvMode=(getIntent()!=null&&getIntent().getBooleanExtra("tv_mode",false))||DeviceCompat.isTelevisionDevice(this);
        try{setRequestedOrientation(tvMode?ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE:ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);}catch(Exception ignored){}
        getWindow().setFlags'''
assert old in y
y=y.replace(old,new,1)
yp.write_text(y)
