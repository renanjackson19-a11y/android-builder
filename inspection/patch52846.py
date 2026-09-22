from pathlib import Path
p=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
s=p.read_text()

def rep(old,new,n=1):
    global s
    assert old in s, old[:180]
    s=s.replace(old,new,n)

old='boolean persistentHomeReadPending=false; boolean catalogPrefetchBusy=false,catalogTabPrepareBusy=false; String catalogTabPending=""; long catalogPrefetchAt=0L; GridLayout mobileCategoryGrid=null; JSONArray mobileCategoryRows=new JSONArray(); int mobileCategoryNextIndex=0,mobileCategoryCardW=0,mobileCategoryGen=0; boolean mobileCategoryChunkPending=false; int mobileCategoryTypeId=0,mobileCategoryNextPageNo=1,mobileCategoryNetworkTotal=0,mobileCategoryNetworkRetries=0; String mobileCategoryId=""; boolean mobileCategoryNetworkBusy=false,mobileCategoryNetworkDone=false; java.util.HashSet<String> mobileCategorySeen=new java.util.HashSet<>(); LinearLayout mobileCategoryLoadingFooter=null; TextView mobileCategoryLoadingText=null; ProgressBar mobileCategoryLoadingProgress=null;'
rep(old,old+' java.util.ArrayList<String> mobileCategoryIds=new java.util.ArrayList<>(); int mobileCategoryIdIndex=0; boolean mobileShortsPaging=false;')

rep('mobileCategoryId="";mobileCategoryNetworkBusy=false;mobileCategoryNetworkDone=false;mobileCategorySeen.clear();mobileCategoryLoadingFooter=null;',
    'mobileCategoryId="";mobileCategoryNetworkBusy=false;mobileCategoryNetworkDone=false;mobileCategorySeen.clear();mobileCategoryIds.clear();mobileCategoryIdIndex=0;mobileShortsPaging=false;mobileCategoryLoadingFooter=null;')

rep('if(!recommendations&&("Filmes".equals(selected)||"Séries".equals(selected)||"Shorts".equals(selected))&&!catalogTabReady(selected)){prepareCatalogTabAtomic(selected);return;}',
    'if(!recommendations&&("Filmes".equals(selected)||"Séries".equals(selected))&&!catalogTabReady(selected)){prepareCatalogTabAtomic(selected);return;}')

rep('if("Shorts".equals(selected)){JSONArray featured=featuredForShorts(12);if(featured.length()>0)featureCarousel(featured);loadShortsCategorySections(gen);return;}',
    'if("Shorts".equals(selected)){loadShortsCategorySections(gen);return;}')

old_method=''' void loadShortsCategorySections(final int gen){
  final LinearLayout host=body;if(host==null)return;JSONObject prepared=readHomeCache();JSONArray secs=prepared==null?null:prepared.optJSONArray("result");JSONArray loose=collectShortsLooseItems(secs);
  if(loose.length()>0){grid(loose);return;}
  TextView empty=t("Nenhum GreenShorts encontrado nesta fonte.",14);empty.setTextColor(0xff9da7a2);empty.setGravity(Gravity.CENTER);host.addView(empty,new LinearLayout.LayoutParams(-1,dp(72)));
 }'''

