from pathlib import Path
import sys

p = Path("/var/www/greenplay/public_html/model/stream/epg.php")
if not p.is_file():
    raise SystemExit("epg.php nao encontrado")

s = p.read_text()

start = s.find("function greenplay_epg_canonical_logo_for_request(")
end = s.find("function greenplay_epg_status_signature(", start)
if start < 0 or end < 0:
    raise SystemExit("Funcoes de logo nao encontradas")

new = r'''function greenplay_epg_logo_request_names($request){
    if(!is_array($request)) return array();

    $out=array();

    /*
     * GREENPLAY LOGO SAFE V88.1
     * NUNCA usa tvg-id/epg-id para descobrir o nome visual do canal.
     * O provedor pode mandar um ID de outra emissora.
     */
    foreach(array('name','channel_name','stream_name') as $k){
        $raw=trim((string)($request[$k]??''));
        if($raw==='') continue;

        foreach(greenplay_epg_name_variants($raw) as $n){
            $n=trim((string)$n);
            if($n!=='') $out[$n]=true;
        }
    }

    return array_keys($out);
}

function greenplay_epg_canonical_logo_for_request($request){
    if(!is_array($request)) return '';

    /*
     * IMPORTANTISSIMO:
     * aqui usamos SOMENTE nomes reais do canal.
     * tvg-id fica completamente fora desta funcao.
     */
    $names=greenplay_epg_logo_request_names($request);

    $br='https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/brazil/';
    $media='https://raw.githubusercontent.com/tv-logo/tv-logos/main/misc/media/';
    $commons=function($file){
        return 'https://commons.wikimedia.org/wiki/Special:Redirect/file/'.rawurlencode($file);
    };

    foreach($names as $name){
        $n=strtolower(preg_replace('/[^a-z0-9]+/','',(string)$name));
        if($n==='') continue;

        /*
         * Remove marcadores tecnicos apenas no final.
         */
        do{
            $old=$n;
            $n=preg_replace('/(?:fullhd|fhd|uhd|hd|sd|4k|h265|hevc|alt)$/','',$n);
        }while($old!==$n);

        /* BAND */
        if(preg_match('/^bandnews/',$n)) return $br.'band-news-br.png';
        if(preg_match('/^bandsports?/',$n)) return $br.'band-sports-br.png';
        if(preg_match('/^band(?:internacional|international)/',$n)) return $br.'band-internacional-br.png';
        if(preg_match('/^band(?:brasilia|df|sp|rj|mg|ba|bahia|pe|pr|parana|rs|sc|ce|ceara|pb|rn|al|se|ma|pi|pa|am|ro|rr|ap|ac|to|campinas|minas|nacional)?$/',$n)) return $br.'band-br.png';

        /* SBT */
        if(preg_match('/^sbtnews/',$n)) continue;
        if(preg_match('/^sbt(?:sp|rj|rs|sc|df|brasilia|goias|goiania|recife|bahia|nordeste|norte|sul|sudeste|centrooeste|nacional)?$/',$n)) return $br.'sbt-br.png';

        /* RECORD */
        if(preg_match('/^recordnews/',$n)) return $br.'record-news-br.png';
        if(preg_match('/^(?:record|recordtv)(?:sp|rio|rj|rs|sc|df|brasilia|goias|goiania|bahia|nordeste|norte|sul|sudeste|centrooeste|nacional)?$/',$n)) return $br.'record-br.png';

        /* GLOBO */
        if(preg_match('/^globonews/',$n)) return $br.'globo-news-br.png';
        if(preg_match('/^globoplaynovelas/',$n)) return $br.'globoplay-novelas-br.png';
        if(preg_match('/^tvbahia/',$n)) return $br.'tv-bahia-br.png';
        if(preg_match('/^(?:intertv|redeintertv)/',$n)) return $br.'rede-inter-tv-br.png';
        if(preg_match('/^globo/',$n)) return $br.'globo-br.png';

        /* CNN */
        if($n==='cnnbrasilmoney' || $n==='cnnmoney') return $br.'cnn-brasil-money-br.png';
        if($n==='cnn' || $n==='cnnbrasil') return $br.'cnn-brasil-br.png';
        if(preg_match('/^cnninternational/',$n)) return $commons('CNNinternational-logo.png');

        /* ESPN - PNGs conhecidos; demais ainda podem vir do indice publico exato */
        if(preg_match('/^espn2$/',$n)) return $commons('Espn 2.png');
        if(preg_match('/^espn3$/',$n)) return $commons('Espn3.png');
        if(preg_match('/^espn4$/',$n)) return $br.'espn-4-br.png';
        if(preg_match('/^espn5$/',$n)) return $br.'espn-5-br.png';
        if($n==='espn') return $commons('ESPN logo.png');

        /* SPORTV */
        if(preg_match('/^sportv3$/',$n)) return $br.'sportv3-br.png';
        if(preg_match('/^sportv2$/',$n)) return $br.'sportv2-br.png';
        if($n==='sportv') return $br.'sportv-br.png';

        /* UNIVERSAL */
        if(preg_match('/^universal(?:tv|premiere)?$/',$n)) return $br.'universal-tv-br.png';

        /* HBO */
        if(preg_match('/^hboxtreme/',$n)) return $br.'hbo-xtreme-br.png';
        if(preg_match('/^hbosignature/',$n)) return $br.'hbo-signature-br.png';
        if(preg_match('/^hbopop/',$n)) return $br.'hbo-pop-br.png';
        if(preg_match('/^hboplus/',$n)) return $br.'hbo-plus-br.png';
        if(preg_match('/^hbofamily/',$n)) return $br.'hbo-family-br.png';
        if(preg_match('/^hbomundi/',$n)) return $br.'hbo-mundi-br.png';
        if(preg_match('/^hbo2/',$n)) return $br.'hbo-2-br.png';
        if($n==='hbo') return $br.'hbo-br.png';

        /* TELECINE */
        if(preg_match('/^telecinepremium/',$n)) return $br.'tele-cine-premium-br.png';
        if(preg_match('/^telecinepipoca/',$n)) return $br.'tele-cine-pipoca-br.png';
        if(preg_match('/^telecinetouch/',$n)) return $br.'tele-cine-touch-br.png';
        if(preg_match('/^telecineaction/',$n)) return $br.'tele-cine-action-br.png';
        if(preg_match('/^telecinecult/',$n)) return $br.'tele-cine-cult-br.png';
        if(preg_match('/^telecinefun/',$n)) return $br.'tele-cine-fun-br.png';

        /* OUTROS CANAIS COM LOGO VERIFICADA NO CATALOGO */
        if(preg_match('/^gnt$/',$n)) return $br.'gnt-br.png';
        if(preg_match('/^discoverykids/',$n)) return $br.'discovery-kids-br.png';
        if(preg_match('/^discoveryturbo/',$n)) return $br.'discovery-turbo-br.png';
        if(preg_match('/^discoveryworld/',$n)) return $commons('Discovery World logo.png');
        if(preg_match('/^discovery(?:channel)?$/',$n)) return $commons('Discovery Channel.png');
        if(preg_match('/^discovery(?:homeandhealth|homehealth|hh)/',$n)) return $commons('Discovery Home & Health.png');
        if(preg_match('/^nickelodeon/',$n)) return $commons('NICK2023.png');
        if(preg_match('/^nick(?:jr|junior)/',$n)) return $commons('Nick Jr. logo 2023 (alternative).png');
        if(preg_match('/^tooncast/',$n)) return $br.'tooncast-br.png';
        if(preg_match('/^cartoonnetwork/',$n)) return $br.'cartoon-network-br.png';
        if(preg_match('/^canalrural/',$n)) return $br.'canal-rural-br.png';
        if(preg_match('/^canaldoboi/',$n)) return $commons('Logo Canal do Boi - PNG.png');
        if(preg_match('/^redeamazonica/',$n)) return $commons('Logotipo da Rede Amazônica 2023.png');
        if(preg_match('/^cinesky\d*/',$n)) return $media.'sky.png';
        if(preg_match('/^tvaparecida/',$n)) return $br.'tv-aparecida-br.png';
        if(preg_match('/^tvpaieterno/',$n)) return $br.'tv-pai-eterno-br.png';
        if(preg_match('/^cancaonova/',$n)) return $br.'cancao-nova-tv-br.png';
        if(preg_match('/^novotempo/',$n)) return $br.'novo-tempo-br.png';
        if(preg_match('/^redegospel/',$n)) return $br.'rede-gospel-br.png';
        if(preg_match('/^redevida/',$n)) return $br.'rede-vida-br.png';
        if(preg_match('/^axn/',$n)) return $br.'axn-br.png';
        if(preg_match('/^arte1/',$n)) return $br.'arte1-br.png';
        if(preg_match('/^bis/',$n)) return $br.'bis-br.png';
        if(preg_match('/^futura/',$n)) return $br.'futura-br.png';
        if(preg_match('/^(?:tvcultura|cultura)/',$n)) return $br.'tv-cultura-br.png';
        if(preg_match('/^cinemax/',$n)) return $br.'cinemax-br.png';
        if(preg_match('/^megapix/',$n)) return $br.'megapix-br.png';
        if(preg_match('/^tntseries/',$n)) return $br.'tnt-series-br.png';
        if($n==='tnt') return $br.'tnt-br.png';
        if(preg_match('/^warner(?:channel)?$/',$n)) return $br.'warner-channel-br.png';
        if(preg_match('/^sony(?:channel)?$/',$n)) return $br.'sony-channel-br.png';
    }

    /*
     * Fallback por familia, ainda baseado SOMENTE no nome real.
     */
    $identity=greenplay_epg_request_identity($request);
    $family=(string)($identity['family']??'');

    if($family==='band') return $br.'band-br.png';
    if($family==='sbt') return $br.'sbt-br.png';
    if($family==='record') return $br.'record-br.png';
    if($family==='globo') return $br.'globo-br.png';

    return '';
}

function greenplay_epg_public_logo_for_request($index,$request){
    if(!is_array($index)||!is_array($request)) return '';

    $wanted=greenplay_epg_request_identity($request);
    $safeNames=greenplay_epg_logo_request_names($request);

    $allowed=function($entry) use ($wanted){
        if(!is_array($entry) || empty($entry['url'])) return false;

        $family='';
        $region='';
        $variant='';

        foreach(array(
            (string)($entry['channel_id']??''),
            (string)($entry['name']??'')
        ) as $value){
            if(trim($value)==='') continue;
            if($family==='') $family=greenplay_epg_channel_family($value);
            if($region==='') $region=greenplay_epg_channel_region($value);
            if($variant==='') $variant=greenplay_epg_channel_variant($value);
        }

        if(($wanted['family']??'')!==''){
            if($family==='') return false;
            if($family!==$wanted['family']) return false;
        }

        if(
            ($wanted['variant']??'')!=='' &&
            $variant!=='' &&
            $wanted['variant']!==$variant
        ){
            return false;
        }

        if(
            ($wanted['region']??'')!=='' &&
            $region!=='' &&
            $wanted['region']!==$region
        ){
            return false;
        }

        return true;
    };

    /*
     * tvg-id ainda pode ser aproveitado, mas SOMENTE se a identidade
     * do registro da logo combinar com o nome real do canal.
     */
    $tokens=greenplay_epg_request_tokens($request);
    foreach((array)($tokens['ids']??array()) as $id){
        $id=preg_replace('/@.*$/','',(string)$id);
        $k=strtolower($id);

        if(
            !empty($index['by_id'][$k]) &&
            $allowed($index['by_id'][$k])
        ){
            return (string)$index['by_id'][$k]['url'];
        }
    }

    /*
     * Nome/alias exato usa APENAS nome real, nunca variantes de tvg-id.
     */
    foreach($safeNames as $n){
        if(
            !empty($index['aliases'][$n]) &&
            $allowed($index['aliases'][$n])
        ){
            return (string)$index['aliases'][$n]['url'];
        }
    }

    /*
     * Similaridade forte como ultimo recurso.
     */
    foreach($safeNames as $want){
        if(strlen($want)<5) continue;

        $best=null;
        $bestScore=0;

        foreach((array)($index['aliases']??array()) as $alias=>$entry){
            if(strlen($alias)<5) continue;
            if(!$allowed($entry)) continue;

            preg_match('/\d+/', $want,$wn);
            preg_match('/\d+/', $alias,$an);

            if(
                !empty($wn[0]) &&
                !empty($an[0]) &&
                $wn[0]!==$an[0]
            ){
                continue;
            }

            $score=0;
            similar_text($want,$alias,$score);

            if($score>=92 && $score>$bestScore){
                $bestScore=$score;
                $best=$entry;
            }
        }

        if(is_array($best) && !empty($best['url'])){
            return (string)$best['url'];
        }
    }

    return '';
}
'''

s = s[:start] + new + "\n" + s[end:]

s = s.replace("public_logos_br_v88.json", "public_logos_br_v881.json")
s = s.replace("'engine_version'=>88", "'engine_version'=>881")
s = s.replace("'engine_version'=>88,", "'engine_version'=>881,")

p.write_text(s)
print("GREENPLAY LOGO SAFE V88.1 aplicado")
