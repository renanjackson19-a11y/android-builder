from pathlib import Path
import re

ROOT=Path("work")
APP=ROOT/"app"
JAVA=APP/"src/main/java/fun/greenplay/app"
RES=APP/"src/main/res"
MANIFEST=APP/"src/main/AndroidManifest.xml"
GRADLE=APP/"build.gradle"
PROGUARD=APP/"proguard-rules.pro"

# Exact base: 5.28.70.
g=GRADLE.read_text()
assert "versionCode 52870" in g and "versionName '5.28.70'" in g
g=g.replace("versionCode 52870","versionCode 52871",1)
g=g.replace("versionName '5.28.70'","versionName '5.28.71'",1)
old_debug="""        debug {
            applicationIdSuffix '.debug'
            signingConfig signingConfigs.stableDebug
        }"""
new_debug="""        debug {
            applicationIdSuffix '.debug'
            signingConfig signingConfigs.stableDebug
            debuggable false
            jniDebuggable false
            minifyEnabled true
            shrinkResources false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }"""
assert old_debug in g
g=g.replace(old_debug,new_debug,1)
GRADLE.write_text(g)

# Harden ProGuard/R8. Do not keep the whole app package: that defeated obfuscation.
PROGUARD.write_text(r'''# GreenPlay APK hardening: keep only runtime entrypoints/bridges that genuinely
# need stable reflection/manifest access. Android Gradle/R8 preserves manifest
# components; Cast OptionsProvider is also referenced through manifest metadata.
-keep class fun.greenplay.app.CastOptionsProvider { *; }
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
-keepattributes *Annotation*,Signature,InnerClasses,EnclosingMethod
-renamesourcefileattribute SourceFile

# Prevent API/media URLs or exception text from leaking through app Log calls.
-assumenosideeffects class android.util.Log {
    public static *** v(...);
    public static *** d(...);
    public static *** i(...);
    public static *** w(...);
    public static *** e(...);
    public static *** wtf(...);
}

# Keep the runtime secret decoder intact so R8 does not constant-fold the
# reconstructed values back into a plain string in classes.dex.
-keep,allowobfuscation class fun.greenplay.app.Secrets { *; }
''')

# Extract existing API constants at build time, then remove their plaintext
# literals from the generated app source. No secret is copied into this patch.
api_path=JAVA/"Api.java"
api=api_path.read_text()
mb=re.search(r'static final String BASE="([^"]+)";',api)
mt=re.search(r'static final String TOKEN="([^"]+)";',api)
assert mb and mt
base=mb.group(1)
token=mt.group(1)

def enc_arrays(value, seed):
    keys=[]
    data=[]
    for i,ch in enumerate(value):
        k=((seed + i*73 + (i*i*11)) % 223) + 19
        keys.append(k)
        data.append(ord(ch)^k)
    return data,keys

bd,bk=enc_arrays(base,41)
td,tk=enc_arrays(token,97)

def ints(a): return ",".join(str(x) for x in a)

(JAVA/"Secrets.java").write_text(f'''package fun.greenplay.app;

final class Secrets {{
    private Secrets(){{}}
    private static final int[] B={{{ints(bd)}}};
    private static final int[] BK={{{ints(bk)}}};
    private static final int[] T={{{ints(td)}}};
    private static final int[] TK={{{ints(tk)}}};
    private static String decode(int[] data,int[] key){{
        char[] out=new char[data.length];
        for(int i=0;i<data.length;i++)out[i]=(char)(data[i]^key[i]);
        return new String(out);
    }}
    static String apiBase(){{return decode(B,BK);}}
    static String apiToken(){{return decode(T,TK);}}
}}
''')

api=api[:mb.start()]+'static final String BASE=Secrets.apiBase();'+api[mb.end():]
mt2=re.search(r'static final String TOKEN="([^"]+)";',api)
assert mt2
api=api[:mt2.start()]+'static final String TOKEN=Secrets.apiToken();'+api[mt2.end():]
# Never propagate raw networking exception messages to screens; they can contain
# hostnames, URLs or local network details.
api=api.replace('catch(Exception e){String msg=e.getMessage();MAIN.post(()->cb.err(msg));}',
                'catch(Exception e){String msg="Falha de conexão";MAIN.post(()->cb.err(msg));}')
