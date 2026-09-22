from pathlib import Path
p=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
s=p.read_text()

def rep(old,new,n=1):
    global s
    assert old in s, old[:180]
    s=s.replace(old,new,n)

rep('String raw="catalog52842_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);',
    'String raw="catalog52843_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);')

rep('''  addHomeTopMediaTab(tabs,R.drawable.top_series,"Séries",selected);
  if(currentProviderHasShorts())addHomeTopMediaTab(tabs,R.drawable.top_shorts,"Shorts",selected);''',
    '''  addHomeTopMediaTab(tabs,R.drawable.top_series,"Séries",selected);''')

rep('''   final LinearLayout movieHost=new LinearLayout(MainActivity.this);movieHost.setOrientation(LinearLayout.VERTICAL);body.addView(movieHost,new LinearLayout.LayoutParams(-1,-2));
   final LinearLayout seriesHost=new LinearLayout(MainActivity.this);seriesHost.setOrientation(LinearLayout.VERTICAL);body.addView(seriesHost,new LinearLayout.LayoutParams(-1,-2));
   final LinearLayout otherHost=new LinearLayout(MainActivity.this);otherHost.setOrientation(LinearLayout.VERTICAL);body.addView(otherHost,new LinearLayout.LayoutParams(-1,-2));''',
'''   final LinearLayout shortsHost=new LinearLayout(MainActivity.this);shortsHost.setOrientation(LinearLayout.VERTICAL);body.addView(shortsHost,new LinearLayout.LayoutParams(-1,-2));
   final LinearLayout movieHost=new LinearLayout(MainActivity.this);movieHost.setOrientation(LinearLayout.VERTICAL);body.addView(movieHost,new LinearLayout.LayoutParams(-1,-2));
   final LinearLayout seriesHost=new LinearLayout(MainActivity.this);seriesHost.setOrientation(LinearLayout.VERTICAL);body.addView(seriesHost,new LinearLayout.LayoutParams(-1,-2));
   final LinearLayout otherHost=new LinearLayout(MainActivity.this);otherHost.setOrientation(LinearLayout.VERTICAL);body.addView(otherHost,new LinearLayout.LayoutParams(-1,-2));''')

rep('''   renderHomeSectionsChunked(sections,1,movieHost,gen,0);
   renderHomeSectionsChunked(sections,2,seriesHost,gen,0);
   renderHomeOtherSectionsChunked(sections,otherHost,gen,0);''',
'''   renderGreenShortsLooseSection(sections,shortsHost,gen);
   renderHomeSectionsChunked(sections,1,movieHost,gen,0);
   renderHomeSectionsChunked(sections,2,seriesHost,gen,0);
   renderHomeOtherSectionsChunked(sections,otherHost,gen,0);''')

