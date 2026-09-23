from pathlib import Path
root=Path("work")

# Version
p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52874" in s and "versionName '5.28.74'" in s
s=s.replace("versionCode 52874","versionCode 52875",1).replace("versionName '5.28.74'","versionName '5.28.75'",1)
p.write_text(s)

# Reusable custom VPN dialog: follows GreenPlay's own dark/green UI.
(root/"app/src/main/java/fun/greenplay/app/VpnBlockDialog.java").write_text(r'''package fun.greenplay.app;

import android.app.Activity;
import android.app.Dialog;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.StateListDrawable;
import android.os.Build;
import android.view.Gravity;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.LinearLayout;
import android.widget.TextView;

final class VpnBlockDialog {
 private VpnBlockDialog(){}

 static int dp(Activity a,int n){return (int)(n*a.getResources().getDisplayMetrics().density+.5f);}

 static GradientDrawable solid(Activity a,int color,int radius){
  GradientDrawable g=new GradientDrawable();
  g.setColor(color);g.setCornerRadius(dp(a,radius));
  return g;
 }

 static GradientDrawable outlined(Activity a,int color,int radius,int strokeColor){
  GradientDrawable g=solid(a,color,radius);
  g.setStroke(dp(a,1),strokeColor);
  return g;
 }

 static StateListDrawable secondaryBg(Activity a){
  StateListDrawable s=new StateListDrawable();
  GradientDrawable focus=outlined(a,0xff183126,16,0xff20e070);focus.setStroke(dp(a,2),0xff20e070);
  GradientDrawable normal=outlined(a,0xff111916,16,0xff304239);
  s.addState(new int[]{android.R.attr.state_focused},focus);
  s.addState(new int[]{android.R.attr.state_pressed},focus);
  s.addState(new int[]{},normal);
  return s;
 }

 static StateListDrawable primaryBg(Activity a){
  StateListDrawable s=new StateListDrawable();
  GradientDrawable focus=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{0xff49f58a,0xff78f6a5});
  focus.setCornerRadius(dp(a,16));focus.setStroke(dp(a,2),Color.WHITE);
  GradientDrawable normal=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{0xff20df70,0xff49e986});
  normal.setCornerRadius(dp(a,16));
  s.addState(new int[]{android.R.attr.state_focused},focus);
  s.addState(new int[]{android.R.attr.state_pressed},focus);
  s.addState(new int[]{},normal);
  return s;
 }

 static TextView text(Activity a,String value,float sp,int color,boolean bold){
  TextView v=new TextView(a);v.setText(value);v.setTextSize(sp);v.setTextColor(color);
  if(bold)v.setTypeface(Typeface.DEFAULT,Typeface.BOLD);
  v.setIncludeFontPadding(false);
  return v;
 }

 static TextView action(Activity a,String value,boolean primary){
  TextView b=text(a,value,13,primary?0xff04110a:0xff20e070,true);
  b.setGravity(Gravity.CENTER);b.setFocusable(true);b.setClickable(true);
  b.setPadding(dp(a,14),0,dp(a,14),0);
  b.setBackground(primary?primaryBg(a):secondaryBg(a));
  return b;
 }

 static Dialog show(Activity a,String message,boolean retryMode,Runnable retry,Runnable exit){
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
 }
}
''')

