from pathlib import Path
root=Path("work")
p=root/"app/build.gradle"
s=p.read_text()
assert "versionCode 52878" in s and "versionName '5.28.78'" in s
s=s.replace("versionCode 52878","versionCode 52879",1).replace("versionName '5.28.78'","versionName '5.28.79'",1)
p.write_text(s)

p=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
s=p.read_text()

old="ImageView homeHeaderLogo,tvEpgLogo; TextView homeHeaderBrandFallback;"
new="ImageView homeHeaderLogo,tvEpgLogo,tvPreviewLoadingLogo; TextView homeHeaderBrandFallback; ProgressBar tvPreviewLoadingProgress; TextView tvPreviewLoadingStatus;"
assert old in s
s=s.replace(old,new,1)

old='''  TextView header=t("Servidores",18);
  header.setTypeface(null,1);header.setGravity(Gravity.CENTER);
  top.addView(header,new LinearLayout.LayoutParams(0,dp(44),1));'''
new='''  LinearLayout headerBox=new LinearLayout(this);headerBox.setOrientation(LinearLayout.VERTICAL);headerBox.setGravity(Gravity.CENTER);
  TextView header=t("Servidores",20);header.setTypeface(null,1);header.setGravity(Gravity.CENTER);header.setIncludeFontPadding(false);
  TextView headerSub=t("Escolha onde deseja conectar",10);headerSub.setTextColor(0xff8fa099);headerSub.setGravity(Gravity.CENTER);headerSub.setIncludeFontPadding(false);
  headerBox.addView(header,new LinearLayout.LayoutParams(-1,dp(25)));headerBox.addView(headerSub,new LinearLayout.LayoutParams(-1,dp(16)));
  top.addView(headerBox,new LinearLayout.LayoutParams(0,dp(44),1));'''
assert old in s
s=s.replace(old,new,1)

old='''  ImageView logo=new ImageView(this);
  logo.setScaleType(ImageView.ScaleType.FIT_CENTER);applyAppLogo(logo);
  LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(tvMode?62:54));
  lp.setMargins(dp(92),dp(2),dp(92),dp(2));wrap.addView(logo,lp);

  TextView title=t("Escolha um servidor",24);
  title.setTypeface(null,1);title.setGravity(Gravity.CENTER);title.setPadding(0,dp(3),0,0);
  wrap.addView(title,new LinearLayout.LayoutParams(-1,-2));

  TextView sub=t("Selecione o servidor que deseja conectar",14);
  sub.setTextColor(0xffb1b8b4);sub.setGravity(Gravity.CENTER);sub.setPadding(0,0,0,0);
  LinearLayout.LayoutParams slp=new LinearLayout.LayoutParams(-1,-2);slp.setMargins(0,dp(4),0,dp(14));wrap.addView(sub,slp);'''
new='''  LinearLayout intro=new LinearLayout(this);intro.setOrientation(LinearLayout.HORIZONTAL);intro.setGravity(Gravity.CENTER_VERTICAL);intro.setPadding(dp(4),dp(4),dp(4),dp(10));
  ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);applyAppLogo(logo);intro.addView(logo,new LinearLayout.LayoutParams(dp(tvMode?58:50),dp(tvMode?46:40)));
  LinearLayout introText=new LinearLayout(this);introText.setOrientation(LinearLayout.VERTICAL);introText.setPadding(dp(11),0,0,0);
  TextView title=t("Escolha seu servidor",18);title.setTypeface(null,1);title.setTextColor(Color.WHITE);title.setIncludeFontPadding(false);introText.addView(title,new LinearLayout.LayoutParams(-1,-2));
  TextView sub=t("Você pode trocar a qualquer momento",11);sub.setTextColor(0xff8fa099);sub.setIncludeFontPadding(false);LinearLayout.LayoutParams slp=new LinearLayout.LayoutParams(-1,-2);slp.setMargins(0,dp(4),0,0);introText.addView(sub,slp);
  intro.addView(introText,new LinearLayout.LayoutParams(0,-2,1));wrap.addView(intro,new LinearLayout.LayoutParams(-1,-2));'''
assert old in s
s=s.replace(old,new,1)

