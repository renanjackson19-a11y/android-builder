from pathlib import Path
p=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
s=p.read_text()

s=s.replace('String raw="catalog52836_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);',
            'String raw="catalog52839_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);',1)

old='boolean cachedTvBrowserCategoryComplete(int typeId,String categoryId){JSONObject cache=readHomeCache();JSONArray secs=cache==null?null:cache.optJSONArray("result");if(secs==null)return false;for(int i=0;i<secs.length();i++){JSONObject sec=secs.optJSONObject(i);if(sec==null)continue;int t=sec.optInt("type_id",sec.optInt("video_type",1));if(t==typeId&&categoryId.equals(sec.optString("category_id","")))return sec.optInt("category_complete",0)==1;}return false;}'
new='boolean categorySectionActuallyComplete(JSONObject sec){if(sec==null)return false;JSONArray d=sec.optJSONArray("data");int have=d==null?0:d.length();int total=categoryKnownTotal(sec);return total>0&&have>=total;}\n boolean cachedTvBrowserCategoryComplete(int typeId,String categoryId){JSONObject cache=readHomeCache();JSONArray secs=cache==null?null:cache.optJSONArray("result");if(secs==null)return false;for(int i=0;i<secs.length();i++){JSONObject sec=secs.optJSONObject(i);if(sec==null)continue;int t=sec.optInt("type_id",sec.optInt("video_type",1));if(t==typeId&&categoryId.equals(sec.optString("category_id","")))return categorySectionActuallyComplete(sec);}return false;}'
assert old in s
s=s.replace(old,new,1)

old='int categoryResponseTotal(JSONObject j){if(j==null)return 0;String[] keys={"total_rows","total","total_count","recordsTotal","records_total","count"};for(String k:keys){int n=jsonPositiveInt(j,k);if(n>0)return n;}JSONObject p=j.optJSONObject("pagination");if(p!=null){int n=jsonPositiveInt(p,"total","total_rows","total_count","recordsTotal","count");if(n>0)return n;}JSONObject d=j.optJSONObject("data");if(d!=null){int n=jsonPositiveInt(d,"total","total_rows","total_count","recordsTotal","count");if(n>0)return n;}return 0;}'
new='int categoryResponseTotal(JSONObject j){if(j==null)return 0;String[] keys={"total_rows","total_count","recordsTotal","records_total","total"};for(String k:keys){int n=jsonPositiveInt(j,k);if(n>0)return n;}JSONObject p=j.optJSONObject("pagination");if(p!=null){int n=jsonPositiveInt(p,"total_rows","total_count","recordsTotal","records_total","total");if(n>0)return n;}JSONObject d=j.optJSONObject("data");if(d!=null){int n=jsonPositiveInt(d,"total_rows","total_count","recordsTotal","records_total","total");if(n>0)return n;}return 0;}'
assert old in s
s=s.replace(old,new,1)

old='int categoryPageSize(){return 160;}\n Map<String,String> categoryPageArgs(int typeId,String categoryId,int page,int offset){String contentType=typeId==2?"series":"movie";String size=String.valueOf(categoryPageSize());return Api.m("user_id",uid,"type",contentType,"category_id",categoryId,"page_no",String.valueOf(page),"page",String.valueOf(page),"offset",String.valueOf(Math.max(0,offset)),"limit",size,"per_page",size,"page_size",size,"full_catalog","0","all","1");}'
new='int categoryPageSize(){return 120;}\n Map<String,String> categoryPageArgs(int typeId,String categoryId,int page,int offset){String contentType=typeId==2?"series":"movie";String size=String.valueOf(categoryPageSize()),off=String.valueOf(Math.max(0,offset));return Api.m("user_id",uid,"type",contentType,"category_id",categoryId,"page_no",String.valueOf(page),"page",String.valueOf(page),"current_page",String.valueOf(page),"page_index",String.valueOf(Math.max(0,page-1)),"offset",off,"start",off,"skip",off,"from",off,"start_index",off,"length",size,"limit",size,"per_page",size,"page_size",size,"full_catalog","0","all","1");}'
assert old in s
s=s.replace(old,new,1)

old='JSONArray cached=cachedTvBrowserCategory(typeId,categoryId);if(cached!=null&&cached.length()>0){showTvCatalogRowsRv(cached,recycler);if(cachedTvBrowserCategoryComplete(typeId,categoryId))return;}else showTvCatalogStateRv("Carregando conteúdo…");fetchAllCategoryPagesCancelable(typeId,categoryId,request,new AllPagesCB(){public void ok(JSONArray a){if(request!=tvBrowserGridGeneration||recycler.getParent()==null)return;if(a==null||a.length()==0){if(cached==null||cached.length()==0)showTvCatalogStateRv("Nenhum conteúdo nesta categoria");return;}showTvCatalogRowsRv(a,recycler);}public void err(String e){if(request!=tvBrowserGridGeneration||recycler.getParent()==null)return;if(cached==null||cached.length()==0)showTvCatalogStateRv("Não foi possível carregar. Tente novamente.");}});'
new='JSONArray cached=cachedTvBrowserCategory(typeId,categoryId);if(cached!=null&&cached.length()>0){showTvCatalogRowsRv(cached,recycler);if(cachedTvBrowserCategoryComplete(typeId,categoryId))return;}else showTvCatalogStateRv("Carregando conteúdo…");fetchAllCategoryPagesCancelable(typeId,categoryId,request,new AllPagesCB(){public void ok(JSONArray a){if(request!=tvBrowserGridGeneration||recycler.getParent()==null)return;if(a==null||a.length()==0){if(cached==null||cached.length()==0)showTvCatalogStateRv("Nenhum conteúdo nesta categoria");return;}showTvCatalogRowsRv(mergeCategoryRows(cached,a),recycler);}public void err(String e){if(request!=tvBrowserGridGeneration||recycler.getParent()==null)return;if(cached==null||cached.length()==0)showTvCatalogStateRv("Não foi possível carregar. Tente novamente.");}});'
assert old in s
s=s.replace(old,new,1)

old='final String cid=sec.optString("category_id","").trim();final boolean categoryComplete=sec.optInt("category_complete",0)==1;final JSONArray first=sec.optJSONArray("data");'
new='final String cid=sec.optString("category_id","").trim();final boolean categoryComplete=categorySectionActuallyComplete(sec);final JSONArray first=sec.optJSONArray("data");'
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52838' in t and "versionName '5.28.38'" in t
t=t.replace('versionCode 52838','versionCode 52839',1).replace("versionName '5.28.38'","versionName '5.28.39'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52839.txt').write_text("""GreenPlay 5.28.39

- Corrige cache antigo marcando preview como categoria completa.
- Novo schema catalog52839 por usuário+provedor.
- Só considera categoria completa quando quantidade carregada >= total real.
- Sempre busca o restante quando a Home tem apenas preview.
- Paginação em blocos de 120 com aliases page/offset/start/skip/from.
- TV mescla preview cacheado com páginas novas sem perder os primeiros itens.
- Mantém contagem por categoria e Home preservada ao voltar do Perfil.
""")

out=p.read_text()
assert 'catalog52839_' in out
assert 'categorySectionActuallyComplete' in out
assert '"start",off' in out and '"skip",off' in out and '"from",off' in out and '"length",size' in out
assert '"limit","5000"' not in out
assert '"full_catalog","1"' not in out
assert 'versionCode 52839' in b.read_text()
print('OK 5.28.39')
