from pathlib import Path

p=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
s=p.read_text()
assert 'catalog52848_' in s
s=s.replace('catalog52848_','catalog52849_',1)
p.write_text(s)

player=Path('work/app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java')
player.write_text(r'''package fun.greenplay.app;

import android.app.*;
import android.os.*;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.view.*;
import android.webkit.*;
import android.widget.*;
import android.content.res.ColorStateList;
import java.util.Locale;

public class YouTubePlayerActivity extends Activity {
    FrameLayout root;
    WebView web;
    View touchShield;
    LinearLayout controls;
    TextView back,back10,play,fwd10,time;
    SeekBar seek;
    Handler h=new Handler(Looper.getMainLooper());
    Runnable hideTask;
    boolean seeking=false,tvMode=false,ready=false;
    int green=Color.rgb(32,224,112);
    String videoId="";

    int dp(int n){return(int)(n*getResources().getDisplayMetrics().density+.5f);}
    GradientDrawable bg(int c,int r){GradientDrawable g=new GradientDrawable();g.setColor(c);g.setCornerRadius(dp(r));return g;}
    TextView tx(String s,int size){TextView t=new TextView(this);t.setText(s);t.setTextColor(Color.WHITE);t.setTextSize(size);t.setGravity(Gravity.CENTER);return t;}
    GradientDrawable focusBg(){GradientDrawable g=bg(0xee102019,14);g.setStroke(dp(3),green);return g;}
    void tvControl(View v){
        if(!tvMode||v==null)return;
        v.setFocusable(true);v.setFocusableInTouchMode(false);
        final android.graphics.drawable.Drawable normal=v.getBackground();
        v.setOnFocusChangeListener((x,has)->{
            x.animate().scaleX(has?1.06f:1f).scaleY(has?1.06f:1f).setDuration(90).start();
            if(android.os.Build.VERSION.SDK_INT>=21)x.setTranslationZ(has?dp(14):0);
            if(has){showControls();x.setBackground(focusBg());if(x instanceof TextView)((TextView)x).setTextColor(green);}
            else{x.setBackground(normal);if(x instanceof TextView)((TextView)x).setTextColor(Color.WHITE);}
        });
    }

    @Override public void onCreate(Bundle b){
        super.onCreate(b);
        tvMode=DeviceCompat.isTelevisionDevice(this);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        applyImmersive();

        if(getIntent()!=null)videoId=getIntent().getStringExtra("youtube_id");
        if(videoId==null)videoId="";
        videoId=videoId.replaceAll("[^A-Za-z0-9_-]","");
        if(videoId.isEmpty()){finish();return;}

        build();
        loadPlayer();
        h.post(poll);
        showControls();
    }

    void applyImmersive(){
        try{getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY|View.SYSTEM_UI_FLAG_FULLSCREEN|
            View.SYSTEM_UI_FLAG_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN|
            View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_LAYOUT_STABLE
        );}catch(Exception ignored){}
    }

    void build(){
        root=new FrameLayout(this);root.setBackgroundColor(Color.BLACK);

        web=new WebView(this);web.setBackgroundColor(Color.BLACK);
        WebSettings ws=web.getSettings();
        ws.setJavaScriptEnabled(true);ws.setDomStorageEnabled(true);ws.setMediaPlaybackRequiresUserGesture(false);
        ws.setLoadsImagesAutomatically(true);ws.setUseWideViewPort(true);ws.setLoadWithOverviewMode(true);
        web.setWebChromeClient(new WebChromeClient());
        web.setWebViewClient(new WebViewClient());
        web.setLongClickable(false);web.setHapticFeedbackEnabled(false);
        web.setOnLongClickListener(v->true);
        web.setOnTouchListener((v,e)->true);
        root.addView(web,new FrameLayout.LayoutParams(-1,-1));

        touchShield=new View(this);touchShield.setBackgroundColor(Color.TRANSPARENT);touchShield.setClickable(true);
        touchShield.setOnClickListener(v->{if(controls.getVisibility()==View.VISIBLE)hideControls();else showControls();});
        root.addView(touchShield,new FrameLayout.LayoutParams(-1,-1));

        back=tx("‹",34);back.setBackground(bg(0x77000000,24));back.setOnClickListener(v->finish());
        FrameLayout.LayoutParams bp=new FrameLayout.LayoutParams(dp(48),dp(48),Gravity.TOP|Gravity.LEFT);
        bp.setMargins(dp(14),dp(14),0,0);root.addView(back,bp);

        controls=new LinearLayout(this);controls.setOrientation(LinearLayout.VERTICAL);
        controls.setPadding(dp(12),dp(8),dp(12),dp(7));
        GradientDrawable controlsBg=bg(0xe30a0f0c,20);controlsBg.setStroke(dp(1),0x66415b4e);
        controls.setBackground(controlsBg);controls.setElevation(dp(12));

        LinearLayout buttons=new LinearLayout(this);buttons.setGravity(Gravity.CENTER);
        back10=tx("↶ 10s",15);play=tx("Ⅱ",26);fwd10=tx("10s ↷",15);
        back10.setBackground(bg(0x55131c17,14));play.setBackground(bg(0x77131c17,18));fwd10.setBackground(bg(0x55131c17,14));
        LinearLayout.LayoutParams b1=new LinearLayout.LayoutParams(0,dp(46),1f);b1.setMargins(dp(3),0,dp(3),0);
        LinearLayout.LayoutParams b2=new LinearLayout.LayoutParams(0,dp(46),1f);b2.setMargins(dp(3),0,dp(3),0);
        LinearLayout.LayoutParams b3=new LinearLayout.LayoutParams(0,dp(46),1f);b3.setMargins(dp(3),0,dp(3),0);
        buttons.addView(back10,b1);buttons.addView(play,b2);buttons.addView(fwd10,b3);
        controls.addView(buttons,new LinearLayout.LayoutParams(-1,dp(48)));

        LinearLayout progress=new LinearLayout(this);progress.setGravity(Gravity.CENTER_VERTICAL);
        time=tx("00:00 / 00:00",12);time.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);
        progress.addView(time,new LinearLayout.LayoutParams(dp(112),dp(34)));
        seek=new SeekBar(this);seek.setMax(1000);
        seek.setProgressTintList(ColorStateList.valueOf(green));
        seek.setProgressBackgroundTintList(ColorStateList.valueOf(0xff38443e));
        seek.setThumbTintList(ColorStateList.valueOf(green));
        progress.addView(seek,new LinearLayout.LayoutParams(0,dp(34),1));
        controls.addView(progress,new LinearLayout.LayoutParams(-1,dp(34)));

        FrameLayout.LayoutParams cp=new FrameLayout.LayoutParams(-1,dp(94),Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);
        cp.setMargins(dp(14),0,dp(14),dp(16));root.addView(controls,cp);

        back10.setOnClickListener(v->{eval("gpSeekBy(-10)");showControls();});
        play.setOnClickListener(v->{eval("gpToggle()");showControls();});
        fwd10.setOnClickListener(v->{eval("gpSeekBy(10)");showControls();});

        seek.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){
            public void onProgressChanged(SeekBar s,int p,boolean fromUser){}
            public void onStartTrackingTouch(SeekBar s){seeking=true;showControls();}
            public void onStopTrackingTouch(SeekBar s){seeking=false;eval("gpSeek("+(s.getProgress()/1000.0)+")");showControls();}
        });

        if(tvMode){tvControl(back);tvControl(back10);tvControl(play);tvControl(fwd10);tvControl(seek);play.postDelayed(()->play.requestFocus(),180);}
        setContentView(root);
    }

    void loadPlayer(){
        String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'>"+
            "<style>html,body,#p{margin:0;padding:0;width:100%;height:100%;background:#000;overflow:hidden}iframe{width:100%!important;height:100%!important;border:0}</style>"+
            "<script src='https://www.youtube.com/iframe_api'></script></head><body><div id='p'></div><script>"+
            "var player,ready=false;function onYouTubeIframeAPIReady(){player=new YT.Player('p',{videoId:'"+videoId+"',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,iv_load_policy:3,cc_load_policy:0,playsinline:1,rel:0,modestbranding:1,origin:'https://greenplay.fun'},events:{onReady:function(e){ready=true;e.target.playVideo();}}});}"+
            "function gpToggle(){if(!ready)return;var s=player.getPlayerState();if(s==1)player.pauseVideo();else player.playVideo();}"+
            "function gpSeek(r){if(!ready)return;var d=player.getDuration()||0;player.seekTo(Math.max(0,Math.min(d,d*r)),true);}"+
            "function gpSeekBy(s){if(!ready)return;var d=player.getDuration()||0;player.seekTo(Math.max(0,Math.min(d,(player.getCurrentTime()||0)+s)),true);}"+
            "function gpTime(){if(!ready)return '0|0|0';return (player.getCurrentTime()||0)+'|'+(player.getDuration()||0)+'|'+player.getPlayerState();}"+
            "</script></body></html>";
        web.loadDataWithBaseURL("https://greenplay.fun/",html,"text/html","UTF-8",null);
    }

    void eval(String js){if(web!=null)web.evaluateJavascript("javascript:"+js,null);}
    String fmt(double sec){int s=Math.max(0,(int)sec),hh=s/3600,mm=(s%3600)/60,ss=s%60;return hh>0?String.format(Locale.US,"%d:%02d:%02d",hh,mm,ss):String.format(Locale.US,"%02d:%02d",mm,ss);}

    final Runnable poll=new Runnable(){public void run(){
        if(web!=null)web.evaluateJavascript("javascript:gpTime()",v->{
            try{
                if(v==null)return;String z=v;
                if(z.length()>=2&&z.charAt(0)==34&&z.charAt(z.length()-1)==34)z=z.substring(1,z.length()-1);
                String[] a=z.split("\\|");if(a.length<3)return;
                double cur=Double.parseDouble(a[0]),dur=Double.parseDouble(a[1]);int st=(int)Double.parseDouble(a[2]);
                ready=dur>0||st!=0;time.setText(fmt(cur)+" / "+fmt(dur));play.setText(st==1?"Ⅱ":"▶");
                if(!seeking&&dur>0)seek.setProgress((int)Math.max(0,Math.min(1000,(cur/dur)*1000)));
            }catch(Exception ignored){}
        });
        h.postDelayed(this,750);
    }};

    void showControls(){
        controls.setVisibility(View.VISIBLE);back.setVisibility(View.VISIBLE);
        controls.bringToFront();back.bringToFront();
        if(hideTask!=null)h.removeCallbacks(hideTask);
        hideTask=()->{if(!seeking&&!tvMode)hideControls();};
        h.postDelayed(hideTask,tvMode?6500:5000);
    }
    void hideControls(){if(controls!=null)controls.setVisibility(View.GONE);if(back!=null)back.setVisibility(View.GONE);}

    @Override public boolean dispatchKeyEvent(KeyEvent e){
        if(e!=null&&e.getAction()==KeyEvent.ACTION_DOWN){
            int k=e.getKeyCode();
            if(k==KeyEvent.KEYCODE_BACK){finish();return true;}
            if(k==KeyEvent.KEYCODE_MEDIA_PLAY_PAUSE||k==KeyEvent.KEYCODE_MEDIA_PLAY||k==KeyEvent.KEYCODE_MEDIA_PAUSE||k==KeyEvent.KEYCODE_DPAD_CENTER||k==KeyEvent.KEYCODE_ENTER||k==KeyEvent.KEYCODE_NUMPAD_ENTER){eval("gpToggle()");showControls();return true;}
            if(k==KeyEvent.KEYCODE_MEDIA_REWIND||k==KeyEvent.KEYCODE_DPAD_LEFT){eval("gpSeekBy(-10)");showControls();return true;}
            if(k==KeyEvent.KEYCODE_MEDIA_FAST_FORWARD||k==KeyEvent.KEYCODE_DPAD_RIGHT){eval("gpSeekBy(10)");showControls();return true;}
            if(k==KeyEvent.KEYCODE_DPAD_UP||k==KeyEvent.KEYCODE_DPAD_DOWN){showControls();return true;}
        }
        return super.dispatchKeyEvent(e);
    }

    @Override public void onWindowFocusChanged(boolean hasFocus){super.onWindowFocusChanged(hasFocus);if(hasFocus)applyImmersive();}
    @Override protected void onPause(){eval("if(ready)player.pauseVideo()");super.onPause();}
    @Override protected void onResume(){super.onResume();applyImmersive();}
    @Override protected void onDestroy(){
        h.removeCallbacksAndMessages(null);
        if(web!=null){try{web.stopLoading();web.loadUrl("about:blank");web.removeAllViews();web.destroy();}catch(Exception ignored){}web=null;}
        super.onDestroy();
    }
}
''')

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52848' in t and "versionName '5.28.48'" in t
t=t.replace('versionCode 52848','versionCode 52849',1).replace("versionName '5.28.48'","versionName '5.28.49'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52849.txt').write_text("""GreenPlay 5.28.49

- GreenShorts usa controles visuais do player normal GreenPlay.
- Toque não é repassado ao player incorporado: evita abrir compartilhamento/controles externos.
- Remove título duplicado/cabeçalho externo do topo durante a interação.
- Controles GreenPlay: voltar, -10s, play/pause, +10s e barra de progresso.
- Controle remoto: OK play/pause, esquerda/direita -10/+10s.
- Títulos do catálogo são entregues pelo painel já traduzidos para português quando possível.
""")

assert 'catalog52849_' in p.read_text()
assert 'web.setOnTouchListener((v,e)->true);' in player.read_text()
assert 'versionCode 52849' in b.read_text()
print('OK 5.28.49')
