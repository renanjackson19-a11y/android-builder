from pathlib import Path
root=Path('work')

# version
p=root/'app/build.gradle'
s=p.read_text()
assert 'versionCode 52872' in s and "versionName '5.28.72'" in s
s=s.replace('versionCode 52872','versionCode 52873',1).replace("versionName '5.28.72'","versionName '5.28.73'",1)
p.write_text(s)

# VPN detection in SecurityGuard
p=root/'app/src/main/java/fun/greenplay/app/SecurityGuard.java'
s=p.read_text()
assert 'static boolean vpnActive(' not in s
s=s.replace('import android.os.Debug;','import android.os.Debug;\nimport android.os.Build;\nimport android.content.Context;\nimport android.net.ConnectivityManager;\nimport android.net.Network;\nimport android.net.NetworkCapabilities;\nimport android.net.NetworkInfo;',1)
needle=''' static boolean tamperRisk(){\n'''
insert=''' static boolean vpnActive(Context context){\n  if(context==null)return false;\n  try{\n   ConnectivityManager cm=(ConnectivityManager)context.getSystemService(Context.CONNECTIVITY_SERVICE);\n   if(cm==null)return false;\n   if(Build.VERSION.SDK_INT>=23){\n    Network active=cm.getActiveNetwork();\n    if(active!=null){NetworkCapabilities caps=cm.getNetworkCapabilities(active);if(caps!=null&&caps.hasTransport(NetworkCapabilities.TRANSPORT_VPN))return true;}\n    Network[] all=cm.getAllNetworks();\n    if(all!=null)for(Network n:all){NetworkCapabilities caps=cm.getNetworkCapabilities(n);if(caps!=null&&caps.hasTransport(NetworkCapabilities.TRANSPORT_VPN))return true;}\n   }\n   NetworkInfo legacy=cm.getNetworkInfo(ConnectivityManager.TYPE_VPN);\n   return legacy!=null&&legacy.isConnectedOrConnecting();\n  }catch(Throwable ignored){return false;}\n }\n'''
assert needle in s
s=s.replace(needle,insert+needle,1)
p.write_text(s)

# MainActivity startup + foreground + media gates
p=root/'app/src/main/java/fun/greenplay/app/MainActivity.java'
s=p.read_text()
old='public class MainActivity extends Activity{ // GreenPlay 5.28.37\n'
new='public class MainActivity extends Activity{ // GreenPlay 5.28.37\n android.app.AlertDialog vpnBlockDialog; android.net.ConnectivityManager.NetworkCallback vpnWatch; boolean vpnStartupBlocked=false;\n'
assert old in s
s=s.replace(old,new,1)
old='public void onCreate(Bundle b){super.onCreate(b);SecurityGuard.hardenWebView();sp=getSharedPreferences("gp",0);'
new='public void onCreate(Bundle b){super.onCreate(b);SecurityGuard.hardenWebView();if(SecurityGuard.vpnActive(this)){vpnStartupBlocked=true;showVpnBlocked(true);return;}sp=getSharedPreferences("gp",0);'
assert old in s
s=s.replace(old,new,1)
old='@Override protected void onResume(){super.onResume();AppUpdater.resumeInstall(this);'
new='@Override protected void onResume(){super.onResume();if(vpnStartupBlocked||SecurityGuard.vpnActive(this)){showVpnBlocked(vpnStartupBlocked);return;}startVpnWatch();AppUpdater.resumeInstall(this);'
assert old in s
s=s.replace(old,new,1)
old='@Override protected void onPause(){try{if(!tvOrientationTransition)'
new='@Override protected void onPause(){stopVpnWatch();try{if(!tvOrientationTransition)'
assert old in s
s=s.replace(old,new,1)

