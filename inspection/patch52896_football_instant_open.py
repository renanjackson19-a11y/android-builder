from pathlib import Path

main = Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s = main.read_text(encoding="utf-8")

old = """ void startExistingSession(){
  syncDevice(null);refreshAccountContext(null);"""
new = """ void startExistingSession(){
  prefetchFootballToday();
  syncDevice(null);refreshAccountContext(null);"""
if old not in s:
    raise SystemExit("startExistingSession anchor not found")
s = s.replace(old, new, 1)

old = """  sp.edit().putString("provider_id",id).putString("provider_name",name).putInt("provider_movies_count",movieCount).putInt("provider_series_count",seriesCount).putInt("provider_live_count",liveCount).putBoolean("provider_has_live",sessionHasLive).apply();
  // v16.47:"""
new = """  sp.edit().putString("provider_id",id).putString("provider_name",name).putInt("provider_movies_count",movieCount).putInt("provider_series_count",seriesCount).putInt("provider_live_count",liveCount).putBoolean("provider_has_live",sessionHasLive).apply();
  prefetchFootballToday();
  // v16.47:"""
if old not in s:
    raise SystemExit("provider anchor not found")
s = s.replace(old, new, 1)

old = """   public void ok(JSONObject j){
    footballPrefetchBusy=false;
    JSONArray a=j.optJSONArray("result");
    if(j.optInt("status",200)==200&&a!=null&&a.length()>0)saveFootballCache(date,a);
   }"""
new = """   public void ok(JSONObject j){
    footballPrefetchBusy=false;
    JSONArray a=j.optJSONArray("result");
    if(j.optInt("status",200)==200&&a!=null&&a.length()>0){
     saveFootballCache(date,a);
     if(date.equals(footballSelectedDate)&&body!=null){
      View v=body.findViewWithTag("football_rows");
      if(v instanceof LinearLayout)renderFootballRows(a);
     }
    }
   }"""
if old not in s:
    raise SystemExit("prefetch callback anchor not found")
s = s.replace(old, new, 1)

old = """  final JSONArray cached=footballCachedRows(date,10L*60L*1000L);
  final boolean hadCached=cached!=null&&cached.length()>0;
  if(hadCached)renderFootballRows(cached);else renderFootballLoading();

  if(hadCached&&footballCacheAge(date)<45000L)return;

  Api.post("football",Api.m("date",date),new Api.CB(){"""
new = """  final JSONArray cached=footballCachedRows(date,24L*60L*60L*1000L);
  final boolean hadCached=cached!=null&&cached.length()>0;
  if(hadCached)renderFootballRows(cached);else renderFootballLoading();

  if(hadCached&&footballCacheAge(date)<45000L)return;
  String today=footballDayKey(java.util.Calendar.getInstance());
  if(footballPrefetchBusy&&date.equals(today))return;

  Api.post("football",Api.m("date",date),new Api.CB(){"""
if old not in s:
    raise SystemExit("load cache anchor not found")
s = s.replace(old, new, 1)

# Keep the shell fallback but start it immediately rather than after 350 ms.
s = s.replace(
    'new Handler(Looper.getMainLooper()).postDelayed(()->{if(!isFinishing())prefetchFootballToday();},350);',
    'prefetchFootballToday();',
    1,
)

main.write_text(s, encoding="utf-8")

gradle = Path("work/app/build.gradle")
g = gradle.read_text(encoding="utf-8")
g = g.replace("versionCode 52895", "versionCode 52896")
g = g.replace("versionName '5.28.95'", "versionName '5.28.96'")
gradle.write_text(g, encoding="utf-8")

notes = Path("work/app/RELEASE_NOTES.txt")
old_notes = notes.read_text(encoding="utf-8") if notes.exists() else ""
notes.write_text(
    "Futebol abre mais rápido: pré-carregamento iniciado antes da Home.\n"
    "Cache do dia aparece imediatamente e atualiza em segundo plano.\n"
    "Evita consulta duplicada quando a agenda já está sendo pré-carregada.\n" + old_notes,
    encoding="utf-8",
)