old=''' void renderProviderChoices(LinearLayout host,JSONArray a){if(a==null||a.length()==0){providerChoiceError(host,"Nenhum servidor disponível no momento.");return;}host.setTag("provider_ready");for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o!=null)providerChoiceCard(host,o);}if(tvMode&&host!=null&&host.getChildCount()>0)requestTvFocus(host.getChildAt(0));}
 void providerChoiceCard(LinearLayout host,JSONObject o){
  String id=o.optString("id",o.optString("provider_id",""));if(id.isEmpty())return;String name=o.optString("name","Servidor");int movies=providerCount(o,"movies"),series=providerCount(o,"series"),live=providerCount(o,"live");rememberProviderCaps(id,name,movies,series,live);
  String caps="";if(movies!=0)caps="Filmes";if(series!=0)caps+=(caps.isEmpty()?"":"  •  ")+"Séries";if(live>0)caps+=(caps.isEmpty()?"":"  •  ")+"TV ao vivo";if(caps.isEmpty())caps="Conteúdo disponível";
  LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER_VERTICAL);card.setPadding(dp(12),dp(8),dp(10),dp(8));GradientDrawable bg=round(0xe3161c19,18);bg.setStroke(dp(1),0x6634e77d);card.setBackground(bg);card.setElevation(dp(2));
  TextView icon=t("▦",18);icon.setTextColor(GREEN);icon.setGravity(Gravity.CENTER);icon.setPadding(0,0,0,0);GradientDrawable ig=round(0x3d1bcf69,12);ig.setStroke(dp(1),0x7a34e77d);icon.setBackground(ig);LinearLayout.LayoutParams iLp=new LinearLayout.LayoutParams(dp(46),dp(46));iLp.setMargins(0,0,dp(12),0);card.addView(icon,iLp);
  LinearLayout mid=new LinearLayout(this);mid.setOrientation(LinearLayout.VERTICAL);mid.setGravity(Gravity.CENTER_VERTICAL);mid.setPadding(0,0,dp(4),0);TextView n=t(name,16);n.setTypeface(null,1);n.setTextColor(Color.WHITE);n.setPadding(0,0,0,0);n.setMaxLines(1);n.setEllipsize(android.text.TextUtils.TruncateAt.END);mid.addView(n);TextView c=t(caps,12);c.setTextColor(0xffaeb5b1);c.setPadding(0,dp(3),0,0);mid.addView(c);card.addView(mid,new LinearLayout.LayoutParams(0,-2,1));
  TextView ar=t("›",25);ar.setTextColor(0xffd7ddd9);ar.setGravity(Gravity.CENTER);ar.setPadding(0,0,0,0);card.addView(ar,new LinearLayout.LayoutParams(dp(32),dp(46)));
  final int providerMovies=movies,providerSeries=series,providerLive=live;
  card.setOnClickListener(v->connectProviderReady(id,name,providerMovies,providerSeries,providerLive,card,ar));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(70));lp.setMargins(0,0,0,dp(8));host.addView(card,lp);
 }'''
