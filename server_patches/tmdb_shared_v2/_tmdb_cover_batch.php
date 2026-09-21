<?php
/* GREENPLAY TMDB COVER ON-DEMAND V2.7
 * TMDB-only + cache compartilhado entre provedores.
 * Busca resiliente para nomes de listas IPTV:
 * - remove marcadores técnicos/numeração
 * - extrai ano do próprio título
 * - tenta aliases separados por " - "
 * - com ano conhecido, tenta versões curtas do título
 * - aceita resultado único somente com critérios seguros
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

if(!function_exists('gp_tmdb_cover_year_from_text')){
function gp_tmdb_cover_year_from_text($v){
    if(preg_match('/(?:^|[^0-9])((?:19|20)[0-9]{2})(?:[^0-9]|$)/',(string)$v,$m))return (string)$m[1];
    return '';
}}

if(!function_exists('gp_tmdb_cover_item_year')){
function gp_tmdb_cover_item_year($it){
    if(!is_array($it))$it=(array)$it;
    $v=(string)($it['year']??($it['release_date']??($it['releaseDate']??'')));
    $y=function_exists('gp_tmdb_year')?gp_tmdb_year($v):'';
    if($y!=='')return $y;
    return gp_tmdb_cover_year_from_text((string)($it['name']??($it['title']??'')));
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
    $yr=function_exists('gp_tmdb_year')?gp_tmdb_year($year):'';
    $titles=array($title);
    if(function_exists('gp_tmdb_cover_search_title')){
        $clean=gp_tmdb_cover_search_title($title);
        if($clean!=='' && gp_tmdb_cover_norm($clean)!==gp_tmdb_cover_norm($title))$titles[]=$clean;
    }
    foreach(array_unique($titles) as $tt){
        $f=gp_tmdb_shared_file($type,$tt,$year);if($f!=='')$files[]=$f;
        if($yr!==''){$g=gp_tmdb_shared_file($type,$tt,'');if($g!=='')$files[]=$g;}
    }
    $files=array_values(array_unique($files));
    foreach($files as $path){
        if(!is_file($path))continue;
        $j=json_decode(@file_get_contents($path),true);
        if(!is_array($j)||empty($j['tmdb_id'])||empty($j['poster']))continue;
        if($yr!==''){
            $cy=gp_tmdb_year((string)($j['year']??($j['release_date']??'')));
            // Com ano conhecido na fonte, cache compartilhado sem ano não é confiável.
            // Também rejeita obra de época distante; tolerância de 3 anos cobre lançamentos regionais.
            if($cy===''||abs((int)$cy-(int)$yr)>3)continue;
        }
        return $j;
    }
    return null;
}}

if(!function_exists('gp_tmdb_shared_set')){
function gp_tmdb_shared_set($type,$title,$year,$data){
    if(!is_array($data)||empty($data['tmdb_id'])||empty($data['poster']))return false;
    $titles=array($title);
    if(function_exists('gp_tmdb_cover_search_title')){
        $clean=gp_tmdb_cover_search_title($title);
        if($clean!=='' && gp_tmdb_cover_norm($clean)!==gp_tmdb_cover_norm($title))$titles[]=$clean;
    }
    $targets=array();
    foreach(array_unique($titles) as $tt){
        $targets[]=gp_tmdb_shared_file($type,$tt,$year);
        $targets[]=gp_tmdb_shared_file($type,$tt,'');
    }
    $targets=array_filter(array_unique($targets));
    $ok=false;$json=json_encode($data,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
    if($json===false)return false;
    foreach($targets as $f){
        $tmp=$f.'.tmp.'.getmypid();
        if(@file_put_contents($tmp,$json,LOCK_EX)!==false){@chmod($tmp,0664);if(!@rename($tmp,$f)){@copy($tmp,$f);@unlink($tmp);} $ok=true;}
    }
    return $ok;
}}

if(!function_exists('gp_tmdb_cover_search_title')){
function gp_tmdb_cover_search_title($title){
    $q=trim((string)$title);
    if(function_exists('gp_tmdb_clean_title')){
        $x=trim((string)gp_tmdb_clean_title($q));
        if($x!=='')$q=$x;
    }
    $q=preg_replace('/[\[\(\{][^\]\)\}]{0,50}(?:dublad[oa]|dublagem|legendad[oa]|dual(?: audio)?|pt[- ]?br|portugu[eê]s|4k|2160p|1080p|720p|480p|fhd|uhd|hdr10?|dolby|web[- .]?dl|web[- .]?rip|blu[- .]?ray|bluray|bdrip|dvdrip|h\.?26[45]|hevc|x26[45]|aac|ac3|eac3|adulto|xxx|mex|arabe|iraque|espanhol|ma)[^\]\)\}]{0,50}[\]\)\}]/iu',' ',$q);
    $q=preg_replace('/\[(?:L|DUB|LEG|MEX|MA)\b[^\]]*$/iu',' ',$q);
    $q=preg_replace('/\b(?:dublad[oa]|legendad[oa]|dual(?:\s+audio)?|pt[- ]?br|4k|2160p|1080p|720p|480p|fhd|uhd|hdr10?|web[- .]?dl|web[- .]?rip|blu[- .]?ray|bluray|bdrip|dvdrip|h\.?26[45]|hevc|x26[45]|aac|ac3|eac3)\b/iu',' ',$q);
    $q=preg_replace('/\bS\d{1,2}\s*E\d{1,3}\b/iu',' ',$q);
    $q=preg_replace('/\b(?:temporada|season)\s*\d{1,2}\b/iu',' ',$q);
    $q=preg_replace('/\s*\((?:19|20)\d{2}\)\s*$/u',' ',$q);
    // Remove rótulos de plataforma usados pela lista.
    $q=preg_replace('/[\[\(](?:netflix|globoplay|globo\s*play|hbo\s*max|max|paramount\+?|prime\s*video|amazon\s*prime|disney\+?|star\+?|apple\s*tv\+?|sbt\+?|crunchyroll|directv|discovery\+?)[\]\)]/iu',' ',$q);
    $q=preg_replace('/\s*[-–—|:]\s*(?:netflix|globoplay|globo\s*play|hbo\s*max|max|paramount\+?|prime\s*video|amazon\s*prime|disney\+?|star\+?|apple\s*tv\+?|sbt\+?|crunchyroll|directv|discovery\+?)\s*$/iu',' ',$q);
    $q=preg_replace('/^\s*\d{1,3}\s*[-.:|]\s*/u','',$q);
    $q=preg_replace('/^[\s\-–—_|:]+|[\s\-–—_|:]+$/u','',$q);
    $q=preg_replace('/\s{2,}/u',' ',$q);
    return trim($q);
}}

