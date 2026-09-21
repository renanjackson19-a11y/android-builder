package fun.greenplay.app;
import android.content.*;import android.graphics.*;import android.os.*;import android.util.LruCache;import android.view.*;import android.widget.*;import java.io.*;import java.net.*;import java.security.*;import java.util.*;import java.util.concurrent.*;
class Img{
 static ThreadFactory imageThreadFactory(final String prefix){return new ThreadFactory(){int n=0;public Thread newThread(Runnable r){Thread t=new Thread(()->{try{android.os.Process.setThreadPriority(android.os.Process.THREAD_PRIORITY_BACKGROUND);}catch(Exception ignored){}r.run();},prefix+(++n));t.setDaemon(true);return t;}};}
 static final ExecutorService VISIBLE_POOL=Executors.newFixedThreadPool(6,imageThreadFactory("gp-img-"));
 static final ExecutorService PREFETCH_POOL=Executors.newFixedThreadPool(3,imageThreadFactory("gp-prefetch-"));
 static final ExecutorService LOGO_VISIBLE_POOL=Executors.newFixedThreadPool(8,imageThreadFactory("gp-logo-visible-"));
 static final ExecutorService LOGO_PREFETCH_POOL=Executors.newFixedThreadPool(18,imageThreadFactory("gp-logo-prefetch-"));
 static final ThreadPoolExecutor CATALOG_POOL=(ThreadPoolExecutor)Executors.newFixedThreadPool(3,imageThreadFactory("gp-catalog-"));
 static final java.util.concurrent.atomic.AtomicInteger CATALOG_EPOCH=new java.util.concurrent.atomic.AtomicInteger(1);
 interface LogoProgress{void onProgress(int finished,int total);}
 static final Handler MAIN=new Handler(Looper.getMainLooper());
 static final int MEM_KB=Math.max(20*1024,Math.min(48*1024,(int)(Runtime.getRuntime().maxMemory()/1024/6)));
 static final LruCache<String,Bitmap> MEM=new LruCache<String,Bitmap>(MEM_KB){protected int sizeOf(String k,Bitmap b){return Math.max(1,b.getByteCount()/1024);}};
 static final LruCache<String,Bitmap> CATALOG_MEM=new LruCache<String,Bitmap>(12*1024){protected int sizeOf(String k,Bitmap b){return Math.max(1,b.getByteCount()/1024);}};
 static final ConcurrentHashMap<String,Object> LOCKS=new ConcurrentHashMap<>();
 static final ConcurrentHashMap<String,Object> CATALOG_LOCKS=new ConcurrentHashMap<>();
 static String normalize(String url){
  if(url==null)return "";url=url.trim();if(url.isEmpty())return "";
  if(url.startsWith("//"))url="https:"+url;
  if(url.startsWith("http://image.tmdb.org"))url="https://image.tmdb.org"+url.substring("http://image.tmdb.org".length());
  if(url.startsWith("https://image.tmdb.org//"))url="https://image.tmdb.org/"+url.substring("https://image.tmdb.org//".length());
  if(url.startsWith("https://image.tmdb.org/t/p/")){url=url.replace("/w200/","/w780/").replace("/w300/","/w780/").replace("/w342/","/w780/").replace("/w500/","/w780/");}
  if(url.startsWith("/"))return "https://greenplay.fun"+url;
  if(!url.startsWith("http://")&&!url.startsWith("https://"))return "https://greenplay.fun/"+url.replaceFirst("^/+","");
  return url;
 }
 static String key(String u){try{MessageDigest d=MessageDigest.getInstance("SHA-256");byte[] b=d.digest(u.getBytes("UTF-8"));StringBuilder s=new StringBuilder();for(byte x:b)s.append(String.format(java.util.Locale.US,"%02x",x));return s.toString();}catch(Exception e){return String.valueOf(u.hashCode());}}
 static File file(Context c,String u){File d=new File(c.getCacheDir(),"gp_img");if(!d.exists())d.mkdirs();return new File(d,key(u)+".img");}
 static boolean hasCached(Context ctx,String... urls){
  if(ctx==null||urls==null)return false;Context app=ctx.getApplicationContext();
  for(String raw:urls){String u=normalize(raw);if(u.isEmpty())continue;try{if(MEM.get(u)!=null)return true;File f=file(app,u);if(f.exists()&&f.length()>32)return true;}catch(Exception ignored){}}
  return false;
 }
 static Bitmap decode(byte[] raw){try{BitmapFactory.Options bounds=new BitmapFactory.Options();bounds.inJustDecodeBounds=true;BitmapFactory.decodeByteArray(raw,0,raw.length,bounds);int max=Math.max(bounds.outWidth,bounds.outHeight);int sample=1;while(max/sample>1500)sample*=2;BitmapFactory.Options opt=new BitmapFactory.Options();opt.inSampleSize=Math.max(1,sample);opt.inPreferredConfig=Bitmap.Config.ARGB_8888;opt.inDither=true;return BitmapFactory.decodeByteArray(raw,0,raw.length,opt);}catch(Exception e){return null;}}
 static Bitmap decodeLogo(byte[] raw){try{BitmapFactory.Options bounds=new BitmapFactory.Options();bounds.inJustDecodeBounds=true;BitmapFactory.decodeByteArray(raw,0,raw.length,bounds);int max=Math.max(bounds.outWidth,bounds.outHeight);int sample=1;while(max/sample>384)sample*=2;BitmapFactory.Options opt=new BitmapFactory.Options();opt.inSampleSize=Math.max(1,sample);opt.inPreferredConfig=Bitmap.Config.ARGB_8888;opt.inDither=false;return BitmapFactory.decodeByteArray(raw,0,raw.length,opt);}catch(Exception e){return null;}}
 static Bitmap disk(Context c,String u){try{File f=file(c,u);if(!f.exists()||f.length()==0)return null;byte[] raw=new byte[(int)f.length()];try(FileInputStream in=new FileInputStream(f)){int off=0,n;while(off<raw.length&&(n=in.read(raw,off,raw.length-off))>0)off+=n;}Bitmap b=decode(raw);if(b==null)f.delete();return b;}catch(Exception e){return null;}}
 static Bitmap diskLogo(Context c,String u){try{File f=file(c,u);if(!f.exists()||f.length()==0||f.length()>8*1024*1024)return null;byte[] raw=new byte[(int)f.length()];try(FileInputStream in=new FileInputStream(f)){int off=0,n;while(off<raw.length&&(n=in.read(raw,off,raw.length-off))>0)off+=n;}Bitmap b=decodeLogo(raw);if(b==null)f.delete();return b;}catch(Exception e){return null;}}
 static Bitmap network(Context ctx,String u){
  for(int attempt=0;attempt<2;attempt++){
   HttpURLConnection c=null;InputStream in=null;FileOutputStream out=null;
   try{c=(HttpURLConnection)new URL(u).openConnection();c.setInstanceFollowRedirects(true);c.setConnectTimeout(6500);c.setReadTimeout(10000);c.setUseCaches(true);c.setRequestProperty("User-Agent","Mozilla/5.0 (Android) GreenPlay");c.setRequestProperty("Accept","image/avif,image/webp,image/apng,image/*,*/*;q=0.8");int code=c.getResponseCode();if(code<200||code>=400)throw new IOException("HTTP "+code);in=c.getInputStream();ByteArrayOutputStream bytes=new ByteArrayOutputStream();byte[] buf=new byte[16384];int n;while((n=in.read(buf))>0)bytes.write(buf,0,n);byte[] raw=bytes.toByteArray();Bitmap b=decode(raw);if(b!=null){MEM.put(u,b);try{out=new FileOutputStream(file(ctx,u));out.write(raw);}catch(Exception ignored){}}return b;}catch(Exception e){if(attempt==0)try{Thread.sleep(120);}catch(Exception ignored){}}finally{try{if(in!=null)in.close();}catch(Exception ignored){}try{if(out!=null)out.close();}catch(Exception ignored){}if(c!=null)c.disconnect();}
  }
  return null;
 }
 static Bitmap fetch(Context ctx,String u){
  Bitmap m=MEM.get(u);if(m!=null)return m;
  Object lock=LOCKS.computeIfAbsent(u,k->new Object());
  try{synchronized(lock){m=MEM.get(u);if(m!=null)return m;Bitmap d=disk(ctx,u);if(d!=null){MEM.put(u,d);return d;}return network(ctx,u);}}finally{LOCKS.remove(u,lock);}
 }
 static Bitmap decodeCatalog(byte[] raw){try{BitmapFactory.Options bounds=new BitmapFactory.Options();bounds.inJustDecodeBounds=true;BitmapFactory.decodeByteArray(raw,0,raw.length,bounds);int max=Math.max(bounds.outWidth,bounds.outHeight);int sample=1;while(max/sample>560)sample*=2;BitmapFactory.Options opt=new BitmapFactory.Options();opt.inSampleSize=Math.max(1,sample);opt.inPreferredConfig=Bitmap.Config.RGB_565;opt.inDither=true;return BitmapFactory.decodeByteArray(raw,0,raw.length,opt);}catch(Exception e){return null;}}
 static Bitmap diskCatalog(Context c,String u){try{File f=file(c,u);if(!f.exists()||f.length()==0||f.length()>14*1024*1024)return null;byte[] raw=new byte[(int)f.length()];try(FileInputStream in=new FileInputStream(f)){int off=0,n;while(off<raw.length&&(n=in.read(raw,off,raw.length-off))>0)off+=n;}Bitmap b=decodeCatalog(raw);if(b==null)f.delete();return b;}catch(Exception e){return null;}}
 static Bitmap networkCatalog(Context ctx,String u){HttpURLConnection c=null;InputStream in=null;FileOutputStream out=null;try{c=(HttpURLConnection)new URL(u).openConnection();c.setInstanceFollowRedirects(true);c.setConnectTimeout(4500);c.setReadTimeout(7000);c.setUseCaches(true);c.setRequestProperty("User-Agent","Mozilla/5.0 (Android) GreenPlay");c.setRequestProperty("Accept","image/avif,image/webp,image/apng,image/*,*/*;q=0.8");int code=c.getResponseCode();if(code<200||code>=400)return null;in=c.getInputStream();ByteArrayOutputStream bytes=new ByteArrayOutputStream();byte[] buf=new byte[16384];int n,total=0;while((n=in.read(buf))>0){total+=n;if(total>14*1024*1024)return null;bytes.write(buf,0,n);}byte[] raw=bytes.toByteArray();Bitmap b=decodeCatalog(raw);if(b!=null){CATALOG_MEM.put(u,b);try{out=new FileOutputStream(file(ctx,u));out.write(raw);}catch(Exception ignored){}}return b;}catch(Exception e){return null;}finally{try{if(in!=null)in.close();}catch(Exception ignored){}try{if(out!=null)out.close();}catch(Exception ignored){}if(c!=null)c.disconnect();}}
 static Bitmap fetchCatalog(Context ctx,String u){Bitmap m=CATALOG_MEM.get(u);if(m!=null)return m;String lk="cat:"+u;Object lock=CATALOG_LOCKS.computeIfAbsent(lk,k->new Object());try{synchronized(lock){m=CATALOG_MEM.get(u);if(m!=null)return m;Bitmap d=diskCatalog(ctx,u);if(d!=null){CATALOG_MEM.put(u,d);return d;}return networkCatalog(ctx,u);}}finally{CATALOG_LOCKS.remove(lk,lock);}}
 static void cancelCatalogLoads(){CATALOG_EPOCH.incrementAndGet();try{CATALOG_POOL.getQueue().clear();}catch(Exception ignored){}try{CATALOG_MEM.trimToSize(6*1024);}catch(Exception ignored){}}
 static void loadCatalogBest(ImageView v,String... urls){if(v==null)return;java.util.ArrayList<String> list=new java.util.ArrayList<>();java.util.HashSet<String> seen=new java.util.HashSet<>();if(urls!=null)for(String raw:urls){String u=normalize(raw);if(!u.isEmpty()&&seen.add(u))list.add(u);}if(list.isEmpty())return;String tag=android.text.TextUtils.join("|gp-cat|",list);v.setTag(tag);for(String u:list){Bitmap m=CATALOG_MEM.get(u);if(m!=null){v.setImageBitmap(m);v.setAlpha(1f);return;}}Context app=v.getContext().getApplicationContext();final int epoch=CATALOG_EPOCH.get();CATALOG_POOL.execute(()->{if(epoch!=CATALOG_EPOCH.get())return;Bitmap best=null;for(String u:list){if(epoch!=CATALOG_EPOCH.get())return;best=fetchCatalog(app,u);if(best!=null)break;}final Bitmap b=best;if(b==null||epoch!=CATALOG_EPOCH.get())return;MAIN.post(()->{if(epoch!=CATALOG_EPOCH.get())return;Object cur=v.getTag();if(cur!=null&&tag.equals(cur.toString())){v.setImageBitmap(b);v.setAlpha(1f);}});});}
 static Bitmap networkLogo(Context ctx,String u){
  HttpURLConnection c=null;InputStream in=null;FileOutputStream out=null;
  try{URL target=new URL(u);c=(HttpURLConnection)target.openConnection();c.setInstanceFollowRedirects(true);String path=target.getPath()==null?"":target.getPath();boolean localLogo=path.contains("/storage/channel_logos/");c.setConnectTimeout(localLogo?1000:1800);c.setReadTimeout(localLogo?2200:3200);c.setUseCaches(true);c.setRequestProperty("User-Agent","Mozilla/5.0 (Android) GreenPlay");c.setRequestProperty("Accept","image/avif,image/webp,image/apng,image/*,*/*;q=0.8");int code=c.getResponseCode();if(code<200||code>=400)return null;in=c.getInputStream();ByteArrayOutputStream bytes=new ByteArrayOutputStream();byte[] buf=new byte[16384];int n,total=0;while((n=in.read(buf))>0){total+=n;if(total>8*1024*1024)return null;bytes.write(buf,0,n);}byte[] raw=bytes.toByteArray();Bitmap b=decodeLogo(raw);if(b!=null){MEM.put(u,b);try{out=new FileOutputStream(file(ctx,u));out.write(raw);}catch(Exception ignored){}}return b;}catch(Exception e){return null;}finally{try{if(in!=null)in.close();}catch(Exception ignored){}try{if(out!=null)out.close();}catch(Exception ignored){}if(c!=null)c.disconnect();}
 }
 static Bitmap fetchLogoFast(Context ctx,String u){
  Bitmap m=MEM.get(u);if(m!=null)return m;Object lock=LOCKS.computeIfAbsent(u,k->new Object());
  try{synchronized(lock){m=MEM.get(u);if(m!=null)return m;Bitmap d=diskLogo(ctx,u);if(d!=null){MEM.put(u,d);return d;}return networkLogo(ctx,u);}}finally{LOCKS.remove(u,lock);}
 }
 static void loadLogoBest(ImageView v,String... urls){
  if(v==null)return;java.util.ArrayList<String> list=new java.util.ArrayList<>();java.util.HashSet<String> seen=new java.util.HashSet<>();
  if(urls!=null)for(String raw:urls){String u=normalize(raw);if(!u.isEmpty()&&seen.add(u))list.add(u);}if(list.isEmpty()){v.setTag("");return;}
  String tag=android.text.TextUtils.join("|gp-logo|",list);v.setTag(tag);
  for(String u:list){Bitmap m=MEM.get(u);if(m!=null){v.setImageBitmap(m);v.setAlpha(1f);return;}}
  Context app=v.getContext().getApplicationContext();LOGO_VISIBLE_POOL.execute(()->{Bitmap best=null;for(String u:list){best=fetchLogoFast(app,u);if(best!=null)break;}final Bitmap b=best;if(b==null)return;MAIN.post(()->{Object cur=v.getTag();if(cur!=null&&tag.equals(cur.toString())){v.setImageBitmap(b);v.setAlpha(1f);}});});
 }
 static void prefetchLogoGroups(Context ctx,java.util.List<? extends java.util.List<String>> groups,LogoProgress progress,Runnable done){
  if(groups==null||groups.isEmpty()){MAIN.post(done);return;}Context app=ctx.getApplicationContext();java.util.ArrayList<java.util.ArrayList<String>> work=new java.util.ArrayList<>();
  for(java.util.List<String> g:groups){java.util.ArrayList<String> one=new java.util.ArrayList<>();java.util.HashSet<String> seen=new java.util.HashSet<>();if(g!=null)for(String raw:g){String u=normalize(raw);if(!u.isEmpty()&&seen.add(u))one.add(u);}if(!one.isEmpty())work.add(one);}if(work.isEmpty()){MAIN.post(done);return;}
  final int total=work.size(),workers=Math.min(18,total);java.util.concurrent.atomic.AtomicInteger next=new java.util.concurrent.atomic.AtomicInteger(0),finished=new java.util.concurrent.atomic.AtomicInteger(0);java.util.concurrent.atomic.AtomicBoolean ended=new java.util.concurrent.atomic.AtomicBoolean(false);
  for(int w=0;w<workers;w++)LOGO_PREFETCH_POOL.execute(()->{while(true){int idx=next.getAndIncrement();if(idx>=total)break;java.util.ArrayList<String> one=work.get(idx);for(String u:one){if(fetchLogoFast(app,u)!=null)break;}int n=finished.incrementAndGet();MAIN.post(()->{if(progress!=null)progress.onProgress(n,total);if(n>=total&&ended.compareAndSet(false,true))done.run();});}});
 }
 static void show(ImageView v,String u,Bitmap b){if(b==null)return;MAIN.post(()->{Object tag=v.getTag();if(tag!=null&&u.equals(tag.toString())){v.setImageBitmap(b);v.setAlpha(1f);}});}
 static void enqueue(ImageView v,String u){Context app=v.getContext().getApplicationContext();VISIBLE_POOL.execute(()->show(v,u,fetch(app,u)));}
 static void load(ImageView v,String url){String u=normalize(url);v.setTag(u);if(u.isEmpty())return;Bitmap m=MEM.get(u);if(m!=null){v.setImageBitmap(m);return;}enqueue(v,u);}
 static void loadVisible(ImageView v,String url){
  // v16.50: não mantém um OnPreDrawListener por imagem. Em Homes grandes isso
  // executava centenas de verificações a cada frame e causava engasgos ao rolar.
  // A fila visível é limitada e o lock por URL continua evitando downloads duplicados.
  String u=normalize(url);v.setTag(u);if(u.isEmpty())return;Bitmap m=MEM.get(u);if(m!=null){v.setImageBitmap(m);return;}enqueue(v,u);
 }

