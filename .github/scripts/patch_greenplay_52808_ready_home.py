#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 4:
    raise SystemExit("uso: patch_greenplay_52808_ready_home.py MainActivity.java Img.java app/build.gradle")

main=Path(sys.argv[1]); img=Path(sys.argv[2]); gradle=Path(sys.argv[3])
s=main.read_text(encoding="utf-8")

def method_bounds(src, marker):
    start=src.find(marker)
    if start<0: raise SystemExit("metodo nao encontrado: "+marker)
    op=src.find("{",start)
    if op<0: raise SystemExit("abertura nao encontrada: "+marker)
    depth=0;i=op;state="code"
    while i<len(src):
        ch=src[i]; nx=src[i+1] if i+1<len(src) else ""
        if state=="code":
            if ch=='"': state="double"
            elif ch=="'": state="single"
            elif ch=="/" and nx=="/": state="line"; i+=1
            elif ch=="/" and nx=="*": state="block"; i+=1
            elif ch=="{": depth+=1
            elif ch=="}":
                depth-=1
                if depth==0: return start,i+1
        elif state=="double":
            if ch=="\\": i+=1
            elif ch=='"': state="code"
        elif state=="single":
            if ch=="\\": i+=1
            elif ch=="'": state="code"
        elif state=="line":
            if ch=="\n": state="code"
        elif state=="block":
            if ch=="*" and nx=="/": state="code"; i+=1
        i+=1
    raise SystemExit("fim nao encontrado: "+marker)

def replace_method(src, marker, replacement):
    a,b=method_bounds(src,marker)
    return src[:a]+replacement.rstrip()+src[b:]

# Helper: mede somente os primeiros cards realmente visiveis de cada trilho.
insert_marker=" JSONObject protectHomePayload(JSONObject fresh){ return fresh; }"
helper=r'''
 int homeArtworkCoveragePct(JSONObject rootJson){
  int total=0,ready=0;
  try{
   JSONArray sections=rootJson==null?null:rootJson.optJSONArray("result");
   if(sections==null)return 0;
   for(int i=0;i<sections.length()&&total<120;i++){
    JSONObject sec=sections.optJSONObject(i);if(sec==null)continue;
    int t=sec.optInt("type_id",sec.optInt("video_type",1));if(t!=1&&t!=2)continue;
    JSONArray a=sec.optJSONArray("data");if(a==null)continue;
    for(int k=0;k<a.length()&&k<3&&total<120;k++){
     JSONObject x=a.optJSONObject(k);if(x==null)continue;total++;
     String u=detailValue(x,"thumbnail","portrait_img","image","poster","landscape","landscape_img","backdrop");
     if(!u.trim().isEmpty())ready++;
    }
   }
  }catch(Exception ignored){}
  if(total==0)return 0;
  return Math.round((ready*100f)/total);
 }
'''
if "int homeArtworkCoveragePct(JSONObject rootJson)" not in s:
    if insert_marker not in s: raise SystemExit("protectHomePayload nao encontrado")
    s=s.replace(insert_marker,insert_marker+"\n"+helper,1)

s=replace_method(s,"void warmCriticalHomeImages(JSONObject j,Runnable done){",r'''
 void warmCriticalHomeImages(JSONObject j,Runnable done){
  java.util.ArrayList<String> urls=new java.util.ArrayList<>();java.util.HashSet<String> seen=new java.util.HashSet<>();
  try{
   JSONArray sections=j==null?null:j.optJSONArray("result");
   if(sections!=null)for(int i=0;i<sections.length()&&urls.size()<24;i++){
    JSONObject sec=sections.optJSONObject(i);if(sec==null)continue;JSONArray data=sec.optJSONArray("data");if(data==null)continue;
    for(int k=0;k<data.length()&&k<3&&urls.size()<24;k++){
     JSONObject x=data.optJSONObject(k);if(x==null)continue;
     String poster=detailValue(x,"thumbnail","portrait_img","image","poster");
     if(!poster.isEmpty()&&seen.add(poster))urls.add(poster);
    }
   }
  }catch(Exception ignored){}
  Img.prefetchCritical(this,urls,Math.min(24,urls.size()),3200,done);
 }''')

