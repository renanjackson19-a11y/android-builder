<?php
/* GREENPLAY TMDB COVER ON-DEMAND V2
 * TMDB-only + cache compartilhado entre provedores.
 */
$gpRoot=dirname(__DIR__,2);
require_once $gpRoot.'/config/tmdb.php';

if(!function_exists('gp_tmdb_cover_norm')){
function gp_tmdb_cover_norm($v){
    $v=trim((string)$v);
    if(function_exists('gp_tmdb_clean_title'))$v=gp_tmdb_clean_title($v);
    if(function_exists('iconv')){$x=@iconv('UTF-8','ASCII//TRANSLIT//IGNORE',$v);if($x!==false)$v=$x;}
    $v=strtolower($v);
    $v=preg_replace('/[^a-z0-9]+/',' ',$v);
    return trim(preg_replace('/\s+/',' ',$v));
}}

if(!function_exists('gp_tmdb_cover_item_id')){
function gp_tmdb_cover_item_id($it,$type){
    if(!is_array($it))$it=(array)$it;
    $id=$type==='series'
        ?($it['series_id']??($it['stream_id']??($it['id']??'')))
        :($it['stream_id']??($it['id']??''));
    return preg_replace('/[^0-9]/','',(string)$id);
}}

if(!function_exists('gp_tmdb_cover_item_title')){
function gp_tmdb_cover_item_title($it){
    if(!is_array($it))$it=(array)$it;
    return trim((string)($it['name']??($it['title']??'')));
}}

if(!function_exists('gp_tmdb_cover_item_year')){
function gp_tmdb_cover_item_year($it){
    if(!is_array($it))$it=(array)$it;
    return function_exists('gp_tmdb_year')?gp_tmdb_year((string)($it['year']??($it['release_date']??($it['releaseDate']??'')))):'';
}}

if(!function_exists('gp_tmdb_shared_dir')){
function gp_tmdb_shared_dir(){
    $d=dirname(__DIR__,2).'/cache/tmdb/shared';
    if(!is_dir($d))@mkdir($d,0775,true);
    return $d;
}}

if(!function_exists('gp_tmdb_shared_file')){
function gp_tmdb_shared_file($type,$title,$year=''){
    $type=$type==='series'?'series':'movie';
    $norm=gp_tmdb_cover_norm($title);
    $yr=function_exists('gp_tmdb_year')?gp_tmdb_year($year):'';
    if($norm==='')return '';
    return gp_tmdb_shared_dir().'/'.$type.'_'.sha1($norm.'|'.$yr).'.json';
}}

if(!function_exists('gp_tmdb_shared_get')){
function gp_tmdb_shared_get($type,$title,$year=''){
    $files=array();
    $f=gp_tmdb_shared_file($type,$title,$year);if($f!=='')$files[]=$f;
    $yr=function_exists('gp_tmdb_year')?gp_tmdb_year($year):'';
    if($yr!==''){$g=gp_tmdb_shared_file($type,$title,'');if($g!==''&&$g!==$f)$files[]=$g;}
    foreach($files as $path){
        if(!is_file($path))continue;
        $j=json_decode(@file_get_contents($path),true);
        if(!is_array($j)||empty($j['tmdb_id'])||empty($j['poster']))continue;
        if($yr!==''&&!empty($j['release_date'])){
            $cy=gp_tmdb_year((string)$j['release_date']);
            if($cy!==''&&abs((int)$cy-(int)$yr)>1)continue;
        }
        return $j;
    }
    return null;
}}