needle=''' void renderHomeSectionsChunked(JSONArray sections,int wanted,LinearLayout target,int gen,int start){'''
insert=''' JSONArray collectGreenShortsLoose(JSONArray sections){JSONArray out=new JSONArray();java.util.HashSet<String> seen=new java.util.HashSet<>();if(sections==null)return out;for(int i=0;i<sections.length();i++){JSONObject sec=sections.optJSONObject(i);if(sec==null||!isShortsSection(sec))continue;JSONArray data=sec.optJSONArray("data");if(data==null)continue;for(int j=0;j<data.length();j++){JSONObject x=data.optJSONObject(j);if(x==null)continue;String k=itemKey(x);if(k==null||k.trim().isEmpty())k=x.optString("id",x.optString("video_id",x.optString("name","")))+"|"+x.optString("stream_url",x.optString("url",""));if(seen.add(k))out.put(x);}}return out;}
 void renderGreenShortsLooseSection(JSONArray sections,LinearLayout host,int gen){if((gen!=viewGen&&!cachedHomeHostValid(host))||host==null||host.getParent()==null)return;JSONArray rows=collectGreenShortsLoose(sections);if(rows.length()==0){host.setVisibility(View.GONE);return;}host.setVisibility(View.VISIBLE);LinearLayout h=new LinearLayout(this);h.setGravity(Gravity.CENTER_VERTICAL);h.setPadding(dp(2),dp(6),0,dp(1));TextView title=t("GreenShorts",18);title.setTypeface(null,1);h.addView(title,new LinearLayout.LayoutParams(-1,dp(44)));host.addView(h);greenShortsLooseRowInto(host,rows);}
 void greenShortsLooseRowInto(LinearLayout host,JSONArray a){if(host==null||a==null||a.length()==0)return;if(wideTvUi()){HorizontalScrollView hs=new HorizontalScrollView(this);hs.setHorizontalScrollBarEnabled(false);LinearLayout r=new LinearLayout(this);r.setOrientation(LinearLayout.HORIZONTAL);r.setPadding(dp(2),0,dp(10),0);int w=Math.max(dp(136),Math.min(dp(160),(getResources().getDisplayMetrics().widthPixels-dp(110))/Math.max(6,Math.min(8,screenWidthDp()/165))));int imageH=(int)(w*1.42f);for(int i=0;i<a.length();i++){JSONObject source=a.optJSONObject(i);if(source==null)continue;JSONObject x=mergeDetailJson(source,readDetailCache(source));if(x==null)x=source;final JSONObject clickItem=source;LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setFocusable(true);ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setBackground(round(CARD,12));im.setClipToOutline(true);im.setImageResource(R.drawable.greenshorts_fallback);Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("poster",""),x.optString("landscape",""),x.optString("landscape_img",""));c.addView(im,new LinearLayout.LayoutParams(-1,imageH));TextView n=t(x.optString("name",x.optString("title","")),13);n.setMaxLines(1);n.setEllipsize(android.text.TextUtils.TruncateAt.END);n.setPadding(dp(2),dp(6),dp(2),0);c.addView(n,new LinearLayout.LayoutParams(-1,dp(34)));c.setOnClickListener(v->details(clickItem));LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(w,imageH+dp(38));cp.setMargins(0,0,dp(14),0);r.addView(c,cp);}hs.addView(r);host.addView(hs,new LinearLayout.LayoutParams(-1,imageH+dp(44)));return;}HorizontalScrollView hs=new HorizontalScrollView(this);hs.setHorizontalScrollBarEnabled(false);LinearLayout r=new LinearLayout(this);r.setOrientation(LinearLayout.HORIZONTAL);for(int i=0;i<a.length();i++){JSONObject source=a.optJSONObject(i);if(source==null)continue;JSONObject x=mergeDetailJson(source,readDetailCache(source));if(x==null)x=source;final JSONObject clickItem=source;LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setBackground(round(CARD,15));im.setClipToOutline(true);im.setImageResource(R.drawable.greenshorts_fallback);Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("poster",""),x.optString("landscape",""),x.optString("landscape_img",""));c.addView(im,new LinearLayout.LayoutParams(-1,dp(150)));TextView n=t(x.optString("name",x.optString("title","")),12);n.setMaxLines(2);n.setEllipsize(android.text.TextUtils.TruncateAt.END);n.setPadding(dp(3),dp(5),dp(3),0);c.addView(n,new LinearLayout.LayoutParams(-1,dp(40)));c.setOnClickListener(v->details(clickItem));LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(dp(104),dp(194));cp.setMargins(dp(3),0,dp(8),0);r.addView(c,cp);}hs.addView(r);host.addView(hs,new LinearLayout.LayoutParams(-1,dp(198)));}
 void renderHomeSectionsChunked(JSONArray sections,int wanted,LinearLayout target,int gen,int start){'''
rep(needle,insert)

# Fallback antigo só existia porque GreenShorts era aba. Agora só a seção GreenShorts usa o fallback enviado.
rep('if("Shorts".equals(activeHomeTab))im.setImageResource(R.drawable.top_shorts);','',2)

p.write_text(s)

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52842' in t and "versionName '5.28.42'" in t
t=t.replace('versionCode 52842','versionCode 52843',1).replace("versionName '5.28.42'","versionName '5.28.43'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52843.txt').write_text("""GreenPlay 5.28.43

- Altera somente GreenShorts na interface.
- GreenShorts removido da barra superior.
- GreenShorts aparece como uma única seção solta na Home quando o provedor possui esse conteúdo.
- Sem subcategorias internas e sem seta para outra categoria.
- Conteúdos ReelShort/Reels Shorts/GreenShorts são agregados numa única fileira.
- Usa a arte enviada pelo usuário como fallback quando a capa real não existe ou falha.
- Filmes, Séries, TV e demais áreas não foram alterados.
""")

out=p.read_text()
assert 'catalog52843_' in out
assert 'addHomeTopMediaTab(tabs,R.drawable.top_shorts' not in out
assert 'renderGreenShortsLooseSection' in out
assert 'R.drawable.greenshorts_fallback' in out
assert 'versionCode 52843' in b.read_text()
print('OK 5.28.43')