new_method=''' void loadShortsCategorySections(final int gen){
  final LinearLayout host=body;if(host==null)return;
  final TextView loading=t("Carregando GreenShorts…",14);loading.setTextColor(0xff9da7a2);loading.setGravity(Gravity.CENTER);host.addView(loading,new LinearLayout.LayoutParams(-1,dp(72)));
  Api.post("get_category",Api.m("type","movie","user_id",uid),new Api.CB(){public void ok(JSONObject j){
   if(gen!=viewGen||host!=body)return;JSONArray cats=j.optJSONArray("result");java.util.ArrayList<JSONObject> found=new java.util.ArrayList<>();
   if(cats!=null)for(int i=0;i<cats.length();i++){JSONObject c=cats.optJSONObject(i);if(c!=null&&isShortsCategory(c))found.add(c);}
   if(found.isEmpty()){if(loading.getParent()!=null)host.removeView(loading);showShortsEmpty(host);return;}
   java.util.Collections.sort(found,(a,b)->Integer.compare(categoryKnownTotal(b),categoryKnownTotal(a)));
   if(wideTvUi()){fetchAllShortsDirectTv(found,0,1,new JSONArray(),new java.util.HashSet<String>(),gen,loading);return;}
   fetchFirstShortsDirectMobile(found,0,gen,loading);
  }public void err(String e){if(gen!=viewGen||host!=body)return;if(loading.getParent()!=null)host.removeView(loading);showShortsEmpty(host);}});
 }
 void showShortsEmpty(LinearLayout host){if(host==null)return;TextView empty=t("Nenhum GreenShorts encontrado nesta fonte.",14);empty.setTextColor(0xff9da7a2);empty.setGravity(Gravity.CENTER);host.addView(empty,new LinearLayout.LayoutParams(-1,dp(72)));}
 JSONArray strictShortsCategoryRows(String cid,JSONArray data){JSONArray out=new JSONArray();if(cid==null||data==null)return out;String wanted=cid.trim();for(int i=0;i<data.length();i++){JSONObject x=data.optJSONObject(i);if(x==null)continue;String actual=shortsItemCategoryId(x);if(!wanted.isEmpty()&&wanted.equals(actual))out.put(x);}return out;}
 JSONArray firstRows(JSONArray src,int max){JSONArray out=new JSONArray();if(src==null)return out;for(int i=0;i<Math.min(max,src.length());i++){JSONObject x=src.optJSONObject(i);if(x!=null)out.put(x);}return out;}
 void fetchFirstShortsDirectMobile(java.util.ArrayList<JSONObject> cats,int index,final int gen,final TextView loading){
  if(gen!=viewGen)return;if(index>=cats.size()){if(loading!=null&&loading.getParent()!=null)body.removeView(loading);showShortsEmpty(body);return;}
  JSONObject cat=cats.get(index);final String cid=cat.optString("category_id",cat.optString("id","")).trim();if(cid.isEmpty()){fetchFirstShortsDirectMobile(cats,index+1,gen,loading);return;}
  Api.post("content_by_category",categoryPageArgs(1,cid,1,0),new Api.CB(){public void ok(JSONObject j){
   if(gen!=viewGen)return;JSONArray clean=strictShortsCategoryRows(cid,j.optJSONArray("result"));if(clean.length()==0){fetchFirstShortsDirectMobile(cats,index+1,gen,loading);return;}
   if(loading!=null&&loading.getParent()!=null)body.removeView(loading);JSONArray hero=firstRows(clean,12);if(hero.length()>0)featureCarousel(hero);grid(clean);
   java.util.ArrayList<String> ids=new java.util.ArrayList<>();for(int k=index;k<cats.size();k++){JSONObject c=cats.get(k);String x=c.optString("category_id",c.optString("id","")).trim();if(!x.isEmpty())ids.add(x);}
   startMobileShortsPaging(ids,2,clean,gen);
  }public void err(String e){if(gen==viewGen)fetchFirstShortsDirectMobile(cats,index+1,gen,loading);}});
 }
 void fetchAllShortsDirectTv(java.util.ArrayList<JSONObject> cats,int catIndex,int page,JSONArray acc,java.util.HashSet<String> seen,final int gen,final TextView loading){
  if(gen!=viewGen)return;if(catIndex>=cats.size()){if(loading!=null&&loading.getParent()!=null)body.removeView(loading);if(acc.length()==0){showShortsEmpty(body);return;}JSONArray hero=firstRows(acc,12);if(hero.length()>0)featureCarousel(hero);grid(acc);return;}
  JSONObject cat=cats.get(catIndex);final String cid=cat.optString("category_id",cat.optString("id","")).trim();if(cid.isEmpty()){fetchAllShortsDirectTv(cats,catIndex+1,1,acc,seen,gen,loading);return;}
  final int p=page;Api.post("content_by_category",categoryPageArgs(1,cid,p,(p-1)*categoryPageSize()),new Api.CB(){public void ok(JSONObject j){
   if(gen!=viewGen)return;JSONArray clean=strictShortsCategoryRows(cid,j.optJSONArray("result"));for(int i=0;i<clean.length();i++){JSONObject x=clean.optJSONObject(i);if(x==null)continue;String k=itemKey(x);if(seen.add(k))acc.put(x);}
   boolean more=j.optBoolean("more_page",clean.length()>=categoryPageSize());if(more&&clean.length()>0)fetchAllShortsDirectTv(cats,catIndex,p+1,acc,seen,gen,loading);else fetchAllShortsDirectTv(cats,catIndex+1,1,acc,seen,gen,loading);
  }public void err(String e){if(gen==viewGen)fetchAllShortsDirectTv(cats,catIndex+1,1,acc,seen,gen,loading);}});
 }'''
