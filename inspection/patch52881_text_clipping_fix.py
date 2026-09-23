from pathlib import Path
root=Path("work")

p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52880" in s and "versionName '5.28.80'" in s
s=s.replace("versionCode 52880","versionCode 52881",1).replace("versionName '5.28.80'","versionName '5.28.81'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

# Header: stop clipping the title/subtitle at the top.
old='''  LinearLayout headerBox=new LinearLayout(this);headerBox.setOrientation(LinearLayout.VERTICAL);headerBox.setGravity(Gravity.CENTER);
  TextView header=t("Servidores",20);header.setTypeface(null,1);header.setGravity(Gravity.CENTER);header.setIncludeFontPadding(false);
  TextView headerSub=t("Escolha onde deseja conectar  •  v5.28.80",10);headerSub.setTextColor(0xff8fa099);headerSub.setGravity(Gravity.CENTER);headerSub.setIncludeFontPadding(false);
  headerBox.addView(header,new LinearLayout.LayoutParams(-1,dp(25)));headerBox.addView(headerSub,new LinearLayout.LayoutParams(-1,dp(16)));
  top.addView(headerBox,new LinearLayout.LayoutParams(0,dp(44),1));'''
new='''  LinearLayout headerBox=new LinearLayout(this);headerBox.setOrientation(LinearLayout.VERTICAL);headerBox.setGravity(Gravity.CENTER);
  TextView header=t("Servidores",19);header.setTypeface(null,1);header.setGravity(Gravity.CENTER);header.setIncludeFontPadding(true);header.setPadding(0,dp(2),0,0);
  TextView headerSub=t("Escolha onde deseja conectar  •  v5.28.81",9);headerSub.setTextColor(0xff8fa099);headerSub.setGravity(Gravity.CENTER);headerSub.setIncludeFontPadding(true);
  LinearLayout.LayoutParams hp1=new LinearLayout.LayoutParams(-1,-2);LinearLayout.LayoutParams hp2=new LinearLayout.LayoutParams(-1,-2);hp2.setMargins(0,-dp(1),0,0);
  headerBox.addView(header,hp1);headerBox.addView(headerSub,hp2);
  top.addView(headerBox,new LinearLayout.LayoutParams(0,dp(52),1));'''
assert old in s
s=s.replace(old,new,1)

old='''  top.addView(spacer,new LinearLayout.LayoutParams(dp(44),dp(44)));
  root.addView(top,new LinearLayout.LayoutParams(-1,dp(50)));'''
new='''  top.addView(spacer,new LinearLayout.LayoutParams(dp(44),dp(48)));
  root.addView(top,new LinearLayout.LayoutParams(-1,dp(58)));'''
assert old in s
s=s.replace(old,new,1)

# Give back button a little more breathing room while staying fixed.
old='''  top.addView(back,new LinearLayout.LayoutParams(dp(44),dp(44)));'''
new='''  LinearLayout.LayoutParams backLp=new LinearLayout.LayoutParams(dp(46),dp(46));backLp.setMargins(0,dp(2),0,0);top.addView(back,backLp);'''
assert old in s
s=s.replace(old,new,1)

# Intro title/subtitle also use real font metrics.
s=s.replace('title.setIncludeFontPadding(false);introText.addView(title,new LinearLayout.LayoutParams(-1,-2));',
            'title.setIncludeFontPadding(true);introText.addView(title,new LinearLayout.LayoutParams(-1,-2));',1)
s=s.replace('sub.setIncludeFontPadding(false);LinearLayout.LayoutParams slp=',
            'sub.setIncludeFontPadding(true);LinearLayout.LayoutParams slp=',1)

# Server names: remove the fixed 26dp text box that clipped the font.
old='''  LinearLayout nameRow=new LinearLayout(this);nameRow.setGravity(Gravity.CENTER_VERTICAL);TextView n=t(name,16);n.setTypeface(null,1);n.setTextColor(Color.WHITE);n.setIncludeFontPadding(false);n.setMaxLines(1);n.setEllipsize(android.text.TextUtils.TruncateAt.END);nameRow.addView(n,new LinearLayout.LayoutParams(0,dp(26),1));if(active){TextView badge=t("EM USO",9);badge.setTextColor(0xff04140a);badge.setTypeface(null,1);badge.setGravity(Gravity.CENTER);badge.setIncludeFontPadding(false);badge.setBackground(round(GREEN,10));LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(dp(54),dp(22));bp.setMargins(dp(8),0,0,0);nameRow.addView(badge,bp);}mid.addView(nameRow,new LinearLayout.LayoutParams(-1,dp(26)));'''
new='''  LinearLayout nameRow=new LinearLayout(this);nameRow.setGravity(Gravity.CENTER_VERTICAL);nameRow.setMinimumHeight(dp(30));TextView n=t(name,16);n.setTypeface(null,1);n.setTextColor(Color.WHITE);n.setIncludeFontPadding(true);n.setGravity(Gravity.CENTER_VERTICAL);n.setMaxLines(1);n.setEllipsize(android.text.TextUtils.TruncateAt.END);nameRow.addView(n,new LinearLayout.LayoutParams(0,-2,1));if(active){TextView badge=t("EM USO",9);badge.setTextColor(0xff04140a);badge.setTypeface(null,1);badge.setGravity(Gravity.CENTER);badge.setIncludeFontPadding(true);badge.setBackground(round(GREEN,10));LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(dp(56),dp(24));bp.setMargins(dp(8),0,0,0);nameRow.addView(badge,bp);}mid.addView(nameRow,new LinearLayout.LayoutParams(-1,-2));'''
assert old in s
s=s.replace(old,new,1)

# Chips: allow font padding and slightly more height.
old=''' TextView providerChoiceChip(String label){TextView chip=t(label,10);chip.setTextColor(0xffa9b8b0);chip.setGravity(Gravity.CENTER);chip.setIncludeFontPadding(false);chip.setPadding(dp(9),0,dp(9),0);GradientDrawable cb=round(0xff101a15,12);cb.setStroke(dp(1),0xff294338);chip.setBackground(cb);return chip;}'''
new=''' TextView providerChoiceChip(String label){TextView chip=t(label,10);chip.setTextColor(0xffa9b8b0);chip.setGravity(Gravity.CENTER);chip.setIncludeFontPadding(true);chip.setPadding(dp(9),0,dp(9),0);GradientDrawable cb=round(0xff101a15,12);cb.setStroke(dp(1),0xff294338);chip.setBackground(cb);return chip;}'''
assert old in s
s=s.replace(old,new,1)
s=s.replace('new LinearLayout.LayoutParams(-2,dp(24))','new LinearLayout.LayoutParams(-2,dp(26))')
s=s.replace('new LinearLayout.LayoutParams(-1,dp(27))','new LinearLayout.LayoutParams(-1,dp(29))',1)
s=s.replace('LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(74));lp.setMargins(0,0,0,dp(9));host.addView(card,lp);',
            'LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(82));lp.setMargins(0,0,0,dp(9));host.addView(card,lp);',1)

# TV loading status: fixed-height + no font padding was clipping both GREENPLAY/AO VIVO and CONECTANDO AO VIVO.
old='''  tvPreviewLoadingStatus=t("GREENPLAY • AO VIVO",wide?10:9);tvPreviewLoadingStatus.setTextColor(GREEN);tvPreviewLoadingStatus.setTypeface(null,1);tvPreviewLoadingStatus.setGravity(Gravity.CENTER);tvPreviewLoadingStatus.setLetterSpacing(.12f);tvPreviewLoadingStatus.setIncludeFontPadding(false);LinearLayout.LayoutParams stp=new LinearLayout.LayoutParams(-1,dp(wide?24:21));stp.setMargins(0,dp(wide?8:6),0,0);tvPreviewPlaceholder.addView(tvPreviewLoadingStatus,stp);

  tvPreviewTitle=t("Selecione um canal",wide?21:18);tvPreviewTitle.setTypeface(null,1);tvPreviewTitle.setGravity(Gravity.CENTER);tvPreviewTitle.setTextColor(Color.WHITE);tvPreviewTitle.setIncludeFontPadding(false);tvPreviewPlaceholder.addView(tvPreviewTitle,new LinearLayout.LayoutParams(-1,dp(wide?36:32)));

  tvPreviewSubtitle=t(wide?"Escolha um canal na lista para começar":"Escolha um canal para começar",wide?12:11);tvPreviewSubtitle.setTextColor(0xff8d9993);tvPreviewSubtitle.setGravity(Gravity.CENTER);tvPreviewSubtitle.setMaxLines(2);tvPreviewSubtitle.setEllipsize(android.text.TextUtils.TruncateAt.END);tvPreviewSubtitle.setIncludeFontPadding(false);tvPreviewPlaceholder.addView(tvPreviewSubtitle,new LinearLayout.LayoutParams(-1,dp(wide?30:28)));'''
new='''  tvPreviewLoadingStatus=t("GREENPLAY • AO VIVO",wide?10:9);tvPreviewLoadingStatus.setTextColor(GREEN);tvPreviewLoadingStatus.setTypeface(null,1);tvPreviewLoadingStatus.setGravity(Gravity.CENTER);tvPreviewLoadingStatus.setLetterSpacing(.10f);tvPreviewLoadingStatus.setIncludeFontPadding(true);tvPreviewLoadingStatus.setPadding(0,dp(2),0,dp(2));LinearLayout.LayoutParams stp=new LinearLayout.LayoutParams(-1,-2);stp.setMargins(0,dp(wide?9:7),0,dp(3));tvPreviewPlaceholder.addView(tvPreviewLoadingStatus,stp);

  tvPreviewTitle=t("Selecione um canal",wide?21:18);tvPreviewTitle.setTypeface(null,1);tvPreviewTitle.setGravity(Gravity.CENTER);tvPreviewTitle.setTextColor(Color.WHITE);tvPreviewTitle.setIncludeFontPadding(true);tvPreviewTitle.setPadding(0,dp(1),0,dp(1));tvPreviewPlaceholder.addView(tvPreviewTitle,new LinearLayout.LayoutParams(-1,-2));

  tvPreviewSubtitle=t(wide?"Escolha um canal na lista para começar":"Escolha um canal para começar",wide?12:11);tvPreviewSubtitle.setTextColor(0xff8d9993);tvPreviewSubtitle.setGravity(Gravity.CENTER);tvPreviewSubtitle.setMaxLines(2);tvPreviewSubtitle.setEllipsize(android.text.TextUtils.TruncateAt.END);tvPreviewSubtitle.setIncludeFontPadding(true);LinearLayout.LayoutParams subp=new LinearLayout.LayoutParams(-1,-2);subp.setMargins(0,dp(5),0,0);tvPreviewPlaceholder.addView(tvPreviewSubtitle,subp);'''
assert old in s
s=s.replace(old,new,1)

# Progress line a little farther down so it never collides with subtitle/status.
old='''  LinearLayout.LayoutParams pp=new LinearLayout.LayoutParams(dp(wide?220:170),dp(3));pp.gravity=Gravity.CENTER_HORIZONTAL;pp.setMargins(0,dp(wide?14:11),0,0);tvPreviewPlaceholder.addView(tvPreviewLoadingProgress,pp);'''
new='''  LinearLayout.LayoutParams pp=new LinearLayout.LayoutParams(dp(wide?220:170),dp(3));pp.gravity=Gravity.CENTER_HORIZONTAL;pp.setMargins(0,dp(wide?16:13),0,0);tvPreviewPlaceholder.addView(tvPreviewLoadingProgress,pp);'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.81 — Correção de textos cortados
Corrigido o título Servidores no topo: usa altura real da fonte e mais espaço vertical.
Corrigidos nomes dos servidores nos cards: não ficam mais cortados em cima/baixo.
Corrigido GREENPLAY/AO VIVO e CONECTANDO AO VIVO no carregamento dos canais.
Botão Voltar recebeu mais respiro sem sair do topo fixo.
Mantidos visual profissional, conjugação de fontes, VPN e player da 5.28.80.

"""+prior)
print("patched 5.28.81")