new=''' void renderProviderChoices(LinearLayout host,JSONArray a){if(a==null||a.length()==0){providerChoiceError(host,"Nenhum servidor disponível no momento.");return;}host.setTag("provider_ready");for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o!=null)providerChoiceCard(host,o);}if(tvMode&&host!=null&&host.getChildCount()>0)requestTvFocus(host.getChildAt(0));}
 TextView providerChoiceChip(String label){TextView chip=t(label,10);chip.setTextColor(0xffa9b8b0);chip.setGravity(Gravity.CENTER);chip.setIncludeFontPadding(false);chip.setPadding(dp(9),0,dp(9),0);GradientDrawable cb=round(0xff101a15,12);cb.setStroke(dp(1),0xff294338);chip.setBackground(cb);return chip;}
 void providerChoiceCard(LinearLayout host,JSONObject o){
  String id=o.optString("id",o.optString("provider_id",""));if(id.isEmpty())return;String name=o.optString("name","Servidor");int movies=providerCount(o,"movies"),series=providerCount(o,"series"),live=providerCount(o,"live");rememberProviderCaps(id,name,movies,series,live);
  boolean active=id.equals(Api.PROVIDER==null?"":Api.PROVIDER);boolean hasMovies=movies>0||o.optInt("app_movie",0)==1||o.optInt("has_movies",0)==1;boolean hasSeries=series>0||o.optInt("app_series",0)==1||o.optInt("has_series",0)==1;boolean hasLive=live>0||o.optInt("app_live",0)==1||o.optInt("has_live",0)==1;
  LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER_VERTICAL);card.setPadding(dp(13),dp(10),dp(10),dp(10));GradientDrawable bg=round(active?0xf012211a:0xef111915,20);bg.setStroke(dp(active?2:1),active?GREEN:0xff2a3b33);card.setBackground(bg);if(Build.VERSION.SDK_INT>=21)card.setElevation(dp(active?5:2));
  ImageView icon=new ImageView(this);icon.setImageResource(R.drawable.ic_server);icon.setScaleType(ImageView.ScaleType.CENTER_INSIDE);icon.setPadding(dp(13),dp(13),dp(13),dp(13));if(Build.VERSION.SDK_INT>=21)icon.setImageTintList(android.content.res.ColorStateList.valueOf(active?GREEN:0xff75d99d));GradientDrawable ig=round(active?0xff143b27:0xff10291d,15);ig.setStroke(dp(1),active?0xff34e77d:0xff285940);icon.setBackground(ig);LinearLayout.LayoutParams iLp=new LinearLayout.LayoutParams(dp(52),dp(52));iLp.setMargins(0,0,dp(13),0);card.addView(icon,iLp);
  LinearLayout mid=new LinearLayout(this);mid.setOrientation(LinearLayout.VERTICAL);mid.setGravity(Gravity.CENTER_VERTICAL);mid.setPadding(0,0,dp(6),0);
  LinearLayout nameRow=new LinearLayout(this);nameRow.setGravity(Gravity.CENTER_VERTICAL);TextView n=t(name,16);n.setTypeface(null,1);n.setTextColor(Color.WHITE);n.setIncludeFontPadding(false);n.setMaxLines(1);n.setEllipsize(android.text.TextUtils.TruncateAt.END);nameRow.addView(n,new LinearLayout.LayoutParams(0,dp(26),1));if(active){TextView badge=t("EM USO",9);badge.setTextColor(0xff04140a);badge.setTypeface(null,1);badge.setGravity(Gravity.CENTER);badge.setIncludeFontPadding(false);badge.setBackground(round(GREEN,10));LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(dp(54),dp(22));bp.setMargins(dp(8),0,0,0);nameRow.addView(badge,bp);}mid.addView(nameRow,new LinearLayout.LayoutParams(-1,dp(26)));
  LinearLayout chips=new LinearLayout(this);chips.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);if(hasMovies){TextView x=providerChoiceChip("Filmes");chips.addView(x,new LinearLayout.LayoutParams(-2,dp(24)));}if(hasSeries){TextView x=providerChoiceChip("Séries");LinearLayout.LayoutParams xp=new LinearLayout.LayoutParams(-2,dp(24));xp.setMargins(dp(6),0,0,0);chips.addView(x,xp);}if(hasLive){TextView x=providerChoiceChip("TV ao vivo");LinearLayout.LayoutParams xp=new LinearLayout.LayoutParams(-2,dp(24));xp.setMargins(dp(6),0,0,0);chips.addView(x,xp);}if(chips.getChildCount()==0){TextView x=providerChoiceChip("Conteúdo disponível");chips.addView(x,new LinearLayout.LayoutParams(-2,dp(24)));}LinearLayout.LayoutParams chp=new LinearLayout.LayoutParams(-1,dp(27));chp.setMargins(0,dp(5),0,0);mid.addView(chips,chp);card.addView(mid,new LinearLayout.LayoutParams(0,-2,1));
  TextView ar=t(active?"✓":"›",active?18:26);ar.setTextColor(active?GREEN:0xffb4beb8);ar.setGravity(Gravity.CENTER);ar.setPadding(0,0,0,0);if(active){GradientDrawable ab=round(0xff123122,16);ab.setStroke(dp(1),0xff2e7950);ar.setBackground(ab);}card.addView(ar,new LinearLayout.LayoutParams(dp(38),dp(48)));
  final int providerMovies=movies,providerSeries=series,providerLive=live;card.setFocusable(true);if(tvMode)armTvFocus(card);
  card.setOnClickListener(v->connectProviderReady(id,name,providerMovies,providerSeries,providerLive,card,ar));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(82));lp.setMargins(0,0,0,dp(10));host.addView(card,lp);
 }'''
