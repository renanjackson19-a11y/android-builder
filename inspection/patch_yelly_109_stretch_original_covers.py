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

# Home Yelly: usar SOMENTE a arte original do catálogo para a capa.
# O enriquecimento continua valendo para título/sinopse/detalhes, mas não
# pode trocar a capa da Home por um poster de TMDB associado incorretamente.
one(
'''void loadGreenShortsCover(ImageView im,JSONObject x){if(im==null)return;im.setBackgroundColor(CARD);im.setImageResource(R.drawable.greenshorts_fallback);if(x==null)return;Img.loadBest(im,greenShortsCoverCandidate(x.optString("portrait_img","")),greenShortsCoverCandidate(x.optString("poster","")),greenShortsCoverCandidate(x.optString("cover","")),greenShortsCoverCandidate(x.optString("cover_image","")),greenShortsTmdbPoster(x),greenShortsCoverCandidate(x.optString("image","")),greenShortsCoverCandidate(x.optString("thumbnail","")),greenShortsCoverCandidate(x.optString("landscape","")),greenShortsCoverCandidate(x.optString("landscape_img","")),greenShortsCoverCandidate(x.optString("backdrop","")));}''',
'''void loadGreenShortsCover(ImageView im,JSONObject x){if(im==null)return;im.setBackgroundColor(CARD);im.setImageResource(R.drawable.greenshorts_fallback);if(x==null)return;Img.loadBest(im,greenShortsCoverCandidate(x.optString("portrait_img","")),greenShortsCoverCandidate(x.optString("poster","")),greenShortsCoverCandidate(x.optString("image","")),greenShortsCoverCandidate(x.optString("thumbnail","")),greenShortsCoverCandidate(x.optString("landscape","")),greenShortsCoverCandidate(x.optString("landscape_img","")),greenShortsCoverCandidate(x.optString("backdrop","")));}''',
'catalog cover only')

# Sem imagem duplicada no meio, sem blur/fundo e sem FIT_CENTER.
# A capa é esticada exatamente até as quatro bordas do card.
one(
'''void renderGreenShortCardPoster(FrameLayout poster,JSONObject x){if(poster==null)return;poster.removeAllViews();ImageView fill=new ImageView(this);fill.setScaleType(ImageView.ScaleType.CENTER_CROP);fill.setAlpha(.48f);loadGreenShortsCover(fill,x);poster.addView(fill,new FrameLayout.LayoutParams(-1,-1));View dim=new View(this);dim.setBackgroundColor(0x22000000);poster.addView(dim,new FrameLayout.LayoutParams(-1,-1));ImageView full=new ImageView(this);full.setScaleType(ImageView.ScaleType.FIT_CENTER);loadGreenShortsCover(full,x);full.setBackgroundColor(Color.TRANSPARENT);poster.addView(full,new FrameLayout.LayoutParams(-1,-1));}''',
'''void renderGreenShortCardPoster(FrameLayout poster,JSONObject x){if(poster==null)return;poster.removeAllViews();ImageView cover=new ImageView(this);cover.setScaleType(ImageView.ScaleType.FIT_XY);cover.setBackgroundColor(CARD);loadGreenShortsCover(cover,x);poster.addView(cover,new FrameLayout.LayoutParams(-1,-1));}''',
'stretch full card')

# Se chegar enriquecimento, não substituir a arte original do catálogo.
one(
'''void refreshVisibleGreenShortCard(JSONObject source){if(source==null||!"Shorts".equals(activeHomeTab))return;String key="yelly_short|"+detailCacheKey(source);JSONObject merged=mergeDetailJson(source,readDetailCache(source));if(merged==null)merged=source;GridLayout[] grids={mobileCategoryGrid,tvShortsGrid};for(GridLayout g:grids){if(g==null)continue;for(int i=0;i<g.getChildCount();i++){View child=g.getChildAt(i);if(!(child instanceof LinearLayout))continue;Object tag=child.getTag();if(tag==null||!key.equals(String.valueOf(tag)))continue;LinearLayout c=(LinearLayout)child;if(c.getChildCount()<1||!(c.getChildAt(0) instanceof FrameLayout))continue;renderGreenShortCardPoster((FrameLayout)c.getChildAt(0),merged);}}}''',
'''void refreshVisibleGreenShortCard(JSONObject source){if(source==null||!"Shorts".equals(activeHomeTab))return;String key="yelly_short|"+detailCacheKey(source);GridLayout[] grids={mobileCategoryGrid,tvShortsGrid};for(GridLayout g:grids){if(g==null)continue;for(int i=0;i<g.getChildCount();i++){View child=g.getChildAt(i);if(!(child instanceof LinearLayout))continue;Object tag=child.getTag();if(tag==null||!key.equals(String.valueOf(tag)))continue;LinearLayout c=(LinearLayout)child;if(c.getChildCount()<1||!(c.getChildAt(0) instanceof FrameLayout))continue;renderGreenShortCardPoster((FrameLayout)c.getChildAt(0),source);}}}''',
'do not replace home cover from enrich')

