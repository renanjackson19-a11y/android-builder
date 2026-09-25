from pathlib import Path

root=Path("work")

player=root/"app/src/main/java/fun/greenplay/app/PlayerActivity.java"
p=player.read_text(encoding="utf-8")
old=""" void build(){frame=new FrameLayout(this);frame.setBackgroundColor(Color.BLACK);
  displayMode=(forcePortrait&&!tvMode)?3:getSharedPreferences("gp",0).getInt("player_display_mode",0);if(displayMode<0||displayMode>3)displayMode=0;playerView=new PlayerView(this);playerView.setUseController(false);playerView.setShutterBackgroundColor(Color.BLACK);FrameLayout.LayoutParams vp=new FrameLayout.LayoutParams(-1,-1,Gravity.CENTER);frame.addView(playerView,vp);"""
new=""" void build(){frame=new FrameLayout(this);frame.setBackgroundColor(Color.BLACK);
  ImageView movieBackdrop=new ImageView(this);movieBackdrop.setScaleType(ImageView.ScaleType.CENTER_CROP);movieBackdrop.setBackgroundColor(Color.BLACK);String backdropUrl=!movieLandscape.isEmpty()?movieLandscape:moviePoster;if(!backdropUrl.isEmpty())Img.loadVisible(movieBackdrop,backdropUrl);frame.addView(movieBackdrop,new FrameLayout.LayoutParams(-1,-1));View backdropDim=new View(this);backdropDim.setBackgroundColor(0x66000000);frame.addView(backdropDim,new FrameLayout.LayoutParams(-1,-1));
  displayMode=(forcePortrait&&!tvMode)?3:getSharedPreferences("gp",0).getInt("player_display_mode",0);if(displayMode<0||displayMode>3)displayMode=0;playerView=new PlayerView(this);playerView.setUseController(false);playerView.setShutterBackgroundColor(Color.TRANSPARENT);FrameLayout.LayoutParams vp=new FrameLayout.LayoutParams(-1,-1,Gravity.CENTER);frame.addView(playerView,vp);"""
if old not in p:
    raise SystemExit("PlayerActivity build anchor not found")
p=p.replace(old,new,1)
player.write_text(p,encoding="utf-8")

grad=root/"app/build.gradle"
g=grad.read_text(encoding="utf-8")
if "versionCode 10014" not in g or "versionName '1.0.14'" not in g:
    raise SystemExit("wrong base version")
g=g.replace("versionCode 10014","versionCode 10015",1)
g=g.replace("versionName '1.0.14'","versionName '1.0.15'",1)
grad.write_text(g,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.15
Stories sem YouTube: removido WebView, iframe, Shorts, logo, canal e compartilhar do YouTube.
Stories agora usam diretamente os videos do catalogo Yelly com Media3/ExoPlayer.
Cada Story e um preview de ate 2 minutos e o botao Assistir agora abre o filme completo.
Banner fixo Yelly no fundo, logo Yelly no topo direito, Favoritar e Comentarios mantidos.
Player completo usa a capa/backdrop do proprio filme como fundo atras do video.
""",encoding="utf-8")
print("YELLY_115_NATIVE_STORIES_OK")
