from pathlib import Path
p=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
s=p.read_text()

old='Map<String,String> categoryPageArgs(int typeId,String categoryId,int page,int offset){String contentType=typeId==2?"series":"movie";String size=String.valueOf(categoryPageSize());return Api.m("user_id",uid,"type",contentType,"category_id",categoryId,"page_no",String.valueOf(page),"page",String.valueOf(page),"offset",String.valueOf(Math.max(0,offset)),"limit",size,"per_page",size,"page_size",size,"full_catalog","0");}'
new='Map<String,String> categoryPageArgs(int typeId,String categoryId,int page,int offset){String contentType=typeId==2?"series":"movie";String size=String.valueOf(categoryPageSize());return Api.m("user_id",uid,"type",contentType,"category_id",categoryId,"page_no",String.valueOf(page),"page",String.valueOf(page),"offset",String.valueOf(Math.max(0,offset)),"limit",size,"per_page",size,"page_size",size,"full_catalog","0","all","1");}'
assert old in s
s=s.replace(old,new,1)

old='void showTvCatalogRowsRv(JSONArray rows,androidx.recyclerview.widget.RecyclerView recycler){if(recycler==null||tvCatalogAdapter==null)return;tvCatalogState.setVisibility(View.GONE);recycler.setVisibility(View.VISIBLE);tvCatalogRows=rows==null?new JSONArray():rows;tvCatalogAdapter.submit(tvCatalogRows);recycler.scrollToPosition(0);}'
new='void showTvCatalogRowsRv(JSONArray rows,androidx.recyclerview.widget.RecyclerView recycler){if(recycler==null||tvCatalogAdapter==null)return;tvCatalogState.setVisibility(View.GONE);recycler.setVisibility(View.VISIBLE);tvCatalogRows=rows==null?new JSONArray():rows;tvCatalogAdapter.submit(tvCatalogRows);}'
assert old in s
s=s.replace(old,new,1)

old='void loadTvBrowserGridRv(int typeId,String categoryId,androidx.recyclerview.widget.RecyclerView recycler){if(recycler==null)return;final int request=++tvBrowserGridGeneration;try{Img.cancelCatalogLoads();}catch(Exception ignored){}tvCatalogRows=new JSONArray();'
new='void loadTvBrowserGridRv(int typeId,String categoryId,androidx.recyclerview.widget.RecyclerView recycler){if(recycler==null)return;final int request=++tvBrowserGridGeneration;try{Img.cancelCatalogLoads();}catch(Exception ignored){}try{recycler.scrollToPosition(0);}catch(Exception ignored){}tvCatalogRows=new JSONArray();'
assert old in s
s=s.replace(old,new,1)

old='if(total>0&&acc.length()>=total){cb.ok(acc);return;}if(added==0){if(total>0&&acc.length()<total){cb.err("Catálogo incompleto");return;}cb.ok(acc);return;}if(request!=tvBrowserGridGeneration)return;fetchAllCategoryPagesRawCancelable(typeId,raw,page+1,acc,seen,request,cb);'
new='if(total>0&&acc.length()>=total){cb.ok(acc);return;}if(added==0){if(total>0&&acc.length()<total){cb.err("Catálogo incompleto");return;}cb.ok(acc);return;}cb.ok(acc);if(request!=tvBrowserGridGeneration)return;fetchAllCategoryPagesRawCancelable(typeId,raw,page+1,acc,seen,request,cb);'
assert old in s
s=s.replace(old,new,1)

anchor='boolean tvKidsCategoryName(String raw){String n=tvNormalizeMatch(raw);return n.contains("kids")||n.contains("infantil")||n.contains("crianc")||n.contains("animacao")||n.contains("animation")||n.contains("familia")||n.contains("family");}'
helpers='''int categoryKnownTotal(JSONObject c){if(c==null)return 0;String[] keys={"category_total","total_rows","total","total_count","recordsTotal","records_total","count","content_count","items_count","movie_count","movies_count","series_count"};for(String k:keys){int n=jsonPositiveInt(c,k);if(n>0)return n;}return 0;}
 String categoryCountText(int n){if(n<=0)return "";try{return java.text.NumberFormat.getIntegerInstance(new java.util.Locale("pt","BR")).format(n);}catch(Exception e){return String.valueOf(n);}}
 String categoryNameWithCount(String name,JSONObject c){int n=categoryKnownTotal(c);return n>0?name+"  ·  "+categoryCountText(n):name;}
 '''+anchor
