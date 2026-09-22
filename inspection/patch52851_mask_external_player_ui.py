from pathlib import Path

player=Path('work/app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java')
s=player.read_text()

# Keep the existing YouTube iframe playback, but visually mask the external
# top/bottom chrome the user marked. GreenPlay controls remain above the masks.
old='''        root.addView(web,new FrameLayout.LayoutParams(-1,-1));

        touchShield=new View(this);touchShield.setBackgroundColor(Color.TRANSPARENT);touchShield.setClickable(true);'''
new='''        root.addView(web,new FrameLayout.LayoutParams(-1,-1));

        int screenH=getResources().getDisplayMetrics().heightPixels;
        int topMaskH=Math.max(dp(48),Math.min(dp(82),(int)(screenH*0.09f)));
        int bottomMaskH=Math.max(dp(64),Math.min(dp(110),(int)(screenH*0.11f)));

        View topMask=new View(this);
        topMask.setBackgroundColor(Color.BLACK);
        FrameLayout.LayoutParams topMaskLp=new FrameLayout.LayoutParams(-1,topMaskH,Gravity.TOP);
        root.addView(topMask,topMaskLp);

        View bottomMask=new View(this);
        bottomMask.setBackgroundColor(Color.BLACK);
        FrameLayout.LayoutParams bottomMaskLp=new FrameLayout.LayoutParams(-1,bottomMaskH,Gravity.BOTTOM);
        root.addView(bottomMask,bottomMaskLp);

        touchShield=new View(this);touchShield.setBackgroundColor(Color.TRANSPARENT);touchShield.setClickable(true);'''
assert old in s, 'web/touchShield insertion point not found'
s=s.replace(old,new,1)

# Keep GreenPlay back button above the top mask.
old2='''        FrameLayout.LayoutParams bp=new FrameLayout.LayoutParams(dp(48),dp(48),Gravity.TOP|Gravity.LEFT);
        bp.setMargins(dp(14),dp(14),0,0);root.addView(back,bp);'''
new2='''        FrameLayout.LayoutParams bp=new FrameLayout.LayoutParams(dp(48),dp(48),Gravity.TOP|Gravity.LEFT);
        bp.setMargins(dp(14),dp(14),0,0);root.addView(back,bp);
        back.bringToFront();'''
assert old2 in s
s=s.replace(old2,new2,1)

# Place GreenPlay controls on top of the bottom mask.
old3='''        FrameLayout.LayoutParams cp=new FrameLayout.LayoutParams(-1,dp(94),Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);
        cp.setMargins(dp(14),0,dp(14),dp(16));root.addView(controls,cp);'''
new3='''        FrameLayout.LayoutParams cp=new FrameLayout.LayoutParams(-1,dp(94),Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);
        cp.setMargins(dp(14),0,dp(14),dp(10));root.addView(controls,cp);
        controls.bringToFront();'''
assert old3 in s
s=s.replace(old3,new3,1)

# Prevent custom control hiding from revealing the masked external chrome.
old4='''    void hideControls(){if(controls!=null)controls.setVisibility(View.GONE);if(back!=null)back.setVisibility(View.GONE);}'''
new4='''    void hideControls(){if(controls!=null)controls.setVisibility(View.GONE);if(back!=null)back.setVisibility(View.GONE);}'''
# no-op replacement just verifies source shape
assert old4 in s

player.write_text(s)

main=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
ms=main.read_text()
ms=ms.replace('catalog52850_','catalog52851_',1)
main.write_text(ms)

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52850' in t and "versionName '5.28.50'" in t
t=t.replace('versionCode 52850','versionCode 52851',1).replace("versionName '5.28.50'","versionName '5.28.51'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52851.txt').write_text("""GreenPlay 5.28.51

- Mantém a reprodução incorporada atual funcionando.
- Oculta visualmente o cabeçalho externo no topo do vídeo.
- Oculta visualmente a faixa inferior externa com compartilhar, miniatura e marca.
- Mantém os controles próprios do GreenPlay por cima.
- Não altera o catálogo nem a lógica das capas da 5.28.50.
""")

assert 'topMaskH' in player.read_text()
assert 'bottomMaskH' in player.read_text()
assert 'versionCode 52851' in b.read_text()
print('OK 5.28.51')
