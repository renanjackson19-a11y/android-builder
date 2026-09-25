from pathlib import Path

root=Path("work")
app=root/"app/src/main/java/fun/greenplay/app"

# Use the same dorama playback mechanism as GreenPlay: WebView + YouTube IFrame API,
# touch blocked from the embedded player and app-owned controls layered above it.
src=Path("inspection/YellyGreenPlayDoramaPlayer.java")
(app/"YouTubePlayerActivity.java").write_text(src.read_text(encoding="utf-8"),encoding="utf-8")

# Keep Yelly presentation clean: don't prefix titles/details with source name.
p=app/"MainActivity.java"
m=p.read_text(encoding="utf-8")
m=m.replace('if(!x.optString("youtube_id","").trim().isEmpty()||"youtube".equalsIgnoreCase(x.optString("source",""))||"greenshorts".equalsIgnoreCase(x.optString("source","")))return "YouTube";',
            'if(!x.optString("youtube_id","").trim().isEmpty()||"youtube".equalsIgnoreCase(x.optString("source",""))||"greenshorts".equalsIgnoreCase(x.optString("source","")))return "Yelly";')
m=m.replace('if(isYoutube){View srcBadge=detailIdBadge("Fonte:  "+doramaSourceName(source));LinearLayout.LayoutParams slp0=new LinearLayout.LayoutParams(-2,-2);slp0.setMargins(0,dp(2),0,dp(12));host.addView(srcBadge,slp0);}',
            'if(isYoutube&&isExternalDorama(source)){View srcBadge=detailIdBadge("Fonte:  "+doramaSourceName(source));LinearLayout.LayoutParams slp0=new LinearLayout.LayoutParams(-2,-2);slp0.setMargins(0,dp(2),0,dp(12));host.addView(srcBadge,slp0);}')
p.write_text(m,encoding="utf-8")

p=app/"StoriesActivity.java"
s=p.read_text(encoding="utf-8")
s=s.replace('title.setText("YouTube  •  "+nm);','title.setText(nm);')
p.write_text(s,encoding="utf-8")

manifest=root/"app/src/main/AndroidManifest.xml"
x=manifest.read_text(encoding="utf-8")
if "YouTubePlayerActivity" not in x:
    x=x.replace('  <activity android:name=".PlayerActivity"','  <activity android:name=".YouTubePlayerActivity" android:exported="false" android:screenOrientation="unspecified" android:configChanges="orientation|screenSize"/>\n  <activity android:name=".PlayerActivity"',1)
manifest.write_text(x,encoding="utf-8")

g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10022" not in t or "versionName '1.0.22'" not in t:
    raise SystemExit("wrong base")
t=t.replace("versionCode 10022","versionCode 10023",1).replace("versionName '1.0.22'","versionName '1.0.23'",1)
g.write_text(t,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.23
- Reprodução dos doramas do catálogo YouTube passou a seguir o mesmo mecanismo usado no GreenPlay.
- Player incorporado via YouTube IFrame API em WebView.
- Toque não é repassado ao player incorporado; controles visuais ficam por conta do Yelly.
- Controles: voltar, -10s, play/pause, +10s e barra de progresso.
- Controle remoto: OK play/pause, esquerda/direita -10/+10s.
- Removido o texto visível 'Fonte: YouTube' da interface do Yelly.
- Mantidos os demais catálogos sem alterar o aplicativo GreenPlay.
""",encoding="utf-8")
print("YELLY_123_GREENPLAY_DORAMA_FLOW_OK")