if(!function_exists('gp_tmdb_cover_candidates')){
function gp_tmdb_cover_candidates($title,$year=''){
    $base=gp_tmdb_cover_search_title($title);
    $out=array();
    $add=function($v)use(&$out){
        $v=trim(preg_replace('/\s{2,}/u',' ',(string)$v));
        $n=gp_tmdb_cover_norm($v);
        if($v===''||$n===''||strlen($n)<3)return;
        foreach($out as $old){if(gp_tmdb_cover_norm($old)===$n)return;}
        $out[]=$v;
    };
    $add($base);

    // Títulos de doramas/novelas costumam trazer tradução + nome original separados por hífen.
    $parts=preg_split('/\s+[-–—]\s+/u',$base);
    if(is_array($parts)&&count($parts)>1){
        for($i=count($parts)-1;$i>=0;$i--){
            $p=trim((string)$parts[$i]);
            $words=preg_split('/\s+/u',$p,-1,PREG_SPLIT_NO_EMPTY);
            if(strlen(gp_tmdb_cover_norm($p))>=5 && count($words)<=10)$add($p);
        }
    }

    $yr=function_exists('gp_tmdb_year')?gp_tmdb_year($year):'';
    $words=preg_split('/\s+/u',$base,-1,PREG_SPLIT_NO_EMPTY);
    $cnt=count($words);

    // Variante sem a conjunção "e": ajuda nomes como "Law e Order Crime Organizado".
    if($cnt>=3){
        $noE=preg_replace('/\s+e\s+/iu',' ',$base);
        if($noE!==$base)$add($noE);
    }

    // Tenta prefixos e sufixos úteis mesmo sem ano.
    foreach(array(5,4,3,2) as $n){
        if($cnt>$n){
            $first=implode(' ',array_slice($words,0,$n));
            $last=implode(' ',array_slice($words,-$n));
            if(strlen(gp_tmdb_cover_norm($first))>=7)$add($first);
            if(strlen(gp_tmdb_cover_norm($last))>=7)$add($last);
        }
    }

    // Com ano conhecido podemos tentar também uma palavra distintiva.
    if($yr!=='' && $cnt>1){
        $one=(string)$words[0];
        if(strlen(gp_tmdb_cover_norm($one))>=5)$add($one);
    }

    return array_slice($out,0,12);
}}

