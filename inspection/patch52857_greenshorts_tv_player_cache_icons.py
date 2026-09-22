from pathlib import Path

gradle=Path("work/app/build.gradle")
g=gradle.read_text()
assert "versionCode 52856" in g and "versionName '5.28.56'" in g
g=g.replace("versionCode 52856","versionCode 52857",1).replace("versionName '5.28.56'","versionName '5.28.57'",1)
gradle.write_text(g)

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

pairs=[
(
'if(currentProviderHasLive()){navTv=tvHeroNavAction("TV",()->tvNavigate(2));uiTextSize(navTv,16);menu.addView(navTv,new LinearLayout.LayoutParams(dp(54),dp(58)));}else navTv=null;',
'if(currentProviderHasLive()){navTv=tvHeroNavAction("",()->tvNavigate(2));navTv.setContentDescription("TV");navTv.setGravity(Gravity.CENTER);try{Drawable tvIcon=getResources().getDrawable(R.drawable.top_tv);tvIcon.setBounds(0,0,dp(60),dp(38));navTv.setCompoundDrawables(tvIcon,null,null,null);navTv.setCompoundDrawablePadding(0);}catch(Exception ignored){navTv.setText("TV");uiTextSize(navTv,16);}menu.addView(navTv,new LinearLayout.LayoutParams(dp(72),dp(58)));}else navTv=null;'
),
(
'navFootball=tvHeroNavAction("",()->openTvFootball());navFootball.setContentDescription("Futebol");try{Drawable fut=getResources().getDrawable(R.drawable.football_logo);fut.setBounds(0,0,dp(108),dp(38));navFootball.setCompoundDrawables(fut,null,null,null);navFootball.setCompoundDrawablePadding(0);}catch(Exception ignored){navFootball.setText("Futebol");}menu.addView(navFootball,new LinearLayout.LayoutParams(dp(116),dp(58)));',
'navFootball=tvHeroNavAction("",()->openTvFootball());navFootball.setContentDescription("Futebol");navFootball.setGravity(Gravity.CENTER);try{Drawable fut=getResources().getDrawable(R.drawable.football_logo);fut.setBounds(0,0,dp(68),dp(38));navFootball.setCompoundDrawables(fut,null,null,null);navFootball.setCompoundDrawablePadding(0);}catch(Exception ignored){navFootball.setText("Futebol");}menu.addView(navFootball,new LinearLayout.LayoutParams(dp(80),dp(58)));'
),
(
'navMovies=tvHeroNavAction("Filmes",()->{if(tvMode)openTvCatalogBrowser(1,"Filmes",false);else{if(detailOpen)closeDetails();homeTab("Filmes");}});uiTextSize(navMovies,16);menu.addView(navMovies,new LinearLayout.LayoutParams(dp(78),dp(58)));',
'navMovies=tvHeroNavAction("",()->{if(tvMode)openTvCatalogBrowser(1,"Filmes",false);else{if(detailOpen)closeDetails();homeTab("Filmes");}});navMovies.setContentDescription("Filmes");navMovies.setGravity(Gravity.CENTER);try{Drawable movies=getResources().getDrawable(R.drawable.top_filmes);movies.setBounds(0,0,dp(60),dp(38));navMovies.setCompoundDrawables(movies,null,null,null);navMovies.setCompoundDrawablePadding(0);}catch(Exception ignored){navMovies.setText("Filmes");uiTextSize(navMovies,16);}menu.addView(navMovies,new LinearLayout.LayoutParams(dp(72),dp(58)));'
),
(
'navSeries=tvHeroNavAction("Séries",()->{if(tvMode)openTvCatalogBrowser(2,"Séries",false);else{if(detailOpen)closeDetails();homeTab("Séries");}});uiTextSize(navSeries,16);menu.addView(navSeries,new LinearLayout.LayoutParams(dp(78),dp(58)));',
'navSeries=tvHeroNavAction("",()->{if(tvMode)openTvCatalogBrowser(2,"Séries",false);else{if(detailOpen)closeDetails();homeTab("Séries");}});navSeries.setContentDescription("Séries");navSeries.setGravity(Gravity.CENTER);try{Drawable series=getResources().getDrawable(R.drawable.top_series);series.setBounds(0,0,dp(60),dp(38));navSeries.setCompoundDrawables(series,null,null,null);navSeries.setCompoundDrawablePadding(0);}catch(Exception ignored){navSeries.setText("Séries");uiTextSize(navSeries,16);}menu.addView(navSeries,new LinearLayout.LayoutParams(dp(72),dp(58)));'
),
(
'navShorts=tvHeroNavAction("",()->{if(detailOpen)closeDetails();homeTab("Shorts");});navShorts.setContentDescription("GreenShorts");navShorts.setGravity(Gravity.CENTER);navShorts.setPadding(0,0,0,0);try{Drawable shorts=getResources().getDrawable(R.drawable.top_shorts);shorts.setBounds(0,0,dp(118),dp(39));navShorts.setCompoundDrawables(shorts,null,null,null);navShorts.setCompoundDrawablePadding(0);}catch(Exception ignored){navShorts.setText("GreenShorts");uiTextSize(navShorts,15);}menu.addView(navShorts,new LinearLayout.LayoutParams(dp(132),dp(58)));',
'navShorts=tvHeroNavAction("",()->{if(detailOpen)closeDetails();homeTab("Shorts");});navShorts.setContentDescription("GreenShorts");navShorts.setGravity(Gravity.CENTER);navShorts.setPadding(0,0,0,0);try{Drawable shorts=getResources().getDrawable(R.drawable.top_shorts);shorts.setBounds(0,0,dp(60),dp(38));navShorts.setCompoundDrawables(shorts,null,null,null);navShorts.setCompoundDrawablePadding(0);}catch(Exception ignored){navShorts.setText("GreenShorts");uiTextSize(navShorts,15);}menu.addView(navShorts,new LinearLayout.LayoutParams(dp(72),dp(58)));'
)
]
for old,new in pairs:
    assert old in s, old[:90]
    s=s.replace(old,new,1)

