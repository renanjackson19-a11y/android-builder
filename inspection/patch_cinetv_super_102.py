from pathlib import Path

root = Path("work")
main = root / "app/src/main/java/fun/greenplay/app/MainActivity.java"
gradle = root / "app/build.gradle"
notes = root / "app/RELEASE_NOTES.txt"

s = main.read_text(encoding="utf-8")

old1 = 'TextView eyebrow=t("PREPARANDO GREENPLAY",tvMode?10:10);'
new1 = 'String loadingBrand=(appName==null||appName.trim().isEmpty())?"CINETV SUPER":appName.trim().toUpperCase(java.util.Locale.ROOT);TextView eyebrow=t("PREPARANDO "+loadingBrand,tvMode?10:10);'
if old1 not in s:
    raise SystemExit("Loading GreenPlay marker not found")
s = s.replace(old1, new1, 1)

old2 = 'tvPreviewLoadingStatus=t("GREENPLAY • AO VIVO",wide?10:9);'
new2 = 'String liveLoadingBrand=(appName==null||appName.trim().isEmpty())?"CINETV SUPER":appName.trim().toUpperCase(java.util.Locale.ROOT);tvPreviewLoadingStatus=t(liveLoadingBrand+" • AO VIVO",wide?10:9);'
if old2 not in s:
    raise SystemExit("Live GreenPlay marker not found")
s = s.replace(old2, new2, 1)

main.write_text(s, encoding="utf-8")

g = gradle.read_text(encoding="utf-8")
if "versionCode 101" not in g or "versionName '1.0.1'" not in g:
    raise SystemExit("CineTV 1.0.1 version markers not found")
g = g.replace("versionCode 101", "versionCode 102", 1)
g = g.replace("versionName '1.0.1'", "versionName '1.0.2'", 1)
gradle.write_text(g, encoding="utf-8")

notes.write_text("""CineTV Super 1.0.2
Identidade corrigida nas telas de sincronização e carregamento da TV.
Removidos os textos visíveis GreenPlay do carregamento da CineTV Super.
Compatível com a integração de franquia e reprodução acelerada pela matriz.
""", encoding="utf-8")

check = main.read_text(encoding="utf-8")
if '"PREPARANDO GREENPLAY"' in check or '"GREENPLAY • AO VIVO"' in check:
    raise SystemExit("Visible GreenPlay loading text still present")
print("CineTV Super 1.0.2 branding patch applied")
