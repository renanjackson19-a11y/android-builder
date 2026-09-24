from pathlib import Path
import shutil

src = Path("work")
main = src / "app/src/main/java/fun/greenplay/app/MainActivity.java"
s = main.read_text(encoding="utf-8")

s = s.replace(
    "static final int REQ_PROFILE_PHOTO=8601;",
    "static final int REQ_PROFILE_PHOTO=8601,REQ_FOOTBALL_NOTIFICATIONS=8602;",
    1,
)

s = s.replace(
    "boolean footballPrefetchBusy=false;",
    "boolean footballPrefetchBusy=false,openFootballFromNotification=false;",
    1,
)

s = s.replace(
    'requestedStartNav=getIntent()!=null?getIntent().getIntExtra("gp_restore_nav",-1):-1;',
    'requestedStartNav=getIntent()!=null?getIntent().getIntExtra("gp_restore_nav",-1):-1;openFootballFromNotification=getIntent()!=null&&getIntent().getBooleanExtra("gp_open_football",false);',
    1,
)

s = s.replace(
    'sp=getSharedPreferences("gp",0);tvMode=',
    'sp=getSharedPreferences("gp",0);FootballReminderManager.rescheduleAll(this);tvMode=',
    1,
)

pause_anchor = " @Override protected void onPause(){"
on_new = ' @Override protected void onNewIntent(Intent i){super.onNewIntent(i);setIntent(i);if(i!=null&&i.getBooleanExtra("gp_open_football",false)){openFootballFromNotification=true;if(uid!=null&&!uid.isEmpty()&&body!=null){openFootballFromNotification=false;openTvFootball();}}}\n'
if pause_anchor not in s:
    raise SystemExit("onPause anchor not found")
s = s.replace(pause_anchor, on_new + pause_anchor, 1)

old_shell = """  int firstNav=requestedStartNav;requestedStartNav=-1;
  if(firstNav>=0){openInitialNav(firstNav);}"""
new_shell = """  int firstNav=requestedStartNav;requestedStartNav=-1;
  if(openFootballFromNotification){openFootballFromNotification=false;openTvFootball();}
  else if(firstNav>=0){openInitialNav(firstNav);}"""
if old_shell not in s:
    raise SystemExit("shell anchor not found")
s = s.replace(old_shell, new_shell, 1)

row_anchor = " View footballGameRow(JSONObject x){"
helpers = """ void requestFootballReminderPermission(){
  if(Build.VERSION.SDK_INT>=33&&checkSelfPermission("android.permission.POST_NOTIFICATIONS")!=android.content.pm.PackageManager.PERMISSION_GRANTED){
   try{requestPermissions(new String[]{"android.permission.POST_NOTIFICATIONS"},REQ_FOOTBALL_NOTIFICATIONS);}catch(Exception ignored){}
  }
 }
 void styleFootballReminderButton(TextView v,boolean active){
  if(v==null)return;
  v.setText(active?"🔔  Lembrete ativado":"🔔  Lembrar-me");
  v.setTextColor(active?0xff8dffb4:0xffd2ddd7);
  v.setTypeface(null,1);v.setGravity(Gravity.CENTER);
  GradientDrawable b=round(active?0xff0d2b1d:0xff151f1a,12);
  b.setStroke(dp(1),active?GREEN:0xff355246);v.setBackground(b);
 }
"""
if row_anchor not in s:
    raise SystemExit("row anchor not found")
s = s.replace(row_anchor, helpers + row_anchor, 1)

watch_anchor = '  if(live&&x.optBoolean("watch_available",false)){'
reminder_ui = """  long reminderTs=x.optLong("timestamp",0);
  boolean reminderEligible=!live&&reminderTs>System.currentTimeMillis()/1000L-60L;
  if(reminderEligible){
   final TextView remind=t("",12);
   boolean activeReminder=FootballReminderManager.isActive(this,x);
   styleFootballReminderButton(remind,activeReminder);
   remind.setFocusable(tvMode);
   remind.setContentDescription(activeReminder?"Lembrete ativado":"Lembrar quando o jogo começar");
   remind.setOnClickListener(v->{
    boolean now=FootballReminderManager.toggle(MainActivity.this,x);
    styleFootballReminderButton(remind,now);
    remind.setContentDescription(now?"Lembrete ativado":"Lembrar quando o jogo começar");
    if(now){
     requestFootballReminderPermission();
     Toast.makeText(MainActivity.this,"Lembrete ativado. Vou avisar quando o jogo começar.",Toast.LENGTH_SHORT).show();
    }else Toast.makeText(MainActivity.this,"Lembrete removido.",Toast.LENGTH_SHORT).show();
   });
   if(tvMode)armTvFocus(remind);
   LinearLayout.LayoutParams rlp=new LinearLayout.LayoutParams(-1,dp(38));
   rlp.setMargins(0,dp(6),0,0);
   wrap.addView(remind,rlp);
  }

  if(live&&x.optBoolean("watch_available",false)){"""
if watch_anchor not in s:
    raise SystemExit("watch anchor not found")
s = s.replace(watch_anchor, reminder_ui, 1)
main.write_text(s, encoding="utf-8")

manifest = src / "app/src/main/AndroidManifest.xml"
m = manifest.read_text(encoding="utf-8")
m = m.replace(
    '<uses-permission android:name="android.permission.INTERNET"/>',
    '<uses-permission android:name="android.permission.INTERNET"/><uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>',
    1,
)
m = m.replace(
    '<service android:name=".OfflineDownloadService" android:exported="false" android:foregroundServiceType="dataSync"/>',
    '<service android:name=".OfflineDownloadService" android:exported="false" android:foregroundServiceType="dataSync"/>\n  <receiver android:name=".FootballReminderReceiver" android:exported="false"/>',
    1,
)
manifest.write_text(m, encoding="utf-8")

java_dir = src / "app/src/main/java/fun/greenplay/app"
shutil.copy2("inspection/52895/FootballReminderManager.java", java_dir / "FootballReminderManager.java")
shutil.copy2("inspection/52895/FootballReminderReceiver.java", java_dir / "FootballReminderReceiver.java")

gradle = src / "app/build.gradle"
g = gradle.read_text(encoding="utf-8")
g = g.replace("versionCode 52894", "versionCode 52895")
g = g.replace("versionName '5.28.94'", "versionName '5.28.95'")
gradle.write_text(g, encoding="utf-8")

notes = src / "app/RELEASE_NOTES.txt"
old = notes.read_text(encoding="utf-8") if notes.exists() else ""
notes.write_text(
    "Lembrete de jogos com notificação quando a partida entrar ao vivo.\n"
    "Botão Lembrar-me nos jogos agendados.\n"
    "Ao tocar na notificação, abre a área de Futebol.\n" + old,
    encoding="utf-8",
)
