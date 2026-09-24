from pathlib import Path
import re, base64

root=Path('work')
main=root/'app/src/main/java/fun/greenplay/app/MainActivity.java'
s=main.read_text(encoding='utf-8')

def one(old,new,label=None):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label or old[:80]} count={n}')
    s=s.replace(old,new,1)

def method(start_marker,end_marker,new_text,label):
    global s
    a=s.find(start_marker)
    if a<0: raise SystemExit(label+' start missing')
    b=s.find(end_marker,a)
    if b<0: raise SystemExit(label+' end missing')
    s=s[:a]+new_text+s[b:]

# Brand palette + independent identity.
one('int GREEN=Color.rgb(32,224,112); final int BG=Color.rgb(7,17,12),CARD=Color.rgb(16,32,24);',
    'int GREEN=Color.rgb(255,79,154); final int BG=Color.rgb(12,8,11),CARD=Color.rgb(29,18,24);', 'colors')
one('String uid="",reseller="",appName="GreenPlay",logoUrl="",bgUrl="";',
    'String uid="",reseller="",appName="Yelly Doramas",logoUrl="",bgUrl="";', 'brand field')
one('String liveSearch="",activeHomeTab="Recomendações",homeCachedTab="",tvPendingCategoryHint="",footballSelectedDate="";',
    'String liveSearch="",activeHomeTab="Shorts",homeCachedTab="",tvPendingCategoryHint="",footballSelectedDate="";', 'home field')

# Yelly has no provider selection, football reminder or GreenPlay updater.
old_oncreate=re.search(r' public void onCreate\(Bundle b\)\{.*?\n',s).group(0)
new_oncreate=' public void onCreate(Bundle b){super.onCreate(b);SecurityGuard.hardenWebView();if(SecurityGuard.vpnActive(this)){vpnStartupBlocked=true;showVpnBlocked(true);return;}sp=getSharedPreferences("yelly",0);tvMode=DeviceCompat.isTelevisionDevice(this)||sp.getBoolean("force_tv_mode",false);requestedStartNav=getIntent()!=null?getIntent().getIntExtra("gp_restore_nav",-1):-1;openFootballFromNotification=false;configureWindowForCurrentMode();migrateLegacyOfflineDownloads();uid=sp.getString("uid","");reseller=sp.getString("reseller","");Api.PROVIDER="";loadIdentityCache();boolean modeChange=getIntent()!=null&&getIntent().getBooleanExtra("gp_mode_change",false);boolean hardModeReload=getIntent()!=null&&getIntent().getBooleanExtra("gp_hard_mode_reload",false);if(uid.isEmpty())login();else if(hardModeReload)startAfterHardModeReload();else if(modeChange)startAfterModeChange();else startExistingSession();refreshIdentity();}\n'
s=s.replace(old_oncreate,new_oncreate,1)
old_resume=re.search(r' @Override protected void onResume\(\)\{.*?\n',s).group(0)
new_resume=' @Override protected void onResume(){super.onResume();if(vpnStartupBlocked||SecurityGuard.vpnActive(this)){showVpnBlocked(vpnStartupBlocked);return;}startVpnWatch();if(tvMode&&!modeSwitchPending&&!tvImeActive)enterTvImmersiveUi();if(!wideTvUi())enforceGlobalBottomNav();updateGlobalCastButtonState();if(detailOpen&&activeSeriesResumeHost!=null&&activeSeriesDetail!=null)renderSeriesResume(activeSeriesSource,activeSeriesDetail,activeSeriesResumeHost);if(tvResumeAfterFullscreen){tvResumeAfterFullscreen=false;}if(playerRoundTrip)new Handler(Looper.getMainLooper()).postDelayed(()->restorePlayerReturnState(),60);}\n'
s=s.replace(old_resume,new_resume,1)

