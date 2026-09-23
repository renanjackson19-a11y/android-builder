from pathlib import Path
root=Path("work")

# version
p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52874" in s and "versionName '5.28.74'" in s
s=s.replace("versionCode 52874","versionCode 52875",1).replace("versionName '5.28.74'","versionName '5.28.75'",1)
p.write_text(s)

# Native GreenPlay-styled VPN dialog. No image assets.
vpn_ui = r'''package fun.greenplay.app;

import android.app.Activity;
import android.app.Dialog;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.StateListDrawable;
import android.view.Gravity;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.LinearLayout;
import android.widget.TextView;

final class VpnNoticeDialog {
 private VpnNoticeDialog(){}

 private static int dp(Activity a,int n){return (int)(n*a.getResources().getDisplayMetrics().density+.5f);}

 private static GradientDrawable round(int color,int radius,Activity a){
  GradientDrawable g=new GradientDrawable();
  g.setColor(color);
  g.setCornerRadius(dp(a,radius));
  return g;
 }

 private static StateListDrawable primaryBg(Activity a){
  StateListDrawable s=new StateListDrawable();
  GradientDrawable focus=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{0xff58f58e,0xff87ffae});
  focus.setCornerRadius(dp(a,19));
  focus.setStroke(dp(a,2),Color.WHITE);
  GradientDrawable normal=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{0xff20df70,0xff55ec8a});
  normal.setCornerRadius(dp(a,19));
  s.addState(new int[]{android.R.attr.state_focused},focus);
  s.addState(new int[]{android.R.attr.state_pressed},focus);
  s.addState(new int[]{},normal);
  return s;
 }

 private static StateListDrawable secondaryBg(Activity a){
  StateListDrawable s=new StateListDrawable();
  GradientDrawable focus=round(0xff173a26,19,a);
  focus.setStroke(dp(a,2),0xff55ec8a);
  GradientDrawable normal=round(0xff101a15,19,a);
  normal.setStroke(dp(a,1),0xff3b5f4d);
  s.addState(new int[]{android.R.attr.state_focused},focus);
  s.addState(new int[]{android.R.attr.state_pressed},focus);
  s.addState(new int[]{},normal);
  return s;
 }

 static Dialog show(Activity a,String message,boolean showExit,String primaryLabel,Runnable primary,Runnable exit){
  final Dialog d=new Dialog(a);
  d.requestWindowFeature(Window.FEATURE_NO_TITLE);
  d.setCancelable(false);
  d.setCanceledOnTouchOutside(false);

  LinearLayout shell=new LinearLayout(a);
  shell.setOrientation(LinearLayout.VERTICAL);
  shell.setPadding(dp(a,22),dp(a,20),dp(a,22),dp(a,18));
  GradientDrawable bg=round(0xff0d1712,24,a);
  bg.setStroke(dp(a,1),0xff2d5b43);
  shell.setBackground(bg);
  if(android.os.Build.VERSION.SDK_INT>=21)shell.setElevation(dp(a,10));

  View accent=new View(a);
  accent.setBackground(round(0xff20e070,3,a));
  LinearLayout.LayoutParams accentLp=new LinearLayout.LayoutParams(dp(a,46),dp(a,4));
  accentLp.setMargins(0,0,0,dp(a,15));
  shell.addView(accent,accentLp);

  TextView title=new TextView(a);
  title.setText("VPN detectada");
  title.setTextColor(Color.WHITE);
  title.setTextSize(22);
  title.setTypeface(null,android.graphics.Typeface.BOLD);
  title.setGravity(Gravity.START);
  shell.addView(title,new LinearLayout.LayoutParams(-1,-2));

  TextView body=new TextView(a);
  body.setText(message);
  body.setTextColor(0xffb9c5bf);
  body.setTextSize(15);
  body.setLineSpacing(0,1.16f);
  body.setGravity(Gravity.START);
  body.setPadding(0,dp(a,9),0,dp(a,18));
  shell.addView(body,new LinearLayout.LayoutParams(-1,-2));

  LinearLayout actions=new LinearLayout(a);
  actions.setOrientation(LinearLayout.HORIZONTAL);
  actions.setGravity(Gravity.END|Gravity.CENTER_VERTICAL);

  if(showExit){
   TextView out=new TextView(a);
   out.setText("Sair");
   out.setTextColor(0xffdce7e1);
   out.setTextSize(15);
   out.setTypeface(null,android.graphics.Typeface.BOLD);
   out.setGravity(Gravity.CENTER);
   out.setFocusable(true);
   out.setClickable(true);
   out.setBackground(secondaryBg(a));
   out.setOnClickListener(v->{try{d.dismiss();}catch(Exception ignored){}if(exit!=null)exit.run();});
   LinearLayout.LayoutParams olp=new LinearLayout.LayoutParams(0,dp(a,48),1);
   olp.setMargins(0,0,dp(a,10),0);
   actions.addView(out,olp);
  }

  TextView ok=new TextView(a);
  ok.setText(primaryLabel==null||primaryLabel.isEmpty()?"OK":primaryLabel);
  ok.setTextColor(0xff031109);
  ok.setTextSize(15);
  ok.setTypeface(null,android.graphics.Typeface.BOLD);
  ok.setGravity(Gravity.CENTER);
  ok.setFocusable(true);
  ok.setClickable(true);
  ok.setBackground(primaryBg(a));
  ok.setOnClickListener(v->{try{d.dismiss();}catch(Exception ignored){}if(primary!=null)primary.run();});
  LinearLayout.LayoutParams plp=new LinearLayout.LayoutParams(showExit?0:-1,dp(a,48),showExit?1.35f:0f);
  actions.addView(ok,plp);

  shell.addView(actions,new LinearLayout.LayoutParams(-1,-2));

  d.setContentView(shell);
  Window w=d.getWindow();
  if(w!=null){
   w.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
   w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);
   WindowManager.LayoutParams lp=w.getAttributes();
   lp.dimAmount=.64f;
   w.setAttributes(lp);
  }
  d.show();
  if(w!=null){
   int sw=a.getResources().getDisplayMetrics().widthPixels;
   int max=dp(a,560);
   int width=Math.min(max,Math.max(dp(a,290),sw-dp(a,34)));
   w.setLayout(width,WindowManager.LayoutParams.WRAP_CONTENT);
   w.setGravity(Gravity.CENTER);
  }
  ok.requestFocus();
  return d;
 }
}
'''
(root/"app/src/main/java/fun/greenplay/app/VpnNoticeDialog.java").write_text(vpn_ui)

