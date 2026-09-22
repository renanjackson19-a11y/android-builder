from pathlib import Path
p=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
s=p.read_text()

old='boolean persistentHomeReadPending=false; boolean catalogPrefetchBusy=false,catalogTabPrepareBusy=false; String catalogTabPending=""; long catalogPrefetchAt=0L; GridLayout mobileCategoryGrid=null; JSONArray mobileCategoryRows=new JSONArray(); int mobileCategoryNextIndex=0,mobileCategoryCardW=0,mobileCategoryGen=0; boolean mobileCategoryChunkPending=false;'
new='boolean persistentHomeReadPending=false; boolean catalogPrefetchBusy=false,catalogTabPrepareBusy=false; String catalogTabPending=""; long catalogPrefetchAt=0L; GridLayout mobileCategoryGrid=null; JSONArray mobileCategoryRows=new JSONArray(); int mobileCategoryNextIndex=0,mobileCategoryCardW=0,mobileCategoryGen=0; boolean mobileCategoryChunkPending=false; int mobileCategoryTypeId=0,mobileCategoryNextPageNo=1,mobileCategoryNetworkTotal=0,mobileCategoryNetworkRetries=0; String mobileCategoryId=""; boolean mobileCategoryNetworkBusy=false,mobileCategoryNetworkDone=false; java.util.HashSet<String> mobileCategorySeen=new java.util.HashSet<>();'
assert old in s
s=s.replace(old,new,1)

old='void clear(){viewGen++;cancelTvCatalogWork();releaseTvInlinePlayer();try{if(mainScroll!=null)mainScroll.setOnScrollChangeListener((View.OnScrollChangeListener)null);}catch(Exception ignored){}mobileCategoryGrid=null;mobileCategoryRows=new JSONArray();mobileCategoryNextIndex=0;mobileCategoryChunkPending=false;if(body!=null){body.removeAllViews();/* v5.2: nunca herdar a largura da tela anterior. A Home/Destaque usa sempre o mesmo inset TV; páginas especiais aplicam o próprio inset depois de clear(). */int side=wideTvUi()?dp(28):dp(18);body.setPadding(side,wideTvUi()?dp(12):dp(2),side,wideTvUi()?dp(18):dp(10));}}'
new='void clear(){viewGen++;cancelTvCatalogWork();releaseTvInlinePlayer();try{if(mainScroll!=null)mainScroll.setOnScrollChangeListener((View.OnScrollChangeListener)null);}catch(Exception ignored){}mobileCategoryGrid=null;mobileCategoryRows=new JSONArray();mobileCategoryNextIndex=0;mobileCategoryChunkPending=false;mobileCategoryTypeId=0;mobileCategoryNextPageNo=1;mobileCategoryNetworkTotal=0;mobileCategoryNetworkRetries=0;mobileCategoryId="";mobileCategoryNetworkBusy=false;mobileCategoryNetworkDone=false;mobileCategorySeen.clear();if(body!=null){body.removeAllViews();/* v5.2: nunca herdar a largura da tela anterior. A Home/Destaque usa sempre o mesmo inset TV; páginas especiais aplicam o próprio inset depois de clear(). */int side=wideTvUi()?dp(28):dp(18);body.setPadding(side,wideTvUi()?dp(12):dp(2),side,wideTvUi()?dp(18):dp(10));}}'
assert old in s
s=s.replace(old,new,1)

