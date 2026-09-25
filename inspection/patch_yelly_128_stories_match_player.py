from pathlib import Path

root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")

old='''  ytTopMask=new View(this);ytTopMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ytp=new FrameLayout.LayoutParams(-1,storyTopMaskH,Gravity.TOP);ytp.setMargins(0,dp(64),0,0);root.addView(ytTopMask,ytp);
  ytBottomMask=new View(this);ytBottomMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ybp=new FrameLayout.LayoutParams(-1,storyBottomMaskH,Gravity.BOTTOM);ybp.setMargins(0,0,0,dp(112));root.addView(ytBottomMask,ybp);'''
new='''  ytTopMask=new View(this);ytTopMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ytp=new FrameLayout.LayoutParams(-1,storyTopMaskH,Gravity.TOP);root.addView(ytTopMask,ytp);
  ytBottomMask=new View(this);ytBottomMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ybp=new FrameLayout.LayoutParams(-1,storyBottomMaskH,Gravity.BOTTOM);root.addView(ytBottomMask,ybp);'''
if old not in s: raise SystemExit("stories mask margins anchor missing")
s=s.replace(old,new,1)

# Keep the full-screen video untouched; UI floats over it instead of squeezing the visible center.
old='''  shade=new View(this);GradientDrawable shadeBg=new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM,new int[]{0x66000000,0x00000000,0x00000000,0xbb060306});shade.setBackground(shadeBg);root.addView(shade,new FrameLayout.LayoutParams(-1,-1));'''
new='''  shade=new View(this);GradientDrawable shadeBg=new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM,new int[]{0x33000000,0x00000000,0x00000000,0x66060306});shade.setBackground(shadeBg);root.addView(shade,new FrameLayout.LayoutParams(-1,-1));'''
if old not in s: raise SystemExit("stories shade anchor missing")
s=s.replace(old,new,1)

p.write_text(s,encoding="utf-8")

g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10027" not in t or "versionName '1.0.27'" not in t: raise SystemExit("wrong base")
t=t.replace("versionCode 10027","versionCode 10028",1).replace("versionName '1.0.27'","versionName '1.0.28'",1)
g.write_text(t,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.28
- Stories agora seguem o mesmo enquadramento real do player principal.
- Removidas as margens de 64dp em cima e 112dp embaixo que ainda deslocavam as faixas pretas para dentro da imagem.
- As faixas ficam nas bordas da tela, sem diminuir a área central do vídeo.
- Sombra do Stories foi suavizada para não deixar os atores visualmente menores/escuros.
- Vídeo continua ocupando 100% da tela, mantendo swipe, Favoritar, Comentários e Assistir agora.
- GreenPlay não foi alterado.
""",encoding="utf-8")
print("YELLY_128_STORIES_MATCH_MAIN_PLAYER_OK")