# MainActivity use custom dialog
p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()
s=s.replace("android.app.AlertDialog vpnBlockDialog;","android.app.Dialog vpnBlockDialog;",1)
old=''' void showVpnBlocked(boolean startup){
  if(isFinishing())return;vpnStartupBlocked=vpnStartupBlocked||startup;
  try{if(vpnBlockDialog!=null&&vpnBlockDialog.isShowing())return;}catch(Exception ignored){}
  android.app.AlertDialog d=new android.app.AlertDialog.Builder(this).setTitle("VPN detectada").setMessage("Desative a VPN para usar o GreenPlay. Enquanto a VPN estiver ativa, Filmes, Séries e Canais ficam bloqueados.").setCancelable(false).setPositiveButton("Tentar novamente",(dlg,w)->{if(SecurityGuard.vpnActive(this)){vpnBlockDialog=null;new Handler(Looper.getMainLooper()).postDelayed(()->showVpnBlocked(vpnStartupBlocked),180);}else{boolean restart=vpnStartupBlocked;vpnStartupBlocked=false;vpnBlockDialog=null;if(restart)recreate();else startVpnWatch();}}).setNegativeButton("Sair",(dlg,w)->{try{finishAndRemoveTask();}catch(Exception e){finish();}}).create();
  vpnBlockDialog=d;d.setOnDismissListener(x->{if(vpnBlockDialog==d)vpnBlockDialog=null;});d.show();
 }'''
