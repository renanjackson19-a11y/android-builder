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
 }
 View footballGameRow(JSONObject x){'''
new=''' String footballBroadcastText(JSONObject game){
  if(game==null)return "";JSONArray a=game.optJSONArray("broadcast_names");if(a==null||a.length()==0)return "";java.util.ArrayList<String> names=new java.util.ArrayList<>();
  for(int i=0;i<a.length()&&names.size()<4;i++){String n=a.optString(i,"").trim();if(!n.isEmpty()&&!names.contains(n))names.add(n);}return android.text.TextUtils.join(" • ",names);
 }
 void watchFootballGame(JSONObject game){
  if(game==null||!game.optBoolean("live",false))return;if(blockVpnProtectedContent())return;
  JSONObject direct=game.optJSONObject("watch_channel");
  if(direct!=null){String u=direct.optString("video_1080",direct.optString("video_720",direct.optString("video_480",direct.optString("video_320",""))));if(!u.trim().isEmpty()){openLiveAllowed(direct);return;}}
  String search=game.optString("watch_search","").trim();openFootballMappedChannel(search,false);
 }
 View footballGameRow(JSONObject x){'''
assert old in s
s=s.replace(old,new,1)

old='''  String round=league.optString("round","");if(!round.isEmpty()){TextView r=t(round,10);r.setTextColor(0xff718079);r.setSingleLine(true);r.setEllipsize(android.text.TextUtils.TruncateAt.END);wrap.addView(r,new LinearLayout.LayoutParams(-1,dp(20)));}
  if(live){
   TextView watch=t("▶  ASSISTIR",13);watch.setTypeface(null,1);watch.setTextColor(0xff07150d);watch.setGravity(Gravity.CENTER);watch.setFocusable(tvMode);GradientDrawable wb=round(GREEN,13);watch.setBackground(wb);watch.setContentDescription("Assistir jogo ao vivo");watch.setOnClickListener(v->watchFootballGame(x));if(tvMode)armTvFocus(watch);LinearLayout.LayoutParams wlp=new LinearLayout.LayoutParams(-1,dp(42));wlp.setMargins(0,dp(6),0,0);wrap.addView(watch,wlp);
  }
  return wrap;'''
new='''  String round=league.optString("round","");if(!round.isEmpty()){TextView r=t(round,10);r.setTextColor(0xff718079);r.setSingleLine(true);r.setEllipsize(android.text.TextUtils.TruncateAt.END);wrap.addView(r,new LinearLayout.LayoutParams(-1,dp(20)));}
  String broadcaster=footballBroadcastText(x);String mapped=x.optString("watch_search","").trim();
  if(!broadcaster.isEmpty()){TextView bt=t("Onde assistir: "+broadcaster,11);bt.setTextColor(0xffaab8b0);bt.setMaxLines(2);bt.setEllipsize(android.text.TextUtils.TruncateAt.END);bt.setPadding(0,dp(3),0,0);wrap.addView(bt,new LinearLayout.LayoutParams(-1,-2));}
  if(!mapped.isEmpty()){TextView mt=t("GreenPlay: "+mapped,11);mt.setTextColor(GREEN);mt.setTypeface(null,1);mt.setSingleLine(true);mt.setEllipsize(android.text.TextUtils.TruncateAt.END);mt.setPadding(0,dp(3),0,0);wrap.addView(mt,new LinearLayout.LayoutParams(-1,dp(24)));}
  if(live){
   TextView watch=t("▶  ASSISTIR",13);watch.setTypeface(null,1);watch.setTextColor(0xff07150d);watch.setGravity(Gravity.CENTER);watch.setFocusable(tvMode);GradientDrawable wb=round(GREEN,13);watch.setBackground(wb);watch.setContentDescription("Assistir jogo ao vivo");watch.setOnClickListener(v->watchFootballGame(x));if(tvMode)armTvFocus(watch);LinearLayout.LayoutParams wlp=new LinearLayout.LayoutParams(-1,dp(42));wlp.setMargins(0,dp(7),0,0);wrap.addView(watch,wlp);
  }
  return wrap;'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prev=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.91 — canais de transmissão automáticos no Futebol
A tela de jogos mostra automaticamente Onde assistir quando a agenda informa a emissora/plataforma.
Quando o servidor do cliente possui o canal correspondente, o card mostra GreenPlay: nome do canal encontrado.
Ao ficar AO VIVO, ASSISTIR abre diretamente o canal resolvido pelo servidor, sem cadastro manual jogo por jogo.
Se a emissora ainda não foi publicada ou o canal não existe na fonte atual, o app mantém fallback para TV ao vivo.
Mantidos centralização, fontes grátis, futebol brasileiro e internacional, VPN, player e pesquisa.

"""+prev)
print("patched 5.28.91")
