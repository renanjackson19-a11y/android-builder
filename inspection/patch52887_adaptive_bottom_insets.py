from pathlib import Path
root=Path("work")

p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52886" in s and "versionName '5.28.86'" in s
s=s.replace("versionCode 52886","versionCode 52887",1).replace("versionName '5.28.86'","versionName '5.28.87'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

# Remember the real system navigation inset for each device.
old=''' static final int REQ_PROFILE_PHOTO=8601; static final int TAG_SKIP_TV_FOCUS_FX=0x4f120001;'''
new=''' static final int REQ_PROFILE_PHOTO=8601; int mobileBottomInsetPx=0; static final int TAG_SKIP_TV_FOCUS_FX=0x4f120001;'''
assert old in s
s=s.replace(old,new,1)

# Add navigation-bar inset helpers next to the existing safe-area helpers.
old=''' void standardRootInsets(){if(root!=null)root.setPadding(0,wideTvUi()?0:dp(18),0,0);}
 void tvRootInsets(){if(root!=null)root.setPadding(0,wideTvUi()?0:Math.max(dp(34),systemSafeTopPx()+dp(8)),0,0);}'''
new=''' void standardRootInsets(){if(root!=null)root.setPadding(0,wideTvUi()?0:dp(18),0,0);}
 int navigationBottomInsetPx(android.view.WindowInsets wi){
  int bottom=0;try{
   if(wi!=null){
    if(android.os.Build.VERSION.SDK_INT>=30){
     android.graphics.Insets nav=wi.getInsets(android.view.WindowInsets.Type.navigationBars());
     android.graphics.Insets gest=wi.getInsets(android.view.WindowInsets.Type.systemGestures());
     bottom=Math.max(nav.bottom,gest.bottom);
    }else bottom=Math.max(wi.getSystemWindowInsetBottom(),wi.getStableInsetBottom());
   }
  }catch(Throwable ignored){}
  return Math.max(0,bottom);
 }
 int currentNavigationBottomInsetPx(){
  int bottom=mobileBottomInsetPx;try{
   if(android.os.Build.VERSION.SDK_INT>=23){
    android.view.WindowInsets wi=getWindow().getDecorView().getRootWindowInsets();
    bottom=Math.max(bottom,navigationBottomInsetPx(wi));
   }
  }catch(Throwable ignored){}
  return Math.max(0,bottom);
 }
 void applyMobileBottomNavInsets(android.view.WindowInsets wi){
  if(wideTvUi()||navBar==null)return;
  int inset=navigationBottomInsetPx(wi);if(inset<=0)inset=currentNavigationBottomInsetPx();
  mobileBottomInsetPx=Math.max(0,inset);
  navBar.setGravity(Gravity.CENTER);
  navBar.setPadding(0,dp(3),0,dp(2)+mobileBottomInsetPx);
  ViewGroup.LayoutParams raw=navBar.getLayoutParams();
  if(raw instanceof LinearLayout.LayoutParams){
   LinearLayout.LayoutParams lp=(LinearLayout.LayoutParams)raw;
   lp.width=-1;lp.height=dp(64)+mobileBottomInsetPx;lp.setMargins(0,0,0,0);navBar.setLayoutParams(lp);
  }
 }
 void installMobileBottomNavInsets(){
  if(wideTvUi()||navBar==null)return;
  if(android.os.Build.VERSION.SDK_INT>=20){
   navBar.setOnApplyWindowInsetsListener((v,wi)->{applyMobileBottomNavInsets(wi);return wi;});
   navBar.post(()->{try{navBar.requestApplyInsets();}catch(Throwable ignored){applyMobileBottomNavInsets(null);}});
  }else applyMobileBottomNavInsets(null);
 }
 void tvRootInsets(){if(root!=null)root.setPadding(0,wideTvUi()?0:Math.max(dp(34),systemSafeTopPx()+dp(8)),0,0);}'''
assert old in s
s=s.replace(old,new,1)

# Install the listener when the mobile shell creates the navigation bar.
old='''   root.addView(navBar,new LinearLayout.LayoutParams(-1,dp(64)));enforceGlobalBottomNav();'''
new='''   root.addView(navBar,new LinearLayout.LayoutParams(-1,dp(64)));installMobileBottomNavInsets();enforceGlobalBottomNav();'''
assert old in s
s=s.replace(old,new,1)

# Never force the bottom bar back to 64dp after insets have been applied.
old=''' void enforceGlobalBottomNav(){if(wideTvUi()||navBar==null)return;if(root!=null&&!detailOpen&&!plansScreen&&!providerSwitchScreen&&!authScreen)standardRootInsets();navBar.setGravity(Gravity.CENTER);navBar.setPadding(0,dp(3),0,dp(2));navBar.setBackgroundColor(0xff102018);ViewGroup.LayoutParams raw=navBar.getLayoutParams();if(raw instanceof LinearLayout.LayoutParams){LinearLayout.LayoutParams lp=(LinearLayout.LayoutParams)raw;lp.width=-1;lp.height=dp(64);lp.setMargins(0,0,0,0);navBar.setLayoutParams(lp);}}'''
new=''' void enforceGlobalBottomNav(){if(wideTvUi()||navBar==null)return;if(root!=null&&!detailOpen&&!plansScreen&&!providerSwitchScreen&&!authScreen)standardRootInsets();navBar.setBackgroundColor(0xff102018);applyMobileBottomNavInsets(null);}'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.87 — Barra inferior adaptativa
A barra inferior agora lê a área de navegação real informada pelo Android (WindowInsets).
Em aparelhos com três botões, o GreenPlay sobe Início/Favoritos/TV/Downloads/Perfil para não ficarem atrás dos botões do sistema.
Em aparelhos com navegação por gestos, o espaço é calculado separadamente e não cria uma margem fixa exagerada.
A altura da barra passa a ser 64dp + o inset real do aparelho e se reajusta automaticamente.
Mantidas pesquisa completa da 5.28.86, player, VPN, conjugação de fontes e demais telas.

"""+prior)
print("patched 5.28.87")