old='''  if(wideTvUi()){
   final TextView loading=t("Carregando mais conteúdo…",14);loading.setTextColor(0xff9da7a2);loading.setGravity(Gravity.CENTER);host.addView(loading,new LinearLayout.LayoutParams(-1,dp(56)));
   fetchYoutubeShortsPage(1,0,new JSONArray(),new java.util.HashSet<String>(),gen,host,loading);return;
  }
  JSONArray seed=readGreenShortsSeedCache();'''
new='''  if(wideTvUi()){
   JSONArray fullCache=readGreenShortsTvCache();boolean hadFullCache=fullCache.length()>0;JSONArray visible=hadFullCache?fullCache:readGreenShortsSeedCache();
   if(visible.length()>0)grid(visible);
   refreshTvGreenShortsInBackground(gen,host,hadFullCache,visible.length());return;
  }
  JSONArray seed=readGreenShortsSeedCache();'''
assert old in s
s=s.replace(old,new,1)

anchor=''' void saveGreenShortsSeedCache(JSONArray rows){if(rows==null||rows.length()==0)return;JSONArray out=new JSONArray();for(int i=0;i<Math.min(greenShortsPageSize(),rows.length());i++){JSONObject x=rows.optJSONObject(i);if(x!=null)out.put(x);}sp.edit().putString(greenShortsSeedKey(),out.toString()).apply();}
'''
extra=anchor+''' String greenShortsTvCacheKey(){return "greenshorts_tv_full_v52857";}
 JSONArray readGreenShortsTvCache(){try{String raw=sp.getString(greenShortsTvCacheKey(),"");return raw.isEmpty()?new JSONArray():new JSONArray(raw);}catch(Exception e){return new JSONArray();}}
 void saveGreenShortsTvCache(JSONArray rows){if(rows==null||rows.length()==0)return;JSONArray out=new JSONArray();for(int i=0;i<Math.min(1000,rows.length());i++){JSONObject x=rows.optJSONObject(i);if(x!=null)out.put(x);}sp.edit().putString(greenShortsTvCacheKey(),out.toString()).apply();}
 void refreshTvGreenShortsInBackground(final int gen,final LinearLayout host,final boolean hadFullCache,final int visibleCount){fetchTvGreenShortsPage(1,0,new JSONArray(),new java.util.HashSet<String>(),gen,host,hadFullCache,visibleCount,false);}
 void fetchTvGreenShortsPage(final int page,final int offset,final JSONArray acc,final java.util.HashSet<String> seen,final int gen,final LinearLayout host,final boolean hadFullCache,final int visibleCount,final boolean alreadyShown){
  if(!hostValid(gen,host)||!"Shorts".equals(activeHomeTab))return;Api.post("greenshorts",Api.m("user_id",uid,"page_no",String.valueOf(page),"page",String.valueOf(page),"offset",String.valueOf(offset),"limit","120","per_page","120"),new Api.CB(){public void ok(JSONObject j){
   if(!hostValid(gen,host)||!"Shorts".equals(activeHomeTab))return;JSONArray rows=j.optJSONArray("result");int added=0;if(rows!=null)for(int i=0;i<rows.length();i++){JSONObject x=rows.optJSONObject(i);if(x==null)continue;String y=x.optString("youtube_id","").trim();if(y.isEmpty())continue;if(seen.add("yt|"+y)){acc.put(x);added++;}}
   boolean shown=alreadyShown;if(!shown&&visibleCount==0&&acc.length()>0){JSONArray first=new JSONArray();for(int i=0;i<acc.length();i++){JSONObject x=acc.optJSONObject(i);if(x!=null)first.put(x);}grid(first);shown=true;}
   boolean more=j.optBoolean("more_page",false);if(more&&rows!=null&&rows.length()>0&&added>0){fetchTvGreenShortsPage(page+1,offset+rows.length(),acc,seen,gen,host,hadFullCache,visibleCount,shown);return;}
   if(acc.length()==0){if(visibleCount==0){TextView empty=t("Nenhum GreenShorts disponível no momento.",14);empty.setTextColor(0xff9da7a2);empty.setGravity(Gravity.CENTER);host.addView(empty,new LinearLayout.LayoutParams(-1,dp(72)));}return;}saveGreenShortsTvCache(acc);saveGreenShortsSeedCache(acc);if(!hadFullCache&&(visibleCount==0||acc.length()!=visibleCount)&&hostValid(gen,host)&&"Shorts".equals(activeHomeTab)){host.removeAllViews();grid(acc);}
  }public void err(String e){if(!hostValid(gen,host)||visibleCount>0)return;TextView empty=t("Não foi possível atualizar o GreenShorts.",14);empty.setTextColor(0xff9da7a2);empty.setGravity(Gravity.CENTER);host.addView(empty,new LinearLayout.LayoutParams(-1,dp(72)));}});
 }
'''
assert anchor in s
s=s.replace(anchor,extra,1)