api_path.write_text(api)

# Android Keystore-backed string protection + encrypted catalog snapshots.
(JAVA/"SecureStore.java").write_text(r'''package fun.greenplay.app;

import android.content.Context;
import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyProperties;
import android.util.Base64;
import java.io.*;
import java.security.KeyStore;
import java.util.Arrays;
import javax.crypto.*;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.SecretKey;

final class SecureStore {
    static final String PREFIX="gpe1:";
    private static final String ALIAS="greenplay_store_v1";
    private static final byte[] MAGIC=new byte[]{'G','P','F','1'};
    private static volatile SecretKey cached;

    private SecureStore(){}

    static synchronized SecretKey key() throws Exception {
        if(cached!=null)return cached;
        KeyStore ks=KeyStore.getInstance("AndroidKeyStore");
        ks.load(null);
        SecretKey k=(SecretKey)ks.getKey(ALIAS,null);
        if(k==null){
            KeyGenerator kg=KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES,"AndroidKeyStore");
            KeyGenParameterSpec spec=new KeyGenParameterSpec.Builder(
                    ALIAS,KeyProperties.PURPOSE_ENCRYPT|KeyProperties.PURPOSE_DECRYPT)
                    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                    .setRandomizedEncryptionRequired(true)
                    .build();
            kg.init(spec);
            k=kg.generateKey();
        }
        cached=k;
        return k;
    }

    static String seal(String plain){
        if(plain==null)return null;
        try{
            Cipher c=Cipher.getInstance("AES/GCM/NoPadding");
            c.init(Cipher.ENCRYPT_MODE,key());
            byte[] iv=c.getIV();
            byte[] ct=c.doFinal(plain.getBytes(java.nio.charset.StandardCharsets.UTF_8));
            ByteArrayOutputStream b=new ByteArrayOutputStream(iv.length+ct.length+1);
            b.write(iv.length);b.write(iv);b.write(ct);
            return PREFIX+Base64.encodeToString(b.toByteArray(),Base64.NO_WRAP);
        }catch(Throwable e){return null;}
    }

    static String open(String raw){
        if(raw==null)return null;
        if(!raw.startsWith(PREFIX))return raw;
        try{
            byte[] all=Base64.decode(raw.substring(PREFIX.length()),Base64.NO_WRAP);
            if(all.length<14)return null;
            int n=all[0]&0xff;
            if(n<12||n>32||all.length<=1+n)return null;
            byte[] iv=Arrays.copyOfRange(all,1,1+n);
            byte[] ct=Arrays.copyOfRange(all,1+n,all.length);
            Cipher c=Cipher.getInstance("AES/GCM/NoPadding");
            c.init(Cipher.DECRYPT_MODE,key(),new GCMParameterSpec(128,iv));
            return new String(c.doFinal(ct),java.nio.charset.StandardCharsets.UTF_8);
        }catch(Throwable e){return null;}
    }

    static OutputStream encryptedOutput(OutputStream raw) throws Exception {
        Cipher c=Cipher.getInstance("AES/GCM/NoPadding");
        c.init(Cipher.ENCRYPT_MODE,key());
        byte[] iv=c.getIV();
        raw.write(MAGIC);raw.write(iv.length);raw.write(iv);
        return new CipherOutputStream(raw,c);
    }

    static InputStream encryptedInput(InputStream raw) throws Exception {
        try{
            byte[] magic=new byte[4];
            if(readFully(raw,magic)!=4||!Arrays.equals(magic,MAGIC))throw new IOException("legacy cache");
            int n=raw.read();
            if(n<12||n>32)throw new IOException("cache inválido");
            byte[] iv=new byte[n];
            if(readFully(raw,iv)!=n)throw new EOFException("cache truncado");
            Cipher c=Cipher.getInstance("AES/GCM/NoPadding");
            c.init(Cipher.DECRYPT_MODE,key(),new GCMParameterSpec(128,iv));
            return new CipherInputStream(raw,c);
        }catch(Exception e){
            try{raw.close();}catch(Exception ignored){}
            throw e;
        }
    }

    private static int readFully(InputStream in,byte[] b)throws IOException{
        int off=0,n;
        while(off<b.length&&(n=in.read(b,off,b.length-off))>0)off+=n;
        return off;
    }

    static void scrubLegacyCatalog(Context context){
        try{
            File dir=new File(context.getFilesDir(),"gp_catalog");
            File[] files=dir.listFiles();
            if(files==null)return;
            for(File f:files){
                if(f==null||!f.isFile())continue;
                boolean secure=false;
                try(FileInputStream in=new FileInputStream(f)){
                    byte[] m=new byte[4];
                    secure=readFully(in,m)==4&&Arrays.equals(m,MAGIC);
                }catch(Throwable ignored){}
                if(!secure)try{f.delete();}catch(Throwable ignored){}
            }
        }catch(Throwable ignored){}
    }
}
''')

