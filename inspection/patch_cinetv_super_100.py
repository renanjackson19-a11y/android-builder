from pathlib import Path
import re, json

root=Path("work")
java_root=root/"app/src/main/java"
res=root/"app/src/main/res"
gradle=root/"app/build.gradle"
manifest=root/"app/src/main/AndroidManifest.xml"

# Change the Android package/domain without touching internal method/resource identifiers.
for p in list(java_root.rglob("*.java")) + list(res.rglob("*.xml")) + [manifest]:
    s=p.read_text(encoding="utf-8")
    s=s.replace("fun.greenplay.app","site.clickaqui.cinetv")
    s=s.replace("greenplay.fun","cinetv.clickaqui.site")
    p.write_text(s,encoding="utf-8")

# Replace old brand only inside Java string literals. Internal identifiers may keep
# their historical names because they are never visible to the franchise/customer.
string_re=re.compile(r'"(?:\\.|[^"\\])*"')
for p in java_root.rglob("*.java"):
    s=p.read_text(encoding="utf-8")
    def repl(m):
        x=m.group(0)
        return x.replace("Green Play","CineTV Super").replace("GreenPlay","CineTV Super")
    p.write_text(string_re.sub(repl,s),encoding="utf-8")

# Keep app runtime on the franchise API only.
secret=java_root/"fun/greenplay/app/SecretStrings.java"
secret.write_text("""package site.clickaqui.cinetv;
final class SecretStrings{
 private SecretStrings(){}
 static String apiBase(){int[]v={50,46,46,42,41,96,117,117,57,51,52,63,46,44,116,57,54,51,57,49,59,43,47,51,116,41,51,46,63,117,59,42,51,117,62,46,54,51,44,63,117};char[]c=new char[v.length];for(int i=0;i<v.length;i++)c[i]=(char)(v[i]^0x5a);return new String(c);}
 static String apiToken(){int[]v={15,15,85,3,6,15,5,5,7,83,3,83,15,83,7,83,2,3,3,2,5,83,5,14,85,86,83,14,5,3,86,5,83,85,84,5,4,6,85,81,86,7,0,82,0,84,7,82};char[]c=new char[v.length];for(int i=0;i<v.length;i++)c[i]=(char)(v[i]^0x37);return new String(c);}
}
""",encoding="utf-8")

# API bootstrap route must pass through the franchise proxy.
main=java_root/"fun/greenplay/app/MainActivity.java"
s=main.read_text(encoding="utf-8")
s=s.replace('"bootstrap_home/index.php"','"bootstrap_home"')
main.write_text(s,encoding="utf-8")

# Package/version are fully independent from GreenPlay.
g=gradle.read_text(encoding="utf-8")
g=g.replace("namespace 'fun.greenplay.app'","namespace 'site.clickaqui.cinetv'")
g=g.replace("applicationId 'fun.greenplay.app'","applicationId 'site.clickaqui.cinetv'")
g=g.replace("versionCode 52899","versionCode 100")
g=g.replace("versionName '5.28.99'","versionName '1.0.0'")
g=g.replace("            applicationIdSuffix '.debug'\n","")
g=g.replace("GreenPlay","CineTV Super")
gradle.write_text(g,encoding="utf-8")

# Manifest resources use CineTV names.
m=manifest.read_text(encoding="utf-8")
m=m.replace('android:label="CineTV Super" android:icon="@drawable/greenplay_app_icon" android:roundIcon="@drawable/greenplay_app_icon"',
            'android:label="CineTV Super" android:icon="@drawable/cinetv_app_icon" android:roundIcon="@drawable/cinetv_app_icon"')
m=m.replace('android:banner="@drawable/tv_banner"','android:banner="@drawable/cinetv_tv_banner"')
manifest.write_text(m,encoding="utf-8")

# Local logo/background resource names.
s=main.read_text(encoding="utf-8")
s=s.replace("R.drawable.greenplay_logo_fallback","R.drawable.cinetv_logo_fallback")
s=s.replace("R.drawable.login_cinema_bg","R.drawable.cinetv_login_bg")
main.write_text(s,encoding="utf-8")

# Remove obsolete branded drawable files before workflow installs CineTV assets.
for name in ["greenplay_app_icon.png","greenplay_logo_fallback.png","tv_banner.png","login_cinema_bg.png"]:
    p=res/"drawable-nodpi"/name
    if p.exists(): p.unlink()

# Brand strings and network security.
(res/"values/strings.xml").write_text('<resources><string name="app_name">CineTV Super</string></resources>\n',encoding="utf-8")
net=res/"xml/network_security_config.xml"
ns=net.read_text(encoding="utf-8").replace("greenplay.fun","cinetv.clickaqui.site")
net.write_text(ns,encoding="utf-8")

# Fresh release notes: no GreenPlay history in the franchise APK metadata.
(root/"app/RELEASE_NOTES.txt").write_text("""CineTV Super 1.0.0
Aplicativo oficial CineTV Super.
Identidade visual CineTV Super em celular, Android TV e TV Box.
Painel e API exclusivos da franquia.
Catálogo integrado à matriz sem exibir configuração de provedores no painel da franquia.
Correções de estabilidade do teclado e controle remoto em TV preservadas.
""",encoding="utf-8")

# Verify public labels, domain and release notes use only the franchise identity.
checks=[manifest,res/"values/strings.xml",root/"app/RELEASE_NOTES.txt"]
for p in checks:
    t=p.read_text(encoding="utf-8",errors="ignore")
    if "GreenPlay" in t or "Green Play" in t or "greenplay.fun" in t:
        raise SystemExit("Old visible branding remains in "+str(p))
print("CineTV Super 1.0.0 branding/API patch applied")
