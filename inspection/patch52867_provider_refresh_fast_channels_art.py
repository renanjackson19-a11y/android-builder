from pathlib import Path

g=Path("work/app/build.gradle")
s=g.read_text()
assert "versionCode 52866" in s
assert "versionName '5.28.66'" in s
s=s.replace("versionCode 52866","versionCode 52867",1).replace("versionName '5.28.66'","versionName '5.28.67'",1)
g.write_text(s)

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

# Fresh provider source of truth: never depend on the older general_setting snapshot.
old=''' void loadProviderChoices(final LinearLayout host,final TextView loading){
  if(host!=null)host.setTag("provider_loading");
  Api.post("general_setting",Api.m(),new Api.CB(){public void ok(JSONObject j){JSONArray cfg=j.optJSONArray("result");String raw="";if(cfg!=null){for(int i=0;i<cfg.length();i++){JSONObject x=cfg.optJSONObject(i);if(x!=null&&"greenplay_providers_json".equals(x.optString("key"))){raw=x.optString("value","");break;}}}try{final JSONArray configured=raw.isEmpty()?null:new JSONArray(raw);if(configured!=null&&configured.length()>0){
    Api.post("get_providers",Api.m("user_id",uid,"reseller_code",reseller),new Api.CB(){public void ok(JSONObject meta){JSONArray actual=meta.optJSONArray("result");host.removeAllViews();renderProviderChoices(host,mergeProviderCapabilities(configured,actual));}public void err(String e){host.removeAllViews();renderProviderChoices(host,configured);}});return;
   }}catch(Exception ignored){}loadProviderChoicesLegacy(host);}public void err(String e){loadProviderChoicesLegacy(host);}});
 }'''
new=''' void loadProviderChoices(final LinearLayout host,final TextView loading){
  if(host!=null)host.setTag("provider_loading");
  Api.post("get_providers",Api.m("user_id",uid,"reseller_code",reseller,"fresh","1"),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");host.removeAllViews();if(a==null||a.length()==0){providerChoiceError(host,"Nenhum servidor disponível.");return;}renderProviderChoices(host,a);}public void err(String e){loadProviderChoicesLegacy(host);}});
 }'''
assert old in s
s=s.replace(old,new,1)

# Unknown count must use capability flags immediately instead of hiding TV until a manual panel load.
old=''' int providerCount(JSONObject o,String kind){
  if(o==null)return -1;
  // Painel v131.1: 0 significa vazio confirmado; counts_ready=0 significa ainda não contado.
  if(o.has("counts_ready")&&o.optInt("counts_ready",1)==0)return -1;
  String sourceType=o.optString("source_type","").toLowerCase(java.util.Locale.ROOT);
  if(sourceType.startsWith("m3u")&&o.has("cache_ready")&&o.optInt("cache_ready",1)==0)return -1;
  if("movies".equals(kind)){if(o.has("movies_count"))return o.optInt("movies_count",-1);if(o.has("movies"))return o.optInt("movies",-1);}
  if("series".equals(kind)){if(o.has("series_count"))return o.optInt("series_count",-1);if(o.has("series"))return o.optInt("series",-1);}
  if("live".equals(kind)){
   if(o.has("channels_count"))return o.optInt("channels_count",-1);if(o.has("live_count"))return o.optInt("live_count",-1);if(o.has("channels"))return o.optInt("channels",-1);if(o.has("tv_count"))return o.optInt("tv_count",-1);
   if(o.has("has_live"))return o.optBoolean("has_live",false)?1:0;if(o.has("live_enabled"))return o.optBoolean("live_enabled",false)?1:0;if(o.has("supports_live"))return o.optBoolean("supports_live",false)?1:0;
  }
  return -1;
 }'''
new=''' int providerCount(JSONObject o,String kind){
  if(o==null)return -1;
  boolean ready=!o.has("counts_ready")||o.optInt("counts_ready",1)!=0;
  int v=-1;
  if("movies".equals(kind)){
   if(o.has("movies_count"))v=o.optInt("movies_count",-1);else if(o.has("movies"))v=o.optInt("movies",-1);
   if(v>=0)return v;
   if(o.optInt("has_movies",o.optBoolean("has_movies",false)?1:0)==1||o.optInt("app_movie",o.optBoolean("app_movie",false)?1:0)==1)return 1;
  }
  if("series".equals(kind)){
   if(o.has("series_count"))v=o.optInt("series_count",-1);else if(o.has("series"))v=o.optInt("series",-1);
   if(v>=0)return v;
   if(o.optInt("has_series",o.optBoolean("has_series",false)?1:0)==1||o.optInt("app_series",o.optBoolean("app_series",false)?1:0)==1)return 1;
  }
  if("live".equals(kind)){
   if(o.has("channels_count"))v=o.optInt("channels_count",-1);else if(o.has("live_count"))v=o.optInt("live_count",-1);else if(o.has("channels"))v=o.optInt("channels",-1);else if(o.has("tv_count"))v=o.optInt("tv_count",-1);
   if(v>=0)return v;
   if(o.optInt("has_live",o.optBoolean("has_live",false)?1:0)==1||o.optInt("app_live",o.optBoolean("app_live",false)?1:0)==1||o.optBoolean("live_enabled",false)||o.optBoolean("supports_live",false))return 1;
  }
  return ready?0:-1;
 }'''