anchor=' void shell(){\n'
methods=r''' void showVpnBlocked(boolean startup){
  if(isFinishing())return;vpnStartupBlocked=vpnStartupBlocked||startup;
  try{if(vpnBlockDialog!=null&&vpnBlockDialog.isShowing())return;}catch(Exception ignored){}
  android.app.AlertDialog d=new android.app.AlertDialog.Builder(this).setTitle("VPN detectada").setMessage("Desative a VPN para usar o GreenPlay. Enquanto a VPN estiver ativa, Filmes, Séries e Canais ficam bloqueados.").setCancelable(false).setPositiveButton("Tentar novamente",(dlg,w)->{if(SecurityGuard.vpnActive(this)){vpnBlockDialog=null;new Handler(Looper.getMainLooper()).postDelayed(()->showVpnBlocked(vpnStartupBlocked),180);}else{boolean restart=vpnStartupBlocked;vpnStartupBlocked=false;vpnBlockDialog=null;if(restart)recreate();else startVpnWatch();}}).setNegativeButton("Sair",(dlg,w)->{try{finishAndRemoveTask();}catch(Exception e){finish();}}).create();
  vpnBlockDialog=d;d.setOnDismissListener(x->{if(vpnBlockDialog==d)vpnBlockDialog=null;});d.show();
 }
 boolean blockVpnProtectedContent(){if(!SecurityGuard.vpnActive(this))return false;showVpnBlocked(false);return true;}
 void startVpnWatch(){
  if(vpnWatch!=null||Build.VERSION.SDK_INT<21)return;
  try{android.net.ConnectivityManager cm=(android.net.ConnectivityManager)getSystemService(CONNECTIVITY_SERVICE);if(cm==null)return;android.net.NetworkRequest req=new android.net.NetworkRequest.Builder().addTransportType(android.net.NetworkCapabilities.TRANSPORT_VPN).build();vpnWatch=new android.net.ConnectivityManager.NetworkCallback(){@Override public void onAvailable(android.net.Network n){runOnUiThread(()->{if(!isFinishing())showVpnBlocked(false);});}@Override public void onCapabilitiesChanged(android.net.Network n,android.net.NetworkCapabilities c){if(c!=null&&c.hasTransport(android.net.NetworkCapabilities.TRANSPORT_VPN))runOnUiThread(()->{if(!isFinishing())showVpnBlocked(false);});}};cm.registerNetworkCallback(req,vpnWatch);}catch(Throwable ignored){vpnWatch=null;}
 }
 void stopVpnWatch(){try{if(vpnWatch!=null){android.net.ConnectivityManager cm=(android.net.ConnectivityManager)getSystemService(CONNECTIVITY_SERVICE);if(cm!=null)cm.unregisterNetworkCallback(vpnWatch);}}catch(Throwable ignored){}vpnWatch=null;}
'''
assert anchor in s
s=s.replace(anchor,methods+anchor,1)

# Block protected areas before their data/screens open
old=' void openTvCatalogBrowser(int typeId,String title,boolean kidsOnly){\n  if(!tvMode){homeTab(title);return;}'
new=' void openTvCatalogBrowser(int typeId,String title,boolean kidsOnly){\n  if(!kidsOnly&&blockVpnProtectedContent())return;\n  if(!tvMode){homeTab(title);return;}'
assert old in s
s=s.replace(old,new,1)
old=' void homeTab(String selected){\n  if(selected==null||selected.trim().isEmpty())selected="Recomendações";'
new=' void homeTab(String selected){\n  if(selected==null||selected.trim().isEmpty())selected="Recomendações";\n  if(("Filmes".equals(selected)||"Séries".equals(selected))&&blockVpnProtectedContent())return;'
assert old in s
s=s.replace(old,new,1)
old=' void liveContent(){\n  // v16.132:'
new=' void liveContent(){\n  if(blockVpnProtectedContent())return;\n  // v16.132:'
assert old in s
s=s.replace(old,new,1)
old='void launchOnlinePlayer(Intent in){if(blockTamperedPlayback())return;'
new='void launchOnlinePlayer(Intent in){if(blockVpnProtectedContent())return;if(blockTamperedPlayback())return;'
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

# PlayerActivity: defense-in-depth if launched through an unexpected path
p=root/'app/src/main/java/fun/greenplay/app/PlayerActivity.java'
s=p.read_text()
assert 'boolean vpnStartupBlocked=false;' not in s
s=s.replace('public class PlayerActivity extends Activity{\n','public class PlayerActivity extends Activity{\n boolean vpnStartupBlocked=false;\n',1)
old='public void onCreate(Bundle b){super.onCreate(b);if(SecurityGuard.tamperRisk()){'
new='public void onCreate(Bundle b){super.onCreate(b);if(SecurityGuard.vpnActive(this)){vpnStartupBlocked=true;new android.app.AlertDialog.Builder(this).setTitle("VPN detectada").setMessage("Desative a VPN para assistir Canais, Filmes e Séries.").setCancelable(false).setPositiveButton("OK",(d,w)->finish()).show();return;}if(SecurityGuard.tamperRisk()){'
assert old in s
s=s.replace(old,new,1)
old='@Override protected void onResume(){super.onResume();applyImmersive();'
new='@Override protected void onResume(){super.onResume();if(vpnStartupBlocked)return;if(SecurityGuard.vpnActive(this)){try{if(player!=null)player.pause();}catch(Exception ignored){}new android.app.AlertDialog.Builder(this).setTitle("VPN detectada").setMessage("Desative a VPN para continuar a reprodução.").setCancelable(false).setPositiveButton("OK",(d,w)->finish()).show();return;}applyImmersive();'
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

notes=root/'app/RELEASE_NOTES.txt'
prior=notes.read_text() if notes.exists() else ''
notes.write_text('''5.28.73 — Bloqueio de VPN\nVPN detectada antes da entrada no aplicativo bloqueia o acesso e pede para desativar.\nSe a VPN for ativada com o app aberto, o GreenPlay detecta a rede VPN e exibe o bloqueio.\nFilmes, Séries e Canais têm verificação adicional antes de abrir/reproduzir.\nReprodução continua direta, sem proxy/relay no VPS.\n\n'''+prior)
print('patched 5.28.73')
