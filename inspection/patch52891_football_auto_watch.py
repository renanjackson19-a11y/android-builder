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
  if(direct!=null){
   String u=direct.optString("video_1080",direct.optString("video_720",direct.optString("video_480",direct.optString("video_320",""))));
   if(u!=null&&!u.trim().isEmpty()){openLiveAllowed(direct);return;}
  }
  String search=game.optString("watch_search","").trim();openFootballMappedChannel(search,false);
 }'''
assert old in s
s=s.replace(old,new,1)

old='''  String round=league.optString("round","");if(!round.isEmpty()){TextView r=t(round,10);r.setTextColor(0xff718079);r.setSingleLine(true);r.setEllipsize(android.text.TextUtils.TruncateAt.END);wrap.addView(r,new LinearLayout.LayoutParams(-1,dp(20)));}
  if(live){
   TextView watch=t("▶  ASSISTIR",13);watch.setTypeface(null,1);watch.setTextColor(0xff07150d);watch.setGravity(Gravity.CENTER);watch.setFocusable(tvMode);GradientDrawable wb=round(GREEN,13);watch.setBackground(wb);watch.setContentDescription("Assistir jogo ao vivo");watch.setOnClickListener(v->watchFootballGame(x));if(tvMode)armTvFocus(watch);LinearLayout.LayoutParams wlp=new LinearLayout.LayoutParams(-1,dp(42));wlp.setMargins(0,dp(6),0,0);wrap.addView(watch,wlp);
  }'''
new='''  String round=league.optString("round","");if(!round.isEmpty()){TextView r=t(round,10);r.setTextColor(0xff718079);r.setSingleLine(true);r.setEllipsize(android.text.TextUtils.TruncateAt.END);wrap.addView(r,new LinearLayout.LayoutParams(-1,dp(20)));}
  JSONArray bn=x.optJSONArray("broadcast_names");StringBuilder tvs=new StringBuilder();if(bn!=null){for(int i=0;i<bn.length();i++){String n=bn.optString(i,"").trim();if(n.isEmpty())continue;if(tvs.length()>0)tvs.append(" • ");tvs.append(n);}}
  if(tvs.length()>0){TextView tv=t("Transmissão: "+tvs,11);tv.setTextColor(0xffb8c8bf);tv.setMaxLines(2);tv.setEllipsize(android.text.TextUtils.TruncateAt.END);tv.setPadding(0,dp(2),0,dp(2));wrap.addView(tv,new LinearLayout.LayoutParams(-1,-2));}
  String mapped=x.optString("watch_search","").trim();boolean linked=x.optBoolean("watch_available",false)&&!mapped.isEmpty();
  if(linked){TextView m=t("GreenPlay: "+mapped,11);m.setTextColor(GREEN);m.setMaxLines(2);m.setEllipsize(android.text.TextUtils.TruncateAt.END);m.setPadding(0,dp(2),0,dp(3));wrap.addView(m,new LinearLayout.LayoutParams(-1,-2));}
  else if(tvs.length()>0){TextView m=t("GreenPlay: vínculo automático aguardando canal",10);m.setTextColor(0xff819188);m.setPadding(0,dp(1),0,dp(3));wrap.addView(m,new LinearLayout.LayoutParams(-1,-2));}
  if(live){
   String label=linked?"▶  ASSISTIR":"ABRIR TV";
   TextView watch=t(label,13);watch.setTypeface(null,1);watch.setTextColor(linked?0xff07150d:0xffd9e0dc);watch.setGravity(Gravity.CENTER);watch.setFocusable(tvMode);GradientDrawable wb=round(linked?GREEN:0xff263d31,13);watch.setBackground(wb);watch.setContentDescription(linked?"Assistir jogo ao vivo":"Abrir TV ao vivo");watch.setOnClickListener(v->watchFootballGame(x));if(tvMode)armTvFocus(watch);LinearLayout.LayoutParams wlp=new LinearLayout.LayoutParams(-1,dp(42));wlp.setMargins(0,dp(6),0,0);wrap.addView(watch,wlp);
  }'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.91 — Futebol com transmissão automática
Mostra no card as emissoras/plataformas que transmitirão cada partida.
Mostra o canal correspondente encontrado automaticamente no servidor atual do GreenPlay.
Quando a partida entra AO VIVO e o vínculo automático existe, ASSISTIR abre diretamente o canal resolvido pelo servidor, sem cadastro manual no painel.
Se a emissora já foi divulgada mas o canal ainda não existe na fonte, o app indica a situação e ABRIR TV continua disponível.
Mantidos futebol brasileiro completo, agenda internacional, VPN, player e demais recursos anteriores.

"""+prior)
print("patched 5.28.91")