new=''' void showVpnBlocked(boolean startup){
  if(isFinishing())return;vpnStartupBlocked=vpnStartupBlocked||startup;
  try{if(vpnBlockDialog!=null&&vpnBlockDialog.isShowing())return;}catch(Exception ignored){}
  final boolean startupNow=vpnStartupBlocked;
  android.app.Dialog d=VpnNoticeDialog.show(this,
   "Desative a VPN para usar o GreenPlay.\\nEnquanto a VPN estiver ativa, Filmes, Séries e Canais ficam bloqueados.",
   true,"Tentar novamente",
   ()->{vpnBlockDialog=null;if(SecurityGuard.vpnActive(this)){new Handler(Looper.getMainLooper()).postDelayed(()->showVpnBlocked(vpnStartupBlocked),180);}else{boolean restart=vpnStartupBlocked;vpnStartupBlocked=false;if(restart)recreate();else startVpnWatch();}},
   ()->{vpnBlockDialog=null;try{finishAndRemoveTask();}catch(Exception e){finish();}});
  vpnBlockDialog=d;d.setOnDismissListener(x->{if(vpnBlockDialog==d)vpnBlockDialog=null;});
 }'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

# PlayerActivity custom dialog and de-duplicate repeated alerts
p=root/"app/src/main/java/fun/greenplay/app/PlayerActivity.java"
s=p.read_text()
s=s.replace("boolean vpnStartupBlocked=false; Runnable vpnPlayerPoll;","boolean vpnStartupBlocked=false; Runnable vpnPlayerPoll; android.app.Dialog vpnNoticeDialog;",1)

old='''public void onCreate(Bundle b){super.onCreate(b);if(SecurityGuard.vpnActive(this)){vpnStartupBlocked=true;new android.app.AlertDialog.Builder(this).setTitle("VPN detectada").setMessage("Desative a VPN para assistir Canais, Filmes e Séries.").setCancelable(false).setPositiveButton("OK",(d,w)->finish()).show();return;}if(SecurityGuard.tamperRisk()){'''
new='''public void onCreate(Bundle b){super.onCreate(b);if(SecurityGuard.vpnActive(this)){vpnStartupBlocked=true;showPlayerVpnNotice("Desative a VPN para assistir Canais, Filmes e Séries.");return;}if(SecurityGuard.tamperRisk()){'''
assert old in s
s=s.replace(old,new,1)

anchor=''' String nz(String v){return v==null?"":v;}'''
insert=''' void showPlayerVpnNotice(String message){
  if(isFinishing())return;
  try{if(vpnNoticeDialog!=null&&vpnNoticeDialog.isShowing())return;}catch(Exception ignored){}
  android.app.Dialog d=VpnNoticeDialog.show(this,message,false,"OK",()->{vpnNoticeDialog=null;finish();},null);
  vpnNoticeDialog=d;d.setOnDismissListener(x->{if(vpnNoticeDialog==d)vpnNoticeDialog=null;});
 }
'''
assert anchor in s
s=s.replace(anchor,insert+anchor,1)

old=''' void startPlayerVpnPoll(){if(vpnPlayerPoll==null)vpnPlayerPoll=new Runnable(){public void run(){if(isFinishing())return;if(SecurityGuard.vpnActive(PlayerActivity.this)){try{if(player!=null)player.pause();}catch(Exception ignored){}new android.app.AlertDialog.Builder(PlayerActivity.this).setTitle("VPN detectada").setMessage("Desative a VPN para continuar a reprodução.").setCancelable(false).setPositiveButton("OK",(d,w)->finish()).show();return;}h.postDelayed(this,650);}};h.removeCallbacks(vpnPlayerPoll);h.postDelayed(vpnPlayerPoll,350);}'''
new=''' void startPlayerVpnPoll(){if(vpnPlayerPoll==null)vpnPlayerPoll=new Runnable(){public void run(){if(isFinishing())return;if(SecurityGuard.vpnActive(PlayerActivity.this)){try{if(player!=null)player.pause();}catch(Exception ignored){}showPlayerVpnNotice("Desative a VPN para continuar a reprodução.");return;}h.postDelayed(this,650);}};h.removeCallbacks(vpnPlayerPoll);h.postDelayed(vpnPlayerPoll,350);}'''
assert old in s
s=s.replace(old,new,1)

old='''@Override protected void onResume(){super.onResume();if(vpnStartupBlocked)return;if(SecurityGuard.vpnActive(this)){try{if(player!=null)player.pause();}catch(Exception ignored){}new android.app.AlertDialog.Builder(this).setTitle("VPN detectada").setMessage("Desative a VPN para continuar a reprodução.").setCancelable(false).setPositiveButton("OK",(d,w)->finish()).show();return;}startPlayerVpnPoll();applyImmersive();if(resumeAfterBackground&&player!=null&&prepared){resumeAfterBackground=false;player.play();}}'''
new='''@Override protected void onResume(){super.onResume();if(vpnStartupBlocked)return;if(SecurityGuard.vpnActive(this)){try{if(player!=null)player.pause();}catch(Exception ignored){}showPlayerVpnNotice("Desative a VPN para continuar a reprodução.");return;}startPlayerVpnPoll();applyImmersive();if(resumeAfterBackground&&player!=null&&prepared){resumeAfterBackground=false;player.play();}}'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.75 — Aviso de VPN no padrão visual GreenPlay
Substituído o AlertDialog cinza padrão do Android por modal nativo feito no próprio app.
Sem fotos, sem imagens externas e sem ícones externos.
Fundo verde-escuro, borda discreta, cantos arredondados e botões no padrão GreenPlay.
Aplicado tanto na tela principal quanto no player.
Mantida a detecção reforçada de VPN da 5.28.74.
\n"""+prior)

print("patched 5.28.75")
