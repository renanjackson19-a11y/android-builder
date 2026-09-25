from pathlib import Path

root=Path("work")

def replace_method(text, marker, new_method):
    start=text.find(marker)
    if start<0:
        raise SystemExit("marker not found: "+marker)
    brace=text.find("{", start)
    if brace<0:
        raise SystemExit("opening brace not found: "+marker)
    depth=0
    end=None
    for i in range(brace,len(text)):
        ch=text[i]
        if ch=="{": depth+=1
        elif ch=="}":
            depth-=1
            if depth==0:
                end=i+1
                break
    if end is None:
        raise SystemExit("end not found: "+marker)
    return text[:start]+new_method+text[end:]

demo_expr='"android.resource://"+getPackageName()+"/"+R.raw.yelly_demo'

# Stories already use Media3/ExoPlayer in the 1.0.16 source.
stories=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=stories.read_text(encoding="utf-8")
s=replace_method(s,"    String playUrl(JSONObject x)","""    String playUrl(JSONObject x){String u=val(x,"video_1080","video_720","video_480","video_320","video_url","stream_url","url");if(!u.isEmpty())return u;return "android.resource://"+getPackageName()+"/"+R.raw.yelly_demo;}""")
stories.write_text(s,encoding="utf-8")

# Catalog detail: for this test build, open the same fully native Yelly player.
main=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
m=main.read_text(encoding="utf-8")
m=replace_method(m," void openYoutubeVideo(JSONObject source,String title,boolean restart)",""" void openYoutubeVideo(JSONObject source,String title,boolean restart){if(source==null)return;String u=detailPlayUrl(source);if(u.isEmpty())u="android.resource://"+getPackageName()+"/"+R.raw.yelly_demo;openPlayableUrl(source,title==null?"Yelly Doramas":title,false,u);}""")
main.write_text(m,encoding="utf-8")

# PlayerActivity is native Media3. No YouTube/WebView path is used.
player=root/"app/src/main/java/fun/greenplay/app/PlayerActivity.java"
p=player.read_text(encoding="utf-8")
if "new ExoPlayer.Builder" not in p or "PlayerView" not in p:
    raise SystemExit("native player missing")
player.write_text(p,encoding="utf-8")

manifest=root/"app/src/main/AndroidManifest.xml"
x=manifest.read_text(encoding="utf-8")
if "YouTubePlayerActivity" in x:
    raise SystemExit("YouTube player still registered in 1.0.16 base")
manifest.write_text(x,encoding="utf-8")

grad=root/"app/build.gradle"
g=grad.read_text(encoding="utf-8")
if "versionCode 10016" not in g or "versionName '1.0.16'" not in g:
    raise SystemExit("wrong base")
g=g.replace("versionCode 10016","versionCode 10020",1)
g=g.replace("versionName '1.0.16'","versionName '1.0.20'",1)
grad.write_text(g,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.20 - TESTE PLAYER NATIVO
- Remove completamente o player/WebView do YouTube do caminho de reprodução.
- Stories usam Media3/ExoPlayer do próprio Yelly.
- Tela Assistir usa PlayerActivity nativo do Yelly.
- Para demonstrar o visual antes de cadastrar a nova fonte, itens sem stream_url usam um vídeo demo local empacotado no APK.
- Títulos, capas, favoritos e comentários continuam vindo do catálogo Yelly.
- Quando a nova fonte for cadastrada, basta fornecer stream_url/MP4/HLS; o player nativo já prioriza a URL real automaticamente.
""",encoding="utf-8")
print("YELLY_120_NATIVE_DEMO_OK")
