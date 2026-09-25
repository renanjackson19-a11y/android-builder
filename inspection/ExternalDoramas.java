package fun.greenplay.app;

import android.os.Handler;
import android.os.Looper;
import org.json.*;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.*;

final class ExternalDoramas {
    interface CB { void ok(JSONArray rows); void err(String message); }
    private static final ExecutorService NET=Executors.newFixedThreadPool(3);
    private static final Handler MAIN=new Handler(Looper.getMainLooper());

    static void fetchAll(CB cb){ NET.execute(()->{
        JSONArray out=new JSONArray(); HashSet<String> seen=new HashSet<>();
        tryProvider(out,seen,"dramatall");
        tryProvider(out,seen,"dramahub");
        MAIN.post(()->cb.ok(out));
    }); }

    static void resolve(JSONObject item, CB cb){ NET.execute(()->{
        JSONArray out=new JSONArray();
        try{
            String provider=item==null?"":item.optString("provider_source","");
            String id=item==null?"":item.optString("external_id",item.optString("id",""));
            JSONObject resolved=null;
            if("dramatall".equals(provider)) resolved=resolveDramaTall(item,id);
            else if("dramahub".equals(provider)) resolved=resolveDramaHub(item,id);
            if(resolved!=null) out.put(resolved);
        }catch(Exception ignored){}
        MAIN.post(()->{ if(out.length()>0)cb.ok(out); else cb.err("Fonte sem vídeo direto"); });
    }); }

    private static void tryProvider(JSONArray out, HashSet<String> seen, String provider){
        try{
            ArrayList<JSONObject> rows=new ArrayList<>();
            if("dramatall".equals(provider)){
                String[] eps={"drama/api/v1/playlets","drama/api/v1/featured-episodes","drama/api/v1/playlets/ranking","drama/api/v1/recent"};
                for(String ep:eps){JSONObject j=requestSmart("https://app.coocent.net/"+ep,params());collectRows(j,rows,0);}
            }else if("dramahub".equals(provider)){
                String[] eps={"/v1/drama/list","/v1/category/featured","/v1/rank/list"};
                for(String ep:eps){JSONObject j=requestSmart("https://api.dramaverses.com"+ep,params());collectRows(j,rows,0);}
            }
            int added=0;
            for(JSONObject raw:rows){
                JSONObject x=normalize(raw,provider); if(x==null)continue;
                String k=key(x); if(k.isEmpty()||!seen.add(k))continue;
                out.put(x); if(++added>=180)break;
            }
        }catch(Exception ignored){}
    }

    private static JSONObject resolveDramaTall(JSONObject base,String id){
        if(id==null||id.isEmpty())return null;
        String enc=url(id);
        String[] eps={"https://app.coocent.net/drama/api/v1/playlets/"+enc+"/episodes","https://app.coocent.net/drama/api/v1/playlets/"+enc};
        for(String u:eps){JSONObject j=requestSmart(u,params());JSONObject m=mergeResolved(base,j,"dramatall");if(m!=null&&!media(m).isEmpty())return m;}
        return null;
    }

    private static JSONObject resolveDramaHub(JSONObject base,String id){
        if(id==null||id.isEmpty())return null;
        HashMap<String,String> p=params();p.put("drama_id",id);p.put("id",id);
        String[] eps={"https://api.dramaverses.com/v1/drama/list","https://api.dramaverses.com/v1/drama/unlocked_list"};
        for(String u:eps){JSONObject j=requestSmart(u,p);JSONObject m=mergeResolved(base,j,"dramahub");if(m!=null&&!media(m).isEmpty())return m;}
        return null;
    }

    private static JSONObject mergeResolved(JSONObject base,JSONObject response,String provider){
        if(response==null)return null;
        String stream=media(response); if(stream.isEmpty())return null;
        JSONObject out=copy(base); try{out.put("stream_url",stream);out.put("video_url",stream);out.put("provider_source",provider);out.put("source","external");}catch(Exception ignored){}
        String cover=cover(response);if(!cover.isEmpty())try{if(out.optString("thumbnail","").isEmpty())out.put("thumbnail",cover);if(out.optString("portrait_img","").isEmpty())out.put("portrait_img",cover);}catch(Exception ignored){}
        return out;
    }