# Grid principal: capa original do catálogo, não o objeto enriquecido.
one(
'''if(yellyShort){c.setTag("yelly_short|"+detailCacheKey(x));renderGreenShortCardPoster(poster,use);}else{''',
'''if(yellyShort){c.setTag("yelly_short|"+detailCacheKey(x));renderGreenShortCardPoster(poster,x);}else{''',
'grid original cover')

# Abrir mais as laterais no celular para os 3 cards ocuparem melhor a largura.
one(
'''else usable=getResources().getDisplayMetrics().widthPixels-dp(52);int w=Math.max(dp(112),usable/cols);int gen=viewGen;''',
'''else usable=getResources().getDisplayMetrics().widthPixels-dp("Shorts".equals(activeHomeTab)?34:52);int w=Math.max(dp(112),usable/cols);int gen=viewGen;''',
'wider shorts grid')

one(
'''GridLayout.LayoutParams lp=new GridLayout.LayoutParams();lp.width=mobileCategoryCardW;lp.height=h;lp.setMargins(dp(4),dp(5),dp(6),dp(9));mobileCategoryGrid.addView(c,lp);''',
'''GridLayout.LayoutParams lp=new GridLayout.LayoutParams();lp.width=mobileCategoryCardW;lp.height=h;if("Shorts".equals(activeHomeTab))lp.setMargins(dp(2),dp(5),dp(2),dp(9));else lp.setMargins(dp(4),dp(5),dp(6),dp(9));mobileCategoryGrid.addView(c,lp);''',
'less side gaps')

# Carrossel e fileira de Doramas: mesma regra, preencher todo o retângulo
# usando a arte ORIGINAL do catálogo.
one(
'''ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,x);else Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("landscape",""),x.optString("landscape_img",""));f.addView(im,new FrameLayout.LayoutParams(-1,-1));''',
'''ImageView im=new ImageView(this);im.setScaleType("Shorts".equals(activeHomeTab)?ImageView.ScaleType.FIT_XY:ImageView.ScaleType.CENTER_CROP);if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,x);else Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("landscape",""),x.optString("landscape_img",""));f.addView(im,new FrameLayout.LayoutParams(-1,-1));''',
'feature stretch')

old='''ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setBackground(round(CARD,15));im.setClipToOutline(true);if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,x);else Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("landscape",""),x.optString("landscape_img",""));'''
new='''ImageView im=new ImageView(this);im.setScaleType("Shorts".equals(activeHomeTab)?ImageView.ScaleType.FIT_XY:ImageView.ScaleType.CENTER_CROP);im.setBackground(round(CARD,15));im.setClipToOutline(true);if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,source);else Img.loadBest(im,x.optString("thumbnail",""),x.optString("portrait_img",""),x.optString("image",""),x.optString("landscape",""),x.optString("landscape_img",""));'''
one(old,new,'poster row stretch and original cover')

main.write_text(s,encoding='utf-8')

g=grad.read_text(encoding='utf-8')
if "versionCode 10008" not in g or "versionName '1.0.8'" not in g:
    raise SystemExit('expected 1.0.8 base')
g=g.replace('versionCode 10008','versionCode 10009',1).replace("versionName '1.0.8'","versionName '1.0.9'",1)
grad.write_text(g,encoding='utf-8')

(root/'app/RELEASE_NOTES.txt').write_text('''Yelly Doramas 1.0.9
Home: removido o efeito de capa duplicada no meio do card.
A capa agora é uma única imagem esticada com FIT_XY até esquerda, direita, topo e base do card.
A Home não usa mais poster do enriquecimento/TMDB para substituir a capa do catálogo, evitando capas erradas como Mondo Vino em Doramas diferentes.
O enriquecimento continua sendo usado para títulos, sinopse e detalhes em português.
Grid de 3 colunas com laterais mais ajustadas e menos espaço entre os cards.
Carrossel e fileiras de Doramas seguem a mesma regra de preenchimento integral da capa.
''',encoding='utf-8')
print('YELLY_109_PATCH_OK')
