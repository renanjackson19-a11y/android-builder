from pathlib import Path
p=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
s=p.read_text()

def rep(old,new,n=1):
    global s
    assert old in s, old[:220]
    s=s.replace(old,new,n)

rep('String raw="catalog52844_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);',
    'String raw="catalog52845_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);')

rep(''' JSONArray featuredForShorts(int max){
  JSONArray out=new JSONArray();JSONObject prepared=readHomeCache();JSONArray sections=prepared==null?null:prepared.optJSONArray("result");if(sections==null||max<=0)return out;java.util.HashSet<String> seen=new java.util.HashSet<>();
  for(int i=0;i<sections.length()&&out.length()<max;i++){JSONObject sec=sections.optJSONObject(i);if(sec==null||!isShortsSection(sec))continue;JSONArray a=sec.optJSONArray("data");if(a==null)continue;for(int j=0;j<a.length()&&out.length()<max;j++){JSONObject x=a.optJSONObject(j);if(x==null)continue;String k=itemKey(x);if(seen.add(k))out.put(x);}}return out;
 }''',
''' JSONArray featuredForShorts(int max){
  JSONArray out=new JSONArray();JSONObject prepared=readHomeCache();JSONArray sections=prepared==null?null:prepared.optJSONArray("result");if(sections==null||max<=0)return out;java.util.HashSet<String> seen=new java.util.HashSet<>();
  for(int i=0;i<sections.length()&&out.length()<max;i++){JSONObject sec=sections.optJSONObject(i);if(sec==null||!isShortsSection(sec))continue;JSONArray a=filterShortsSectionItems(sec,sec.optJSONArray("data"));if(a==null)continue;for(int j=0;j<a.length()&&out.length()<max;j++){JSONObject x=a.optJSONObject(j);if(x==null)continue;String k=itemKey(x);if(seen.add(k))out.put(x);}}return out;
 }''')

rep(''' JSONArray collectShortsLooseItems(JSONArray secs){JSONArray out=new JSONArray();java.util.HashSet<String> seen=new java.util.HashSet<>();if(secs==null)return out;for(int i=0;i<secs.length();i++){JSONObject sec=secs.optJSONObject(i);if(sec==null||!isShortsSection(sec))continue;JSONArray data=sec.optJSONArray("data");if(data==null)continue;for(int j=0;j<data.length();j++){JSONObject x=data.optJSONObject(j);if(x==null)continue;String k=itemKey(x);if(k==null||k.trim().isEmpty())k=x.optString("id",x.optString("video_id",x.optString("name","")))+"|"+x.optString("stream_url",x.optString("url",""));if(seen.add(k))out.put(x);}}return out;}''',
''' String shortsItemCategoryId(JSONObject x){if(x==null)return "";String cid=x.optString("category_id","").trim();if(cid.isEmpty())cid=x.optString("categoryId","").trim();if(cid.isEmpty())cid=x.optString("raw_category_id","").trim();return cid;}
 boolean shortsItemMatchesSection(JSONObject x,JSONObject sec){if(x==null||sec==null)return false;String expected=sec.optString("category_id",sec.optString("id","")).trim();String actual=shortsItemCategoryId(x);if(!expected.isEmpty()&&!actual.isEmpty())return expected.equals(actual);String itemCategory=x.optString("category_name",x.optString("category",""));return !itemCategory.trim().isEmpty()&&isShortsCategoryTitle(itemCategory);}
 JSONArray filterShortsSectionItems(JSONObject sec,JSONArray data){JSONArray out=new JSONArray();if(sec==null||data==null)return out;for(int i=0;i<data.length();i++){JSONObject x=data.optJSONObject(i);if(x!=null&&shortsItemMatchesSection(x,sec))out.put(x);}return out;}
 JSONArray collectShortsLooseItems(JSONArray secs){JSONArray out=new JSONArray();java.util.HashSet<String> seen=new java.util.HashSet<>();if(secs==null)return out;for(int i=0;i<secs.length();i++){JSONObject sec=secs.optJSONObject(i);if(sec==null||!isShortsSection(sec))continue;JSONArray data=filterShortsSectionItems(sec,sec.optJSONArray("data"));for(int j=0;j<data.length();j++){JSONObject x=data.optJSONObject(j);if(x==null)continue;String k=itemKey(x);if(k==null||k.trim().isEmpty())k=x.optString("id",x.optString("video_id",x.optString("name","")))+"|"+x.optString("stream_url",x.optString("url",""));if(seen.add(k))out.put(x);}}return out;}''')

rep('''JSONArray a=r.optJSONArray("result");if(a!=null&&a.length()>0){JSONObject sec=new JSONObject();try{sec.put("title",ftitle);sec.put("category_id",fcid);sec.put("type_id",1);sec.put("video_type",1);sec.put("section_kind","shorts");sec.put("data",a);sections.put(sec);}catch(Exception ignored){}}''',
'''JSONArray a=r.optJSONArray("result");if(a!=null&&a.length()>0){JSONObject sec=new JSONObject();try{sec.put("title",ftitle);sec.put("category_id",fcid);sec.put("type_id",1);sec.put("video_type",1);sec.put("section_kind","shorts");JSONArray clean=filterShortsSectionItems(sec,a);if(clean.length()>0){sec.put("data",clean);sections.put(sec);}}catch(Exception ignored){}}''')

rep('''if(d!=null&&d.length()>0){try{sec.put("section_kind","shorts");}catch(Exception ignored){}out.put(sec);continue;}''',
'''if(d!=null&&d.length()>0){try{sec.put("section_kind","shorts");JSONArray clean=filterShortsSectionItems(sec,d);if(clean.length()>0){sec.put("data",clean);out.put(sec);continue;}}catch(Exception ignored){}}''')

p.write_text(s)

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52844' in t and "versionName '5.28.44'" in t
t=t.replace('versionCode 52844','versionCode 52845',1).replace("versionName '5.28.44'","versionName '5.28.45'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52845.txt').write_text("""GreenPlay 5.28.45

- GreenShorts continua na barra superior.
- Filtro estrito por category_id: filmes comuns não entram na aba GreenShorts.
- Itens sem category_id só entram se o próprio item identificar categoria Shorts.
- O mesmo filtro vale para o carrossel destaque e para a grade.
- Mantém conteúdos soltos, sem subcategorias.
- Mantém a arte GreenShorts do usuário como fallback de capa.
- Não altera Filmes, Séries, TV ou Futebol.
""")

out=p.read_text()
assert 'catalog52845_' in out
assert 'shortsItemMatchesSection' in out
assert 'filterShortsSectionItems' in out
assert 'addHomeTopMediaTab(tabs,R.drawable.top_shorts,"Shorts",selected)' in out
assert 'versionCode 52845' in b.read_text()
print('OK 5.28.45')
