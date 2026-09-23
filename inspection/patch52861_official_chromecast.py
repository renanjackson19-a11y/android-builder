from pathlib import Path

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

old=''' void updateCastButtonsIn(View v){if(v==null)return;if(v instanceof ImageView&&"gp_cast_header".equals(v.getTag())){try{((ImageView)v).setColorFilter(CastHelper.isConnected(this)?GREEN:0xffe6ebe8);}catch(Exception ignored){}}if(v instanceof ViewGroup){ViewGroup g=(ViewGroup)v;for(int i=0;i<g.getChildCount();i++)updateCastButtonsIn(g.getChildAt(i));}}
 void ensureGlobalCastButton(){if(globalCastButton!=null&&globalCastButton.getParent()==contentFrame){try{contentFrame.removeView(globalCastButton);}catch(Exception ignored){}}globalCastButton=null;updateGlobalCastButtonState();}
 ImageView headerCastButton(){ImageView b=new ImageView(this);b.setTag("gp_cast_header");b.setImageResource(R.drawable.ic_cast);b.setScaleType(ImageView.ScaleType.CENTER_INSIDE);b.setPadding(dp(8),dp(7),dp(8),dp(7));GradientDrawable cb=round(0x44111815,19);cb.setStroke(dp(1),0xff3b4641);b.setBackground(cb);b.setContentDescription("Transmitir para TV");b.setClickable(true);b.setFocusable(true);b.setOnClickListener(v->CastHelper.openChooser(MainActivity.this));b.setOnLongClickListener(v->{CastHelper.openSystemMirror(MainActivity.this);return true;});b.setColorFilter(CastHelper.isConnected(this)?GREEN:0xffe6ebe8);return b;}'''
new=''' void updateCastButtonsIn(View v){if(v==null)return;if(v instanceof ImageView&&"gp_cast_header".equals(v.getTag())){try{((ImageView)v).setColorFilter(CastHelper.isConnected(this)?GREEN:0xffe6ebe8);}catch(Exception ignored){}}if(v instanceof ViewGroup){ViewGroup g=(ViewGroup)v;for(int i=0;i<g.getChildCount();i++)updateCastButtonsIn(g.getChildAt(i));}}
 void ensureGlobalCastButton(){if(globalCastButton!=null&&globalCastButton.getParent()==contentFrame){try{contentFrame.removeView(globalCastButton);}catch(Exception ignored){}}globalCastButton=null;updateGlobalCastButtonState();}
 View headerCastButton(){
  androidx.mediarouter.app.MediaRouteButton b=new androidx.mediarouter.app.MediaRouteButton(this);
  b.setTag("gp_cast_header");b.setContentDescription("Transmitir para Chromecast");b.setClickable(true);b.setFocusable(true);
  b.setPadding(dp(5),dp(4),dp(5),dp(4));GradientDrawable cb=round(0x44111815,19);cb.setStroke(dp(1),0xff3b4641);b.setBackground(cb);
  try{com.google.android.gms.cast.framework.CastButtonFactory.setUpMediaRouteButton(getApplicationContext(),b);}catch(Exception e){android.util.Log.w("GreenPlayCast","Falha ao configurar botao oficial do Google Cast",e);}
  b.setOnLongClickListener(v->{CastHelper.openSystemMirror(MainActivity.this);return true;});
  return b;
 }'''
assert old in s, "header cast block not found"
s=s.replace(old,new,1)

old='''if(!tvMode){ImageView cast=headerCastButton();LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(dp(40),dp(38));clp.setMargins(dp(8),0,0,0);top.addView(cast,clp);}'''
new='''if(!tvMode){View cast=headerCastButton();LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(dp(44),dp(40));clp.setMargins(dp(8),0,0,0);top.addView(cast,clp);}'''
assert s.count(old)>=1, "first cast view usage not found"
s=s.replace(old,new)

p.write_text(s)

p=Path("work/app/src/main/java/fun/greenplay/app/CastHelper.java")
s=p.read_text()

