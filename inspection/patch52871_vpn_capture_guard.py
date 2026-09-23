from pathlib import Path

g=Path("work/app/build.gradle")
s=g.read_text()
assert "versionCode 52870" in s
assert "versionName '5.28.70'" in s
s=s.replace("versionCode 52870","versionCode 52871",1)
s=s.replace("versionName '5.28.70'","versionName '5.28.71'",1)
g.write_text(s)

# Shared VPN / local packet capture detector.
ng=Path("work/app/src/main/java/fun/greenplay/app/NetworkGuard.java")
ng.write_text(r'''package fun.greenplay.app;

public final class NetworkGuard {
    private NetworkGuard(){}

    public static boolean isVpnOrCaptureActive(android.content.Context context){
        try{
            android.net.ConnectivityManager cm=(android.net.ConnectivityManager)context.getSystemService(android.content.Context.CONNECTIVITY_SERVICE);
            if(cm!=null){
                if(android.os.Build.VERSION.SDK_INT>=23){
                    android.net.Network[] all=cm.getAllNetworks();
                    if(all!=null){
                        for(android.net.Network n:all){
                            android.net.NetworkCapabilities caps=cm.getNetworkCapabilities(n);
                            if(caps!=null&&caps.hasTransport(android.net.NetworkCapabilities.TRANSPORT_VPN))return true;
                        }
                    }
                }else{
                    android.net.NetworkInfo ni=cm.getNetworkInfo(android.net.ConnectivityManager.TYPE_VPN);
                    if(ni!=null&&ni.isConnectedOrConnecting())return true;
                }
            }
        }catch(Exception ignored){}

        // Fallback for VPNService based capture tools such as PCAPdroid/NetGuard
        // on devices that do not expose TRANSPORT_VPN reliably.
        try{
            java.util.Enumeration<java.net.NetworkInterface> en=java.net.NetworkInterface.getNetworkInterfaces();
            while(en!=null&&en.hasMoreElements()){
                java.net.NetworkInterface it=en.nextElement();
                if(it==null||!it.isUp()||it.isLoopback())continue;
                String n=it.getName()==null?"":it.getName().toLowerCase(java.util.Locale.US);
                if(n.startsWith("tun")||n.startsWith("ppp")||n.startsWith("wg")||n.startsWith("ipsec"))return true;
            }
        }catch(Exception ignored){}
        return false;
    }
}
''')

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

old='''boolean authScreen=false,detailOpen=false,searchScreenOpen=false,exitDialogOpen=false,providerSwitchScreen=false,plansScreen=false,providerAvailabilityCheckBusy=false;'''
new='''boolean authScreen=false,detailOpen=false,searchScreenOpen=false,exitDialogOpen=false,providerSwitchScreen=false,plansScreen=false,providerAvailabilityCheckBusy=false,networkGuardBlocking=false;'''
assert old in s
s=s.replace(old,new,1)

old=''' public void onCreate(Bundle b){super.onCreate(b);sp=getSharedPreferences("gp",0);tvMode=DeviceCompat.isTelevisionDevice(this)||sp.getBoolean("force_tv_mode",false);requestedStartNav=getIntent()!=null?getIntent().getIntExtra("gp_restore_nav",-1):-1;configureWindowForCurrentMode();migrateLegacyOfflineDownloads();uid=sp.getString("uid","");reseller=sp.getString("reseller","");Api.PROVIDER=sp.getString("provider_id","");loadIdentityCache();boolean modeChange=getIntent()!=null&&getIntent().getBooleanExtra("gp_mode_change",false);boolean hardModeReload=getIntent()!=null&&getIntent().getBooleanExtra("gp_hard_mode_reload",false);if(uid.isEmpty())login();else if(hardModeReload)startAfterHardModeReload();else if(modeChange)startAfterModeChange();else startExistingSession();refreshIdentity();new Handler(Looper.getMainLooper()).postDelayed(()->{if(!isFinishing())AppUpdater.check(this);},2500);}'''
new=''' public void onCreate(Bundle b){super.onCreate(b);sp=getSharedPreferences("gp",0);tvMode=DeviceCompat.isTelevisionDevice(this)||sp.getBoolean("force_tv_mode",false);requestedStartNav=getIntent()!=null?getIntent().getIntExtra("gp_restore_nav",-1):-1;configureWindowForCurrentMode();migrateLegacyOfflineDownloads();uid=sp.getString("uid","");reseller=sp.getString("reseller","");Api.PROVIDER=sp.getString("provider_id","");loadIdentityCache();if(NetworkGuard.isVpnOrCaptureActive(this)){showNetworkGuardScreen();return;}boolean modeChange=getIntent()!=null&&getIntent().getBooleanExtra("gp_mode_change",false);boolean hardModeReload=getIntent()!=null&&getIntent().getBooleanExtra("gp_hard_mode_reload",false);if(uid.isEmpty())login();else if(hardModeReload)startAfterHardModeReload();else if(modeChange)startAfterModeChange();else startExistingSession();refreshIdentity();new Handler(Looper.getMainLooper()).postDelayed(()->{if(!isFinishing())AppUpdater.check(this);},2500);}'''
assert old in s
s=s.replace(old,new,1)

