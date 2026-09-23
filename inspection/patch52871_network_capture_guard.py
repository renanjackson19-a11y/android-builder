from pathlib import Path

g=Path("work/app/build.gradle")
s=g.read_text()
assert "versionCode 52870" in s
assert "versionName '5.28.70'" in s
s=s.replace("versionCode 52870","versionCode 52871",1)
s=s.replace("versionName '5.28.70'","versionName '5.28.71'",1)
g.write_text(s)

# Add network guard helper.
ng=Path("work/app/src/main/java/fun/greenplay/app/NetworkGuard.java")
ng.write_text(r'''package fun.greenplay.app;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.Network;
import android.net.NetworkCapabilities;
import android.net.NetworkInfo;
import android.net.ProxyInfo;
import android.os.Build;

public final class NetworkGuard {
    private NetworkGuard(){}

    public static boolean captureRisk(Context context){
        if(context==null)return false;
        try{
            ConnectivityManager cm=(ConnectivityManager)context.getSystemService(Context.CONNECTIVITY_SERVICE);
            if(cm!=null){
                if(Build.VERSION.SDK_INT>=23){
                    Network n=cm.getActiveNetwork();
                    NetworkCapabilities caps=n==null?null:cm.getNetworkCapabilities(n);
                    if(caps!=null&&caps.hasTransport(NetworkCapabilities.TRANSPORT_VPN))return true;
                    try{
                        ProxyInfo px=cm.getDefaultProxy();
                        if(px!=null&&px.getHost()!=null&&!px.getHost().trim().isEmpty())return true;
                    }catch(Throwable ignored){}
                }else{
                    try{
                        NetworkInfo vpn=cm.getNetworkInfo(ConnectivityManager.TYPE_VPN);
                        if(vpn!=null&&vpn.isConnected())return true;
                    }catch(Throwable ignored){}
                }
            }
        }catch(Throwable ignored){}

        try{
            String h=System.getProperty("http.proxyHost","");
            String hs=System.getProperty("https.proxyHost","");
            if((h!=null&&!h.trim().isEmpty())||(hs!=null&&!hs.trim().isEmpty()))return true;
        }catch(Throwable ignored){}
        return false;
    }
}
''')

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

# Add single guard method near utility block.
anchor=''' void rememberPlayerReturnState(){playerRoundTrip=true;playerReturnScroll=mainScroll;playerReturnBody=body;playerReturnY=mainScroll==null?0:mainScroll.getScrollY();playerReturnNav=currentNavIndex;playerReturnTab=activeHomeTab==null?"":activeHomeTab;}'''
helper=''' boolean blockProtectedPlayback(){
  if(!NetworkGuard.captureRisk(this))return false;
  showAppNotice("Para proteger a fonte, desative VPN, proxy ou aplicativo de captura de rede para assistir.",true);
  return true;
 }
 void rememberPlayerReturnState(){playerRoundTrip=true;playerReturnScroll=mainScroll;playerReturnBody=body;playerReturnY=mainScroll==null?0:mainScroll.getScrollY();playerReturnNav=currentNavIndex;playerReturnTab=activeHomeTab==null?"":activeHomeTab;}'''
assert anchor in s
s=s.replace(anchor,helper,1)

old=''' void playLiveInlineAllowed(JSONObject x){
  if(x!=null){String remember=tvChannelKey(x);if(!remember.isEmpty())sp.edit().putString(tvLastChannelPrefKey(),remember).apply();}'''
new=''' void playLiveInlineAllowed(JSONObject x){
  if(blockProtectedPlayback())return;
  if(x!=null){String remember=tvChannelKey(x);if(!remember.isEmpty())sp.edit().putString(tvLastChannelPrefKey(),remember).apply();}'''
assert old in s
s=s.replace(old,new,1)

