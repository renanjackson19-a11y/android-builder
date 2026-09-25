from pathlib import Path

root=Path('work')
main=root/'app/src/main/java/fun/greenplay/app/MainActivity.java'
stories=root/'app/src/main/java/fun/greenplay/app/StoriesActivity.java'
yt=root/'app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java'
grad=root/'app/build.gradle'

s=main.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 got {n}')
    s=s.replace(old,new,1)

# 1) Home Doramas: usar primeiro a arte vertical e preencher o card inteiro.
one(
'''void loadGreenShortsCover(ImageView im,JSONObject x){if(im==null)return;im.setScaleType(ImageView.ScaleType.FIT_CENTER);im.setBackgroundColor(0xff090609);im.setImageResource(R.drawable.greenshorts_fallback);if(x==null)return;Img.loadBest(im,greenShortsCoverCandidate(x.optString("thumbnail","")),greenShortsCoverCandidate(x.optString("portrait_img","")),greenShortsCoverCandidate(x.optString("image","")),greenShortsCoverCandidate(x.optString("poster","")),greenShortsCoverCandidate(x.optString("landscape","")),greenShortsCoverCandidate(x.optString("landscape_img","")),greenShortsCoverCandidate(x.optString("backdrop","")));}''',
'''void loadGreenShortsCover(ImageView im,JSONObject x){if(im==null)return;im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setBackgroundColor(CARD);im.setImageResource(R.drawable.greenshorts_fallback);if(x==null)return;Img.loadBest(im,greenShortsCoverCandidate(x.optString("portrait_img","")),greenShortsCoverCandidate(x.optString("poster","")),greenShortsCoverCandidate(x.optString("image","")),greenShortsCoverCandidate(x.optString("thumbnail","")),greenShortsCoverCandidate(x.optString("landscape","")),greenShortsCoverCandidate(x.optString("landscape_img","")),greenShortsCoverCandidate(x.optString("backdrop","")));}''',
'home shorts portrait fill')

# 2) Tirar o botão/ícone de play sobre as capas dos Doramas na Home.
old_card='''LinearLayout card(JSONObject x){JSONObject merged=isYoutubeShort(x)?x:mergeDetailJson(x,readDetailCache(x));final JSONObject use=merged==null?x:merged;LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setPadding(dp(2),dp(2),dp(2),0);c.setFocusable(true);FrameLayout poster=new FrameLayout(this);poster.setBackground(round(CARD,13));ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,use);else Img.loadBest(im,use.optString("thumbnail",""),use.optString("portrait_img",""),use.optString("image",""),use.optString("poster",""),use.optString("landscape",""),use.optString("landscape_img",""),use.optString("backdrop",""));poster.addView(im,new FrameLayout.LayoutParams(-1,-1));TextView badge=t("▶",10);badge.setTextColor(Color.WHITE);badge.setGravity(Gravity.CENTER);badge.setBackground(round(0xaa000000,20));FrameLayout.LayoutParams bp=new FrameLayout.LayoutParams(dp(28),dp(28),Gravity.BOTTOM|Gravity.RIGHT);bp.setMargins(0,0,dp(7),dp(7));poster.addView(badge,bp);c.addView(poster,new LinearLayout.LayoutParams(-1,dp(158)));TextView n=t(use.optString("name",use.optString("title","")),13);n.setPadding(dp(2),dp(6),dp(2),0);n.setMaxLines(2);n.setEllipsize(android.text.TextUtils.TruncateAt.END);c.addView(n,new LinearLayout.LayoutParams(-1,dp(42)));c.setOnClickListener(v->details(use));c.setOnLongClickListener(v->{toggleFav(use);return true;});return c;}'''
new_card='''LinearLayout card(JSONObject x){JSONObject merged=isYoutubeShort(x)?x:mergeDetailJson(x,readDetailCache(x));final JSONObject use=merged==null?x:merged;LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setPadding(dp(2),dp(2),dp(2),0);c.setFocusable(true);FrameLayout poster=new FrameLayout(this);poster.setBackground(round(CARD,13));poster.setClipToOutline(true);ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,use);else Img.loadBest(im,use.optString("thumbnail",""),use.optString("portrait_img",""),use.optString("image",""),use.optString("poster",""),use.optString("landscape",""),use.optString("landscape_img",""),use.optString("backdrop",""));poster.addView(im,new FrameLayout.LayoutParams(-1,-1));if(!"Shorts".equals(activeHomeTab)){TextView badge=t("▶",10);badge.setTextColor(Color.WHITE);badge.setGravity(Gravity.CENTER);badge.setBackground(round(0xaa000000,20));FrameLayout.LayoutParams bp=new FrameLayout.LayoutParams(dp(28),dp(28),Gravity.BOTTOM|Gravity.RIGHT);bp.setMargins(0,0,dp(7),dp(7));poster.addView(badge,bp);}c.addView(poster,new LinearLayout.LayoutParams(-1,dp(158)));TextView n=t(use.optString("name",use.optString("title","")),13);n.setPadding(dp(2),dp(6),dp(2),0);n.setMaxLines(2);n.setEllipsize(android.text.TextUtils.TruncateAt.END);c.addView(n,new LinearLayout.LayoutParams(-1,dp(42)));c.setOnClickListener(v->details(use));c.setOnLongClickListener(v->{toggleFav(use);return true;});return c;}'''
one(old_card,new_card,'remove shorts play badge')

