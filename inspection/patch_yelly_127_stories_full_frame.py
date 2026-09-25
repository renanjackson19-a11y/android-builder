from pathlib import Path

root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")

# Stories must use the same full-frame video area as the main player.
old='''FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1);if(!tvMode)wp.setMargins(0,dp(64),0,dp(112));root.addView(web,wp);'''
new='''FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1);root.addView(web,wp);'''
if old not in s: raise SystemExit("stories web layout anchor missing")
s=s.replace(old,new,1)

old='''String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'><style>html,body{margin:0;width:100%;height:100%;background:transparent;overflow:hidden}#p{position:absolute;left:50%;top:50%;border:0;background:#000;transform:translate(-50%,-50%)}</style><script src='https://www.youtube.com/iframe_api'></script></head><body><div id='p'></div><script>var player,previewSent=false,previewLimit=120,tv="+(tvMode?"true":"false")+";function sizeP(){var p=document.getElementById('p');if(!p)return;var iw=window.innerWidth,ih=window.innerHeight,w=iw,h=ih;if(!tv){h=Math.min(ih,iw*16/9);w=Math.min(iw,h*9/16);}p.style.width=w+'px';p.style.height=h+'px';}sizeP();window.addEventListener('resize',sizeP);function finishPreview()'''
new='''String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'><style>html,body,#p{margin:0;padding:0;width:100%;height:100%;background:#000;overflow:hidden}#p{position:absolute;left:0;top:0;border:0}iframe{width:100%!important;height:100%!important;border:0}</style><script src='https://www.youtube.com/iframe_api'></script></head><body><div id='p'></div><script>var player,previewSent=false,previewLimit=120,tv="+(tvMode?"true":"false")+";function finishPreview()'''
if old not in s: raise SystemExit("stories player sizing anchor missing")
s=s.replace(old,new,1)

p.write_text(s,encoding="utf-8")

g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10026" not in t or "versionName '1.0.26'" not in t: raise SystemExit("wrong 1.0.26 base")
t=t.replace("versionCode 10026","versionCode 10027",1).replace("versionName '1.0.26'","versionName '1.0.27'",1)
g.write_text(t,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.27
- Stories agora usam a área de vídeo inteira, igual ao player principal.
- Removidas as margens que encolhiam o vídeo no Stories.
- O iframe ocupa 100% da largura e altura; as faixas pretas ficam apenas por cima, sem reduzir o tamanho dos atores.
- Mantidos swipe vertical, Favoritar, Comentários, Assistir agora e preview de até 2 minutos.
- Mantido o catálogo inicial aleatório da 1.0.26.
""",encoding="utf-8")
print("YELLY_127_STORIES_FULL_FRAME_OK")
