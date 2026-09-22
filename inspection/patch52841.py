from pathlib import Path
p=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
s=p.read_text()

def rep(old,new,n=1):
    global s
    assert old in s, old[:120]
    s=s.replace(old,new,n)

rep('java.util.HashSet<String> mobileCategorySeen=new java.util.HashSet<>();',
    'java.util.HashSet<String> mobileCategorySeen=new java.util.HashSet<>(); LinearLayout mobileCategoryLoadingFooter=null; TextView mobileCategoryLoadingText=null; ProgressBar mobileCategoryLoadingProgress=null;')
rep('String raw="catalog52839_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);',
    'String raw="catalog52841_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);')
rep('mobileCategorySeen.clear();if(body!=null){body.removeAllViews();',
    'mobileCategorySeen.clear();mobileCategoryLoadingFooter=null;mobileCategoryLoadingText=null;mobileCategoryLoadingProgress=null;if(body!=null){body.removeAllViews();')
rep('mobileCategoryGrid=g;mobileCategoryRows=mergeCategoryRows(null,a);mobileCategoryNextIndex=0;mobileCategoryCardW=w;mobileCategoryGen=gen;mobileCategoryChunkPending=false;maybeLoadMoreMobileCategory(true);',
    'mobileCategoryGrid=g;mobileCategoryRows=mergeCategoryRows(null,a);mobileCategoryNextIndex=0;mobileCategoryCardW=w;mobileCategoryGen=gen;mobileCategoryChunkPending=false;buildMobileCategoryLoadingFooter();maybeLoadMoreMobileCategory(true);')
needle='''  if(mainScroll!=null)mainScroll.setOnScrollChangeListener((v,sx,sy,ox,oy)->{if(gen!=viewGen||mobileCategoryGrid!=g)return;int remaining=body==null?0:body.getHeight()-(sy+mainScroll.getHeight());if(remaining<dp(900)){maybeLoadMoreMobileCategory(false);maybeLoadNextMobileCategoryPage();}});
 }
 void startMobileCategoryPaging'''
insert='''  if(mainScroll!=null)mainScroll.setOnScrollChangeListener((v,sx,sy,ox,oy)->{if(gen!=viewGen||mobileCategoryGrid!=g)return;int remaining=body==null?0:body.getHeight()-(sy+mainScroll.getHeight());if(remaining<dp(900)){maybeLoadMoreMobileCategory(false);maybeLoadNextMobileCategoryPage();}});
 }
 void buildMobileCategoryLoadingFooter(){if(body==null||wideTvUi())return;LinearLayout f=new LinearLayout(this);f.setGravity(Gravity.CENTER);f.setOrientation(LinearLayout.HORIZONTAL);f.setPadding(dp(8),dp(12),dp(8),dp(18));ProgressBar pb=new ProgressBar(this,null,android.R.attr.progressBarStyleSmall);pb.setIndeterminate(true);f.addView(pb,new LinearLayout.LayoutParams(dp(26),dp(26)));TextView tx=t("Carregando mais conteúdo…",14);tx.setTextColor(0xffaab5af);LinearLayout.LayoutParams tlp=new LinearLayout.LayoutParams(-2,dp(32));tlp.setMargins(dp(10),0,0,0);f.addView(tx,tlp);f.setVisibility(View.GONE);body.addView(f,new LinearLayout.LayoutParams(-1,dp(62)));mobileCategoryLoadingFooter=f;mobileCategoryLoadingText=tx;mobileCategoryLoadingProgress=pb;}
 void setMobileCategoryLoading(boolean show,String text){if(mobileCategoryLoadingFooter==null)return;if(mobileCategoryLoadingText!=null&&text!=null&&!text.isEmpty())mobileCategoryLoadingText.setText(text);if(mobileCategoryLoadingProgress!=null)mobileCategoryLoadingProgress.setVisibility(show?View.VISIBLE:View.GONE);mobileCategoryLoadingFooter.setVisibility(show?View.VISIBLE:View.GONE);}
 void startMobileCategoryPaging'''
rep(needle,insert)
rep('mobileCategoryNetworkDone=mobileCategoryId.isEmpty();mobileCategorySeen.clear();',
    'mobileCategoryNetworkDone=mobileCategoryId.isEmpty();mobileCategorySeen.clear();setMobileCategoryLoading(!mobileCategoryNetworkDone,"Carregando mais conteúdo…");')