 static void loadBest(ImageView v,String... urls){
  if(v==null)return;java.util.ArrayList<String> list=new java.util.ArrayList<>();java.util.HashSet<String> seen=new java.util.HashSet<>();
  if(urls!=null)for(String raw:urls){String u=normalize(raw);if(!u.isEmpty()&&seen.add(u))list.add(u);}
  if(list.isEmpty())return;String tag=android.text.TextUtils.join("|gp|",list);v.setTag(tag);Context app=v.getContext().getApplicationContext();
  // v16.207: NUNCA decodificar o cache em disco na thread principal.
  // A v16.194 passou a testar disk() aqui para cada card. Em Homes grandes isso fazia
  // dezenas/centenas de leituras + BitmapFactory.decode no UI thread e o Android podia
  // disparar "GreenPlay não está respondendo" (ANR), mesmo com a tela já desenhada.
  // Na UI thread consultamos somente a RAM; disco/rede ficam 100% no pool de imagens.
  for(String u:list){Bitmap m=MEM.get(u);if(m!=null){v.setImageBitmap(m);v.setAlpha(1f);return;}}
  VISIBLE_POOL.execute(()->{Bitmap best=null;for(String u:list){best=fetch(app,u);if(best!=null)break;}final Bitmap b=best;if(b==null)return;MAIN.post(()->{Object cur=v.getTag();if(cur!=null&&tag.equals(cur.toString())){v.setImageBitmap(b);v.setAlpha(1f);}});});
 }

