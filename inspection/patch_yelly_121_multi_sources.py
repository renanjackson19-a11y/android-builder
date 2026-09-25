from pathlib import Path

root=Path("work")
app=root/"app/src/main/java/fun/greenplay/app"

# Add the direct multi-source client.
(app/"ExternalDoramas.java").write_text(Path("inspection/ExternalDoramas.java").read_text(encoding="utf-8"),encoding="utf-8")

p=app/"StoriesActivity.java"
s=p.read_text(encoding="utf-8")
s=s.replace('void fetchCatalog(){fetchGreenShortsPage();}','void fetchCatalog(){fetchGreenShortsPage();fetchExternalSources();}',1)
s=s.replace('    void fetchCategoryWave(){fetchGreenShortsPage();}\n','''    void fetchCategoryWave(){fetchGreenShortsPage();}

    void fetchExternalSources(){
        ExternalDoramas.fetchAll(new ExternalDoramas.CB(){
            public void ok(JSONArray a){int before=items.length();appendExternal(a);if(before==0&&items.length()>0){shuffleArray(items);index=0;show(0);}}
            public void err(String e){}
        });
    }

    void appendExternal(JSONArray a){if(a==null)return;for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;String p=x.optString("provider_source","");String id=x.optString("external_id",x.optString("id",x.optString("name","")));String k="ext|"+p+"|"+id;if(seen.add(k))items.put(x);}}
''',1)

old='''    void resolveItem(JSONObject x,int token,boolean forFull){
        String direct=playUrl(x);if(!direct.isEmpty()){currentResolved=x;if(forFull)launchFull(x);else startPreview(x,token);return;}
        String q=x.optString("original_title",x.optString("name",x.optString("title",""))).trim();'''
new='''    void resolveItem(JSONObject x,int token,boolean forFull){
        String direct=playUrl(x);if(!direct.isEmpty()){currentResolved=x;if(forFull)launchFull(x);else startPreview(x,token);return;}
        if("external".equalsIgnoreCase(x.optString("source",""))||!x.optString("provider_source","").isEmpty()){
            ExternalDoramas.resolve(x,new ExternalDoramas.CB(){
                public void ok(JSONArray a){if(token!=storyToken&&!forFull)return;JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;JSONObject merged=mergeJson(x,d);currentResolved=merged;if(playUrl(merged).isEmpty()){if(forFull)Toast.makeText(StoriesActivity.this,"Fonte sem vídeo direto disponível.",Toast.LENGTH_SHORT).show();else advanceUnavailable();return;}if(forFull)launchFull(merged);else startPreview(merged,token);}
                public void err(String e){if(forFull)Toast.makeText(StoriesActivity.this,"Fonte indisponível agora.",Toast.LENGTH_SHORT).show();else advanceUnavailable();}
            });return;
        }
        String q=x.optString("original_title",x.optString("name",x.optString("title",""))).trim();'''
if old not in s: raise SystemExit("Stories resolve anchor missing")
s=s.replace(old,new,1)

old='String playUrl(JSONObject x){String u=val(x,"video_1080","video_720","video_480","video_320","video_url","stream_url","url");if(!u.isEmpty())return u;return "android.resource://"+getPackageName()+"/"+R.raw.yelly_demo;}'
new='String playUrl(JSONObject x){String u=val(x,"video_1080","video_720","video_480","video_320","video_url","stream_url","url");if(!u.isEmpty())return u;if(x!=null&&("external".equalsIgnoreCase(x.optString("source",""))||!x.optString("provider_source","").isEmpty()))return "";return "android.resource://"+getPackageName()+"/"+R.raw.yelly_demo;}'
if old not in s: raise SystemExit("Stories playUrl anchor missing")
s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")

p=app/"MainActivity.java"
m=p.read_text(encoding="utf-8")
old='if(rows.length()>0){saveGreenShortsSeedCache(rows);prefetchGreenShortDetails(rows,24);featureCarousel(rows);}grid(rows);startGreenShortsPaging(rows,gen);'
new='if(rows.length()>0){saveGreenShortsSeedCache(rows);prefetchGreenShortDetails(rows,24);featureCarousel(rows);}grid(rows);startGreenShortsPaging(rows,gen);loadExternalDoramasHome(gen);'
if old not in m: raise SystemExit("home success anchor missing")
m=m.replace(old,new,1)
old='grid(new JSONArray());startGreenShortsPaging(new JSONArray(),gen);}});'
new='grid(new JSONArray());startGreenShortsPaging(new JSONArray(),gen);loadExternalDoramasHome(gen);}});'
if old not in m: raise SystemExit("home error anchor missing")
m=m.replace(old,new,1)

