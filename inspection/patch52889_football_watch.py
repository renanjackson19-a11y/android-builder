from pathlib import Path
root=Path("work")

p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52888" in s and "versionName '5.28.88'" in s
s=s.replace("versionCode 52888","versionCode 52889",1).replace("versionName '5.28.88'","versionName '5.28.89'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

# Center today's date chip better on mobile.
old='''  if(tvMode)for(int i=0;i+1<chips.size();i++)linkTvHorizontal(chips.get(i),chips.get(i+1));
  LinearLayout card=new LinearLayout(this);'''
new='''  if(tvMode)for(int i=0;i+1<chips.size();i++)linkTvHorizontal(chips.get(i),chips.get(i+1));
  if(chips.size()>2&&!tvMode){datesScroll.post(()->{try{View c=chips.get(2);int x=Math.max(0,c.getLeft()-(datesScroll.getWidth()-c.getWidth())/2);datesScroll.scrollTo(x,0);}catch(Exception ignored){}});}
  LinearLayout card=new LinearLayout(this);'''
assert old in s
s=s.replace(old,new,1)

old=''' void renderFootballRows(JSONArray rows){View v=body==null?null:body.findViewWithTag("football_rows");if(!(v instanceof LinearLayout))return;LinearLayout host=(LinearLayout)v;host.removeAllViews();final int gen=++viewGen;final int[] idx={0};final Handler h=new Handler(Looper.getMainLooper());Runnable add=new Runnable(){public void run(){if(gen!=viewGen||host.getParent()==null)return;int end=Math.min(rows.length(),idx[0]+12);for(;idx[0]<end;idx[0]++){JSONObject x=rows.optJSONObject(idx[0]);if(x!=null)host.addView(footballGameRow(x),new LinearLayout.LayoutParams(-1,-2));}if(idx[0]<rows.length())h.postDelayed(this,16);}};h.post(add);}
 View footballGameRow(JSONObject x){'''
new=''' void renderFootballRows(JSONArray rows){View v=body==null?null:body.findViewWithTag("football_rows");if(!(v instanceof LinearLayout))return;LinearLayout host=(LinearLayout)v;host.removeAllViews();final int gen=++viewGen;final int[] idx={0};final Handler h=new Handler(Looper.getMainLooper());Runnable add=new Runnable(){public void run(){if(gen!=viewGen||host.getParent()==null)return;int end=Math.min(rows.length(),idx[0]+12);for(;idx[0]<end;idx[0]++){JSONObject x=rows.optJSONObject(idx[0]);if(x!=null)host.addView(footballGameRow(x),new LinearLayout.LayoutParams(-1,-2));}if(idx[0]<rows.length())h.postDelayed(this,16);}};h.post(add);}
 JSONObject bestFootballChannel(JSONArray rows,String search){
  if(rows==null||rows.length()==0)return null;String q=search==null?"":search.trim().toLowerCase(java.util.Locale.ROOT);JSONObject best=null;int bestScore=-999;
  for(int i=0;i<rows.length();i++){JSONObject x=rows.optJSONObject(i);if(x==null||!isRealLiveChannel(x))continue;String n=tvChannelName(x).toLowerCase(java.util.Locale.ROOT);int score=0;if(!q.isEmpty()){if(n.equals(q))score+=100;else if(n.startsWith(q))score+=70;else if(n.contains(q))score+=50;else continue;}if(n.contains("4k"))score+=9;else if(n.contains("fhd"))score+=8;else if(n.contains(" hd"))score+=6;else if(n.contains("sd"))score-=2;if(score>bestScore){best=x;bestScore=score;}}
  return best;
 }
 void openFootballMappedChannel(String search,boolean typed){
  if(search==null||search.trim().isEmpty()){Toast.makeText(this,"Canal deste jogo ainda não foi definido no painel.",Toast.LENGTH_LONG).show();liveContent();return;}
  JSONArray cached=filterLiveSnapshot("",search);JSONObject hit=bestFootballChannel(cached,search);if(hit!=null){openLiveAllowed(hit);return;}
  fetchAllLiveChannelPages("",search,typed,0,new JSONArray(),new java.util.HashSet<String>(),new AllPagesCB(){public void ok(JSONArray a){runOnUiThread(()->{JSONObject ch=bestFootballChannel(a,search);if(ch!=null){openLiveAllowed(ch);return;}if(!typed){openFootballMappedChannel(search,true);return;}Toast.makeText(MainActivity.this,"Canal configurado não foi encontrado neste servidor.",Toast.LENGTH_LONG).show();liveContent();});}public void err(String e){runOnUiThread(()->{if(!typed){openFootballMappedChannel(search,true);return;}Toast.makeText(MainActivity.this,"Não foi possível localizar o canal da transmissão.",Toast.LENGTH_LONG).show();liveContent();});}});
 }
 void watchFootballGame(JSONObject game){
  if(game==null||!game.optBoolean("live",false))return;if(blockVpnProtectedContent())return;
  String search=game.optString("watch_search","").trim();openFootballMappedChannel(search,false);
 }
 View footballGameRow(JSONObject x){'''
assert old in s
s=s.replace(old,new,1)

old='''  LinearLayout top=new LinearLayout(this);top.setGravity(Gravity.CENTER_VERTICAL);TextView lg=t(league.optString("name","Futebol"),11);lg.setSingleLine(true);lg.setEllipsize(android.text.TextUtils.TruncateAt.END);lg.setTextColor(0xff98aaa0);top.addView(lg,new LinearLayout.LayoutParams(0,dp(24),1));TextView st=t(live?("● "+status):(time+"  "+status),11);st.setTextColor(live?GREEN:0xffb9c4be);st.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);top.addView(st,new LinearLayout.LayoutParams(-2,dp(26)));wrap.addView(top,new LinearLayout.LayoutParams(-1,dp(24)));
  LinearLayout teams=new LinearLayout(this);teams.setGravity(Gravity.CENTER_VERTICAL);ImageView hi=new ImageView(this);hi.setScaleType(ImageView.ScaleType.FIT_CENTER);Img.loadVisible(hi,home.optString("logo",""));teams.addView(hi,new LinearLayout.LayoutParams(dp(36),dp(36)));TextView hn=t(home.optString("name",""),14);hn.setTypeface(null,1);hn.setSingleLine(true);hn.setEllipsize(android.text.TextUtils.TruncateAt.END);hn.setPadding(dp(7),0,dp(4),0);teams.addView(hn,new LinearLayout.LayoutParams(0,dp(42),1));TextView sc=t(score,15);sc.setTypeface(null,1);sc.setGravity(Gravity.CENTER);sc.setTextColor(Color.WHITE);teams.addView(sc,new LinearLayout.LayoutParams(dp(64),dp(42)));TextView an=t(away.optString("name",""),14);an.setTypeface(null,1);an.setSingleLine(true);an.setEllipsize(android.text.TextUtils.TruncateAt.END);an.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);an.setPadding(dp(4),0,dp(7),0);teams.addView(an,new LinearLayout.LayoutParams(0,dp(42),1));ImageView ai=new ImageView(this);ai.setScaleType(ImageView.ScaleType.FIT_CENTER);Img.loadVisible(ai,away.optString("logo",""));teams.addView(ai,new LinearLayout.LayoutParams(dp(36),dp(36)));wrap.addView(teams,new LinearLayout.LayoutParams(-1,dp(48)));
  String round=league.optString("round","");if(!round.isEmpty()){TextView r=t(round,10);r.setTextColor(0xff718079);r.setSingleLine(true);r.setEllipsize(android.text.TextUtils.TruncateAt.END);wrap.addView(r,new LinearLayout.LayoutParams(-1,dp(20)));}
  return wrap;'''
new='''  LinearLayout top=new LinearLayout(this);top.setGravity(Gravity.CENTER_VERTICAL);TextView lg=t(league.optString("name","Futebol"),11);lg.setSingleLine(true);lg.setEllipsize(android.text.TextUtils.TruncateAt.END);lg.setTextColor(0xff98aaa0);top.addView(lg,new LinearLayout.LayoutParams(0,dp(28),1));TextView st=t(live?("● "+status):(time+"  "+status),11);st.setTextColor(live?GREEN:0xffb9c4be);st.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);top.addView(st,new LinearLayout.LayoutParams(-2,dp(28)));wrap.addView(top,new LinearLayout.LayoutParams(-1,dp(28)));
  LinearLayout teams=new LinearLayout(this);teams.setGravity(Gravity.CENTER_VERTICAL);ImageView hi=new ImageView(this);hi.setScaleType(ImageView.ScaleType.FIT_CENTER);String hl=home.optString("logo","");if(!hl.isEmpty())Img.loadVisible(hi,hl);teams.addView(hi,new LinearLayout.LayoutParams(dp(34),dp(34)));TextView hn=t(home.optString("name",""),13);hn.setTypeface(null,1);hn.setMaxLines(2);hn.setEllipsize(android.text.TextUtils.TruncateAt.END);hn.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);hn.setPadding(dp(7),0,dp(4),0);teams.addView(hn,new LinearLayout.LayoutParams(0,dp(54),1));TextView sc=t(score,15);sc.setTypeface(null,1);sc.setGravity(Gravity.CENTER);sc.setTextColor(Color.WHITE);teams.addView(sc,new LinearLayout.LayoutParams(dp(58),dp(54)));TextView an=t(away.optString("name",""),13);an.setTypeface(null,1);an.setMaxLines(2);an.setEllipsize(android.text.TextUtils.TruncateAt.END);an.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);an.setPadding(dp(4),0,dp(7),0);teams.addView(an,new LinearLayout.LayoutParams(0,dp(54),1));ImageView ai=new ImageView(this);ai.setScaleType(ImageView.ScaleType.FIT_CENTER);String al=away.optString("logo","");if(!al.isEmpty())Img.loadVisible(ai,al);teams.addView(ai,new LinearLayout.LayoutParams(dp(34),dp(34)));wrap.addView(teams,new LinearLayout.LayoutParams(-1,dp(58)));
  String round=league.optString("round","");if(!round.isEmpty()){TextView r=t(round,10);r.setTextColor(0xff718079);r.setSingleLine(true);r.setEllipsize(android.text.TextUtils.TruncateAt.END);wrap.addView(r,new LinearLayout.LayoutParams(-1,dp(20)));}
  if(live){
   TextView watch=t("▶  ASSISTIR",13);watch.setTypeface(null,1);watch.setTextColor(0xff07150d);watch.setGravity(Gravity.CENTER);watch.setFocusable(tvMode);GradientDrawable wb=round(GREEN,13);watch.setBackground(wb);watch.setContentDescription("Assistir jogo ao vivo");watch.setOnClickListener(v->watchFootballGame(x));if(tvMode)armTvFocus(watch);LinearLayout.LayoutParams wlp=new LinearLayout.LayoutParams(-1,dp(42));wlp.setMargins(0,dp(6),0,0);wrap.addView(watch,wlp);
  }
  return wrap;'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.89 — Futebol ao vivo com botão Assistir
Jogos ao vivo agora exibem botão ASSISTIR.
Quando o canal é vinculado no Painel > API de Futebol, o app procura esse canal no servidor atual e abre a transmissão diretamente.
Se o canal ainda não estiver vinculado ou não existir na fonte atual, o app abre a área de TV para seleção manual.
A tela de jogos ganhou nomes de times em até duas linhas, liga com mais espaço e data de hoje centralizada.
Mantidas pesquisa completa, barra inferior adaptativa, VPN, player e conjugação.

"""+prior)
print("patched 5.28.89")