# 3) Pedir metadados/sinopse em português no enriquecimento.
one(
'''java.util.Map<String,String> doramaEnrichArgs(JSONObject source){if(source==null)return Api.m();String q=source.optString("original_title",source.optString("name",source.optString("title","")));return Api.m("title",q,"display_name",source.optString("name",source.optString("title","")),"thumbnail",source.optString("thumbnail",source.optString("portrait_img","")),"landscape",source.optString("landscape",source.optString("backdrop","")),"series_key",source.optString("series_key",""),"category_name",source.optString("category_name","Yelly Doramas"));}''',
'''java.util.Map<String,String> doramaEnrichArgs(JSONObject source){if(source==null)return Api.m();String q=source.optString("original_title",source.optString("name",source.optString("title","")));return Api.m("title",q,"display_name",source.optString("name",source.optString("title","")),"thumbnail",source.optString("thumbnail",source.optString("portrait_img","")),"landscape",source.optString("landscape",source.optString("backdrop","")),"series_key",source.optString("series_key",""),"category_name",source.optString("category_name","Yelly Doramas"),"language","pt-BR","lang","pt-BR","locale","pt-BR");}''',
'dorama enrichment pt-BR')

# 4) Guardar e priorizar campos portugueses quando o backend enviar.
one(
'''if(dst==null||src==null)return;String[] keys={"name","title","thumbnail","portrait_img","image","landscape","landscape_img","poster","backdrop","description","genre","category_name","rating","imdb_rating","tmdb_id","release_date"};''',
'''if(dst==null||src==null)return;String[] keys={"name","title","thumbnail","portrait_img","image","landscape","landscape_img","poster","backdrop","description_pt","overview_pt","synopsis_pt","sinopse","description","plot","overview","genre","category_name","rating","imdb_rating","tmdb_id","release_date"};''',
'copy portuguese detail fields')

