from pathlib import Path

root=Path("work")
app=root/"app/src/main/java/fun/greenplay/app"

def replace_method(text, marker, new_method):
    start=text.find(marker)
    if start<0: raise SystemExit("marker not found: "+marker)
    brace=text.find("{",start)
    depth=0; end=None
    for i in range(brace,len(text)):
        if text[i]=="{": depth+=1
        elif text[i]=="}":
            depth-=1
            if depth==0:
                end=i+1; break
    if end is None: raise SystemExit("method end not found: "+marker)
    return text[:start]+new_method+text[end:]

# Home: keep sources separated, never mixed in the same grid.
p=app/"MainActivity.java"
m=p.read_text(encoding="utf-8")

m=m.replace(
'''   if(seed.length()>0)grid(seed);
   fetchYoutubeShortsTvProgressive(1,0,seen,gen,host);
   return;''',
'''   if(seed.length()>0)grid(seed);
   fetchYoutubeShortsTvProgressive(1,0,seen,gen,host);
   loadExternalDoramasHome(gen);
   return;''',1)

m=m.replace(
'''  if(seed.length()>0){prefetchGreenShortDetails(seed,24);featureCarousel(seed);grid(seed);startGreenShortsPaging(seed,gen);return;}''',
'''  if(seed.length()>0){prefetchGreenShortDetails(seed,24);featureCarousel(seed);grid(seed);startGreenShortsPaging(seed,gen);loadExternalDoramasHome(gen);return;}''',1)

new_external=''' void loadExternalDoramasHome(final int gen){
  ExternalDoramas.fetchAll(new ExternalDoramas.CB(){
   public void ok(JSONArray ext){
    if(gen!=viewGen||body==null||ext==null||ext.length()==0)return;
    JSONArray hub=filterExternalSource(ext,"dramahub"), tall=filterExternalSource(ext,"dramatall");
    renderExternalSourceRow("DramaHub",hub,gen);
    renderExternalSourceRow("DramaTall",tall,gen);
   }
   public void err(String e){}
  });
 }'''
m=replace_method(m," void loadExternalDoramasHome(final int gen)",new_external)

anchor=" int greenShortsPageSize(){return 60;}"
helpers=''' JSONArray filterExternalSource(JSONArray src,String provider){
  JSONArray out=new JSONArray();if(src==null)return out;
  for(int i=0;i<src.length();i++){JSONObject x=src.optJSONObject(i);if(x!=null&&provider.equalsIgnoreCase(x.optString("provider_source","")))out.put(x);}
  return out;
 }
 void renderExternalSourceRow(String label,JSONArray rows,int gen){
  if(gen!=viewGen||body==null||rows==null||rows.length()==0)return;
  TextView h=t("Fonte:  "+label,17);h.setTypeface(null,1);h.setTextColor(GREEN);h.setPadding(dp(4),dp(14),0,dp(6));
  body.addView(h,new LinearLayout.LayoutParams(-1,dp(46)));
  posterRowInto(body,rows);
 }
 boolean isExternalDorama(JSONObject x){return x!=null&&("external".equalsIgnoreCase(x.optString("source",""))||!x.optString("provider_source","").trim().isEmpty());}
 String doramaSourceName(JSONObject x){
  if(x==null)return "Yelly";
  String p=x.optString("provider_source","").toLowerCase(java.util.Locale.ROOT);
  if("dramahub".equals(p))return "DramaHub";
  if("dramatall".equals(p))return "DramaTall";
  if(!x.optString("youtube_id","").trim().isEmpty()||"youtube".equalsIgnoreCase(x.optString("source",""))||"greenshorts".equalsIgnoreCase(x.optString("source","")))return "YouTube";
  return "Yelly";
 }
'''+anchor
if anchor not in m: raise SystemExit("greenShortsPageSize anchor missing")
m=m.replace(anchor,helpers,1)