if(!function_exists('gp_tmdb_shared_set')){
function gp_tmdb_shared_set($type,$title,$year,$data){
    if(!is_array($data)||empty($data['tmdb_id'])||empty($data['poster']))return false;
    $targets=array_filter(array_unique(array(
        gp_tmdb_shared_file($type,$title,$year),
        gp_tmdb_shared_file($type,$title,'')
    )));
    $ok=false;$json=json_encode($data,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
    if($json===false)return false;
    foreach($targets as $f){
        $tmp=$f.'.tmp.'.getmypid();
        if(@file_put_contents($tmp,$json,LOCK_EX)!==false){@chmod($tmp,0664);if(!@rename($tmp,$f)){@copy($tmp,$f);@unlink($tmp);} $ok=true;}
    }
    return $ok;
}}

if(!function_exists('gp_tmdb_cover_pick')){
function gp_tmdb_cover_pick($json,$title,$year,$type){
    $rows=is_array($json['results']??null)?$json['results']:array();
    $want=gp_tmdb_cover_norm($title);$wantYear=gp_tmdb_year($year);$best=null;$bestScore=-1;
    foreach(array_slice($rows,0,12) as $i=>$r){
        if(!is_array($r)||empty($r['poster_path']))continue;
        $t=$type==='series'?(string)($r['name']??''):(string)($r['title']??'');
        $o=$type==='series'?(string)($r['original_name']??''):(string)($r['original_title']??'');
        $date=$type==='series'?(string)($r['first_air_date']??''):(string)($r['release_date']??'');
        $names=array_values(array_filter(array_unique(array(gp_tmdb_cover_norm($t),gp_tmdb_cover_norm($o)))));
        $score=0;$sim=0;
        foreach($names as $n){
            if($n===$want&&$want!==''){$score=max($score,200);continue;}
            $pct=0;similar_text($want,$n,$pct);$sim=max($sim,$pct);
            if($want!==''&&$n!==''&&(strpos($n,$want)!==false||strpos($want,$n)!==false))$score=max($score,120);
        }
        $score=max($score,$sim);
        $cy=gp_tmdb_year($date);
        if($wantYear!==''&&$cy!==''){
            $diff=abs((int)$wantYear-(int)$cy);
            if($diff===0)$score+=25;elseif($diff===1)$score+=8;else $score-=15;
        }
        $score+=max(0,6-(int)$i);
        if($score>$bestScore){$bestScore=$score;$best=$r;}
    }
    if(!$best)return null;
    if($bestScore<94)return null;
    return $best;
}}

if(!function_exists('gp_tmdb_cover_search_url')){
function gp_tmdb_cover_search_url($job,$type,$cfg,&$headers){
    $searchType=$type==='series'?'tv':'movie';
    $params=array('language'=>(string)($cfg['language']??'pt-BR'),'query'=>$job['title'],'include_adult'=>'false');
    $region=(string)($cfg['region']??'BR');if($region!=='')$params['region']=$region;
    $yr=gp_tmdb_year($job['year']);if($yr!==''){$params[$type==='series'?'first_air_date_year':'year']=$yr;}
    $token=(string)$cfg['token'];$mode=(string)($cfg['auth_mode']??'auto');if($mode==='auto')$mode=gp_tmdb_credential_mode($token);
    $headers=array('Accept: application/json','Connection: close');
    if($mode==='api_key_v3')$params['api_key']=$token;else $headers[]='Authorization: Bearer '.$token;
    return 'https://api.themoviedb.org/3/search/'.$searchType.'?'.http_build_query($params,'','&',PHP_QUERY_RFC3986);
}}

if(!function_exists('gp_tmdb_cover_batch')){
function gp_tmdb_cover_batch($items,$type,$limit=40){
    $type=$type==='series'?'series':'movie';$cfg=gp_tmdb_cfg();
    if(empty($cfg['enabled'])||empty($cfg['token']))return array('requested'=>0,'shared'=>0,'cached'=>0,'matched'=>0,'failed'=>0);
    $items=array_slice((array)$items,0,max(0,(int)$limit));
    $jobs=array();$cached=0;$shared=0;$matched=0;$failed=0;$requested=0;
    foreach($items as $it){
        if(!is_array($it))$it=(array)$it;
        $id=gp_tmdb_cover_item_id($it,$type);$title=gp_tmdb_cover_item_title($it);$year=gp_tmdb_cover_item_year($it);
        if($id===''||$title==='')continue;
        $existing=gp_tmdb_content_cache_get($type,$id);
        if(is_array($existing)&&!empty($existing['tmdb_id'])&&!empty($existing['poster'])){$cached++;gp_tmdb_shared_set($type,$title,$year,$existing);continue;}
        $reuse=gp_tmdb_shared_get($type,$title,$year);
        if(is_array($reuse)&&gp_tmdb_content_cache_set($type,$id,$reuse)){$shared++;continue;}
        $jobs[]=array('id'=>$id,'title'=>$title,'year'=>$year);
    }
    if(!$jobs)return array('requested'=>0,'shared'=>$shared,'cached'=>$cached,'matched'=>0,'failed'=>0);
    foreach(array_chunk($jobs,12) as $chunk){
        $mh=curl_multi_init();$handles=array();
        foreach($chunk as $i=>$job){
            $headers=array();$url=gp_tmdb_cover_search_url($job,$type,$cfg,$headers);$ch=curl_init();
            curl_setopt_array($ch,array(CURLOPT_URL=>$url,CURLOPT_RETURNTRANSFER=>true,CURLOPT_FOLLOWLOCATION=>true,CURLOPT_CONNECTTIMEOUT=>4,CURLOPT_TIMEOUT=>9,CURLOPT_SSL_VERIFYPEER=>true,CURLOPT_SSL_VERIFYHOST=>2,CURLOPT_HTTPHEADER=>$headers,CURLOPT_USERAGENT=>'GreenPlay-TMDB-OnDemand/2.1'));
            curl_multi_add_handle($mh,$ch);$handles[$i]=array('ch'=>$ch,'job'=>$job);$requested++;
        }
        $running=null;do{$mrc=curl_multi_exec($mh,$running);if($running){$n=curl_multi_select($mh,0.25);if($n===-1)usleep(50000);}}while($running&&$mrc===CURLM_OK);
        foreach($handles as $h){
            $ch=$h['ch'];$job=$h['job'];$raw=curl_multi_getcontent($ch);$http=(int)curl_getinfo($ch,CURLINFO_HTTP_CODE);$err=(int)curl_errno($ch);
            $json=(!$err&&$http>=200&&$http<300)?json_decode($raw,true):null;$pick=is_array($json)?gp_tmdb_cover_pick($json,$job['title'],$job['year'],$type):null;
            if($pick){
                $release=$type==='series'?(string)($pick['first_air_date']??''):(string)($pick['release_date']??'');
                $data=array('cache_version'=>4,'cover_cache_version'=>2,'tmdb_id'=>(int)($pick['id']??0),'title'=>$type==='series'?(string)($pick['name']??$job['title']):(string)($pick['title']??$job['title']),'original_title'=>$type==='series'?(string)($pick['original_name']??''):(string)($pick['original_title']??''),'poster'=>gp_tmdb_img($pick['poster_path']??'','w500'),'backdrop'=>gp_tmdb_img($pick['backdrop_path']??'','w1280'),'overview'=>(string)($pick['overview']??''),'release_date'=>$release,'year'=>gp_tmdb_year($release),'rating'=>(string)($pick['vote_average']??''),'genre'=>'','runtime_minutes'=>'','director'=>'','cast_list'=>array(),'cast'=>'');
                if(!empty($data['tmdb_id'])&&!empty($data['poster'])&&gp_tmdb_content_cache_set($type,$job['id'],$data)){
                    gp_tmdb_shared_set($type,$job['title'],$job['year'],$data);$matched++;
                }else $failed++;
            }else $failed++;
            curl_multi_remove_handle($mh,$ch);curl_close($ch);
        }
        curl_multi_close($mh);usleep(60000);
    }
    return array('requested'=>$requested,'shared'=>$shared,'cached'=>$cached,'matched'=>$matched,'failed'=>$failed);
}}
