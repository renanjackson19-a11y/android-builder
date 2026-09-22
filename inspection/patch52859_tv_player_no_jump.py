from pathlib import Path

gradle=Path("work/app/build.gradle")
g=gradle.read_text()
assert "versionCode 52858" in g
assert "versionName '5.28.58'" in g
g=g.replace("versionCode 52858","versionCode 52859",1)
g=g.replace("versionName '5.28.58'","versionName '5.28.59'",1)
gradle.write_text(g)

p=Path("work/app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java")
s=p.read_text()

old='''    @Override public void onCreate(Bundle b){
        super.onCreate(b);
        tvMode=(getIntent()!=null&&getIntent().getBooleanExtra("tv_mode",false))||DeviceCompat.isTelevisionDevice(this);
        try{setRequestedOrientation(tvMode?ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE:ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);}catch(Exception ignored){}
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,WindowManager.LayoutParams.FLAG_FULLSCREEN);'''
new='''    @Override public void onCreate(Bundle b){
        tvMode=(getIntent()!=null&&getIntent().getBooleanExtra("tv_mode",false))||DeviceCompat.isTelevisionDevice(this);
        try{setRequestedOrientation(tvMode?ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE:ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);}catch(Exception ignored){}
        super.onCreate(b);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,WindowManager.LayoutParams.FLAG_FULLSCREEN);'''
assert old in s
s=s.replace(old,new,1)

old='''        build();
        loadPlayer();
        h.post(poll);
        showControls();'''
new='''        build();
        if(tvMode)root.postDelayed(()->{if(!isFinishing())loadPlayer();},140);else loadPlayer();
        h.post(poll);
        showControls();'''
assert old in s
s=s.replace(old,new,1)

old='''        web=new WebView(this);web.setBackgroundColor(Color.BLACK);'''
new='''        web=new WebView(this);web.setBackgroundColor(Color.BLACK);web.setAlpha(tvMode?0f:1f);'''
assert old in s
s=s.replace(old,new,1)

old='''events:{onReady:function(e){ready=true;if("+resumeMs+">0)e.target.seekTo("+(resumeMs/1000.0)+",true);e.target.playVideo();},onStateChange:function(e){if(e.data==0)AndroidBridge.completed();}}});}"+'''
new='''events:{onReady:function(e){ready=true;if("+resumeMs+">0)e.target.seekTo("+(resumeMs/1000.0)+",true);e.target.playVideo();AndroidBridge.playerReady();},onStateChange:function(e){if(e.data==0)AndroidBridge.completed();}}});}"+'''
assert old in s
s=s.replace(old,new,1)

old='''        web.addJavascriptInterface(new Object(){@android.webkit.JavascriptInterface public void completed(){runOnUiThread(()->clearProgress());}},"AndroidBridge");'''
new='''        web.addJavascriptInterface(new Object(){
            @android.webkit.JavascriptInterface public void completed(){runOnUiThread(()->clearProgress());}
            @android.webkit.JavascriptInterface public void playerReady(){runOnUiThread(()->{if(web!=null){web.setTranslationX(0f);web.setTranslationY(0f);web.animate().alpha(1f).setDuration(120).start();}});}
        },"AndroidBridge");'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)