rep(old_method,new_method)

rep('if(wideTvUi()||gen!=viewGen)return;mobileCategoryTypeId=typeId;mobileCategoryId=categoryId==null?"":categoryId.trim();mobileCategoryNextPageNo=1;',
    'if(wideTvUi()||gen!=viewGen)return;mobileShortsPaging=false;mobileCategoryIds.clear();mobileCategoryIdIndex=0;mobileCategoryTypeId=typeId;mobileCategoryId=categoryId==null?"":categoryId.trim();mobileCategoryNextPageNo=1;')

needle=''' void maybeLoadNextMobileCategoryPage(){
'''
insert=''' void startMobileShortsPaging(java.util.ArrayList<String> ids,int nextPage,JSONArray first,int gen){
  if(wideTvUi()||gen!=viewGen)return;mobileShortsPaging=true;mobileCategoryIds.clear();if(ids!=null)mobileCategoryIds.addAll(ids);mobileCategoryIdIndex=0;mobileCategoryTypeId=1;mobileCategoryId=mobileCategoryIds.isEmpty()?"":mobileCategoryIds.get(0);mobileCategoryNextPageNo=Math.max(1,nextPage);mobileCategoryNetworkTotal=0;mobileCategoryNetworkRetries=0;mobileCategoryNetworkBusy=false;mobileCategoryNetworkDone=mobileCategoryId.isEmpty();mobileCategorySeen.clear();setMobileCategoryLoading(!mobileCategoryNetworkDone,"Carregando mais conteúdo…");
  JSONArray seed=mobileCategoryRows==null?first:mobileCategoryRows;if(seed!=null)for(int i=0;i<seed.length();i++){JSONObject x=seed.optJSONObject(i);if(x==null)continue;String k=itemKey(x);if(k==null||k.trim().isEmpty())k=x.optString("id",x.optString("video_id",x.optString("name","")))+"|"+x.optString("stream_url",x.optString("url",""));mobileCategorySeen.add(k);}
  maybeLoadNextMobileCategoryPage();
 }
 void maybeLoadNextMobileCategoryPage(){
'''
rep(needle,insert)

old_page='''   JSONArray rows=j.optJSONArray("result");int total=categoryResponseTotal(j);if(total>0)mobileCategoryNetworkTotal=total;if(rows!=null)for(int i=0;i<rows.length();i++){JSONObject x=rows.optJSONObject(i);if(x==null)continue;String k=itemKey(x);if(k==null||k.trim().isEmpty())k=x.optString("id",x.optString("video_id",x.optString("name","")))+"|"+x.optString("stream_url",x.optString("url",""));if(mobileCategorySeen.add(k))mobileCategoryRows.put(x);}
   boolean more=j.optBoolean("more_page",rows!=null&&rows.length()>=categoryPageSize());if((mobileCategoryNetworkTotal>0&&mobileCategoryRows.length()>=mobileCategoryNetworkTotal)||!more||rows==null||rows.length()==0){mobileCategoryNetworkDone=true;}else{mobileCategoryNextPageNo=page+1;}setMobileCategoryLoading(!mobileCategoryNetworkDone,"Carregando mais conteúdo…");
   maybeLoadMoreMobileCategory(true);if(!mobileCategoryNetworkDone&&mainScroll!=null&&body!=null){int remaining=body.getHeight()-(mainScroll.getScrollY()+mainScroll.getHeight());if(remaining<dp(900))mainScroll.postDelayed(()->maybeLoadNextMobileCategoryPage(),60);}'''
