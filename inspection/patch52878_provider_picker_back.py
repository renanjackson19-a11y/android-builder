from pathlib import Path
root=Path("work")

# Version
p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52876" in s and "versionName '5.28.76'" in s
s=s.replace("versionCode 52876","versionCode 52878",1).replace("versionName '5.28.76'","versionName '5.28.78'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

old=''' void providerSelectAfterLogin(boolean canCancel){
  authScreen=false;providerSwitchScreen=canCancel;base(true);root.setPadding(dp(18),standardPageTopPx(),dp(18),dp(10));
  if(canCancel){
   LinearLayout closeRow=new LinearLayout(this);closeRow.setGravity(Gravity.RIGHT|Gravity.BOTTOM);closeRow.setPadding(0,statusBarHeightPx(),0,0);
   TextView close=t("×",27);close.setGravity(Gravity.CENTER);close.setTextColor(Color.WHITE);close.setPadding(0,0,0,0);GradientDrawable xbg=round(0x99131d18,22);xbg.setStroke(dp(1),0xff315344);close.setBackground(xbg);close.setContentDescription("Fechar seleção de servidor");close.setOnClickListener(v->cancelProviderSwitch());
   closeRow.addView(close,new LinearLayout.LayoutParams(dp(46),dp(46)));root.addView(closeRow,new LinearLayout.LayoutParams(-1,statusBarHeightPx()+dp(52)));
  }
  ScrollView screen=new ScrollView(this);screen.setFillViewport(true);screen.setVerticalScrollBarEnabled(false);screen.setClipToPadding(false);
  LinearLayout wrap=new LinearLayout(this);wrap.setOrientation(LinearLayout.VERTICAL);wrap.setGravity(Gravity.CENTER_HORIZONTAL|Gravity.CENTER_VERTICAL);int providerSide=wideTvUi()?Math.max(dp(48),(getResources().getDisplayMetrics().widthPixels-dp(720))/2):0;wrap.setPadding(providerSide,dp(2),providerSide,dp(6));wrap.setTranslationY(-dp(44));screen.addView(wrap,new ScrollView.LayoutParams(-1,-1));root.addView(screen,new LinearLayout.LayoutParams(-1,0,1));
  ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);applyAppLogo(logo);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(62));lp.setMargins(dp(76),0,dp(76),dp(2));wrap.addView(logo,lp);
  TextView title=t("Escolha um servidor",24);title.setTypeface(null,1);title.setGravity(Gravity.CENTER);title.setPadding(0,dp(4),0,0);wrap.addView(title,new LinearLayout.LayoutParams(-1,-2));
  TextView sub=t("Selecione o servidor que deseja conectar",14);sub.setTextColor(0xffb1b8b4);sub.setGravity(Gravity.CENTER);sub.setPadding(0,0,0,0);LinearLayout.LayoutParams slp=new LinearLayout.LayoutParams(-1,-2);slp.setMargins(0,dp(4),0,dp(10));wrap.addView(sub,slp);
  LinearLayout list=new LinearLayout(this);list.setOrientation(LinearLayout.VERTICAL);list.setGravity(Gravity.CENTER_HORIZONTAL);list.setPadding(dp(4),0,dp(4),0);wrap.addView(list,new LinearLayout.LayoutParams(-1,-2));
  TextView loading=t("Carregando servidores…",13);loading.setTextColor(0xffb1b8b4);loading.setGravity(Gravity.CENTER);list.addView(loading,new LinearLayout.LayoutParams(-1,dp(54)));
  loadProviderChoices(list,loading);
 }'''

new=''' void providerSelectAfterLogin(boolean canCancel){
  authScreen=false;
  boolean hasPreviousProvider=(Api.PROVIDER!=null&&!Api.PROVIDER.trim().isEmpty())||!sp.getString("provider_id","").trim().isEmpty();
  final boolean canReturn=canCancel||hasPreviousProvider;
  providerSwitchScreen=canReturn;
  base(true);
  root.setPadding(dp(14),standardPageTopPx(),dp(14),dp(8));

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
  top.addView(back,new LinearLayout.LayoutParams(dp(44),dp(44)));

  TextView header=t("Servidores",18);
  header.setTypeface(null,1);header.setGravity(Gravity.CENTER);
  top.addView(header,new LinearLayout.LayoutParams(0,dp(44),1));

  View spacer=new View(this);
  top.addView(spacer,new LinearLayout.LayoutParams(dp(44),dp(44)));
  root.addView(top,new LinearLayout.LayoutParams(-1,dp(50)));

  ScrollView screen=new ScrollView(this);
  screen.setFillViewport(true);screen.setVerticalScrollBarEnabled(false);screen.setClipToPadding(false);
  screen.setPadding(0,0,0,dp(28));

  LinearLayout wrap=new LinearLayout(this);
  wrap.setOrientation(LinearLayout.VERTICAL);
  wrap.setGravity(Gravity.CENTER_HORIZONTAL);
  int providerSide=wideTvUi()?Math.max(dp(48),(getResources().getDisplayMetrics().widthPixels-dp(720))/2):0;
  wrap.setPadding(providerSide,dp(2),providerSide,dp(18));
  // Sem translationY: evita cortar logo/cabeçalho e mantém a tela estável ao voltar.
  screen.addView(wrap,new ScrollView.LayoutParams(-1,-2));
  root.addView(screen,new LinearLayout.LayoutParams(-1,0,1));

  ImageView logo=new ImageView(this);
  logo.setScaleType(ImageView.ScaleType.FIT_CENTER);applyAppLogo(logo);
  LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(tvMode?62:54));
  lp.setMargins(dp(92),dp(2),dp(92),dp(2));wrap.addView(logo,lp);

  TextView title=t("Escolha um servidor",24);
  title.setTypeface(null,1);title.setGravity(Gravity.CENTER);title.setPadding(0,dp(3),0,0);
  wrap.addView(title,new LinearLayout.LayoutParams(-1,-2));

  TextView sub=t("Selecione o servidor que deseja conectar",14);
  sub.setTextColor(0xffb1b8b4);sub.setGravity(Gravity.CENTER);sub.setPadding(0,0,0,0);
  LinearLayout.LayoutParams slp=new LinearLayout.LayoutParams(-1,-2);slp.setMargins(0,dp(4),0,dp(14));wrap.addView(sub,slp);

  LinearLayout list=new LinearLayout(this);
  list.setOrientation(LinearLayout.VERTICAL);list.setGravity(Gravity.CENTER_HORIZONTAL);
  list.setPadding(dp(2),0,dp(2),dp(18));wrap.addView(list,new LinearLayout.LayoutParams(-1,-2));

  TextView loading=t("Carregando servidores…",13);
  loading.setTextColor(0xffb1b8b4);loading.setGravity(Gravity.CENTER);
  list.addView(loading,new LinearLayout.LayoutParams(-1,dp(54)));
  loadProviderChoices(list,loading);
 }'''

assert old in s
s=s.replace(old,new,1)

# Back button should return from the provider picker whenever there is a previous server.
old='''  if(providerSwitchScreen){cancelProviderSwitch();return;}'''
new='''  if(providerSwitchScreen){cancelProviderSwitch();return;}'''
assert old in s  # behavior already correct; retained intentionally

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.78 — Tela de servidores corrigida
Botão Voltar fixo no topo da seleção de servidores.
Voltar funciona mesmo se a tela for reaberta com um servidor anterior salvo.
Removido deslocamento negativo que cortava o topo/logo.
Lista ganhou respiro inferior para o último servidor não ficar preso na barra do sistema.
Mantidas VPN, player e demais comportamentos da 5.28.76.
\n"""+prior)

print("patched 5.28.78")