# Transparent encrypted SharedPreferences wrapper. All String values in "gp"
# are encrypted at rest. Legacy plaintext values are migrated on first read.
(JAVA/"SecurePreferences.java").write_text(r'''package fun.greenplay.app;

import android.content.Context;
import android.content.SharedPreferences;
import java.util.*;

final class SecurePreferences implements SharedPreferences {
    private final SharedPreferences base;
    private SecurePreferences(SharedPreferences b){base=b;}
    static SharedPreferences get(Context c){return new SecurePreferences(c.getSharedPreferences("gp",Context.MODE_PRIVATE));}

    private String decode(String key,String raw,String def){
        if(raw==null)return def;
        if(raw.startsWith(SecureStore.PREFIX)){
            String p=SecureStore.open(raw);
            return p==null?def:p;
        }
        String sealed=SecureStore.seal(raw);
        if(sealed!=null)base.edit().putString(key,sealed).apply();
        else base.edit().remove(key).apply();
        return raw;
    }

    @Override public Map<String,?> getAll(){
        Map<String,?> src=base.getAll();Map<String,Object> out=new HashMap<>();
        for(Map.Entry<String,?> e:src.entrySet()){
            Object v=e.getValue();
            if(v instanceof String)v=decode(e.getKey(),(String)v,null);
            else if(v instanceof Set){
                Set<String> z=new HashSet<>();
                for(Object x:(Set<?>)v)if(x instanceof String){String p=SecureStore.open((String)x);if(p!=null)z.add(p);}
                v=z;
            }
            out.put(e.getKey(),v);
        }
        return out;
    }
    @Override public String getString(String key,String def){return decode(key,base.getString(key,null),def);}
    @Override public Set<String> getStringSet(String key,Set<String> def){
        Set<String> src=base.getStringSet(key,null);if(src==null)return def;
        Set<String> out=new HashSet<>();for(String x:src){String p=SecureStore.open(x);if(p!=null)out.add(p);}return out;
    }
    @Override public int getInt(String k,int d){return base.getInt(k,d);}
    @Override public long getLong(String k,long d){return base.getLong(k,d);}
    @Override public float getFloat(String k,float d){return base.getFloat(k,d);}
    @Override public boolean getBoolean(String k,boolean d){return base.getBoolean(k,d);}
    @Override public boolean contains(String k){return base.contains(k);}
    @Override public Editor edit(){return new E(base.edit());}
    @Override public void registerOnSharedPreferenceChangeListener(OnSharedPreferenceChangeListener l){base.registerOnSharedPreferenceChangeListener(l);}
    @Override public void unregisterOnSharedPreferenceChangeListener(OnSharedPreferenceChangeListener l){base.unregisterOnSharedPreferenceChangeListener(l);}

    static final class E implements Editor{
        final Editor e;E(Editor x){e=x;}
        @Override public Editor putString(String k,String v){if(v==null)return remove(k);String s=SecureStore.seal(v);if(s==null)return remove(k);e.putString(k,s);return this;}
        @Override public Editor putStringSet(String k,Set<String> v){if(v==null)return remove(k);Set<String> out=new HashSet<>();for(String x:v){String s=SecureStore.seal(x);if(s!=null)out.add(s);}e.putStringSet(k,out);return this;}
        @Override public Editor putInt(String k,int v){e.putInt(k,v);return this;}
        @Override public Editor putLong(String k,long v){e.putLong(k,v);return this;}
        @Override public Editor putFloat(String k,float v){e.putFloat(k,v);return this;}
        @Override public Editor putBoolean(String k,boolean v){e.putBoolean(k,v);return this;}
        @Override public Editor remove(String k){e.remove(k);return this;}
        @Override public Editor clear(){e.clear();return this;}
        @Override public boolean commit(){return e.commit();}
        @Override public void apply(){e.apply();}
    }
}
''')

