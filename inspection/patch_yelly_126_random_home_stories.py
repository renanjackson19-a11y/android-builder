from pathlib import Path

root=Path("work")
app=root/"app/src/main/java/fun/greenplay/app"

# 1) Full player: keep the user's requested extra black area below the AI/header region.
p=app/"YouTubePlayerActivity.java"
s=p.read_text(encoding="utf-8")
old='int topMaskH=Math.max(dp(48),Math.min(dp(82),(int)(screenH*0.09f)));'
new='int topMaskH=Math.max(dp(64),Math.min(dp(118),(int)(screenH*0.125f)));'
if old not in s: raise SystemExit("full player top mask anchor missing")
s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")

# 2) Home/catalog: randomize the first visible catalog items every time the Home is rebuilt.
p=app/"MainActivity.java"
m=p.read_text(encoding="utf-8")

anchor=''' void loadShortsCategorySections(final int gen){'''
helper=''' JSONArray randomCatalogStart(JSONArray src){
  JSONArray out=new JSONArray();if(src==null||src.length()==0)return out;
  java.util.ArrayList<JSONObject> pool=new java.util.ArrayList<>();
  for(int i=0;i<src.length();i++){JSONObject x=src.optJSONObject(i);if(x!=null)pool.add(x);}
  java.util.Collections.shuffle(pool,new java.util.Random(System.nanoTime()^((long)(++featuredShuffleTick)*2654435761L)));
  for(JSONObject x:pool)out.put(x);
  return out;
 }
'''+anchor
if anchor not in m: raise SystemExit("loadShortsCategorySections anchor missing")
m=m.replace(anchor,helper,1)

old='''  JSONArray seed=readGreenShortsSeedCache();
  if(wideTvUi()){
   final java.util.HashSet<String> seen=new java.util.HashSet<>();
   for(int i=0;i<seed.length();i++){JSONObject x=seed.optJSONObject(i);if(x==null)continue;String y=x.optString("youtube_id","").trim();String k=!y.isEmpty()?"yt|"+y:itemKey(x);if(k!=null&&!k.trim().isEmpty())seen.add(k);}
   if(seed.length()>0)grid(seed);'''
new='''  JSONArray seed=readGreenShortsSeedCache();
  JSONArray startRows=randomCatalogStart(seed);
  if(wideTvUi()){
   final java.util.HashSet<String> seen=new java.util.HashSet<>();
   for(int i=0;i<seed.length();i++){JSONObject x=seed.optJSONObject(i);if(x==null)continue;String y=x.optString("youtube_id","").trim();String k=!y.isEmpty()?"yt|"+y:itemKey(x);if(k!=null&&!k.trim().isEmpty())seen.add(k);}
   if(startRows.length()>0)grid(startRows);'''
if old not in m: raise SystemExit("seed tv block missing")
m=m.replace(old,new,1)

old='''  if(seed.length()>0){prefetchGreenShortDetails(seed,24);featureCarousel(seed);grid(seed);startGreenShortsPaging(seed,gen);loadExternalDoramasHome(gen);return;}'''
new='''  if(seed.length()>0){prefetchGreenShortDetails(seed,24);featureCarousel(startRows);grid(startRows);startGreenShortsPaging(startRows,gen);loadExternalDoramasHome(gen);return;}'''
if old not in m: raise SystemExit("seed mobile block missing")
m=m.replace(old,new,1)

old='''JSONArray rows=j.optJSONArray("result");if(rows==null)rows=new JSONArray();if(rows.length()>0){saveGreenShortsSeedCache(rows);prefetchGreenShortDetails(rows,24);featureCarousel(rows);}grid(rows);startGreenShortsPaging(rows,gen);loadExternalDoramasHome(gen);'''
new='''JSONArray rows=j.optJSONArray("result");if(rows==null)rows=new JSONArray();JSONArray startRows=randomCatalogStart(rows);if(rows.length()>0){saveGreenShortsSeedCache(rows);prefetchGreenShortDetails(rows,24);featureCarousel(startRows);}grid(startRows);startGreenShortsPaging(startRows,gen);loadExternalDoramasHome(gen);'''
if old not in m: raise SystemExit("network initial block missing")
m=m.replace(old,new,1)
p.write_text(m,encoding="utf-8")

# 3) Stories: follow the same GreenPlay player framing concept.
p=app/"StoriesActivity.java"
st=p.read_text(encoding="utf-8")