s=replace_method(s,"void warmHomeImages(JSONObject j,Runnable done){",r'''
 void warmHomeImages(JSONObject j,Runnable done){
  java.util.ArrayList<String> critical=new java.util.ArrayList<>();
  java.util.ArrayList<String> background=new java.util.ArrayList<>();
  java.util.HashSet<String> seen=new java.util.HashSet<>();
  try{
   JSONArray sections=j==null?null:j.optJSONArray("result");
   if(sections!=null)for(int i=0;i<sections.length()&&background.size()<180;i++){
    JSONObject sec=sections.optJSONObject(i);if(sec==null)continue;JSONArray data=sec.optJSONArray("data");if(data==null)continue;
    for(int k=0;k<data.length()&&k<6&&background.size()<180;k++){
     JSONObject x=data.optJSONObject(k);if(x==null)continue;
     String poster=detailValue(x,"thumbnail","portrait_img","image","poster");
     String land=detailValue(x,"landscape","landscape_img","backdrop");
     if(!poster.isEmpty()&&seen.add(poster)){
      background.add(poster);
      // No celular aparecem ~3 posters por trilho. A tela de sincronizacao segura
      // esses cards antes de abrir a Home.
      if(k<3&&critical.size()<96)critical.add(poster);
     }
     // Hero usa landscape; aquece apenas os primeiros, sem duplicar dezenas de backdrops.
     if(i<8&&k==0&&!land.isEmpty()&&seen.add(land)){
      background.add(land);if(critical.size()<96)critical.add(land);
     }
    }
   }
  }catch(Exception ignored){}
  if(critical.isEmpty()){done.run();return;}
  Img.prefetchCritical(this,critical,Math.min(96,critical.size()),7800,()->{
   done.run();
   Img.prefetchBackground(this,background);
  });
 }''')

s=replace_method(s,"void startExistingSessionReadyConfirmed(){",r'''
 void startExistingSessionReadyConfirmed(){
  if(Api.PROVIDER==null||Api.PROVIDER.trim().isEmpty()){providerSelectAfterLogin();return;}
  JSONObject cache=readHomeCache();
  if(cache!=null&&cache.optJSONArray("result")!=null&&cache.optJSONArray("result").length()>0){
   // 5.28.8: snapshot antigo/incompleto nao abre a Home com cards vazios.
   // Se os primeiros cards dos trilhos ainda nao vieram com arte do painel, refaz bootstrap.
   if(isPersistentHomeStale()||homeArtworkCoveragePct(cache)<92){
    showProviderBootstrap(sp.getString("provider_name","GreenPlay"));return;
   }
   showQuickResumeScreen();
   final JSONObject readyCache=cache;
   warmHomeImages(readyCache,()->{
    if(isFinishing())return;
    shell();markPersistentHomeUsed();warmCachedHomeAssets(readyCache);scheduleCatalogRefreshIfNeeded();
   });
   return;
  }
  showQuickResumeScreen();
  loadPersistentHomeAsync(new PersistentHomeCB(){public void ok(JSONObject disk){
   if(isFinishing())return;saveHomeCache(disk);
   if(isPersistentHomeStale()||homeArtworkCoveragePct(disk)<92){
    showProviderBootstrap(sp.getString("provider_name","GreenPlay"));return;
   }
   warmHomeImages(disk,()->{
    if(isFinishing())return;
    shell();markPersistentHomeUsed();warmCachedHomeAssets(disk);scheduleCatalogRefreshIfNeeded();
   });
  }public void miss(){if(!isFinishing())showProviderBootstrap(sp.getString("provider_name","GreenPlay"));}});
 }''')

# Novo schema para nao reutilizar snapshot 5.28.7 ja salvo com buracos.
if "catalog52807_" not in s: raise SystemExit("schema catalog52807 nao encontrado")
s=s.replace("catalog52807_","catalog52808_")

main.write_text(s,encoding="utf-8")

im=img.read_text(encoding="utf-8")
im=im.replace(
 'static final ExecutorService VISIBLE_POOL=Executors.newFixedThreadPool(6,imageThreadFactory("gp-img-"));',
 'static final ExecutorService VISIBLE_POOL=Executors.newFixedThreadPool(8,imageThreadFactory("gp-img-"));'
)
# w500 ja e suficiente para poster; nao transformar em w780 no 3G/4G.
old='url=url.replace("/w200/","/w780/").replace("/w300/","/w780/").replace("/w342/","/w780/").replace("/w500/","/w780/");'
new='url=url.replace("/w200/","/w500/").replace("/w300/","/w500/").replace("/w342/","/w500/");'
if old not in im: raise SystemExit("normalize TMDB w780 nao encontrado")
im=im.replace(old,new,1)
img.write_text(im,encoding="utf-8")

g=gradle.read_text(encoding="utf-8")
g=g.replace("versionCode 52807","versionCode 52808")
g=g.replace("versionName '5.28.7'","versionName '5.28.8'")
if "versionCode 52808" not in g or "versionName '5.28.8'" not in g:
    raise SystemExit("falha versao 52808")
gradle.write_text(g,encoding="utf-8")

notes=gradle.parent/"RELEASE_NOTES.txt"
notes.write_text(
 "# GreenPlay 5.28.8 / 52808\n"
 "Home pronta antes de aparecer: snapshot com capas visiveis incompletas e refeito.\n"
 "Inicializacao aquece os primeiros posters de cada trilho durante a tela de sincronizacao.\n"
 "Cache 5.28.7 e invalidado uma vez para remover snapshots salvos com cards vazios.\n"
 "TMDB w500 permanece w500 em vez de baixar w780 desnecessariamente.\n"
 "Pool visivel de imagens: 8 downloads paralelos.\n"
 "Sem content_enrich/worker no aplicativo.\n"
 "Nenhuma alteracao em EPG, canais ou player.\n",
 encoding="utf-8"
)
print("PATCH_52808_OK")
