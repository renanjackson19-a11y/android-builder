from pathlib import Path
root=Path("work")

p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52887" in s and "versionName '5.28.87'" in s
s=s.replace("versionCode 52887","versionCode 52888",1).replace("versionName '5.28.87'","versionName '5.28.88'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

old=''' int navigationBottomInsetPx(android.view.WindowInsets wi){
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
 }'''
new=''' int navigationBottomInsetPx(android.view.WindowInsets wi){
  int bottom=0;try{
   if(wi!=null){
    if(android.os.Build.VERSION.SDK_INT>=30){
     // Para posicionar a barra do app devemos respeitar apenas a barra de
     // navegacao do sistema. systemGestures() e maior em muitos aparelhos
     // com gestos e fazia a barra do GreenPlay ficar duas vezes mais alta.
     android.graphics.Insets nav=wi.getInsets(android.view.WindowInsets.Type.navigationBars());
     bottom=nav.bottom;
    }else{
     // stableInsetBottom pode continuar com a altura antiga dos 3 botoes mesmo
     // quando o usuario usa gestos. O inset atual e o valor correto aqui.
     bottom=wi.getSystemWindowInsetBottom();
    }
   }
  }catch(Throwable ignored){}
  if(bottom<0)bottom=0;
  // Protecao contra valores anormais de OEM/ROM. Uma barra de navegacao real
  // nao precisa reservar mais que 64dp para manter os controles do app seguros.
  return Math.min(bottom,dp(64));
 }
 int currentNavigationBottomInsetPx(){
  try{
   if(android.os.Build.VERSION.SDK_INT>=23){
    android.view.WindowInsets wi=getWindow().getDecorView().getRootWindowInsets();
    if(wi!=null)return navigationBottomInsetPx(wi);
   }
  }catch(Throwable ignored){}
  return Math.max(0,mobileBottomInsetPx);
 }
 void applyMobileBottomNavInsets(android.view.WindowInsets wi){
  if(wideTvUi()||navBar==null)return;
  int inset=wi!=null?navigationBottomInsetPx(wi):currentNavigationBottomInsetPx();
  mobileBottomInsetPx=Math.max(0,inset);

  // Base mais compacta. O espaco extra e exatamente o que o Android informa
  // para a navegacao daquele aparelho.
  int baseH=dp(58);
  navBar.setGravity(Gravity.CENTER);
  navBar.setPadding(0,dp(2),0,dp(2)+mobileBottomInsetPx);
  ViewGroup.LayoutParams raw=navBar.getLayoutParams();
  if(raw instanceof LinearLayout.LayoutParams){
   LinearLayout.LayoutParams lp=(LinearLayout.LayoutParams)raw;
   lp.width=-1;lp.height=baseH+mobileBottomInsetPx;lp.setMargins(0,0,0,0);navBar.setLayoutParams(lp);
  }
 }'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.88 — Correção da barra inferior em gestos e 3 botões
Corrigido o excesso de altura visto em aparelhos com navegação por gestos.
A barra agora usa somente navigationBars() do Android, sem somar systemGestures().
Em Android antigo usa o inset atual, sem stableInsetBottom que podia manter a altura antiga dos 3 botões.
A barra base foi reduzida de 64dp para 58dp e recebe somente o espaço real da navegação do aparelho.
Mantida proteção para celulares com 3 botões, sem cobrir Início/Favoritos/TV/Downloads/Perfil.
Mantidas pesquisa completa, player, VPN e conjugação de fontes.

"""+prior)
print("patched 5.28.88")
