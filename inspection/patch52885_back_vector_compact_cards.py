from pathlib import Path
root=Path("work")

p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52884" in s and "versionName '5.28.84'" in s
s=s.replace("versionCode 52884","versionCode 52885",1).replace("versionName '5.28.84'","versionName '5.28.85'",1)
p.write_text(s)

# Real vector back icon: avoids the clipped/diagonal Unicode glyph.
d=root/"app/src/main/res/drawable/ic_arrow_back.xml"
d.write_text("""<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <path
        android:fillColor="#FFFFFFFF"
        android:pathData="M20,11H7.83l5.59,-5.59L12,4l-8,8 8,8 1.42,-1.41L7.83,13H20v-2z"/>
</vector>
""")

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

old='''  TextView back=t("‹",28);
  back.setGravity(Gravity.CENTER);
  back.setTextColor(canReturn?Color.WHITE:0x00ffffff);
  back.setFocusable(canReturn);
  back.setClickable(canReturn);
  back.setContentDescription("Voltar");
  if(canReturn){
   GradientDrawable bbg=round(0x85131d18,16);bbg.setStroke(dp(1),0xff2b493b);back.setBackground(bbg);
   back.setOnClickListener(v->cancelProviderSwitch());
   if(tvMode)armTvFocus(back);
  }
  LinearLayout.LayoutParams backLp=new LinearLayout.LayoutParams(dp(36),dp(36));backLp.setMargins(0,dp(2),0,0);top.addView(back,backLp);'''
new='''  ImageView back=new ImageView(this);
  back.setImageResource(R.drawable.ic_arrow_back);
  back.setScaleType(ImageView.ScaleType.CENTER_INSIDE);
  back.setPadding(dp(9),dp(9),dp(9),dp(9));
  back.setAlpha(canReturn?1f:0f);
  back.setFocusable(canReturn);
  back.setClickable(canReturn);
  back.setContentDescription("Voltar");
  if(canReturn){
   if(Build.VERSION.SDK_INT>=21)back.setImageTintList(android.content.res.ColorStateList.valueOf(Color.WHITE));
   GradientDrawable bbg=round(0x85131d18,18);bbg.setStroke(dp(1),0xff2b493b);back.setBackground(bbg);
   back.setOnClickListener(v->cancelProviderSwitch());
   if(tvMode)armTvFocus(back);
  }
  LinearLayout.LayoutParams backLp=new LinearLayout.LayoutParams(dp(42),dp(42));backLp.setMargins(0,dp(1),0,0);top.addView(back,backLp);'''
assert old in s
s=s.replace(old,new,1)

# Keep the title geometrically centered with the same width reserved on the right.
s=s.replace('top.addView(spacer,new LinearLayout.LayoutParams(dp(36),dp(36)));',
            'top.addView(spacer,new LinearLayout.LayoutParams(dp(42),dp(42)));',1)

# Compact cards: reduce only the excessive top/bottom area while keeping both text lines.
old='''  LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER_VERTICAL);card.setPadding(dp(12),dp(7),dp(10),dp(7));GradientDrawable bg=round(active?0xf013211a:0xf0101713,17);bg.setStroke(dp(1),active?0xff35db78:0xff25372f);card.setBackground(bg);if(Build.VERSION.SDK_INT>=21)card.setElevation(dp(active?3:1));'''
new='''  LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER_VERTICAL);card.setPadding(dp(12),dp(4),dp(10),dp(4));GradientDrawable bg=round(active?0xf013211a:0xf0101713,17);bg.setStroke(dp(1),active?0xff35db78:0xff25372f);card.setBackground(bg);if(Build.VERSION.SDK_INT>=21)card.setElevation(dp(active?3:1));'''
assert old in s
s=s.replace(old,new,1)

