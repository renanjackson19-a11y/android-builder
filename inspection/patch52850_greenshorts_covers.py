from pathlib import Path
p=Path('work/app/src/main/java/fun/greenplay/app/MainActivity.java')
s=p.read_text()

old='ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,x);else Img.loadBest'
new='ImageView im=new ImageView(this);im.setScaleType("Shorts".equals(activeHomeTab)?ImageView.ScaleType.FIT_CENTER:ImageView.ScaleType.CENTER_CROP);if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,x);else Img.loadBest'
assert old in s
s=s.replace(old,new,1)

old2='ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,use);else Img.loadBest'
new2='ImageView im=new ImageView(this);im.setScaleType("Shorts".equals(activeHomeTab)?ImageView.ScaleType.FIT_CENTER:ImageView.ScaleType.CENTER_CROP);if("Shorts".equals(activeHomeTab))loadGreenShortsCover(im,use);else Img.loadBest'
assert old2 in s
s=s.replace(old2,new2,1)

# GreenShorts rows/other mobile cards: keep entire artwork visible too.
old3='ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setBackground(round(CARD,15));im.setClipToOutline(true);if("Shorts".equals(activeHomeTab))im.setImageResource(R.drawable.top_shorts);Img.loadBest'
new3='ImageView im=new ImageView(this);im.setScaleType("Shorts".equals(activeHomeTab)?ImageView.ScaleType.FIT_CENTER:ImageView.ScaleType.CENTER_CROP);im.setBackground(round(CARD,15));im.setClipToOutline(true);if("Shorts".equals(activeHomeTab))im.setImageResource(R.drawable.top_shorts);Img.loadBest'
if old3 in s:
    s=s.replace(old3,new3,1)

s=s.replace('catalog52849_','catalog52850_',1)
p.write_text(s)

b=Path('work/app/build.gradle')
t=b.read_text()
assert 'versionCode 52849' in t and "versionName '5.28.49'" in t
t=t.replace('versionCode 52849','versionCode 52850',1).replace("versionName '5.28.49'","versionName '5.28.50'",1)
b.write_text(t)

Path('work/README_GREENPLAY_5_28_52850.txt').write_text("""GreenPlay 5.28.50

- GreenShorts: capas sem zoom/corte.
- Imagens centralizadas preservando a proporcao original.
- Ajuste aplicado ao destaque e ao grid/listas do GreenShorts.
- Filmes e series normais continuam com o comportamento anterior.
""")

assert 'ImageView.ScaleType.FIT_CENTER:ImageView.ScaleType.CENTER_CROP' in p.read_text()
assert 'versionCode 52850' in b.read_text()
print('OK 5.28.50')
