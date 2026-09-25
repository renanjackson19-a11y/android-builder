from pathlib import Path

root=Path('work')
stories=root/'app/src/main/java/fun/greenplay/app/StoriesActivity.java'
grad=root/'app/build.gradle'

s=stories.read_text(encoding='utf-8')

old='''  View ytBrandMask=new View(this);ytBrandMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(dp(136),dp(54),Gravity.RIGHT|Gravity.BOTTOM);ybm.setMargins(0,0,dp(2),dp(2));root.addView(ytBrandMask,ybm);'''
new='''  if(!tvMode){View ytTopMask=new View(this);ytTopMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ytm=new FrameLayout.LayoutParams(-1,dp(86),Gravity.TOP);root.addView(ytTopMask,ytm);View ytBottomMask=new View(this);ytBottomMask.setBackgroundColor(Color.BLACK);FrameLayout.LayoutParams ybm=new FrameLayout.LayoutParams(-1,dp(108),Gravity.BOTTOM);root.addView(ytBottomMask,ybm);}'''
if s.count(old)!=1:
    raise SystemExit(f'youtube mask block expected 1 got {s.count(old)}')
s=s.replace(old,new,1)

old='''  hint=t(tvMode?"↑ ↓  trocar Story":"↑  deslize para o próximo",12);hint.setTextColor(0xffd4c4cc);FrameLayout.LayoutParams hp=new FrameLayout.LayoutParams(-2,dp(32),Gravity.TOP|Gravity.CENTER_HORIZONTAL);hp.setMargins(0,dp(16),0,0);root.addView(hint,hp);'''
new='''  hint=t(tvMode?"↑ ↓  trocar Story":"",12);hint.setTextColor(0xffd4c4cc);if(tvMode){FrameLayout.LayoutParams hp=new FrameLayout.LayoutParams(-2,dp(32),Gravity.TOP|Gravity.CENTER_HORIZONTAL);hp.setMargins(0,dp(16),0,0);root.addView(hint,hp);}'''
if s.count(old)!=1:
    raise SystemExit(f'hint block expected 1 got {s.count(old)}')
s=s.replace(old,new,1)

stories.write_text(s,encoding='utf-8')

g=grad.read_text(encoding='utf-8')
if "versionCode 10010" not in g or "versionName '1.0.10'" not in g:
    raise SystemExit('expected Yelly 1.0.10 base')
g=g.replace('versionCode 10010','versionCode 10011',1).replace("versionName '1.0.10'","versionName '1.0.11'",1)
grad.write_text(g,encoding='utf-8')

(root/'app/RELEASE_NOTES.txt').write_text('''Yelly Doramas 1.0.11
Stories: removidas as informações visuais do YouTube que apareciam no topo (título/canal) e na parte inferior (compartilhar/miniatura/canal).
Também removido o texto "deslize para o próximo" no topo do celular para deixar a tela limpa.
Mantidos os controles próprios do Yelly: Favoritar, Comentários, Assistir, título, contador e barra de progresso.
Home permanece exatamente no visual restaurado da 1.0.10.
''',encoding='utf-8')
print('YELLY_111_CLEAN_STORIES_UI_OK')