# Mode switches go straight back to Yelly catalog.
method(' void startAfterHardModeReload(){',' void startAfterModeChange(){', ''' void startAfterHardModeReload(){
  modeReloadScreen=true;showModeReloadScreenNow();
  new Handler(Looper.getMainLooper()).postDelayed(()->{if(isFinishing())return;modeReloadScreen=false;shell();refreshEntitlements(()->{});},260);
 }
''','hard mode')
method(' void startAfterModeChange(){',' void showModeReloadScreenNow(){', ''' void startAfterModeChange(){
  shell();refreshEntitlements(()->{});
 }
 
''','mode change')

# Identity is local to this app; panel can still manage account/plan content.
method(' void loadIdentityCache(){',' float tvUiScale(){', ''' void loadIdentityCache(){appName="Yelly Doramas";logoUrl="";bgUrl="";GREEN=Color.rgb(255,79,154);}
 void refreshIdentity(){appName="Yelly Doramas";logoUrl="";bgUrl="";refreshHomeHeaderBranding();}
 void applyAppLogo(ImageView im){if(im==null)return;try{im.setImageResource(R.drawable.yelly_logo);im.setAlpha(1f);}catch(Exception ignored){}}
''','identity')

# Login/registration no longer asks for IPTV server.
one('refreshEntitlements(()->providerSelectAfterLogin());','refreshEntitlements(()->shell());','login provider')
one('refreshEntitlements(()->prepareHomeThenShell(msg,go));','refreshEntitlements(()->shell());','register provider')
method(' void startExistingSession(){',' void startExistingSessionReady(){', ''' void startExistingSession(){
  syncDevice(null);refreshAccountContext(null);
  JSONObject access=readCachedAccessStatus();if(access!=null)applyEntitlements(access);
  shell();
  refreshEntitlements(()->{if(accessDenied(readCachedAccessStatus()))showAccessExpiredDialog(accessDeniedMessage(readCachedAccessStatus()));});
 }
''','existing session')

# Home is always Doramas/Minisséries.
one('boolean shouldDefaultToTvLanding(){return tvMode&&currentProviderHasLive();}','boolean shouldDefaultToTvLanding(){return false;}','default landing')
method(' void restoreHomeView(){',' void discardSectionPageState(){', ''' void restoreHomeView(){
  if(homeScrollCache!=null&&homeBodyCache!=null&&contentFrame!=null&&homeBodyCache.getChildCount()==0){attachPermanentHomeHost();homeViewAvailable=true;homeScrollY=0;homeTab("Shorts");return;}
  if(homeViewAvailable&&homeScrollCache!=null&&homeBodyCache!=null&&contentFrame!=null){activeHomeTab="Shorts";homeCachedTab="Shorts";attachPermanentHomeHost();setNav(0);if(wideTvUi())syncTvHeader("Shorts");final int y=homeScrollY;mainScroll.setVisibility(View.VISIBLE);mainScroll.post(()->{mainScroll.scrollTo(0,y);mainScroll.requestLayout();});return;}
  attachPermanentHomeHost();home();
 }
''','restore home')
one('sectionReturnTab=(returnTab==null||returnTab.trim().isEmpty())?"Recomendações":returnTab;', 'sectionReturnTab=(returnTab==null||returnTab.trim().isEmpty())?"Shorts":returnTab;', 'section return')
s=s.replace('activeHomeTab=(returnTab==null||returnTab.isEmpty())?"Recomendações":returnTab;', 'activeHomeTab=(returnTab==null||returnTab.isEmpty())?"Shorts":returnTab;')
s=s.replace('if("Recomendações".equals(activeHomeTab))restoreHomeView();else homeTab(activeHomeTab);', 'if("Shorts".equals(activeHomeTab))restoreHomeView();else homeTab(activeHomeTab);')
method(' void goHomeNow(){','  void clear(){', ''' void goHomeNow(){
  discardSectionPageState();releaseTvInlinePlayer();standardRootInsets();plansScreen=false;planFlowStage=0;providerSwitchScreen=false;searchScreenOpen=false;
  if(pixTimer!=null){try{pixTimer.cancel();}catch(Exception ignored){}pixTimer=null;}
  if(accessExpiredOverlay!=null)dismissAccessExpiredOverlay();if(detailOpen)closeDetails();if(navBar!=null)navBar.setVisibility(View.VISIBLE);
  if(contentFrame==null){shell();return;}homeScrollY=0;
  if(!"Shorts".equals(activeHomeTab))homeTab("Shorts");else{restoreHomeView();if(mainScroll!=null){mainScroll.scrollTo(0,0);mainScroll.post(()->{if(mainScroll==homeScrollCache)mainScroll.scrollTo(0,0);});}if(tvMode)keepTvHomeAnchored();}
 }
''','go home')
one(' void home(){homeTab("Recomendações");if(tvMode)keepTvHomeAnchored();}', ' void home(){homeTab("Shorts");if(tvMode)keepTvHomeAnchored();}', 'home')

