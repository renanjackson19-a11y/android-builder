package fun.greenplay.app;

import android.app.*;
import android.os.*;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.view.*;
import android.widget.*;
import android.content.*;
import android.content.pm.ActivityInfo;
import org.json.*;
import java.util.*;

import androidx.media3.common.C;
import androidx.media3.common.MediaItem;
import androidx.media3.common.PlaybackException;
import androidx.media3.common.Player;
import androidx.media3.exoplayer.ExoPlayer;
import androidx.media3.ui.AspectRatioFrameLayout;
import androidx.media3.ui.PlayerView;

public class StoriesActivity extends Activity {
    FrameLayout root, storyLayer;
    ImageView banner, logoTop;
    PlayerView playerView;
    ExoPlayer player;
    View shade, swipe;
    LinearLayout info, actions;
    TextView title, watchNow, fav, comments, back, hint;
    ProgressBar progress;
    Handler h = new Handler(Looper.getMainLooper());
    android.content.SharedPreferences sp;

    JSONArray items = new JSONArray();
    JSONArray categories = new JSONArray();
    final HashSet<String> seen = new HashSet<>();
    final ArrayList<String> sourceUrls = new ArrayList<>();

    int index=0, accent=Color.rgb(184,0,125), storyToken=0, sourceIndex=0, fetchRound=0, pendingCategoryCalls=0;
    boolean tvMode=false, dragging=false, swipeAnimating=false, loading=false, ready=false, openingFull=false;
    float downY=0, downX=0;
    String uid="";
    JSONObject currentResolved=null;
    static final long PREVIEW_MS=120000L;

    int dp(int n){return (int)(n*getResources().getDisplayMetrics().density+.5f);}
    GradientDrawable round(int c,int r){GradientDrawable g=new GradientDrawable();g.setColor(c);g.setCornerRadius(dp(r));return g;}
    TextView t(String s,int z){TextView v=new TextView(this);v.setText(s);v.setTextColor(Color.WHITE);v.setTextSize(z);v.setGravity(Gravity.CENTER);return v;}

    @Override public void onCreate(Bundle b){
        super.onCreate(b);
        sp=getSharedPreferences("yelly",0);
        uid=getIntent()==null?"":getIntent().getStringExtra("user_id");if(uid==null)uid="";
        try{accent=Color.parseColor(sp.getString("app_color","#B8007D"));}catch(Exception ignored){}
        tvMode=DeviceCompat.isTelevisionDevice(this);
        try{setRequestedOrientation(tvMode?ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE:ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);}catch(Exception ignored){}
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        immersive();build();buildPlayer();fetchCatalog();
    }