anchor=' int greenShortsPageSize(){return 60;}'
helper=''' void loadExternalDoramasHome(final int gen){
  ExternalDoramas.fetchAll(new ExternalDoramas.CB(){public void ok(JSONArray ext){if(gen!=viewGen||ext==null||ext.length()==0)return;if(wideTvUi()){if(tvShortsGrid!=null&&tvShortsGridGen==gen&&tvShortsCardW>0)addGridChunk(tvShortsGrid,ext,0,tvShortsCardW,gen);else grid(ext);return;}if(mobileCategoryRows==null)mobileCategoryRows=new JSONArray();java.util.HashSet<String> known=new java.util.HashSet<>();for(int i=0;i<mobileCategoryRows.length();i++){JSONObject q=mobileCategoryRows.optJSONObject(i);if(q!=null)known.add(itemKey(q));}for(int i=0;i<ext.length();i++){JSONObject x=ext.optJSONObject(i);if(x==null)continue;String k=itemKey(x);if(k==null||k.isEmpty())k=x.optString("provider_source","")+"|"+x.optString("external_id",x.optString("id",""));if(known.add(k)){mobileCategoryRows.put(x);mobileCategorySeen.add(k);}}maybeLoadMoreMobileCategory(true);}public void err(String e){}});
 }
'''+anchor
if anchor not in m: raise SystemExit("home helper anchor missing")
m=m.replace(anchor,helper,1)

old='boolean isYoutubeShort(JSONObject x){return x!=null&&(!x.optString("youtube_id","").trim().isEmpty()||"youtube".equalsIgnoreCase(x.optString("source","")));}'
new='boolean isYoutubeShort(JSONObject x){return x!=null&&(!x.optString("youtube_id","").trim().isEmpty()||"youtube".equalsIgnoreCase(x.optString("source",""))||"external".equalsIgnoreCase(x.optString("source",""))||!x.optString("provider_source","").trim().isEmpty());}'
if old not in m: raise SystemExit("isYoutubeShort anchor missing")
m=m.replace(old,new,1)

old='void openYoutubeVideo(JSONObject source,String title,boolean restart){if(source==null)return;String u=detailPlayUrl(source);if(u.isEmpty())u="android.resource://"+getPackageName()+"/"+R.raw.yelly_demo;openPlayableUrl(source,title==null?"Yelly Doramas":title,false,u);}'
new='''void openYoutubeVideo(JSONObject source,String title,boolean restart){if(source==null)return;String u=detailPlayUrl(source);boolean external="external".equalsIgnoreCase(source.optString("source",""))||!source.optString("provider_source","").trim().isEmpty();if(!u.isEmpty()){openPlayableUrl(source,title==null?"Yelly Doramas":title,false,u);return;}if(external){ExternalDoramas.resolve(source,new ExternalDoramas.CB(){public void ok(JSONArray a){JSONObject r=(a!=null&&a.length()>0)?a.optJSONObject(0):null;String ru=detailPlayUrl(r);if(ru.isEmpty()){runOnUiThread(()->Toast.makeText(MainActivity.this,"Fonte sem vídeo direto disponível.",Toast.LENGTH_SHORT).show());return;}runOnUiThread(()->openPlayableUrl(r,title==null?"Yelly Doramas":title,false,ru));}public void err(String e){runOnUiThread(()->Toast.makeText(MainActivity.this,"Fonte indisponível agora.",Toast.LENGTH_SHORT).show());}});return;}u="android.resource://"+getPackageName()+"/"+R.raw.yelly_demo;openPlayableUrl(source,title==null?"Yelly Doramas":title,false,u);}'''
if old not in m: raise SystemExit("external playback anchor missing")
m=m.replace(old,new,1)
p.write_text(m,encoding="utf-8")

p=root/"app/build.gradle"
g=p.read_text(encoding="utf-8")
if "versionCode 10020" not in g or "versionName '1.0.20'" not in g: raise SystemExit("wrong base")
g=g.replace("versionCode 10020","versionCode 10021",1)
g=g.replace("versionName '1.0.20'","versionName '1.0.21'",1)
p.write_text(g,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.21
- Junta o catálogo atual do Yelly com fontes externas detectadas nos APKs enviados.
- DramaTall e DramaHub são consultados sem token; somente respostas públicas válidas entram.
- Catálogo externo é mesclado na Home Doramas e nos Stories, com remoção de duplicados.
- URLs MP4/HLS encontradas são abertas no player nativo Media3/ExoPlayer do Yelly.
- Para itens externos sem stream na listagem, o app tenta buscar detalhe/episódios antes de reproduzir.
- Fontes que exigirem autenticação ou não responderem são ignoradas sem quebrar o restante do app.
- StoryReel permanece fora da integração automática porque os links observados usam assinatura temporária.
""",encoding="utf-8")
print("YELLY_121_MULTI_SOURCE_OK")