# Shorts becomes the permanent Home host.
anchor=' void homeTab(String selected){\n  if(selected==null||selected.trim().isEmpty())selected="Recomendações";'
new=''' void homeTab(String selected){
  if(selected==null||selected.trim().isEmpty())selected="Shorts";
  if("Shorts".equals(selected)){
   activeHomeTab="Shorts";
   if(contentFrame!=null)attachPermanentHomeHost();
   clear();setNav(0);if(wideTvUi()&&body!=null)body.setPadding(dp(28),dp(12),dp(28),dp(18));homeViewAvailable=true;homeScrollY=0;homeCachedTab="Shorts";homeTop("Shorts");final int yellyGen=viewGen;if(tvMode)keepTvHomeAnchored();loadShortsCategorySections(yellyGen);return;
  }'''
one(anchor,new,'homeTab intro')

# Remove football prefetch from shell.
s=s.replace('  prefetchFootballToday();\n','')

# Mobile nav: Início, Favoritos, Downloads, Perfil only.
one('navHome=navItem("","Início",0);navFav=navItem("","Favoritos",1);if(currentProviderHasLive())navTv=navItem("","TV",2);else navTv=null;navDownloads=navItem("","Downloads",3);navProfile=navItem("","Perfil",4);ensureGlobalCastButton();',
    'navHome=navItem("","Início",0);navFav=navItem("","Favoritos",1);navTv=null;navDownloads=navItem("","Downloads",3);navProfile=navItem("","Perfil",4);ensureGlobalCastButton();', 'mobile nav')

