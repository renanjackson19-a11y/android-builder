from pathlib import Path

g=Path("work/app/build.gradle")
s=g.read_text()
assert "versionCode 52869" in s
assert "versionName '5.28.69'" in s
s=s.replace("versionCode 52869","versionCode 52870",1)
s=s.replace("versionName '5.28.69'","versionName '5.28.70'",1)
g.write_text(s)

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

# Never reuse old per-provider capability cache to resurrect TV/Movies/Series.
old=''' String providerCapKey(String id,String name,String kind){String base=(id==null||id.trim().isEmpty()?name:id);if(base==null)base="";base=base.trim().toLowerCase(java.util.Locale.ROOT).replaceAll("[^a-z0-9_-]+","_");return "provider_cap_"+base+"_"+kind;}'''
new=''' String providerCapKey(String id,String name,String kind){String base=(id==null||id.trim().isEmpty()?name:id);if(base==null)base="";base=base.trim().toLowerCase(java.util.Locale.ROOT).replaceAll("[^a-z0-9_-]+","_");return "provider_cap_v52870_"+base+"_"+kind;}'''
assert old in s
s=s.replace(old,new,1)

old='''   int mv=providerCount(hit!=null?hit:copy,"movies"),se=providerCount(hit!=null?hit:copy,"series"),lv=providerCount(hit!=null?hit:copy,"live");
   if(mv<=0){int c=cachedProviderCap(id,name,"movies");if(c>0)mv=c;}if(se<=0){int c=cachedProviderCap(id,name,"series");if(c>0)se=c;}if(lv<=0){int c=cachedProviderCap(id,name,"live");if(c>0)lv=c;}
'''
new='''   int mv=providerCount(hit!=null?hit:copy,"movies"),se=providerCount(hit!=null?hit:copy,"series"),lv=providerCount(hit!=null?hit:copy,"live");
'''
assert old in s
s=s.replace(old,new,1)

old='''  String id=o.optString("id",o.optString("provider_id",""));if(id.isEmpty())return;String name=o.optString("name","Servidor");int movies=providerCount(o,"movies"),series=providerCount(o,"series"),live=providerCount(o,"live");if(movies<=0){int c=cachedProviderCap(id,name,"movies");if(c>0)movies=c;}if(series<=0){int c=cachedProviderCap(id,name,"series");if(c>0)series=c;}if(live<=0){int c=cachedProviderCap(id,name,"live");if(c>0)live=c;}rememberProviderCaps(id,name,movies,series,live);
'''
new='''  String id=o.optString("id",o.optString("provider_id",""));if(id.isEmpty())return;String name=o.optString("name","Servidor");int movies=providerCount(o,"movies"),series=providerCount(o,"series"),live=providerCount(o,"live");rememberProviderCaps(id,name,movies,series,live);
'''
assert old in s
s=s.replace(old,new,1)

# Refresh the currently selected provider counts from the server source of truth.
anchor=''' boolean currentProviderHasLive(){
  int direct=sp.getInt("provider_live_count",-1);
  if(direct>=0){sessionLiveKnown=true;sessionHasLive=direct>0;return sessionHasLive;}
  if(sessionLiveKnown)return sessionHasLive;
  return false;
 }
'''
helper=''' boolean currentProviderHasLive(){
  int direct=sp.getInt("provider_live_count",-1);
  if(direct>=0){sessionLiveKnown=true;sessionHasLive=direct>0;return sessionHasLive;}
  if(sessionLiveKnown)return sessionHasLive;
  return false;
 }
 boolean syncCurrentProviderCounts(JSONObject o,boolean refreshUi){
  if(o==null)return false;String id=o.optString("id",o.optString("provider_id",""));String current=Api.PROVIDER==null?"":Api.PROVIDER;if(id.isEmpty()||!id.equals(current))return false;
  String name=o.optString("name",sp.getString("provider_name","Servidor"));int mv=providerCount(o,"movies"),se=providerCount(o,"series"),lv=providerCount(o,"live");
  int oldMv=sp.getInt("provider_movies_count",-1),oldSe=sp.getInt("provider_series_count",-1),oldLv=sp.getInt("provider_live_count",-1);
  boolean changed=oldMv!=mv||oldSe!=se||oldLv!=lv;
  sessionLiveKnown=true;sessionHasLive=lv>0;rememberProviderCaps(id,name,mv,se,lv);
  sp.edit().putString("provider_name",name).putInt("provider_movies_count",mv).putInt("provider_series_count",se).putInt("provider_live_count",lv).putBoolean("provider_has_live",sessionHasLive).apply();
  if(changed){clearPreparedHome();if(refreshUi&&!authScreen&&!providerSwitchScreen){runOnUiThread(()->{if(currentNavIndex==2&&!sessionHasLive)home();else if(currentNavIndex==0)home();else shell();});}}
  return changed;
 }
'''
assert anchor in s
s=s.replace(anchor,helper,1)

