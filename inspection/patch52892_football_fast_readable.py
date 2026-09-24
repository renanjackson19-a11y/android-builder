from pathlib import Path
root=Path("work")

p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52891" in s and "versionName '5.28.91'" in s
s=s.replace("versionCode 52891","versionCode 52892",1).replace("versionName '5.28.91'","versionName '5.28.92'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

# Small in-memory football cache: revisiting Today/Tomorrow is instant.
needle='''final java.util.HashMap<String,String[]> tvEpgCache=new java.util.HashMap<>(); final java.util.HashMap<String,Long> tvEpgCacheAt=new java.util.HashMap<>(); static final long TV_EPG_CACHE_MS=50000L;'''
repl='''final java.util.HashMap<String,String[]> tvEpgCache=new java.util.HashMap<>(); final java.util.HashMap<String,Long> tvEpgCacheAt=new java.util.HashMap<>(); static final long TV_EPG_CACHE_MS=50000L;
 final java.util.HashMap<String,JSONArray> footballDayCache=new java.util.HashMap<>(); final java.util.HashMap<String,Long> footballDayCacheAt=new java.util.HashMap<>(); int footballLoadToken=0; static final long FOOTBALL_DAY_CACHE_MS=60000L;'''
assert needle in s
s=s.replace(needle,repl,1)

old=''' void loadFootballDate(String date){renderFootballLoading();Api.post("football",Api.m("date",date),new Api.CB(){public void ok(JSONObject j){if(body==null)return;JSONArray a=j.optJSONArray("result");if(j.optInt("status",200)!=200||a==null||a.length()==0){renderFootballEmptyState();return;}renderFootballRows(a);}public void err(String e){View v=body==null?null:body.findViewWithTag("football_rows");if(!(v instanceof LinearLayout))return;LinearLayout host=(LinearLayout)v;host.removeAllViews();TextView msg=t("Não foi possível carregar os jogos agora.",15);msg.setGravity(Gravity.CENTER);msg.setTextColor(0xffffb4ab);host.addView(msg,new LinearLayout.LayoutParams(-1,dp(54)));TextView sub=t("Tente novamente em alguns instantes.",12);sub.setGravity(Gravity.CENTER);sub.setTextColor(0xff8f9c95);host.addView(sub,new LinearLayout.LayoutParams(-1,dp(34)));}});}'''
new=''' String footballCacheKey(String date){return (Api.PROVIDER==null?"":Api.PROVIDER)+"|"+(date==null?"":date);}
 void loadFootballDate(String date){
  final int token=++footballLoadToken;final String key=footballCacheKey(date);final boolean hadCache=footballDayCache.containsKey(key);JSONArray cached=footballDayCache.get(key);Long cachedAt=footballDayCacheAt.get(key);
  if(hadCache){if(cached==null||cached.length()==0)renderFootballEmptyState();else renderFootballRows(cached);}else renderFootballLoading();
  if(hadCache&&cachedAt!=null&&System.currentTimeMillis()-cachedAt<FOOTBALL_DAY_CACHE_MS)return;
  Api.post("football",Api.m("date",date),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");if(a==null)a=new JSONArray();footballDayCache.put(key,a);footballDayCacheAt.put(key,System.currentTimeMillis());if(token!=footballLoadToken||body==null)return;if(j.optInt("status",200)!=200||a.length()==0){renderFootballEmptyState();return;}renderFootballRows(a);}public void err(String e){if(token!=footballLoadToken||body==null||hadCache)return;View v=body.findViewWithTag("football_rows");if(!(v instanceof LinearLayout))return;LinearLayout host=(LinearLayout)v;host.removeAllViews();TextView msg=t("Não foi possível carregar os jogos agora.",15);msg.setGravity(Gravity.CENTER);msg.setTextColor(0xffffb4ab);host.addView(msg,new LinearLayout.LayoutParams(-1,dp(54)));TextView sub=t("Tente novamente em alguns instantes.",12);sub.setGravity(Gravity.CENTER);sub.setTextColor(0xff8f9c95);host.addView(sub,new LinearLayout.LayoutParams(-1,dp(34)));}});}
 '''
assert old in s
s=s.replace(old,new,1)

old='''  String broadcaster=footballBroadcastText(x);String mapped=x.optString("watch_search","").trim();
  if(!broadcaster.isEmpty()){TextView bt=t("Onde assistir: "+broadcaster,11);bt.setTextColor(0xffaab8b0);bt.setMaxLines(2);bt.setEllipsize(android.text.TextUtils.TruncateAt.END);bt.setPadding(0,dp(3),0,0);wrap.addView(bt,new LinearLayout.LayoutParams(-1,-2));}
  if(!mapped.isEmpty()){TextView mt=t("GreenPlay: "+mapped,11);mt.setTextColor(GREEN);mt.setTypeface(null,1);mt.setSingleLine(true);mt.setEllipsize(android.text.TextUtils.TruncateAt.END);mt.setPadding(0,dp(3),0,0);wrap.addView(mt,new LinearLayout.LayoutParams(-1,dp(24)));}
  if(live){'''
new='''  String broadcaster=footballBroadcastText(x);String mapped=x.optString("watch_search","").trim();String watchServer=x.optString("watch_server_name","Seu servidor").trim();if(watchServer.isEmpty())watchServer="Seu servidor";
  if(!broadcaster.isEmpty()||!mapped.isEmpty()){
   LinearLayout info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(10),dp(8),dp(10),dp(8));GradientDrawable ib=round(0xff0b2116,11);ib.setStroke(dp(1),!mapped.isEmpty()?0xff2b7148:0xff294236);info.setBackground(ib);
   LinearLayout.LayoutParams ilp=new LinearLayout.LayoutParams(-1,-2);ilp.setMargins(0,dp(6),0,dp(2));
   if(!broadcaster.isEmpty()){
    TextView bl=t("ONDE ASSISTIR",10);bl.setTypeface(null,1);bl.setTextColor(0xff8fc8a6);bl.setLetterSpacing(.04f);info.addView(bl,new LinearLayout.LayoutParams(-1,-2));
    TextView bv=t(broadcaster,14);bv.setTypeface(null,1);bv.setTextColor(Color.WHITE);bv.setMaxLines(3);bv.setPadding(0,dp(2),0,0);info.addView(bv,new LinearLayout.LayoutParams(-1,-2));
   }
   if(!mapped.isEmpty()){
    TextView ml=t("NO GREENPLAY • "+watchServer.toUpperCase(java.util.Locale.getDefault()),10);ml.setTypeface(null,1);ml.setTextColor(GREEN);ml.setPadding(0,broadcaster.isEmpty()?0:dp(7),0,0);info.addView(ml,new LinearLayout.LayoutParams(-1,-2));
    TextView mv=t(mapped,14);mv.setTypeface(null,1);mv.setTextColor(0xffe8fff0);mv.setMaxLines(2);mv.setPadding(0,dp(2),0,0);info.addView(mv,new LinearLayout.LayoutParams(-1,-2));
   }else if(!broadcaster.isEmpty()){
    TextView wait=t("Canal correspondente ainda não apareceu neste servidor.",11);wait.setTextColor(0xffffc66d);wait.setPadding(0,dp(7),0,0);wait.setMaxLines(2);info.addView(wait,new LinearLayout.LayoutParams(-1,-2));
   }
   wrap.addView(info,ilp);
  }
  if(live){'''
assert old in s
s=s.replace(old,new,1)

# Keep the live button comfortably separated from the information box.
old='''LinearLayout.LayoutParams wlp=new LinearLayout.LayoutParams(-1,dp(42));wlp.setMargins(0,dp(7),0,0);wrap.addView(watch,wlp);'''
new='''LinearLayout.LayoutParams wlp=new LinearLayout.LayoutParams(-1,dp(44));wlp.setMargins(0,dp(9),0,0);wrap.addView(watch,wlp);'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.92 — Futebol mais legível e carregamento rápido
Bloco de transmissão redesenhado nos cards: emissora e canal GreenPlay agora ficam grandes, em área própria e sem texto cortado.
Mostra o servidor atual junto do canal vinculado automaticamente.
Cache de 60 segundos por data/servidor: voltar para Hoje, Amanhã ou Ontem fica instantâneo.
Respostas antigas são ignoradas ao trocar datas rapidamente.
Botão Assistir continua aparecendo somente quando a partida estiver ao vivo.
Mantidos vínculo automático por fonte, reprodução direta do provedor, VPN, pesquisa e demais recursos da 5.28.91.

"""+prior)
print("patched 5.28.92")