# Conservative anti-debug / anti-hook checks. Root alone is intentionally NOT
# blocked because Android TV/TV Box compatibility has priority.
(JAVA/"RuntimeGuard.java").write_text(r'''package fun.greenplay.app;

import android.os.Debug;
import java.io.*;

final class RuntimeGuard {
    private RuntimeGuard(){}
    static boolean blocked(){
        try{if(Debug.isDebuggerConnected()||Debug.waitingForDebugger())return true;}catch(Throwable ignored){}
        if(traced())return true;
        String[] classes={"de.robv.android.xposed.XposedBridge","com.saurik.substrate.MS$2"};
        for(String n:classes)try{Class.forName(n,false,RuntimeGuard.class.getClassLoader());return true;}catch(Throwable ignored){}
        try(BufferedReader r=new BufferedReader(new FileReader("/proc/self/maps"))){
            String line;
            while((line=r.readLine())!=null){
                String x=line.toLowerCase(java.util.Locale.ROOT);
                if(x.contains("frida-agent")||x.contains("libfrida")||x.contains("xposed")||x.contains("substrate"))return true;
            }
        }catch(Throwable ignored){}
        return false;
    }
    static boolean traced(){
        try(BufferedReader r=new BufferedReader(new FileReader("/proc/self/status"))){
            String line;while((line=r.readLine())!=null)if(line.startsWith("TracerPid:")){
                return Integer.parseInt(line.substring(line.indexOf(':')+1).trim())>0;
            }
        }catch(Throwable ignored){}
        return false;
    }
}
''')

# Central switches: WebView debugging off and Media3 internal logging off when
# the installed Media3 version exposes that switch.
(JAVA/"AppSecurity.java").write_text(r'''package fun.greenplay.app;

final class AppSecurity {
    private AppSecurity(){}
    static void apply(){
        try{android.webkit.WebView.setWebContentsDebuggingEnabled(false);}catch(Throwable ignored){}
        try{
            Class<?> c=Class.forName("androidx.media3.common.util.Log");
            java.lang.reflect.Field f=c.getField("LOG_LEVEL_OFF");
            java.lang.reflect.Method m=c.getMethod("setLogLevel",int.class);
            m.invoke(null,f.getInt(null));
        }catch(Throwable ignored){}
    }
}
''')

# Move all uses of the main gp preferences onto the encrypted wrapper.
for name in ["MainActivity.java","PlayerActivity.java","YouTubePlayerActivity.java","OfflineDownloadService.java"]:
    p=JAVA/name
    s=p.read_text()
    s=s.replace('getSharedPreferences("gp",0)','SecurePreferences.get(this)')
    s=s.replace('getSharedPreferences("gp",MODE_PRIVATE)','SecurePreferences.get(this)')
    p.write_text(s)

# Protect activity startup without touching normal media URL selection/playback.
for name in ["MainActivity.java","PlayerActivity.java","YouTubePlayerActivity.java"]:
    p=JAVA/name
    s=p.read_text()
    needle="super.onCreate(b);"
    assert needle in s, name
    add='super.onCreate(b);AppSecurity.apply();if(RuntimeGuard.blocked()){android.widget.Toast.makeText(this,"Ambiente de depuração não suportado.",android.widget.Toast.LENGTH_LONG).show();finish();return;}'
    s=s.replace(needle,add,1)
    p.write_text(s)

# Main activity: purge old plaintext catalog files, then only write/read
# encrypted gzip streams. The media objects remain identical in memory, so
# direct HLS/M3U8/TS/MP4 playback is untouched.
main=JAVA/"MainActivity.java"
s=main.read_text()
needle='sp=SecurePreferences.get(this);'
assert needle in s
s=s.replace(needle,'sp=SecurePreferences.get(this);SecureStore.scrubLegacyCatalog(this);',1)