assert old in s
s=s.replace(old,new,1)

old=''' void loadProvidersFromSettings(){Api.post("general_setting",Api.m(),new Api.CB(){public void ok(JSONObject j){JSONArray cfg=j.optJSONArray("result");String raw="";if(cfg!=null){for(int i=0;i<cfg.length();i++){JSONObject x=cfg.optJSONObject(i);if(x!=null&&"greenplay_providers_json".equals(x.optString("key"))){raw=x.optString("value","");break;}}}try{final JSONArray configured=raw.isEmpty()?null:new JSONArray(raw);if(configured!=null&&configured.length()>0){Api.post("get_providers",Api.m("user_id",uid,"reseller_code",reseller),new Api.CB(){public void ok(JSONObject meta){JSONArray actual=meta.optJSONArray("result");JSONArray merged=mergeProviderCapabilities(configured,actual);for(int i=0;i<merged.length();i++){JSONObject o=merged.optJSONObject(i);if(o!=null)providerCard(o);}}public void err(String e){for(int i=0;i<configured.length();i++){JSONObject o=configured.optJSONObject(i);if(o!=null)providerCard(o);}}});return;}}catch(Exception ignored){}loadProvidersLegacy();}public void err(String z){loadProvidersLegacy();}});}'''
new=''' void loadProvidersFromSettings(){loadProvidersLegacy();}'''
assert old in s
s=s.replace(old,new,1)

# Preserve valid source/TMDB art. The server now decides the best fallback.
old=''' void stripUnverifiedCatalogArt(JSONObject rootJson){
  try{JSONArray sections=rootJson==null?null:rootJson.optJSONArray("result");if(sections==null)return;for(int i=0;i<sections.length();i++){JSONObject sec=sections.optJSONObject(i);if(sec==null)continue;int vt=sec.optInt("type_id",sec.optInt("video_type",1));if(vt!=1&&vt!=2)continue;JSONArray data=sec.optJSONArray("data");if(data==null)continue;for(int k=0;k<data.length()&&k<24;k++){JSONObject x=data.optJSONObject(k);if(x==null)continue;if(x.optInt("tmdb_id",0)>0)continue;String[] art={"thumbnail","portrait_img","image","landscape","landscape_img","poster","backdrop","cover"};for(String key:art)x.put(key,"");}}}catch(Exception ignored){}
 }'''
new=''' void stripUnverifiedCatalogArt(JSONObject rootJson){/* 5.28.67: preserva arte válida da fonte/cache; fallback é decidido no servidor. */}'''
assert old in s
s=s.replace(old,new,1)

# Progressive channel loading: render first page immediately, append the rest.
old=''' void tvLoadChannelsDirect(String categoryId,String search,boolean retryAll,int listGen){
  if(listGen!=tvChannelListGeneration)return;final String providerAtRequest=Api.PROVIDER==null?"":Api.PROVIDER;String cat=categoryId==null?"":categoryId;String q=search==null?"":search;
  fetchAllLiveChannelPages(cat,q,false,0,new JSONArray(),new java.util.HashSet<String>(),new AllPagesCB(){public void ok(JSONArray a){if(listGen!=tvChannelListGeneration||tvChannelHost==null||!providerAtRequest.equals(Api.PROVIDER==null?"":Api.PROVIDER))return;if(a!=null&&a.length()>0){tvRenderLiveResult(providerAtRequest,a,listGen);return;}tvLoadChannelsTypedFallback(cat,q,retryAll,providerAtRequest,listGen);}public void err(String x){if(listGen!=tvChannelListGeneration||tvChannelHost==null||!providerAtRequest.equals(Api.PROVIDER==null?"":Api.PROVIDER))return;tvLoadChannelsTypedFallback(cat,q,retryAll,providerAtRequest,listGen);}});
 }'''