assert old in s
s=s.replace(old,new,1)

old='''  tvPreviewPlaceholder=new LinearLayout(this);tvPreviewPlaceholder.setOrientation(LinearLayout.VERTICAL);tvPreviewPlaceholder.setGravity(Gravity.CENTER);tvPreviewPlaceholder.setPadding(dp(10),dp(8),dp(10),dp(8));
  TextView tvIcon=t("▣",35);tvIcon.setGravity(Gravity.CENTER);tvIcon.setTextColor(GREEN);tvIcon.setPadding(0,0,0,0);tvIcon.setBackground(round(0xff242a27,36));tvPreviewPlaceholder.addView(tvIcon,new LinearLayout.LayoutParams(dp(72),dp(72)));
  tvPreviewTitle=t("Escolha um canal",16);tvPreviewTitle.setTypeface(null,1);tvPreviewTitle.setGravity(Gravity.CENTER);tvPreviewTitle.setPadding(0,dp(8),0,0);tvPreviewPlaceholder.addView(tvPreviewTitle,new LinearLayout.LayoutParams(-1,dp(40)));
  tvPreviewSubtitle=t("Selecione um canal da lista para começar",11);tvPreviewSubtitle.setGravity(Gravity.CENTER);tvPreviewSubtitle.setTextColor(0xff8f9692);tvPreviewSubtitle.setPadding(0,0,0,0);tvPreviewPlaceholder.addView(tvPreviewSubtitle,new LinearLayout.LayoutParams(-1,dp(26)));tvPreviewFrame.addView(tvPreviewPlaceholder,new FrameLayout.LayoutParams(-1,-1));'''
new='''  buildTvPreviewPlaceholder(false);tvPreviewFrame.addView(tvPreviewPlaceholder,new FrameLayout.LayoutParams(-1,-1));'''
assert old in s
s=s.replace(old,new,1)

old='''  tvPreviewPlaceholder=new LinearLayout(this);tvPreviewPlaceholder.setOrientation(LinearLayout.VERTICAL);tvPreviewPlaceholder.setGravity(Gravity.CENTER);TextView mark=t("GREENPLAY TV",25);mark.setTextColor(GREEN);mark.setTypeface(null,1);mark.setGravity(Gravity.CENTER);tvPreviewPlaceholder.addView(mark,new LinearLayout.LayoutParams(dp(230),dp(56)));tvPreviewTitle=t("Escolha um canal",20);tvPreviewTitle.setTypeface(null,1);tvPreviewTitle.setGravity(Gravity.CENTER);tvPreviewPlaceholder.addView(tvPreviewTitle,new LinearLayout.LayoutParams(-1,dp(42)));tvPreviewSubtitle=t("Selecione um canal na lista à esquerda",12);tvPreviewSubtitle.setTextColor(0xff8e9993);tvPreviewSubtitle.setGravity(Gravity.CENTER);tvPreviewPlaceholder.addView(tvPreviewSubtitle,new LinearLayout.LayoutParams(-1,dp(32)));tvPreviewFrame.addView(tvPreviewPlaceholder,new FrameLayout.LayoutParams(-1,-1));'''
new='''  buildTvPreviewPlaceholder(true);tvPreviewFrame.addView(tvPreviewPlaceholder,new FrameLayout.LayoutParams(-1,-1));'''
assert old in s
s=s.replace(old,new,1)

