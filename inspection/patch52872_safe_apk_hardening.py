from pathlib import Path

root=Path("work")

# version + hardened update-compatible .debug build
p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52870" in s and "versionName '5.28.70'" in s
s=s.replace("versionCode 52870","versionCode 52872",1).replace("versionName '5.28.70'","versionName '5.28.72'",1)
old="""        debug {
            applicationIdSuffix '.debug'
            signingConfig signingConfigs.stableDebug
        }"""
new="""        debug {
            applicationIdSuffix '.debug'
            signingConfig signingConfigs.stableDebug
            debuggable false
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }"""
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

(root/"app/proguard-rules.pro").write_text(r'''-keepattributes Signature,InnerClasses,EnclosingMethod,*Annotation*
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
-keepnames class fun.greenplay.app.MainActivity
-keepnames class fun.greenplay.app.PlayerActivity
-keepnames class fun.greenplay.app.YouTubePlayerActivity
-keepnames class fun.greenplay.app.OfflineDownloadService
-keep class fun.greenplay.app.CastOptionsProvider { *; }
-renamesourcefileattribute SourceFile
-assumenosideeffects class android.util.Log {
    public static *** v(...);
    public static *** d(...);
    public static *** i(...);
    public static *** w(...);
    public static *** e(...);
}
''')

(root/"app/src/main/java/fun/greenplay/app/SecretStrings.java").write_text(r'''package fun.greenplay.app;
final class SecretStrings{
 private SecretStrings(){}
 static String apiBase(){int[]v={50,46,46,42,41,96,117,117,61,40,63,63,52,42,54,59,35,116,60,47,52,117,59,42,51,117,62,46,54,51,44,63,117};char[]c=new char[v.length];for(int i=0;i<v.length;i++)c[i]=(char)(v[i]^0x5a);return new String(c);}
 static String apiToken(){int[]v={3,2,3,14,3,1,82,82,3,7,4,82,15,5,86,14,1,2,0,82,86,81,84,0,1,7,14,6,84,84,85,1,83,15,84,84,83,3,86,15,81,86,83,81,84,86,3,2};char[]c=new char[v.length];for(int i=0;i<v.length;i++)c[i]=(char)(v[i]^0x37);return new String(c);}
}
''')

p=root/"app/src/main/java/fun/greenplay/app/Api.java"
s=p.read_text()
assert 'static final String BASE="https://greenplay.fun/api/dtlive/";' in s
assert 'static final String TOKEN="454946ee403e82a9657eafc76091ccb6d8ccd4a8fadfca45";' in s
s=s.replace('static final String BASE="https://greenplay.fun/api/dtlive/";','static final String BASE=SecretStrings.apiBase();',1)
s=s.replace('static final String TOKEN="454946ee403e82a9657eafc76091ccb6d8ccd4a8fadfca45";','static final String TOKEN=SecretStrings.apiToken();',1)
s=s.replace('}catch(Exception e){String msg=e.getMessage();MAIN.post(()->cb.err(msg));}', '}catch(Exception e){String msg="Falha de conexão";MAIN.post(()->cb.err(msg));}',1)
p.write_text(s)

(root/"app/src/main/java/fun/greenplay/app/SecretStore.java").write_text(r'''package fun.greenplay.app;
import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyProperties;
import android.util.Base64;
import java.nio.charset.StandardCharsets;
import java.security.KeyStore;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;

final class SecretStore{
 private static final String ALIAS="gp_media_v1";
 private SecretStore(){}
 private static SecretKey key() throws Exception{
  KeyStore ks=KeyStore.getInstance("AndroidKeyStore");ks.load(null);
  java.security.Key k=ks.getKey(ALIAS,null);if(k instanceof SecretKey)return (SecretKey)k;
  KeyGenerator g=KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES,"AndroidKeyStore");
  g.init(new KeyGenParameterSpec.Builder(ALIAS,KeyProperties.PURPOSE_ENCRYPT|KeyProperties.PURPOSE_DECRYPT).setBlockModes(KeyProperties.BLOCK_MODE_GCM).setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE).setRandomizedEncryptionRequired(true).build());
  return g.generateKey();
 }
 static String encrypt(String raw){if(raw==null||raw.isEmpty())return "";try{Cipher c=Cipher.getInstance("AES/GCM/NoPadding");c.init(Cipher.ENCRYPT_MODE,key());byte[]iv=c.getIV(),ct=c.doFinal(raw.getBytes(StandardCharsets.UTF_8));byte[]out=new byte[1+iv.length+ct.length];out[0]=(byte)iv.length;System.arraycopy(iv,0,out,1,iv.length);System.arraycopy(ct,0,out,1+iv.length,ct.length);return Base64.encodeToString(out,Base64.NO_WRAP);}catch(Throwable ignored){return "";}}
 static String decrypt(String blob){if(blob==null||blob.isEmpty())return "";try{byte[]in=Base64.decode(blob,Base64.NO_WRAP);int n=in[0]&0xff;if(n<8||1+n>=in.length)return "";byte[]iv=new byte[n],ct=new byte[in.length-1-n];System.arraycopy(in,1,iv,0,n);System.arraycopy(in,1+n,ct,0,ct.length);Cipher c=Cipher.getInstance("AES/GCM/NoPadding");c.init(Cipher.DECRYPT_MODE,key(),new GCMParameterSpec(128,iv));return new String(c.doFinal(ct),StandardCharsets.UTF_8);}catch(Throwable ignored){return "";}}
}
''')