old='''  web=new WebView(this);web.setBackgroundColor(Color.TRANSPARENT);SecurityGuard.hardenWebView();WebSettings ws=web.getSettings();ws.setJavaScriptEnabled(true);ws.setDomStorageEnabled(true);ws.setMediaPlaybackRequiresUserGesture(false);ws.setAllowFileAccess(false);ws.setAllowContentAccess(false);if(Build.VERSION.SDK_INT>=21)ws.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);web.setWebChromeClient(new WebChromeClient());web.setWebViewClient(new WebViewClient());'''
new='''  web=new WebView(this);web.setBackgroundColor(Color.BLACK);SecurityGuard.hardenWebView();WebSettings ws=web.getSettings();ws.setJavaScriptEnabled(true);ws.setDomStorageEnabled(true);ws.setMediaPlaybackRequiresUserGesture(false);ws.setAllowFileAccess(false);ws.setAllowContentAccess(false);ws.setSaveFormData(false);if(Build.VERSION.SDK_INT>=21)ws.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);web.setWebChromeClient(new WebChromeClient());web.setWebViewClient(new WebViewClient());web.setLongClickable(false);web.setHapticFeedbackEnabled(false);web.setOnLongClickListener(v->true);web.setOnTouchListener((v,e)->true);'''
if old not in st: raise SystemExit("stories web setup missing")
st=st.replace(old,new,1)

old='''FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1);if(!tvMode)wp.setMargins(0,dp(64),0,dp(112));root.addView(web,wp);
  ytTopMask=new View(this);ytTopMask.setBackgroundColor(0xee14080f);FrameLayout.LayoutParams ytp=new FrameLayout.LayoutParams(-1,dp(76),Gravity.TOP);ytp.setMargins(0,dp(64),0,0);root.addView(ytTopMask,ytp);
  ytBottomMask=new View(this);ytBottomMask.setBackgroundColor(0xee14080f);FrameLayout.LayoutParams ybp=new FrameLayout.LayoutParams(-1,dp(64),Gravity.BOTTOM);ybp.setMargins(0,0,0,dp(112));root.addView(ytBottomMask,ybp);'''
new='''FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1);if(!tvMode)wp.setMargins(0,dp(64),0,dp(112));root.addView(web,wp);
  int storyScreenH=getResources().getDisplayMetrics().heightPixels;
  int storyTopMaskH=Math.max(dp(64),Math.min(dp(118),(int)(storyScreenH*0.125f)));
  int storyBottomMaskH=Math.max(dp(64),Math.min(dp(110),(int)(storyScreenH*0.11f)));
  ytTopMask=new View(this);ytTopMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ytp=new FrameLayout.LayoutParams(-1,storyTopMaskH,Gravity.TOP);ytp.setMargins(0,dp(64),0,0);root.addView(ytTopMask,ytp);
  ytBottomMask=new View(this);ytBottomMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ybp=new FrameLayout.LayoutParams(-1,storyBottomMaskH,Gravity.BOTTOM);ybp.setMargins(0,0,0,dp(112));root.addView(ytBottomMask,ybp);'''
if old not in st: raise SystemExit("stories masks missing")
st=st.replace(old,new,1)

# Use the same base/origin used by the working GreenPlay player.
st=st.replace("origin:'https://yellyplay.online'","origin:'https://greenplay.fun'")
st=st.replace('web.loadDataWithBaseURL("https://yellyplay.online/",html,"text/html","UTF-8",null);',
              'web.loadDataWithBaseURL("https://greenplay.fun/",html,"text/html","UTF-8",null);')

p.write_text(st,encoding="utf-8")

# Version
g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10024" not in t or "versionName '1.0.24'" not in t: raise SystemExit("wrong 1.0.24 base")
t=t.replace("versionCode 10024","versionCode 10026",1).replace("versionName '1.0.24'","versionName '1.0.26'",1)
g.write_text(t,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.26
- Faixa preta superior do player desce mais, cobrindo a área logo após o aviso IA.
- Início do catálogo agora embaralha os filmes/doramas, então os primeiros destaques mudam a cada abertura/recriação da Home.
- Stories passam a usar o mesmo conceito de enquadramento do player do GreenPlay: toque bloqueado no player incorporado e faixas pretas superior/inferior cobrindo o chrome externo.
- Stories continuam com swipe vertical, Favoritar, Comentários e Assistir agora.
- Nenhum arquivo do aplicativo GreenPlay foi alterado.
""",encoding="utf-8")
print("YELLY_126_RANDOM_HOME_GREENPLAY_STORIES_OK")