old=''' void castTvInlineToTv(){if(tvActiveChannel==null){showAppNotice("Escolha um canal antes de transmitir.",true);return;}'''
new=''' void castTvInlineToTv(){if(blockProtectedPlayback())return;if(tvActiveChannel==null){showAppNotice("Escolha um canal antes de transmitir.",true);return;}'''
assert old in s
s=s.replace(old,new,1)

old=''' void launchOnlinePlayer(Intent in){if(in!=null&&!tvMode&&CastHelper.isConnected(this)){'''
new=''' void launchOnlinePlayer(Intent in){if(blockProtectedPlayback())return;if(in!=null&&!tvMode&&CastHelper.isConnected(this)){'''
assert old in s
s=s.replace(old,new,1)

old=''' void downloadOfflineUrls(JSONArray urls,String name,String poster,String contentId,String videoType,String existingPath){
  try{'''
new=''' void downloadOfflineUrls(JSONArray urls,String name,String poster,String contentId,String videoType,String existingPath){
  if(blockProtectedPlayback())return;
  try{'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

# PlayerActivity: guard again in case VPN/proxy is enabled after navigation.
p=Path("work/app/src/main/java/fun/greenplay/app/PlayerActivity.java")
s=p.read_text()
old=''' boolean live=false,prepared=false,switching=false,tickerStarted=false,episodeQueue=false,tvMode=false,forcePortrait=false,resumeAfterBackground=false,seekingTouch=false,shortsLandscapeCanvas=false;'''
new=''' boolean live=false,prepared=false,switching=false,tickerStarted=false,episodeQueue=false,tvMode=false,forcePortrait=false,resumeAfterBackground=false,seekingTouch=false,shortsLandscapeCanvas=false,offline=false;'''
assert old in s
s=s.replace(old,new,1)

old=''' public void onCreate(Bundle b){super.onCreate(b);tvMode=DeviceCompat.isTelevisionDevice(this);forcePortrait=getIntent()!=null&&getIntent().getBooleanExtra("force_portrait",false);'''
new=''' public void onCreate(Bundle b){super.onCreate(b);offline=getIntent()!=null&&getIntent().getBooleanExtra("offline",false);if(!offline&&NetworkGuard.captureRisk(this)){Toast.makeText(this,"Desative VPN, proxy ou captura de rede para assistir.",Toast.LENGTH_LONG).show();finish();return;}tvMode=DeviceCompat.isTelevisionDevice(this);forcePortrait=getIntent()!=null&&getIntent().getBooleanExtra("force_portrait",false);'''
assert old in s
s=s.replace(old,new,1)

old=''' @Override protected void onResume(){super.onResume();applyImmersive();if(resumeAfterBackground&&player!=null&&prepared){resumeAfterBackground=false;player.play();}}'''
new=''' @Override protected void onResume(){super.onResume();if(!offline&&NetworkGuard.captureRisk(this)){try{if(player!=null)player.pause();}catch(Exception ignored){}Toast.makeText(this,"Desative VPN, proxy ou captura de rede para continuar.",Toast.LENGTH_LONG).show();finish();return;}applyImmersive();if(resumeAfterBackground&&player!=null&&prepared){resumeAfterBackground=false;player.play();}}'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

# Prevent user-installed CA from MITMing GreenPlay API, while keeping provider compatibility.
manifest=Path("work/app/src/main/AndroidManifest.xml")
s=manifest.read_text()
old='''android:usesCleartextTraffic="true" android:allowBackup="false"'''
new='''android:usesCleartextTraffic="true" android:networkSecurityConfig="@xml/network_security_config" android:allowBackup="false"'''
assert old in s
s=s.replace(old,new,1)
manifest.write_text(s)

xml=Path("work/app/src/main/res/xml/network_security_config.xml")
xml.parent.mkdir(parents=True,exist_ok=True)
xml.write_text('''<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors>
            <certificates src="system"/>
            <certificates src="user"/>
        </trust-anchors>
    </base-config>
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">greenplay.fun</domain>
        <trust-anchors>
            <certificates src="system"/>
        </trust-anchors>
    </domain-config>
</network-security-config>
''')
