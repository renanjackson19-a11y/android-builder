from pathlib import Path

root=Path('work')
main=root/'app/src/main/java/fun/greenplay/app/MainActivity.java'
stories=root/'app/src/main/java/fun/greenplay/app/StoriesActivity.java'
grad=root/'app/build.gradle'
s=main.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 got {n}')
    s=s.replace(old,new,1)

one('void loadGreenShortsCover(ImageView im,JSONObject x){if(im==null)return;im.setImageResource(R.drawable.greenshorts_fallback);if(x==null)return;Img.loadBest(im,greenShortsCoverCandidate(x.optString("thumbnail","")),greenShortsCoverCandidate(x.optString("portrait_img","")),greenShortsCoverCandidate(x.optString("image","")),greenShortsCoverCandidate(x.optString("poster","")),greenShortsCoverCandidate(x.optString("landscape","")),greenShortsCoverCandidate(x.optString("landscape_img","")),greenShortsCoverCandidate(x.optString("backdrop","")));}',
'''void loadGreenShortsCover(ImageView im,JSONObject x){if(im==null)return;im.setScaleType(ImageView.ScaleType.FIT_CENTER);im.setBackgroundColor(0xff090609);im.setImageResource(R.drawable.greenshorts_fallback);if(x==null)return;Img.loadBest(im,greenShortsCoverCandidate(x.optString("thumbnail","")),greenShortsCoverCandidate(x.optString("portrait_img","")),greenShortsCoverCandidate(x.optString("image","")),greenShortsCoverCandidate(x.optString("poster","")),greenShortsCoverCandidate(x.optString("landscape","")),greenShortsCoverCandidate(x.optString("landscape_img","")),greenShortsCoverCandidate(x.optString("backdrop","")));}''','shorts cover fit')

one('boolean detailNeedsEnrich(JSONObject d){if(d==null)return true;if(isYoutubeShort(d))return false;String desc=detailValue(d,"description","plot","overview"),genre=detailValue(d,"category_name","genre","genres"),rating=detailValue(d,"imdb_rating","rating","vote_average","score"),back=detailValue(d,"landscape","landscape_img","backdrop","backdrop_path");JSONArray cast=d.optJSONArray("cast_list");int vt=d.optInt("video_type",d.optInt("type_id",1));boolean series=vt==2||"series".equalsIgnoreCase(d.optString("type",""));if(series&&detailSeriesSeasons(d).length()==0)return true;return desc.isEmpty()||genre.isEmpty()||rating.isEmpty()||back.isEmpty()||cast==null||cast.length()==0;}',
'boolean detailNeedsEnrich(JSONObject d){if(d==null)return true;if(isYoutubeShort(d)){String desc=detailValue(d,"description","plot","overview");return d.optInt("tmdb_enriched",0)!=1||desc.trim().isEmpty();}String desc=detailValue(d,"description","plot","overview"),genre=detailValue(d,"category_name","genre","genres"),rating=detailValue(d,"imdb_rating","rating","vote_average","score"),back=detailValue(d,"landscape","landscape_img","backdrop","backdrop_path");JSONArray cast=d.optJSONArray("cast_list");int vt=d.optInt("video_type",d.optInt("type_id",1));boolean series=vt==2||"series".equalsIgnoreCase(d.optString("type",""));if(series&&detailSeriesSeasons(d).length()==0)return true;return desc.isEmpty()||genre.isEmpty()||rating.isEmpty()||back.isEmpty()||cast==null||cast.length()==0;}','short synopsis state')

needle=' void prepareDetailForOpen(JSONObject source,DetailPrepareCB cb){\n'
helper=''' java.util.Map<String,String> doramaEnrichArgs(JSONObject source){if(source==null)return Api.m();String q=source.optString("original_title",source.optString("name",source.optString("title","")));return Api.m("title",q,"display_name",source.optString("name",source.optString("title","")),"thumbnail",source.optString("thumbnail",source.optString("portrait_img","")),"landscape",source.optString("landscape",source.optString("backdrop","")),"series_key",source.optString("series_key",""),"category_name",source.optString("category_name","Yelly Doramas"));}
 void prefetchGreenShortDetails(JSONArray rows,int limit){if(rows==null)return;for(int i=0;i<Math.min(limit,rows.length());i++){JSONObject x=rows.optJSONObject(i);if(x!=null&&isYoutubeShort(x))queueDetailPrefetch(x);}pumpDetailPrefetch();}
'''
if needle not in s: raise SystemExit('prepare helper anchor missing')
s=s.replace(needle,helper+needle,1)

