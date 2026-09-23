from pathlib import Path
g=Path("work/app/build.gradle")
s=g.read_text()
assert "versionCode 52861" in s
assert "versionName '5.28.61'" in s
s=s.replace("versionCode 52861","versionCode 52862",1).replace("versionName '5.28.61'","versionName '5.28.62'",1)
g.write_text(s)

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()
old=''' View headerCastButton(){
  androidx.mediarouter.app.MediaRouteButton b=new androidx.mediarouter.app.MediaRouteButton(this);
  b.setTag("gp_cast_header");b.setContentDescription("Transmitir para Chromecast");b.setClickable(true);b.setFocusable(true);
  b.setPadding(dp(5),dp(4),dp(5),dp(4));GradientDrawable cb=round(0x44111815,19);cb.setStroke(dp(1),0xff3b4641);b.setBackground(cb);
  try{com.google.android.gms.cast.framework.CastButtonFactory.setUpMediaRouteButton(getApplicationContext(),b);}catch(Exception e){android.util.Log.w("GreenPlayCast","Falha ao configurar botao oficial do Google Cast",e);}
  b.setOnLongClickListener(v->{CastHelper.openSystemMirror(MainActivity.this);return true;});
  return b;
 }'''
new=''' ImageView headerCastButton(){
  ImageView b=new ImageView(this);b.setTag("gp_cast_header");b.setImageResource(R.drawable.ic_cast);b.setScaleType(ImageView.ScaleType.CENTER_INSIDE);
  b.setPadding(dp(8),dp(7),dp(8),dp(7));GradientDrawable cb=round(0x44111815,19);cb.setStroke(dp(1),0xff3b4641);b.setBackground(cb);
  b.setContentDescription("Transmitir para Chromecast");b.setClickable(true);b.setFocusable(true);
  b.setOnClickListener(v->CastHelper.openChooser(MainActivity.this));
  b.setOnLongClickListener(v->{CastHelper.openSystemMirror(MainActivity.this);return true;});
  b.setColorFilter(CastHelper.isConnected(this)?GREEN:0xffe6ebe8);
  return b;
 }'''
assert old in s, "official cast button block not found"
s=s.replace(old,new,1)
p.write_text(s)
