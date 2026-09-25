from pathlib import Path

root=Path('work')
stories=root/'app/src/main/java/fun/greenplay/app/StoriesActivity.java'
yt=root/'app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java'
grad=root/'app/build.gradle'

s=stories.read_text(encoding='utf-8')

def one(text,old,new,label):
    n=text.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 got {n}')
    return text.replace(old,new,1)

# Campos para usar a capa do próprio filme nas áreas antes pretas.
s=one(s,
'FrameLayout root;WebView web;ImageView poster;View shade,swipe;LinearLayout info,actions;',
'FrameLayout root;WebView web;ImageView poster,topCoverMask,bottomCoverMask;View shade,swipe;LinearLayout info,actions;',
'story cover mask fields')

# O WebView fica invisível durante a troca até o novo vídeo estar pronto.
s=one(s,
'''web.setWebChromeClient(new WebChromeClient());web.setWebViewClient(new WebViewClient());try{web.setLayerType(View.LAYER_TYPE_HARDWARE,null);}catch(Exception ignored){}root.addView(web,new FrameLayout.LayoutParams(-1,-1));
  if(!tvMode){View ytTopMask=new View(this);ytTopMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ytm=new FrameLayout.LayoutParams(-1,dp(86),Gravity.TOP);root.addView(ytTopMask,ytm);View ytBottomMask=new View(this);ytBottomMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(-1,dp(108),Gravity.BOTTOM);root.addView(ytBottomMask,ybm);}''',
'''web.setWebChromeClient(new WebChromeClient());web.setWebViewClient(new WebViewClient());web.addJavascriptInterface(new Object(){@android.webkit.JavascriptInterface public void ready(){runOnUiThread(()->{if(web!=null&&!dragging&&!swipeAnimating){web.setTranslationY(0f);web.animate().alpha(1f).setDuration(110).start();}});}},"StoryBridge");try{web.setLayerType(View.LAYER_TYPE_HARDWARE,null);}catch(Exception ignored){}root.addView(web,new FrameLayout.LayoutParams(-1,-1));
  if(!tvMode){topCoverMask=new ImageView(this);topCoverMask.setScaleType(ImageView.ScaleType.CENTER_CROP);topCoverMask.setBackgroundColor(Color.BLACK);topCoverMask.setAlpha(.82f);FrameLayout.LayoutParams ytm=new FrameLayout.LayoutParams(-1,dp(86),Gravity.TOP);root.addView(topCoverMask,ytm);bottomCoverMask=new ImageView(this);bottomCoverMask.setScaleType(ImageView.ScaleType.CENTER_CROP);bottomCoverMask.setBackgroundColor(Color.BLACK);bottomCoverMask.setAlpha(.82f);FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(-1,dp(108),Gravity.BOTTOM);root.addView(bottomCoverMask,ybm);}''',
'story poster masks and ready bridge')

# Swipe: não arrastar o WebView do YouTube. Isso era o que fazia aparecer um flash
# do vídeo anterior. Durante o gesto mostramos a capa e os elementos Yelly.
s=one(s,
'''void setSwipeOffset(float y){float lim=Math.max(1,root.getHeight());float v=Math.max(-lim,Math.min(lim,y));if(poster!=null)poster.setTranslationY(v);if(web!=null)web.setTranslationY(v);if(shade!=null)shade.setTranslationY(v);if(info!=null)info.setTranslationY(v);if(actions!=null)actions.setTranslationY(v);}''',
'''void setSwipeOffset(float y){float lim=Math.max(1,root.getHeight());float v=Math.max(-lim,Math.min(lim,y));if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(poster!=null)poster.setTranslationY(v);if(shade!=null)shade.setTranslationY(v);if(info!=null)info.setTranslationY(v);if(actions!=null)actions.setTranslationY(v);}''',
'hide web while swiping')

s=one(s,
'''void animateSwipeBack(){if(root==null)return;swipeAnimating=true;animateSwipeViews(0,120,()->swipeAnimating=false);}''',
'''void animateSwipeBack(){if(root==null)return;swipeAnimating=true;animateSwipeViews(0,120,()->{swipeAnimating=false;if(web!=null)web.animate().alpha(1f).setDuration(90).start();});}''',
'restore current web after canceled swipe')

