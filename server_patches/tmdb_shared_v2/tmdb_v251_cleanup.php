<?php
/**
 * GREENPLAY TMDB V2.5.1 CLEANUP
 * Remove somente matches recentes inseguros (cover_cache_version 3/4):
 * - fonte tem ano conhecido
 * - resultado TMDB sem ano, ou distante mais de 3 anos
 */
if(PHP_SAPI!=='cli'){http_response_code(403);exit("CLI only\n");}
set_time_limit(0);
ini_set('memory_limit','2048M');

$root='/var/www/greenplay/public_html';
$_SERVER['DOCUMENT_ROOT']=$root;
$_SERVER['HTTP_HOST']='localhost';

require_once $root.'/config/config.php';
require_once $root.'/config/tmdb.php';
if(!function_exists('greenplay_providers')) require_once $root.'/model/stream/stream.php';
if(!function_exists('greenplay_m3u_lite_catalog')) require_once $root.'/model/stream/m3u.php';
require_once $root.'/api/dtlive/_tmdb_cover_batch.php';

function gp_v251_unlink_shared_if_same($type,$title,$year,$tmdbId){
    foreach(array(
        gp_tmdb_shared_file($type,$title,$year),
        gp_tmdb_shared_file($type,$title,'')
    ) as $f){
        if(!$f||!is_file($f))continue;
        $j=json_decode(@file_get_contents($f),true);
        if(is_array($j)&&(string)($j['tmdb_id']??'')===(string)$tmdbId)@unlink($f);
    }
}

$cfg=greenplay_providers();
$checked=0;$removed=0;

foreach((array)($cfg['providers']??array()) as $provider){
    if((string)($provider['enabled']??'1')!=='1')continue;
    $pid=preg_replace('/[^a-zA-Z0-9_-]/','',(string)($provider['id']??($provider['provider_id']??'')));
    if($pid==='')continue;

    $provider['id']=$pid;
    $provider['provider_id']=$pid;
    $GLOBALS['GP_TMDB_PROVIDER_ID']=$pid;

    if(!function_exists('greenplay_provider_is_m3u')||!greenplay_provider_is_m3u($provider))continue;
    $catalog=greenplay_m3u_lite_catalog($provider,false);
    if(!is_array($catalog))continue;

    foreach(array('series','movie') as $type){
        foreach((array)($catalog[$type]??array()) as $it){
            if(!is_array($it))$it=(array)$it;

            $id=gp_tmdb_cover_item_id($it,$type);
            $title=gp_tmdb_cover_item_title($it);
            $sy=gp_tmdb_cover_item_year($it);

            if($id===''||$title===''||$sy==='')continue;

            $cache=gp_tmdb_content_cache_get($type,$id);
            if(!is_array($cache))continue;

            $cv=(int)($cache['cover_cache_version']??0);
            if($cv!==3 && $cv!==4)continue;

            $checked++;

            $cy=gp_tmdb_year((string)($cache['year']??($cache['release_date']??'')));
            $unsafe=($cy==='') || abs((int)$sy-(int)$cy)>3;
            if(!$unsafe)continue;

            $tmdbId=(string)($cache['tmdb_id']??'');
            $file=gp_tmdb_content_cache_file($type,$id);

            if($file&&is_file($file))@unlink($file);
            gp_v251_unlink_shared_if_same($type,$title,$sy,$tmdbId);

            $removed++;
            echo "REMOVIDO provider={$pid} type={$type} id={$id} source_year={$sy} cache_year=".($cy===''?'NONE':$cy)." tmdb_id={$tmdbId} title={$title}\n";
        }
    }
}

echo "FINAL checked={$checked} removed={$removed}\n";