old=''' void openSection(JSONObject sec){
  final String returnTab=activeHomeTab;beginSectionPage(returnTab);
  int typeId=sec.optInt("type_id",sec.optInt("video_type",1));clear();setNav(0);final int gen=viewGen;String title=cleanCategoryDisplayTitle(sec.optString("title","Conteúdos"),typeId);pageTitle(title,()->closeSectionPage());
  final String cid=sec.optString("category_id","").trim();final boolean categoryComplete=categorySectionActuallyComplete(sec);final JSONArray first=sec.optJSONArray("data");
  if(first!=null&&first.length()>0)grid(first);
  if(cid.isEmpty()||categoryComplete)return;
  fetchAllCategoryPages(typeId,cid,new AllPagesCB(){public void ok(JSONArray full){if(gen!=viewGen||full==null||full.length()==0)return;JSONArray merged=mergeCategoryRows(first,full);if(first==null||first.length()==0){grid(merged);return;}if(!wideTvUi()&&mobileCategoryGrid!=null&&mobileCategoryGen==gen){mobileCategoryRows=merged;maybeLoadMoreMobileCategory(true);}else if(wideTvUi()&&merged.length()>first.length()){grid(merged);}}public void err(String e){/* Mantem a amostra e permite nova tentativa ao reabrir. */}});
 }
 void grid(JSONArray a){
  int cols=wideTvUi()?tvGridColumns():3;GridLayout g=new GridLayout(this);g.setColumnCount(cols);g.setUseDefaultMargins(false);body.addView(g,new LinearLayout.LayoutParams(-1,-2));
  if(a==null||a.length()==0)return;int side=wideTvUi()?tvContentSide():dp(18);int usable=getResources().getDisplayMetrics().widthPixels-(wideTvUi()?side*2:dp(52));int w=Math.max(dp(112),usable/cols);int gen=viewGen;
  if(wideTvUi()){addGridChunk(g,a,0,w,gen);return;}
  mobileCategoryGrid=g;mobileCategoryRows=a;mobileCategoryNextIndex=0;mobileCategoryCardW=w;mobileCategoryGen=gen;mobileCategoryChunkPending=false;maybeLoadMoreMobileCategory(true);
  if(mainScroll!=null)mainScroll.setOnScrollChangeListener((v,sx,sy,ox,oy)->{if(gen!=viewGen||mobileCategoryGrid!=g)return;int remaining=body==null?0:body.getHeight()-(sy+mainScroll.getHeight());if(remaining<dp(900))maybeLoadMoreMobileCategory(false);});
 }
'''
new=''' void openSection(JSONObject sec){
  final String returnTab=activeHomeTab;beginSectionPage(returnTab);
  int typeId=sec.optInt("type_id",sec.optInt("video_type",1));clear();setNav(0);final int gen=viewGen;String title=cleanCategoryDisplayTitle(sec.optString("title","Conteúdos"),typeId);pageTitle(title,()->closeSectionPage());
  final String cid=sec.optString("category_id","").trim();final boolean categoryComplete=categorySectionActuallyComplete(sec);final JSONArray first=sec.optJSONArray("data");
  if(!wideTvUi()){
   grid(first==null?new JSONArray():first);
   if(!cid.isEmpty()&&!categoryComplete)startMobileCategoryPaging(typeId,cid,first,gen);
   return;
  }
  if(first!=null&&first.length()>0)grid(first);
  if(cid.isEmpty()||categoryComplete)return;
  fetchAllCategoryPages(typeId,cid,new AllPagesCB(){public void ok(JSONArray full){if(gen!=viewGen||full==null||full.length()==0)return;JSONArray merged=mergeCategoryRows(first,full);if(first==null||first.length()==0){grid(merged);return;}if(merged.length()>first.length()){grid(merged);}}public void err(String e){/* Mantem a amostra e permite nova tentativa ao reabrir. */}});
 }
 void grid(JSONArray a){
  int cols=wideTvUi()?tvGridColumns():3;GridLayout g=new GridLayout(this);g.setColumnCount(cols);g.setUseDefaultMargins(false);body.addView(g,new LinearLayout.LayoutParams(-1,-2));
  int side=wideTvUi()?tvContentSide():dp(18);int usable=getResources().getDisplayMetrics().widthPixels-(wideTvUi()?side*2:dp(52));int w=Math.max(dp(112),usable/cols);int gen=viewGen;
  if(wideTvUi()){if(a!=null&&a.length()>0)addGridChunk(g,a,0,w,gen);return;}
  mobileCategoryGrid=g;mobileCategoryRows=mergeCategoryRows(null,a);mobileCategoryNextIndex=0;mobileCategoryCardW=w;mobileCategoryGen=gen;mobileCategoryChunkPending=false;maybeLoadMoreMobileCategory(true);
  if(mainScroll!=null)mainScroll.setOnScrollChangeListener((v,sx,sy,ox,oy)->{if(gen!=viewGen||mobileCategoryGrid!=g)return;int remaining=body==null?0:body.getHeight()-(sy+mainScroll.getHeight());if(remaining<dp(900)){maybeLoadMoreMobileCategory(false);maybeLoadNextMobileCategoryPage();}});
 }
 void startMobileCategoryPaging(int typeId,String categoryId,JSONArray first,int gen){
  if(wideTvUi()||gen!=viewGen)return;mobileCategoryTypeId=typeId;mobileCategoryId=categoryId==null?"":categoryId.trim();mobileCategoryNextPageNo=1;mobileCategoryNetworkTotal=0;mobileCategoryNetworkRetries=0;mobileCategoryNetworkBusy=false;mobileCategoryNetworkDone=mobileCategoryId.isEmpty();mobileCategorySeen.clear();
  JSONArray seed=mobileCategoryRows==null?new JSONArray():mobileCategoryRows;for(int i=0;i<seed.length();i++){JSONObject x=seed.optJSONObject(i);if(x==null)continue;String k=itemKey(x);if(k==null||k.trim().isEmpty())k=x.optString("id",x.optString("video_id",x.optString("name","")))+"|"+x.optString("stream_url",x.optString("url",""));mobileCategorySeen.add(k);}
  maybeLoadNextMobileCategoryPage();
 }
 void maybeLoadNextMobileCategoryPage(){
  if(wideTvUi()||mobileCategoryNetworkDone||mobileCategoryNetworkBusy||mobileCategoryId==null||mobileCategoryId.isEmpty()||mobileCategoryGrid==null||mobileCategoryGen!=viewGen)return;
  final int gen=mobileCategoryGen,page=mobileCategoryNextPageNo;final String cid=mobileCategoryId;final int typeId=mobileCategoryTypeId;mobileCategoryNetworkBusy=true;
  Api.post("content_by_category",categoryPageArgs(typeId,cid,page,(page-1)*categoryPageSize()),new Api.CB(){public void ok(JSONObject j){
   if(gen!=viewGen||mobileCategoryGen!=gen)return;mobileCategoryNetworkBusy=false;mobileCategoryNetworkRetries=0;if(j.optInt("status",200)!=200){mobileCategoryNetworkDone=false;return;}
   JSONArray rows=j.optJSONArray("result");int total=categoryResponseTotal(j);if(total>0)mobileCategoryNetworkTotal=total;if(rows!=null)for(int i=0;i<rows.length();i++){JSONObject x=rows.optJSONObject(i);if(x==null)continue;String k=itemKey(x);if(k==null||k.trim().isEmpty())k=x.optString("id",x.optString("video_id",x.optString("name","")))+"|"+x.optString("stream_url",x.optString("url",""));if(mobileCategorySeen.add(k))mobileCategoryRows.put(x);}
   boolean more=j.optBoolean("more_page",rows!=null&&rows.length()>=categoryPageSize());if((mobileCategoryNetworkTotal>0&&mobileCategoryRows.length()>=mobileCategoryNetworkTotal)||!more||rows==null||rows.length()==0){mobileCategoryNetworkDone=true;}else{mobileCategoryNextPageNo=page+1;}
   maybeLoadMoreMobileCategory(true);if(!mobileCategoryNetworkDone&&mainScroll!=null&&body!=null){int remaining=body.getHeight()-(mainScroll.getScrollY()+mainScroll.getHeight());if(remaining<dp(900))mainScroll.postDelayed(()->maybeLoadNextMobileCategoryPage(),60);}
  }public void err(String e){if(gen!=viewGen||mobileCategoryGen!=gen)return;mobileCategoryNetworkBusy=false;if(mobileCategoryNetworkRetries<2){mobileCategoryNetworkRetries++;new Handler(Looper.getMainLooper()).postDelayed(()->maybeLoadNextMobileCategoryPage(),250L*mobileCategoryNetworkRetries);}}});
 }
'''
assert old in s
s=s.replace(old,new,1)

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52839' in t and "versionName '5.28.39'" in t
t=t.replace('versionCode 52839','versionCode 52840',1).replace("versionName '5.28.39'","versionName '5.28.40'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52840.txt').write_text("""GreenPlay 5.28.40

- Mobile: paginação real por rolagem nas categorias de Filmes e Séries.
- Não espera baixar milhares de itens para atualizar a grade.
- Lotes de 120, sem limite lógico por categoria.
- Próxima página é solicitada ao aproximar do fim da lista.
- Usa total_rows / more_page para saber quando a categoria realmente terminou.
- Duas novas tentativas automáticas em falha temporária de página.
- Cache/preview da Home não é inflado com o catálogo completo.
- Funciona por provider_id, sem IDs de provedor fixos no APK.
""")

out=p.read_text()
assert 'startMobileCategoryPaging' in out
assert 'maybeLoadNextMobileCategoryPage' in out
assert 'mobileCategoryNetworkTotal' in out
assert '"limit","5000"' not in out
assert '"full_catalog","1"' not in out
print('OK 5.28.40')