one('''  h.postDelayed(deliver,3200);
  int vt=source.optInt("video_type",source.optInt("type_id",1));String vid=source.optString("id",source.optString("video_id",""));
  Api.post("content_detail",Api.m("user_id",uid,"video_id",vid,"video_type",String.valueOf(vt)),new Api.CB(){
''',
'''  h.postDelayed(deliver,isYoutubeShort(source)?5200:3200);
  if(isYoutubeShort(source)){Api.post("dorama_enrich",doramaEnrichArgs(source),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d!=null)saveDetailCache(source,d);h.removeCallbacks(deliver);deliver.run();}public void err(String e){h.removeCallbacks(deliver);deliver.run();}});return;}
  int vt=source.optInt("video_type",source.optInt("type_id",1));String vid=source.optString("id",source.optString("video_id",""));
  Api.post("content_detail",Api.m("user_id",uid,"video_id",vid,"video_type",String.valueOf(vt)),new Api.CB(){
''','prepare synopsis before detail')

one('''   JSONObject x=detailPrefetchQueue.poll();if(x==null)continue;String key=detailCacheKey(x);detailPrefetchActive++;
   Api.post("content_detail",Api.m("user_id",uid,"video_id",x.optString("id"),"video_type",x.optString("video_type",x.optString("type_id","1"))),new Api.CB(){
    public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d!=null)saveDetailCache(x,d);finishDetailPrefetch(key);}
    public void err(String e){finishDetailPrefetch(key);}
   });
''',
'''   JSONObject x=detailPrefetchQueue.poll();if(x==null)continue;String key=detailCacheKey(x);detailPrefetchActive++;
   String ep=isYoutubeShort(x)?"dorama_enrich":"content_detail";java.util.Map<String,String> args=isYoutubeShort(x)?doramaEnrichArgs(x):Api.m("user_id",uid,"video_id",x.optString("id"),"video_type",x.optString("video_type",x.optString("type_id","1")));
   Api.post(ep,args,new Api.CB(){
    public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d!=null)saveDetailCache(x,d);finishDetailPrefetch(key);}
    public void err(String e){finishDetailPrefetch(key);}
   });
''','prefetch dorama metadata')

one('if(seed.length()>0){featureCarousel(seed);grid(seed);startGreenShortsPaging(seed,gen);return;}',
    'if(seed.length()>0){prefetchGreenShortDetails(seed,24);featureCarousel(seed);grid(seed);startGreenShortsPaging(seed,gen);return;}','seed metadata prefetch')

one('if(rows.length()>0){saveGreenShortsSeedCache(rows);featureCarousel(rows);}grid(rows);startGreenShortsPaging(rows,gen);',
    'if(rows.length()>0){saveGreenShortsSeedCache(rows);prefetchGreenShortDetails(rows,24);featureCarousel(rows);}grid(rows);startGreenShortsPaging(rows,gen);','network metadata prefetch')

poster_old='if("Shorts".equals(activeHomeTab))im.setImageResource(R.drawable.top_shorts);Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("landscape",""),x.optString("landscape_img",""));'
poster_new='if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,x);else Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("landscape",""),x.optString("landscape_img",""));'
if poster_old in s:s=s.replace(poster_old,poster_new,1)

main.write_text(s,encoding='utf-8')

st=stories.read_text(encoding='utf-8')
old='public void err(String e){loading=false;title.setText("Não foi possível carregar os Stories.");}});}'
new='public void err(String e){loading=false;if(page<=1&&loadSeedFallback())return;title.setText("Não foi possível carregar os Stories.");}});}'
if st.count(old)!=1:raise SystemExit('stories err anchor missing')
st=st.replace(old,new,1)
anchor=' String cleanTitle(String s){'
helper=''' boolean loadSeedFallback(){try{String raw=sp.getString("greenshorts_seed_v52852","");if(raw.trim().isEmpty())return false;JSONArray a=new JSONArray(raw);if(a.length()==0)return false;items=new JSONArray();for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x!=null&&!x.optString("youtube_id","").trim().isEmpty())items.put(x);}more=true;page=2;if(items.length()>0){show(0);return true;}}catch(Exception ignored){}return false;}
'''
if anchor not in st:raise SystemExit('stories fallback anchor missing')
st=st.replace(anchor,helper+anchor,1)
stories.write_text(st,encoding='utf-8')

g=grad.read_text(encoding='utf-8').replace('versionCode 10004','versionCode 10005').replace("versionName '1.0.4'","versionName '1.0.5'")
grad.write_text(g,encoding='utf-8')

(root/'app/RELEASE_NOTES.txt').write_text('''Yelly Doramas 1.0.5
Stories corrigidos para respostas do catálogo com caracteres inválidos e fallback no catálogo salvo.
Capas dos Doramas mantêm a arte original inteira, centralizada e sem esticar/cortar.
Títulos, sinopses e metadados dos primeiros Doramas são pré-carregados em segundo plano.
Ao abrir um Dorama, o app aguarda o enriquecimento da sinopse antes de mostrar a tela de detalhes.
''',encoding='utf-8')
print('YELLY_105_PATCH_OK')
