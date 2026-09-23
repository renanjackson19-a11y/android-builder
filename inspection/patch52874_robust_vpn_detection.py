from pathlib import Path
root=Path("work")

# Version
p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52873" in s and "versionName '5.28.73'" in s
s=s.replace("versionCode 52873","versionCode 52874",1).replace("versionName '5.28.73'","versionName '5.28.74'",1)
p.write_text(s)

# Robust VPN detection: Android network transport + TUN/TAP/WireGuard/IPsec interfaces
p=root/"app/src/main/java/fun/greenplay/app/SecurityGuard.java"
s=p.read_text()
s=s.replace("import java.util.Locale;","import java.util.Locale;\nimport java.net.NetworkInterface;\nimport java.util.Enumeration;",1)

old=''' static boolean vpnActive(Context context){
  if(context==null)return false;
  try{
   ConnectivityManager cm=(ConnectivityManager)context.getSystemService(Context.CONNECTIVITY_SERVICE);
   if(cm==null)return false;
   if(Build.VERSION.SDK_INT>=23){
    Network active=cm.getActiveNetwork();
    if(active!=null){NetworkCapabilities caps=cm.getNetworkCapabilities(active);if(caps!=null&&caps.hasTransport(NetworkCapabilities.TRANSPORT_VPN))return true;}
    Network[] all=cm.getAllNetworks();
    if(all!=null)for(Network n:all){NetworkCapabilities caps=cm.getNetworkCapabilities(n);if(caps!=null&&caps.hasTransport(NetworkCapabilities.TRANSPORT_VPN))return true;}
   }
   NetworkInfo legacy=cm.getNetworkInfo(ConnectivityManager.TYPE_VPN);
   return legacy!=null&&legacy.isConnectedOrConnecting();
  }catch(Throwable ignored){return false;}
 }
'''
new=''' static boolean vpnActive(Context context){
  if(vpnInterfaceActive())return true;
  if(context==null)return false;
  try{
   ConnectivityManager cm=(ConnectivityManager)context.getSystemService(Context.CONNECTIVITY_SERVICE);
   if(cm!=null){
    if(Build.VERSION.SDK_INT>=23){
     Network active=cm.getActiveNetwork();
     if(active!=null){NetworkCapabilities caps=cm.getNetworkCapabilities(active);if(caps!=null&&caps.hasTransport(NetworkCapabilities.TRANSPORT_VPN))return true;}
     Network[] all=cm.getAllNetworks();
     if(all!=null)for(Network n:all){NetworkCapabilities caps=cm.getNetworkCapabilities(n);if(caps!=null&&caps.hasTransport(NetworkCapabilities.TRANSPORT_VPN))return true;}
    }
    try{NetworkInfo legacy=cm.getNetworkInfo(ConnectivityManager.TYPE_VPN);if(legacy!=null&&legacy.isConnectedOrConnecting())return true;}catch(Throwable ignored){}
   }
  }catch(Throwable ignored){}
  return vpnInterfaceActive();
 }
 static boolean vpnInterfaceActive(){
  try{
   Enumeration<NetworkInterface> all=NetworkInterface.getNetworkInterfaces();
   if(all==null)return false;
   while(all.hasMoreElements()){
    NetworkInterface ni=all.nextElement();
    if(ni==null)continue;
    try{if(!ni.isUp()||ni.isLoopback())continue;}catch(Throwable ignored){}
    String n=ni.getName();if(n==null)continue;n=n.toLowerCase(Locale.US);
    if(n.startsWith("tun")||n.startsWith("tap")||n.startsWith("wg")||n.startsWith("vpn")||n.contains("ipsec"))return true;
   }
  }catch(Throwable ignored){}
  return false;
 }
'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

# MainActivity: keep polling while app is visible, because some local-capture VPNs
# are not exposed as the active NetworkCapabilities transport to this app.
p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()
old='android.app.AlertDialog vpnBlockDialog; android.net.ConnectivityManager.NetworkCallback vpnWatch; boolean vpnStartupBlocked=false;'
new='android.app.AlertDialog vpnBlockDialog; android.net.ConnectivityManager.NetworkCallback vpnWatch; boolean vpnStartupBlocked=false; android.os.Handler vpnPollHandler=new android.os.Handler(android.os.Looper.getMainLooper()); Runnable vpnPollTask;'
assert old in s
s=s.replace(old,new,1)

old=''' void startVpnWatch(){
  if(vpnWatch!=null||Build.VERSION.SDK_INT<21)return;
  try{android.net.ConnectivityManager cm=(android.net.ConnectivityManager)getSystemService(CONNECTIVITY_SERVICE);if(cm==null)return;android.net.NetworkRequest req=new android.net.NetworkRequest.Builder().addTransportType(android.net.NetworkCapabilities.TRANSPORT_VPN).build();vpnWatch=new android.net.ConnectivityManager.NetworkCallback(){@Override public void onAvailable(android.net.Network n){runOnUiThread(()->{if(!isFinishing())showVpnBlocked(false);});}@Override public void onCapabilitiesChanged(android.net.Network n,android.net.NetworkCapabilities c){if(c!=null&&c.hasTransport(android.net.NetworkCapabilities.TRANSPORT_VPN))runOnUiThread(()->{if(!isFinishing())showVpnBlocked(false);});}};cm.registerNetworkCallback(req,vpnWatch);}catch(Throwable ignored){vpnWatch=null;}
 }
 void stopVpnWatch(){try{if(vpnWatch!=null){android.net.ConnectivityManager cm=(android.net.ConnectivityManager)getSystemService(CONNECTIVITY_SERVICE);if(cm!=null)cm.unregisterNetworkCallback(vpnWatch);}}catch(Throwable ignored){}vpnWatch=null;}
