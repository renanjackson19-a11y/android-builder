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
  if(direct!=null&&direct.length()>0){openLiveAllowed(direct);return;}
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

  JSONArray broadcastNames=x.optJSONArray("broadcast_names");StringBuilder bt=new StringBuilder();
  if(broadcastNames!=null)for(int bi=0;bi<broadcastNames.length()&&bi<4;bi++){String bn=broadcastNames.optString(bi,"").trim();if(bn.isEmpty())continue;if(bt.length()>0)bt.append(" • ");bt.append(bn);}
  if(bt.length()>0){TextView tv=t("📺  Onde assistir: "+bt,11);tv.setTextColor(0xffb8c7bf);tv.setMaxLines(2);tv.setEllipsize(android.text.TextUtils.TruncateAt.END);tv.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);wrap.addView(tv,new LinearLayout.LayoutParams(-1,dp(bt.length()>42?38:26)));}

  JSONObject linked=x.optJSONObject("watch_channel");String linkedName=linked==null?"":linked.optString("name",linked.optString("stream_name","")).trim();
  if(!linkedName.isEmpty()){TextView lc=t("GreenPlay: "+linkedName,11);lc.setTextColor(GREEN);lc.setTypeface(null,1);lc.setSingleLine(true);lc.setEllipsize(android.text.TextUtils.TruncateAt.END);wrap.addView(lc,new LinearLayout.LayoutParams(-1,dp(24)));}

  if(live&&x.optBoolean("watch_available",false)){
   TextView watch=t("▶  ASSISTIR AGORA",13);watch.setTypeface(null,1);watch.setTextColor(0xff07150d);watch.setGravity(Gravity.CENTER);watch.setFocusable(tvMode);GradientDrawable wb=round(GREEN,13);watch.setBackground(wb);watch.setContentDescription("Assistir jogo ao vivo");watch.setOnClickListener(v->watchFootballGame(x));if(tvMode)armTvFocus(watch);LinearLayout.LayoutParams wlp=new LinearLayout.LayoutParams(-1,dp(42));wlp.setMargins(0,dp(6),0,0);wrap.addView(watch,wlp);
  }else if(live){
   TextView wait=t("AO VIVO • canal ainda não localizado neste servidor",11);wait.setGravity(Gravity.CENTER);wait.setTextColor(0xffffc46b);LinearLayout.LayoutParams wlp=new LinearLayout.LayoutParams(-1,dp(34));wlp.setMargins(0,dp(4),0,0);wrap.addView(wait,wlp);
  }
  return wrap;'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.91 — Canais dos jogos + assistir automático
Os cards de Futebol agora mostram automaticamente as emissoras/plataformas divulgadas para cada partida.
Quando o GreenPlay encontra o canal correspondente no servidor atual, o card também mostra o canal GreenPlay vinculado.
Em jogo AO VIVO com canal localizado, aparece ASSISTIR AGORA e o app abre diretamente o canal exato retornado pelo servidor.
Quando a partida está ao vivo mas o canal ainda não existe na fonte atual, o card informa isso sem mandar o usuário para um canal errado.
Não é necessário cadastrar link manualmente no painel; o vínculo é feito automaticamente a partir da agenda + canais do provedor atual.

"""+prior)
print("patched 5.28.91")