    private static JSONObject normalize(JSONObject r,String provider){
        if(r==null)return null;
        String id=first(r,"id","drama_id","playlet_id","playletId","book_id","short_play_id","shortPlayId","video_id");
        String title=first(r,"title","name","drama_name","dramaName","playlet_name","playletName","short_play_name","shortPlayName","book_name");
        if(id.isEmpty()&&title.isEmpty())return null;
        String img=cover(r),stream=media(r),desc=first(r,"description","desc","summary","introduction","intro","synopsis","plot");
        JSONObject x=new JSONObject();
        try{
            x.put("id",provider+"_"+(id.isEmpty()?Integer.toHexString(title.hashCode()):id));x.put("external_id",id);x.put("provider_source",provider);x.put("source","external");
            x.put("name",title.isEmpty()?"Yelly Doramas":title);x.put("title",title.isEmpty()?"Yelly Doramas":title);x.put("original_title",title);
            x.put("thumbnail",img);x.put("portrait_img",img);x.put("poster",img);x.put("landscape",img);x.put("landscape_img",img);x.put("backdrop",img);
            x.put("description",desc);x.put("overview",desc);x.put("video_type",1);x.put("type_id",1);x.put("category_name","Yelly Doramas");x.put("category_id","yelly");
            if(!stream.isEmpty()){x.put("stream_url",stream);x.put("video_url",stream);}
        }catch(Exception ignored){}
        return x;
    }

    private static JSONObject requestSmart(String url,HashMap<String,String> p){
        JSONObject j=request(url,"GET",p); if(hasUsefulJson(j))return j;
        return request(url,"POST",p);
    }
    private static boolean hasUsefulJson(JSONObject j){return j!=null&&j.length()>0;}
    private static JSONObject request(String raw,String method,HashMap<String,String> p){
        HttpURLConnection c=null; try{
            String u=raw; if("GET".equals(method)&&p!=null&&!p.isEmpty())u+=(u.contains("?")?"&":"?")+query(p);
            c=(HttpURLConnection)new URL(u).openConnection();c.setConnectTimeout(7000);c.setReadTimeout(9000);c.setUseCaches(false);c.setRequestMethod(method);
            c.setRequestProperty("Accept","application/json");c.setRequestProperty("Accept-Language","pt-BR,pt;q=0.9,en;q=0.7");c.setRequestProperty("User-Agent","YellyDoramas/1.0 Android");
            if("POST".equals(method)){c.setDoOutput(true);c.setRequestProperty("Content-Type","application/json");JSONObject b=new JSONObject();for(Map.Entry<String,String> e:p.entrySet())b.put(e.getKey(),e.getValue());try(OutputStream o=c.getOutputStream()){o.write(b.toString().getBytes(StandardCharsets.UTF_8));}}
            int code=c.getResponseCode();if(code<200||code>=400)return null;InputStream in=c.getInputStream();if(in==null)return null;String text=read(in);if(text.isEmpty())return null;Object root=new JSONTokener(text).nextValue();if(root instanceof JSONObject)return (JSONObject)root;if(root instanceof JSONArray){JSONObject wrap=new JSONObject();wrap.put("data",root);return wrap;}return null;
        }catch(Exception e){return null;}finally{if(c!=null)c.disconnect();}
    }

