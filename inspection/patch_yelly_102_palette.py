from pathlib import Path
import re, colorsys

root=Path('work')
main=root/'app/src/main/java/fun/greenplay/app/MainActivity.java'

def recolor_hex(text):
    pat=re.compile(r'0x([0-9a-fA-F]{2})([0-9a-fA-F]{6})')
    def conv(m):
        a=m.group(1).lower()
        rgb=m.group(2)
        r,g,b=[int(rgb[i:i+2],16) for i in (0,2,4)]
        # Only inherited green/teal-biased UI colors.
        if not (g > r + 2 and g > b + 2):
            return m.group(0)
        h,s,v=colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
        # Preserve brightness while moving all green/teal UI tones to Yelly plum/rose.
        if s < 0.18:
            # Neutral text/dividers: warm rose-neutral instead of green-gray.
            rr=max(0,min(255,round(v*255)))
            gg=max(0,min(255,round(v*255*0.94)))
            bb=max(0,min(255,round(v*255*0.98)))
        else:
            # Saturated/dark surfaces: deep plum/rose hue.
            nr,ng,nb=colorsys.hsv_to_rgb(330/360.0,s,v)
            rr,gg,bb=round(nr*255),round(ng*255),round(nb*255)
        return '0x'+a+f'{rr:02x}{gg:02x}{bb:02x}'
    return pat.sub(conv,text)

# Recolor every Java/XML UI resource so no inherited GreenPlay green remains.
targets=list((root/'app/src/main/java').rglob('*.java'))+list((root/'app/src/main/res').rglob('*.xml'))
for p in targets:
    try:
        old=p.read_text(encoding='utf-8')
    except Exception:
        continue
    new=recolor_hex(old)
    new=new.replace('#20E070','#B8007D').replace('#20e070','#b8007d')
    new=new.replace('#21DF70','#B8007D').replace('#21df70','#b8007d')
    new=new.replace('#48F784','#E03A99').replace('#48f784','#e03a99')
    if new!=old:
        p.write_text(new,encoding='utf-8')

# Explicit Yelly palette for the profile screen shown by the user.
s=main.read_text(encoding='utf-8')
profile_map={
    '0xff101a15':'0xff21121b',
    '0xff111d18':'0xff24131d',
    '0xff101713':'0xff1f1219',
    '0xff111a15':'0xff22131b',
    '0xff252b2a':'0xff33242c',
    '0xff8d9a93':'0xff9b9097',
    '0xff9ca8a2':'0xffaaa0a6',
    '0xff93a099':'0xffa0959c',
    '0xff83918a':'0xff91868d',
    '0xff8f9693':'0xff9a9297',
    '0xff6e7b74':'0xff7d7078',
    '0xff969d99':'0xffa39aa0',
    '0xff69716d':'0xff786d73',
    '0xffc9d1cd':'0xffd4cbd0',
}
for a,b in profile_map.items():
    s=s.replace(a,b)

# Warm the global dark card palette slightly toward plum.
s=s.replace('final int BG=Color.rgb(12,8,11),CARD=Color.rgb(29,18,24);',
            'final int BG=Color.rgb(12,7,11),CARD=Color.rgb(31,16,25);')

main.write_text(s,encoding='utf-8')

grad=root/'app/build.gradle'
g=grad.read_text(encoding='utf-8')
g=g.replace('versionCode 10001','versionCode 10002')
g=g.replace("versionName '1.0.1'","versionName '1.0.2'")
grad.write_text(g,encoding='utf-8')

(root/'app/RELEASE_NOTES.txt').write_text('''Yelly Doramas 1.0.2
Removidos os tons verdes herdados do GreenPlay em todo o aplicativo.
Perfil, cartões, divisórias, estados de foco e textos agora usam paleta Yelly em preto/plum/rosa.
Mantida a sincronização de logo, fundo e cor principal pelo painel Yelly.
Mantido o login corrigido da versão 1.0.1.
''',encoding='utf-8')
print('YELLY_102_PALETTE_OK')
