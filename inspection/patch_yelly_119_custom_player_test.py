from pathlib import Path

root=Path("work")

def replace_once(s,old,new,label):
    if s.count(old)!=1:
        raise SystemExit(f"{label}: {s.count(old)}")
    return s.replace(old,new,1)

p=root/"app/src/main/java/fun/greenplay/app/StoriesActivity.java"
s=p.read_text(encoding="utf-8")
s=replace_once(s,
'FrameLayout root;WebView web;ImageView poster,logoTop;View shade,swipe,ytTopMask,ytBottomMask;LinearLayout info,actions;',
'FrameLayout root;WebView web;ImageView poster,logoTop;View shade,swipe;LinearLayout info,actions;',
'fields')
old="""FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1);if(!tvMode)wp.setMargins(0,dp(64),0,dp(112));root.addView(web,wp);
  ytTopMask=new View(this);ytTopMask.setBackgroundColor(0xee14080f);FrameLayout.LayoutParams ytp=new FrameLayout.LayoutParams(-1,dp(76),Gravity.TOP);ytp.setMargins(0,dp(64),0,0);root.addView(ytTopMask,ytp);
  ytBottomMask=new View(this);ytBottomMask.setBackgroundColor(0xee14080f);FrameLayout.LayoutParams ybp=new FrameLayout.LayoutParams(-1,dp(64),Gravity.BOTTOM);ybp.setMargins(0,0,0,dp(112));root.addView(ytBottomMask,ybp);"""
new="""FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1);root.addView(web,wp);"""
s=replace_once(s,old,new,'story mask block')
oldcss="#p{position:absolute;left:50%;top:50%;border:0;background:#000;transform:translate(-50%,-50%)}"
newcss="#p{position:absolute;left:50%;top:50%;border:0;background:transparent;transform:translate(-50%,-50%);overflow:hidden}#p iframe{position:absolute!important;left:0!important;top:-44px!important;width:100%!important;height:calc(100% + 88px)!important;border:0!important}"
s=replace_once(s,oldcss,newcss,'story css')
p.write_text(s,encoding="utf-8")

p=root/"app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java"
y=p.read_text(encoding="utf-8")
y=replace_once(y,'View touchShield,ytTopMask,ytBottomMask,ytBrandMask;','View touchShield;','player fields')
old="""FrameLayout.LayoutParams wlp=new FrameLayout.LayoutParams(-1,-1);if(!tvMode)wlp.setMargins(0,dp(68),0,dp(106));root.addView(web,wlp);
        if(!tvMode){
            ytTopMask=new View(this);ytTopMask.setBackground(bg(0xee14080f,0));FrameLayout.LayoutParams tlp=new FrameLayout.LayoutParams(-1,dp(74),Gravity.TOP);tlp.setMargins(0,dp(68),0,0);root.addView(ytTopMask,tlp);
            ytBottomMask=new View(this);ytBottomMask.setBackground(bg(0xee14080f,0));FrameLayout.LayoutParams blp=new FrameLayout.LayoutParams(-1,dp(62),Gravity.BOTTOM);blp.setMargins(0,0,0,dp(106));root.addView(ytBottomMask,blp);
            ytBrandMask=new View(this);ytBrandMask.setBackground(bg(0xee14080f,12));FrameLayout.LayoutParams brp=new FrameLayout.LayoutParams(dp(124),dp(48),Gravity.RIGHT|Gravity.BOTTOM);brp.setMargins(0,0,dp(2),dp(106));root.addView(ytBrandMask,brp);
        }"""
y=replace_once(y,old,'root.addView(web,new FrameLayout.LayoutParams(-1,-1));','player masks')
y=replace_once(y,
"#p{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#000}iframe{width:100%!important;height:100%!important;border:0}",
"#p{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:transparent;overflow:hidden}#p iframe{position:absolute!important;left:0!important;top:-52px!important;width:100%!important;height:calc(100% + 104px)!important;border:0!important}",
'player css')
y=y.replace('GradientDrawable controlsBg=bg(0xe30f0a0c,20);controlsBg.setStroke(dp(1),0x665b414e);',
            'GradientDrawable controlsBg=bg(0xdc120a10,22);controlsBg.setStroke(dp(1),0x55754862);',1)
y=y.replace('back10=tx("↶ 10s",15);play=tx("Ⅱ",26);fwd10=tx("10s ↷",15);',
            'back10=tx("↶ 10s",15);play=tx("▶",28);fwd10=tx("10s ↷",15);',1)
p.write_text(y,encoding="utf-8")

p=root/"app/build.gradle"
g=p.read_text(encoding="utf-8")
g=replace_once(g,'versionCode 10017','versionCode 10019','code')
g=replace_once(g,"versionName '1.0.17'","versionName '1.0.19'",'name')
p.write_text(g,encoding="utf-8")

(root/"app/RELEASE_NOTES.txt").write_text("""Yelly Doramas 1.0.19
- Player visual próprio do Yelly para teste.
- A fonte continua sendo o ID interno atual, mas URL/ID não aparecem na interface.
- Controles visíveis são do Yelly: play/pause, 10s, barra de progresso e tempo.
- Removidas as faixas/sombras pintadas por cima do vídeo.
- O conteúdo embutido é recortado dentro da área de vídeo para a interface ficar limpa.
- Stories mantêm banner Yelly, Favoritar, Comentários e Assistir agora.
""",encoding="utf-8")
print("YELLY_119_CUSTOM_PLAYER_OK")