old='void openYoutubeVideo(JSONObject source,String title,boolean restart){String id=youtubeVideoId(source);if(id.isEmpty()){Toast.makeText(this,"Vídeo indisponível.",Toast.LENGTH_SHORT).show();return;}if(restart)clearGreenShortResume(source);Intent in=new Intent(this,YouTubePlayerActivity.class);in.putExtra("youtube_id",id);in.putExtra("greenshorts_id",id);in.putExtra("title",title==null?"GreenShorts":title);in.putExtra("poster",detailValue(source,"thumbnail","portrait_img","poster","image"));int resume=restart?0:greenShortResumePosition(source);if(resume>0)in.putExtra("resume_ms",resume);startActivity(in);}'
new='void openYoutubeVideo(JSONObject source,String title,boolean restart){String id=youtubeVideoId(source);if(id.isEmpty()){Toast.makeText(this,"Vídeo indisponível.",Toast.LENGTH_SHORT).show();return;}if(restart)clearGreenShortResume(source);Intent in=new Intent(this,YouTubePlayerActivity.class);in.putExtra("youtube_id",id);in.putExtra("greenshorts_id",id);in.putExtra("title",title==null?"GreenShorts":title);in.putExtra("poster",detailValue(source,"thumbnail","portrait_img","poster","image"));in.putExtra("tv_mode",tvMode);int resume=restart?0:greenShortResumePosition(source);if(resume>0)in.putExtra("resume_ms",resume);startActivity(in);}'
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

yp=Path("work/app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java")
y=yp.read_text()
old='''        tvMode=DeviceCompat.isTelevisionDevice(this);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,WindowManager.LayoutParams.FLAG_FULLSCREEN);'''
new='''        tvMode=DeviceCompat.isTelevisionDevice(this)||getSharedPreferences("gp",0).getBoolean("force_tv_mode",false)||(getIntent()!=null&&getIntent().getBooleanExtra("tv_mode",false));
        try{setRequestedOrientation(tvMode?android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE:android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT);}catch(Exception ignored){}
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,WindowManager.LayoutParams.FLAG_FULLSCREEN);'''
assert old in y
y=y.replace(old,new,1)

old='''        int screenH=getResources().getDisplayMetrics().heightPixels;
        int topMaskH=Math.max(dp(48),Math.min(dp(82),(int)(screenH*0.09f)));
        int bottomMaskH=Math.max(dp(64),Math.min(dp(110),(int)(screenH*0.11f)));

        View topMask=new View(this);
        topMask.setBackgroundColor(Color.BLACK);
        FrameLayout.LayoutParams topMaskLp=new FrameLayout.LayoutParams(-1,topMaskH,Gravity.TOP);
        root.addView(topMask,topMaskLp);

        View bottomMask=new View(this);
        bottomMask.setBackgroundColor(Color.BLACK);
        FrameLayout.LayoutParams bottomMaskLp=new FrameLayout.LayoutParams(-1,bottomMaskH,Gravity.BOTTOM);
        root.addView(bottomMask,bottomMaskLp);'''
new='''        if(!tvMode){
            int screenH=getResources().getDisplayMetrics().heightPixels;
            int topMaskH=Math.max(dp(48),Math.min(dp(82),(int)(screenH*0.09f)));
            int bottomMaskH=Math.max(dp(64),Math.min(dp(110),(int)(screenH*0.11f)));
            View topMask=new View(this);topMask.setBackgroundColor(Color.BLACK);root.addView(topMask,new FrameLayout.LayoutParams(-1,topMaskH,Gravity.TOP));
            View bottomMask=new View(this);bottomMask.setBackgroundColor(Color.BLACK);root.addView(bottomMask,new FrameLayout.LayoutParams(-1,bottomMaskH,Gravity.BOTTOM));
        }'''
assert old in y
y=y.replace(old,new,1)
yp.write_text(y)