assert anchor in s
s=s.replace(anchor,helpers,1)

old='try{c.put("category_id",id.isEmpty()?"__cached_"+i:id);c.put("category_name",name);c.put("_tv_type",typeId);}catch(Exception ignored){}out.put(c);'
new='try{c.put("category_id",id.isEmpty()?"__cached_"+i:id);c.put("category_name",name);c.put("_tv_type",typeId);int total=categoryKnownTotal(sec);if(total>0)c.put("category_total",total);}catch(Exception ignored){}out.put(c);'
assert old in s
s=s.replace(old,new,1)

old='String name=cleanCategoryDisplayTitle(c.optString("category_name",c.optString("name","Categoria")),typeId);TextView chip=t(name,13);'
new='String name=cleanCategoryDisplayTitle(c.optString("category_name",c.optString("name","Categoria")),typeId);String label=categoryNameWithCount(name,c);TextView chip=t(label,13);'
assert s.count(old)>=2
s=s.replace(old,new,2)

old='String rawTitle=fixTitle(sec.optString("title",wanted==1?"Filmes":"Séries"));String title=typedCategoryTitle(rawTitle,wanted);final JSONObject fsec=sec;sectionHeaderInto(target,title,()->openSection(fsec));'
new='String rawTitle=fixTitle(sec.optString("title",wanted==1?"Filmes":"Séries"));String title=categoryNameWithCount(typedCategoryTitle(rawTitle,wanted),sec);final JSONObject fsec=sec;sectionHeaderInto(target,title,()->openSection(fsec));'
assert old in s
s=s.replace(old,new,1)

old='String title=fixTitle(sec.optString("title",typeId==2?"Séries":"Filmes"));if(cid>0)shownCats.add(typeId+":"+cid);shownNames.add(typeId+":"+title.trim().toLowerCase(java.util.Locale.ROOT));final JSONObject fsec=sec;sectionHeaderInto(host,typedCategoryTitle(title,typeId),()->openSection(fsec));'
new='String title=fixTitle(sec.optString("title",typeId==2?"Séries":"Filmes"));if(cid>0)shownCats.add(typeId+":"+cid);shownNames.add(typeId+":"+title.trim().toLowerCase(java.util.Locale.ROOT));final JSONObject fsec=sec;sectionHeaderInto(host,categoryNameWithCount(typedCategoryTitle(title,typeId),sec),()->openSection(fsec));'
assert old in s
s=s.replace(old,new,1)

old='String rawTitle=fixTitle(sec.optString("title",typeId==2?"Séries":"Filmes"));String title=typedCategoryTitle(rawTitle,typeId);final JSONObject fsec=sec;sectionHeaderInto(host,title,()->openSection(fsec));'
new='String rawTitle=fixTitle(sec.optString("title",typeId==2?"Séries":"Filmes"));String title=categoryNameWithCount(typedCategoryTitle(rawTitle,typeId),sec);final JSONObject fsec=sec;sectionHeaderInto(host,title,()->openSection(fsec));'
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52837' in t and "versionName '5.28.37'" in t
t=t.replace('versionCode 52837','versionCode 52838',1).replace("versionName '5.28.37'","versionName '5.28.38'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52838.txt').write_text("""GreenPlay 5.28.38

- Corrige categorias presas no primeiro lote.
- full_catalog=0; sem limit=5000.
- all=1 apenas como sinal do catálogo completo paginado do painel.
- TV atualiza a grade a cada página recebida sem voltar ao topo.
- Mantém Home preservada ao voltar do Perfil.
- Mostra quantidade total nas categorias de Filmes/Séries quando o total real está disponível.
""")

out=p.read_text()
assert '"limit","5000"' not in out
assert '"full_catalog","1"' not in out
assert '"full_catalog","0","all","1"' in out
assert 'categoryNameWithCount' in out
assert 'versionCode 52838' in b.read_text()
print('OK 5.28.38')