(root/"app/src/main/java/fun/greenplay/app/SecurityGuard.java").write_text(r'''package fun.greenplay.app;
import android.os.Debug;
import android.webkit.WebView;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Locale;
final class SecurityGuard{
 private SecurityGuard(){}
 static void hardenWebView(){try{WebView.setWebContentsDebuggingEnabled(false);}catch(Throwable ignored){}}
 static boolean tamperRisk(){
  try{if(Debug.isDebuggerConnected()||Debug.waitingForDebugger())return true;}catch(Throwable ignored){}
  try(BufferedReader r=new BufferedReader(new FileReader("/proc/self/maps"))){String x;while((x=r.readLine())!=null){String z=x.toLowerCase(Locale.US);if(z.contains("frida")||z.contains("xposed")||z.contains("lsposed")||z.contains("substrate"))return true;}}catch(Throwable ignored){}
  return false;
 }
}
''')

p=root/"app/src/main/AndroidManifest.xml"
s=p.read_text()
old='android:usesCleartextTraffic="true" android:allowBackup="false" android:extractNativeLibs="true"'
new='android:usesCleartextTraffic="true" android:networkSecurityConfig="@xml/network_security_config" android:debuggable="false" android:allowBackup="false" android:extractNativeLibs="true"'
assert old in s
s=s.replace(old,new,1)
s=s.replace('<activity android:name=".PlayerActivity" ', '<activity android:name=".PlayerActivity" android:exported="false" ',1)
s=s.replace('<activity android:name=".YouTubePlayerActivity" ', '<activity android:name=".YouTubePlayerActivity" android:exported="false" ',1)
p.write_text(s)

xml=root/"app/src/main/res/xml/network_security_config.xml"
xml.parent.mkdir(parents=True,exist_ok=True)
xml.write_text('''<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors><certificates src="system"/></trust-anchors>
    </base-config>
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">greenplay.fun</domain>
        <trust-anchors><certificates src="system"/></trust-anchors>
    </domain-config>
</network-security-config>
''')

p=root/"app/src/main/java/fun/greenplay/app/CastHelper.java"
s=p.read_text()
s=s.replace('   android.util.Log.e("GreenPlayCast","Falha ao abrir Google Cast",e);\n','')
s=s.replace('   android.util.Log.e("GreenPlayCast","Google Cast indisponivel",e);\n','')
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java"
s=p.read_text()
old='''        WebSettings ws=web.getSettings();
        ws.setJavaScriptEnabled(true);ws.setDomStorageEnabled(true);ws.setMediaPlaybackRequiresUserGesture(false);
        ws.setLoadsImagesAutomatically(true);ws.setUseWideViewPort(true);ws.setLoadWithOverviewMode(true);'''
new='''        SecurityGuard.hardenWebView();
        WebSettings ws=web.getSettings();
        ws.setJavaScriptEnabled(true);ws.setDomStorageEnabled(true);ws.setMediaPlaybackRequiresUserGesture(false);
        ws.setAllowFileAccess(false);ws.setAllowContentAccess(false);ws.setSaveFormData(false);
        if(android.os.Build.VERSION.SDK_INT>=21)ws.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        ws.setLoadsImagesAutomatically(true);ws.setUseWideViewPort(true);ws.setLoadWithOverviewMode(true);'''
assert old in s
s=s.replace(old,new,1)
old='''        super.onCreate(b);
        getWindow().setFlags'''