old='''  ImageView icon=new ImageView(this);icon.setImageResource(R.drawable.ic_server);icon.setScaleType(ImageView.ScaleType.CENTER_INSIDE);icon.setPadding(dp(10),dp(10),dp(10),dp(10));if(Build.VERSION.SDK_INT>=21)icon.setImageTintList(android.content.res.ColorStateList.valueOf(active?GREEN:0xff6fd095));GradientDrawable ig=round(active?0xff143a27:0xff102219,12);ig.setStroke(dp(1),active?0xff34e77d:0xff28523e);icon.setBackground(ig);LinearLayout.LayoutParams iLp=new LinearLayout.LayoutParams(dp(44),dp(44));iLp.setMargins(0,0,dp(11),0);card.addView(icon,iLp);'''
new='''  ImageView icon=new ImageView(this);icon.setImageResource(R.drawable.ic_server);icon.setScaleType(ImageView.ScaleType.CENTER_INSIDE);icon.setPadding(dp(9),dp(9),dp(9),dp(9));if(Build.VERSION.SDK_INT>=21)icon.setImageTintList(android.content.res.ColorStateList.valueOf(active?GREEN:0xff6fd095));GradientDrawable ig=round(active?0xff143a27:0xff102219,11);ig.setStroke(dp(1),active?0xff34e77d:0xff28523e);icon.setBackground(ig);LinearLayout.LayoutParams iLp=new LinearLayout.LayoutParams(dp(40),dp(40));iLp.setMargins(0,0,dp(11),0);card.addView(icon,iLp);'''
assert old in s
s=s.replace(old,new,1)

old='''  LinearLayout mid=new LinearLayout(this);mid.setOrientation(LinearLayout.VERTICAL);mid.setGravity(Gravity.CENTER_VERTICAL);mid.setPadding(0,dp(2),dp(6),dp(2));mid.setMinimumHeight(dp(50));'''
new='''  LinearLayout mid=new LinearLayout(this);mid.setOrientation(LinearLayout.VERTICAL);mid.setGravity(Gravity.CENTER_VERTICAL);mid.setPadding(0,0,dp(6),0);mid.setMinimumHeight(dp(44));'''
assert old in s
s=s.replace(old,new,1)

s=s.replace('TextView n=t(name,16);','TextView n=t(name,15);',1)
s=s.replace('TextView contentLine=t(providerContentLabel(hasMovies,hasSeries,hasLive),11);',
            'TextView contentLine=t(providerContentLabel(hasMovies,hasSeries,hasLive),10);',1)

old='''  LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(-1,-2);clp.setMargins(0,dp(2),0,0);mid.addView(contentLine,clp);'''
new='''  LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(-1,-2);clp.setMargins(0,0,0,0);mid.addView(contentLine,clp);'''
assert old in s
s=s.replace(old,new,1)

old='''  card.addView(ar,new LinearLayout.LayoutParams(dp(38),dp(44)));'''
new='''  card.addView(ar,new LinearLayout.LayoutParams(dp(36),dp(40)));'''
assert old in s
s=s.replace(old,new,1)

old='''  card.setOnClickListener(v->connectProviderReady(id,name,providerMovies,providerSeries,providerLive,card,ar));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(84));lp.setMargins(0,0,0,dp(8));host.addView(card,lp);'''
new='''  card.setOnClickListener(v->connectProviderReady(id,name,providerMovies,providerSeries,providerLive,card,ar));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(72));lp.setMargins(0,0,0,dp(6));host.addView(card,lp);'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.85 — Voltar real + cards compactos
Botão Voltar agora usa ícone vetorial real, centralizado, sem o bug do traço/barra.
Mantida a área segura abaixo do relógio/status do Android.
Cards dos servidores ficaram mais baixos, reduzindo somente o excesso de espaço superior e inferior.
Filmes • Séries • TV ao vivo continua visível em uma segunda linha.
Ícone do servidor e seta/check também foram reduzidos proporcionalmente.
Mantidos VPN, conjugação, player e carregamento de canais.

"""+prior)
print("patched 5.28.85")
