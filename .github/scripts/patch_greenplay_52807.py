#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit("uso: patch_greenplay_52807.py MainActivity.java app/build.gradle")

main = Path(sys.argv[1])
gradle = Path(sys.argv[2])
s = main.read_text(encoding="utf-8")

def method_bounds(src, marker):
    start = src.find(marker)
    if start < 0:
        raise SystemExit("metodo nao encontrado: " + marker)
    op = src.find("{", start)
    if op < 0:
        raise SystemExit("abertura nao encontrada: " + marker)
    depth = 0
    i = op
    state = "code"
    while i < len(src):
        ch = src[i]
        nx = src[i + 1] if i + 1 < len(src) else ""
        if state == "code":
            if ch == '"':
                state = "double"
            elif ch == "'":
                state = "single"
            elif ch == "/" and nx == "/":
                state = "line"
                i += 1
            elif ch == "/" and nx == "*":
                state = "block"
                i += 1
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return start, i + 1
        elif state == "double":
            if ch == "\\":
                i += 1
            elif ch == '"':
                state = "code"
        elif state == "single":
            if ch == "\\":
                i += 1
            elif ch == "'":
                state = "code"
        elif state == "line":
            if ch == "\n":
                state = "code"
        elif state == "block":
            if ch == "*" and nx == "/":
                state = "code"
                i += 1
        i += 1
    raise SystemExit("fim nao encontrado: " + marker)

def replace_method(src, marker, replacement):
    a, b = method_bounds(src, marker)
    return src[:a] + replacement.rstrip() + src[b:]

old_boot = "prepareCriticalDetails(snapshot,()->warmHomeImages(snapshot,catalogReady));"
if old_boot not in s:
    raise SystemExit("bootstrap prepareCriticalDetails nao encontrado")
s = s.replace(old_boot, "warmHomeImages(snapshot,catalogReady);", 1)

s = replace_method(s, "void scheduleCatalogRefreshIfNeeded(){", r'''
void scheduleCatalogRefreshIfNeeded(){
  if(!shouldRefreshCatalogInBackground())return;
  new Handler(Looper.getMainLooper()).postDelayed(()->{
   if(isFinishing()||Api.PROVIDER==null||Api.PROVIDER.trim().isEmpty())return;
   fetchProviderSnapshot(sp.getInt("provider_movies_count",-1),sp.getInt("provider_series_count",-1),new PreparedHomeCB(){public void ok(JSONObject fresh){
    if(fresh==null)return;
    saveHomeCache(fresh);persistHomeCacheAsync(fresh);markPersistentHomeUsed();
    if(!isFinishing()&&currentNavIndex==0&&!detailOpen&&homeViewAvailable){
     int y=mainScroll==null?0:mainScroll.getScrollY();
     home();
     if(mainScroll!=null&&y>0)mainScroll.post(()->mainScroll.scrollTo(0,y));
    }
   }public void err(String e){}});
  },1500);
 }''')

s = replace_method(s, "void prepareHomeThenShell(TextView msg,Button action){", r'''
void prepareHomeThenShell(TextView msg,Button action){
  if(msg!=null){msg.setTextColor(0xffa8b8b0);msg.setText("Preparando seu catálogo…");}
  fetchPreparedHome(-1,-1,new PreparedHomeCB(){public void ok(JSONObject j){
   JSONArray a=j.optJSONArray("result");
   if(a!=null&&a.length()>0){
    saveHomeCache(j);sp.edit().putBoolean(homeExtrasKey(),false).apply();homeExtrasStarted=false;
    warmHomeImages(j,()->{saveHomeCache(j);shell();prefetchDetailsFromCatalog(j,24);});
   }else shell();
  }public void err(String e){shell();}});
 }''')

s = replace_method(s, "void prepareCriticalDetails(JSONObject rootJson,Runnable done){", r'''
void prepareCriticalDetails(JSONObject rootJson,Runnable done){
  if(rootJson!=null)saveHomeCache(rootJson);
  if(done!=null)done.run();
 }''')

s = replace_method(s, "void pumpDetailPrefetch(){", r'''
void pumpDetailPrefetch(){
  while(detailPrefetchActive<3&&!detailPrefetchQueue.isEmpty()){
   JSONObject x=detailPrefetchQueue.poll();if(x==null)continue;
   String key=detailCacheKey(x);detailPrefetchActive++;
   String vid=x.optString("id",x.optString("video_id",""));
   String vt=x.optString("video_type",x.optString("type_id","1"));
   Api.post("content_detail",Api.m("user_id",uid,"video_id",vid,"video_type",vt),new Api.CB(){
    public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d!=null)saveDetailCache(x,d);finishDetailPrefetch(key);}
    public void err(String e){finishDetailPrefetch(key);}
   });
  }
 }''')

s = replace_method(s, "void ensureTmdbCardArtwork(JSONObject source,ImageView im,TextView label){", r'''
void ensureTmdbCardArtwork(JSONObject source,ImageView im,TextView label){
  if(source==null||im==null)return;
  JSONObject merged=mergeDetailJson(source,readDetailCache(source));if(merged==null)merged=source;
  String poster=detailValue(merged,"thumbnail","portrait_img","image","poster","cover","stream_icon");
  String land=detailValue(merged,"landscape","landscape_img","backdrop","backdrop_path");
  if(poster.isEmpty()&&land.isEmpty())return;
  Img.loadBest(im,
   merged.optString("thumbnail",""),merged.optString("portrait_img",""),merged.optString("image",""),
   merged.optString("poster",""),merged.optString("cover",""),merged.optString("stream_icon",""),
   merged.optString("landscape",""),merged.optString("landscape_img",""),merged.optString("backdrop",""),merged.optString("backdrop_path",""));
  if(label!=null)label.setText(merged.optString("name",merged.optString("title",source.optString("name",source.optString("title","")))));
 }''')