old='java.io.OutputStream fos=new java.io.FileOutputStream(tmp);java.util.zip.GZIPOutputStream gz=new java.util.zip.GZIPOutputStream(fos,32768);'
new='java.io.OutputStream fos=new java.io.FileOutputStream(tmp);java.io.OutputStream secureOut=SecureStore.encryptedOutput(fos);java.util.zip.GZIPOutputStream gz=new java.util.zip.GZIPOutputStream(secureOut,32768);'
assert old in s
s=s.replace(old,new,1)

old='java.io.InputStream in=new java.util.zip.GZIPInputStream(new java.io.BufferedInputStream(new java.io.FileInputStream(f),32768),32768);'
new='java.io.InputStream rawIn=new java.io.BufferedInputStream(new java.io.FileInputStream(f),32768);java.io.InputStream secureIn=SecureStore.encryptedInput(rawIn);java.io.InputStream in=new java.util.zip.GZIPInputStream(secureIn,32768);'
assert old in s
s=s.replace(old,new,1)
main.write_text(s)

# Remove explicit app logging calls (R8 also strips any that remain).
for p in JAVA.glob("*.java"):
    s=p.read_text()
    s=re.sub(r'android\.util\.Log\.[vdiew]\([^;]*\);','',s)
    p.write_text(s)

# Manifest: API connection is pinned to system trust only, but provider playback
# remains cleartext-compatible and user-CA-compatible to avoid breaking IPTV
# sources that still use HTTP or unusual TLS.
m=MANIFEST.read_text()
old='android:usesCleartextTraffic="true" android:allowBackup="false"'
new='android:usesCleartextTraffic="true" android:networkSecurityConfig="@xml/network_security_config" android:allowBackup="false"'
assert old in m
m=m.replace(old,new,1)
m=m.replace('<activity android:name=".PlayerActivity" ', '<activity android:name=".PlayerActivity" android:exported="false" ',1)
m=m.replace('<activity android:name=".YouTubePlayerActivity" ', '<activity android:name=".YouTubePlayerActivity" android:exported="false" ',1)
MANIFEST.write_text(m)

(RES/"xml").mkdir(parents=True,exist_ok=True)
(RES/"xml/network_security_config.xml").write_text('''<?xml version="1.0" encoding="utf-8"?>
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

# Release notes included in APK metadata.
notes=APP/"RELEASE_NOTES.txt"
old_notes=notes.read_text() if notes.exists() else ""
extra='''\n5.28.71 - Proteção do APK sem relay\n- Reprodução continua direta da fonte; nenhum proxy/relay de mídia.\n- SharedPreferences de texto cifradas com Android Keystore (AES-GCM).\n- Snapshot persistente do catálogo cifrado; cache antigo em texto é descartado.\n- R8/ofuscação no APK debug distribuído e debuggable=false.\n- WebView debugging e logs do app desativados.\n- API GreenPlay sem mensagens de erro contendo host/URL e com confiança TLS restrita ao sistema.\n- Anti-debug/anti-hook conservador; root sozinho não bloqueia TV Box.\n'''
if "5.28.71 - Proteção do APK sem relay" not in old_notes:
    notes.write_text(old_notes.rstrip()+extra)

# Safety assertions: preserve direct playback and do not reintroduce VPN blocking/relay.
alljava="\n".join(p.read_text() for p in JAVA.glob("*.java"))
assert 'TRANSPORT_VPN' not in alljava and 'TYPE_VPN' not in alljava
assert 'greenplay-media-proxy' not in alljava
assert 'blockProtectedPlayback' not in alljava
assert 'MediaItem.Builder().setUri' in (JAVA/"PlayerActivity.java").read_text()
assert 'setUri(Uri.parse(url))' in (JAVA/"MainActivity.java").read_text()
legacy_prefs="\n".join(p.read_text() for p in JAVA.glob("*.java") if p.name!="SecurePreferences.java")
assert 'getSharedPreferences("gp"' not in legacy_prefs
assert token not in alljava
assert base not in (JAVA/"Api.java").read_text()