# Compact TV header dedicated to Yelly.
method(' LinearLayout buildTvAppHeader(){',' Drawable tvHeaderNavBackground', ''' LinearLayout buildTvAppHeader(){
  LinearLayout bar=new LinearLayout(this);bar.setGravity(Gravity.CENTER_VERTICAL);bar.setPadding(dp(16),0,dp(16),0);bar.setBackgroundColor(0xff0c080b);if(android.os.Build.VERSION.SDK_INT>=21)bar.setElevation(dp(3));
  FrameLayout brand=new FrameLayout(this);brand.setFocusable(false);brand.setClickable(false);brand.setBackgroundColor(Color.TRANSPARENT);brand.setContentDescription("Yelly Doramas");ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);logo.setAdjustViewBounds(true);logo.setPadding(dp(8),dp(6),dp(8),dp(6));brand.addView(logo,new FrameLayout.LayoutParams(-1,-1));applyAppLogo(logo);bar.addView(brand,new LinearLayout.LayoutParams(dp(230),-1));
  LinearLayout menu=new LinearLayout(this);menu.setGravity(Gravity.CENTER);navShorts=tvHeroNavAction("Doramas",()->{if(detailOpen)closeDetails();homeTab("Shorts");});navHome=navShorts;uiTextSize(navShorts,17);menu.addView(navShorts,new LinearLayout.LayoutParams(dp(130),dp(60)));navFav=tvHeroNavAction("Favoritos",()->tvNavigate(1));uiTextSize(navFav,16);menu.addView(navFav,new LinearLayout.LayoutParams(dp(130),dp(60)));navDownloads=tvHeroNavAction("Downloads",()->tvNavigate(3));uiTextSize(navDownloads,16);menu.addView(navDownloads,new LinearLayout.LayoutParams(dp(130),dp(60)));bar.addView(menu,new LinearLayout.LayoutParams(0,-1,1));
  LinearLayout tools=new LinearLayout(this);tools.setGravity(Gravity.CENTER_VERTICAL|Gravity.RIGHT);TextView profileTop=tvUtilityAction("♙","Perfil",()->tvNavigate(4));navProfile=profileTop;tools.addView(profileTop,new LinearLayout.LayoutParams(dp(46),dp(46)));TextView clock=t("",14);clock.setGravity(Gravity.CENTER);clock.setTextColor(0xfff7d5e4);clock.setTypeface(null,1);tools.addView(clock,new LinearLayout.LayoutParams(dp(72),-1));Runnable tick=new Runnable(){public void run(){try{clock.setText(new java.text.SimpleDateFormat("HH:mm",java.util.Locale.getDefault()).format(new java.util.Date()));clock.postDelayed(this,30000);}catch(Exception ignored){}}};clock.post(tick);bar.addView(tools,new LinearLayout.LayoutParams(dp(230),-1));
  linkTvHorizontal(navShorts,navFav);linkTvHorizontal(navFav,navDownloads);linkTvHorizontal(navDownloads,profileTop);return bar;
 }
''','tv header')
method(' void syncTvHeader(String selected){',' void cancelProviderSwitch(){', ''' void syncTvHeader(String selected){
  if(!wideTvUi())return;TextView[] all={navShorts,navFav,navDownloads,navProfile};TextView active=null;if(currentNavIndex==1)active=navFav;else if(currentNavIndex==3)active=navDownloads;else if(currentNavIndex==4)active=navProfile;else active=navShorts;for(TextView v:all)if(v!=null)styleTvHeaderItem(v,v==active,v.hasFocus());
 }
''','sync tv header')
method('boolean isTvHeaderActive(TextView v){','void runTvHeaderAction', '''boolean isTvHeaderActive(TextView v){
 if(v==null)return false;if(currentNavIndex==1)return v==navFav;if(currentNavIndex==3)return v==navDownloads;if(currentNavIndex==4)return v==navProfile;return v==navShorts||v==navHome;
}
''','tv active')

# Mobile home header: accepted compact logo + search; no TV/football/film tabs.
method(' void homeTop(String selected){',' boolean validTopSection', ''' void homeTop(String selected){
  if(wideTvUi()){syncTvHeader(selected);return;}
  LinearLayout topWrap=new LinearLayout(this);topWrap.setOrientation(LinearLayout.VERTICAL);topWrap.setPadding(0,dp(20),0,dp(8));LinearLayout top=new LinearLayout(this);top.setGravity(Gravity.CENTER_VERTICAL);
  FrameLayout brandSlot=new FrameLayout(this);homeHeaderLogo=new ImageView(this);homeHeaderLogo.setScaleType(ImageView.ScaleType.FIT_CENTER);homeHeaderLogo.setAdjustViewBounds(true);brandSlot.addView(homeHeaderLogo,new FrameLayout.LayoutParams(-1,-1));homeHeaderBrandFallback=t("Yelly Doramas",14);homeHeaderBrandFallback.setVisibility(View.GONE);brandSlot.addView(homeHeaderBrandFallback,new FrameLayout.LayoutParams(-1,-1));LinearLayout.LayoutParams brandLp=new LinearLayout.LayoutParams(dp(128),dp(40));brandLp.setMargins(0,0,dp(10),0);top.addView(brandSlot,brandLp);refreshHomeHeaderBranding();
  LinearLayout searchBox=new LinearLayout(this);searchBox.setGravity(Gravity.CENTER_VERTICAL);searchBox.setPadding(dp(13),0,dp(5),0);GradientDrawable sBg=round(0xff23171d,21);sBg.setStroke(dp(1),0xff5a3445);searchBox.setBackground(sBg);TextView hint=t("Buscar doramas",14);hint.setTextColor(0xffc9aeb9);hint.setGravity(Gravity.CENTER_VERTICAL);hint.setSingleLine(true);hint.setPadding(0,0,0,0);searchBox.addView(hint,new LinearLayout.LayoutParams(0,dp(38),1));TextView si=t("⌕",22);si.setTextColor(Color.WHITE);si.setGravity(Gravity.CENTER);si.setPadding(0,0,0,0);searchBox.addView(si,new LinearLayout.LayoutParams(dp(34),dp(38)));searchBox.setOnClickListener(v->searchDialog());top.addView(searchBox,new LinearLayout.LayoutParams(0,dp(38),1));View cast=headerCastButton();LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(dp(44),dp(40));clp.setMargins(dp(8),0,0,0);top.addView(cast,clp);topWrap.addView(top,new LinearLayout.LayoutParams(-1,dp(42)));
  TextView label=t("Doramas & Minisséries",16);label.setTypeface(null,1);label.setTextColor(0xffffb3d2);label.setPadding(dp(2),dp(8),0,dp(4));topWrap.addView(label,new LinearLayout.LayoutParams(-1,dp(38)));body.addView(topWrap,new LinearLayout.LayoutParams(-1,-2));
 }
''','home top')

