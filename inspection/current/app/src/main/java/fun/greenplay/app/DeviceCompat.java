package fun.greenplay.app;

import android.app.Activity;
import android.app.UiModeManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.res.Configuration;
import android.os.Build;

/** Device classification kept deliberately independent from brand-specific UI code. */
public final class DeviceCompat {
 private DeviceCompat(){}

 public static boolean isTelevisionDevice(Context context){
  if(context==null)return false;
  try{
   if(context instanceof Activity){
    Intent in=((Activity)context).getIntent();
    if(in!=null&&in.hasCategory(Intent.CATEGORY_LEANBACK_LAUNCHER))return true;
   }
   UiModeManager ui=(UiModeManager)context.getSystemService(Context.UI_MODE_SERVICE);
   if(ui!=null&&ui.getCurrentModeType()==Configuration.UI_MODE_TYPE_TELEVISION)return true;

   PackageManager pm=context.getPackageManager();
   if(pm!=null){
    if(pm.hasSystemFeature(PackageManager.FEATURE_LEANBACK)
      ||pm.hasSystemFeature("android.software.leanback_only")
      ||pm.hasSystemFeature(PackageManager.FEATURE_TELEVISION)
      ||pm.hasSystemFeature("android.hardware.type.television")
      ||pm.hasSystemFeature("amazon.hardware.fire_tv"))return true;
   }

   Configuration cfg=context.getResources().getConfiguration();
   boolean noTouch=cfg.touchscreen==Configuration.TOUCHSCREEN_NOTOUCH;
   if(pm!=null&&!pm.hasSystemFeature(PackageManager.FEATURE_TOUCHSCREEN))noTouch=true;
   boolean dpad=cfg.navigation==Configuration.NAVIGATION_DPAD;
   boolean large=cfg.smallestScreenWidthDp>=600
     ||(cfg.screenLayout&Configuration.SCREENLAYOUT_SIZE_MASK)>=Configuration.SCREENLAYOUT_SIZE_LARGE;
   boolean hdmi=pm!=null&&(pm.hasSystemFeature("android.hardware.hdmi.cec")||pm.hasSystemFeature("android.hardware.hdmi.output"));
   android.util.DisplayMetrics dm=context.getResources().getDisplayMetrics();
   int longPx=Math.max(dm.widthPixels,dm.heightPixels),shortPx=Math.min(dm.widthPixels,dm.heightPixels);
   boolean landscapePanel=longPx>=960&&shortPx>=500&&longPx>shortPx;
   boolean remoteInput=false;
   try{for(int id:android.view.InputDevice.getDeviceIds()){android.view.InputDevice dev=android.view.InputDevice.getDevice(id);if(dev==null)continue;int src=dev.getSources();if((src&android.view.InputDevice.SOURCE_DPAD)==android.view.InputDevice.SOURCE_DPAD||(src&android.view.InputDevice.SOURCE_GAMEPAD)==android.view.InputDevice.SOURCE_GAMEPAD){remoteInput=true;break;}}}catch(Exception ignored){}
   if(hdmi&&dpad)return true;
   if(noTouch&&large&&(dpad||hdmi||cfg.smallestScreenWidthDp>=720))return true;
   // V16.138: muitas TV Boxes genéricas anunciam densidade/tamanho como telefone e não expõem LEANBACK.
   // Ausência real de touchscreen + saída fixa 16:9/HD já é um sinal forte e evita cair no layout móvel ampliado.
   if(noTouch&&landscapePanel)return true;
   if(landscapePanel&&remoteInput&&hdmi)return true;

   String fingerprint=(Build.MANUFACTURER+" "+Build.BRAND+" "+Build.MODEL+" "+Build.PRODUCT+" "+Build.DEVICE+" "+Build.HARDWARE).toLowerCase(java.util.Locale.ROOT);
   if(containsAny(fingerprint,"fire tv","firetv","android tv","google tv","bravia","shield android tv","mibox","mi box","tvbox","tv box","smart tv","smarttv","mecool","formuler","vontar","tanix","a95x")
      ||(landscapePanel&&containsAny(fingerprint,"x96","mxq","h96","tx3","tx6","tx9","hk1","t95","qplus","q plus","s905","s912","s922","rk322","rk3318","rk3328","rk3566","amlogic","rockchip","allwinner","onn. 4k","chromecast")))return true;
  }catch(Exception ignored){}
  return false;
 }

 private static boolean containsAny(String source,String... terms){
  if(source==null)return false;
  for(String term:terms)if(term!=null&&!term.isEmpty()&&source.contains(term))return true;
  return false;
 }
}
