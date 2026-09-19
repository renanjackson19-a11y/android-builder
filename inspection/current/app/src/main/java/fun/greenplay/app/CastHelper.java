package fun.greenplay.app;

import android.app.*;
import android.content.*;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.os.*;
import android.view.*;
import android.widget.*;
import androidx.mediarouter.app.MediaRouteChooserDialog;
import androidx.mediarouter.media.MediaRouteSelector;
import androidx.mediarouter.media.MediaRouter;
import com.google.android.gms.cast.CastMediaControlIntent;
import com.google.android.gms.cast.MediaInfo;
import com.google.android.gms.cast.MediaLoadRequestData;
import com.google.android.gms.cast.MediaMetadata;
import com.google.android.gms.cast.framework.CastContext;
import com.google.android.gms.cast.framework.CastSession;
import com.google.android.gms.cast.framework.media.RemoteMediaClient;

public final class CastHelper {
 private CastHelper(){}
 public static boolean isConnected(Activity a){try{if(a==null)return false;CastSession s=CastContext.getSharedInstance(a).getSessionManager().getCurrentCastSession();return s!=null&&s.isConnected();}catch(Exception e){return false;}}
 public static void openChooser(Activity a){if(a==null)return;if(DeviceCompat.isTelevisionDevice(a))return;try{CastContext ctx=CastContext.getSharedInstance(a);CastSession current=ctx.getSessionManager().getCurrentCastSession();if(current!=null&&current.isConnected()){Toast.makeText(a,"TV já conectada. Escolha um conteúdo para transmitir.",Toast.LENGTH_SHORT).show();return;}MediaRouteChooserDialog chooser=new MediaRouteChooserDialog(a,R.style.GreenPlayCastDialogTheme);MediaRouteSelector selector=selector();MediaRouter router=MediaRouter.getInstance(a);MediaRouter.Callback scan=new MediaRouter.Callback(){};router.addCallback(selector,scan,MediaRouter.CALLBACK_FLAG_PERFORM_ACTIVE_SCAN);chooser.setRouteSelector(selector);chooser.setTitle("Conectar à TV");chooser.setOnDismissListener(d->{try{router.removeCallback(scan);}catch(Exception ignored){}if(!isConnected(a))Toast.makeText(a,"Se a TV/Box não tiver Google Cast, segure o botão Transmitir para abrir o espelhamento do Android.",Toast.LENGTH_LONG).show();});chooser.show();}catch(Exception e){openSystemMirror(a);}}
 public static void cast(Activity a,String url,String title,boolean live,Runnable onStarted){
  if(a!=null&&DeviceCompat.isTelevisionDevice(a))return;
  if(a==null||url==null||url.trim().isEmpty()){Toast.makeText(a,"Conteúdo indisponível para transmitir.",Toast.LENGTH_LONG).show();return;}
  try{
   CastContext ctx=CastContext.getSharedInstance(a);
   CastSession current=ctx.getSessionManager().getCurrentCastSession();
   if(current!=null&&current.isConnected()){load(a,current,url,title,live,onStarted);return;}
   final MediaRouteChooserDialog chooser=new MediaRouteChooserDialog(a, R.style.GreenPlayCastDialogTheme);
   MediaRouteSelector selector=selector();MediaRouter router=MediaRouter.getInstance(a);MediaRouter.Callback scan=new MediaRouter.Callback(){};router.addCallback(selector,scan,MediaRouter.CALLBACK_FLAG_PERFORM_ACTIVE_SCAN);
   chooser.setRouteSelector(selector);chooser.setTitle("Transmitir para");chooser.setOnDismissListener(d->{try{router.removeCallback(scan);}catch(Exception ignored){}});chooser.show();
   final Handler h=new Handler(Looper.getMainLooper());final long until=SystemClock.elapsedRealtime()+30000L;
   Runnable check=new Runnable(){public void run(){
    if(a.isFinishing())return;
    try{CastSession s=CastContext.getSharedInstance(a).getSessionManager().getCurrentCastSession();if(s!=null&&s.isConnected()){if(chooser.isShowing())chooser.dismiss();load(a,s,url,title,live,onStarted);return;}}catch(Exception ignored){}
    if(SystemClock.elapsedRealtime()<until&&chooser.isShowing())h.postDelayed(this,350);
   }};h.postDelayed(check,350);
  }catch(Exception e){
   android.util.Log.w("GreenPlayCast","Google Cast indisponivel; usando espelhamento do sistema",e);
   openSystemMirror(a);
  }
 }
 public static void openSystemMirror(Activity a){
  if(a==null)return;
  String[] actions={android.provider.Settings.ACTION_CAST_SETTINGS,"android.settings.WIFI_DISPLAY_SETTINGS",android.provider.Settings.ACTION_WIRELESS_SETTINGS};
  for(String action:actions){
   try{
    Intent in=new Intent(action);
    if(in.resolveActivity(a.getPackageManager())!=null){
     Toast.makeText(a,"Google Cast indisponível neste dispositivo. Iniciando espelhamento de tela...",Toast.LENGTH_LONG).show();
     a.startActivity(in);
     return;
    }
   }catch(Exception ignored){}
  }
  Toast.makeText(a,"Este aparelho não oferece Google Cast nem uma tela de espelhamento compatível.",Toast.LENGTH_LONG).show();
 }
 static MediaRouteSelector selector(){return new MediaRouteSelector.Builder().addControlCategory(CastMediaControlIntent.categoryForCast(CastMediaControlIntent.DEFAULT_MEDIA_RECEIVER_APPLICATION_ID)).build();}
 static void load(Activity a,CastSession session,String url,String title,boolean live,Runnable onStarted){
  try{RemoteMediaClient client=session.getRemoteMediaClient();if(client==null){Toast.makeText(a,"Não foi possível controlar a TV selecionada.",Toast.LENGTH_LONG).show();return;}
   MediaMetadata meta=new MediaMetadata(MediaMetadata.MEDIA_TYPE_MOVIE);meta.putString(MediaMetadata.KEY_TITLE,title==null||title.trim().isEmpty()?"GreenPlay":title.trim());
   MediaInfo info=new MediaInfo.Builder(url).setStreamType(live?MediaInfo.STREAM_TYPE_LIVE:MediaInfo.STREAM_TYPE_BUFFERED).setContentType(contentType(url)).setMetadata(meta).build();
   MediaLoadRequestData req=new MediaLoadRequestData.Builder().setMediaInfo(info).setAutoplay(true).build();client.load(req);
   Toast.makeText(a,"Reprodução enviada para a TV. Você pode apagar a tela do celular.",Toast.LENGTH_LONG).show();if(onStarted!=null)onStarted.run();
  }catch(Exception e){Toast.makeText(a,"A TV não conseguiu iniciar este conteúdo.",Toast.LENGTH_LONG).show();}
 }
 static String contentType(String u){String s=u==null?"":u.toLowerCase(java.util.Locale.ROOT);if(s.contains(".m3u8"))return "application/x-mpegURL";if(s.contains(".ts")||s.contains("mpegts"))return "video/mp2t";if(s.contains(".webm"))return "video/webm";return "video/mp4";}
}