s = replace_method(s, "void prepareDetailForOpen(JSONObject source,DetailPrepareCB cb){", r'''
void prepareDetailForOpen(JSONObject source,DetailPrepareCB cb){
  saveDetailCache(source,source);
  JSONObject first=mergeDetailJson(source,readDetailCache(source));
  if(first!=null&&!detailNeedsEnrich(first)){cb.done(first);return;}
  final boolean[] delivered={false};final Handler h=new Handler(Looper.getMainLooper());
  final Runnable deliver=()->{if(delivered[0])return;delivered[0]=true;JSONObject ready=mergeDetailJson(source,readDetailCache(source));cb.done(ready==null?source:ready);};
  h.postDelayed(deliver,2600);
  int vt=source.optInt("video_type",source.optInt("type_id",1));String vid=source.optString("id",source.optString("video_id",""));
  Api.post("content_detail",Api.m("user_id",uid,"video_id",vid,"video_type",String.valueOf(vt)),new Api.CB(){
   public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d!=null)saveDetailCache(source,d);h.removeCallbacks(deliver);deliver.run();}
   public void err(String e){h.removeCallbacks(deliver);deliver.run();}
  });
 }''')

s = replace_method(s, "void requestDetailEnrich(JSONObject source,TextView hn,ImageView heroImage,TextView heart,String fallbackTitle,LinearLayout detailHost,int gen){", r'''
void requestDetailEnrich(JSONObject source,TextView hn,ImageView heroImage,TextView heart,String fallbackTitle,LinearLayout detailHost,int gen){
  JSONObject cur=readDetailCache(source);if(!detailNeedsEnrich(cur))return;
  int vt=source.optInt("video_type",source.optInt("type_id",1));
  if(vt==2&&(cur==null||detailSeriesSeasons(cur).length()==0))return;
  Api.post("content_detail",Api.m("user_id",uid,"video_id",source.optString("id",source.optString("video_id","")),"video_type",String.valueOf(vt)),new Api.CB(){
   public void ok(JSONObject j){if(gen!=viewGen||!detailOpen)return;JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d==null)return;saveDetailCache(source,d);JSONObject merged=readDetailCache(source);if(merged==null)return;int y=mainScroll==null?0:mainScroll.getScrollY();detailHost.removeAllViews();renderDetailContent(detailHost,source,merged,hn,heroImage,heart,fallbackTitle,false);if(mainScroll!=null&&y>0)mainScroll.post(()->mainScroll.scrollTo(0,y));}
   public void err(String e){}
  });
 }''')

s = replace_method(s, "boolean cardHasTmdbArt(JSONObject x){", r'''
boolean cardHasTmdbArt(JSONObject x){
  if(x==null)return false;
  return !detailValue(x,"thumbnail","portrait_img","image","poster","cover","stream_icon","landscape","landscape_img","backdrop").isEmpty();
 }''')

replacements = {
    'Img.loadCatalogBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("landscape",""),x.optString("landscape_img",""));':
    'Img.loadCatalogBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("poster",""),x.optString("cover",""),x.optString("stream_icon",""),x.optString("landscape",""),x.optString("landscape_img",""),x.optString("backdrop",""));',
    'Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("landscape",""),x.optString("landscape_img",""));':
    'Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("poster",""),x.optString("cover",""),x.optString("stream_icon",""),x.optString("landscape",""),x.optString("landscape_img",""),x.optString("backdrop",""));',
    'Img.loadBest(im,use.optString("thumbnail",""),use.optString("portrait_img",""),use.optString("image",""),use.optString("landscape",""),use.optString("landscape_img",""));':
    'Img.loadBest(im,use.optString("thumbnail",""),use.optString("portrait_img",""),use.optString("image",""),use.optString("poster",""),use.optString("cover",""),use.optString("stream_icon",""),use.optString("landscape",""),use.optString("landscape_img",""),use.optString("backdrop",""));'
}
for old, new in replacements.items():
    s = s.replace(old, new)

if "catalog52805_" not in s:
    raise SystemExit("schema catalog52805 nao encontrado")
s = s.replace("catalog52805_", "catalog52807_")

if 'Api.post("content_enrich"' in s:
    raise SystemExit("ERRO: ainda existe chamada content_enrich")
if "prepareCriticalDetails(snapshot,()->warmHomeImages" in s:
    raise SystemExit("ERRO: bootstrap ainda depende de prepareCriticalDetails")

main.write_text(s, encoding="utf-8")

g = gradle.read_text(encoding="utf-8")
g = g.replace("versionCode 52805", "versionCode 52807")
g = g.replace("versionName '5.28.5'", "versionName '5.28.7'")
if "versionCode 52807" not in g or "versionName '5.28.7'" not in g:
    raise SystemExit("falha ao atualizar versao")
gradle.write_text(g, encoding="utf-8")

notes = gradle.parent / "RELEASE_NOTES.txt"
notes.write_text(
    "# GreenPlay 5.28.7 / 52807\n"
    "Capas: snapshot/painel volta a ser a fonte da verdade.\n"
    "Removida dependencia de content_enrich/worker TMDB no app.\n"
    "Home nao espera TMDB card por card para abrir.\n"
    "Cards usam thumbnail, portrait_img, image, poster, cover e stream_icon recebidos da API.\n"
    "Snapshot 52805 e invalidado uma vez para sincronizacao limpa.\n"
    "Nenhuma alteracao em EPG, canais ou player ao vivo.\n",
    encoding="utf-8",
)

print("PATCH_52807_OK")
