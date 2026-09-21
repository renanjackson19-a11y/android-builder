from pathlib import Path
import re
ROOT=Path('/var/www/greenplay/public_html')
boot=ROOT/'api/dtlive/bootstrap_home/index.php'
cat=ROOT/'api/dtlive/content_by_category/index.php'
for p in (boot,cat):
    if not p.is_file(): raise SystemExit(f'ERRO: arquivo ausente: {p}')

def req_helper(s):
    line="require_once dirname(__DIR__).'/_tmdb_cover_batch.php';"
    if line not in s:
        needle="require_once dirname(__DIR__).'/_common.php';"
        if needle not in s: raise SystemExit('ERRO: _common.php nao localizado')
        s=s.replace(needle,needle+'\n'+line,1)
    return s

s=req_helper(boot.read_text())
s=re.sub(r"\$GLOBALS\['GP_TMDB_COVER_BUDGET'\]\s*=\s*\d+\s*;",'',s)
if 'GREENPLAY TMDB SHARED PROVIDER V2' not in s:
    needle='$srv=dt_provider_server();'
    add="""$srv=dt_provider_server();
// GREENPLAY TMDB SHARED PROVIDER V2
$gpTmdbPid=preg_replace('/[^a-zA-Z0-9_-]/','',(string)($srv['provider_id']??($srv['id']??'')));
if($gpTmdbPid!=='')$GLOBALS['GP_TMDB_PROVIDER_ID']=$gpTmdbPid;"""
    if needle not in s: raise SystemExit('ERRO: dt_provider_server bootstrap nao localizado')
    s=s.replace(needle,add,1)
if 'GREENPLAY TMDB SHARED HOME V2' not in s:
    needle='function gp724_section($type,$cid,$title,$items,$sid,$srv,$playAllowed){'
    add=needle+"""
  // GREENPLAY TMDB SHARED HOME V2
  if(($type==='movie'||$type==='series')&&function_exists('gp_tmdb_cover_batch')){
    gp_tmdb_cover_batch(array_slice((array)$items,0,4),$type,4);
  }"""
    if needle not in s: raise SystemExit('ERRO: gp724_section nao localizada')
    s=s.replace(needle,add,1)
boot.write_text(s)

s=req_helper(cat.read_text())
s=re.sub(r"\$GLOBALS\['GP_TMDB_COVER_BUDGET'\]\s*=\s*[^;]+;",'',s)
if 'GREENPLAY TMDB SHARED PROVIDER V2' not in s:
    needle='$acc=dt_user_access($uid);'
    add=needle+"""
// GREENPLAY TMDB SHARED PROVIDER V2
$gpTmdbSrv=dt_provider_server();
$gpTmdbPid=preg_replace('/[^a-zA-Z0-9_-]/','',(string)($gpTmdbSrv['provider_id']??($gpTmdbSrv['id']??'')));
if($gpTmdbPid!=='')$GLOBALS['GP_TMDB_PROVIDER_ID']=$gpTmdbPid;"""
    if needle not in s: raise SystemExit('ERRO: dt_user_access category nao localizado')
    s=s.replace(needle,add,1)
if 'gp_tmdb_cover_batch($slice,$type,$per)' not in s:
    needle='$slice=array_slice($items,$start,$per);'
    add=needle+"""
// GREENPLAY TMDB SHARED CATEGORY V2
if(function_exists('gp_tmdb_cover_batch'))gp_tmdb_cover_batch($slice,$type,$per);"""
    if needle not in s: raise SystemExit('ERRO: slice category nao localizado')
    s=s.replace(needle,add,1)
cat.write_text(s)
print('TMDB SHARED V2 instalado em bootstrap_home e content_by_category.')
