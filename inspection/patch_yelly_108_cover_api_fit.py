from pathlib import Path

root=Path('work')
main=root/'app/src/main/java/fun/greenplay/app/MainActivity.java'
grad=root/'app/build.gradle'

s=main.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 got {n}')
    s=s.replace(old,new,1)

# 1) Usar também a capa vertical enriquecida pela API/TMDB e não forçar CENTER_CROP
# em todo lugar. Cada tela escolhe seu ScaleType.
old='''String greenShortsCoverCandidate(String raw){if(raw==null)return "";String v=raw.trim();if(v.isEmpty())return "";String s=v.toLowerCase(java.util.Locale.ROOT);String flat=s.replaceAll("[^a-z0-9]","");if(flat.contains("reelshort")||flat.contains("reelsshort")||flat.contains("reelshorttv")||flat.contains("shortslogo")||flat.contains("reelshortlogo"))return "";return v;}
 void loadGreenShortsCover(ImageView im,JSONObject x){if(im==null)return;im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setBackgroundColor(CARD);im.setImageResource(R.drawable.greenshorts_fallback);if(x==null)return;Img.loadBest(im,greenShortsCoverCandidate(x.optString("portrait_img","")),greenShortsCoverCandidate(x.optString("poster","")),greenShortsCoverCandidate(x.optString("image","")),greenShortsCoverCandidate(x.optString("thumbnail","")),greenShortsCoverCandidate(x.optString("landscape","")),greenShortsCoverCandidate(x.optString("landscape_img","")),greenShortsCoverCandidate(x.optString("backdrop","")));}'''
new='''String greenShortsCoverCandidate(String raw){if(raw==null)return "";String v=raw.trim();if(v.isEmpty())return "";String s=v.toLowerCase(java.util.Locale.ROOT);String flat=s.replaceAll("[^a-z0-9]","");if(flat.contains("reelshort")||flat.contains("reelsshort")||flat.contains("reelshorttv")||flat.contains("shortslogo")||flat.contains("reelshortlogo"))return "";return v;}
 String greenShortsTmdbPoster(JSONObject x){if(x==null)return "";String p=greenShortsCoverCandidate(x.optString("poster_path",x.optString("tmdb_poster_path","")));if(p.isEmpty())return "";if(p.startsWith("/"))return "https://image.tmdb.org/t/p/w500"+p;return p;}
 void loadGreenShortsCover(ImageView im,JSONObject x){if(im==null)return;im.setBackgroundColor(CARD);im.setImageResource(R.drawable.greenshorts_fallback);if(x==null)return;Img.loadBest(im,greenShortsCoverCandidate(x.optString("portrait_img","")),greenShortsCoverCandidate(x.optString("poster","")),greenShortsCoverCandidate(x.optString("cover","")),greenShortsCoverCandidate(x.optString("cover_image","")),greenShortsTmdbPoster(x),greenShortsCoverCandidate(x.optString("image","")),greenShortsCoverCandidate(x.optString("thumbnail","")),greenShortsCoverCandidate(x.optString("landscape","")),greenShortsCoverCandidate(x.optString("landscape_img","")),greenShortsCoverCandidate(x.optString("backdrop","")));}
 void renderGreenShortCardPoster(FrameLayout poster,JSONObject x){if(poster==null)return;poster.removeAllViews();ImageView fill=new ImageView(this);fill.setScaleType(ImageView.ScaleType.CENTER_CROP);fill.setAlpha(.48f);loadGreenShortsCover(fill,x);poster.addView(fill,new FrameLayout.LayoutParams(-1,-1));View dim=new View(this);dim.setBackgroundColor(0x22000000);poster.addView(dim,new FrameLayout.LayoutParams(-1,-1));ImageView full=new ImageView(this);full.setScaleType(ImageView.ScaleType.FIT_CENTER);loadGreenShortsCover(full,x);full.setBackgroundColor(Color.TRANSPARENT);poster.addView(full,new FrameLayout.LayoutParams(-1,-1));}
 void refreshVisibleGreenShortCard(JSONObject source){if(source==null||!"Shorts".equals(activeHomeTab))return;String key="yelly_short|"+detailCacheKey(source);JSONObject merged=mergeDetailJson(source,readDetailCache(source));if(merged==null)merged=source;GridLayout[] grids={mobileCategoryGrid,tvShortsGrid};for(GridLayout g:grids){if(g==null)continue;for(int i=0;i<g.getChildCount();i++){View child=g.getChildAt(i);if(!(child instanceof LinearLayout))continue;Object tag=child.getTag();if(tag==null||!key.equals(String.valueOf(tag)))continue;LinearLayout c=(LinearLayout)child;if(c.getChildCount()<1||!(c.getChildAt(0) instanceof FrameLayout))continue;renderGreenShortCardPoster((FrameLayout)c.getChildAt(0),merged);}}}'''