new='''        super.onCreate(b);
        if(SecurityGuard.tamperRisk()){Toast.makeText(this,"Reprodução indisponível em ambiente instrumentado.",Toast.LENGTH_LONG).show();finish();return;}
        getWindow().setFlags'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()
old='public void onCreate(Bundle b){super.onCreate(b);sp=getSharedPreferences("gp",0);'
new='public void onCreate(Bundle b){super.onCreate(b);SecurityGuard.hardenWebView();sp=getSharedPreferences("gp",0);'
assert old in s
s=s.replace(old,new,1)

anchor='void rememberPlayerReturnState(){playerRoundTrip=true;playerReturnScroll=mainScroll;playerReturnBody=body;playerReturnY=mainScroll==null?0:mainScroll.getScrollY();playerReturnNav=currentNavIndex;playerReturnTab=activeHomeTab==null?"":activeHomeTab;}'
assert anchor in s
s=s.replace(anchor,'boolean blockTamperedPlayback(){if(!SecurityGuard.tamperRisk())return false;showAppNotice("Ambiente de depuração ou instrumentação detectado.",true);return true;}\n '+anchor,1)
old='void playLiveInlineAllowed(JSONObject x){\n  if(x!=null){'
assert old in s
s=s.replace(old,'void playLiveInlineAllowed(JSONObject x){\n  if(blockTamperedPlayback())return;\n  if(x!=null){',1)
old='void launchOnlinePlayer(Intent in){if(in!=null&&!tvMode&&CastHelper.isConnected(this)){'
assert old in s
s=s.replace(old,'void launchOnlinePlayer(Intent in){if(blockTamperedPlayback())return;if(in!=null&&!tvMode&&CastHelper.isConnected(this)){',1)

old=''' JSONArray offlineArray(){try{return new JSONArray(sp.getString("offline_items","[]"));}catch(Exception e){return new JSONArray();}}
 void saveOfflineArray(JSONArray a){sp.edit().putString("offline_items",a.toString()).apply();}'''
new=''' JSONArray offlineArray(){try{JSONArray a=new JSONArray(sp.getString("offline_items","[]"));boolean dirty=false;for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o==null)continue;String legacy=o.optString("source_url","");JSONArray old=o.optJSONArray("source_urls");if(!legacy.isEmpty()||(old!=null&&old.length()>0)){JSONArray urls=old!=null?old:new JSONArray();if(urls.length()==0&&!legacy.isEmpty())urls.put(legacy);String blob=secureOfflineBlob(legacy,urls);if(!blob.isEmpty())o.put("source_blob",blob);o.remove("source_url");o.remove("source_urls");dirty=true;}}if(dirty)saveOfflineArray(a);return a;}catch(Exception e){return new JSONArray();}}
 void saveOfflineArray(JSONArray a){sp.edit().putString("offline_items",a.toString()).apply();}
 String secureOfflineBlob(String primary,JSONArray urls){try{JSONObject x=new JSONObject();x.put("primary",primary==null?"":primary);x.put("urls",urls==null?new JSONArray():urls);return SecretStore.encrypt(x.toString());}catch(Exception e){return "";}}
 JSONArray secureOfflineUrls(JSONObject o){JSONArray out=new JSONArray();try{String raw=SecretStore.decrypt(o==null?"":o.optString("source_blob",""));if(raw.isEmpty())return out;JSONObject x=new JSONObject(raw);JSONArray a=x.optJSONArray("urls");java.util.HashSet<String> seen=new java.util.HashSet<>();String p=x.optString("primary","");addOfflineUrl(out,seen,p);if(a!=null)for(int i=0;i<a.length();i++)addOfflineUrl(out,seen,a.optString(i,""));}catch(Exception ignored){}return out;}'''
assert old in s
s=s.replace(old,new,1)

old='''   JSONArray a=offlineArray();for(int i=a.length()-1;i>=0;i--){JSONObject old=a.optJSONObject(i);if(old!=null&&contentId.equals(old.optString("content_id"))&&videoType.equals(old.optString("video_type","1")))a.remove(i);}JSONObject o=new JSONObject();o.put("content_id",contentId);o.put("video_type",videoType);o.put("title",name);o.put("poster",poster);o.put("path",dest.getAbsolutePath());o.put("source_url",primary);o.put("source_urls",urls);o.put("status","queued");o.put("downloaded",0);o.put("total",0);o.put("created_at",System.currentTimeMillis());a.put(o);saveOfflineArray(a);
   startOfflineService(o);Toast.makeText(this,"Preparando download.",Toast.LENGTH_SHORT).show();'''
new='''   JSONArray a=offlineArray();for(int i=a.length()-1;i>=0;i--){JSONObject old=a.optJSONObject(i);if(old!=null&&contentId.equals(old.optString("content_id"))&&videoType.equals(old.optString("video_type","1")))a.remove(i);}JSONObject o=new JSONObject();o.put("content_id",contentId);o.put("video_type",videoType);o.put("title",name);o.put("poster",poster);o.put("path",dest.getAbsolutePath());String sourceBlob=secureOfflineBlob(primary,urls);if(!sourceBlob.isEmpty())o.put("source_blob",sourceBlob);o.put("status","queued");o.put("downloaded",0);o.put("total",0);o.put("created_at",System.currentTimeMillis());a.put(o);saveOfflineArray(a);
   startOfflineService(o,primary,urls);Toast.makeText(this,"Preparando download.",Toast.LENGTH_SHORT).show();'''
assert old in s
s=s.replace(old,new,1)

old=''' void startOfflineService(JSONObject o){try{Intent it=new Intent(this,OfflineDownloadService.class);it.setAction(OfflineDownloadService.ACTION_START);it.putExtra("url",o.optString("source_url",""));JSONArray urls=o.optJSONArray("source_urls");it.putExtra("urls",urls==null?"":urls.toString());it.putExtra("title",o.optString("title","Conteúdo"));it.putExtra("poster",o.optString("poster",""));it.putExtra("content_id",o.optString("content_id","0"));it.putExtra("video_type",o.optString("video_type","1"));it.putExtra("path",o.optString("path",""));if(Build.VERSION.SDK_INT>=26)startForegroundService(it);else startService(it);}catch(Exception e){Toast.makeText(this,"Não foi possível iniciar o download.",Toast.LENGTH_SHORT).show();}}
 void retryOffline(JSONObject old){if(old==null)return;try{JSONArray urls=old.optJSONArray("source_urls");if(urls==null||urls.length()==0){urls=new JSONArray();String u=old.optString("source_url","");if(!u.isEmpty())urls.put(u);}downloadOfflineUrls(urls,old.optString("title","Conteúdo"),old.optString("poster",""),old.optString("content_id","0"),old.optString("video_type","1"),old.optString("path",""));}catch(Exception ignored){}}'''
new=''' void startOfflineService(JSONObject o,String primary,JSONArray urls){try{Intent it=new Intent(this,OfflineDownloadService.class);it.setAction(OfflineDownloadService.ACTION_START);it.putExtra("url",primary==null?"":primary);it.putExtra("urls",urls==null?"":urls.toString());it.putExtra("title",o.optString("title","Conteúdo"));it.putExtra("poster",o.optString("poster",""));it.putExtra("content_id",o.optString("content_id","0"));it.putExtra("video_type",o.optString("video_type","1"));it.putExtra("path",o.optString("path",""));if(Build.VERSION.SDK_INT>=26)startForegroundService(it);else startService(it);}catch(Exception e){Toast.makeText(this,"Não foi possível iniciar o download.",Toast.LENGTH_SHORT).show();}}
 void retryOffline(JSONObject old){if(old==null)return;try{JSONArray urls=secureOfflineUrls(old);if(urls.length()==0){Toast.makeText(this,"Link protegido indisponível. Abra o conteúdo novamente para baixar.",Toast.LENGTH_SHORT).show();return;}downloadOfflineUrls(urls,old.optString("title","Conteúdo"),old.optString("poster",""),old.optString("content_id","0"),old.optString("video_type","1"),old.optString("path",""));}catch(Exception ignored){}}'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/PlayerActivity.java"