old=''' @Override protected void onResume(){super.onResume();AppUpdater.resumeInstall(this);new Handler(Looper.getMainLooper()).postDelayed(()->{if(!isFinishing())AppUpdater.check(this);},900);new Handler(Looper.getMainLooper()).postDelayed(()->{if(!isFinishing())checkCurrentProviderAvailability(false);},1400);if(tvMode&&!modeSwitchPending)enterTvImmersiveUi();if(!wideTvUi())enforceGlobalBottomNav();updateGlobalCastButtonState();if(detailOpen&&activeSeriesResumeHost!=null&&activeSeriesDetail!=null)renderSeriesResume(activeSeriesSource,activeSeriesDetail,activeSeriesResumeHost);if(tvResumeAfterFullscreen){tvResumeAfterFullscreen=false;}if(tvResumeAfterBackground&&!tvOrientationTransition&&tvInlinePlayer!=null&&tvActiveChannel!=null){tvResumeAfterBackground=false;resumeTvAtLiveEdge();}if(playerRoundTrip)new Handler(Looper.getMainLooper()).postDelayed(()->restorePlayerReturnState(),60);}'''
new=''' @Override protected void onResume(){super.onResume();if(NetworkGuard.isVpnOrCaptureActive(this)){showNetworkGuardScreen();return;}if(networkGuardBlocking){networkGuardBlocking=false;recreate();return;}AppUpdater.resumeInstall(this);new Handler(Looper.getMainLooper()).postDelayed(()->{if(!isFinishing())AppUpdater.check(this);},900);new Handler(Looper.getMainLooper()).postDelayed(()->{if(!isFinishing())checkCurrentProviderAvailability(false);},1400);if(tvMode&&!modeSwitchPending)enterTvImmersiveUi();if(!wideTvUi())enforceGlobalBottomNav();updateGlobalCastButtonState();if(detailOpen&&activeSeriesResumeHost!=null&&activeSeriesDetail!=null)renderSeriesResume(activeSeriesSource,activeSeriesDetail,activeSeriesResumeHost);if(tvResumeAfterFullscreen){tvResumeAfterFullscreen=false;}if(tvResumeAfterBackground&&!tvOrientationTransition&&tvInlinePlayer!=null&&tvActiveChannel!=null){tvResumeAfterBackground=false;resumeTvAtLiveEdge();}if(playerRoundTrip)new Handler(Looper.getMainLooper()).postDelayed(()->restorePlayerReturnState(),60);}'''
assert old in s
s=s.replace(old,new,1)

