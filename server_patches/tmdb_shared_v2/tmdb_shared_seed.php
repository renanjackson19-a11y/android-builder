<?php
if(PHP_SAPI!=='cli'){http_response_code(403);exit;}
set_time_limit(0);ini_set('memory_limit','2048M');
$root='/var/www/greenplay/public_html';$_SERVER['DOCUMENT_ROOT']=$root;
require_once $root.'/config/config.php';
require_once $root.'/config/tmdb.php';
require_once $root.'/model/stream/stream.php';
require_once $root.'/model/stream/m3u.php';
require_once $root.'/api/dtlive/_tmdb_cover_batch.php';
$cfg=greenplay_providers();$total=0;$shared=0;$providers=0;
foreach((array)($cfg['providers']??array()) as $p){
    if((string)($p['enabled']??'1')!=='1')continue;
    $pid=preg_replace('/[^a-zA-Z0-9_-]/','',(string)($p['id']??($p['provider_id']??'')));
    if($pid==='')continue;
    $GLOBALS['GP_TMDB_PROVIDER_ID']=$pid;$providers++;
    $srv=array_merge((array)$p,array('id'=>$pid,'provider_id'=>$pid));
    $cat=function_exists('greenplay_m3u_lite_catalog')?greenplay_m3u_lite_catalog($srv,false):array();
    if(!is_array($cat))continue;
    foreach(array('movie','series') as $type){
        foreach((array)($cat[$type]??array()) as $it){
            if(!is_array($it))$it=(array)$it;
            $id=gp_tmdb_cover_item_id($it,$type);$title=gp_tmdb_cover_item_title($it);$year=gp_tmdb_cover_item_year($it);
            if($id===''||$title==='')continue;$total++;
            $cache=gp_tmdb_content_cache_get($type,$id);
            if(is_array($cache)&&!empty($cache['tmdb_id'])&&!empty($cache['poster'])){
                if(gp_tmdb_shared_set($type,$title,$year,$cache))$shared++;
            }
        }
    }
    echo "provider={$pid} shared={$shared} scanned={$total}\n";
}
echo "FINAL providers={$providers} scanned={$total} shared={$shared}\n";
