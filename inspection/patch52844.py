from pathlib import Path
p=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
s=p.read_text()

def rep(old,new,n=1):
    global s
    assert old in s, old[:200]
    s=s.replace(old,new,n)

rep('String raw="catalog52842_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);',
    'String raw="catalog52844_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);')

rep(''' void loadShortsCategorySections(final int gen){
  final LinearLayout host=body;if(host==null)return;boolean any=false;JSONObject prepared=readHomeCache();JSONArray secs=prepared==null?null:prepared.optJSONArray("result");
  if(secs!=null){for(int i=0;i<secs.length();i++){JSONObject sec=secs.optJSONObject(i);if(sec==null||!isShortsSection(sec))continue;JSONArray data=sec.optJSONArray("data");if(data==null||data.length()==0)continue;final JSONObject fsec=sec;String title=cleanCategoryDisplayTitle(sec.optString("title","Reels Shorts"),1);sectionHeaderInto(host,title,()->openSection(fsec));posterRowInto(host,data);any=true;}}
  if(!any){TextView empty=t("Nenhum GreenShorts encontrado nesta fonte.",14);empty.setTextColor(0xff9da7a2);empty.setGravity(Gravity.CENTER);host.addView(empty,new LinearLayout.LayoutParams(-1,dp(72)));}
 }''',
''' JSONArray collectShortsLooseItems(JSONArray secs){JSONArray out=new JSONArray();java.util.HashSet<String> seen=new java.util.HashSet<>();if(secs==null)return out;for(int i=0;i<secs.length();i++){JSONObject sec=secs.optJSONObject(i);if(sec==null||!isShortsSection(sec))continue;JSONArray data=sec.optJSONArray("data");if(data==null)continue;for(int j=0;j<data.length();j++){JSONObject x=data.optJSONObject(j);if(x==null)continue;String k=itemKey(x);if(k==null||k.trim().isEmpty())k=x.optString("id",x.optString("video_id",x.optString("name","")))+"|"+x.optString("stream_url",x.optString("url",""));if(seen.add(k))out.put(x);}}return out;}
 void loadShortsCategorySections(final int gen){
  final LinearLayout host=body;if(host==null)return;JSONObject prepared=readHomeCache();JSONArray secs=prepared==null?null:prepared.optJSONArray("result");JSONArray loose=collectShortsLooseItems(secs);
  if(loose.length()>0){grid(loose);return;}
  TextView empty=t("Nenhum GreenShorts encontrado nesta fonte.",14);empty.setTextColor(0xff9da7a2);empty.setGravity(Gravity.CENTER);host.addView(empty,new LinearLayout.LayoutParams(-1,dp(72)));
 }''')

rep(''' boolean isShortsSection(JSONObject sec){if(sec==null)return false;return isShortsCategoryTitle(sec.optString("title",sec.optString("category_name",sec.optString("name",""))));}''',
''' boolean isShortsSection(JSONObject sec){if(sec==null)return false;return isShortsCategoryTitle(sec.optString("title",sec.optString("category_name",sec.optString("name",""))));}
 String greenShortsCoverCandidate(String raw){if(raw==null)return "";String v=raw.trim();if(v.isEmpty())return "";String s=v.toLowerCase(java.util.Locale.ROOT);String flat=s.replaceAll("[^a-z0-9]","");if(flat.contains("reelshort")||flat.contains("reelsshort")||flat.contains("reelshorttv")||flat.contains("shortslogo")||flat.contains("reelshortlogo"))return "";return v;}
 void loadGreenShortsCover(ImageView im,JSONObject x){if(im==null)return;im.setImageResource(R.drawable.greenshorts_fallback);if(x==null)return;Img.loadBest(im,greenShortsCoverCandidate(x.optString("thumbnail","")),greenShortsCoverCandidate(x.optString("portrait_img","")),greenShortsCoverCandidate(x.optString("image","")),greenShortsCoverCandidate(x.optString("poster","")),greenShortsCoverCandidate(x.optString("landscape","")),greenShortsCoverCandidate(x.optString("landscape_img","")),greenShortsCoverCandidate(x.optString("backdrop","")));}''')

rep('''FrameLayout poster=new FrameLayout(this);poster.setBackground(round(CARD,13));ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);if("Shorts".equals(activeHomeTab))im.setImageResource(R.drawable.top_shorts);Img.loadBest(im,use.optString("thumbnail",""),use.optString("portrait_img",""),use.optString("image",""),use.optString("poster",""),use.optString("landscape",""),use.optString("landscape_img",""),use.optString("backdrop",""));poster.addView(im,new FrameLayout.LayoutParams(-1,-1));''',
'''FrameLayout poster=new FrameLayout(this);poster.setBackground(round(CARD,13));ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,use);else Img.loadBest(im,use.optString("thumbnail",""),use.optString("portrait_img",""),use.optString("image",""),use.optString("poster",""),use.optString("landscape",""),use.optString("landscape_img",""),use.optString("backdrop",""));poster.addView(im,new FrameLayout.LayoutParams(-1,-1));''')

rep('''ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("landscape",""),x.optString("landscape_img",""));f.addView(im,new FrameLayout.LayoutParams(-1,-1));''',
'''ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,x);else Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("landscape",""),x.optString("landscape_img",""));f.addView(im,new FrameLayout.LayoutParams(-1,-1));''',1)

p.write_text(s)

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52842' in t and "versionName '5.28.42'" in t
t=t.replace('versionCode 52842','versionCode 52844',1).replace("versionName '5.28.42'","versionName '5.28.44'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52844.txt').write_text("""GreenPlay 5.28.44

- GreenShorts continua na barra superior.
- A aba continua automática por provedor: sem Shorts, ela fica oculta.
- Dentro de GreenShorts não há subcategorias; os conteúdos ficam soltos em uma única grade.
- Capas genéricas ReelShort/Reels Shorts são ignoradas.
- Sem capa válida, usa a arte GreenShorts enviada pelo usuário.
- Filmes, Séries, TV e demais áreas não foram alterados.
""")

out=p.read_text()
assert 'catalog52844_' in out
assert 'addHomeTopMediaTab(tabs,R.drawable.top_shorts,"Shorts",selected)' in out
assert 'collectShortsLooseItems' in out
assert 'loadGreenShortsCover' in out
assert 'R.drawable.greenshorts_fallback' in out
assert 'versionCode 52844' in b.read_text()
print('OK 5.28.44')
