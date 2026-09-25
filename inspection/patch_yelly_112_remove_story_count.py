from pathlib import Path

root=Path('work')
stories=root/'app/src/main/java/fun/greenplay/app/StoriesActivity.java'
grad=root/'app/build.gradle'

s=stories.read_text(encoding='utf-8')

old='''meta.setText("Yelly Doramas  •  "+(index+1)+" / "+(totalRows>0?totalRows:items.length()));if(progress!=null)progress.setProgress(0);'''
new='''meta.setText("Yelly Doramas");if(progress!=null)progress.setProgress(0);'''
if s.count(old)!=1:
    raise SystemExit(f'story counter expected 1 got {s.count(old)}')
s=s.replace(old,new,1)

stories.write_text(s,encoding='utf-8')

g=grad.read_text(encoding='utf-8')
if "versionCode 10011" not in g or "versionName '1.0.11'" not in g:
    raise SystemExit('expected Yelly 1.0.11 base')
g=g.replace('versionCode 10011','versionCode 10012',1).replace("versionName '1.0.11'","versionName '1.0.12'",1)
grad.write_text(g,encoding='utf-8')

(root/'app/RELEASE_NOTES.txt').write_text('''Yelly Doramas 1.0.12
Stories: removido completamente o contador de quantidade/posição (ex.: 5 / 3173).
Agora aparece somente "Yelly Doramas" nessa linha.
Mantidos os demais controles e o visual da 1.0.11.
''',encoding='utf-8')
print('YELLY_112_REMOVE_STORY_COUNT_OK')