old=''' void showTvPreviewLoading(String name){clearTvBackdrop();if(tvPreviewPlaceholder!=null)tvPreviewPlaceholder.setVisibility(View.VISIBLE);if(tvPreviewTitle!=null)tvPreviewTitle.setText("Carregando canal...");if(tvPreviewSubtitle!=null)tvPreviewSubtitle.setText(name==null?"":name);if(tvSoundButton!=null)tvSoundButton.setVisibility(View.GONE);if(tvCastButton!=null)tvCastButton.setVisibility(View.GONE);if(tvFullButton!=null)tvFullButton.setVisibility(View.GONE);hideTvEpgOverlay();if(tvInlinePlayerView!=null)tvInlinePlayerView.setVisibility(View.VISIBLE);}
 void showTvPreviewError(String msg){tvInlinePrepared=false;if(tvInlinePlayerView!=null)tvInlinePlayerView.setVisibility(View.GONE);if(tvPreviewPlaceholder!=null)tvPreviewPlaceholder.setVisibility(View.VISIBLE);if(tvPreviewTitle!=null)tvPreviewTitle.setText("Não foi possível reproduzir");if(tvPreviewSubtitle!=null)tvPreviewSubtitle.setText(msg==null||msg.isEmpty()?"Tente outro canal.":msg);if(tvSoundButton!=null)tvSoundButton.setVisibility(View.GONE);if(tvCastButton!=null)tvCastButton.setVisibility(View.GONE);if(tvFullButton!=null)tvFullButton.setVisibility(View.GONE);hideTvEpgOverlay();}'''
