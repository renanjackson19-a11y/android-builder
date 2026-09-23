from pathlib import Path
root=Path("work")

p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52881" in s and "versionName '5.28.81'" in s
s=s.replace("versionCode 52881","versionCode 52882",1).replace("versionName '5.28.81'","versionName '5.28.82'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

# Remove temporary visible version marker from production UI.
s=s.replace('TextView headerSub=t("Escolha onde deseja conectar  •  v5.28.81",9);',
            'TextView headerSub=t("Escolha onde deseja conectar",9);',1)

# Replace pill chips with one clean content line.
old=''' TextView providerChoiceChip(String label){TextView chip=t(label,10);chip.setTextColor(0xffa9b8b0);chip.setGravity(Gravity.CENTER);chip.setIncludeFontPadding(true);chip.setPadding(dp(9),0,dp(9),0);GradientDrawable cb=round(0xff101a15,12);cb.setStroke(dp(1),0xff294338);chip.setBackground(cb);return chip;}'''
new=''' String providerContentLabel(boolean movies,boolean series,boolean live){
  StringBuilder b=new StringBuilder();
  if(movies)b.append("Filmes");
  if(series){if(b.length()>0)b.append("  •  ");b.append("Séries");}
  if(live){if(b.length()>0)b.append("  •  ");b.append("TV ao vivo");}
  if(b.length()==0)b.append("Conteúdo disponível");
  return b.toString();
 }'''
assert old in s
s=s.replace(old,new,1)

old='''  LinearLayout nameRow=new LinearLayout(this);nameRow.setGravity(Gravity.CENTER_VERTICAL);nameRow.setMinimumHeight(dp(30));TextView n=t(name,16);n.setTypeface(null,1);n.setTextColor(Color.WHITE);n.setIncludeFontPadding(true);n.setGravity(Gravity.CENTER_VERTICAL);n.setMaxLines(1);n.setEllipsize(android.text.TextUtils.TruncateAt.END);nameRow.addView(n,new LinearLayout.LayoutParams(0,-2,1));if(active){TextView badge=t("EM USO",9);badge.setTextColor(0xff04140a);badge.setTypeface(null,1);badge.setGravity(Gravity.CENTER);badge.setIncludeFontPadding(true);badge.setBackground(round(GREEN,10));LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(dp(56),dp(24));bp.setMargins(dp(8),0,0,0);nameRow.addView(badge,bp);}mid.addView(nameRow,new LinearLayout.LayoutParams(-1,-2));
  LinearLayout chips=new LinearLayout(this);chips.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);if(hasMovies){TextView x=providerChoiceChip("Filmes");chips.addView(x,new LinearLayout.LayoutParams(-2,dp(26)));}if(hasSeries){TextView x=providerChoiceChip("Séries");LinearLayout.LayoutParams xp=new LinearLayout.LayoutParams(-2,dp(26));xp.setMargins(dp(6),0,0,0);chips.addView(x,xp);}if(hasLive){TextView x=providerChoiceChip("TV ao vivo");LinearLayout.LayoutParams xp=new LinearLayout.LayoutParams(-2,dp(26));xp.setMargins(dp(6),0,0,0);chips.addView(x,xp);}if(chips.getChildCount()==0){TextView x=providerChoiceChip("Conteúdo disponível");chips.addView(x,new LinearLayout.LayoutParams(-2,dp(26)));}LinearLayout.LayoutParams chp=new LinearLayout.LayoutParams(-1,dp(29));chp.setMargins(0,dp(5),0,0);mid.addView(chips,chp);card.addView(mid,new LinearLayout.LayoutParams(0,-2,1));
  TextView ar=t(active?"✓":"›",active?18:26);ar.setTextColor(active?GREEN:0xffb4beb8);ar.setGravity(Gravity.CENTER);ar.setPadding(0,0,0,0);if(active){GradientDrawable ab=round(0xff123122,16);ab.setStroke(dp(1),0xff2e7950);ar.setBackground(ab);}card.addView(ar,new LinearLayout.LayoutParams(dp(38),dp(48)));'''
new='''  LinearLayout nameRow=new LinearLayout(this);nameRow.setGravity(Gravity.CENTER_VERTICAL);nameRow.setMinimumHeight(dp(28));
  TextView n=t(name,16);n.setTypeface(null,1);n.setTextColor(Color.WHITE);n.setIncludeFontPadding(true);n.setGravity(Gravity.CENTER_VERTICAL);n.setMaxLines(1);n.setEllipsize(android.text.TextUtils.TruncateAt.END);nameRow.addView(n,new LinearLayout.LayoutParams(0,-2,1));
  if(active){TextView activeLabel=t("ATIVO",9);activeLabel.setTextColor(GREEN);activeLabel.setTypeface(null,1);activeLabel.setGravity(Gravity.CENTER);activeLabel.setIncludeFontPadding(true);activeLabel.setPadding(dp(8),0,dp(8),0);GradientDrawable ag=round(0xff10261a,10);ag.setStroke(dp(1),0xff2c6d49);activeLabel.setBackground(ag);LinearLayout.LayoutParams ap=new LinearLayout.LayoutParams(-2,dp(22));ap.setMargins(dp(8),0,0,0);nameRow.addView(activeLabel,ap);}
  mid.addView(nameRow,new LinearLayout.LayoutParams(-1,-2));

  TextView contentLine=t(providerContentLabel(hasMovies,hasSeries,hasLive),11);
  contentLine.setTextColor(0xff9aa8a0);contentLine.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);contentLine.setIncludeFontPadding(true);contentLine.setMaxLines(1);contentLine.setEllipsize(android.text.TextUtils.TruncateAt.END);
  LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(-1,-2);clp.setMargins(0,dp(5),0,0);mid.addView(contentLine,clp);
  card.addView(mid,new LinearLayout.LayoutParams(0,-2,1));

  TextView ar=t(active?"✓":"›",active?19:26);ar.setTextColor(active?GREEN:0xffb4beb8);ar.setGravity(Gravity.CENTER);ar.setPadding(0,0,0,0);
  if(active){GradientDrawable ab=round(0xff10261a,15);ab.setStroke(dp(1),0xff2c6d49);ar.setBackground(ab);}
  card.addView(ar,new LinearLayout.LayoutParams(dp(38),dp(44)));'''
assert old in s
s=s.replace(old,new,1)

# Cards can now be a little more compact because pills are gone.
old='LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(82));lp.setMargins(0,0,0,dp(9));host.addView(card,lp);'
new='LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(74));lp.setMargins(0,0,0,dp(9));host.addView(card,lp);'
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.82 — Tela de servidores refinada
Removidos os chips/pílulas de Filmes, Séries e TV ao vivo.
Conteúdos agora aparecem em uma única linha discreta e limpa abaixo do nome.
Servidor atual usa selo ATIVO escuro com contorno verde, sem bloco verde chamativo.
Check do servidor ativo permanece na direita.
Removido o marcador de versão visível do cabeçalho.
Mantidas as correções de texto, carregamento de canais, VPN, conjugação e player.

"""+prior)
print("patched 5.28.82")