anchor='''String detailValue(JSONObject d,String...keys){if(d==null)return "";for(String k:keys){String v=d.optString(k,"");if(v!=null&&!v.trim().isEmpty()&&!"null".equalsIgnoreCase(v.trim()))return v.trim();}return "";}'''
helper='''String detailValue(JSONObject d,String...keys){if(d==null)return "";for(String k:keys){String v=d.optString(k,"");if(v!=null&&!v.trim().isEmpty()&&!"null".equalsIgnoreCase(v.trim()))return v.trim();}return "";}
 String doramaDescriptionPt(JSONObject d){String pt=detailValue(d,"description_pt","overview_pt","synopsis_pt","sinopse","plot_pt","description_pt_br","overview_pt_br");if(!pt.isEmpty())return pt;String raw=detailValue(d,"description","plot","overview");if(raw.isEmpty())return "";String l=raw.toLowerCase(java.util.Locale.ROOT);int en=0,br=0;String[] ew={" the "," and "," with "," her "," his "," she "," he "," after "," when "," must "," their "," from "," into "," becomes "," discovers "," love "};for(String w:ew)if((" "+l+" ").contains(w))en++;String[] pw={" que "," com "," ela "," ele "," depois "," quando "," seu "," sua "," seus "," suas "," para "," uma "," um "," amor "," descobre "," precisa "," entre "};for(String w:pw)if((" "+l+" ").contains(w))br++;if(en>=3&&en>br+1)return "";return raw;}
 String cleanCastName(String raw){if(raw==null)return "";String n=raw.trim();n=n.replaceAll("(?i)\\\\s*[·•|/\\\\-–—]?\\\\s*\\\\(?\\\\d+\\\\s*(filmes?|movies?|obras?|t[ií]tulos?)\\\\)?\\\\s*$","").trim();return n;}'''
one(anchor,helper,'pt synopsis helper')

# 5) Sinopse: usar somente português quando disponível; nunca exibir fallback claramente inglês.
one(
'''boolean detailNeedsEnrich(JSONObject d){if(d==null)return true;if(isYoutubeShort(d)){String desc=detailValue(d,"description","plot","overview");return d.optInt("tmdb_enriched",0)!=1||desc.trim().isEmpty();}String desc=detailValue(d,"description","plot","overview"),genre=detailValue(d,"category_name","genre","genres"),rating=detailValue(d,"imdb_rating","rating","vote_average","score"),back=detailValue(d,"landscape","landscape_img","backdrop","backdrop_path");JSONArray cast=d.optJSONArray("cast_list");int vt=d.optInt("video_type",d.optInt("type_id",1));boolean series=vt==2||"series".equalsIgnoreCase(d.optString("type",""));if(series&&detailSeriesSeasons(d).length()==0)return true;return desc.isEmpty()||genre.isEmpty()||rating.isEmpty()||back.isEmpty()||cast==null||cast.length()==0;}''',
'''boolean detailNeedsEnrich(JSONObject d){if(d==null)return true;if(isYoutubeShort(d)){String desc=doramaDescriptionPt(d);return d.optInt("tmdb_enriched",0)!=1||desc.trim().isEmpty();}String desc=detailValue(d,"description","plot","overview"),genre=detailValue(d,"category_name","genre","genres"),rating=detailValue(d,"imdb_rating","rating","vote_average","score"),back=detailValue(d,"landscape","landscape_img","backdrop","backdrop_path");JSONArray cast=d.optJSONArray("cast_list");int vt=d.optInt("video_type",d.optInt("type_id",1));boolean series=vt==2||"series".equalsIgnoreCase(d.optString("type",""));if(series&&detailSeriesSeasons(d).length()==0)return true;return desc.isEmpty()||genre.isEmpty()||rating.isEmpty()||back.isEmpty()||cast==null||cast.length()==0;}''',
'detail enrichment requires pt synopsis')

one(
'''String desc=detailValue(d,"description","plot","overview");String date=detailValue(d,"release_date","date","first_air_date");String genre=detailValue(d,"category_name","genre","genres");String cast=detailValue(d,"cast");JSONArray castList=d.optJSONArray("cast_list");String dur=detailValue(d,"video_duration","duration","runtime");String rating=detailValue(d,"imdb_rating","rating","vote_average","score");final String displayTitle=tmdbTitle;''',
'''String desc=(isYoutubeShort(source)||isYoutubeShort(d))?doramaDescriptionPt(d):detailValue(d,"description","plot","overview");String date=detailValue(d,"release_date","date","first_air_date");String genre=detailValue(d,"category_name","genre","genres");String cast=detailValue(d,"cast");JSONArray castList=d.optJSONArray("cast_list");String dur=detailValue(d,"video_duration","duration","runtime");String rating=detailValue(d,"imdb_rating","rating","vote_average","score");final String displayTitle=tmdbTitle;''',
'details uses pt synopsis')