one(old,new,'short cover helpers')

# 2) Home: usar o cache enriquecido da API também nos Doramas e renderizar
# a capa completa por cima de um fundo preenchido. Assim a arte não fica com
# faixa preta e o nome que já vem dentro da imagem não é cortado.
old='''LinearLayout card(JSONObject x){JSONObject merged=isYoutubeShort(x)?x:mergeDetailJson(x,readDetailCache(x));final JSONObject use=merged==null?x:merged;LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setPadding(dp(2),dp(2),dp(2),0);c.setFocusable(true);FrameLayout poster=new FrameLayout(this);poster.setBackground(round(CARD,13));poster.setClipToOutline(true);ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,use);else Img.loadBest(im,use.optString("thumbnail",""),use.optString("portrait_img",""),use.optString("image",""),use.optString("poster",""),use.optString("landscape",""),use.optString("landscape_img",""),use.optString("backdrop",""));poster.addView(im,new FrameLayout.LayoutParams(-1,-1));if(!"Shorts".equals(activeHomeTab)){TextView badge=t("▶",10);badge.setTextColor(Color.WHITE);badge.setGravity(Gravity.CENTER);badge.setBackground(round(0xaa000000,20));FrameLayout.LayoutParams bp=new FrameLayout.LayoutParams(dp(28),dp(28),Gravity.BOTTOM|Gravity.RIGHT);bp.setMargins(0,0,dp(7),dp(7));poster.addView(badge,bp);}c.addView(poster,new LinearLayout.LayoutParams(-1,dp(158)));TextView n=t(use.optString("name",use.optString("title","")),13);n.setPadding(dp(2),dp(6),dp(2),0);n.setMaxLines(2);n.setEllipsize(android.text.TextUtils.TruncateAt.END);c.addView(n,new LinearLayout.LayoutParams(-1,dp(42)));c.setOnClickListener(v->details(use));c.setOnLongClickListener(v->{toggleFav(use);return true;});return c;}'''
new='''LinearLayout card(JSONObject x){JSONObject merged=mergeDetailJson(x,readDetailCache(x));final JSONObject use=merged==null?x:merged;LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setPadding(dp(2),dp(2),dp(2),0);c.setFocusable(true);FrameLayout poster=new FrameLayout(this);poster.setBackground(round(CARD,13));poster.setClipToOutline(true);boolean yellyShort="Shorts".equals(activeHomeTab);if(yellyShort){c.setTag("yelly_short|"+detailCacheKey(x));renderGreenShortCardPoster(poster,use);}else{ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);Img.loadBest(im,use.optString("thumbnail",""),use.optString("portrait_img",""),use.optString("image",""),use.optString("poster",""),use.optString("landscape",""),use.optString("landscape_img",""),use.optString("backdrop",""));poster.addView(im,new FrameLayout.LayoutParams(-1,-1));TextView badge=t("▶",10);badge.setTextColor(Color.WHITE);badge.setGravity(Gravity.CENTER);badge.setBackground(round(0xaa000000,20));FrameLayout.LayoutParams bp=new FrameLayout.LayoutParams(dp(28),dp(28),Gravity.BOTTOM|Gravity.RIGHT);bp.setMargins(0,0,dp(7),dp(7));poster.addView(badge,bp);}int baseW=mobileCategoryCardW>0?mobileCategoryCardW:dp(112);int posterH=yellyShort?(wideTvUi()?Math.max(dp(186),(int)(baseW*1.42f)):Math.max(dp(168),(int)(baseW*1.50f))):dp(158);c.addView(poster,new LinearLayout.LayoutParams(-1,posterH));TextView n=t(use.optString("name",use.optString("title","")),13);n.setPadding(dp(2),dp(6),dp(2),0);n.setMaxLines(2);n.setEllipsize(android.text.TextUtils.TruncateAt.END);c.addView(n,new LinearLayout.LayoutParams(-1,dp(42)));c.setOnClickListener(v->details(use));c.setOnLongClickListener(v->{toggleFav(use);return true;});return c;}'''
one(old,new,'home dorama card')