if(!function_exists('gp_tmdb_cover_pick')){
function gp_tmdb_cover_pick($json,$title,$year,$type,$queryUsed=''){
    $rows=is_array($json['results']??null)?$json['results']:array();
    $full=gp_tmdb_cover_norm(gp_tmdb_cover_search_title($title));
    $query=gp_tmdb_cover_norm($queryUsed!==''?$queryUsed:$title);
    $wantYear=gp_tmdb_year($year);
    $best=null;$bestScore=-1;$bestYear='';
    foreach(array_slice($rows,0,12) as $i=>$r){
        if(!is_array($r)||(empty($r['poster_path'])&&empty($r['backdrop_path'])))continue;
        $t=$type==='series'?(string)($r['name']??''):(string)($r['title']??'');
        $o=$type==='series'?(string)($r['original_name']??''):(string)($r['original_title']??'');
        $date=$type==='series'?(string)($r['first_air_date']??''):(string)($r['release_date']??'');
        $names=array_values(array_filter(array_unique(array(gp_tmdb_cover_norm($t),gp_tmdb_cover_norm($o)))));
        $score=0;
        foreach($names as $n){
            foreach(array($full,$query) as $want){
                if($want===''||$n==='')continue;
                if($n===$want){$score=max($score,220);continue;}
                if(strpos($n,$want)!==false||strpos($want,$n)!==false){
                    $score=max($score,$want===$full?150:92);
                }
                $pct=0;similar_text($want,$n,$pct);$score=max($score,$pct);
            }
        }
        $cy=gp_tmdb_year($date);
        if($wantYear!==''){
            if($cy===''){
                // Sem ano no resultado, não aceite match frouxo quando a fonte tem ano.
                // Só um match textual exato do título completo pode sobreviver.
                $exactFull=false;
                foreach($names as $n){if($full!==''&&$n===$full){$exactFull=true;break;}}
                if(!$exactFull)continue;
            }else{
                $diff=abs((int)$wantYear-(int)$cy);
                // Segurança: com ano conhecido, não aceitar obra de época diferente.
                // Tolerância de 3 anos cobre lançamentos regionais tardios.
                if($diff>3)continue;
                if($diff===0)$score+=40;
                elseif($diff===1)$score+=18;
                else $score+=5;
            }
        }
        $score+=max(0,6-(int)$i);
        if($score>$bestScore){$bestScore=$score;$best=$r;$bestYear=$cy;}
    }
    if(!$best)return null;
    if($bestScore>=94)return $best;

    // Resultado único: aceitar apenas em cenários relativamente seguros.
    $usable=array_values(array_filter($rows,function($r){return is_array($r)&&(!empty($r['poster_path'])||!empty($r['backdrop_path']));}));
    if(count($usable)===1){
        if($wantYear!=='' && $bestYear!=='' && $wantYear===$bestYear)return $best;
        if($wantYear===''){
            $words=preg_split('/\s+/u',$query,-1,PREG_SPLIT_NO_EMPTY);
            $maxLen=0;foreach($words as $w)$maxLen=max($maxLen,strlen($w));
            if(count($words)>=3 || $maxLen>=10)return $best;
        }
    }
    return null;
}}