new_page='''   JSONArray rows=j.optJSONArray("result");if(mobileShortsPaging)rows=strictShortsCategoryRows(cid,rows);int total=categoryResponseTotal(j);if(total>0)mobileCategoryNetworkTotal=total;if(rows!=null)for(int i=0;i<rows.length();i++){JSONObject x=rows.optJSONObject(i);if(x==null)continue;String k=itemKey(x);if(k==null||k.trim().isEmpty())k=x.optString("id",x.optString("video_id",x.optString("name","")))+"|"+x.optString("stream_url",x.optString("url",""));if(mobileCategorySeen.add(k))mobileCategoryRows.put(x);}
   boolean more=j.optBoolean("more_page",rows!=null&&rows.length()>=categoryPageSize());boolean categoryDone=!more||rows==null||rows.length()==0;if(!mobileShortsPaging&&mobileCategoryNetworkTotal>0&&mobileCategoryRows.length()>=mobileCategoryNetworkTotal)categoryDone=true;
   if(categoryDone&&mobileShortsPaging&&mobileCategoryIdIndex+1<mobileCategoryIds.size()){mobileCategoryIdIndex++;mobileCategoryId=mobileCategoryIds.get(mobileCategoryIdIndex);mobileCategoryNextPageNo=1;mobileCategoryNetworkTotal=0;mobileCategoryNetworkDone=false;}else if(categoryDone){mobileCategoryNetworkDone=true;}else{mobileCategoryNextPageNo=page+1;}
   setMobileCategoryLoading(!mobileCategoryNetworkDone,"Carregando mais conteúdo…");maybeLoadMoreMobileCategory(true);if(!mobileCategoryNetworkDone&&mainScroll!=null&&body!=null){int remaining=body.getHeight()-(mainScroll.getScrollY()+mainScroll.getHeight());if(remaining<dp(900))mainScroll.postDelayed(()->maybeLoadNextMobileCategoryPage(),60);}'''
rep(old_page,new_page)

rep('LinearLayout card(JSONObject x){JSONObject merged=mergeDetailJson(x,readDetailCache(x));final JSONObject use=merged==null?x:merged;',
    'LinearLayout card(JSONObject x){JSONObject merged="Shorts".equals(activeHomeTab)?x:mergeDetailJson(x,readDetailCache(x));final JSONObject use=merged==null?x:merged;')

rep('String raw="catalog52845_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);',
    'String raw="catalog52846_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);')

p.write_text(s)

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52845' in t and "versionName '5.28.45'" in t
t=t.replace('versionCode 52845','versionCode 52846',1).replace("versionName '5.28.45'","versionName '5.28.46'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52846.txt').write_text("""GreenPlay 5.28.46

- GreenShorts deixa de usar a lista de itens do cache da Home.
- Ao abrir GreenShorts, o app consulta get_category do provedor ativo e busca somente category_id(s) realmente Shorts.
- Filmes normais de outras categorias não entram no banner nem na grade.
- Suporta mais de uma categoria Shorts no mesmo provedor e continua paginando entre elas.
- Mobile pagina conforme rolagem; TV/TV Box busca todas as páginas das categorias Shorts.
- Cards GreenShorts não reutilizam detalhe antigo do cache para substituir nome/capa do item.
- Fallback GreenShorts será a arte enviada pelo usuário.
- GreenShorts continua no topo e continua oculto quando o provedor não possui Shorts.
""")

out=p.read_text()
assert 'catalog52846_' in out
assert 'fetchFirstShortsDirectMobile' in out
assert 'fetchAllShortsDirectTv' in out
assert 'startMobileShortsPaging' in out
assert '||"Shorts".equals(selected)' not in out[out.index('void homeTab'):out.index('void homeSectionTab')]
assert 'versionCode 52846' in b.read_text()
print('OK 5.28.46')
