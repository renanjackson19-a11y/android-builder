from pathlib import Path
root=Path("work")

# Version
p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52875" in s and "versionName '5.28.75'" in s
s=s.replace("versionCode 52875","versionCode 52876",1).replace("versionName '5.28.75'","versionName '5.28.76'",1)
p.write_text(s)

# Rework only the VPN modal UI/animation.
p=root/"app/src/main/java/fun/greenplay/app/VpnBlockDialog.java"
s=p.read_text()

s=s.replace("import android.view.WindowManager;","import android.view.WindowManager;\nimport android.view.animation.DecelerateInterpolator;",1)

old=''' static Dialog show(Activity a,String message,boolean retryMode,Runnable retry,Runnable exit){
  final Dialog d=new Dialog(a);
  d.requestWindowFeature(Window.FEATURE_NO_TITLE);
  d.setCancelable(false);

  LinearLayout card=new LinearLayout(a);
  card.setOrientation(LinearLayout.VERTICAL);
  card.setPadding(dp(a,24),dp(a,22),dp(a,24),dp(a,22));
  GradientDrawable cardBg=outlined(a,0xff101916,24,0xff2b3b33);
  card.setBackground(cardBg);
  if(Build.VERSION.SDK_INT>=21)card.setElevation(dp(a,14));

  TextView kicker=text(a,"PROTEÇÃO DE REDE",10,0xff20e070,true);
  kicker.setLetterSpacing(.12f);
  card.addView(kicker,new LinearLayout.LayoutParams(-1,-2));

  TextView title=text(a,"VPN detectada",22,Color.WHITE,true);
  LinearLayout.LayoutParams tlp=new LinearLayout.LayoutParams(-1,-2);tlp.setMargins(0,dp(a,8),0,0);
  card.addView(title,tlp);

  TextView body=text(a,message,15,0xffbac5bf,false);
  body.setLineSpacing(0,1.12f);
  LinearLayout.LayoutParams blp=new LinearLayout.LayoutParams(-1,-2);blp.setMargins(0,dp(a,12),0,0);
  card.addView(body,blp);

  View divider=new View(a);divider.setBackgroundColor(0xff25342c);
  LinearLayout.LayoutParams dlp=new LinearLayout.LayoutParams(-1,dp(a,1));dlp.setMargins(0,dp(a,20),0,dp(a,16));
  card.addView(divider,dlp);

  LinearLayout buttons=new LinearLayout(a);
  buttons.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);
  if(retryMode){
   TextView out=action(a,"SAIR",false);
   TextView again=action(a,"TENTAR NOVAMENTE",true);
   LinearLayout.LayoutParams olp=new LinearLayout.LayoutParams(0,dp(a,50),.40f);olp.setMargins(0,0,dp(a,10),0);
   LinearLayout.LayoutParams alp=new LinearLayout.LayoutParams(0,dp(a,50),.60f);
   buttons.addView(out,olp);buttons.addView(again,alp);
   out.setOnClickListener(v->{d.dismiss();if(exit!=null)exit.run();});
   again.setOnClickListener(v->{d.dismiss();if(retry!=null)retry.run();});
   again.requestFocus();
  }else{
   TextView ok=action(a,"OK",true);
   LinearLayout.LayoutParams olp=new LinearLayout.LayoutParams(dp(a,156),dp(a,50));
   buttons.addView(ok,olp);
   ok.setOnClickListener(v->{d.dismiss();if(exit!=null)exit.run();});
   ok.requestFocus();
  }
  card.addView(buttons,new LinearLayout.LayoutParams(-1,-2));

  d.setContentView(card);
  d.setOnShowListener(x->{
   Window w=d.getWindow();if(w==null)return;
   w.setBackgroundDrawableResource(android.R.color.transparent);
   WindowManager.LayoutParams lp=new WindowManager.LayoutParams();
   lp.copyFrom(w.getAttributes());
   int screen=a.getResources().getDisplayMetrics().widthPixels;
   int target=Math.min(screen-dp(a,32),dp(a,560));
   if(DeviceCompat.isTelevisionDevice(a))target=Math.min(screen-dp(a,120),dp(a,760));
   lp.width=Math.max(dp(a,280),target);lp.height=WindowManager.LayoutParams.WRAP_CONTENT;lp.dimAmount=.72f;
   w.setAttributes(lp);w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);
  });
  d.show();
  return d;
 }'''
