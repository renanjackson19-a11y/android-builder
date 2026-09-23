from pathlib import Path

g=Path("work/app/build.gradle")
s=g.read_text()
assert "versionCode 52868" in s
assert "versionName '5.28.68'" in s
s=s.replace("versionCode 52868","versionCode 52869",1)
s=s.replace("versionName '5.28.68'","versionName '5.28.69'",1)
g.write_text(s)

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

old=''' int providerCount(JSONObject o,String kind){
  if(o==null)return -1;
  boolean ready=!o.has("counts_ready")||o.optInt("counts_ready",1)!=0;
  int v=-1;
  if("movies".equals(kind)){
   if(o.has("movies_count"))v=o.optInt("movies_count",-1);else if(o.has("movies"))v=o.optInt("movies",-1);
   if(v>=0)return v;
   if(o.optInt("has_movies",o.optBoolean("has_movies",false)?1:0)==1||o.optInt("app_movie",o.optBoolean("app_movie",false)?1:0)==1)return 1;
  }
  if("series".equals(kind)){
   if(o.has("series_count"))v=o.optInt("series_count",-1);else if(o.has("series"))v=o.optInt("series",-1);
   if(v>=0)return v;
   if(o.optInt("has_series",o.optBoolean("has_series",false)?1:0)==1||o.optInt("app_series",o.optBoolean("app_series",false)?1:0)==1)return 1;
  }
  if("live".equals(kind)){
   if(o.has("channels_count"))v=o.optInt("channels_count",-1);else if(o.has("live_count"))v=o.optInt("live_count",-1);else if(o.has("channels"))v=o.optInt("channels",-1);else if(o.has("tv_count"))v=o.optInt("tv_count",-1);
   if(v>=0)return v;
   if(o.optInt("has_live",o.optBoolean("has_live",false)?1:0)==1||o.optInt("app_live",o.optBoolean("app_live",false)?1:0)==1||o.optBoolean("live_enabled",false)||o.optBoolean("supports_live",false))return 1;
  }
  return ready?0:-1;
 }'''
new=''' int providerCount(JSONObject o,String kind){
  if(o==null)return 0;
  int v=0;
  if("movies".equals(kind)){
   if(o.has("movies_count"))v=o.optInt("movies_count",0);else if(o.has("movies"))v=o.optInt("movies",0);
  }else if("series".equals(kind)){
   if(o.has("series_count"))v=o.optInt("series_count",0);else if(o.has("series"))v=o.optInt("series",0);
  }else if("live".equals(kind)){
   if(o.has("channels_count"))v=o.optInt("channels_count",0);else if(o.has("live_count"))v=o.optInt("live_count",0);else if(o.has("channels"))v=o.optInt("channels",0);else if(o.has("tv_count"))v=o.optInt("tv_count",0);
  }
  return Math.max(0,v);
 }'''
assert old in s
s=s.replace(old,new,1)

old=''' void providerCard(JSONObject o){String id=o.optString("id",o.optString("provider_id",""));String name=o.optString("name","Servidor");String active=Api.PROVIDER==null?"":Api.PROVIDER;int movies=providerCount(o,"movies"),series=providerCount(o,"series"),live=providerCount(o,"live");if(movies<=0){int c=cachedProviderCap(id,name,"movies");if(c>0)movies=c;}if(series<=0){int c=cachedProviderCap(id,name,"series");if(c>0)series=c;}if(live<=0){int c=cachedProviderCap(id,name,"live");if(c>0)live=c;}rememberProviderCaps(id,name,movies,series,live);String caps="";if(movies!=0)caps="Filmes";if(series!=0)caps+=(caps.isEmpty()?"":"  •  ")+"Séries";if(live>0)caps+=(caps.isEmpty()?"":"  •  ")+"TV ao vivo";if(caps.isEmpty())caps="Conteúdo disponível";'''
new=''' void providerCard(JSONObject o){String id=o.optString("id",o.optString("provider_id",""));String name=o.optString("name","Servidor");String active=Api.PROVIDER==null?"":Api.PROVIDER;int movies=providerCount(o,"movies"),series=providerCount(o,"series"),live=providerCount(o,"live");rememberProviderCaps(id,name,movies,series,live);String caps="";if(movies>0)caps="Filmes";if(series>0)caps+=(caps.isEmpty()?"":"  •  ")+"Séries";if(live>0)caps+=(caps.isEmpty()?"":"  •  ")+"TV ao vivo";if(caps.isEmpty())caps="Conteúdo em preparação";'''
assert old in s
s=s.replace(old,new,1)