# MainActivity: replace stock gray AlertDialog with GreenPlay custom dialog.
p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()
s=s.replace("android.app.AlertDialog vpnBlockDialog;","android.app.Dialog vpnBlockDialog;",1)
old=''' void showVpnBlocked(boolean startup){
  if(isFinishing())return;vpnStartupBlocked=vpnStartupBlocked||startup;
  try{if(vpnBlockDialog!=null&&vpnBlockDialog.isShowing())return;}catch(Exception ignored){}
  android.app.AlertDialog d=new android.app.AlertDialog.Builder(this).setTitle("VPN detectada").setMessage("Desative a VPN para usar o GreenPlay. Enquanto a VPN estiver ativa, Filmes, Séries e Canais ficam bloqueados.").setCancelable(false).setPositiveButton("Tentar novamente",(dlg,w)->{if(SecurityGuard.vpnActive(this)){vpnBlockDialog=null;new Handler(Looper.getMainLooper()).postDelayed(()->showVpnBlocked(vpnStartupBlocked),180);}else{boolean restart=vpnStartupBlocked;vpnStartupBlocked=false;vpnBlockDialog=null;if(restart)recreate();else startVpnWatch();}}).setNegativeButton("Sair",(dlg,w)->{try{finishAndRemoveTask();}catch(Exception e){finish();}}).create();
  vpnBlockDialog=d;d.setOnDismissListener(x->{if(vpnBlockDialog==d)vpnBlockDialog=null;});d.show();
 }
'''
new=''' void showVpnBlocked(boolean startup){
  if(isFinishing())return;vpnStartupBlocked=vpnStartupBlocked||startup;
  try{if(vpnBlockDialog!=null&&vpnBlockDialog.isShowing())return;}catch(Exception ignored){}
  final android.app.Dialog[] ref=new android.app.Dialog[1];
  android.app.Dialog d=VpnBlockDialog.show(this,
   "Desative a VPN para usar o GreenPlay. Enquanto a VPN estiver ativa, Filmes, Séries e Canais ficam bloqueados.",
   true,
   ()->{vpnBlockDialog=null;if(SecurityGuard.vpnActive(this)){new Handler(Looper.getMainLooper()).postDelayed(()->showVpnBlocked(vpnStartupBlocked),180);}else{boolean restart=vpnStartupBlocked;vpnStartupBlocked=false;if(restart)recreate();else startVpnWatch();}},
   ()->{vpnBlockDialog=null;try{finishAndRemoveTask();}catch(Exception e){finish();}}
  );
  ref[0]=d;vpnBlockDialog=d;d.setOnDismissListener(x->{if(vpnBlockDialog==ref[0])vpnBlockDialog=null;});
 }
'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

# PlayerActivity: use the same native custom dialog instead of stock AlertDialog.
p=root/"app/src/main/java/fun/greenplay/app/PlayerActivity.java"
s=p.read_text()
s=s.replace("boolean vpnStartupBlocked=false; Runnable vpnPlayerPoll;","boolean vpnStartupBlocked=false; Runnable vpnPlayerPoll; android.app.Dialog vpnPlayerDialog;",1)

old='''public void onCreate(Bundle b){super.onCreate(b);if(SecurityGuard.vpnActive(this)){vpnStartupBlocked=true;new android.app.AlertDialog.Builder(this).setTitle("VPN detectada").setMessage("Desative a VPN para assistir Canais, Filmes e Séries.").setCancelable(false).setPositiveButton("OK",(d,w)->finish()).show();return;}if(SecurityGuard.tamperRisk()){'''
new='''public void onCreate(Bundle b){super.onCreate(b);if(SecurityGuard.vpnActive(this)){vpnStartupBlocked=true;showPlayerVpnDialog("Desative a VPN para assistir Canais, Filmes e Séries.");return;}if(SecurityGuard.tamperRisk()){'''
assert old in s
s=s.replace(old,new,1)

old=''' void startPlayerVpnPoll(){if(vpnPlayerPoll==null)vpnPlayerPoll=new Runnable(){public void run(){if(isFinishing())return;if(SecurityGuard.vpnActive(PlayerActivity.this)){try{if(player!=null)player.pause();}catch(Exception ignored){}new android.app.AlertDialog.Builder(PlayerActivity.this).setTitle("VPN detectada").setMessage("Desative a VPN para continuar a reprodução.").setCancelable(false).setPositiveButton("OK",(d,w)->finish()).show();return;}h.postDelayed(this,650);}};h.removeCallbacks(vpnPlayerPoll);h.postDelayed(vpnPlayerPoll,350);}
'''
new=''' void showPlayerVpnDialog(String msg){if(isFinishing())return;try{if(vpnPlayerDialog!=null&&vpnPlayerDialog.isShowing())return;}catch(Exception ignored){}final android.app.Dialog[] ref=new android.app.Dialog[1];android.app.Dialog d=VpnBlockDialog.show(this,msg,false,null,()->finish());ref[0]=d;vpnPlayerDialog=d;d.setOnDismissListener(x->{if(vpnPlayerDialog==ref[0])vpnPlayerDialog=null;});}
 void startPlayerVpnPoll(){if(vpnPlayerPoll==null)vpnPlayerPoll=new Runnable(){public void run(){if(isFinishing())return;if(SecurityGuard.vpnActive(PlayerActivity.this)){try{if(player!=null)player.pause();}catch(Exception ignored){}showPlayerVpnDialog("Desative a VPN para continuar a reprodução.");return;}h.postDelayed(this,650);}};h.removeCallbacks(vpnPlayerPoll);h.postDelayed(vpnPlayerPoll,350);}
'''
assert old in s
s=s.replace(old,new,1)

old=''' @Override protected void onResume(){super.onResume();if(vpnStartupBlocked)return;if(SecurityGuard.vpnActive(this)){try{if(player!=null)player.pause();}catch(Exception ignored){}new android.app.AlertDialog.Builder(this).setTitle("VPN detectada").setMessage("Desative a VPN para continuar a reprodução.").setCancelable(false).setPositiveButton("OK",(d,w)->finish()).show();return;}startPlayerVpnPoll();applyImmersive();if(resumeAfterBackground&&player!=null&&prepared){resumeAfterBackground=false;player.play();}}'''
new=''' @Override protected void onResume(){super.onResume();if(vpnStartupBlocked)return;if(SecurityGuard.vpnActive(this)){try{if(player!=null)player.pause();}catch(Exception ignored){}showPlayerVpnDialog("Desative a VPN para continuar a reprodução.");return;}startPlayerVpnPoll();applyImmersive();if(resumeAfterBackground&&player!=null&&prepared){resumeAfterBackground=false;player.play();}}'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.75 — Alerta VPN no padrão GreenPlay
Substituído o AlertDialog cinza padrão do Android por um modal nativo próprio.
Visual escuro igual ao aplicativo, borda discreta, tipografia limpa e verde GreenPlay.
Mesma proteção/detecção da 5.28.74; alteração somente visual do aviso.
Sem imagens/fotos e sem proxy/relay.
\n"""+prior)

print("patched 5.28.75")