# 3) Altura da grade acompanha a proporção vertical da capa.
old='''int start=mobileCategoryNextIndex,len=mobileCategoryRows.length(),end=Math.min(len,start+48),h=dp(196);'''
new='''int start=mobileCategoryNextIndex,len=mobileCategoryRows.length(),end=Math.min(len,start+48),h="Shorts".equals(activeHomeTab)?Math.max(dp(214),(int)(mobileCategoryCardW*1.50f)+dp(46)):dp(196);'''
one(old,new,'mobile shorts row height')

old='''if(gen!=viewGen||g==null||g.getParent()==null)return;int end=Math.min(a.length(),start+(wideTvUi()?24:12));int h=wideTvUi()?dp(246):dp(196);'''
new='''if(gen!=viewGen||g==null||g.getParent()==null)return;int end=Math.min(a.length(),start+(wideTvUi()?24:12));int h="Shorts".equals(activeHomeTab)?Math.max(dp(252),(int)(w*1.42f)+dp(48)):(wideTvUi()?dp(246):dp(196));'''
one(old,new,'tv shorts row height')

# 4) Quando o enriquecimento da API terminar, atualizar imediatamente a capa
# visível para usar o poster vertical retornado, sem precisar fechar/reabrir.
old='''public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d!=null)saveDetailCache(x,d);finishDetailPrefetch(key);}'''
new='''public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d!=null){saveDetailCache(x,d);if(isYoutubeShort(x))refreshVisibleGreenShortCard(x);}finishDetailPrefetch(key);}'''
one(old,new,'refresh enriched short cover')

main.write_text(s,encoding='utf-8')

g=grad.read_text(encoding='utf-8')
if "versionCode 10007" not in g or "versionName '1.0.7'" not in g:
    raise SystemExit('expected Yelly 1.0.7 base')
g=g.replace('versionCode 10007','versionCode 10008',1).replace("versionName '1.0.7'","versionName '1.0.8'",1)
grad.write_text(g,encoding='utf-8')

(root/'app/RELEASE_NOTES.txt').write_text('''Yelly Doramas 1.0.8
Home Doramas: corrigido corte do texto que já faz parte da arte da capa.
Os cards agora usam a imagem inteira em FIT_CENTER sobre um fundo preenchido com a própria capa, evitando faixas pretas e mantendo o card cheio.
A grade usa proporção vertical maior para combinar melhor com posters de Doramas.
A Home agora aproveita o cache enriquecido da API também nos Doramas, em vez de ignorá-lo.
Capa da API/TMDB: prioridade para portrait_img, poster, cover e poster_path; poster_path relativo do TMDB é convertido para imagem w500.
Quando dorama_enrich termina, a capa visível é atualizada na hora.
Mantidas as correções da 1.0.7: sinopse pt-BR, elenco sem quantidade de filmes, Stories e identidade Yelly.
''',encoding='utf-8')
print('YELLY_108_PATCH_OK')