new=''' void buildTvPreviewPlaceholder(boolean wide){
  tvPreviewPlaceholder=new LinearLayout(this);tvPreviewPlaceholder.setOrientation(LinearLayout.VERTICAL);tvPreviewPlaceholder.setGravity(Gravity.CENTER);tvPreviewPlaceholder.setPadding(dp(wide?28:16),dp(wide?20:14),dp(wide?28:16),dp(wide?20:14));tvPreviewPlaceholder.setBackgroundColor(0xff010604);
  tvPreviewLoadingLogo=new ImageView(this);tvPreviewLoadingLogo.setScaleType(ImageView.ScaleType.FIT_CENTER);tvPreviewLoadingLogo.setImageResource(R.drawable.ic_nav_tv);tvPreviewLoadingLogo.setPadding(dp(wide?15:11),dp(wide?15:11),dp(wide?15:11),dp(wide?15:11));GradientDrawable lg=round(0xff101b16,wide?20:17);lg.setStroke(dp(1),0xff2c6849);tvPreviewLoadingLogo.setBackground(lg);if(Build.VERSION.SDK_INT>=21)tvPreviewLoadingLogo.setImageTintList(android.content.res.ColorStateList.valueOf(GREEN));tvPreviewPlaceholder.addView(tvPreviewLoadingLogo,new LinearLayout.LayoutParams(dp(wide?82:64),dp(wide?82:64)));
  tvPreviewLoadingStatus=t("GREENPLAY TV",wide?10:9);tvPreviewLoadingStatus.setTextColor(GREEN);tvPreviewLoadingStatus.setTypeface(null,1);tvPreviewLoadingStatus.setGravity(Gravity.CENTER);tvPreviewLoadingStatus.setLetterSpacing(.14f);tvPreviewLoadingStatus.setIncludeFontPadding(false);LinearLayout.LayoutParams stp=new LinearLayout.LayoutParams(-1,dp(wide?25:22));stp.setMargins(0,dp(wide?13:10),0,0);tvPreviewPlaceholder.addView(tvPreviewLoadingStatus,stp);
  tvPreviewTitle=t("Escolha um canal",wide?20:17);tvPreviewTitle.setTypeface(null,1);tvPreviewTitle.setGravity(Gravity.CENTER);tvPreviewTitle.setTextColor(Color.WHITE);tvPreviewTitle.setIncludeFontPadding(false);tvPreviewPlaceholder.addView(tvPreviewTitle,new LinearLayout.LayoutParams(-1,dp(wide?34:31)));
  tvPreviewSubtitle=t(wide?"Selecione um canal na lista à esquerda":"Selecione um canal da lista para começar",wide?12:11);tvPreviewSubtitle.setTextColor(0xff8f9c95);tvPreviewSubtitle.setGravity(Gravity.CENTER);tvPreviewSubtitle.setMaxLines(2);tvPreviewSubtitle.setEllipsize(android.text.TextUtils.TruncateAt.END);tvPreviewSubtitle.setIncludeFontPadding(false);tvPreviewPlaceholder.addView(tvPreviewSubtitle,new LinearLayout.LayoutParams(-1,dp(wide?32:29)));
  tvPreviewLoadingProgress=new ProgressBar(this);tvPreviewLoadingProgress.setIndeterminate(true);if(Build.VERSION.SDK_INT>=21)tvPreviewLoadingProgress.setIndeterminateTintList(android.content.res.ColorStateList.valueOf(GREEN));tvPreviewLoadingProgress.setVisibility(View.GONE);LinearLayout.LayoutParams pp=new LinearLayout.LayoutParams(dp(wide?30:26),dp(wide?30:26));pp.gravity=Gravity.CENTER_HORIZONTAL;pp.setMargins(0,dp(wide?10:8),0,0);tvPreviewPlaceholder.addView(tvPreviewLoadingProgress,pp);
 }
 void showTvPreviewLoading(String name){
  clearTvBackdrop();if(tvPreviewPlaceholder!=null){tvPreviewPlaceholder.animate().cancel();tvPreviewPlaceholder.setAlpha(0f);tvPreviewPlaceholder.setVisibility(View.VISIBLE);tvPreviewPlaceholder.animate().alpha(1f).setDuration(140).start();}
  if(tvPreviewLoadingStatus!=null){tvPreviewLoadingStatus.setText("CONECTANDO AO VIVO");tvPreviewLoadingStatus.setTextColor(GREEN);}
  if(tvPreviewLoadingProgress!=null)tvPreviewLoadingProgress.setVisibility(View.VISIBLE);
  if(tvPreviewLoadingLogo!=null){tvPreviewLoadingLogo.setImageResource(R.drawable.ic_nav_tv);if(Build.VERSION.SDK_INT>=21)tvPreviewLoadingLogo.setImageTintList(android.content.res.ColorStateList.valueOf(GREEN));if(tvActiveChannel!=null){String a=tvActiveChannel.optString("provider_icon",tvActiveChannel.optString("stream_icon",""));String b=tvActiveChannel.optString("thumbnail",tvActiveChannel.optString("image",""));String c=tvActiveChannel.optString("epg_logo",tvActiveChannel.optString("fallback_logo",""));if(!a.isEmpty()||!b.isEmpty()||!c.isEmpty()){if(Build.VERSION.SDK_INT>=21)tvPreviewLoadingLogo.setImageTintList(null);Img.loadBest(tvPreviewLoadingLogo,a,b,c);}}}
  if(tvPreviewTitle!=null)tvPreviewTitle.setText("Abrindo canal");if(tvPreviewSubtitle!=null)tvPreviewSubtitle.setText(name==null||name.trim().isEmpty()?"Preparando o sinal ao vivo":name.trim());if(tvSoundButton!=null)tvSoundButton.setVisibility(View.GONE);if(tvCastButton!=null)tvCastButton.setVisibility(View.GONE);if(tvFullButton!=null)tvFullButton.setVisibility(View.GONE);hideTvEpgOverlay();if(tvInlinePlayerView!=null)tvInlinePlayerView.setVisibility(View.VISIBLE);
 }
 void showTvPreviewError(String msg){tvInlinePrepared=false;if(tvInlinePlayerView!=null)tvInlinePlayerView.setVisibility(View.GONE);if(tvPreviewPlaceholder!=null){tvPreviewPlaceholder.animate().cancel();tvPreviewPlaceholder.setAlpha(1f);tvPreviewPlaceholder.setVisibility(View.VISIBLE);}if(tvPreviewLoadingProgress!=null)tvPreviewLoadingProgress.setVisibility(View.GONE);if(tvPreviewLoadingStatus!=null){tvPreviewLoadingStatus.setText("SINAL INDISPONÍVEL");tvPreviewLoadingStatus.setTextColor(0xffff7078);}if(tvPreviewTitle!=null)tvPreviewTitle.setText("Não foi possível reproduzir");if(tvPreviewSubtitle!=null)tvPreviewSubtitle.setText(msg==null||msg.isEmpty()?"Tente outro canal.":msg);if(tvSoundButton!=null)tvSoundButton.setVisibility(View.GONE);if(tvCastButton!=null)tvCastButton.setVisibility(View.GONE);if(tvFullButton!=null)tvFullButton.setVisibility(View.GONE);hideTvEpgOverlay();}'''
assert old in s
s=s.replace(old,new,1)

