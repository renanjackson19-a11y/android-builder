from pathlib import Path
root=Path("work")

p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52890" in s and "versionName '5.28.90'" in s
s=s.replace("versionCode 52890","versionCode 52891",1).replace("versionName '5.28.90'","versionName '5.28.91'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

old=''' void watchFootballGame(JSONObject game){
  if(game==null||!game.optBoolean("live",false))return;if(blockVpnProtectedContent())return;
  String search=game.optString("watch_search","").trim();openFootballMappedChannel(search,false);
 }'''
new=''' void watchFootballGame(JSONObject game){
  if(game==null||!game.optBoolean("live",false))return;if(blockVpnProtectedContent())return;
  JSONObject direct=game.optJSONObject("watch_channel");
  if(direct!=null&&direct.optString("video_720",direct.optString("video_1080","")).trim().length()>0){openLiveAllowed(direct);return;}
  String search=game.optString("watch_search","").trim();openFootballMappedChannel(search,false);
 }'''
assert old in s
s=s.replace(old,new,1)

old='''  String round=league.optString("round","");if(!round.isEmpty()){TextView r=t(round,10);r.setTextColor(0xff718079);r.setSingleLine(true);r.setEllipsize(android.text.TextUtils.TruncateAt.END);wrap.addView(r,new LinearLayout.LayoutParams(-1,dp(20)));}
  if(live){
   TextView watch=t("▶  ASSISTIR",13);watch.setTypeface(null,1);watch.setTextColor(0xff07150d);watch.setGravity(Gravity.CENTER);watch.setFocusable(tvMode);GradientDrawable wb=round(GREEN,13);watch.setBackground(wb);watch.setContentDescription("Assistir jogo ao vivo");watch.setOnClickListener(v->watchFootballGame(x));if(tvMode)armTvFocus(watch);LinearLayout.LayoutParams wlp=new LinearLayout.LayoutParams(-1,dp(42));wlp.setMargins(0,dp(6),0,0);wrap.addView(watch,wlp);
  }
  return wrap;'''
new='''  String round=league.optString("round","");if(!round.isEmpty()){TextView r=t(round,10);r.setTextColor(0xff718079);r.setSingleLine(true);r.setEllipsize(android.text.TextUtils.TruncateAt.END);wrap.addView(r,new LinearLayout.LayoutParams(-1,dp(20)));}

  String mapped=x.optString("watch_search","").trim();
  String broadcaster=x.optString("watch_broadcaster","").trim();
  JSONArray broadcastNames=x.optJSONArray("broadcast_names");
  StringBuilder stations=new StringBuilder();
  if(broadcastNames!=null){for(int i=0;i<broadcastNames.length();i++){String n=broadcastNames.optString(i,"").trim();if(n.isEmpty())continue;if(stations.length()>0)stations.append(" • ");stations.append(n);if(stations.length()>72)break;}}
  String tx="";
  if(!mapped.isEmpty()){tx="Canal: "+mapped;if(!broadcaster.isEmpty()&&!broadcaster.equalsIgnoreCase(mapped))tx="Transmissão: "+broadcaster+"  •  "+mapped;}
  else if(stations.length()>0)tx="Onde assistir: "+stations;
  if(!tx.isEmpty()){TextView tr=t(tx,11);tr.setTextColor(mapped.isEmpty()?0xffa9b5ae:GREEN);tr.setMaxLines(2);tr.setEllipsize(android.text.TextUtils.TruncateAt.END);tr.setPadding(0,dp(3),0,dp(2));wrap.addView(tr,new LinearLayout.LayoutParams(-1,-2));}

  if(live){
   boolean available=x.optBoolean("watch_available",false)||!mapped.isEmpty()||x.optJSONObject("watch_channel")!=null;
   TextView watch=t(available?"▶  ASSISTIR":"CANAL AINDA NÃO LOCALIZADO",13);watch.setTypeface(null,1);watch.setTextColor(available?0xff07150d:0xff9ba7a1);watch.setGravity(Gravity.CENTER);watch.setFocusable(tvMode&&available);GradientDrawable wb=round(available?GREEN:0xff16211b,13);if(!available)wb.setStroke(dp(1),0xff31473a);watch.setBackground(wb);watch.setContentDescription(available?"Assistir jogo ao vivo":"Canal ainda não localizado");if(available)watch.setOnClickListener(v->watchFootballGame(x));if(tvMode&&available)armTvFocus(watch);LinearLayout.LayoutParams wlp=new LinearLayout.LayoutParams(-1,dp(42));wlp.setMargins(0,dp(6),0,0);wrap.addView(watch,wlp);
  }
  return wrap;'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.91 — Canais automáticos nos jogos
Os cards de Futebol agora mostram a emissora/canal quando a agenda informa transmissão.
Quando o VPS encontra o canal correspondente no servidor atual, o card mostra o canal do GreenPlay.
Em jogos ao vivo vinculados, ASSISTIR abre diretamente o canal resolvido pelo servidor.
Se o jogo estiver ao vivo mas ainda sem canal correspondente, o card informa que o canal ainda não foi localizado.
Mantidos Futebol Brasileiro separado da fonte Internacional, centralização e demais recursos da 5.28.90.

"""+prior)
print("patched 5.28.91")