'''
new=''' void startVpnWatch(){
  if(vpnWatch==null&&Build.VERSION.SDK_INT>=21){
   try{android.net.ConnectivityManager cm=(android.net.ConnectivityManager)getSystemService(CONNECTIVITY_SERVICE);if(cm!=null){android.net.NetworkRequest req=new android.net.NetworkRequest.Builder().addTransportType(android.net.NetworkCapabilities.TRANSPORT_VPN).build();vpnWatch=new android.net.ConnectivityManager.NetworkCallback(){@Override public void onAvailable(android.net.Network n){runOnUiThread(()->{if(!isFinishing()&&SecurityGuard.vpnActive(MainActivity.this))showVpnBlocked(false);});}@Override public void onCapabilitiesChanged(android.net.Network n,android.net.NetworkCapabilities c){if(c!=null&&c.hasTransport(android.net.NetworkCapabilities.TRANSPORT_VPN))runOnUiThread(()->{if(!isFinishing())showVpnBlocked(false);});}};cm.registerNetworkCallback(req,vpnWatch);}}catch(Throwable ignored){vpnWatch=null;}
  }
  if(vpnPollTask==null)vpnPollTask=new Runnable(){public void run(){if(!isFinishing()&&SecurityGuard.vpnActive(MainActivity.this))showVpnBlocked(false);if(vpnPollHandler!=null)vpnPollHandler.postDelayed(this,650);}};
  vpnPollHandler.removeCallbacks(vpnPollTask);vpnPollHandler.postDelayed(vpnPollTask,350);
 }
 void stopVpnWatch(){
  try{if(vpnWatch!=null){android.net.ConnectivityManager cm=(android.net.ConnectivityManager)getSystemService(CONNECTIVITY_SERVICE);if(cm!=null)cm.unregisterNetworkCallback(vpnWatch);}}catch(Throwable ignored){}
  vpnWatch=null;
  try{if(vpnPollTask!=null)vpnPollHandler.removeCallbacks(vpnPollTask);}catch(Throwable ignored){}
 }
'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

# PlayerActivity: poll during actual playback too.
p=root/"app/src/main/java/fun/greenplay/app/PlayerActivity.java"
s=p.read_text()
old='boolean vpnStartupBlocked=false;'
new='boolean vpnStartupBlocked=false; Runnable vpnPlayerPoll;'
assert old in s
s=s.replace(old,new,1)

anchor=''' @Override protected void onPause(){savePlaybackProgress(false);try{resumeAfterBackground=player!=null&&player.isPlaying();if(player!=null)player.pause();}catch(Exception ignored){}super.onPause();}
'''
replacement=''' void startPlayerVpnPoll(){if(vpnPlayerPoll==null)vpnPlayerPoll=new Runnable(){public void run(){if(isFinishing())return;if(SecurityGuard.vpnActive(PlayerActivity.this)){try{if(player!=null)player.pause();}catch(Exception ignored){}new android.app.AlertDialog.Builder(PlayerActivity.this).setTitle("VPN detectada").setMessage("Desative a VPN para continuar a reprodução.").setCancelable(false).setPositiveButton("OK",(d,w)->finish()).show();return;}h.postDelayed(this,650);}};h.removeCallbacks(vpnPlayerPoll);h.postDelayed(vpnPlayerPoll,350);}
 void stopPlayerVpnPoll(){if(vpnPlayerPoll!=null)h.removeCallbacks(vpnPlayerPoll);}
 @Override protected void onPause(){stopPlayerVpnPoll();savePlaybackProgress(false);try{resumeAfterBackground=player!=null&&player.isPlaying();if(player!=null)player.pause();}catch(Exception ignored){}super.onPause();}
'''
assert anchor in s
s=s.replace(anchor,replacement,1)

old='''@Override protected void onResume(){super.onResume();if(vpnStartupBlocked)return;if(SecurityGuard.vpnActive(this)){try{if(player!=null)player.pause();}catch(Exception ignored){}new android.app.AlertDialog.Builder(this).setTitle("VPN detectada").setMessage("Desative a VPN para continuar a reprodução.").setCancelable(false).setPositiveButton("OK",(d,w)->finish()).show();return;}applyImmersive();if(resumeAfterBackground&&player!=null&&prepared){resumeAfterBackground=false;player.play();}}'''
new='''@Override protected void onResume(){super.onResume();if(vpnStartupBlocked)return;if(SecurityGuard.vpnActive(this)){try{if(player!=null)player.pause();}catch(Exception ignored){}new android.app.AlertDialog.Builder(this).setTitle("VPN detectada").setMessage("Desative a VPN para continuar a reprodução.").setCancelable(false).setPositiveButton("OK",(d,w)->finish()).show();return;}startPlayerVpnPoll();applyImmersive();if(resumeAfterBackground&&player!=null&&prepared){resumeAfterBackground=false;player.play();}}'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.74 — Detecção reforçada de VPN
Detecção agora combina NetworkCapabilities com interfaces TUN/TAP/WireGuard/IPsec.
Inclui verificação periódica com o app aberto e durante a reprodução.
Bloqueia antes da entrada, ao acessar Filmes/Séries/Canais e se a VPN for ligada durante o vídeo.
Mantém reprodução direta, sem proxy/relay.
\n"""+prior)

print("patched 5.28.74")
