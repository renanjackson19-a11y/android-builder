#!/usr/bin/env bash
set -euo pipefail

ROOT=/var/www/greenplay/public_html
BASE=https://raw.githubusercontent.com/renanjackson19-a11y/android-builder/main/server_patches/football_v1

mkdir -p "$ROOT/api/dtlive/football" "$ROOT/cache/football"

curl -fsSL "$BASE/api/dtlive/football/index.php"   -o "$ROOT/api/dtlive/football/index.php"

if [ ! -f "$ROOT/config/football.php" ]; then
  curl -fsSL "$BASE/config/football.php.example"     -o "$ROOT/config/football.php"
fi

chown -R www-data:www-data "$ROOT/api/dtlive/football" "$ROOT/cache/football"
chown www-data:www-data "$ROOT/config/football.php"
chmod 0775 "$ROOT/cache/football"
chmod 0644 "$ROOT/api/dtlive/football/index.php"
chmod 0640 "$ROOT/config/football.php"

php -l "$ROOT/api/dtlive/football/index.php"
php -l "$ROOT/config/football.php"

echo
echo "OK - GreenPlay Football V1 instalado"
echo "Edite a chave em: $ROOT/config/football.php"