# Branding labels / visible copy.
s=s.replace('"GreenShorts"','"Yelly Doramas"')
s=s.replace('GreenPlay não está respondendo','Yelly não está respondendo')
s=s.replace('Abrindo GreenPlay','Abrindo Yelly')
s=s.replace('PREPARANDO GREENPLAY','PREPARANDO YELLY')
s=s.replace('Sincronizando canais, filmes, séries e imagens','Sincronizando doramas, minisséries e imagens')
s=s.replace('Validando acesso e sincronizando o catálogo completo…','Validando acesso e sincronizando o catálogo Yelly…')
s=s.replace('"GreenPlay"', '"Yelly"')
s=s.replace('appName="Yelly"', 'appName="Yelly Doramas"')

# Favorites copy is dorama-only.
s=s.replace('"Filmes, séries e canais que você guardou"','"Doramas e minisséries que você guardou"')
s=s.replace('"Toque no coração de qualquer filme, série ou canal e ele fica guardado aqui para você encontrar rápido."','"Toque no coração de qualquer dorama e ele fica guardado aqui para você encontrar rápido."')

# Stable favorites key for YouTube content.
method(' void toggleFav(JSONObject x){',' void favorites(){', ''' void toggleFav(JSONObject x){try{JSONArray a=new JSONArray(sp.getString("favs","[]"));String key=itemKey(x);String yt=x==null?"":x.optString("youtube_id","");if(!yt.isEmpty())key="yt|"+yt;for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o==null)continue;String ok=itemKey(o);String oy=o.optString("youtube_id","");if(!oy.isEmpty())ok="yt|"+oy;if(key.equals(ok)){a.remove(i);sp.edit().putString("favs",a.toString()).apply();Toast.makeText(this,"Removido dos favoritos",Toast.LENGTH_SHORT).show();return;}}a.put(x);sp.edit().putString("favs",a.toString()).apply();Toast.makeText(this,"Adicionado aos favoritos",Toast.LENGTH_SHORT).show();}catch(Exception ignored){}}
''','favorites key')

# Profile: remove server-specific UI and language.
s=s.replace('"Vendedor: "+sp.getString("reseller_name",reseller.isEmpty()?"Yelly":reseller)', '"Yelly Doramas"')
s=s.replace('TextView serverValue=profileInfoLine(infoCard,"◉","Servidor",sp.getString("provider_name","Yelly"),0xfff1f1f1);','TextView serverValue=profileInfoLine(infoCard,"◉","Catálogo","Yelly Doramas",0xfff1f1f1);')
s=s.replace('  profileOptionRow(account,R.drawable.ic_server,"Trocar de servidor","Escolha outra fonte de conteúdo",v->chooseProvider(),false);\n','')