rep('final int typeId=mobileCategoryTypeId;mobileCategoryNetworkBusy=true;',
    'final int typeId=mobileCategoryTypeId;mobileCategoryNetworkBusy=true;setMobileCategoryLoading(true,"Carregando mais conteúdo…");')
rep('if(j.optInt("status",200)!=200){mobileCategoryNetworkDone=false;return;}',
    'if(j.optInt("status",200)!=200){mobileCategoryNetworkDone=false;setMobileCategoryLoading(true,"Carregando mais conteúdo…");return;}')
rep('else{mobileCategoryNextPageNo=page+1;}\n   maybeLoadMoreMobileCategory(true);',
    'else{mobileCategoryNextPageNo=page+1;}setMobileCategoryLoading(!mobileCategoryNetworkDone,"Carregando mais conteúdo…");\n   maybeLoadMoreMobileCategory(true);')
rep('''}public void err(String e){if(gen!=viewGen||mobileCategoryGen!=gen)return;mobileCategoryNetworkBusy=false;if(mobileCategoryNetworkRetries<2){mobileCategoryNetworkRetries++;new Handler(Looper.getMainLooper()).postDelayed(()->maybeLoadNextMobileCategoryPage(),250L*mobileCategoryNetworkRetries);}}});''',
    '''}public void err(String e){if(gen!=viewGen||mobileCategoryGen!=gen)return;mobileCategoryNetworkBusy=false;setMobileCategoryLoading(true,mobileCategoryNetworkRetries<2?"Carregando mais conteúdo…":"Não foi possível carregar mais. Role para tentar novamente.");if(mobileCategoryNetworkRetries<2){mobileCategoryNetworkRetries++;new Handler(Looper.getMainLooper()).postDelayed(()->maybeLoadNextMobileCategoryPage(),250L*mobileCategoryNetworkRetries);}}});''')
old_method=''' void maybeLoadMoreMobileCategory(boolean immediate){if(wideTvUi()||mobileCategoryChunkPending||mobileCategoryGrid==null||mobileCategoryRows==null||mobileCategoryGen!=viewGen)return;if(mobileCategoryNextIndex>=mobileCategoryRows.length())return;mobileCategoryChunkPending=true;Runnable run=()->{if(mobileCategoryGrid==null||mobileCategoryGen!=viewGen){mobileCategoryChunkPending=false;return;}int start=mobileCategoryNextIndex,end=Math.min(mobileCategoryRows.length(),start+48),h=dp(196);for(int i=start;i<end;i++){JSONObject x=mobileCategoryRows.optJSONObject(i);if(x==null)continue;LinearLayout c=card(x);GridLayout.LayoutParams lp=new GridLayout.LayoutParams();lp.width=mobileCategoryCardW;lp.height=h;lp.setMargins(dp(4),dp(5),dp(6),dp(9));mobileCategoryGrid.addView(c,lp);}mobileCategoryNextIndex=end;mobileCategoryChunkPending=false;if(mainScroll!=null&&mobileCategoryNextIndex<mobileCategoryRows.length()&&body!=null&&body.getHeight()<=mainScroll.getHeight()+dp(300))mainScroll.postDelayed(()->maybeLoadMoreMobileCategory(false),20);};if(immediate)run.run();else mobileCategoryGrid.postDelayed(run,12);}'''
new_method=''' void maybeLoadMoreMobileCategory(boolean immediate){if(wideTvUi()||mobileCategoryChunkPending||mobileCategoryGrid==null||mobileCategoryRows==null||mobileCategoryGen!=viewGen)return;if(mobileCategoryNextIndex>=mobileCategoryRows.length())return;mobileCategoryChunkPending=true;Runnable run=()->{if(mobileCategoryGrid==null||mobileCategoryGen!=viewGen){mobileCategoryChunkPending=false;return;}int start=mobileCategoryNextIndex,len=mobileCategoryRows.length(),end=Math.min(len,start+48),h=dp(196);if(!mobileCategoryNetworkDone){int n=end-start;n-=n%3;if(n<=0){mobileCategoryChunkPending=false;maybeLoadNextMobileCategoryPage();return;}end=start+n;}else if(end>=len){int n=end-start;if(n>1&&n%3==1)end--;}boolean finalSingle=mobileCategoryNetworkDone&&start==len-1&&end==len;if(finalSingle){Space pre=new Space(this);GridLayout.LayoutParams sp=new GridLayout.LayoutParams();sp.width=mobileCategoryCardW;sp.height=dp(1);mobileCategoryGrid.addView(pre,sp);}for(int i=start;i<end;i++){JSONObject x=mobileCategoryRows.optJSONObject(i);if(x==null)continue;LinearLayout c=card(x);GridLayout.LayoutParams lp=new GridLayout.LayoutParams();lp.width=mobileCategoryCardW;lp.height=h;lp.setMargins(dp(4),dp(5),dp(6),dp(9));mobileCategoryGrid.addView(c,lp);}if(finalSingle){Space post=new Space(this);GridLayout.LayoutParams sp2=new GridLayout.LayoutParams();sp2.width=mobileCategoryCardW;sp2.height=dp(1);mobileCategoryGrid.addView(post,sp2);}mobileCategoryNextIndex=end;mobileCategoryChunkPending=false;if(mainScroll!=null&&mobileCategoryNextIndex<mobileCategoryRows.length()&&body!=null&&body.getHeight()<=mainScroll.getHeight()+dp(300))mainScroll.postDelayed(()->maybeLoadMoreMobileCategory(false),20);};if(immediate)run.run();else mobileCategoryGrid.postDelayed(run,12);}'''
rep(old_method,new_method)
rep('final String fcid=cid, fname=name, contentType=typeId==2?"series":"movie";active[0]++;',
    'final String fcid=cid, fname=name, contentType=typeId==2?"series":"movie";final int ftotal=categoryKnownTotal(cat);active[0]++;')