    private static void collectRows(Object node,ArrayList<JSONObject> out,int depth){
        if(node==null||depth>6||out.size()>450)return;
        if(node instanceof JSONArray){JSONArray a=(JSONArray)node;int hit=0;for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o!=null&&looksLikeItem(o))hit++;}if(hit>0){for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o!=null&&looksLikeItem(o))out.add(o);}return;}for(int i=0;i<a.length();i++)collectRows(a.opt(i),out,depth+1);return;}
        if(node instanceof JSONObject){JSONObject o=(JSONObject)node;Iterator<String> it=o.keys();while(it.hasNext())collectRows(o.opt(it.next()),out,depth+1);}
    }
    private static boolean looksLikeItem(JSONObject o){return !first(o,"title","name","drama_name","dramaName","playlet_name","playletName","short_play_name","shortPlayName").isEmpty()&&!first(o,"id","drama_id","playlet_id","playletId","book_id","short_play_id","shortPlayId","video_id").isEmpty();}

    private static String media(Object node){return media(node,0);}
    private static String media(Object node,int depth){
        if(node==null||depth>7)return "";
        if(node instanceof JSONObject){JSONObject o=(JSONObject)node;String[] keys={"stream_url","streamUrl","video_url","videoUrl","play_url","playUrl","main_play_url","mainPlayUrl","hls_url","hlsUrl","m3u8","url_1080","video_1080","url_720","video_720","url_480","video_480","url"};for(String k:keys){Object v=o.opt(k);if(v instanceof String&&isMedia((String)v))return ((String)v).trim();}Iterator<String> it=o.keys();while(it.hasNext()){String v=media(o.opt(it.next()),depth+1);if(!v.isEmpty())return v;}}
        else if(node instanceof JSONArray){JSONArray a=(JSONArray)node;for(int i=0;i<a.length();i++){String v=media(a.opt(i),depth+1);if(!v.isEmpty())return v;}}
        else if(node instanceof String&&isMedia((String)node))return ((String)node).trim();
        return "";
    }
    private static boolean isMedia(String u){if(u==null)return false;String s=u.trim().toLowerCase(Locale.ROOT);if(!(s.startsWith("https://")||s.startsWith("http://")))return false;return s.contains(".m3u8")||s.matches(".*\\.(mp4|m4v|webm)(\\?.*)?$");}
    private static String cover(Object node){return cover(node,0);}
    private static String cover(Object node,int depth){if(node==null||depth>5)return "";if(node instanceof JSONObject){JSONObject o=(JSONObject)node;String[] ks={"cover_url","coverUrl","cover","poster","poster_url","posterUrl","thumbnail","image","vertical_cover","verticalCover","featured_cover_url","portrait_img"};for(String k:ks){String v=o.optString(k,"").trim();if(isHttp(v))return v;}Iterator<String> it=o.keys();while(it.hasNext()){Object v=o.opt(it.next());if(v instanceof JSONObject){String x=cover(v,depth+1);if(!x.isEmpty())return x;}}}return "";}
    private static String first(JSONObject o,String...ks){if(o==null)return "";for(String k:ks){Object v=o.opt(k);if(v!=null&&!(v instanceof JSONObject)&&!(v instanceof JSONArray)){String s=String.valueOf(v).trim();if(!s.isEmpty()&&!"null".equalsIgnoreCase(s))return s;}}return "";}
    private static JSONObject copy(JSONObject src){JSONObject o=new JSONObject();if(src==null)return o;try{Iterator<String> it=src.keys();while(it.hasNext()){String k=it.next();o.put(k,src.opt(k));}}catch(Exception ignored){}return o;}
    private static String key(JSONObject x){String id=x.optString("external_id","");String p=x.optString("provider_source","");if(!id.isEmpty())return p+"|"+id;return p+"|"+x.optString("name","").toLowerCase(Locale.ROOT);}
    private static HashMap<String,String> params(){HashMap<String,String> p=new HashMap<>();p.put("page","1");p.put("page_no","1");p.put("page_size","100");p.put("limit","100");p.put("lang","pt");p.put("language","pt-BR");p.put("locale","pt_BR");return p;}
    private static String query(HashMap<String,String> p)throws Exception{StringBuilder s=new StringBuilder();for(Map.Entry<String,String> e:p.entrySet()){if(s.length()>0)s.append('&');s.append(URLEncoder.encode(e.getKey(),"UTF-8")).append('=').append(URLEncoder.encode(e.getValue(),"UTF-8"));}return s.toString();}
    private static String url(String s){try{return URLEncoder.encode(s,"UTF-8");}catch(Exception e){return s;}}
    private static boolean isHttp(String s){return s!=null&&(s.startsWith("https://")||s.startsWith("http://"));}
    private static String read(InputStream in)throws Exception{BufferedReader r=new BufferedReader(new InputStreamReader(in,StandardCharsets.UTF_8));StringBuilder s=new StringBuilder();char[] b=new char[8192];int n;while((n=r.read(b))>0&&s.length()<8*1024*1024)s.append(b,0,n);return s.toString();}
}