    void immersive(){if(tvMode)return;try{getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY|View.SYSTEM_UI_FLAG_FULLSCREEN|View.SYSTEM_UI_FLAG_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN|View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_LAYOUT_STABLE);}catch(Exception ignored){}}
    @Override public void onWindowFocusChanged(boolean has){super.onWindowFocusChanged(has);if(has)immersive();}

    void build(){
        root=new FrameLayout(this);root.setBackgroundColor(Color.BLACK);
        banner=new ImageView(this);banner.setScaleType(ImageView.ScaleType.CENTER_CROP);banner.setImageResource(R.drawable.story_banner_bg);root.addView(banner,new FrameLayout.LayoutParams(-1,-1));

        storyLayer=new FrameLayout(this);storyLayer.setBackgroundColor(Color.TRANSPARENT);
        FrameLayout.LayoutParams slp=new FrameLayout.LayoutParams(-1,-1);root.addView(storyLayer,slp);

        playerView=new PlayerView(this);playerView.setUseController(false);playerView.setResizeMode(AspectRatioFrameLayout.RESIZE_MODE_FIT);playerView.setBackgroundColor(Color.TRANSPARENT);playerView.setShutterBackgroundColor(Color.TRANSPARENT);playerView.setKeepContentOnPlayerReset(true);
        FrameLayout.LayoutParams pp=new FrameLayout.LayoutParams(-1,-1);if(!tvMode){pp.setMargins(0,dp(64),0,dp(150));}storyLayer.addView(playerView,pp);

        shade=new View(this);GradientDrawable sbg=new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM,new int[]{0x33000000,0x00000000,0x00000000,0xaa090508});shade.setBackground(sbg);storyLayer.addView(shade,new FrameLayout.LayoutParams(-1,-1));

        swipe=new View(this);swipe.setBackgroundColor(Color.TRANSPARENT);swipe.setOnTouchListener((v,e)->{
            if(swipeAnimating)return true;int a=e.getActionMasked();
            if(a==MotionEvent.ACTION_DOWN){downY=e.getY();downX=e.getX();dragging=false;return true;}
            if(a==MotionEvent.ACTION_MOVE){float dy=e.getY()-downY,dx=e.getX()-downX;if(Math.abs(dy)>dp(4)&&Math.abs(dy)>Math.abs(dx)){dragging=true;setSwipeOffset(dy);}return true;}
            if(a==MotionEvent.ACTION_UP||a==MotionEvent.ACTION_CANCEL){float dy=e.getY()-downY,dx=e.getX()-downX;if(dragging&&Math.abs(dy)>dp(72)&&Math.abs(dy)>Math.abs(dx))animateStorySwap(dy<0);else{animateSwipeBack();if(!dragging)toggle();}dragging=false;return true;}return true;
        });root.addView(swipe,new FrameLayout.LayoutParams(-1,-1));

        back=t("‹",34);back.setBackground(round(0x77000000,24));back.setOnClickListener(v->finish());FrameLayout.LayoutParams bp=new FrameLayout.LayoutParams(dp(48),dp(48),Gravity.TOP|Gravity.LEFT);bp.setMargins(dp(14),dp(14),0,0);root.addView(back,bp);

        logoTop=new ImageView(this);logoTop.setImageResource(R.drawable.yelly_logo);logoTop.setScaleType(ImageView.ScaleType.FIT_CENTER);FrameLayout.LayoutParams lpLogo=new FrameLayout.LayoutParams(dp(100),dp(46),Gravity.TOP|Gravity.RIGHT);lpLogo.setMargins(0,dp(16),dp(12),0);root.addView(logoTop,lpLogo);

        info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(18),dp(8),dp(96),dp(8));
        title=t("Carregando Stories…",19);title.setGravity(Gravity.LEFT);title.setTypeface(null,1);title.setMaxLines(3);title.setEllipsize(android.text.TextUtils.TruncateAt.END);info.addView(title,new LinearLayout.LayoutParams(-1,-2));
        watchNow=t("▶  Assistir agora",13);watchNow.setTypeface(null,1);watchNow.setGravity(Gravity.CENTER);watchNow.setTextColor(Color.WHITE);watchNow.setBackground(round(accent,16));watchNow.setPadding(dp(15),dp(8),dp(15),dp(8));watchNow.setOnClickListener(v->openFull());LinearLayout.LayoutParams wlp=new LinearLayout.LayoutParams(-2,dp(42));wlp.setMargins(0,dp(9),0,0);info.addView(watchNow,wlp);
        FrameLayout.LayoutParams ip=new FrameLayout.LayoutParams(-1,dp(178),Gravity.BOTTOM);ip.setMargins(0,0,0,dp(34));root.addView(info,ip);

        actions=new LinearLayout(this);actions.setOrientation(LinearLayout.VERTICAL);actions.setGravity(Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);
        fav=action("♡\nFavoritar");fav.setOnClickListener(v->toggleFav());actions.addView(fav,new LinearLayout.LayoutParams(dp(80),dp(76)));
        comments=action("💬\nComentários");LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(dp(80),dp(76));cp.setMargins(0,dp(8),0,0);actions.addView(comments,cp);comments.setOnClickListener(v->openComments());
        FrameLayout.LayoutParams ap=new FrameLayout.LayoutParams(dp(84),dp(172),Gravity.RIGHT|Gravity.BOTTOM);ap.setMargins(0,0,dp(7),dp(122));root.addView(actions,ap);

        hint=t(tvMode?"↑ ↓  trocar Story":"",12);hint.setTextColor(0xffd4c4cc);if(tvMode){FrameLayout.LayoutParams hp=new FrameLayout.LayoutParams(-2,dp(32),Gravity.TOP|Gravity.CENTER_HORIZONTAL);hp.setMargins(0,dp(16),0,0);root.addView(hint,hp);}

        progress=new ProgressBar(this,null,android.R.attr.progressBarStyleHorizontal);progress.setMax(1000);progress.setProgress(0);if(Build.VERSION.SDK_INT>=21){progress.setProgressTintList(android.content.res.ColorStateList.valueOf(accent));progress.setProgressBackgroundTintList(android.content.res.ColorStateList.valueOf(0x55ffffff));}FrameLayout.LayoutParams pg=new FrameLayout.LayoutParams(-1,dp(3),Gravity.TOP);pg.setMargins(dp(12),dp(4),dp(12),0);root.addView(progress,pg);
        setContentView(root);
    }

    TextView action(String label){TextView v=t(label,11);v.setTypeface(null,1);v.setBackground(round(0x66000000,18));v.setPadding(dp(5),dp(8),dp(5),dp(8));v.setFocusable(true);return v;}

    void buildPlayer(){
        player=new ExoPlayer.Builder(this).build();playerView.setPlayer(player);
        player.addListener(new Player.Listener(){
            @Override public void onPlaybackStateChanged(int state){
                if(state==Player.STATE_READY){ready=true;startTicker();}
                else if(state==Player.STATE_ENDED){advanceAfterPreview();}
            }
            @Override public void onPlayerError(PlaybackException error){if(!tryNextSource())advanceUnavailable();}
        });
    }

    void fetchCatalog(){
        if(loading)return;loading=true;title.setText(items.length()==0?"Carregando doramas…":title.getText());
        Api.post("get_category",Api.m("type","movie","user_id",uid),new Api.CB(){public void ok(JSONObject j){categories=j.optJSONArray("result");if(categories==null)categories=new JSONArray();shuffleArray(categories);fetchCategoryWave();}public void err(String e){loading=false;title.setText("Não foi possível carregar os Stories.");}});
    }

    void fetchCategoryWave(){
        if(categories==null||categories.length()==0){loading=false;if(items.length()==0)title.setText("Nenhum conteúdo disponível agora.");return;}
        int take=Math.min(8,categories.length());pendingCategoryCalls=take;final int round=fetchRound++;
        for(int k=0;k<take;k++){
            JSONObject cat=categories.optJSONObject((round*take+k)%categories.length());if(cat==null){categoryDone();continue;}
            String cid=cat.optString("category_id",cat.optString("id","")).trim();if(cid.isEmpty()){categoryDone();continue;}
            int pg=round==0?1:1+new java.util.Random(System.nanoTime()+k).nextInt(6);
            Api.post("content_by_category",Api.m("user_id",uid,"type","movie","category_id",cid,"page_no",String.valueOf(pg),"page",String.valueOf(pg),"offset",String.valueOf((pg-1)*30),"limit","30","per_page","30","full_catalog","0"),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");appendCatalog(a);categoryDone();}public void err(String e){categoryDone();}});
        }
    }

    void categoryDone(){pendingCategoryCalls--;if(pendingCategoryCalls>0)return;loading=false;if(items.length()>0){shuffleArray(items);if(index>=items.length())index=0;if(currentResolved==null)show(index);}else if(fetchRound<3){fetchCategoryWave();}else title.setText("Nenhum conteúdo disponível agora.");}

    void appendCatalog(JSONArray a){if(a==null)return;for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;String id=x.optString("id",x.optString("video_id","")).trim();if(id.isEmpty())continue;String key="movie|"+id;if(seen.add(key)){try{x.put("video_type",1);x.put("type_id",1);}catch(Exception ignored){}items.put(x);}}}

    void shuffleArray(JSONArray a){if(a==null||a.length()<2)return;try{ArrayList<JSONObject> l=new ArrayList<>();for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x!=null)l.add(x);}Collections.shuffle(l,new Random(System.nanoTime()));JSONArray n=new JSONArray();for(JSONObject x:l)n.put(x);if(a==items)items=n;else if(a==categories)categories=n;}catch(Exception ignored){}}

    void show(int i){
        if(items.length()==0)return;index=Math.max(0,Math.min(items.length()-1,i));JSONObject x=items.optJSONObject(index);if(x==null)return;
        int token=++storyToken;ready=false;openingFull=false;currentResolved=null;sourceUrls.clear();sourceIndex=0;if(player!=null){player.stop();player.clearMediaItems();}
        String nm=cleanTitle(x.optString("name",x.optString("title","Yelly Doramas")));title.setText(nm);watchNow.setText("▶  Assistir agora");progress.setProgress(0);fav.setText(isFav(x)?"♥\nFavorito":"♡\nFavoritar");
        resolveItem(x,token,false);
        if(index>=items.length()-12&&!loading)fetchCategoryWave();
    }

    void resolveItem(JSONObject x,int token,boolean forFull){
        String direct=playUrl(x);if(!direct.isEmpty()){currentResolved=x;if(forFull)launchFull(x);else startPreview(x,token);return;}
        String id=x.optString("id",x.optString("video_id","")).trim();if(id.isEmpty()){if(forFull)Toast.makeText(this,"Conteúdo indisponível.",Toast.LENGTH_SHORT).show();else advanceUnavailable();return;}
        Api.post("content_detail",Api.m("user_id",uid,"video_id",id,"video_type","1"),new Api.CB(){public void ok(JSONObject j){if(token!=storyToken&&!forFull)return;JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;JSONObject merged=mergeJson(x,d);currentResolved=merged;if(playUrl(merged).isEmpty()){if(forFull)Toast.makeText(StoriesActivity.this,"Conteúdo indisponível.",Toast.LENGTH_SHORT).show();else advanceUnavailable();return;}if(forFull)launchFull(merged);else startPreview(merged,token);}public void err(String e){if(forFull)Toast.makeText(StoriesActivity.this,"Não foi possível abrir o conteúdo.",Toast.LENGTH_SHORT).show();else advanceUnavailable();}});
    }

    JSONObject mergeJson(JSONObject base,JSONObject more){JSONObject o=new JSONObject();try{if(base!=null){Iterator<String> it=base.keys();while(it.hasNext()){String k=it.next();o.put(k,base.opt(k));}}if(more!=null){Iterator<String> it=more.keys();while(it.hasNext()){String k=it.next();Object v=more.opt(k);if(v!=null)o.put(k,v);}}}catch(Exception ignored){}return o;}
    String val(JSONObject x,String...keys){if(x==null)return "";for(String k:keys){String v=x.optString(k,"").trim();if(!v.isEmpty())return v;}return "";}
    String playUrl(JSONObject x){return val(x,"video_1080","video_720","video_480","video_320","video_url","stream_url","url");}
    void collectSources(JSONObject x){sourceUrls.clear();String[] ks={"video_1080","video_720","video_480","video_320","video_url","stream_url","url"};for(String k:ks){String u=x.optString(k,"").trim();if(!u.isEmpty()&&!sourceUrls.contains(u))sourceUrls.add(u);}sourceIndex=0;}

    void startPreview(JSONObject x,int token){if(token!=storyToken||player==null)return;collectSources(x);if(sourceUrls.isEmpty()){advanceUnavailable();return;}setSource(sourceIndex);}
    void setSource(int idx){if(player==null||idx<0||idx>=sourceUrls.size())return;sourceIndex=idx;ready=false;try{player.stop();player.clearMediaItems();player.setMediaItem(MediaItem.fromUri(sourceUrls.get(idx)));player.setPlayWhenReady(true);player.prepare();}catch(Exception e){if(!tryNextSource())advanceUnavailable();}}
    boolean tryNextSource(){if(sourceIndex+1>=sourceUrls.size())return false;sourceIndex++;h.postDelayed(()->setSource(sourceIndex),120);return true;}

    final Runnable ticker=new Runnable(){public void run(){if(isFinishing()||player==null)return;try{long pos=Math.max(0,player.getCurrentPosition());long dur=player.getDuration();long cap=(dur==C.TIME_UNSET||dur<=0)?PREVIEW_MS:Math.min(PREVIEW_MS,dur);if(cap<=0)cap=PREVIEW_MS;progress.setProgress((int)Math.max(0,Math.min(1000,(pos*1000L)/cap)));if(pos>=cap-120&&player.isPlaying()){advanceAfterPreview();return;}}catch(Exception ignored){}h.postDelayed(this,250);}};
    void startTicker(){h.removeCallbacks(ticker);h.post(ticker);}
    void advanceAfterPreview(){h.removeCallbacks(ticker);if(!swipeAnimating&&!dragging)animateStorySwap(true);}
    void advanceUnavailable(){h.postDelayed(()->{if(!isFinishing()&&!swipeAnimating)animateStorySwap(true);},450);}

    void toggle(){if(player==null||!ready)return;if(player.isPlaying())player.pause();else player.play();}
    void next(){if(index+1<items.length())show(index+1);else{if(!loading)fetchCategoryWave();}}
    void prev(){if(index>0)show(index-1);}

    void setSwipeOffset(float y){float lim=Math.max(1,root.getHeight());float v=Math.max(-lim,Math.min(lim,y));if(storyLayer!=null)storyLayer.setTranslationY(v);if(info!=null)info.setTranslationY(v);if(actions!=null)actions.setTranslationY(v);}
    void animateSwipeBack(){if(root==null)return;swipeAnimating=true;animateViews(0,120,()->swipeAnimating=false);}
    void animateStorySwap(boolean forward){if(forward&&index+1>=items.length()){if(!loading)fetchCategoryWave();animateSwipeBack();return;}if(!forward&&index<=0){animateSwipeBack();return;}swipeAnimating=true;float hgt=Math.max(1,root.getHeight());float out=forward?-hgt:hgt;float incoming=forward?hgt:-hgt;animateViews(out,130,()->{int ni=forward?index+1:index-1;show(ni);setSwipeOffset(incoming);animateViews(0,165,()->swipeAnimating=false);});}
    void animateViews(float y,long ms,Runnable end){if(storyLayer!=null)storyLayer.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)�ctions.animate().translationY(y).setDuration(ms).withEndAction(end).start();else if(end!=null)end.run();}

    String key(JSONObject x){return "movie|"+x.optString("id",x.optString("video_id",x.optString("name","")));}
    boolean isFav(JSONObject x){try{JSONArray a=new JSONArray(sp.getString("favs","[]"));String k=key(x);for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o!=null&&k.equals(key(o)))return true;}}catch(Exception ignored){}return false;}
    void toggleFav(){JSONObject x=items.optJSONObject(index);if(x==null)return;try{JSONArray a=new JSONArray(sp.getString("favs","[]"));String k=key(x);for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o!=null&&k.equals(key(o))){a.remove(i);sp.edit().putString("favs",a.toString()).apply();fav.setText("♡\nFavoritar");return;}}a.put(x);sp.edit().putString("favs",a.toString()).apply();fav.setText("♥\nFavorito");}catch(Exception ignored){}}

    String commentId(JSONObject x){return x==null?"":x.optString("id",x.optString("video_id",""));}
    void openComments(){JSONObject x=items.optJSONObject(index);if(x==null)return;final String vid=commentId(x);if(vid.isEmpty())return;final Dialog d=new Dialog(this);LinearLayout box=new LinearLayout(this);box.setOrientation(LinearLayout.VERTICAL);box.setPadding(dp(16),dp(14),dp(16),dp(12));box.setBackground(round(0xff160b12,24));LinearLayout head=new LinearLayout(this);head.setGravity(Gravity.CENTER_VERTICAL);TextView hh=t("Comentários",20);hh.setTypeface(null,1);hh.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);head.addView(hh,new LinearLayout.LayoutParams(0,dp(48),1));TextView close=t("✕",20);close.setGravity(Gravity.CENTER);close.setBackground(round(0xff2a1721,18));head.addView(close,new LinearLayout.LayoutParams(dp(44),dp(44)));box.addView(head,new LinearLayout.LayoutParams(-1,dp(52)));ScrollView sv=new ScrollView(this);LinearLayout list=new LinearLayout(this);list.setOrientation(LinearLayout.VERTICAL);sv.addView(list,new ScrollView.LayoutParams(-1,-2));box.addView(sv,new LinearLayout.LayoutParams(-1,0,1));LinearLayout send=new LinearLayout(this);send.setGravity(Gravity.CENTER_VERTICAL);EditText input=new EditText(this);input.setHint("Escreva um comentário…");input.setHintTextColor(0xff968990);input.setTextColor(Color.WHITE);input.setTextSize(14);input.setSingleLine(false);input.setMaxLines(3);input.setPadding(dp(14),dp(8),dp(12),dp(8));input.setBackground(round(0xff24131d,16));send.addView(input,new LinearLayout.LayoutParams(0,dp(58),1));TextView go=t("Enviar",14);go.setTypeface(null,1);go.setTextColor(Color.WHITE);go.setBackground(round(accent,16));go.setGravity(Gravity.CENTER);LinearLayout.LayoutParams gp=new LinearLayout.LayoutParams(dp(82),dp(54));gp.setMargins(dp(8),0,0,0);send.addView(go,gp);box.addView(send,new LinearLayout.LayoutParams(-1,dp(66)));d.setContentView(box);close.setOnClickListener(v->d.dismiss());go.setOnClickListener(v->{String c=input.getText().toString().trim();if(c.isEmpty())return;if(uid.isEmpty()){Toast.makeText(this,"Entre na sua conta para comentar.",Toast.LENGTH_SHORT).show();return;}go.setEnabled(false);Api.post("add_comment",Api.m("user_id",uid,"youtube_id","","video_id",vid,"story_title",cleanTitle(x.optString("name",x.optString("title","Yelly Doramas"))),"comment",c),new Api.CB(){public void ok(JSONObject j){runOnUiThread(()->{go.setEnabled(true);input.setText("");loadComments(x,list);});}public void err(String e){runOnUiThread(()->{go.setEnabled(true);Toast.makeText(StoriesActivity.this,"Não foi possível comentar.",Toast.LENGTH_SHORT).show();});}});});d.setOnShowListener(z->{Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(Color.TRANSPARENT));w.setDimAmount(.45f);w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);w.setGravity(Gravity.BOTTOM);w.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);w.setLayout(-1,(int)(getResources().getDisplayMetrics().heightPixels*.76f));}});d.show();loadComments(x,list);}
    void loadComments(JSONObject x,LinearLayout host){host.removeAllViews();String vid=commentId(x);Api.post("get_comment",Api.m("user_id",uid,"youtube_id","","video_id",vid,"limit","80"),new Api.CB(){public void ok(JSONObject j){runOnUiThread(()->{host.removeAllViews();JSONArray a=j.optJSONArray("result");if(a==null||a.length()==0){TextView e=t("Seja o primeiro a comentar.",14);e.setTextColor(0xffb7abb2);e.setPadding(dp(4),dp(18),dp(4),dp(18));host.addView(e);return;}for(int i=0;i<a.length();i++){JSONObject c=a.optJSONObject(i);if(c!=null)host.addView(commentCard(c));}});}public void err(String e){runOnUiThread(()->{host.removeAllViews();TextView m=t("Não foi possível carregar os comentários.",13);m.setTextColor(0xffb7abb2);m.setPadding(0,dp(18),0,dp(18));host.addView(m);});}});}
    View commentCard(JSONObject c){LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setPadding(dp(12),dp(10),dp(12),dp(10));GradientDrawable bg=round(0xff21131a,14);bg.setStroke(dp(1),0xff4a2938);card.setBackground(bg);TextView who=t(c.optString("user_name","Cliente"),13);who.setGravity(Gravity.LEFT);who.setTypeface(null,1);who.setTextColor(0xffff8ec0);card.addView(who);TextView body=t(c.optString("comment",""),14);body.setGravity(Gravity.LEFT);body.setPadding(0,dp(5),0,0);card.addView(body);String reply=c.optString("admin_reply","").trim();if(!reply.isEmpty()){TextView rep=t("Yelly: "+reply,13);rep.setGravity(Gravity.LEFT);rep.setTextColor(0xffffbedb);rep.setPadding(dp(10),dp(8),0,0);card.addView(rep);}LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2);lp.setMargins(0,0,0,dp(8));card.setLayoutParams(lp);return card;}

    void openFull(){JSONObject x=items.optJSONObject(index);if(x==null||openingFull)return;openingFull=true;int token=storyToken;JSONObject r=currentResolved;if(r!=null&&!playUrl(r).isEmpty())launchFull(r);else resolveItem(x,token,true);}
    void launchFull(JSONObject x){openingFull=false;String url=playUrl(x);if(url.isEmpty())return;if(player!=null)player.pause();Intent in=new Intent(this,PlayerActivity.class);in.putExtra("url",url);in.putExtra("url_1080",x.optString("video_1080",""));in.putExtra("url_720",x.optString("video_720",""));in.putExtra("url_480",x.optString("video_480",""));in.putExtra("url_320",x.optString("video_320",""));String nm=cleanTitle(x.optString("name",x.optString("title","Yelly Doramas")));in.putExtra("title",nm);in.putExtra("movie_id",x.optString("id",x.optString("video_id","")));in.putExtra("movie_title",nm);in.putExtra("movie_poster",val(x,"thumbnail","portrait_img","poster","poster_path"));in.putExtra("movie_landscape",val(x,"landscape","landscape_img","backdrop","backdrop_path"));startActivity(in);}

    String cleanTitle(String s){if(s==null)return "Yelly Doramas";s=s.replaceAll("\\s+"," ").trim();return s.isEmpty()?"Yelly Doramas":s;}

    @Override public void onBackPressed(){finish();}
    @Override public boolean dispatchKeyEvent(KeyEvent e){if(tvMode&&e!=null&&e.getAction()==KeyEvent.ACTION_DOWN){int k=e.getKeyCode();if(k==KeyEvent.KEYCODE_DPAD_DOWN){animateStorySwap(true);return true;}if(k==KeyEvent.KEYCODE_DPAD_UP){animateStorySwap(false);return true;}if(k==KeyEvent.KEYCODE_DPAD_CENTER||k==KeyEvent.KEYCODE_ENTER){toggle();return true;}if(k==KeyEvent.KEYCODE_BACK){finish();return true;}}return super.dispatchKeyEvent(e);}
    @Override protected void onPause(){h.removeCallbacks(ticker);try{if(player!=null)player.pause();}catch(Exception ignored){}super.onPause();}
    @Override protected void onResume(){super.onResume();immersive();try{if(player!=null&&ready){player.play();startTicker();}}catch(Exception ignored){}}
    @Override protected void onDestroy(){h.removeCallbacksAndMessages(null);try{if(player!=null){player.release();player=null;}}catch(Exception ignored){}super.onDestroy();}
}
