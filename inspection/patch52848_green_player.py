from pathlib import Path

p=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
s=p.read_text()
assert 'Assistir no YouTube' in s
s=s.replace('Assistir no YouTube','Assistir')
s=s.replace('Vídeo do YouTube indisponível.','Vídeo indisponível.')
s=s.replace('catalog52847_','catalog52848_')
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
import android.content.*;
import java.util.Locale;

public class YouTubePlayerActivity extends Activity {
    FrameLayout root;
    WebView web;
    LinearLayout topBar,bottomBar;
    TextView titleView,timeView,durationView;
    Button backBtn,playBtn;
    SeekBar seek;
    Handler handler=new Handler(Looper.getMainLooper());
    boolean controlsVisible=true, userSeeking=false;
    String videoId="", videoTitle="GreenShorts";

    int dp(int v){return (int)(v*getResources().getDisplayMetrics().density+0.5f);}
    GradientDrawable bg(int color,int radius){
        GradientDrawable g=new GradientDrawable();g.setColor(color);g.setCornerRadius(dp(radius));return g;
    }
    TextView txt(String s,float sp,int color){
        TextView t=new TextView(this);t.setText(s);t.setTextSize(sp);t.setTextColor(color);t.setGravity(Gravity.CENTER_VERTICAL);return t;
    }
    Button btn(String s){
        Button b=new Button(this);b.setText(s);b.setTextColor(Color.WHITE);b.setTextSize(20);b.setAllCaps(false);
        b.setBackground(bg(0x9908120d,26));b.setPadding(0,0,0,0);return b;
    }

    @Override public void onCreate(Bundle b){
        super.onCreate(b);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        getWindow().setStatusBarColor(Color.BLACK);getWindow().setNavigationBarColor(Color.BLACK);
        getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_FULLSCREEN|View.SYSTEM_UI_FLAG_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
        );

        if(getIntent()!=null){
            videoId=getIntent().getStringExtra("youtube_id");
            String t=getIntent().getStringExtra("title");if(t!=null&&!t.trim().isEmpty())videoTitle=t.trim();
        }
        if(videoId==null)videoId="";
        videoId=videoId.replaceAll("[^A-Za-z0-9_-]","");
        if(videoId.isEmpty()){finish();return;}

        root=new FrameLayout(this);root.setBackgroundColor(Color.BLACK);
        web=new WebView(this);web.setBackgroundColor(Color.BLACK);
        WebSettings ws=web.getSettings();
        ws.setJavaScriptEnabled(true);ws.setDomStorageEnabled(true);ws.setMediaPlaybackRequiresUserGesture(false);
        ws.setLoadsImagesAutomatically(true);ws.setUseWideViewPort(true);ws.setLoadWithOverviewMode(true);
        web.setWebChromeClient(new WebChromeClient());
        web.setWebViewClient(new WebViewClient());
        web.setOnTouchListener((v,e)->{if(e.getAction()==MotionEvent.ACTION_DOWN)showControls();return false;});
        root.addView(web,new FrameLayout.LayoutParams(-1,-1));

        topBar=new LinearLayout(this);topBar.setOrientation(LinearLayout.HORIZONTAL);topBar.setGravity(Gravity.CENTER_VERTICAL);
        topBar.setPadding(dp(14),dp(10),dp(14),dp(10));topBar.setBackgroundColor(0xaa000000);
        backBtn=btn("‹");LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(dp(50),dp(50));topBar.addView(backBtn,bp);
        titleView=txt(videoTitle,17,Color.WHITE);titleView.setSingleLine(true);titleView.setEllipsize(android.text.TextUtils.TruncateAt.END);
        LinearLayout.LayoutParams tp=new LinearLayout.LayoutParams(0,dp(50),1f);tp.setMargins(dp(12),0,dp(8),0);topBar.addView(titleView,tp);
        FrameLayout.LayoutParams topLp=new FrameLayout.LayoutParams(-1,dp(70),Gravity.TOP);root.addView(topBar,topLp);

        playBtn=btn("❚❚");FrameLayout.LayoutParams pp=new FrameLayout.LayoutParams(dp(70),dp(70),Gravity.CENTER);root.addView(playBtn,pp);

        bottomBar=new LinearLayout(this);bottomBar.setOrientation(LinearLayout.HORIZONTAL);bottomBar.setGravity(Gravity.CENTER_VERTICAL);
        bottomBar.setPadding(dp(16),dp(8),dp(16),dp(10));bottomBar.setBackgroundColor(0xaa000000);
        timeView=txt("0:00",13,Color.WHITE);durationView=txt("0:00",13,0xffb7c0bb);
        bottomBar.addView(timeView,new LinearLayout.LayoutParams(dp(58),dp(42)));
        seek=new SeekBar(this);seek.setMax(1000);
        LinearLayout.LayoutParams sp=new LinearLayout.LayoutParams(0,dp(42),1f);bottomBar.addView(seek,sp);
        bottomBar.addView(durationView,new LinearLayout.LayoutParams(dp(62),dp(42)));
        FrameLayout.LayoutParams blp=new FrameLayout.LayoutParams(-1,dp(66),Gravity.BOTTOM);root.addView(bottomBar,blp);