s=p.read_text()
old='public void onCreate(Bundle b){super.onCreate(b);tvMode=DeviceCompat.isTelevisionDevice(this);'
new='public void onCreate(Bundle b){super.onCreate(b);if(SecurityGuard.tamperRisk()){Toast.makeText(this,"Reprodução indisponível em ambiente instrumentado.",Toast.LENGTH_LONG).show();finish();return;}tvMode=DeviceCompat.isTelevisionDevice(this);'
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/OfflineDownloadService.java"
s=p.read_text()
old='String safeError(Exception e){String m=e==null?"":e.getMessage();if(m==null||m.trim().isEmpty())return "Falha no download";if(m.length()>100)m=m.substring(0,100);return m;}'
new='String safeError(Exception e){String m=e==null?"":e.getMessage();if(m!=null&&m.matches(".*HTTP [0-9]{3}.*")){java.util.regex.Matcher x=java.util.regex.Pattern.compile("HTTP [0-9]{3}").matcher(m);if(x.find())return x.group();}return "Falha de conexão com a fonte";}'
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""Proteção do APK sem proxy/relay e sem alterar a reprodução direta
URLs de download offline protegidas com Android Keystore
APK não depurável com R8/ofuscação habilitada
Logs de aplicação removidos e erros de rede sanitizados
WebView com depuração desativada e acesso a arquivo/conteúdo bloqueado
Network Security Config protege a API GreenPlay sem bloquear HTTP/HLS/TS das fontes
Proteção best-effort contra debugger/hooking sem bloquear VPN ou root/TV Box
"""+prior)
