from pathlib import Path
root=Path("work")

p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52885" in s and "versionName '5.28.85'" in s
s=s.replace("versionCode 52885","versionCode 52886",1).replace("versionName '5.28.85'","versionName '5.28.86'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/Api.java"
s=p.read_text()
old='else if(ep.equals("get_category"))readTimeout=18000;else if(ep.equals("content_detail")||ep.equals("content_enrich"))readTimeout=35000;'
new='else if(ep.equals("get_category"))readTimeout=18000;else if(ep.equals("search_catalog"))readTimeout=18000;else if(ep.equals("content_detail")||ep.equals("content_enrich"))readTimeout=35000;'
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()
s=s.replace('results.postDelayed(doSearch,120);','results.postDelayed(doSearch,350);',1)
old=''' void renderSearchResults(String query,LinearLayout host){
  if(host==null)return;host.removeAllViews();String q=query==null?"":query.trim();
  if(q.length()<2){TextView hint=t("Digite pelo menos 2 letras para buscar.",14);hint.setTextColor(0xff8f9994);hint.setPadding(dp(4),dp(18),dp(4),0);host.addView(hint);return;}
  JSONArray a=localSearchResults(q);TextView title=t(a.length()>0?"Resultados":"Nenhum resultado encontrado",19);title.setTypeface(null,1);title.setPadding(dp(2),dp(10),dp(2),dp(10));host.addView(title);
  if(a.length()==0)return;
  GridLayout g=new GridLayout(this);g.setColumnCount(3);g.setUseDefaultMargins(false);host.addView(g,new LinearLayout.LayoutParams(-1,-2));int w=(getResources().getDisplayMetrics().widthPixels-dp(52))/3;
  for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;LinearLayout c=card(x);GridLayout.LayoutParams lp=new GridLayout.LayoutParams();lp.width=w;lp.height=dp(196);lp.setMargins(dp(3),dp(4),dp(5),dp(8));g.addView(c,lp);}
 }
'''
new=''' void renderSearchGrid(JSONArray a,LinearLayout host){
  if(host==null)return;TextView title=t(a!=null&&a.length()>0?"Resultados":"Nenhum resultado encontrado",19);title.setTypeface(null,1);title.setPadding(dp(2),dp(10),dp(2),dp(10));host.addView(title);
  if(a==null||a.length()==0)return;
  GridLayout g=new GridLayout(this);g.setColumnCount(3);g.setUseDefaultMargins(false);host.addView(g,new LinearLayout.LayoutParams(-1,-2));int w=(getResources().getDisplayMetrics().widthPixels-dp(52))/3;
  for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;LinearLayout c=card(x);GridLayout.LayoutParams lp=new GridLayout.LayoutParams();lp.width=w;lp.height=dp(196);lp.setMargins(dp(3),dp(4),dp(5),dp(8));g.addView(c,lp);}
 }
 void renderSearchResults(String query,LinearLayout host){
  if(host==null)return;host.removeAllViews();String q=query==null?"":query.trim();
  if(q.length()<2){host.setTag(null);TextView hint=t("Digite pelo menos 2 letras para buscar.",14);hint.setTextColor(0xff8f9994);hint.setPadding(dp(4),dp(18),dp(4),0);host.addView(hint);return;}
  final String requestKey="search|"+q.toLowerCase(java.util.Locale.ROOT);host.setTag(requestKey);
  final JSONArray local=localSearchResults(q);
  TextView wait=t(local.length()>0?"Atualizando resultados…":"Buscando em todo o catálogo…",13);wait.setTextColor(0xff8f9994);wait.setPadding(dp(3),dp(13),dp(3),dp(10));host.addView(wait);
  if(local.length()>0)renderSearchGrid(local,host);
  Api.post("search_catalog",Api.m("user_id",uid,"search",q,"limit","72"),new Api.CB(){public void ok(JSONObject j){runOnUiThread(()->{
    Object tag=host.getTag();if(!searchScreenOpen||tag==null||!requestKey.equals(String.valueOf(tag)))return;
    JSONArray remote=j.optJSONArray("result");host.removeAllViews();if(j.optInt("status",200)==200&&remote!=null){renderSearchGrid(remote,host);return;}
    if(local.length()>0){renderSearchGrid(local,host);return;}TextView e=t("Não foi possível concluir a pesquisa agora.",14);e.setTextColor(0xff9ca6a1);e.setPadding(dp(3),dp(18),dp(3),0);host.addView(e);
  });}public void err(String e){runOnUiThread(()->{Object tag=host.getTag();if(!searchScreenOpen||tag==null||!requestKey.equals(String.valueOf(tag)))return;host.removeAllViews();if(local.length()>0){renderSearchGrid(local,host);return;}TextView m=t("Não foi possível pesquisar agora.",14);m.setTextColor(0xff9ca6a1);m.setPadding(dp(3),dp(18),dp(3),0);host.addView(m);});}});
 }
'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.86 — Pesquisa no catálogo completo
A busca não fica mais limitada aos itens carregados na tela inicial.
Filmes e Séries são pesquisados no catálogo completo do servidor atual, inclusive quando o servidor conjuga fontes diferentes.
Mantida busca local imediata como fallback e adicionada busca completa na VPS com debounce para não sobrecarregar o servidor.
Consulta “A Terra Prometida” validada no Servidor 8.
Mantidos player, VPN, conjugação e interface da 5.28.85.

"""+prior)
print("patched 5.28.86")
