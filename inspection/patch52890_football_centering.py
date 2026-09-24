from pathlib import Path
root=Path("work")

p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52889" in s and "versionName '5.28.89'" in s
s=s.replace("versionCode 52889","versionCode 52890",1).replace("versionName '5.28.89'","versionName '5.28.90'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

old=''' String footballDayKey(java.util.Calendar c){return new java.text.SimpleDateFormat("yyyy-MM-dd",java.util.Locale.US).format(c.getTime());}
 String footballDayLabel(java.util.Calendar c,int offset){String head=offset==0?"HOJE":(offset==-1?"ONTEM":(offset==1?"AMANHÃ":new java.text.SimpleDateFormat("EEE",java.util.Locale.getDefault()).format(c.getTime()).toUpperCase(java.util.Locale.getDefault())));String date=new java.text.SimpleDateFormat("dd/MM",java.util.Locale.getDefault()).format(c.getTime());return head+"\\n"+date;}
 void footballTablePage(){'''
new=''' String footballDayKey(java.util.Calendar c){return new java.text.SimpleDateFormat("yyyy-MM-dd",java.util.Locale.US).format(c.getTime());}
 String footballDayLabel(java.util.Calendar c,int offset){String head=offset==0?"HOJE":(offset==-1?"ONTEM":(offset==1?"AMANHÃ":new java.text.SimpleDateFormat("EEE",java.util.Locale.getDefault()).format(c.getTime()).toUpperCase(java.util.Locale.getDefault())));String date=new java.text.SimpleDateFormat("dd/MM",java.util.Locale.getDefault()).format(c.getTime());return head+"\\n"+date;}
 void centerFootballDateChip(HorizontalScrollView scroll,View chip,boolean smooth){
  if(scroll==null||chip==null)return;
  scroll.post(()->{try{int x=Math.max(0,chip.getLeft()-(scroll.getWidth()-chip.getWidth())/2);if(smooth)scroll.smoothScrollTo(x,0);else scroll.scrollTo(x,0);}catch(Exception ignored){}});
 }
 void footballTablePage(){'''
assert old in s
s=s.replace(old,new,1)

old='''  LinearLayout heading=new LinearLayout(this);heading.setOrientation(LinearLayout.VERTICAL);TextView title=t("Jogos",tvMode?30:25);title.setTypeface(null,1);title.setTextColor(Color.WHITE);title.setPadding(0,0,0,0);heading.addView(title,new LinearLayout.LayoutParams(-1,dp(40)));TextView sub=t("Futebol ao vivo e próximos jogos",14);sub.setTextColor(0xff9ca9a2);sub.setPadding(0,0,0,0);heading.addView(sub,new LinearLayout.LayoutParams(-1,dp(26)));body.addView(heading,new LinearLayout.LayoutParams(-1,dp(70)));'''
new='''  LinearLayout heading=new LinearLayout(this);heading.setOrientation(LinearLayout.VERTICAL);heading.setGravity(Gravity.CENTER_HORIZONTAL);TextView title=t("Jogos",tvMode?30:25);title.setTypeface(null,1);title.setTextColor(Color.WHITE);title.setGravity(Gravity.CENTER);title.setPadding(0,0,0,0);heading.addView(title,new LinearLayout.LayoutParams(-1,dp(40)));TextView sub=t("Futebol ao vivo e próximos jogos",14);sub.setTextColor(0xff9ca9a2);sub.setGravity(Gravity.CENTER);sub.setPadding(0,0,0,0);heading.addView(sub,new LinearLayout.LayoutParams(-1,dp(26)));body.addView(heading,new LinearLayout.LayoutParams(-1,dp(70)));'''
assert old in s
s=s.replace(old,new,1)

old='''  HorizontalScrollView datesScroll=new HorizontalScrollView(this);datesScroll.setHorizontalScrollBarEnabled(false);datesScroll.setOverScrollMode(View.OVER_SCROLL_NEVER);LinearLayout dates=new LinearLayout(this);dates.setOrientation(LinearLayout.HORIZONTAL);dates.setGravity(Gravity.CENTER_VERTICAL);datesScroll.addView(dates,new HorizontalScrollView.LayoutParams(-2,-1));body.addView(datesScroll,new LinearLayout.LayoutParams(-1,dp(66)));'''
new='''  HorizontalScrollView datesScroll=new HorizontalScrollView(this);datesScroll.setHorizontalScrollBarEnabled(false);datesScroll.setOverScrollMode(View.OVER_SCROLL_NEVER);datesScroll.setFillViewport(false);LinearLayout dates=new LinearLayout(this);dates.setOrientation(LinearLayout.HORIZONTAL);dates.setGravity(Gravity.CENTER_VERTICAL);dates.setClipToPadding(false);datesScroll.addView(dates,new HorizontalScrollView.LayoutParams(-2,-1));body.addView(datesScroll,new LinearLayout.LayoutParams(-1,dp(66)));'''
assert old in s
s=s.replace(old,new,1)

old='''chip.setOnClickListener(v->{for(int i=0;i<chips.size();i++){TextView c=chips.get(i);boolean on=i==selected;GradientDrawable g=round(on?0xff123c28:0xff111a16,14);g.setStroke(dp(on?2:1),on?GREEN:0xff2e493a);c.setBackground(g);c.setTextColor(on?GREEN:0xffd9e0dc);}loadFootballDate(String.valueOf(v.getTag()));});}'''
new='''chip.setOnClickListener(v->{for(int i=0;i<chips.size();i++){TextView c=chips.get(i);boolean on=i==selected;GradientDrawable g=round(on?0xff123c28:0xff111a16,14);g.setStroke(dp(on?2:1),on?GREEN:0xff2e493a);c.setBackground(g);c.setTextColor(on?GREEN:0xffd9e0dc);}if(!tvMode)centerFootballDateChip(datesScroll,v,true);loadFootballDate(String.valueOf(v.getTag()));});}'''
assert old in s
s=s.replace(old,new,1)

old='''  if(tvMode)for(int i=0;i+1<chips.size();i++)linkTvHorizontal(chips.get(i),chips.get(i+1));
  if(chips.size()>2&&!tvMode){datesScroll.post(()->{try{View c=chips.get(2);int x=Math.max(0,c.getLeft()-(datesScroll.getWidth()-c.getWidth())/2);datesScroll.scrollTo(x,0);}catch(Exception ignored){}});}
  LinearLayout card=new LinearLayout(this);'''
new='''  if(tvMode)for(int i=0;i+1<chips.size();i++)linkTvHorizontal(chips.get(i),chips.get(i+1));
  if(chips.size()>2&&!tvMode){
   datesScroll.post(()->{try{int side=Math.max(0,(datesScroll.getWidth()-chips.get(2).getWidth())/2);dates.setPadding(side,0,side,0);dates.requestLayout();centerFootballDateChip(datesScroll,chips.get(2),false);}catch(Exception ignored){}});
  }
  LinearLayout card=new LinearLayout(this);'''
assert old in s
s=s.replace(old,new,1)

old='''  TextView listTitle=t("Jogos",20);listTitle.setTypeface(null,1);listTitle.setPadding(0,0,0,dp(6));card.addView(listTitle,new LinearLayout.LayoutParams(-1,dp(36)));'''
new='''  TextView listTitle=t("Jogos",20);listTitle.setTypeface(null,1);listTitle.setGravity(Gravity.CENTER);listTitle.setPadding(0,0,0,dp(6));card.addView(listTitle,new LinearLayout.LayoutParams(-1,dp(36)));'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.90 — Futebol centralizado + múltiplas APIs no painel
Tela Jogos com título e subtítulo centralizados.
O seletor de datas agora centraliza exatamente a opção escolhida, inclusive ao trocar entre ontem/hoje/amanhã.
A faixa de datas ganhou margens internas simétricas para funcionar em larguras diferentes de celular.
O título interno Jogos também foi centralizado.
O painel passou a aceitar API-Football/API-Sports, Footballdata.io e API Futebol Brasileiro self-hosted.
Mantidos botão Assistir ao vivo, VPN, player, pesquisa e demais recursos da 5.28.89.

"""+prior)
print("patched 5.28.90")