one(
'''String fullDesc=desc.isEmpty()?"Sinopse ainda não disponível.":desc;''',
'''String fullDesc=desc.isEmpty()?"Sinopse em português ainda não disponível.":desc;''',
'pt synopsis fallback')

# 6) Elenco: mostrar somente nome limpo, sem quantidade de filmes/obras.
one(
'''String name=ca.optString("name",ca.optString("original_name",""));''',
'''String name=cleanCastName(ca.optString("name",ca.optString("original_name","")));''',
'clean cast counts')

main.write_text(s,encoding='utf-8')

# 7) Stories: também pedir enriquecimento em pt-BR e cobrir a marca do YouTube.
st=stories.read_text(encoding='utf-8')
old='Api.post("dorama_enrich",Api.m("title",raw,"display_name",shown,"thumbnail",img,"landscape",land,"series_key",x.optString("series_key",""),"category_name","Yelly Doramas"),new Api.CB(){'
new='Api.post("dorama_enrich",Api.m("title",raw,"display_name",shown,"thumbnail",img,"landscape",land,"series_key",x.optString("series_key",""),"category_name","Yelly Doramas","language","pt-BR","lang","pt-BR","locale","pt-BR"),new Api.CB(){'
if st.count(old)!=1: raise SystemExit(f'stories pt-BR expected 1 got {st.count(old)}')
st=st.replace(old,new,1)
old='root.addView(web,new FrameLayout.LayoutParams(-1,-1));\n  shade=new View(this);'
new='root.addView(web,new FrameLayout.LayoutParams(-1,-1));\n  View ytBrandMask=new View(this);ytBrandMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(dp(136),dp(54),Gravity.RIGHT|Gravity.BOTTOM);ybm.setMargins(0,0,dp(2),dp(2));root.addView(ytBrandMask,ybm);\n  shade=new View(this);'
if st.count(old)!=1: raise SystemExit(f'stories youtube mask expected 1 got {st.count(old)}')
st=st.replace(old,new,1)
stories.write_text(st,encoding='utf-8')

# 8) Player completo: manter os controles Yelly e cobrir a marca do YouTube.
ys=yt.read_text(encoding='utf-8')
old='root.addView(web,new FrameLayout.LayoutParams(-1,-1));\n\n        if(!tvMode){'
new='root.addView(web,new FrameLayout.LayoutParams(-1,-1));\n        View ytBrandMask=new View(this);ytBrandMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(dp(148),dp(58),Gravity.RIGHT|Gravity.BOTTOM);ybm.setMargins(0,0,dp(2),dp(2));root.addView(ytBrandMask,ybm);\n\n        if(!tvMode){'
if ys.count(old)!=1: raise SystemExit(f'player youtube mask expected 1 got {ys.count(old)}')
ys=ys.replace(old,new,1)
yt.write_text(ys,encoding='utf-8')

g=grad.read_text(encoding='utf-8')
if "versionCode 10006" not in g or "versionName '1.0.6'" not in g:
    raise SystemExit('expected 1.0.6 corrected base')
g=g.replace('versionCode 10006','versionCode 10007',1).replace("versionName '1.0.6'","versionName '1.0.7'",1)
grad.write_text(g,encoding='utf-8')

(root/'app/RELEASE_NOTES.txt').write_text('''Yelly Doramas 1.0.7
Home: capas dos Doramas voltam a preencher o card vertical inteiro, priorizando portrait_img/poster e sem faixas pretas no meio.
Removido o ícone de play sobre as capas dos Doramas na Home.
Detalhes: enriquecimento passa a solicitar pt-BR e prioriza description_pt/overview_pt/synopsis_pt/sinopse.
Sinopse claramente em inglês não é mais exibida como fallback; o app aguarda português ou informa indisponibilidade.
Elenco: nomes limpos, sem quantidade de filmes/obras anexada ao ator.
Stories também solicitam pt-BR. A marca visual do YouTube fica coberta nos Stories e no player completo, mantendo os controles próprios do Yelly.
Mantidos Stories, swipe, catálogo completo, comentários, favoritos, login, identidade do painel e paleta Yelly.
''',encoding='utf-8')
print('YELLY_107_PATCH_OK')