rep('sec.put("type_id",typeId);sec.put("data",a);JSONArray rootSections=',
    'sec.put("type_id",typeId);if(ftotal>0)sec.put("category_total",ftotal);sec.put("data",a);JSONArray rootSections=')
rep('sectionHeaderInto(host,typedCategoryTitle(fname,typeId),()->openSection(sec));posterRowInto(host,a);',
    'sectionHeaderInto(host,categoryNameWithCount(typedCategoryTitle(fname,typeId),sec),()->openSection(sec));posterRowInto(host,a);')
rep('TextView wait=t(name+"  ·  carregando…",15);',
    'String countLabel=categoryNameWithCount(typedCategoryTitle(name,typeId),cat);TextView wait=t(countLabel+"  ·  carregando…",15);')
rep('sec.put("type_id",typeId);sec.put("data",a);}catch(Exception e){}sectionHeaderInto(holder,typedCategoryTitle(name,typeId),()->openSection(sec));',
    'sec.put("type_id",typeId);int ctotal=categoryKnownTotal(cat);if(ctotal>0)sec.put("category_total",ctotal);sec.put("data",a);}catch(Exception e){}sectionHeaderInto(holder,categoryNameWithCount(typedCategoryTitle(name,typeId),sec),()->openSection(sec));')
rep('final String cid=cat.optString("category_id",cat.optString("id","")).trim();final String title=fixTitle(cat.optString("category_name",cat.optString("name",typeId==2?"Séries":"Filmes")));',
    'final String cid=cat.optString("category_id",cat.optString("id","")).trim();final String title=fixTitle(cat.optString("category_name",cat.optString("name",typeId==2?"Séries":"Filmes")));final int catTotal=categoryKnownTotal(cat);')
rep('sec.put("type_id",typeId);sec.put("data",data);}catch(Exception ignored){}sectionHeaderInto(host,typedCategoryTitle(title,typeId),()->openSection(sec));',
    'sec.put("type_id",typeId);if(catTotal>0)sec.put("category_total",catTotal);sec.put("data",data);}catch(Exception ignored){}sectionHeaderInto(host,categoryNameWithCount(typedCategoryTitle(title,typeId),sec),()->openSection(sec));')
p.write_text(s)

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52840' in t and "versionName '5.28.40'" in t
t=t.replace('versionCode 52840','versionCode 52841',1).replace("versionName '5.28.40'","versionName '5.28.41'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52841.txt').write_text('''GreenPlay 5.28.41

- Filmes e Séries: rodapé visível Carregando mais conteúdo durante paginação.
- Última linha não deixa um único card perdido no canto durante carregamento.
- Se o total final terminar em 1 item, ele é centralizado na última linha.
- Cache de catálogo renovado para receber as contagens completas do painel.
- Totais de categorias propagados para Filmes e Séries.
- Paginação continua genérica por provider_id, sem limite lógico de itens.
''')

out=p.read_text()
assert 'catalog52841_' in out
assert 'Carregando mais conteúdo…' in out
assert 'finalSingle' in out
assert 'categoryNameWithCount(typedCategoryTitle(fname,typeId),sec)' in out
assert 'versionCode 52841' in b.read_text()
print('OK 5.28.41')