anchor=''' void configureWindowForCurrentMode(){'''
guard=r''' void showNetworkGuardScreen(){
  networkGuardBlocking=true;
  try{destroyTvInlinePlayer();}catch(Exception ignored){}
  try{getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);}catch(Exception ignored){}
  FrameLayout gate=new FrameLayout(this);gate.setBackgroundColor(BG);
  LinearLayout box=new LinearLayout(this);box.setOrientation(LinearLayout.VERTICAL);box.setGravity(Gravity.CENTER_HORIZONTAL);box.setPadding(dp(tvMode?54:30),dp(tvMode?34:28),dp(tvMode?54:30),dp(tvMode?34:28));
  GradientDrawable card=round(0xff0d1712,26);card.setStroke(dp(1),0xff2b6a49);box.setBackground(card);
  ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);applyAppLogo(logo);box.addView(logo,new LinearLayout.LayoutParams(-1,dp(tvMode?78:92)));
  TextView title=t("Proteção de conexão",tvMode?26:25);title.setTypeface(null,1);title.setGravity(Gravity.CENTER);LinearLayout.LayoutParams tlp=new LinearLayout.LayoutParams(-1,-2);tlp.setMargins(0,dp(18),0,dp(10));box.addView(title,tlp);
  TextView msg=t("VPN ou aplicativo de captura de rede detectado.\n\nDesative a VPN, PCAPdroid, NetGuard ou outro capturador de tráfego para continuar.",tvMode?16:15);msg.setTextColor(0xffc0cbc5);msg.setGravity(Gravity.CENTER);msg.setLineSpacing(0,1.12f);box.addView(msg,new LinearLayout.LayoutParams(-1,-2));
  Button retry=btn("Verificar novamente");LinearLayout.LayoutParams blp=new LinearLayout.LayoutParams(-1,dp(tvMode?54:52));blp.setMargins(0,dp(24),0,0);box.addView(retry,blp);
  retry.setOnClickListener(v->{if(NetworkGuard.isVpnOrCaptureActive(this)){Toast.makeText(this,"Desative a VPN ou capturador de rede para continuar.",Toast.LENGTH_LONG).show();return;}networkGuardBlocking=false;recreate();});
  FrameLayout.LayoutParams lp=new FrameLayout.LayoutParams(tvMode?dp(760):-1,-2,Gravity.CENTER);lp.setMargins(dp(tvMode?20:24),dp(20),dp(tvMode?20:24),dp(20));gate.addView(box,lp);setContentView(gate);
  if(tvMode){retry.setFocusable(true);retry.requestFocus();}
 }
'''
assert anchor in s
s=s.replace(anchor,guard+anchor,1)
p.write_text(s)

# Block direct player if VPN/capture is enabled after the user already entered the app.
p=Path("work/app/src/main/java/fun/greenplay/app/PlayerActivity.java")
s=p.read_text()
old=''' public void onCreate(Bundle b){super.onCreate(b);tvMode=DeviceCompat.isTelevisionDevice(this);'''
new=''' public void onCreate(Bundle b){super.onCreate(b);if(NetworkGuard.isVpnOrCaptureActive(this)){Toast.makeText(this,"Desative a VPN ou capturador de rede para continuar.",Toast.LENGTH_LONG).show();finish();return;}tvMode=DeviceCompat.isTelevisionDevice(this);'''
assert old in s
s=s.replace(old,new,1)
old=''' @Override protected void onResume(){super.onResume();applyImmersive();if(resumeAfterBackground&&player!=null&&prepared){resumeAfterBackground=false;player.play();}}'''
new=''' @Override protected void onResume(){super.onResume();if(NetworkGuard.isVpnOrCaptureActive(this)){try{if(player!=null)player.pause();}catch(Exception ignored){}Toast.makeText(this,"Desative a VPN ou capturador de rede para continuar.",Toast.LENGTH_LONG).show();finish();return;}applyImmersive();if(resumeAfterBackground&&player!=null&&prepared){resumeAfterBackground=false;player.play();}}'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

# Do the same for the YouTube/GreenShorts player.
p=Path("work/app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java")
s=p.read_text()
old='''    @Override public void onCreate(Bundle b){
        tvMode='''
new='''    @Override public void onCreate(Bundle b){
        super.onCreate(b);
        if(NetworkGuard.isVpnOrCaptureActive(this)){Toast.makeText(this,"Desative a VPN ou capturador de rede para continuar.",Toast.LENGTH_LONG).show();finish();return;}
        tvMode='''
assert old in s
s=s.replace(old,new,1)
old='''        super.onCreate(b);
        getWindow().setFlags'''
new='''        getWindow().setFlags'''
assert old in s
s=s.replace(old,new,1)
old='''    @Override protected void onResume(){super.onResume();applyImmersive();}'''
new='''    @Override protected void onResume(){super.onResume();if(NetworkGuard.isVpnOrCaptureActive(this)){Toast.makeText(this,"Desative a VPN ou capturador de rede para continuar.",Toast.LENGTH_LONG).show();finish();return;}applyImmersive();}'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)
