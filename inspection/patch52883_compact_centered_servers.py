from pathlib import Path
root=Path("work")

p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52882" in s and "versionName '5.28.82'" in s
s=s.replace("versionCode 52882","versionCode 52883",1).replace("versionName '5.28.82'","versionName '5.28.83'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

# --- Cabeçalho: mais compacto e realmente centralizado ---
old='''  root.setPadding(dp(14),standardPageTopPx(),dp(14),dp(8));

  // Barra fixa: o botão voltar nunca participa da rolagem da lista.
  LinearLayout top=new LinearLayout(this);
  top.setGravity(Gravity.CENTER_VERTICAL);
  top.setPadding(0,dp(2),0,dp(4));
  TextView back=t("‹",34);
  back.setGravity(Gravity.CENTER);
  back.setTextColor(canReturn?Color.WHITE:0x00ffffff);
  back.setFocusable(canReturn);
  back.setClickable(canReturn);
  back.setContentDescription("Voltar");
  if(canReturn){
   GradientDrawable bbg=round(0x99131d18,21);bbg.setStroke(dp(1),0xff315344);back.setBackground(bbg);
   back.setOnClickListener(v->cancelProviderSwitch());
   if(tvMode)armTvFocus(back);
  }
  LinearLayout.LayoutParams backLp=new LinearLayout.LayoutParams(dp(46),dp(46));backLp.setMargins(0,dp(2),0,0);top.addView(back,backLp);

  LinearLayout headerBox=new LinearLayout(this);headerBox.setOrientation(LinearLayout.VERTICAL);headerBox.setGravity(Gravity.CENTER);
  TextView header=t("Servidores",19);header.setTypeface(null,1);header.setGravity(Gravity.CENTER);header.setIncludeFontPadding(true);header.setPadding(0,dp(2),0,0);
  TextView headerSub=t("Escolha onde deseja conectar",9);headerSub.setTextColor(0xff8fa099);headerSub.setGravity(Gravity.CENTER);headerSub.setIncludeFontPadding(true);
  LinearLayout.LayoutParams hp1=new LinearLayout.LayoutParams(-1,-2);LinearLayout.LayoutParams hp2=new LinearLayout.LayoutParams(-1,-2);hp2.setMargins(0,-dp(1),0,0);
  headerBox.addView(header,hp1);headerBox.addView(headerSub,hp2);
  top.addView(headerBox,new LinearLayout.LayoutParams(0,dp(52),1));

  View spacer=new View(this);
  top.addView(spacer,new LinearLayout.LayoutParams(dp(44),dp(48)));
  root.addView(top,new LinearLayout.LayoutParams(-1,dp(58)));'''
new='''  root.setPadding(dp(12),standardPageTopPx(),dp(12),dp(6));

  // Cabeçalho fixo e compacto. O título fica no centro geométrico da tela.
  LinearLayout top=new LinearLayout(this);
  top.setGravity(Gravity.CENTER_VERTICAL);
  top.setPadding(0,0,0,dp(2));

  TextView back=t("‹",31);
  back.setGravity(Gravity.CENTER);
  back.setTextColor(canReturn?Color.WHITE:0x00ffffff);
  back.setFocusable(canReturn);
  back.setClickable(canReturn);
  back.setContentDescription("Voltar");
  if(canReturn){
   GradientDrawable bbg=round(0x85131d18,18);bbg.setStroke(dp(1),0xff2b493b);back.setBackground(bbg);
   back.setOnClickListener(v->cancelProviderSwitch());
   if(tvMode)armTvFocus(back);
  }
  top.addView(back,new LinearLayout.LayoutParams(dp(40),dp(40)));

  TextView header=t("Servidores",19);
  header.setTypeface(null,1);header.setGravity(Gravity.CENTER);header.setIncludeFontPadding(true);
  top.addView(header,new LinearLayout.LayoutParams(0,dp(42),1));

  View spacer=new View(this);
  top.addView(spacer,new LinearLayout.LayoutParams(dp(40),dp(40)));
  root.addView(top,new LinearLayout.LayoutParams(-1,dp(44)));'''
assert old in s
s=s.replace(old,new,1)

# --- Intro: centralizado, sem ocupar uma faixa larga ---
old='''  LinearLayout intro=new LinearLayout(this);intro.setOrientation(LinearLayout.HORIZONTAL);intro.setGravity(Gravity.CENTER_VERTICAL);intro.setPadding(dp(4),dp(8),dp(4),dp(14));
  ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);applyAppLogo(logo);intro.addView(logo,new LinearLayout.LayoutParams(dp(tvMode?54:46),dp(tvMode?42:36)));
  LinearLayout introText=new LinearLayout(this);introText.setOrientation(LinearLayout.VERTICAL);introText.setPadding(dp(12),0,0,0);
  TextView title=t("Selecione um servidor",17);title.setTypeface(null,1);title.setTextColor(Color.WHITE);title.setIncludeFontPadding(true);introText.addView(title,new LinearLayout.LayoutParams(-1,-2));
  TextView sub=t("Seu conteúdo fica organizado por fonte",10);sub.setTextColor(0xff86978e);sub.setIncludeFontPadding(true);LinearLayout.LayoutParams slp=new LinearLayout.LayoutParams(-1,-2);slp.setMargins(0,dp(3),0,0);introText.addView(sub,slp);
  intro.addView(introText,new LinearLayout.LayoutParams(0,-2,1));wrap.addView(intro,new LinearLayout.LayoutParams(-1,-2));'''
new='''  LinearLayout intro=new LinearLayout(this);intro.setOrientation(LinearLayout.VERTICAL);intro.setGravity(Gravity.CENTER_HORIZONTAL);intro.setPadding(0,dp(4),0,dp(10));

  LinearLayout introMain=new LinearLayout(this);introMain.setOrientation(LinearLayout.HORIZONTAL);introMain.setGravity(Gravity.CENTER_VERTICAL);
  ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);applyAppLogo(logo);
  introMain.addView(logo,new LinearLayout.LayoutParams(dp(tvMode?48:42),dp(tvMode?38:32)));
  TextView title=t("Selecione um servidor",17);title.setTypeface(null,1);title.setTextColor(Color.WHITE);title.setGravity(Gravity.CENTER_VERTICAL);title.setIncludeFontPadding(true);
  LinearLayout.LayoutParams titleLp=new LinearLayout.LayoutParams(-2,-2);titleLp.setMargins(dp(9),0,0,0);introMain.addView(title,titleLp);
  intro.addView(introMain,new LinearLayout.LayoutParams(-2,-2));

  TextView sub=t("Escolha a fonte que deseja usar",10);sub.setTextColor(0xff86978e);sub.setGravity(Gravity.CENTER);sub.setIncludeFontPadding(true);
  LinearLayout.LayoutParams slp=new LinearLayout.LayoutParams(-2,-2);slp.setMargins(0,dp(3),0,0);intro.addView(sub,slp);
  wrap.addView(intro,new LinearLayout.LayoutParams(-1,-2));'''
assert old in s
s=s.replace(old,new,1)

# Menos vazio antes/depois da lista.
s=s.replace('screen.setPadding(0,0,0,dp(28));','screen.setPadding(0,0,0,dp(16));',1)
s=s.replace('wrap.setPadding(providerSide,dp(2),providerSide,dp(18));','wrap.setPadding(providerSide,0,providerSide,dp(10));',1)
s=s.replace('list.setPadding(dp(2),0,dp(2),dp(18));','list.setPadding(dp(2),0,dp(2),dp(10));',1)

# --- Cards: duas linhas visíveis, mais compactos e sem recorte ---
old='''  LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER_VERTICAL);card.setPadding(dp(13),dp(9),dp(11),dp(9));GradientDrawable bg=round(active?0xf013211a:0xf0101713,18);bg.setStroke(dp(1),active?0xff35db78:0xff25372f);card.setBackground(bg);if(Build.VERSION.SDK_INT>=21)card.setElevation(dp(active?4:1));
  ImageView icon=new ImageView(this);icon.setImageResource(R.drawable.ic_server);icon.setScaleType(ImageView.ScaleType.CENTER_INSIDE);icon.setPadding(dp(11),dp(11),dp(11),dp(11));if(Build.VERSION.SDK_INT>=21)icon.setImageTintList(android.content.res.ColorStateList.valueOf(active?GREEN:0xff6fd095));GradientDrawable ig=round(active?0xff143a27:0xff102219,13);ig.setStroke(dp(1),active?0xff34e77d:0xff28523e);icon.setBackground(ig);LinearLayout.LayoutParams iLp=new LinearLayout.LayoutParams(dp(46),dp(46));iLp.setMargins(0,0,dp(12),0);card.addView(icon,iLp);'''
new='''  LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER_VERTICAL);card.setPadding(dp(12),dp(7),dp(10),dp(7));GradientDrawable bg=round(active?0xf013211a:0xf0101713,17);bg.setStroke(dp(1),active?0xff35db78:0xff25372f);card.setBackground(bg);if(Build.VERSION.SDK_INT>=21)card.setElevation(dp(active?3:1));
  ImageView icon=new ImageView(this);icon.setImageResource(R.drawable.ic_server);icon.setScaleType(ImageView.ScaleType.CENTER_INSIDE);icon.setPadding(dp(10),dp(10),dp(10),dp(10));if(Build.VERSION.SDK_INT>=21)icon.setImageTintList(android.content.res.ColorStateList.valueOf(active?GREEN:0xff6fd095));GradientDrawable ig=round(active?0xff143a27:0xff102219,12);ig.setStroke(dp(1),active?0xff34e77d:0xff28523e);icon.setBackground(ig);LinearLayout.LayoutParams iLp=new LinearLayout.LayoutParams(dp(42),dp(42));iLp.setMargins(0,0,dp(11),0);card.addView(icon,iLp);'''
assert old in s
s=s.replace(old,new,1)

old='''  LinearLayout nameRow=new LinearLayout(this);nameRow.setGravity(Gravity.CENTER_VERTICAL);nameRow.setMinimumHeight(dp(28));
  TextView n=t(name,16);n.setTypeface(null,1);n.setTextColor(Color.WHITE);n.setIncludeFontPadding(true);n.setGravity(Gravity.CENTER_VERTICAL);n.setMaxLines(1);n.setEllipsize(android.text.TextUtils.TruncateAt.END);nameRow.addView(n,new LinearLayout.LayoutParams(0,-2,1));
  if(active){TextView activeLabel=t("ATIVO",9);activeLabel.setTextColor(GREEN);activeLabel.setTypeface(null,1);activeLabel.setGravity(Gravity.CENTER);activeLabel.setIncludeFontPadding(true);activeLabel.setPadding(dp(8),0,dp(8),0);GradientDrawable ag=round(0xff10261a,10);ag.setStroke(dp(1),0xff2c6d49);activeLabel.setBackground(ag);LinearLayout.LayoutParams ap=new LinearLayout.LayoutParams(-2,dp(22));ap.setMargins(dp(8),0,0,0);nameRow.addView(activeLabel,ap);}
  mid.addView(nameRow,new LinearLayout.LayoutParams(-1,-2));

  TextView contentLine=t(providerContentLabel(hasMovies,hasSeries,hasLive),11);
  contentLine.setTextColor(0xff9aa8a0);contentLine.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);contentLine.setIncludeFontPadding(true);contentLine.setMaxLines(1);contentLine.setEllipsize(android.text.TextUtils.TruncateAt.END);
  LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(-1,-2);clp.setMargins(0,dp(5),0,0);mid.addView(contentLine,clp);
  card.addView(mid,new LinearLayout.LayoutParams(0,-2,1));'''
new='''  LinearLayout nameRow=new LinearLayout(this);nameRow.setGravity(Gravity.CENTER_VERTICAL);
  TextView n=t(name,16);n.setTypeface(null,1);n.setTextColor(Color.WHITE);n.setIncludeFontPadding(true);n.setGravity(Gravity.CENTER_VERTICAL);n.setMaxLines(1);n.setEllipsize(android.text.TextUtils.TruncateAt.END);nameRow.addView(n,new LinearLayout.LayoutParams(0,-2,1));
  if(active){TextView activeLabel=t("ATIVO",8);activeLabel.setTextColor(GREEN);activeLabel.setTypeface(null,1);activeLabel.setGravity(Gravity.CENTER);activeLabel.setIncludeFontPadding(true);activeLabel.setPadding(dp(7),0,dp(7),0);GradientDrawable ag=round(0xff10261a,9);ag.setStroke(dp(1),0xff2c6d49);activeLabel.setBackground(ag);LinearLayout.LayoutParams ap=new LinearLayout.LayoutParams(-2,dp(20));ap.setMargins(dp(7),0,0,0);nameRow.addView(activeLabel,ap);}
  mid.addView(nameRow,new LinearLayout.LayoutParams(-1,-2));

  TextView contentLine=t(providerContentLabel(hasMovies,hasSeries,hasLive),11);
  contentLine.setTextColor(0xffa4afa9);contentLine.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);contentLine.setIncludeFontPadding(true);contentLine.setSingleLine(true);contentLine.setEllipsize(android.text.TextUtils.TruncateAt.END);
  LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(-1,dp(20));clp.setMargins(0,dp(1),0,0);mid.addView(contentLine,clp);
  card.addView(mid,new LinearLayout.LayoutParams(0,-2,1));'''
assert old in s
s=s.replace(old,new,1)

# Garante espaço real para as duas linhas, sem voltar aos cards altos.
old='''  card.setOnClickListener(v->connectProviderReady(id,name,providerMovies,providerSeries,providerLive,card,ar));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(74));lp.setMargins(0,0,0,dp(9));host.addView(card,lp);'''
new='''  card.setOnClickListener(v->connectProviderReady(id,name,providerMovies,providerSeries,providerLive,card,ar));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(72));lp.setMargins(0,0,0,dp(8));host.addView(card,lp);'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.83 — Servidores compactos e centralizados
Cabeçalho reduzido: botão Voltar menor e título Servidores centralizado de verdade.
Bloco “Selecione um servidor” agora é um conjunto compacto e centralizado, sem ocupar faixa larga.
Reduzidos os espaços de cima/baixo da tela e dos cards.
Restaurada e garantida a identificação abaixo do nome: Filmes • Séries • TV ao vivo (conforme cada fonte).
Cards menores sem cortar a segunda linha.
Selo ATIVO reduzido e discreto.
Mantidos VPN, conjugação de fontes, carregamento de canais e player.

"""+prior)
print("patched 5.28.83")
