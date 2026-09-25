from pathlib import Path

root=Path("work")
app=root/"app/src/main/java/fun/greenplay/app"
p=app/"YouTubePlayerActivity.java"
s=p.read_text(encoding="utf-8")

# Match the GreenPlay 5.28.90 dorama player behavior that hides the embedded
# player's top/bottom chrome behind app-owned framing and controls.
old='''        web=new WebView(this);web.setBackgroundColor(Color.BLACK);
        WebSettings ws=web.getSettings();
        ws.setJavaScriptEnabled(true);ws.setDomStorageEnabled(true);ws.setMediaPlaybackRequiresUserGesture(false);
        ws.setLoadsImagesAutomatically(true);ws.setUseWideViewPort(true);ws.setLoadWithOverviewMode(true);'''
new='''        web=new WebView(this);web.setBackgroundColor(Color.BLACK);web.setAlpha(tvMode?0f:1f);
        SecurityGuard.hardenWebView();
        WebSettings ws=web.getSettings();
        ws.setJavaScriptEnabled(true);ws.setDomStorageEnabled(true);ws.setMediaPlaybackRequiresUserGesture(false);
        ws.setAllowFileAccess(false);ws.setAllowContentAccess(false);ws.setSaveFormData(false);
        if(android.os.Build.VERSION.SDK_INT>=21)ws.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        ws.setLoadsImagesAutomatically(true);ws.setUseWideViewPort(true);ws.setLoadWithOverviewMode(true);'''
if old not in s: raise SystemExit("web setup anchor missing")
s=s.replace(old,new,1)

old='''        web.setOnTouchListener((v,e)->true);
        root.addView(web,new FrameLayout.LayoutParams(-1,-1));

        touchShield=new View(this);'''
new='''        web.setOnTouchListener((v,e)->true);
        root.addView(web,new FrameLayout.LayoutParams(-1,-1));

        if(!tvMode){
            int screenH=getResources().getDisplayMetrics().heightPixels;
            int topMaskH=Math.max(dp(48),Math.min(dp(82),(int)(screenH*0.09f)));
            int bottomMaskH=Math.max(dp(64),Math.min(dp(110),(int)(screenH*0.11f)));
            View topMask=new View(this);topMask.setBackgroundColor(Color.BLACK);
            FrameLayout.LayoutParams topMaskLp=new FrameLayout.LayoutParams(-1,topMaskH,Gravity.TOP);root.addView(topMask,topMaskLp);
            View bottomMask=new View(this);bottomMask.setBackgroundColor(Color.BLACK);
            FrameLayout.LayoutParams bottomMaskLp=new FrameLayout.LayoutParams(-1,bottomMaskH,Gravity.BOTTOM);root.addView(bottomMask,bottomMaskLp);
        }

        touchShield=new View(this);'''
if old not in s: raise SystemExit("mask anchor missing")
s=s.replace(old,new,1)

old='''        FrameLayout.LayoutParams bp=new FrameLayout.LayoutParams(dp(48),dp(48),Gravity.TOP|Gravity.LEFT);
        bp.setMargins(dp(14),dp(14),0,0);root.addView(back,bp);

        controls=new LinearLayout(this);'''
new='''        FrameLayout.LayoutParams bp=new FrameLayout.LayoutParams(dp(48),dp(48),Gravity.TOP|Gravity.LEFT);
        bp.setMargins(dp(14),dp(14),0,0);root.addView(back,bp);
        back.bringToFront();

        controls=new LinearLayout(this);'''
if old not in s: raise SystemExit("back anchor missing")
s=s.replace(old,new,1)

old='''        FrameLayout.LayoutParams cp=new FrameLayout.LayoutParams(-1,dp(94),Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);
        cp.setMargins(dp(14),0,dp(14),dp(16));root.addView(controls,cp);

        back10.setOnClickListener'''
new='''        FrameLayout.LayoutParams cp=new FrameLayout.LayoutParams(-1,dp(94),Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);
        cp.setMargins(dp(14),0,dp(14),dp(10));root.addView(controls,cp);
        controls.bringToFront();

        back10.setOnClickListener'''
