from pathlib import Path

root=Path("work")

# Stories: remove the big visible shadow bands. Hide YouTube chrome by cropping the
# embedded player slightly instead of painting dark strips over the UI.
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")
s=s.replace("ImageView poster,logoTop;View shade,swipe,ytTopMask,ytBottomMask;","ImageView poster,logoTop;View shade,swipe;",1)

old="""FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1);if(!tvMode)wp.setMargins(0,dp(64),0,dp(112));root.addView(web,wp);
  ytTopMask=new View(this);ytTopMask.setBackgroundColor(0xee14080f);FrameLayout.LayoutParams ytp=new FrameLayout.LayoutParams(-1,dp(76),Gravity.TOP);ytp.setMargins(0,dp(64),0,0);root.addView(ytTopMask,ytp);
  ytBottomMask=new View(this);ytBottomMask.setBackgroundColor(0xee14080f);FrameLayout.LayoutParams ybp=new FrameLayout.LayoutParams(-1,dp(64),Gravity.BOTTOM);ybp.setMargins(0,0,0,dp(112));root.addView(ytBottomMask,ybp);"""
new="""FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1);root.addView(web,wp);"""
if old not in s:
    raise SystemExit("Stories mask block not found")
s=s.replace(old,new,1)

old_css="#p{position:absolute;left:50%;top:50%;border:0;background:#000;transform:translate(-50%,-50%)}"
new_css="#p{position:absolute;left:50%;top:50%;border:0;background:transparent;transform:translate(-50%,-50%);overflow:hidden}#p iframe{position:absolute!important;left:0!important;top:-48px!important;width:100%!important;height:calc(100% + 96px)!important;border:0!important}"
if old_css not in s:
    raise SystemExit("Stories CSS anchor not found")
s=s.replace(old_css,new_css,1)
p.write_text(s,encoding="utf-8")

# Full miniseries player: same strategy, no visible dark bands.
p=root/"app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java"
y=p.read_text(encoding="utf-8")
y=y.replace("View touchShield,ytTopMask,ytBottomMask,ytBrandMask;","View touchShield;",1)
old="""FrameLayout.LayoutParams wlp=new FrameLayout.LayoutParams(-1,-1);if(!tvMode)wlp.setMargins(0,dp(68),0,dp(106));root.addView(web,wlp);
        if(!tvMode){
            ytTopMask=new View(this);ytTopMask.setBackground(bg(0xee14080f,0));FrameLayout.LayoutParams tlp=new FrameLayout.LayoutParams(-1,dp(74),Gravity.TOP);tlp.setMargins(0,dp(68),0,0);root.addView(ytTopMask,tlp);
            ytBottomMask=new View(this);ytBottomMask.setBackground(bg(0xee14080f,0));FrameLayout.LayoutParams blp=new FrameLayout.LayoutParams(-1,dp(62),Gravity.BOTTOM);blp.setMargins(0,0,0,dp(106));root.addView(ytBottomMask,blp);
            ytBrandMask=new View(this);ytBrandMask.setBackground(bg(0xee14080f,12));FrameLayout.LayoutParams brp=new FrameLayout.LayoutParams(dp(124),dp(48),Gravity.RIGHT|Gravity.BOTTOM);brp.setMargins(0,0,dp(2),dp(106));root.addView(ytBrandMask,brp);
        }"""
new="""root.addView(web,new FrameLayout.LayoutParams(-1,-1));"""
if old not in y:
    raise SystemExit("Full player mask block not found")
y=y.replace(old,new,1)

old_css="#p{position:absolute;left:50%;top:50%;border:0;background:#000;transform:translate(-50%,-50%)}"
new_css="#p{position:absolute;left:50%;top:50%;border:0;background:transparent;transform:translate(-50%,-50%);overflow:hidden}#p iframe{position:absolute!important;left:0!important;top:-52px!important;width:100%!important;height:calc(100% + 104px)!important;border:0!important}"
if old_css not in y:
    raise SystemExit("Full player CSS anchor not found")
y=y.replace(old_css,new_css,1)
p.write_text(y,encoding="utf-8")

grad=root/"app/build.gradle"
g=grad.read_text(encoding="utf-8")
if "versionCode 10017" not in g or "versionName '1.0.17'" not in g:
    raise SystemExit("wrong 1.0.17 base")
g=g.replace("versionCode 10017","versionCode 10018",1)
g=g.replace("versionName '1.0.17'","versionName '1.0.18'",1)
grad.write_text(g,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.18
- Removidas as faixas/sombras escuras grandes que apareciam sobre o Story.
- O player embutido agora é recortado internamente para esconder os elementos do YouTube sem colocar faixa visível na tela.
- Mantidos URL/ID ocultos, feed correto de minisséries, banner Yelly, Favoritar, Comentários e Assistir agora.
- Player completo também não usa mais as faixas escuras grandes.
""",encoding="utf-8")
print("YELLY_118_REMOVE_SHADOW_BANDS_OK")
