<?php
/**
 * GREENPLAY TMDB V2.8 CLEANUP
 * Remove apenas caches gerados pelas versões permissivas 2.6/2.7
 * (cover_cache_version 6 ou 7), tanto por provedor quanto compartilhados.
 * Os caches anteriores bons são preservados.
 */
if(PHP_SAPI!=='cli'){http_response_code(403);exit("CLI only\n");}
set_time_limit(0);
ini_set('memory_limit','1024M');

$root='/var/www/greenplay/public_html';
$removedContent=0;
$removedShared=0;

$dirs=array(
    $root.'/cache/tmdb/content',
    $root.'/cache/tmdb/shared'
);

$scan=function($base,$shared=false)use(&$removedContent,&$removedShared){
    if(!is_dir($base))return;

    $it=new RecursiveIteratorIterator(
        new RecursiveDirectoryIterator($base,FilesystemIterator::SKIP_DOTS)
    );

    foreach($it as $f){
        if(!$f->isFile())continue;
        if(strtolower($f->getExtension())!=='json')continue;

        $path=$f->getPathname();
        $j=json_decode(@file_get_contents($path),true);
        if(!is_array($j))continue;

        $cv=(int)($j['cover_cache_version']??0);
        if($cv!==6 && $cv!==7)continue;

        if(@unlink($path)){
            if($shared)$removedShared++;
            else $removedContent++;
        }
    }
};

$scan($root.'/cache/tmdb/content',false);
$scan($root.'/cache/tmdb/shared',true);

echo "FINAL removed_content={$removedContent} removed_shared={$removedShared}\n";
