from pathlib import Path

root=Path('work')
grad=root/'app/build.gradle'

g=grad.read_text(encoding='utf-8')
if "versionCode 10007" not in g or "versionName '1.0.7'" not in g:
    raise SystemExit('expected Yelly 1.0.7 base')
g=g.replace('versionCode 10007','versionCode 10010',1).replace("versionName '1.0.7'","versionName '1.0.10'",1)
grad.write_text(g,encoding='utf-8')

(root/'app/RELEASE_NOTES.txt').write_text('''Yelly Doramas 1.0.10
Home restaurada exatamente para o visual da 1.0.7: carrossel grande e capas verticais como na referência enviada.
Removidas as alterações de capa feitas nas versões 1.0.8 e 1.0.9.
Mantidas as correções da 1.0.7: sinopse pt-BR, elenco sem quantidade de filmes, Stories, comentários, favoritos, login, identidade Yelly e marca do YouTube coberta.
''',encoding='utf-8')
print('YELLY_110_RESTORE_107_OK')