s=one(s,
'''void animateSwipeViews(float y,long ms,Runnable end){if(poster!=null)poster.animate().translationY(y).setDuration(ms).start();if(web!=null)web.animate().translationY(y).setDuration(ms).start();if(shade!=null)shade.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)actions.animate().translationY(y).setDuration(ms).withEndAction(end).start();else if(end!=null)end.run();}''',
'''void animateSwipeViews(float y,long ms,Runnable end){if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(poster!=null)poster.animate().translationY(y).setDuration(ms).start();if(shade!=null)shade.animate().translationY(y).setDuration(ms).start();if(info!=null)info.animate().translationY(y).setDuration(ms).start();if(actions!=null)actions.animate().translationY(y).setDuration(ms).withEndAction(end).start();else if(end!=null)end.run();}''',
'never animate old youtube webview')

# Remove completamente o contador (5 / 3173).
s=one(s,
'''meta.setText("Yelly Doramas  •  "+(index+1)+" / "+(totalRows>0?totalRows:items.length()));''',
'''meta.setText("Yelly Doramas");''',
'remove story count')

# Usa a mesma capa do filme nas faixas que antes ficavam pretas e esconde
# o WebView antigo antes de carregar o próximo vídeo.
s=one(s,
'''String img=x.optString("portrait_img",x.optString("thumbnail",""));if(!img.isEmpty())Img.loadVisible(poster,img);play(id);''',
'''String img=x.optString("portrait_img",x.optString("thumbnail",""));if(web!=null){web.animate().cancel();web.setAlpha(0f);web.setTranslationY(0f);}if(!img.isEmpty()){Img.loadVisible(poster,img);if(topCoverMask!=null)Img.loadVisible(topCoverMask,img);if(bottomCoverMask!=null)Img.loadVisible(bottomCoverMask,img);}play(id);''',
'load story cover backgrounds')

# Só exibe o novo WebView quando o vídeo novo estiver realmente pronto.
s=one(s,
'''events:{onReady:function(e){e.target.playVideo();}}});}function gpToggle()''',
'''events:{onReady:function(e){e.target.playVideo();try{StoryBridge.ready();}catch(x){}}}});}function gpToggle()''',
'story player ready callback')

# Se o enriquecimento trocar a capa, atualizar também as áreas que cobrem o preto.
s=one(s,
'''if(!p.isEmpty()){x.put("portrait_img",p);x.put("thumbnail",p);Img.loadVisible(poster,p);}''',
'''if(!p.isEmpty()){x.put("portrait_img",p);x.put("thumbnail",p);Img.loadVisible(poster,p);if(topCoverMask!=null)Img.loadVisible(topCoverMask,p);if(bottomCoverMask!=null)Img.loadVisible(bottomCoverMask,p);}''',
'update enriched cover masks')

stories.write_text(s,encoding='utf-8')

# Player aberto pelo botão "Assistir": trocar as faixas pretas pela capa do filme.
y=yt.read_text(encoding='utf-8')
y=one(y,
'''    FrameLayout root;
    WebView web;
    View touchShield;''',
'''    FrameLayout root;
    WebView web;
    ImageView playerBackdrop,topPosterMask,bottomPosterMask,brandPosterMask;
    View touchShield;''',
'player cover fields')

y=one(y,
'''        root=new FrameLayout(this);root.setBackgroundColor(Color.BLACK);

        web=new WebView(this);web.setBackgroundColor(Color.BLACK);web.setAlpha(tvMode?0f:1f);''',
'''        root=new FrameLayout(this);root.setBackgroundColor(Color.BLACK);
        playerBackdrop=new ImageView(this);playerBackdrop.setScaleType(ImageView.ScaleType.CENTER_CROP);playerBackdrop.setBackgroundColor(Color.BLACK);playerBackdrop.setAlpha(.52f);if(videoPoster!=null&&!videoPoster.trim().isEmpty())Img.loadVisible(playerBackdrop,videoPoster);root.addView(playerBackdrop,new FrameLayout.LayoutParams(-1,-1));

        web=new WebView(this);web.setBackgroundColor(Color.TRANSPARENT);web.setAlpha(tvMode?0f:1f);''',
'player full backdrop')