old='''  Api.post("get_providers",Api.m("user_id",uid,"reseller_code",reseller),new Api.CB(){public void ok(JSONObject j){providerAvailabilityCheckBusy=false;JSONArray a=j.optJSONArray("result");boolean found=false;if(a!=null){for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o==null)continue;String id=o.optString("id",o.optString("provider_id",""));if(current.equals(id)){found=true;break;}}}if(found){providerAvailabilityLastCheck=android.os.SystemClock.elapsedRealtime();if(available!=null)available.run();return;}forgetUnavailableProvider();providerSelectAfterLogin();}public void err(String e){providerAvailabilityCheckBusy=false;if(available!=null)available.run();}});
'''
new='''  Api.post("get_providers",Api.m("user_id",uid,"reseller_code",reseller),new Api.CB(){public void ok(JSONObject j){providerAvailabilityCheckBusy=false;JSONArray a=j.optJSONArray("result");boolean found=false;if(a!=null){for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o==null)continue;String id=o.optString("id",o.optString("provider_id",""));if(current.equals(id)){found=true;syncCurrentProviderCounts(o,false);break;}}}if(found){providerAvailabilityLastCheck=android.os.SystemClock.elapsedRealtime();if(available!=null)available.run();return;}forgetUnavailableProvider();providerSelectAfterLogin();}public void err(String e){providerAvailabilityCheckBusy=false;if(available!=null)available.run();}});
'''
assert old in s
s=s.replace(old,new,1)

old='''  if(uid==null||uid.isEmpty()||Api.PROVIDER==null||Api.PROVIDER.trim().isEmpty()||authScreen||providerSwitchScreen||providerAvailabilityCheckBusy)return;long now=android.os.SystemClock.elapsedRealtime();if(!force&&providerAvailabilityLastCheck>0&&now-providerAvailabilityLastCheck<30000)return;providerAvailabilityCheckBusy=true;final String current=Api.PROVIDER.trim();Api.post("get_providers",Api.m("user_id",uid,"reseller_code",reseller),new Api.CB(){public void ok(JSONObject j){providerAvailabilityCheckBusy=false;providerAvailabilityLastCheck=android.os.SystemClock.elapsedRealtime();JSONArray a=j.optJSONArray("result");boolean found=false;if(a!=null){for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o==null)continue;String id=o.optString("id",o.optString("provider_id",""));if(current.equals(id)){found=true;break;}}}if(!found&&current.equals(Api.PROVIDER==null?"":Api.PROVIDER.trim())){forgetUnavailableProvider();providerSelectAfterLogin();}}public void err(String e){providerAvailabilityCheckBusy=false;}});
'''
new='''  if(uid==null||uid.isEmpty()||Api.PROVIDER==null||Api.PROVIDER.trim().isEmpty()||authScreen||providerSwitchScreen||providerAvailabilityCheckBusy)return;long now=android.os.SystemClock.elapsedRealtime();if(!force&&providerAvailabilityLastCheck>0&&now-providerAvailabilityLastCheck<30000)return;providerAvailabilityCheckBusy=true;final String current=Api.PROVIDER.trim();Api.post("get_providers",Api.m("user_id",uid,"reseller_code",reseller),new Api.CB(){public void ok(JSONObject j){providerAvailabilityCheckBusy=false;providerAvailabilityLastCheck=android.os.SystemClock.elapsedRealtime();JSONArray a=j.optJSONArray("result");boolean found=false;if(a!=null){for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o==null)continue;String id=o.optString("id",o.optString("provider_id",""));if(current.equals(id)){found=true;syncCurrentProviderCounts(o,true);break;}}}if(!found&&current.equals(Api.PROVIDER==null?"":Api.PROVIDER.trim())){forgetUnavailableProvider();providerSelectAfterLogin();}}public void err(String e){providerAvailabilityCheckBusy=false;}});
'''
assert old in s
s=s.replace(old,new,1)

# Reset home snapshot keys again so stale live cards cannot survive the fix.
assert 'catalog52869_' in s
s=s.replace('catalog52869_','catalog52870_',1)
assert 'home_extras_52869_' in s
s=s.replace('home_extras_52869_','home_extras_52870_',1)

p.write_text(s)