old=''' boolean currentProviderHasLive(){
  if(sessionHasLive)return true;
  JSONObject cachedHome=readHomeCache();JSONArray cachedLive=cachedHome==null?null:cachedHome.optJSONArray("live_channels");if(cachedLive!=null&&cachedLive.length()>0){sessionHasLive=true;sessionLiveKnown=true;return true;}
  String id=Api.PROVIDER==null?"":Api.PROVIDER;
  String name=sp.getString("provider_name","");
  int direct=sp.getInt("provider_live_count",-1);
  int cached=cachedProviderCap(id,name,"live");
  if(direct>0||cached>0||sp.getBoolean("provider_has_live",false)){sessionHasLive=true;sessionLiveKnown=true;return true;}
  return false;
 }'''
new=''' boolean currentProviderHasLive(){
  int direct=sp.getInt("provider_live_count",-1);
  if(direct>=0){sessionLiveKnown=true;sessionHasLive=direct>0;return sessionHasLive;}
  if(sessionLiveKnown)return sessionHasLive;
  return false;
 }'''
assert old in s
s=s.replace(old,new,1)

old='''  addHomeTopMediaTab(tabs,R.drawable.top_tv,"TV",selected);'''
new='''  if(currentProviderHasLive())addHomeTopMediaTab(tabs,R.drawable.top_tv,"TV",selected);'''
assert old in s
s=s.replace(old,new,1)

old='''LinearLayout chips=new LinearLayout(this);chips.setGravity(Gravity.CENTER);chips.setOrientation(LinearLayout.HORIZONTAL);String[] names={"Filmes","Séries","TV"};for(String n:names){TextView c=t(n,11);'''
new='''LinearLayout chips=new LinearLayout(this);chips.setGravity(Gravity.CENTER);chips.setOrientation(LinearLayout.HORIZONTAL);java.util.ArrayList<String> names=new java.util.ArrayList<>();if(sp.getInt("provider_movies_count",0)>0)names.add("Filmes");if(sp.getInt("provider_series_count",0)>0)names.add("Séries");if(currentProviderHasLive())names.add("TV");if(names.isEmpty())names.add("Conteúdo");for(String n:names){TextView c=t(n,11);'''
assert old in s
s=s.replace(old,new,1)

# Login / cadastro passa a ser apresentado como teste grátis.
repls=[
 ('authSecondary("Criar uma conta")','authSecondary("Fazer teste grátis")'),
 ('TextView title=t("Criar sua conta",23)','TextView title=t("Fazer teste grátis",23)'),
 ('TextView sub=t("Crie seu usuário e entre com usuário, e-mail ou código de acesso.",15)','TextView sub=t("Crie seu acesso e inicie seu período de teste grátis.",15)'),
 ('Button go=btn("Criar conta e iniciar teste")','Button go=btn("Iniciar teste grátis")'),
 ('"Não foi possível criar a conta"','"Não foi possível iniciar o teste grátis"'),
 ('"Conta criada. Você pode entrar com usuário, e-mail ou código."','"Teste grátis criado. Você pode entrar com usuário, e-mail ou código."')
]
for a,b in repls:
    assert a in s,a
    s=s.replace(a,b,1)

# Invalida snapshot da Home para uma fonte sem TV não herdar o atalho TV.
assert 'catalog52868_' in s
s=s.replace('catalog52868_','catalog52869_',1)
assert 'home_extras_52868_' in s
s=s.replace('home_extras_52868_','home_extras_52869_',1)

p.write_text(s)