y=one(y,
'''        root.addView(web,new FrameLayout.LayoutParams(-1,-1));
        View ytBrandMask=new View(this);ytBrandMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(dp(148),dp(58),Gravity.RIGHT|Gravity.BOTTOM);ybm.setMargins(0,0,dp(2),dp(2));root.addView(ytBrandMask,ybm);

        if(!tvMode){
            int screenH=getResources().getDisplayMetrics().heightPixels;
            int topMaskH=Math.max(dp(48),Math.min(dp(82),(int)(screenH*0.09f)));
            int bottomMaskH=Math.max(dp(64),Math.min(dp(110),(int)(screenH*0.11f)));
            View topMask=new View(this);topMask.setBackgroundColor(Color.BLACK);
            FrameLayout.LayoutParams topMaskLp=new FrameLayout.LayoutParams(-1,topMaskH,Gravity.TOP);root.addView(topMask,topMaskLp);
            View bottomMask=new View(this);bottomMask.setBackgroundColor(Color.BLACK);
            FrameLayout.LayoutParams bottomMaskLp=new FrameLayout.LayoutParams(-1,bottomMaskH,Gravity.BOTTOM);root.addView(bottomMask,bottomMaskLp);
        }''',
'''        root.addView(web,new FrameLayout.LayoutParams(-1,-1));
        brandPosterMask=new ImageView(this);brandPosterMask.setScaleType(ImageView.ScaleType.CENTER_CROP);brandPosterMask.setBackgroundColor(Color.BLACK);brandPosterMask.setAlpha(.90f);if(videoPoster!=null&&!videoPoster.trim().isEmpty())Img.loadVisible(brandPosterMask,videoPoster);FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(dp(148),dp(58),Gravity.RIGHT|Gravity.BOTTOM);ybm.setMargins(0,0,dp(2),dp(2));root.addView(brandPosterMask,ybm);

        if(!tvMode){
            int screenH=getResources().getDisplayMetrics().heightPixels;
            int topMaskH=Math.max(dp(48),Math.min(dp(82),(int)(screenH*0.09f)));
            int bottomMaskH=Math.max(dp(64),Math.min(dp(110),(int)(screenH*0.11f)));
            topPosterMask=new ImageView(this);topPosterMask.setScaleType(ImageView.ScaleType.CENTER_CROP);topPosterMask.setBackgroundColor(Color.BLACK);topPosterMask.setAlpha(.90f);if(videoPoster!=null&&!videoPoster.trim().isEmpty())Img.loadVisible(topPosterMask,videoPoster);
            FrameLayout.LayoutParams topMaskLp=new FrameLayout.LayoutParams(-1,topMaskH,Gravity.TOP);root.addView(topPosterMask,topMaskLp);
            bottomPosterMask=new ImageView(this);bottomPosterMask.setScaleType(ImageView.ScaleType.CENTER_CROP);bottomPosterMask.setBackgroundColor(Color.BLACK);bottomPosterMask.setAlpha(.90f);if(videoPoster!=null&&!videoPoster.trim().isEmpty())Img.loadVisible(bottomPosterMask,videoPoster);
            FrameLayout.LayoutParams bottomMaskLp=new FrameLayout.LayoutParams(-1,bottomMaskH,Gravity.BOTTOM);root.addView(bottomPosterMask,bottomMaskLp);
        }''',
'player poster masks')

# Deixar o HTML transparente para a capa aparecer atrás nas áreas livres.
y=one(y,
'''"<style>html,body,#p{margin:0;padding:0;width:100%;height:100%;background:#000;overflow:hidden}iframe{width:100%!important;height:100%!important;border:0;"+tvCss+"}</style>"+''',
'''"<style>html,body,#p{margin:0;padding:0;width:100%;height:100%;background:transparent;overflow:hidden}iframe{width:100%!important;height:100%!important;border:0;"+tvCss+"}</style>"+''',
'transparent player html')

yt.write_text(y,encoding='utf-8')

g=grad.read_text(encoding='utf-8')
if "versionCode 10011" not in g or "versionName '1.0.11'" not in g:
    raise SystemExit('expected Yelly 1.0.11 base')
g=g.replace('versionCode 10011','versionCode 10012',1).replace("versionName '1.0.11'","versionName '1.0.12'",1)
grad.write_text(g,encoding='utf-8')

(root/'app/RELEASE_NOTES.txt').write_text('''Yelly Doramas 1.0.12
Stories: removido completamente o contador de posição/quantidade (ex.: 5 / 3173). Agora aparece somente "Yelly Doramas".
Stories: as áreas antes pretas no topo e embaixo usam a própria capa do filme como fundo.
Assistir: as áreas pretas do player também usam a capa do filme como fundo.
Swipe: corrigido o flash do vídeo anterior. O WebView antigo deixa de ser arrastado; durante a troca aparece a capa e o novo vídeo só é mostrado quando estiver pronto.
Mantidos Favoritar, Comentários, Assistir, título, progresso e visual da Home da 1.0.10.
''',encoding='utf-8')
print('YELLY_112_STORY_COUNT_COVERS_FLASH_OK')
