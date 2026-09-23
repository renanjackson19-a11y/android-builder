from pathlib import Path
root=Path("work")

p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52876" in s and "versionName '5.28.76'" in s
s=s.replace("versionCode 52876","versionCode 52877",1).replace("versionName '5.28.76'","versionName '5.28.77'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

# Do not fail a source that is known to be movies/series only just because it has no live TV.
old='''  JSONArray data=snapshot.optJSONArray("result");if((data==null||data.length()==0)&&!sessionHasLive){showBootstrapFailure(c,progress,percent,status,detail,name,movieCount,seriesCount,liveCount);return;}'''
new='''  JSONArray data=snapshot.optJSONArray("result");
  boolean vodOnlyKnown=liveKnown&&!hasLive&&liveCount<=0;
  if((data==null||data.length()==0)&&!sessionHasLive&&!vodOnlyKnown){showBootstrapFailure(c,progress,percent,status,detail,name,movieCount,seriesCount,liveCount);return;}'''
assert old in s
s=s.replace(old,new,1)

# The loading footer must reflect what the current source actually has.
old='''  TextView footer=t("FILMES  •  SÉRIES  •  CANAIS  •  CAPAS  •  LOGOS  •  EPG",tvMode?8:9);'''
new='''  String bootstrapFooter=(liveCount==0&&sessionLiveKnown)?"FILMES  •  SÉRIES  •  CAPAS":"FILMES  •  SÉRIES  •  CANAIS  •  CAPAS  •  LOGOS  •  EPG";
  TextView footer=t(bootstrapFooter,tvMode?8:9);'''
assert old in s
s=s.replace(old,new,1)

# If provider metadata already says this source has zero live channels,
# skip the live scan entirely. It was unnecessary for VOD-only sources.
old='''   final boolean[] catalogDone={false};Runnable catalogReady=()->{if(catalogDone[0])return;catalogDone[0]=true;
    setBootstrapProgress(progress,percent,status,detail,58,"Conferindo canais","Validando a lista completa para não deixar nenhum canal de fora…");
    reconcileBootstrapLiveChannels(snapshot,()->{
     JSONArray liveSnapshot=snapshot.optJSONArray("live_channels");boolean hasLive=liveSnapshot!=null&&liveSnapshot.length()>0;
     if(!hasLive){
      setBootstrapProgress(progress,percent,status,detail,96,"Finalizando","Catálogo, capas e detalhes iniciais preparados…");
      finishProviderBootstrapWithLive(c,progress,percent,status,detail,name,movieCount,seriesCount,liveCount,snapshot,false,true,null);return;
     }'''
new='''   final boolean[] catalogDone={false};Runnable catalogReady=()->{if(catalogDone[0])return;catalogDone[0]=true;
    if(sessionLiveKnown&&liveCount<=0){
     setBootstrapProgress(progress,percent,status,detail,92,"Filmes e séries prontos","Finalizando catálogo e capas…");
     finishProviderBootstrapWithLive(c,progress,percent,status,detail,name,movieCount,seriesCount,0,snapshot,false,true,null);return;
    }
    setBootstrapProgress(progress,percent,status,detail,58,"Conferindo canais","Validando a lista completa para não deixar nenhum canal de fora…");
    reconcileBootstrapLiveChannels(snapshot,()->{
     JSONArray liveSnapshot=snapshot.optJSONArray("live_channels");boolean hasLive=liveSnapshot!=null&&liveSnapshot.length()>0;
     if(!hasLive){
      setBootstrapProgress(progress,percent,status,detail,96,"Finalizando","Catálogo, capas e detalhes iniciais preparados…");
      finishProviderBootstrapWithLive(c,progress,percent,status,detail,name,movieCount,seriesCount,liveCount,snapshot,false,true,null);return;
     }'''
assert old in s
s=s.replace(old,new,1)

# VOD-only source with a temporary empty snapshot should enter the app instead of
# getting stuck on the red failure screen; Filmes/Séries load normally on demand.
old='''  setBootstrapProgress(progress,percent,status,detail,100,"Tudo pronto","Abrindo sua experiência…");
  modeReloadScreen=false;new Handler(Looper.getMainLooper()).postDelayed(()->shell(),700);'''
new='''  if(vodOnlyKnown&&(data==null||data.length()==0)){
   setBootstrapProgress(progress,percent,status,detail,100,"Servidor conectado","Abrindo Filmes e Séries…");
  }else{
   setBootstrapProgress(progress,percent,status,detail,100,"Tudo pronto","Abrindo sua experiência…");
  }
  modeReloadScreen=false;new Handler(Looper.getMainLooper()).postDelayed(()->shell(),500);'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.77 — Fonte apenas Filmes/Séries
Servidor conhecido com 0 canais não entra mais em erro por falta de TV.
Bootstrap não procura canais/logos/EPG quando a fonte é somente VOD.
Tela de sincronização mostra apenas Filmes, Séries e Capas nesse tipo de fonte.
Mesmo com snapshot inicial vazio, abre o app e permite carregar Filmes/Séries sob demanda.
Mantida a proteção de VPN e o modal centralizado da 5.28.76.
\n"""+prior)
print("patched 5.28.77")