        backBtn.setOnClickListener(v->finish());
        playBtn.setOnClickListener(v->{eval("gpToggle()");showControls();});
        seek.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){
            public void onProgressChanged(SeekBar b,int p,boolean fromUser){}
            public void onStartTrackingTouch(SeekBar b){userSeeking=true;showControls();}
            public void onStopTrackingTouch(SeekBar b){userSeeking=false;eval("gpSeek("+(b.getProgress()/1000.0)+")");showControls();}
        });

        setContentView(root);
        loadPlayer();
        handler.post(poll);
        showControls();
    }

    void loadPlayer(){
        String safeTitle=videoTitle.replace("\\","\\\\").replace("'","\\'");
        String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'>"+
            "<style>html,body,#p{margin:0;padding:0;width:100%;height:100%;background:#000;overflow:hidden}iframe{width:100%!important;height:100%!important}</style>"+
            "<script src='https://www.youtube.com/iframe_api'></script></head><body><div id='p'></div><script>"+
            "var player,ready=false;function onYouTubeIframeAPIReady(){player=new YT.Player('p',{videoId:'"+videoId+"',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,iv_load_policy:3,playsinline:1,rel:0,modestbranding:1,origin:'https://greenplay.fun'},events:{onReady:function(e){ready=true;e.target.playVideo();}}});}"+
            "function gpToggle(){if(!ready)return;var s=player.getPlayerState();if(s==1)player.pauseVideo();else player.playVideo();}"+
            "function gpSeek(r){if(!ready)return;var d=player.getDuration()||0;player.seekTo(Math.max(0,Math.min(d,d*r)),true);}"+
            "function gpTime(){if(!ready)return '0|0|0';return (player.getCurrentTime()||0)+'|'+(player.getDuration()||0)+'|'+player.getPlayerState();}"+
            "</script></body></html>";
        web.loadDataWithBaseURL("https://greenplay.fun/",html,"text/html","UTF-8",null);
    }

    void eval(String js){if(web!=null)web.evaluateJavascript("javascript:"+js,null);}
    String fmt(double sec){int s=Math.max(0,(int)sec),h=s/3600,m=(s%3600)/60,x=s%60;return h>0?String.format(Locale.US,"%d:%02d:%02d",h,m,x):String.format(Locale.US,"%d:%02d",m,x);}
    final Runnable poll=new Runnable(){public void run(){
        if(web!=null)web.evaluateJavascript("javascript:gpTime()",v->{
            try{
                if(v==null)return;String z=v;if(z.length()>=2&&z.charAt(0)==34&&z.charAt(z.length()-1)==34)z=z.substring(1,z.length()-1);String[] a=z.split("\\|");
                if(a.length<3)return;double cur=Double.parseDouble(a[0]),dur=Double.parseDouble(a[1]);int st=(int)Double.parseDouble(a[2]);
                timeView.setText(fmt(cur));durationView.setText(fmt(dur));playBtn.setText(st==1?"❚❚":"▶");
                if(!userSeeking&&dur>0)seek.setProgress((int)Math.max(0,Math.min(1000,(cur/dur)*1000)));
            }catch(Exception ignored){}
        });
        handler.postDelayed(this,1000);
    }};

    final Runnable hideControls=()->setControls(false);
    void showControls(){setControls(true);handler.removeCallbacks(hideControls);handler.postDelayed(hideControls,3500);}
    void setControls(boolean show){controlsVisible=show;int v=show?View.VISIBLE:View.GONE;topBar.setVisibility(v);bottomBar.setVisibility(v);playBtn.setVisibility(v);}

    @Override public boolean onKeyDown(int key,KeyEvent e){
        if(key==KeyEvent.KEYCODE_DPAD_CENTER||key==KeyEvent.KEYCODE_ENTER||key==KeyEvent.KEYCODE_MEDIA_PLAY_PAUSE){eval("gpToggle()");showControls();return true;}
        if(key==KeyEvent.KEYCODE_DPAD_LEFT){eval("if(ready)player.seekTo(Math.max(0,player.getCurrentTime()-10),true)");showControls();return true;}
        if(key==KeyEvent.KEYCODE_DPAD_RIGHT){eval("if(ready)player.seekTo(player.getCurrentTime()+10,true)");showControls();return true;}
        if(key==KeyEvent.KEYCODE_BACK){finish();return true;}
        return super.onKeyDown(key,e);
    }

    @Override protected void onPause(){eval("if(ready)player.pauseVideo()");super.onPause();}
    @Override protected void onDestroy(){
        handler.removeCallbacksAndMessages(null);
        if(web!=null){try{web.stopLoading();web.loadUrl("about:blank");web.removeAllViews();web.destroy();}catch(Exception ignored){}web=null;}
        super.onDestroy();
    }
}
''')

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52847' in t and "versionName '5.28.47'" in t
t=t.replace('versionCode 52847','versionCode 52848',1).replace("versionName '5.28.47'","versionName '5.28.48'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52848.txt').write_text("""GreenPlay 5.28.48

- GreenShorts: botão mostra somente Assistir.
- Reprodução com moldura/controles próprios do GreenPlay.
- O player incorporado usa controles nativos do app; controles padrão externos ficam desativados.
- Compatível com controle remoto: OK play/pause, esquerda/direita -10/+10s.
- Catálogo GreenShorts continua vindo do endpoint próprio do painel.
- O servidor filtra PT-BR e elimina vídeo/série repetidos entre canais.
""")

assert 'Assistir no YouTube' not in p.read_text()
assert 'versionCode 52848' in b.read_text()
print('OK 5.28.48')