new_open=''' void openYoutubeVideo(JSONObject source,String title,boolean restart){
  if(source==null)return;
  if(isExternalDorama(source)){
   String u=detailPlayUrl(source);
   if(!u.isEmpty()){openPlayableUrl(source,title==null?"Yelly Doramas":title,false,u);return;}
   ExternalDoramas.resolve(source,new ExternalDoramas.CB(){
    public void ok(JSONArray a){JSONObject r=(a!=null&&a.length()>0)?a.optJSONObject(0):null;String ru=detailPlayUrl(r);if(ru.isEmpty()){runOnUiThread(()->Toast.makeText(MainActivity.this,"Esta fonte não entregou vídeo direto.",Toast.LENGTH_SHORT).show());return;}runOnUiThread(()->openPlayableUrl(r,title==null?"Yelly Doramas":title,false,ru));}
    public void err(String e){runOnUiThread(()->Toast.makeText(MainActivity.this,"Fonte indisponível agora.",Toast.LENGTH_SHORT).show());}
   });return;
  }
  String id=youtubeVideoId(source);
  if(id.isEmpty()){Toast.makeText(this,"Vídeo do YouTube indisponível.",Toast.LENGTH_SHORT).show();return;}
  if(restart)clearGreenShortResume(source);
  Intent in=new Intent(this,YouTubePlayerActivity.class);
  in.putExtra("youtube_id",id);in.putExtra("greenshorts_id",id);
  in.putExtra("title",title==null?"Yelly Doramas":title);
  in.putExtra("poster",detailValue(source,"thumbnail","portrait_img","poster","image"));
  in.putExtra("tv_mode",tvMode);
  int resume=restart?0:greenShortResumePosition(source);if(resume>0)in.putExtra("resume_ms",resume);
  startActivity(in);
 }'''
m=replace_method(m," void openYoutubeVideo(JSONObject source,String title,boolean restart)",new_open)

# Visible source indication on detail screens.
needle='''  String providerId=source.optString("id",d.optString("id",""));if(!isYoutube&&!providerId.isEmpty()){View idBadge=detailIdBadge("ID:  "+providerId);LinearLayout.LayoutParams idlp=new LinearLayout.LayoutParams(-2,-2);idlp.setMargins(0,dp(2),0,dp(12));host.addView(idBadge,idlp);}'''
replacement='''  if(isYoutube){View srcBadge=detailIdBadge("Fonte:  "+doramaSourceName(source));LinearLayout.LayoutParams slp0=new LinearLayout.LayoutParams(-2,-2);slp0.setMargins(0,dp(2),0,dp(12));host.addView(srcBadge,slp0);}
  String providerId=source.optString("id",d.optString("id",""));if(!isYoutube&&!providerId.isEmpty()){View idBadge=detailIdBadge("ID:  "+providerId);LinearLayout.LayoutParams idlp=new LinearLayout.LayoutParams(-2,-2);idlp.setMargins(0,dp(2),0,dp(12));host.addView(idBadge,idlp);}'''
if needle not in m: raise SystemExit("detail source badge anchor missing")
m=m.replace(needle,replacement,1)
p.write_text(m,encoding="utf-8")

# Restore working YouTube Stories and make the source obvious.
p=app/"StoriesActivity.java"
s=p.read_text(encoding="utf-8")
needle='title.setText(nm);'
if needle not in s: raise SystemExit("Stories title anchor missing")
s=s.replace(needle,'title.setText("YouTube  •  "+nm);',1)
p.write_text(s,encoding="utf-8")

# Re-register working YouTube player activity.
manifest=root/"app/src/main/AndroidManifest.xml"
x=manifest.read_text(encoding="utf-8")
if "YouTubePlayerActivity" not in x:
    x=x.replace('  <activity android:name=".PlayerActivity"','  <activity android:name=".YouTubePlayerActivity" android:exported="false" android:screenOrientation="unspecified" android:configChanges="orientation|screenSize"/>\n  <activity android:name=".PlayerActivity"',1)
manifest.write_text(x,encoding="utf-8")

grad=root/"app/build.gradle"
g=grad.read_text(encoding="utf-8")
if "versionCode 10021" not in g or "versionName '1.0.21'" not in g: raise SystemExit("wrong 1.0.21 base")
g=g.replace("versionCode 10021","versionCode 10022",1)
g=g.replace("versionName '1.0.21'","versionName '1.0.22'",1)
grad.write_text(g,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.22
- Corrige a mistura de fontes: DramaHub e DramaTall aparecem em seções separadas.
- Tela de detalhes mostra claramente a fonte do conteúdo.
- Stories voltam ao player YouTube funcional usado antes para o catálogo do YouTube.
- Ao abrir conteúdo YouTube, volta a usar YouTubePlayerActivity em vez do vídeo demo local.
- Conteúdo DramaHub/DramaTall continua usando o player nativo Yelly quando houver MP4/HLS.
- Fonte externa sem vídeo direto mostra aviso e não interfere no catálogo YouTube.
""",encoding="utf-8")
print("YELLY_122_SOURCE_SEPARATION_AND_YOUTUBE_RESTORE_OK")
