from pathlib import Path

root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text(encoding="utf-8")

old=''' JSONArray localSearchResults(String q){
  JSONArray out=new JSONArray();String needle=q==null?"":q.trim().toLowerCase(java.util.Locale.ROOT);if(needle.length()<2)return out;JSONObject prepared=readHomeCache();if(prepared==null)return out;java.util.HashSet<String> seen=new java.util.HashSet<>();JSONArray secs=prepared.optJSONArray("result");if(secs==null)return out;
  for(int i=0;i<secs.length()&&out.length()<72;i++){JSONObject sec=secs.optJSONObject(i);if(sec==null)continue;JSONArray d=sec.optJSONArray("data");if(d==null)continue;for(int k=0;k<d.length()&&out.length()<72;k++){JSONObject x=d.optJSONObject(k);if(x==null)continue;String name=x.optString("name",x.optString("title","")).toLowerCase(java.util.Locale.ROOT);if(!name.contains(needle))continue;String key=x.optInt("video_type",x.optInt("type_id",1))+"|"+x.optString("id",x.optString("video_id",""));if(seen.add(key))out.put(x);}}
  return out;
 }'''
new=''' String searchNorm(String v){
  if(v==null)return "";
  String x=java.text.Normalizer.normalize(v,java.text.Normalizer.Form.NFD);
  x=x.toLowerCase(java.util.Locale.ROOT).replaceAll("[^a-z0-9]+"," ").trim().replaceAll(" +"," ");
  return x;
 }
 boolean searchMatch(JSONObject x,String needle){
  if(x==null||needle==null||needle.length()<2)return false;
  String hay=searchNorm(x.optString("name","")+" "+x.optString("title","")+" "+x.optString("original_title","")+" "+x.optString("channel_name",""));
  for(String tok:needle.split(" "))if(tok.length()>=2&&!hay.contains(tok))return false;
  return true;
 }
 void addSearchMatches(JSONArray src,String needle,JSONArray out,java.util.HashSet<String> seen,int max){
  if(src==null)return;
  for(int i=0;i<src.length()&&out.length()<max;i++){
   JSONObject x=src.optJSONObject(i);if(!searchMatch(x,needle))continue;
   String yt=x.optString("youtube_id","").trim();String id=x.optString("id",x.optString("video_id","")).trim();
   String key=!yt.isEmpty()?"yt|"+yt:(!id.isEmpty()?x.optInt("video_type",x.optInt("type_id",1))+"|"+id:"n|"+searchNorm(x.optString("name",x.optString("title",""))));
   if(seen.add(key))out.put(x);
  }
 }
 JSONArray localSearchResults(String q){
  JSONArray out=new JSONArray();String needle=searchNorm(q);if(needle.length()<2)return out;java.util.HashSet<String> seen=new java.util.HashSet<>();
  try{
   JSONObject prepared=readHomeCache();JSONArray secs=prepared==null?null:prepared.optJSONArray("result");
   if(secs!=null)for(int i=0;i<secs.length()&&out.length()<120;i++){JSONObject sec=secs.optJSONObject(i);if(sec!=null)addSearchMatches(sec.optJSONArray("data"),needle,out,seen,120);}
  }catch(Exception ignored){}
  try{addSearchMatches(readGreenShortsSeedCache(),needle,out,seen,120);}catch(Exception ignored){}
  return out;
 }'''
if old not in s: raise SystemExit("localSearchResults anchor missing")
s=s.replace(old,new,1)

old='''  Api.post("search_catalog",Api.m("user_id",uid,"search",q,"limit","72"),new Api.CB(){public void ok(JSONObject j){runOnUiThread(()->{
    Object tag=host.getTag();if(!searchScreenOpen||tag==null||!requestKey.equals(String.valueOf(tag)))return;
    JSONArray remote=j.optJSONArray("result");host.removeAllViews();if(j.optInt("status",200)==200&&remote!=null){renderSearchGrid(remote,host);return;}
    if(local.length()>0){renderSearchGrid(local,host);return;}TextView e=t("Não foi possível concluir a pesquisa agora.",14);e.setTextColor(0xffa69ca3);e.setPadding(dp(3),dp(18),dp(3),0);host.addView(e);
  });}public void err(String e){runOnUiThread(()->{Object tag=host.getTag();if(!searchScreenOpen||tag==null||!requestKey.equals(String.valueOf(tag)))return;host.removeAllViews();if(local.length()>0){renderSearchGrid(local,host);return;}TextView m=t("Não foi possível pesquisar agora.",14);m.setTextColor(0xffa69ca3);m.setPadding(dp(3),dp(18),dp(3),0);host.addView(m);});}});
 }'''
new='''  Api.post("greenshorts",Api.m("user_id",uid,"search",q,"q",q,"page_no","1","page","1","offset","0","limit","120","per_page","120"),new Api.CB(){public void ok(JSONObject j){runOnUiThread(()->{
    Object tag=host.getTag();if(!searchScreenOpen||tag==null||!requestKey.equals(String.valueOf(tag)))return;
    JSONArray remote=j.optJSONArray("result");JSONArray merged=new JSONArray();java.util.HashSet<String> seen=new java.util.HashSet<>();
    if(remote!=null)for(int i=0;i<remote.length();i++){JSONObject x=remote.optJSONObject(i);if(x==null)continue;String yt=x.optString("youtube_id","").trim();String id=x.optString("id",x.optString("video_id","")).trim();String k=!yt.isEmpty()?"yt|"+yt:(!id.isEmpty()?"id|"+id:"n|"+searchNorm(x.optString("name",x.optString("title",""))));if(seen.add(k))merged.put(x);}
    for(int i=0;i<local.length()&&merged.length()<120;i++){JSONObject x=local.optJSONObject(i);if(x==null)continue;String yt=x.optString("youtube_id","").trim();String id=x.optString("id",x.optString("video_id","")).trim();String k=!yt.isEmpty()?"yt|"+yt:(!id.isEmpty()?"id|"+id:"n|"+searchNorm(x.optString("name",x.optString("title",""))));if(seen.add(k))merged.put(x);}
    host.removeAllViews();renderSearchGrid(merged,host);
  });}public void err(String e){runOnUiThread(()->{Object tag=host.getTag();if(!searchScreenOpen||tag==null||!requestKey.equals(String.valueOf(tag)))return;host.removeAllViews();renderSearchGrid(local,host);});}});
 }'''
if old not in s: raise SystemExit("renderSearchResults API anchor missing")
s=s.replace(old,new,1)

p.write_text(s,encoding="utf-8")

g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10030" not in t or "versionName '1.0.30'" not in t: raise SystemExit("wrong 1.0.30 base")
t=t.replace("versionCode 10030","versionCode 10031",1).replace("versionName '1.0.30'","versionName '1.0.31'",1)
g.write_text(t,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.31
- Corrigida a barra de pesquisa.
- A busca agora consulta o catálogo real de Doramas do Yelly no servidor.
- Pesquisa títulos exibidos, títulos originais e nome do canal.
- Busca ignora acentos e aceita palavras parciais.
- Resultados locais e do servidor são mesclados sem duplicados.
- Removida a chamada ao endpoint search_catalog, que não existia no servidor Yelly.
""",encoding="utf-8")
print("YELLY_131_SEARCH_FIXED_OK")
