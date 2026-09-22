from pathlib import Path
p=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
s=p.read_text()

def rep(old,new,n=1):
    global s
    assert old in s, old[:160]
    s=s.replace(old,new,n)

rep('String raw="catalog52841_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);',
    'String raw="catalog52842_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);')

rep(''' void homeTab(String selected){
  if(selected==null||selected.trim().isEmpty())selected="Recomendações";
  final boolean recommendations="Recomendações".equals(selected);''',
''' void homeTab(String selected){
  if(selected==null||selected.trim().isEmpty())selected="Recomendações";
  if("Shorts".equals(selected)&&!currentProviderHasShorts())selected="Recomendações";
  final boolean recommendations="Recomendações".equals(selected);''')

rep(''' boolean hasShortsSections(JSONObject c){JSONArray a=c==null?null:c.optJSONArray("result");if(a==null)return false;for(int i=0;i<a.length();i++){JSONObject sec=a.optJSONObject(i);if(sec!=null&&isShortsSection(sec)){JSONArray d=sec.optJSONArray("data");if(d!=null&&d.length()>0)return true;}}return false;}''',
''' boolean hasShortsSections(JSONObject c){JSONArray a=c==null?null:c.optJSONArray("result");if(a==null)return false;for(int i=0;i<a.length();i++){JSONObject sec=a.optJSONObject(i);if(sec!=null&&isShortsSection(sec)){JSONArray d=sec.optJSONArray("data");if(d!=null&&d.length()>0)return true;}}return false;}
 boolean currentProviderHasShorts(){JSONObject c=readHomeCache();return hasShortsSections(c);}''')

rep('''  addHomeTopMediaTab(tabs,R.drawable.top_series,"Séries",selected);
  addHomeTopMediaTab(tabs,R.drawable.top_shorts,"Shorts",selected);''',
'''  addHomeTopMediaTab(tabs,R.drawable.top_series,"Séries",selected);
  if(currentProviderHasShorts())addHomeTopMediaTab(tabs,R.drawable.top_shorts,"Shorts",selected);''')

rep('''  item.setBackgroundColor(Color.TRANSPARENT);
  ImageView icon=new ImageView(this);''',
'''  item.setBackgroundColor(Color.TRANSPARENT);
  if("Shorts".equals(action))item.setContentDescription("GreenShorts");
  ImageView icon=new ImageView(this);''')

rep(''' String cleanCategoryDisplayTitle(String raw,int typeId){
  String title=fixTitle(raw);if(title==null)title="";title=title.trim();''',
''' String cleanCategoryDisplayTitle(String raw,int typeId){
  String title=fixTitle(raw);if(title==null)title="";title=title.trim();
  if(isShortsCategoryTitle(title))return "GreenShorts";''')

rep('''FrameLayout poster=new FrameLayout(this);poster.setBackground(round(CARD,13));ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);Img.loadBest(im,use.optString("thumbnail",""),use.optString("portrait_img",""),use.optString("image",""),use.optString("poster",""),use.optString("landscape",""),use.optString("landscape_img",""),use.optString("backdrop",""));''',
'''FrameLayout poster=new FrameLayout(this);poster.setBackground(round(CARD,13));ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);if("Shorts".equals(activeHomeTab))im.setImageResource(R.drawable.top_shorts);Img.loadBest(im,use.optString("thumbnail",""),use.optString("portrait_img",""),use.optString("image",""),use.optString("poster",""),use.optString("landscape",""),use.optString("landscape_img",""),use.optString("backdrop",""));''')

rep('''ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setBackground(round(CARD,15));im.setClipToOutline(true);Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("landscape",""),x.optString("landscape_img",""));''',
'''ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setBackground(round(CARD,15));im.setClipToOutline(true);if("Shorts".equals(activeHomeTab))im.setImageResource(R.drawable.top_shorts);Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("landscape",""),x.optString("landscape_img",""));''')

p.write_text(s)

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52841' in t and "versionName '5.28.41'" in t
t=t.replace('versionCode 52841','versionCode 52842',1).replace("versionName '5.28.41'","versionName '5.28.42'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52842.txt').write_text("""GreenPlay 5.28.42

- GreenShorts é detectado dinamicamente por provedor.
- A aba GreenShorts só aparece quando o catálogo ativo realmente contém ReelShort/Reels Shorts/GreenShorts.
- Provedores sem Shorts não mostram a aba, igual à regra da TV ao vivo.
- Regra é provider-scoped e funciona também para provedores adicionados no futuro.
- Todos os nomes ReelShort/Reels Shorts são apresentados como GreenShorts.
- Cards GreenShorts sem capa válida mantêm placeholder GreenShorts em vez de card vazio.
- Cache de catálogo renovado para reavaliar a presença de GreenShorts por provedor.
""")

out=p.read_text()
assert 'catalog52842_' in out
assert 'currentProviderHasShorts()' in out
assert 'if(currentProviderHasShorts())addHomeTopMediaTab' in out
assert 'return "GreenShorts"' in out
assert 'im.setImageResource(R.drawable.top_shorts)' in out
assert 'versionCode 52842' in b.read_text()
print('OK 5.28.42')