if(!function_exists('gp_tmdb_cover_search_url')){
function gp_tmdb_cover_search_url($query,$type,$cfg,&$headers,$yearFilter=''){
    $searchType=$type==='series'?'tv':'movie';
    $params=array(
        'language'=>(string)($cfg['language']??'pt-BR'),
        'query'=>trim((string)$query),
        'include_adult'=>'false'
    );
    $region=(string)($cfg['region']??'BR');if($region!=='')$params['region']=$region;
    $yf=function_exists('gp_tmdb_year')?gp_tmdb_year($yearFilter):'';
    if($yf!=='')$params[$type==='series'?'first_air_date_year':'year']=$yf;
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
        $id=gp_tmdb_cover_item_id($it,$type);
        $title=gp_tmdb_cover_item_title($it);
        $year=gp_tmdb_cover_item_year($it);
        if($id===''||$title==='')continue;

        // Conteúdo adulto explícito não é consultado porque include_adult=false e o TMDB não é fonte confiável para esse catálogo.
        if(preg_match('/(?:^|\s)\[?XXX\]?|\[Adulto\]/iu',$title)){$failed++;continue;}

        $existing=gp_tmdb_content_cache_get($type,$id);
        if(is_array($existing)&&!empty($existing['tmdb_id'])){
            if(empty($existing['poster'])&&!empty($existing['backdrop'])){
                // TMDB pode ter backdrop sem poster. Para o card, use a própria imagem TMDB
                // como fallback em vez de deixar o bloco vazio.
                $existing['poster']=$existing['backdrop'];
                $existing['cover_cache_version']=7;
                gp_tmdb_content_cache_set($type,$id,$existing);
            }
            if(!empty($existing['poster'])){
                $cached++;gp_tmdb_shared_set($type,$title,$year,$existing);continue;
            }
        }

        $reuse=gp_tmdb_shared_get($type,$title,$year);
        if(is_array($reuse)&&gp_tmdb_content_cache_set($type,$id,$reuse)){$shared++;continue;}

        $cands=gp_tmdb_cover_candidates($title,$year);
        if(!$cands){$failed++;continue;}
        $attempts=array();
        foreach($cands as $cand){
            if($year!=='')$attempts[]=array('query'=>$cand,'year'=>$year);
            $attempts[]=array('query'=>$cand,'year'=>'');
            if(count($attempts)>=10)break;
        }
        $jobs[$id]=array('id'=>$id,'title'=>$title,'year'=>$year,'attempts'=>$attempts,'idx'=>0,'done'=>false);
    }

    if(!$jobs)return array('requested'=>0,'shared'=>$shared,'cached'=>$cached,'matched'=>0,'failed'=>$failed);

    $maxRounds=10;
    for($round=0;$round<$maxRounds;$round++){
        $todo=array();
        foreach($jobs as $id=>$job){
            if(!empty($job['done']))continue;
            $idx=(int)$job['idx'];
            if(!isset($job['attempts'][$idx]))continue;
            $todo[$id]=$job;
        }
        if(!$todo)break;

        foreach(array_chunk($todo,4,true) as $chunk){
            $mh=curl_multi_init();$handles=array();

            foreach($chunk as $id=>$job){
                $idx=(int)$job['idx'];
                $attempt=$job['attempts'][$idx];
                $query=(string)$attempt['query'];
                $yearFilter=(string)$attempt['year'];
                $headers=array();$url=gp_tmdb_cover_search_url($query,$type,$cfg,$headers,$yearFilter);$ch=curl_init();
                curl_setopt_array($ch,array(
                    CURLOPT_URL=>$url,
                    CURLOPT_RETURNTRANSFER=>true,
                    CURLOPT_FOLLOWLOCATION=>true,
                    CURLOPT_CONNECTTIMEOUT=>4,
                    CURLOPT_TIMEOUT=>9,
                    CURLOPT_SSL_VERIFYPEER=>true,
                    CURLOPT_SSL_VERIFYHOST=>2,
                    CURLOPT_HTTPHEADER=>$headers,
                    CURLOPT_USERAGENT=>'GreenPlay-TMDB-OnDemand/2.7'
                ));
                curl_multi_add_handle($mh,$ch);
                $handles[$id]=array('ch'=>$ch,'query'=>$query);
                $requested++;
            }

            $running=null;
            do{
                $mrc=curl_multi_exec($mh,$running);
                if($running){$n=curl_multi_select($mh,0.25);if($n===-1)usleep(50000);}
            }while($running&&$mrc===CURLM_OK);

            foreach($handles as $id=>$h){
                $ch=$h['ch'];$query=$h['query'];$job=$jobs[$id];
                $raw=curl_multi_getcontent($ch);
                $http=(int)curl_getinfo($ch,CURLINFO_HTTP_CODE);
                $err=(int)curl_errno($ch);

                $json=(!$err&&$http>=200&&$http<300)?json_decode($raw,true):null;
                $pick=is_array($json)?gp_tmdb_cover_pick($json,$job['title'],$job['year'],$type,$query):null;

                if($pick){
                    $release=$type==='series'?(string)($pick['first_air_date']??''):(string)($pick['release_date']??'');
                    $data=array(
                        'cache_version'=>4,
                        'cover_cache_version'=>7,
                        'tmdb_id'=>(int)($pick['id']??0),
                        'title'=>$type==='series'?(string)($pick['name']??$job['title']):(string)($pick['title']??$job['title']),
                        'original_title'=>$type==='series'?(string)($pick['original_name']??''):(string)($pick['original_title']??''),
                        'poster'=>gp_tmdb_img(!empty($pick['poster_path'])?$pick['poster_path']:($pick['backdrop_path']??''),'w500'),
                        'backdrop'=>gp_tmdb_img($pick['backdrop_path']??($pick['poster_path']??''),'w1280'),
                        'overview'=>(string)($pick['overview']??''),
                        'release_date'=>$release,
                        'year'=>gp_tmdb_year($release),
                        'rating'=>(string)($pick['vote_average']??''),
                        'genre'=>'',
                        'runtime_minutes'=>'',
                        'director'=>'',
                        'cast_list'=>array(),
                        'cast'=>''
                    );
                    if(!empty($data['tmdb_id'])&&!empty($data['poster'])&&gp_tmdb_content_cache_set($type,$job['id'],$data)){
                        gp_tmdb_shared_set($type,$job['title'],$job['year'],$data);
                        $matched++;$jobs[$id]['done']=true;
                    }else{
                        $jobs[$id]['idx']++;
                    }
                }else{
                    $jobs[$id]['idx']++;
                }

                curl_multi_remove_handle($mh,$ch);curl_close($ch);
            }

            curl_multi_close($mh);
            usleep(280000);
        }
    }

    foreach($jobs as $job){
        if(empty($job['done']))$failed++;
    }

    return array(
        'requested'=>$requested,
        'shared'=>$shared,
        'cached'=>$cached,
        'matched'=>$matched,
        'failed'=>$failed
    );
}}
