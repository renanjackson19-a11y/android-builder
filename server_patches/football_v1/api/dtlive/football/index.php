<?php
/* GreenPlay Football V1 - API-Football proxy/cache */
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, max-age=0');

$root = '/var/www/greenplay/public_html';
$cfgFile = $root.'/config/football.php';
$cacheDir = $root.'/cache/football';

function gp_fb_json($status, $data=array(), $http=200){
    http_response_code($http);
    echo json_encode(array_merge(array('status'=>$status), $data), JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
    exit;
}
function gp_fb_input(){
    $in=array();
    $raw=@file_get_contents('php://input');
    if(is_string($raw)&&trim($raw)!==''){
        $j=json_decode($raw,true);
        if(is_array($j)) $in=$j;
    }
    foreach($_GET as $k=>$v) if(!array_key_exists($k,$in)) $in[$k]=$v;
    foreach($_POST as $k=>$v) if(!array_key_exists($k,$in)) $in[$k]=$v;
    return $in;
}
function gp_fb_cfg($file){
    if(!is_file($file)) return array();
    $v=require $file;
    return is_array($v)?$v:array();
}
function gp_fb_http($url,$key,$timeout=18){
    $ch=curl_init($url);
    curl_setopt_array($ch,array(
        CURLOPT_RETURNTRANSFER=>true,
        CURLOPT_FOLLOWLOCATION=>true,
        CURLOPT_CONNECTTIMEOUT=>8,
        CURLOPT_TIMEOUT=>$timeout,
        CURLOPT_HTTPHEADER=>array('x-apisports-key: '.$key,'Accept: application/json'),
        CURLOPT_USERAGENT=>'GreenPlay-Football/1.0'
    ));
    $body=curl_exec($ch);
    $err=curl_error($ch);
    $code=(int)curl_getinfo($ch,CURLINFO_HTTP_CODE);
    curl_close($ch);
    return array('ok'=>$code>=200&&$code<300&&is_string($body)&&$body!=='','http'=>$code,'body'=>(string)$body,'error'=>$err);
}
function gp_fb_status_text($short,$long=''){
    $map=array(
        'TBD'=>'A definir','NS'=>'Não começou','1H'=>'1º tempo','HT'=>'Intervalo','2H'=>'2º tempo','ET'=>'Prorrogação',
        'BT'=>'Intervalo da prorrogação','P'=>'Pênaltis','SUSP'=>'Suspenso','INT'=>'Interrompido','FT'=>'Encerrado','AET'=>'Encerrado após prorrogação',
        'PEN'=>'Encerrado nos pênaltis','PST'=>'Adiado','CANC'=>'Cancelado','ABD'=>'Abandonado','AWD'=>'Resultado administrativo','WO'=>'W.O.','LIVE'=>'Ao vivo'
    );
    return isset($map[$short])?$map[$short]:($long!==''?$long:$short);
}
function gp_fb_row($x){
    $f=(array)($x['fixture']??array());
    $lg=(array)($x['league']??array());
    $tm=(array)($x['teams']??array());
    $go=(array)($x['goals']??array());
    $sc=(array)($x['score']??array());
    $st=(array)($f['status']??array());
    $home=(array)($tm['home']??array());
    $away=(array)($tm['away']??array());
    $short=(string)($st['short']??'');
    $live=in_array($short,array('1H','HT','2H','ET','BT','P','LIVE'),true);
    return array(
        'fixture_id'=>(int)($f['id']??0),
        'timestamp'=>(int)($f['timestamp']??0),
        'date'=>(string)($f['date']??''),
        'timezone'=>(string)($f['timezone']??''),
        'venue'=>array('name'=>(string)(($f['venue']['name']??'')),'city'=>(string)(($f['venue']['city']??''))),
        'status_short'=>$short,
        'status'=>gp_fb_status_text($short,(string)($st['long']??'')),
        'elapsed'=>isset($st['elapsed'])?(int)$st['elapsed']:null,
        'live'=>$live,
        'league'=>array(
            'id'=>(int)($lg['id']??0),'name'=>(string)($lg['name']??''),'country'=>(string)($lg['country']??''),
            'logo'=>(string)($lg['logo']??''),'flag'=>(string)($lg['flag']??''),'season'=>$lg['season']??null,'round'=>(string)($lg['round']??'')
        ),
        'home'=>array('id'=>(int)($home['id']??0),'name'=>(string)($home['name']??''),'logo'=>(string)($home['logo']??''),'winner'=>$home['winner']??null,'goals'=>$go['home']??null),
        'away'=>array('id'=>(int)($away['id']??0),'name'=>(string)($away['name']??''),'logo'=>(string)($away['logo']??''),'winner'=>$away['winner']??null,'goals'=>$go['away']??null),
        'score'=>array('halftime'=>$sc['halftime']??null,'fulltime'=>$sc['fulltime']??null,'extratime'=>$sc['extratime']??null,'penalty'=>$sc['penalty']??null)
    );
}
function gp_fb_country_priority($country){
    $c=strtolower(trim((string)$country));
    if($c==='brazil'||$c==='brasil') return 0;
    if($c==='world') return 1;
    if(in_array($c,array('england','spain','italy','germany','france','portugal'),true)) return 2;
    return 3;
}

$cfg=gp_fb_cfg($cfgFile);
$key=trim((string)($cfg['api_key']??getenv('GREENPLAY_API_FOOTBALL_KEY')));
if($key==='') gp_fb_json(503,array('message'=>'API de futebol ainda não configurada','code'=>'football_key_missing'),503);
$timezone=trim((string)($cfg['timezone']??'America/Sao_Paulo'));
if($timezone==='') $timezone='America/Sao_Paulo';
$input=gp_fb_input();
$date=trim((string)($input['date']??''));
if(!preg_match('/^\d{4}-\d{2}-\d{2}$/',$date)){
    try{$d=new DateTime('now',new DateTimeZone($timezone));$date=$d->format('Y-m-d');}catch(Throwable $e){$date=date('Y-m-d');}
}
$force=!empty($input['force']) && in_array(strtolower((string)$input['force']),array('1','true','yes'),true);
@mkdir($cacheDir,0775,true);
$cache=$cacheDir.'/fixtures_'.$date.'.json';
$now=time();
$today='';try{$today=(new DateTime('now',new DateTimeZone($timezone)))->format('Y-m-d');}catch(Throwable $e){$today=date('Y-m-d');}
$ttl=($date===$today)?max(900,(int)($cfg['today_ttl']??1200)):max(3600,(int)($cfg['other_ttl']??21600));

if(!$force && is_file($cache) && ($now-(int)@filemtime($cache))<$ttl){
    $cached=@file_get_contents($cache);
    $j=$cached?json_decode($cached,true):null;
    if(is_array($j)){
        $j['cached']=true;$j['cache_age']=$now-(int)@filemtime($cache);
        gp_fb_json(200,$j,200);
    }
}

$url='https://v3.football.api-sports.io/fixtures?date='.rawurlencode($date).'&timezone='.rawurlencode($timezone);
$r=gp_fb_http($url,$key,22);
if(!$r['ok']){
    if(is_file($cache)){
        $cached=@file_get_contents($cache);$j=$cached?json_decode($cached,true):null;
        if(is_array($j)){$j['cached']=true;$j['stale']=true;$j['upstream_error']=$r['error']!==''?$r['error']:'HTTP '.$r['http'];gp_fb_json(200,$j,200);}
    }
    gp_fb_json(502,array('message'=>'Falha ao consultar jogos','upstream_http'=>$r['http'],'error'=>$r['error']),502);
}
$j=json_decode($r['body'],true);
if(!is_array($j)) gp_fb_json(502,array('message'=>'Resposta inválida da API de futebol'),502);
if(!empty($j['errors'])){
    gp_fb_json(502,array('message'=>'API de futebol retornou erro','errors'=>$j['errors']),502);
}
$rows=array();
foreach((array)($j['response']??array()) as $x){if(is_array($x))$rows[]=gp_fb_row($x);}
usort($rows,function($a,$b){
    $pa=gp_fb_country_priority($a['league']['country']??'');$pb=gp_fb_country_priority($b['league']['country']??'');
    if($pa!==$pb)return $pa<=>$pb;
    $ta=(int)($a['timestamp']??0);$tb=(int)($b['timestamp']??0);
    if($ta!==$tb)return $ta<=>$tb;
    return strcmp((string)($a['league']['name']??''),(string)($b['league']['name']??''));
});
$out=array(
    'message'=>'ok','date'=>$date,'timezone'=>$timezone,'generated_at'=>$now,'cached'=>false,'cache_ttl'=>$ttl,
    'count'=>count($rows),'result'=>$rows,
    'source'=>'api-football'
);
$tmp=$cache.'.tmp.'.getmypid();
@file_put_contents($tmp,json_encode($out,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),LOCK_EX);
@chmod($tmp,0664);@rename($tmp,$cache);
gp_fb_json(200,$out,200);