 static void warmCached(Context ctx,java.util.List<String> urls,int max,long timeoutMs,Runnable done){
  if(urls==null||urls.isEmpty()){MAIN.post(done);return;}Context app=ctx.getApplicationContext();LinkedHashSet<String> unique=new LinkedHashSet<>();for(String raw:urls){String u=normalize(raw);if(!u.isEmpty())unique.add(u);if(unique.size()>=Math.max(1,max))break;}if(unique.isEmpty()){MAIN.post(done);return;}
  java.util.concurrent.atomic.AtomicInteger remain=new java.util.concurrent.atomic.AtomicInteger(unique.size());java.util.concurrent.atomic.AtomicBoolean fired=new java.util.concurrent.atomic.AtomicBoolean(false);Runnable finish=()->{if(fired.compareAndSet(false,true))done.run();};MAIN.postDelayed(finish,Math.max(250,timeoutMs));
  for(String u:unique)VISIBLE_POOL.execute(()->{try{Bitmap m=MEM.get(u);if(m==null){Bitmap d=disk(app,u);if(d!=null)MEM.put(u,d);}}catch(Exception ignored){}MAIN.post(()->{if(remain.decrementAndGet()<=0)finish.run();});});
 }
 static void warmCachedLogos(Context ctx,java.util.List<String> urls,int max,long timeoutMs,Runnable done){
  if(urls==null||urls.isEmpty()){MAIN.post(done);return;}Context app=ctx.getApplicationContext();LinkedHashSet<String> unique=new LinkedHashSet<>();for(String raw:urls){String u=normalize(raw);if(!u.isEmpty())unique.add(u);if(unique.size()>=Math.max(1,max))break;}if(unique.isEmpty()){MAIN.post(done);return;}
  java.util.concurrent.atomic.AtomicInteger remain=new java.util.concurrent.atomic.AtomicInteger(unique.size());java.util.concurrent.atomic.AtomicBoolean fired=new java.util.concurrent.atomic.AtomicBoolean(false);Runnable finish=()->{if(fired.compareAndSet(false,true))done.run();};MAIN.postDelayed(finish,Math.max(250,timeoutMs));
  for(String u:unique)LOGO_PREFETCH_POOL.execute(()->{try{Bitmap m=MEM.get(u);if(m==null){Bitmap d=diskLogo(app,u);if(d!=null)MEM.put(u,d);}}catch(Exception ignored){}MAIN.post(()->{if(remain.decrementAndGet()<=0)finish.run();});});
 }
 static void prefetchCritical(Context ctx,java.util.List<String> urls,int max,long timeoutMs,Runnable done){
  if(urls==null||urls.isEmpty()){MAIN.post(done);return;}Context app=ctx.getApplicationContext();LinkedHashSet<String> unique=new LinkedHashSet<>();for(String raw:urls){String u=normalize(raw);if(!u.isEmpty())unique.add(u);if(unique.size()>=Math.max(1,max))break;}if(unique.isEmpty()){MAIN.post(done);return;}
  java.util.concurrent.atomic.AtomicInteger remain=new java.util.concurrent.atomic.AtomicInteger(unique.size());java.util.concurrent.atomic.AtomicBoolean fired=new java.util.concurrent.atomic.AtomicBoolean(false);Runnable finish=()->{if(fired.compareAndSet(false,true))done.run();};MAIN.postDelayed(finish,Math.max(300,timeoutMs));
  for(String u:unique)VISIBLE_POOL.execute(()->{fetch(app,u);MAIN.post(()->{if(remain.decrementAndGet()<=0)finish.run();});});
 }
 static void prefetch(Context ctx,java.util.List<String> urls,Runnable done){
  if(urls==null||urls.isEmpty()){MAIN.post(done);return;}Context app=ctx.getApplicationContext();PREFETCH_POOL.execute(()->{int count=0;for(String raw:urls){if(count++>=10)break;String u=normalize(raw);if(!u.isEmpty())fetch(app,u);}MAIN.post(done);});
 }
 static void prefetchBackground(Context ctx,java.util.List<String> urls){
  if(urls==null||urls.isEmpty())return;Context app=ctx.getApplicationContext();LinkedHashSet<String> unique=new LinkedHashSet<>();for(String raw:urls){String u=normalize(raw);if(!u.isEmpty())unique.add(u);if(unique.size()>=48)break;}for(String u:unique)PREFETCH_POOL.execute(()->fetch(app,u));
 }
}