# App-specific mode switch loading text.
s=s.replace('showProviderBootstrap(sp.getString("provider_name","Yelly"));','shell();')

main.write_text(s,encoding='utf-8')

# API + URLs.
secret=root/'app/src/main/java/fun/greenplay/app/SecretStrings.java'
t=secret.read_text(encoding='utf-8')
t=re.sub(r'static String apiBase\(\)\{.*?\}', 'static String apiBase(){return "https://yellyplay.online/api/dtlive/";}', t, count=1)
secret.write_text(t,encoding='utf-8')
for rel in ['app/src/main/java/fun/greenplay/app/Img.java','app/src/main/java/fun/greenplay/app/OfflineDownloadService.java','app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java']:
    p=root/rel
    z=p.read_text(encoding='utf-8').replace('https://greenplay.fun','https://yellyplay.online').replace('GreenPlay','Yelly')
    p.write_text(z,encoding='utf-8')

# Network security.
net=root/'app/src/main/res/xml/network_security_config.xml'
net.write_text(net.read_text(encoding='utf-8').replace('greenplay.fun','yellyplay.online'),encoding='utf-8')

# Android app identity.
grad=root/'app/build.gradle'
g=grad.read_text(encoding='utf-8')
g=g.replace("applicationId 'fun.greenplay.app'", "applicationId 'online.yellyplay.doramas'")
g=g.replace('versionCode 52897','versionCode 10000').replace("versionName '5.28.97'", "versionName '1.0.0'")
g=g.replace("            applicationIdSuffix '.debug'\n",'')
grad.write_text(g,encoding='utf-8')

manifest=root/'app/src/main/AndroidManifest.xml'
m=manifest.read_text(encoding='utf-8')
m=m.replace('<uses-permission android:name="android.permission.INTERNET"/><uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>','<uses-permission android:name="android.permission.INTERNET"/>')
m=m.replace('android:label="GreenPlay" android:icon="@drawable/greenplay_app_icon" android:roundIcon="@drawable/greenplay_app_icon"','android:label="Yelly Doramas" android:icon="@drawable/yelly_app_icon" android:roundIcon="@drawable/yelly_app_icon"')
m=m.replace('android:banner="@drawable/tv_banner"','android:banner="@drawable/yelly_logo"')
m=m.replace('  <receiver android:name=".FootballReminderReceiver" android:exported="false"/>\n','')
manifest.write_text(m,encoding='utf-8')

# Decode exact approved compact header asset.
draw=root/'app/src/main/res/drawable-nodpi'
draw.mkdir(parents=True,exist_ok=True)
logo_b64=''.join(Path(f'inspection/yelly_logo_tiny_{i:02d}.b64').read_text().strip() for i in range(5))
(draw/'yelly_logo.webp').write_bytes(base64.b64decode(logo_b64))

# Simple Yelly launcher icon for first build; header logo is the approved logo.
icon=root/'app/src/main/res/drawable/yelly_app_icon.xml'
icon.write_text('''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
  <path android:fillColor="#160B12" android:pathData="M12,4 L96,4 A8,8 0,0 1,104 12 L104,96 A8,8 0,0 1,96 104 L12,104 A8,8 0,0 1,4 96 L4,12 A8,8 0,0 1,12 4 Z"/>
  <path android:fillColor="#FF4F9A" android:pathData="M31,24 L31,84 L76,54 Z"/>
  <path android:fillColor="#FFB3D2" android:pathData="M70,35 C62,35 58,42 56,46 C54,42 50,35 42,35 C33,35 28,43 28,51 C28,65 43,75 56,84 C69,75 84,65 84,51 C84,43 79,35 70,35 Z"/>
</vector>''',encoding='utf-8')

(root/'app/RELEASE_NOTES.txt').write_text('Yelly Doramas 1.0.0\nAplicativo independente focado em Doramas e Minisséries.\nConectado ao painel yellyplay.online.\nInterface própria para celular, Android TV, TV Box e Fire TV Stick.\n',encoding='utf-8')

print('YELLY_PATCH_OK')