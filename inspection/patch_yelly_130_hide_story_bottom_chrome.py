from pathlib import Path

root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")

# Increase bottom cover so the native YouTube strip is fully hidden.
old='''  int storyBottomMaskH=Math.max(dp(64),Math.min(dp(110),(int)(storyScreenH*0.11f)));'''
new='''  int storyBottomMaskH=(int)(storyScreenH*0.17f);'''
if old not in s: raise SystemExit("bottom mask height anchor missing")
s=s.replace(old,new,1)

# Keep both masks attached to the moving story during swipe, so the external
# bottom strip cannot escape above the fixed mask while the WebView moves.
old=''' void setSwipeOffset(float y){float lim=Math.max(1,root.getHeight());float v=Math.max(-lim,Math.min(lim,y));if(web!=null){web.animate().cancel();web.setAlpha(storyReady?1f:0f);web.setTranslationY(v);}if(shade!=null)shade.setTranslationY(v);if(info!=null)info.setTranslationY(v);if(actions!=null)actions.setTranslationY(v);}'''
new=''' void setSwipeOffset(float y){float lim=Math.max(1,root.getHeight());float v=Math.max(-lim,Math.min(lim,y));if(web!=null){web.animate().cancel();web.setAlpha(storyReady?1f:0f);web.setTranslationY(v);}if(ytTopMask!=null)ytTopMask.setTranslationY(v);if(ytBottomMask!=null)ytBottomMask.setTranslationY(v);if(shade!=null)shade.setTranslationY(v);if(info!=null)info.setTranslationY(v);if(actions!=null)actions.setTranslationY(v);}'''
if old not in s: raise SystemExit("setSwipeOffset anchor missing")
s=s.replace(old,new,1)

old=''' void setIncomingOffset(float y){if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(shade!=null)shade.setTranslationY(y);if(info!=null)info.setTranslationY(y);if(actions!=null)actions.setTranslationY(y);}'''
new=''' void setIncomingOffset(float y){if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(ytTopMask!=null)ytTopMask.setTranslationY(y);if(ytBottomMask!=null)ytBottomMask.setTranslationY(y);if(shade!=null)shade.setTranslationY(y);if(info!=null)info.setTranslationY(y);if(actions!=null)actions.setTranslationY(y);}'''
if old not in s: raise SystemExit("setIncomingOffset anchor missing")
s=s.replace(old,new,1)

old=''' void animateIncomingViews(float y,long ms,Runnable end){if(shade!=null)shade.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)actions.animate().translationY(y).setDuration(ms).withEndAction(end).start();else if(end!=null)end.run();}'''
new=''' void animateIncomingViews(float y,long ms,Runnable end){if(ytTopMask!=null)ytTopMask.animate().translationY(y).setDuration(ms).start();if(ytBottomMask!=null)ytBottomMask.animate().translationY(y).setDuration(ms).start();if(shade!=null)shade.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)actions.animate().translationY(y).setDuration(ms).withEndAction(end).start();else if(end!=null)end.run();}'''
if old not in s: raise SystemExit("animateIncomingViews anchor missing")
s=s.replace(old,new,1)

old=''' void animateSwipeViews(float y,long ms,Runnable end){if(web!=null)web.animate().translationY(y).setDuration(ms).start();if(shade!=null)shade.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)actions.animate().translationY(y).setDuration(ms).withEndAction(end).start();else if(end!=null)end.run();}'''
new=''' void animateSwipeViews(float y,long ms,Runnable end){if(web!=null)web.animate().translationY(y).setDuration(ms).start();if(ytTopMask!=null)ytTopMask.animate().translationY(y).setDuration(ms).start();if(ytBottomMask!=null)ytBottomMask.animate().translationY(y).setDuration(ms).start();if(shade!=null)shade.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)actions.animate().translationY(y).setDuration(ms).withEndAction(end).start();else if(end!=null)end.run();}'''
if old not in s: raise SystemExit("animateSwipeViews anchor missing")
s=s.replace(old,new,1)

old=''' void revealStory(){if(web!=null){web.animate().cancel();web.setTranslationY(0f);web.postDelayed(()->{if(web!=null&&!dragging&&!swipeAnimating)web.animate().alpha(1f).setDuration(120).start();},650);}if(poster!=null){poster.setAlpha(1f);poster.setTranslationY(0f);}}'''
new=''' void revealStory(){if(web!=null){web.animate().cancel();web.setTranslationY(0f);web.postDelayed(()->{if(web!=null&&!dragging&&!swipeAnimating)web.animate().alpha(1f).setDuration(120).start();},650);}if(ytTopMask!=null){ytTopMask.animate().cancel();ytTopMask.setTranslationY(0f);}if(ytBottomMask!=null){ytBottomMask.animate().cancel();ytBottomMask.setTranslationY(0f);}if(poster!=null){poster.setAlpha(1f);poster.setTranslationY(0f);}}'''
if old not in s: raise SystemExit("revealStory anchor missing")
s=s.replace(old,new,1)

p.write_text(s,encoding="utf-8")

g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10029" not in t or "versionName '1.0.29'" not in t: raise SystemExit("wrong 1.0.29 base")
t=t.replace("versionCode 10029","versionCode 10030",1).replace("versionName '1.0.29'","versionName '1.0.30'",1)
g.write_text(t,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.30
- Stories: ocultação inferior reforçada para cobrir completamente compartilhar, miniatura, texto e marca do player externo.
- A máscara inferior agora acompanha o vídeo durante o swipe para cima/baixo, evitando que a barra apareça quando o story se move.
- Máscaras superior e inferior acompanham a animação e voltam corretamente à posição ao terminar a troca.
- Mantido o restante do visual e das cores sem alteração.
""",encoding="utf-8")
print("YELLY_130_STORIES_HIDE_BOTTOM_CHROME_DURING_SWIPE_OK")