new=''' static Dialog show(Activity a,String message,boolean retryMode,Runnable retry,Runnable exit){
  final Dialog d=new Dialog(a);
  d.requestWindowFeature(Window.FEATURE_NO_TITLE);
  d.setCancelable(false);

  final boolean tv=DeviceCompat.isTelevisionDevice(a);

  LinearLayout card=new LinearLayout(a);
  card.setOrientation(LinearLayout.VERTICAL);
  card.setGravity(Gravity.CENTER_HORIZONTAL);
  card.setPadding(dp(a,tv?30:22),dp(a,tv?24:20),dp(a,tv?30:22),dp(a,tv?24:20));
  GradientDrawable cardBg=outlined(a,0xff0d1713,tv?22:20,0xff2a4035);
  card.setBackground(cardBg);
  if(Build.VERSION.SDK_INT>=21)card.setElevation(dp(a,18));

  View accent=new View(a);
  accent.setBackground(solid(a,0xff20e070,2));
  LinearLayout.LayoutParams acp=new LinearLayout.LayoutParams(dp(a,tv?58:46),dp(a,3));
  acp.setMargins(0,0,0,dp(a,13));
  card.addView(accent,acp);

  TextView kicker=text(a,"PROTEÇÃO DE REDE",tv?10:9.5f,0xff20e070,true);
  kicker.setLetterSpacing(.14f);kicker.setGravity(Gravity.CENTER);kicker.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
  card.addView(kicker,new LinearLayout.LayoutParams(-1,-2));

  TextView title=text(a,"VPN detectada",tv?24:21,Color.WHITE,true);
  title.setGravity(Gravity.CENTER);title.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);
  LinearLayout.LayoutParams tlp=new LinearLayout.LayoutParams(-1,-2);tlp.setMargins(0,dp(a,7),0,0);
  card.addView(title,tlp);

  TextView body=text(a,message,tv?15:14.5f,0xffbdc8c2,false);
  body.setGravity(Gravity.CENTER);body.setTextAlignment(View.TEXT_ALIGNMENT_CENTER);body.setLineSpacing(0,1.10f);
  LinearLayout.LayoutParams blp=new LinearLayout.LayoutParams(-1,-2);blp.setMargins(0,dp(a,12),0,0);
  card.addView(body,blp);

  LinearLayout buttons=new LinearLayout(a);
  buttons.setGravity(Gravity.CENTER);
  LinearLayout.LayoutParams bwrap=new LinearLayout.LayoutParams(-1,-2);bwrap.setMargins(0,dp(a,tv?21:18),0,0);

  if(retryMode){
   TextView out=action(a,"SAIR",false);
   TextView again=action(a,"TENTAR NOVAMENTE",true);
   LinearLayout.LayoutParams olp=new LinearLayout.LayoutParams(0,dp(a,tv?52:48),.38f);olp.setMargins(0,0,dp(a,10),0);
   LinearLayout.LayoutParams alp=new LinearLayout.LayoutParams(0,dp(a,tv?52:48),.62f);
   buttons.addView(out,olp);buttons.addView(again,alp);
   out.setOnClickListener(v->{d.dismiss();if(exit!=null)exit.run();});
   again.setOnClickListener(v->{d.dismiss();if(retry!=null)retry.run();});
   again.requestFocus();
  }else{
   TextView ok=action(a,"OK",true);
   LinearLayout.LayoutParams olp=new LinearLayout.LayoutParams(tv?dp(a,190):dp(a,150),dp(a,tv?52:48));
   buttons.addView(ok,olp);
   ok.setOnClickListener(v->{d.dismiss();if(exit!=null)exit.run();});
   ok.requestFocus();
  }
  card.addView(buttons,bwrap);

  d.setContentView(card);

  Window w=d.getWindow();
  if(w!=null){
   w.setBackgroundDrawableResource(android.R.color.transparent);
   w.setGravity(Gravity.CENTER);
   w.setWindowAnimations(0);
   WindowManager.LayoutParams lp=new WindowManager.LayoutParams();
   lp.copyFrom(w.getAttributes());
   int screen=a.getResources().getDisplayMetrics().widthPixels;
   int target=Math.min(screen-dp(a,tv?100:36),dp(a,tv?700:520));
   lp.width=Math.max(dp(a,280),target);
   lp.height=WindowManager.LayoutParams.WRAP_CONTENT;
   lp.gravity=Gravity.CENTER;
   lp.x=0;lp.y=0;
   lp.dimAmount=.68f;
   lp.windowAnimations=0;
   w.setAttributes(lp);
   w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);
  }

  // Important: no horizontal/vertical translation at any point.
  // The modal is born in the exact center and only uses a subtle center scale + fade.
  card.setTranslationX(0f);card.setTranslationY(0f);
  card.setAlpha(0f);card.setScaleX(.94f);card.setScaleY(.94f);
  d.setOnShowListener(x->card.post(()->{
   card.setPivotX(card.getWidth()/2f);card.setPivotY(card.getHeight()/2f);
   card.setTranslationX(0f);card.setTranslationY(0f);
   card.animate().cancel();
   card.animate().alpha(1f).scaleX(1f).scaleY(1f).setDuration(170)
    .setInterpolator(new DecelerateInterpolator()).start();
  }));
  d.show();
  return d;
 }'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.76 — Modal VPN centralizado
Popup nasce no centro desde o primeiro frame, sem deslizar da lateral.
Animação somente fade + escala pelo centro, sem translate X/Y.
Título, aviso e conteúdo alinhados ao centro.
Card mais compacto, espaçamento refinado e melhor proporção em celular/TV.
Mesma detecção de VPN da 5.28.74/5.28.75; mudança visual apenas.
Sem imagens/fotos e sem proxy/relay.
\n"""+prior)

print("patched 5.28.76")