new=''' void tvLoadChannelsDirect(String categoryId,String search,boolean retryAll,int listGen){
  if(listGen!=tvChannelListGeneration)return;final String providerAtRequest=Api.PROVIDER==null?"":Api.PROVIDER;String cat=categoryId==null?"":categoryId;String q=search==null?"":search;
  fetchLiveChannelPagesProgressive(cat,q,false,0,new JSONArray(),new java.util.HashSet<String>(),providerAtRequest,listGen,retryAll);
 }
 void fetchLiveChannelPagesProgressive(String cat,String q,boolean typed,int offset,JSONArray acc,java.util.HashSet<String> seen,String providerAtRequest,int listGen,boolean retryAll){
  if(listGen!=tvChannelListGeneration||tvChannelHost==null||!providerAtRequest.equals(Api.PROVIDER==null?"":Api.PROVIDER))return;
  final int pageSize=100;java.util.Map<String,String> args=Api.m("user_id",uid,"category_id",cat,"limit",String.valueOf(pageSize),"offset",String.valueOf(offset),"search",q);if(typed)args.put("type","live");
  Api.post("get_channel",args,new Api.CB(){public void ok(JSONObject j){
   if(listGen!=tvChannelListGeneration||tvChannelHost==null||!providerAtRequest.equals(Api.PROVIDER==null?"":Api.PROVIDER))return;
   if(j.optInt("status",200)!=200){if(acc.length()==0){if(!typed)tvLoadChannelsTypedFallback(cat,q,retryAll,providerAtRequest,listGen);else tvShowNoLiveResult(q,providerAtRequest,listGen);}return;}
   JSONArray rows=j.optJSONArray("result");if(rows==null||rows.length()==0){if(acc.length()==0){if(!typed)tvLoadChannelsTypedFallback(cat,q,retryAll,providerAtRequest,listGen);else tvShowNoLiveResult(q,providerAtRequest,listGen);}return;}
   int before=acc.length();for(int i=0;i<rows.length();i++){JSONObject x=rows.optJSONObject(i);if(!isRealLiveChannel(x))continue;String key=tvChannelKey(x);if(key==null||key.trim().isEmpty())key=x.optString("stream_url",x.optString("url",""))+"|"+tvChannelName(x);if(seen.add(key))acc.put(x);}
   if(acc.length()>before){
    if(before==0)tvRenderLiveResult(providerAtRequest,acc,listGen);
    else{JSONArray clean=sanitizeLiveChannels(acc);int rendered=tvCurrentChannels==null?0:tvCurrentChannels.length();tvCurrentChannels=clean;if(clean.length()>rendered)renderTvChannelsChunk(tvChannelHost,clean,rendered,listGen);}
   }
   boolean more=j.has("has_more")?j.optBoolean("has_more",false):rows.length()>=pageSize;int next=j.optInt("next_offset",offset+rows.length());if(more&&next>offset){tvChannelHost.postDelayed(()->fetchLiveChannelPagesProgressive(cat,q,typed,next,acc,seen,providerAtRequest,listGen,retryAll),8);return;}
   if(acc.length()==0){if(!typed)tvLoadChannelsTypedFallback(cat,q,retryAll,providerAtRequest,listGen);else tvShowNoLiveResult(q,providerAtRequest,listGen);}
  }public void err(String e){if(acc.length()==0){if(!typed)tvLoadChannelsTypedFallback(cat,q,retryAll,providerAtRequest,listGen);else tvShowNoLiveResult(q,providerAtRequest,listGen);}}});
 }'''
assert old in s
s=s.replace(old,new,1)

# Typed fallback uses the same progressive path.
old=''' void tvLoadChannelsTypedFallback(String cat,String q,boolean retryAll,String providerAtRequest,int listGen){
  if(listGen!=tvChannelListGeneration)return;fetchAllLiveChannelPages(cat,q,true,0,new JSONArray(),new java.util.HashSet<String>(),new AllPagesCB(){public void ok(JSONArray a){if(listGen!=tvChannelListGeneration||tvChannelHost==null||!providerAtRequest.equals(Api.PROVIDER==null?"":Api.PROVIDER))return;if(a!=null&&a.length()>0){tvRenderLiveResult(providerAtRequest,a,listGen);return;}if(retryAll){tvSelectedCategory="";tvLoadChannelsDirect("",q,false,listGen);return;}tvShowNoLiveResult(q,providerAtRequest,listGen);}public void err(String x){if(listGen!=tvChannelListGeneration||tvChannelHost==null||!providerAtRequest.equals(Api.PROVIDER==null?"":Api.PROVIDER))return;if(retryAll){tvSelectedCategory="";tvLoadChannelsDirect("",q,false,listGen);return;}tvShowNoLiveResult(q,providerAtRequest,listGen);}});
 }'''
new=''' void tvLoadChannelsTypedFallback(String cat,String q,boolean retryAll,String providerAtRequest,int listGen){
  if(listGen!=tvChannelListGeneration)return;fetchLiveChannelPagesProgressive(cat,q,true,0,new JSONArray(),new java.util.HashSet<String>(),providerAtRequest,listGen,retryAll);
 }'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

# Disable HTTP caching for dynamic API calls.
p=Path("work/app/src/main/java/fun/greenplay/app/Api.java")
s=p.read_text()
old='''c=(HttpURLConnection)u.openConnection();c.setRequestMethod("POST");c.setConnectTimeout(12000);'''
new='''c=(HttpURLConnection)u.openConnection();c.setUseCaches(false);c.setDefaultUseCaches(false);c.setRequestProperty("Cache-Control","no-cache, no-store");c.setRequestProperty("Pragma","no-cache");c.setRequestMethod("POST");c.setConnectTimeout(12000);'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)
