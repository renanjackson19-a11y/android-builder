<?php
if(PHP_SAPI!=='cli'){http_response_code(403);exit("CLI only\n");}
set_time_limit(0);
ini_set('memory_limit','2048M');

$root='/var/www/greenplay/public_html';
$_SERVER['DOCUMENT_ROOT']=$root;
$_SERVER['HTTP_HOST']='localhost';
if(!defined('DOCUMENT_ROOT')) define('DOCUMENT_ROOT',$root);

require_once $root.'/config/config.php';
if(!function_exists('greenplay_providers')) require_once $root.'/model/stream/stream.php';
if(!function_exists('greenplay_m3u_lite_catalog')) require_once $root.'/model/stream/m3u.php';
require_once $root.'/model/stream/epg.php';

echo "===== PUBLIC LOGOS =====\n";
$idx=greenplay_epg_public_logo_index(true);
echo "channels=".(int)($idx['channels']??0)." aliases=".count((array)($idx['aliases']??array()))." ids=".count((array)($idx['by_id']??array()))."\n";

$c=greenplay_providers();
foreach((array)($c['providers']??array()) as $p){
    if((string)($p['enabled']??'1')!=='1') continue;
    $pid=(string)($p['id']??($p['provider_id']??''));
    if($pid==='') continue;
    $p['id']=$pid; $p['provider_id']=$pid;

    $live=array();
    if(function_exists('greenplay_provider_is_m3u') && greenplay_provider_is_m3u($p)){
        $cat=greenplay_m3u_lite_catalog($p,false);
        $live=(array)($cat['live']??array());
    }

    if(!$live){
        echo "provider={$pid} live=0 skip\n";
        continue;
    }

    echo "provider={$pid} live=".count($live)." rebuilding...\n";
    $st=greenplay_epg_provider_status($p,$live,true);
    echo "provider={$pid} logos=".(int)($st['logo_channels']??0)." total=".(int)($st['total_channels']??count($live))." coverage=".(string)($st['coverage_percent']??'')."\n";
}
echo "OK\n";
