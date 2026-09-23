from pathlib import Path
root=Path("work")
p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52879" in s and "versionName '5.28.79'" in s
s=s.replace("versionCode 52879","versionCode 52880",1).replace("versionName '5.28.79'","versionName '5.28.80'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

# Make the provider screen visibly different and add a version marker so installation is unmistakable.
old='''  TextView headerSub=t("Escolha onde deseja conectar",10);headerSub.setTextColor(0xff8fa099);headerSub.setGravity(Gravity.CENTER);headerSub.setIncludeFontPadding(false);'''
new='''  TextView headerSub=t("Escolha onde deseja conectar  •  v5.28.80",10);headerSub.setTextColor(0xff8fa099);headerSub.setGravity(Gravity.CENTER);headerSub.setIncludeFontPadding(false);'''
assert old in s
s=s.replace(old,new,1)

old='''  LinearLayout intro=new LinearLayout(this);intro.setOrientation(LinearLayout.HORIZONTAL);intro.setGravity(Gravity.CENTER_VERTICAL);intro.setPadding(dp(4),dp(4),dp(4),dp(10));
  ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);applyAppLogo(logo);intro.addView(logo,new LinearLayout.LayoutParams(dp(tvMode?58:50),dp(tvMode?46:40)));
  LinearLayout introText=new LinearLayout(this);introText.setOrientation(LinearLayout.VERTICAL);introText.setPadding(dp(11),0,0,0);
  TextView title=t("Escolha seu servidor",18);title.setTypeface(null,1);title.setTextColor(Color.WHITE);title.setIncludeFontPadding(false);introText.addView(title,new LinearLayout.LayoutParams(-1,-2));
  TextView sub=t("Você pode trocar a qualquer momento",11);sub.setTextColor(0xff8fa099);sub.setIncludeFontPadding(false);LinearLayout.LayoutParams slp=new LinearLayout.LayoutParams(-1,-2);slp.setMargins(0,dp(4),0,0);introText.addView(sub,slp);
  intro.addView(introText,new LinearLayout.LayoutParams(0,-2,1));wrap.addView(intro,new LinearLayout.LayoutParams(-1,-2));'''
new='''  LinearLayout intro=new LinearLayout(this);intro.setOrientation(LinearLayout.HORIZONTAL);intro.setGravity(Gravity.CENTER_VERTICAL);intro.setPadding(dp(4),dp(8),dp(4),dp(14));
  ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);applyAppLogo(logo);intro.addView(logo,new LinearLayout.LayoutParams(dp(tvMode?54:46),dp(tvMode?42:36)));
  LinearLayout introText=new LinearLayout(this);introText.setOrientation(LinearLayout.VERTICAL);introText.setPadding(dp(12),0,0,0);
  TextView title=t("Selecione um servidor",17);title.setTypeface(null,1);title.setTextColor(Color.WHITE);title.setIncludeFontPadding(false);introText.addView(title,new LinearLayout.LayoutParams(-1,-2));
  TextView sub=t("Seu conteúdo fica organizado por fonte",10);sub.setTextColor(0xff86978e);sub.setIncludeFontPadding(false);LinearLayout.LayoutParams slp=new LinearLayout.LayoutParams(-1,-2);slp.setMargins(0,dp(3),0,0);introText.addView(sub,slp);
  intro.addView(introText,new LinearLayout.LayoutParams(0,-2,1));wrap.addView(intro,new LinearLayout.LayoutParams(-1,-2));'''
assert old in s
s=s.replace(old,new,1)

# Refine provider cards: thinner border, softer background, smaller icon, compact height.
old='''  LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER_VERTICAL);card.setPadding(dp(13),dp(10),dp(10),dp(10));GradientDrawable bg=round(active?0xf012211a:0xef111915,20);bg.setStroke(dp(active?2:1),active?GREEN:0xff2a3b33);card.setBackground(bg);if(Build.VERSION.SDK_INT>=21)card.setElevation(dp(active?5:2));
  ImageView icon=new ImageView(this);icon.setImageResource(R.drawable.ic_server);icon.setScaleType(ImageView.ScaleType.CENTER_INSIDE);icon.setPadding(dp(13),dp(13),dp(13),dp(13));if(Build.VERSION.SDK_INT>=21)icon.setImageTintList(android.content.res.ColorStateList.valueOf(active?GREEN:0xff75d99d));GradientDrawable ig=round(active?0xff143b27:0xff10291d,15);ig.setStroke(dp(1),active?0xff34e77d:0xff285940);icon.setBackground(ig);LinearLayout.LayoutParams iLp=new LinearLayout.LayoutParams(dp(52),dp(52));iLp.setMargins(0,0,dp(13),0);card.addView(icon,iLp);'''
new='''  LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER_VERTICAL);card.setPadding(dp(13),dp(9),dp(11),dp(9));GradientDrawable bg=round(active?0xf013211a:0xf0101713,18);bg.setStroke(dp(1),active?0xff35db78:0xff25372f);card.setBackground(bg);if(Build.VERSION.SDK_INT>=21)card.setElevation(dp(active?4:1));
  ImageView icon=new ImageView(this);icon.setImageResource(R.drawable.ic_server);icon.setScaleType(ImageView.ScaleType.CENTER_INSIDE);icon.setPadding(dp(11),dp(11),dp(11),dp(11));if(Build.VERSION.SDK_INT>=21)icon.setImageTintList(android.content.res.ColorStateList.valueOf(active?GREEN:0xff6fd095));GradientDrawable ig=round(active?0xff143a27:0xff102219,13);ig.setStroke(dp(1),active?0xff34e77d:0xff28523e);icon.setBackground(ig);LinearLayout.LayoutParams iLp=new LinearLayout.LayoutParams(dp(46),dp(46));iLp.setMargins(0,0,dp(12),0);card.addView(icon,iLp);'''
assert old in s
s=s.replace(old,new,1)

s=s.replace('LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(82));lp.setMargins(0,0,0,dp(10));host.addView(card,lp);',
            'LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(74));lp.setMargins(0,0,0,dp(9));host.addView(card,lp);',1)

# Completely replace the loading placeholder with a slim professional composition:
# no large circle/square, no old text, logo + status + channel name + horizontal green line.
start=s.index(' void buildTvPreviewPlaceholder(boolean wide){')
end=s.index(' void showTvPreviewError(String msg)', start)
replacement=''' void buildTvPreviewPlaceholder(boolean wide){
  tvPreviewPlaceholder=new LinearLayout(this);tvPreviewPlaceholder.setOrientation(LinearLayout.VERTICAL);tvPreviewPlaceholder.setGravity(Gravity.CENTER);tvPreviewPlaceholder.setPadding(dp(wide?36:24),dp(wide?24:18),dp(wide?36:24),dp(wide?24:18));tvPreviewPlaceholder.setBackgroundColor(0xff010604);

  LinearLayout brandRow=new LinearLayout(this);brandRow.setGravity(Gravity.CENTER);brandRow.setOrientation(LinearLayout.HORIZONTAL);
  tvPreviewLoadingLogo=new ImageView(this);tvPreviewLoadingLogo.setScaleType(ImageView.ScaleType.FIT_CENTER);tvPreviewLoadingLogo.setImageResource(R.drawable.ic_nav_tv);if(Build.VERSION.SDK_INT>=21)tvPreviewLoadingLogo.setImageTintList(android.content.res.ColorStateList.valueOf(GREEN));
  brandRow.addView(tvPreviewLoadingLogo,new LinearLayout.LayoutParams(dp(wide?58:48),dp(wide?58:48)));
  tvPreviewPlaceholder.addView(brandRow,new LinearLayout.LayoutParams(-1,dp(wide?62:52)));

  tvPreviewLoadingStatus=t("GREENPLAY • AO VIVO",wide?10:9);tvPreviewLoadingStatus.setTextColor(GREEN);tvPreviewLoadingStatus.setTypeface(null,1);tvPreviewLoadingStatus.setGravity(Gravity.CENTER);tvPreviewLoadingStatus.setLetterSpacing(.12f);tvPreviewLoadingStatus.setIncludeFontPadding(false);LinearLayout.LayoutParams stp=new LinearLayout.LayoutParams(-1,dp(wide?24:21));stp.setMargins(0,dp(wide?8:6),0,0);tvPreviewPlaceholder.addView(tvPreviewLoadingStatus,stp);

  tvPreviewTitle=t("Selecione um canal",wide?21:18);tvPreviewTitle.setTypeface(null,1);tvPreviewTitle.setGravity(Gravity.CENTER);tvPreviewTitle.setTextColor(Color.WHITE);tvPreviewTitle.setIncludeFontPadding(false);tvPreviewPlaceholder.addView(tvPreviewTitle,new LinearLayout.LayoutParams(-1,dp(wide?36:32)));

  tvPreviewSubtitle=t(wide?"Escolha um canal na lista para começar":"Escolha um canal para começar",wide?12:11);tvPreviewSubtitle.setTextColor(0xff8d9993);tvPreviewSubtitle.setGravity(Gravity.CENTER);tvPreviewSubtitle.setMaxLines(2);tvPreviewSubtitle.setEllipsize(android.text.TextUtils.TruncateAt.END);tvPreviewSubtitle.setIncludeFontPadding(false);tvPreviewPlaceholder.addView(tvPreviewSubtitle,new LinearLayout.LayoutParams(-1,dp(wide?30:28)));

  tvPreviewLoadingProgress=new ProgressBar(this,null,android.R.attr.progressBarStyleHorizontal);tvPreviewLoadingProgress.setIndeterminate(true);if(Build.VERSION.SDK_INT>=21)tvPreviewLoadingProgress.setIndeterminateTintList(android.content.res.ColorStateList.valueOf(GREEN));tvPreviewLoadingProgress.setVisibility(View.GONE);
  LinearLayout.LayoutParams pp=new LinearLayout.LayoutParams(dp(wide?220:170),dp(3));pp.gravity=Gravity.CENTER_HORIZONTAL;pp.setMargins(0,dp(wide?14:11),0,0);tvPreviewPlaceholder.addView(tvPreviewLoadingProgress,pp);
 }
 void showTvPreviewLoading(String name){
  clearTvBackdrop();
  if(tvPreviewPlaceholder!=null){tvPreviewPlaceholder.animate().cancel();tvPreviewPlaceholder.setScaleX(.985f);tvPreviewPlaceholder.setScaleY(.985f);tvPreviewPlaceholder.setAlpha(0f);tvPreviewPlaceholder.setVisibility(View.VISIBLE);tvPreviewPlaceholder.animate().alpha(1f).scaleX(1f).scaleY(1f).setDuration(150).start();}
  if(tvPreviewLoadingStatus!=null){tvPreviewLoadingStatus.setText("CONECTANDO AO VIVO");tvPreviewLoadingStatus.setTextColor(GREEN);}
  if(tvPreviewLoadingProgress!=null)tvPreviewLoadingProgress.setVisibility(View.VISIBLE);
  if(tvPreviewLoadingLogo!=null){
   tvPreviewLoadingLogo.setImageResource(R.drawable.ic_nav_tv);
   if(Build.VERSION.SDK_INT>=21)tvPreviewLoadingLogo.setImageTintList(android.content.res.ColorStateList.valueOf(GREEN));
   if(tvActiveChannel!=null){
    String a=tvActiveChannel.optString("provider_icon",tvActiveChannel.optString("stream_icon",""));
    String b=tvActiveChannel.optString("thumbnail",tvActiveChannel.optString("image",""));
    String c=tvActiveChannel.optString("epg_logo",tvActiveChannel.optString("fallback_logo",""));
    if(!a.isEmpty()||!b.isEmpty()||!c.isEmpty()){if(Build.VERSION.SDK_INT>=21)tvPreviewLoadingLogo.setImageTintList(null);Img.loadBest(tvPreviewLoadingLogo,a,b,c);}
   }
  }
  if(tvPreviewTitle!=null)tvPreviewTitle.setText(name==null||name.trim().isEmpty()?"Abrindo transmissão":name.trim());
  if(tvPreviewSubtitle!=null)tvPreviewSubtitle.setText("Preparando o sinal…");
  if(tvSoundButton!=null)tvSoundButton.setVisibility(View.GONE);if(tvCastButton!=null)tvCastButton.setVisibility(View.GONE);if(tvFullButton!=null)tvFullButton.setVisibility(View.GONE);hideTvEpgOverlay();if(tvInlinePlayerView!=null)tvInlinePlayerView.setVisibility(View.VISIBLE);
 }
'''
s=s[:start]+replacement+s[end:]

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.80 — UI profissional confirmável
Tela Servidores agora mostra v5.28.80 no cabeçalho para confirmar que a atualização instalada é a correta.
Cards de servidor mais compactos, bordas discretas, ícones menores e destaque do servidor em uso.
Carregamento de canal totalmente substituído: sem círculo/quadrado grande, sem texto antigo 'Carregando canal...'.
Agora usa logo do canal, status CONECTANDO AO VIVO, nome do canal, texto Preparando o sinal e barra verde horizontal fina.
Mantidos VPN, conjugação de fontes, player e retorno da tela de servidores.

"""+prior)
print("patched 5.28.80")