old='''if(state==androidx.media3.common.Player.STATE_READY){tvInlinePrepared=true;tvInlineSwitching=false;tvInlineBufferStarts=0;tvInlineBufferingSince=0;tvInlineLastPosition=tvInlinePlayer==null?-1:tvInlinePlayer.getCurrentPosition();tvInlineLastAdvanceAt=android.os.SystemClock.elapsedRealtime();if(tvPreviewPlaceholder!=null)tvPreviewPlaceholder.setVisibility(View.GONE);'''
new='''if(state==androidx.media3.common.Player.STATE_READY){tvInlinePrepared=true;tvInlineSwitching=false;tvInlineBufferStarts=0;tvInlineBufferingSince=0;tvInlineLastPosition=tvInlinePlayer==null?-1:tvInlinePlayer.getCurrentPosition();tvInlineLastAdvanceAt=android.os.SystemClock.elapsedRealtime();if(tvPreviewLoadingProgress!=null)tvPreviewLoadingProgress.setVisibility(View.GONE);if(tvPreviewPlaceholder!=null)tvPreviewPlaceholder.setVisibility(View.GONE);'''
assert old in s
s=s.replace(old,new,1)

old='''if(tvInlineSwitching||tvInlineSources.isEmpty()||tvInlinePlayerView==null)return;if(tvInlineRecoveryCount>=4){tvInlineSwitching=false;if(tvInlineWatchdog!=null&&tvInlineHandler!=null)tvInlineHandler.removeCallbacks(tvInlineWatchdog);if(tvPreviewPlaceholder!=null)tvPreviewPlaceholder.setVisibility(View.VISIBLE);if(tvPreviewTitle!=null)tvPreviewTitle.setText("Canal instável");if(tvPreviewSubtitle!=null)tvPreviewSubtitle.setText(tvMode?"Use ↑ ou ↓ para trocar de canal":"Volte à lista e escolha outro canal");if(tvMode&&tvInlineFullscreen)showTvFullscreenChannelOverlay(false);return;}'''
new='''if(tvInlineSwitching||tvInlineSources.isEmpty()||tvInlinePlayerView==null)return;if(tvInlineRecoveryCount>=4){tvInlineSwitching=false;if(tvInlineWatchdog!=null&&tvInlineHandler!=null)tvInlineHandler.removeCallbacks(tvInlineWatchdog);if(tvPreviewPlaceholder!=null)tvPreviewPlaceholder.setVisibility(View.VISIBLE);if(tvPreviewLoadingProgress!=null)tvPreviewLoadingProgress.setVisibility(View.GONE);if(tvPreviewLoadingStatus!=null){tvPreviewLoadingStatus.setText("SINAL INSTÁVEL");tvPreviewLoadingStatus.setTextColor(0xffffb75e);}if(tvPreviewTitle!=null)tvPreviewTitle.setText("Canal instável");if(tvPreviewSubtitle!=null)tvPreviewSubtitle.setText(tvMode?"Use ↑ ou ↓ para trocar de canal":"Volte à lista e escolha outro canal");if(tvMode&&tvInlineFullscreen)showTvFullscreenChannelOverlay(false);return;}'''
assert old in s
s=s.replace(old,new,1)

old="tvPreviewFrame=null;tvPreviewPlaceholder=null;tvPreviewTitle=null;tvPreviewSubtitle=null;tvNowPlaying=null;"
new="tvPreviewFrame=null;tvPreviewPlaceholder=null;tvPreviewLoadingLogo=null;tvPreviewLoadingProgress=null;tvPreviewLoadingStatus=null;tvPreviewTitle=null;tvPreviewSubtitle=null;tvNowPlaying=null;"
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

notes=root/"app/RELEASE_NOTES.txt"
prior=notes.read_text() if notes.exists() else ""
notes.write_text("""5.28.79 — Servidores e carregamento de canais
Tela de servidores redesenhada com cabeçalho compacto, ícone nativo, chips de conteúdo, destaque EM USO e bordas mais discretas.
Carregamento do canal redesenhado: logo do canal quando disponível, estado CONECTANDO AO VIVO, spinner verde pequeno e transição por fade.
Removido o círculo/quadrado grande de carregamento. Estados de erro e sinal instável agora seguem o mesmo padrão visual.
Mantidos player, VPN, conjugação de fontes e navegação da 5.28.78.

"""+prior)
print("patched 5.28.79")