if old not in s: raise SystemExit("controls anchor missing")
s=s.replace(old,new,1)

old='''    void loadPlayer(){
        String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'>"+
            "<style>html,body,#p{margin:0;padding:0;width:100%;height:100%;background:#000;overflow:hidden}iframe{width:100%!important;height:100%!important;border:0}</style>"+
            "<script src='https://www.youtube.com/iframe_api'></script></head><body><div id='p'></div><script>"+
            "var player,ready=false;function onYouTubeIframeAPIReady(){player=new YT.Player('p',{videoId:'"+videoId+"',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,iv_load_policy:3,cc_load_policy:0,playsinline:1,rel:0,origin:'https://yelly.fun'},events:{onReady:function(e){ready=true;e.target.playVideo();}}});}"+'''
new='''    void loadPlayer(){
        String tvCss=tvMode?"transform:scale(1.48);transform-origin:50% 50%;":"";
        String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'>"+
            "<style>html,body,#p{margin:0;padding:0;width:100%;height:100%;background:#000;overflow:hidden}iframe{width:100%!important;height:100%!important;border:0;"+tvCss+"}</style>"+
            "<script src='https://www.youtube.com/iframe_api'></script></head><body><div id='p'></div><script>"+
            "var player,ready=false;function onYouTubeIframeAPIReady(){player=new YT.Player('p',{videoId:'"+videoId+"',playerVars:{autoplay:1,controls:0,disablekb:1,fs:0,iv_load_policy:3,cc_load_policy:0,playsinline:1,rel:0,modestbranding:1,origin:'https://greenplay.fun'},events:{onReady:function(e){ready=true;e.target.playVideo();AndroidBridge.playerReady();}}});}"+'''
if old not in s: raise SystemExit("loadPlayer anchor missing")
s=s.replace(old,new,1)

old='''            "function gpTime(){if(!ready)return '0|0|0';return (player.getCurrentTime()||0)+'|'+(player.getDuration()||0)+'|'+player.getPlayerState();}"+
            "</script></body></html>";
        web.loadDataWithBaseURL("https://yelly.fun/",html,"text/html","UTF-8",null);
    }'''
new='''            "function gpTime(){if(!ready)return '0|0|0';return (player.getCurrentTime()||0)+'|'+(player.getDuration()||0)+'|'+player.getPlayerState();}"+
            "</script></body></html>";
        web.addJavascriptInterface(new Object(){
            @android.webkit.JavascriptInterface public void playerReady(){runOnUiThread(()->{if(web!=null){web.setTranslationX(0f);web.setTranslationY(0f);web.animate().alpha(1f).setDuration(120).start();}});}
        },"AndroidBridge");
        web.loadDataWithBaseURL("https://greenplay.fun/",html,"text/html","UTF-8",null);
    }'''
if old not in s: raise SystemExit("base url anchor missing")
s=s.replace(old,new,1)

# Preserve Yelly accent color while keeping the GreenPlay framing logic.
p.write_text(s,encoding="utf-8")

g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10023" not in t or "versionName '1.0.23'" not in t: raise SystemExit("wrong base")
t=t.replace("versionCode 10023","versionCode 10024",1).replace("versionName '1.0.23'","versionName '1.0.24'",1)
g.write_text(t,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.24
- Corrigido o player de Doramas para reproduzir com o mesmo enquadramento usado no GreenPlay 5.28.90.
- Faixas superior e inferior do player externo ficam cobertas pela moldura do aplicativo no celular.
- Controles do Yelly ficam acima do vídeo: voltar, -10s, play/pause, +10s e progresso.
- Toques continuam bloqueados no player incorporado.
- TV usa o mesmo ajuste de escala do GreenPlay.
- Não altera nenhum arquivo ou build do aplicativo GreenPlay.
""",encoding="utf-8")
print("YELLY_124_EXACT_GREENPLAY_PLAYER_FRAMING_OK")
