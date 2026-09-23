from pathlib import Path
root=Path("work")

p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52883" in s and "versionName '5.28.83'" in s
s=s.replace("versionCode 52883","versionCode 52884",1).replace("versionName '5.28.83'","versionName '5.28.84'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

# 1) Safe area real: nunca deixar o botão Voltar invadir a barra de status/horário.
old='''  root.setPadding(dp(12),standardPageTopPx(),dp(12),dp(6));'''
new='''  int providerSafeTop=Math.max(standardPageTopPx(),statusBarHeightPx()+dp(8));
  root.setPadding(dp(12),providerSafeTop,dp(12),dp(6));'''
assert old in s
s=s.replace(old,new,1)

# 2) Botão Voltar menor e com respiro; título continua central.
old='''  TextView back=t("‹",31);
  back.setGravity(Gravity.CENTER);'''
new='''  TextView back=t("‹",28);
  back.setGravity(Gravity.CENTER);'''
assert old in s
s=s.replace(old,new,1)

old='''   GradientDrawable bbg=round(0x85131d18,18);bbg.setStroke(dp(1),0xff2b493b);back.setBackground(bbg);'''
new='''   GradientDrawable bbg=round(0x85131d18,16);bbg.setStroke(dp(1),0xff2b493b);back.setBackground(bbg);'''
assert old in s
s=s.replace(old,new,1)

old='''  top.addView(back,new LinearLayout.LayoutParams(dp(40),dp(40)));'''
new='''  LinearLayout.LayoutParams backLp=new LinearLayout.LayoutParams(dp(36),dp(36));backLp.setMargins(0,dp(2),0,0);top.addView(back,backLp);'''
assert old in s
s=s.replace(old,new,1)

old='''  top.addView(header,new LinearLayout.LayoutParams(0,dp(42),1));

  View spacer=new View(this);
  top.addView(spacer,new LinearLayout.LayoutParams(dp(40),dp(40)));
  root.addView(top,new LinearLayout.LayoutParams(-1,dp(44)));'''
new='''  top.addView(header,new LinearLayout.LayoutParams(0,dp(40),1));

  View spacer=new View(this);
  top.addView(spacer,new LinearLayout.LayoutParams(dp(36),dp(36)));
  root.addView(top,new LinearLayout.LayoutParams(-1,dp(42)));'''
assert old in s
s=s.replace(old,new,1)

# 3) A identificação Filmes/Séries/TV precisa de altura real e não pode ser cortada.
old='''  LinearLayout mid=new LinearLayout(this);mid.setOrientation(LinearLayout.VERTICAL);mid.setGravity(Gravity.CENTER_VERTICAL);mid.setPadding(0,0,dp(6),0);'''
new='''  LinearLayout mid=new LinearLayout(this);mid.setOrientation(LinearLayout.VERTICAL);mid.setGravity(Gravity.CENTER_VERTICAL);mid.setPadding(0,dp(2),dp(6),dp(2));mid.setMinimumHeight(dp(50));'''
assert old in s
s=s.replace(old,new,1)

old='''  TextView contentLine=t(providerContentLabel(hasMovies,hasSeries,hasLive),11);
  contentLine.setTextColor(0xffa4afa9);contentLine.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);contentLine.setIncludeFontPadding(true);contentLine.setSingleLine(true);contentLine.setEllipsize(android.text.TextUtils.TruncateAt.END);
  LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(-1,dp(20));clp.setMargins(0,dp(1),0,0);mid.addView(contentLine,clp);'''
new='''  TextView contentLine=t(providerContentLabel(hasMovies,hasSeries,hasLive),11);
  contentLine.setTextColor(0xffaab5af);contentLine.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);contentLine.setIncludeFontPadding(true);contentLine.setSingleLine(true);contentLine.setEllipsize(android.text.TextUtils.TruncateAt.END);contentLine.setPadding(0,dp(1),0,dp(1));
  LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(-1,-2);clp.setMargins(0,dp(2),0,0);mid.addView(contentLine,clp);'''
assert old in s
s=s.replace(old,new,1)

# 4) O card precisa comportar as duas linhas de texto sem clipar.
old='''  card.setOnClickListener(v->connectProviderReady(id,name,providerMovies,providerSeries,providerLive,card,ar));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(72));lp.setMargins(0,0,0,dp(8));host.addView(card,lp);'''
new='''  card.setOnClickListener(v->connectProviderReady(id,name,providerMovies,providerSeries,providerLive,card,ar));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(84));lp.setMargins(0,0,0,dp(8));host.addView(card,lp);'''
assert old in s
s=s.replace(old,new,1)

# 5) Ícone continua compacto, mas alinha com duas linhas.
old='''  ImageView icon=new ImageView(this);icon.setImageResource(R.drawable.ic_server);icon.setScaleType(ImageView.ScaleType.CENTER_INSIDE);icon.setPadding(dp(10),dp(10),dp(10),dp(10));if(Build.VERSION.SDK_INT>=21)icon.setImageTintList(android.content.res.ColorStateList.valueOf(active?GREEN:0xff6fd095));GradientDrawable ig=round(active?0xff143a27:0xff102219,12);ig.setStroke(dp(1),active?0xff34e77d:0xff28523e);icon.setBackground(ig);LinearLayout.LayoutParams iLp=new LinearLayout.LayoutParams(dp(42),dp(42));iLp.setMargins(0,0,dp(11),0);card.addView(icon,iLp);'''
new='''  ImageView icon=new ImageView(this);icon.setImageResource(R.drawable.ic_server);icon.setScaleType(ImageView.ScaleType.CENTER_INSIDE);icon.setPadding(dp(10),dp(10),dp(10),dp(10));if(Build.VERSION.SDK_INT>=21)icon.setImageTintList(android.content.res.ColorStateList.valueOf(active?GREEN:0xff6fd095));GradientDrawable ig=round(active?0xff143a27:0xff102219,12);ig.setStroke(dp(1),active?0xff34e77d:0xff28523e);icon.setBackground(ig);LinearLayout.LayoutParams iLp=new LinearLayout.LayoutParams(dp(44),dp(44));iLp.setMargins(0,0,dp(11),0);card.addView(icon,iLp);'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.84 — Safe area e identificação dos servidores
Botão Voltar fica abaixo da barra de status/horário em qualquer aparelho.
Cabeçalho mantém Servidores centralizado e botão Voltar menor.
Identificação Filmes • Séries • TV ao vivo ganhou altura real e não fica mais cortada.
Cards ganharam espaço vertical suficiente para nome + identificação sem sobreposição.
Mantidos visual, VPN, conjugação de fontes, player e carregamento de canais.

"""+prior)
print("patched 5.28.84")
