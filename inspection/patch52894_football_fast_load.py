from pathlib import Path

main = Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s = main.read_text(encoding="utf-8")

old = 'String liveSearch="",activeHomeTab="Recomendações",homeCachedTab="",tvPendingCategoryHint="";'
new = 'String liveSearch="",activeHomeTab="Recomendações",homeCachedTab="",tvPendingCategoryHint="",footballSelectedDate=""; boolean footballPrefetchBusy=false;'
if old not in s:
    raise SystemExit("field anchor not found")
s = s.replace(old, new, 1)

old = """  int firstNav=requestedStartNav;requestedStartNav=-1;
  if(firstNav>=0){openInitialNav(firstNav);}"""
new = """  new Handler(Looper.getMainLooper()).postDelayed(()->{if(!isFinishing())prefetchFootballToday();},350);
  int firstNav=requestedStartNav;requestedStartNav=-1;
  if(firstNav>=0){openInitialNav(firstNav);}"""
if old not in s:
    raise SystemExit("shell anchor not found")
s = s.replace(old, new, 1)

old = """ void renderFootballEmptyState(){View v=body==null?null:body.findViewWithTag("football_rows");if(!(v instanceof LinearLayout))return;LinearLayout host=(LinearLayout)v;host.removeAllViews();TextView ball=t("⚽",30);ball.setGravity(Gravity.CENTER);host.addView(ball,new LinearLayout.LayoutParams(-1,dp(48)));TextView msg=t("Nenhum jogo encontrado para esta data",15);msg.setTypeface(null,1);msg.setGravity(Gravity.CENTER);msg.setTextColor(0xffd9e0dc);host.addView(msg,new LinearLayout.LayoutParams(-1,dp(42)));}
 void loadFootballDate(String date){renderFootballLoading();Api.post("football",Api.m("date",date),new Api.CB(){public void ok(JSONObject j){if(body==null)return;JSONArray a=j.optJSONArray("result");if(j.optInt("status",200)!=200||a==null||a.length()==0){renderFootballEmptyState();return;}renderFootballRows(a);}public void err(String e){View v=body==null?null:body.findViewWithTag("football_rows");if(!(v instanceof LinearLayout))return;LinearLayout host=(LinearLayout)v;host.removeAllViews();TextView msg=t("Não foi possível carregar os jogos agora.",15);msg.setGravity(Gravity.CENTER);msg.setTextColor(0xffffb4ab);host.addView(msg,new LinearLayout.LayoutParams(-1,dp(54)));TextView sub=t("Tente novamente em alguns instantes.",12);sub.setGravity(Gravity.CENTER);sub.setTextColor(0xff8f9c95);host.addView(sub,new LinearLayout.LayoutParams(-1,dp(34)));}});}"""

new = """ void renderFootballEmptyState(){View v=body==null?null:body.findViewWithTag("football_rows");if(!(v instanceof LinearLayout))return;LinearLayout host=(LinearLayout)v;host.removeAllViews();TextView ball=t("⚽",30);ball.setGravity(Gravity.CENTER);host.addView(ball,new LinearLayout.LayoutParams(-1,dp(48)));TextView msg=t("Nenhum jogo encontrado para esta data",15);msg.setTypeface(null,1);msg.setGravity(Gravity.CENTER);msg.setTextColor(0xffd9e0dc);host.addView(msg,new LinearLayout.LayoutParams(-1,dp(42)));}
 String footballCacheKey(String date){
  String p=Api.PROVIDER==null?"":Api.PROVIDER.trim();
  p=p.replaceAll("[^a-zA-Z0-9_-]","_");
  return "football_rows_"+p+"_"+date;
 }
 long footballCacheAge(String date){
  if(sp==null)return Long.MAX_VALUE;
  long ts=sp.getLong(footballCacheKey(date)+"_ts",0L);
  if(ts<=0)return Long.MAX_VALUE;
  return Math.max(0L,System.currentTimeMillis()-ts);
 }
 JSONArray footballCachedRows(String date,long maxAgeMs){
  try{
   if(sp==null||footballCacheAge(date)>maxAgeMs)return null;
   String raw=sp.getString(footballCacheKey(date),"");
   if(raw==null||raw.trim().isEmpty())return null;
   JSONArray a=new JSONArray(raw);
   return a.length()>0?a:null;
  }catch(Exception ignored){return null;}
 }
 void saveFootballCache(String date,JSONArray rows){
  if(sp==null||rows==null||rows.length()==0)return;
  try{
   sp.edit().putString(footballCacheKey(date),rows.toString())
    .putLong(footballCacheKey(date)+"_ts",System.currentTimeMillis()).apply();
  }catch(Exception ignored){}
 }
 void prefetchFootballToday(){
  if(footballPrefetchBusy||sp==null)return;
  String date=footballDayKey(java.util.Calendar.getInstance());
  if(footballCacheAge(date)<45000L)return;
  footballPrefetchBusy=true;
  Api.post("football",Api.m("date",date),new Api.CB(){
   public void ok(JSONObject j){
    footballPrefetchBusy=false;
    JSONArray a=j.optJSONArray("result");
    if(j.optInt("status",200)==200&&a!=null&&a.length()>0)saveFootballCache(date,a);
   }
   public void err(String e){footballPrefetchBusy=false;}
  });
 }
 void loadFootballDate(String date){
  footballSelectedDate=date;
  final JSONArray cached=footballCachedRows(date,10L*60L*1000L);
  final boolean hadCached=cached!=null&&cached.length()>0;
  if(hadCached)renderFootballRows(cached);else renderFootballLoading();

  if(hadCached&&footballCacheAge(date)<45000L)return;

  Api.post("football",Api.m("date",date),new Api.CB(){
   public void ok(JSONObject j){
    JSONArray a=j.optJSONArray("result");
    boolean good=j.optInt("status",200)==200&&a!=null&&a.length()>0;
    if(good)saveFootballCache(date,a);
    if(body==null||!date.equals(footballSelectedDate))return;
    if(!good){if(!hadCached)renderFootballEmptyState();return;}
    renderFootballRows(a);
   }
   public void err(String e){
    if(body==null||!date.equals(footballSelectedDate)||hadCached)return;
    View v=body.findViewWithTag("football_rows");
    if(!(v instanceof LinearLayout))return;
    LinearLayout host=(LinearLayout)v;
    host.removeAllViews();
    TextView msg=t("Não foi possível carregar os jogos agora.",15);
    msg.setGravity(Gravity.CENTER);
    msg.setTextColor(0xffffb4ab);
    host.addView(msg,new LinearLayout.LayoutParams(-1,dp(54)));
    TextView sub=t("Tente novamente em alguns instantes.",12);
    sub.setGravity(Gravity.CENTER);
    sub.setTextColor(0xff8f9c95);
    host.addView(sub,new LinearLayout.LayoutParams(-1,dp(34)));
   }
  });
 }"""

if old not in s:
    raise SystemExit("football load anchor not found")
s = s.replace(old, new, 1)
main.write_text(s, encoding="utf-8")

gradle = Path("work/app/build.gradle")
g = gradle.read_text(encoding="utf-8")
g = g.replace("versionCode 52893", "versionCode 52894")
g = g.replace("versionName '5.28.93'", "versionName '5.28.94'")
gradle.write_text(g, encoding="utf-8")