old=''' public static void openChooser(Activity a){if(a==null)return;if(DeviceCompat.isTelevisionDevice(a))return;try{CastContext ctx=CastContext.getSharedInstance(a);CastSession current=ctx.getSessionManager().getCurrentCastSession();if(current!=null&&current.isConnected()){Toast.makeText(a,"TV já conectada. Escolha um conteúdo para transmitir.",Toast.LENGTH_SHORT).show();return;}MediaRouteChooserDialog chooser=new MediaRouteChooserDialog(a,R.style.GreenPlayCastDialogTheme);MediaRouteSelector selector=selector();MediaRouter router=MediaRouter.getInstance(a);MediaRouter.Callback scan=new MediaRouter.Callback(){};router.addCallback(selector,scan,MediaRouter.CALLBACK_FLAG_PERFORM_ACTIVE_SCAN);chooser.setRouteSelector(selector);chooser.setTitle("Conectar à TV");chooser.setOnDismissListener(d->{try{router.removeCallback(scan);}catch(Exception ignored){}if(!isConnected(a))Toast.makeText(a,"Se a TV/Box não tiver Google Cast, segure o botão Transmitir para abrir o espelhamento do Android.",Toast.LENGTH_LONG).show();});chooser.show();}catch(Exception e){openSystemMirror(a);}}'''
new=''' public static void openChooser(Activity a){
  if(a==null||DeviceCompat.isTelevisionDevice(a))return;
  try{
   CastContext ctx=CastContext.getSharedInstance(a);CastSession current=ctx.getSessionManager().getCurrentCastSession();
   if(current!=null&&current.isConnected()){Toast.makeText(a,"Chromecast conectado. Escolha o conteúdo para transmitir.",Toast.LENGTH_SHORT).show();return;}
   MediaRouteChooserDialog chooser=new MediaRouteChooserDialog(a,R.style.GreenPlayCastDialogTheme);
   chooser.setRouteSelector(ctx.getMergedSelector());chooser.setTitle("Transmitir para Chromecast");chooser.show();
  }catch(Exception e){
   android.util.Log.e("GreenPlayCast","Falha ao abrir Google Cast",e);
   Toast.makeText(a,"Não foi possível iniciar o Google Cast. Verifique o Google Play Services e se celular e TV estão no mesmo Wi-Fi.",Toast.LENGTH_LONG).show();
  }
 }'''
assert old in s, "openChooser block not found"
s=s.replace(old,new,1)

old='''   final MediaRouteChooserDialog chooser=new MediaRouteChooserDialog(a, R.style.GreenPlayCastDialogTheme);
   MediaRouteSelector selector=selector();MediaRouter router=MediaRouter.getInstance(a);MediaRouter.Callback scan=new MediaRouter.Callback(){};router.addCallback(selector,scan,MediaRouter.CALLBACK_FLAG_PERFORM_ACTIVE_SCAN);
   chooser.setRouteSelector(selector);chooser.setTitle("Transmitir para");chooser.setOnDismissListener(d->{try{router.removeCallback(scan);}catch(Exception ignored){}});chooser.show();'''
new='''   final MediaRouteChooserDialog chooser=new MediaRouteChooserDialog(a, R.style.GreenPlayCastDialogTheme);
   chooser.setRouteSelector(ctx.getMergedSelector());chooser.setTitle("Transmitir para Chromecast");chooser.show();'''
assert old in s, "cast chooser block not found"
s=s.replace(old,new,1)

old='''  }catch(Exception e){
   android.util.Log.w("GreenPlayCast","Google Cast indisponivel; usando espelhamento do sistema",e);
   openSystemMirror(a);
  }'''
new='''  }catch(Exception e){
   android.util.Log.e("GreenPlayCast","Google Cast indisponivel",e);
   Toast.makeText(a,"Google Cast indisponível. Use o botão Transmitir e escolha um Chromecast/Google TV na mesma rede Wi-Fi.",Toast.LENGTH_LONG).show();
  }'''
assert old in s, "cast fallback block not found"
s=s.replace(old,new,1)

p.write_text(s)
