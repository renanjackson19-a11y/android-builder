package fun.greenplay.app;
import android.app.*;import android.os.*;import android.content.*;import android.graphics.Color;import android.graphics.drawable.*;import android.net.Uri;import android.text.InputType;import android.view.*;import android.widget.*;import org.json.*;import java.util.*;
public class MainActivity extends Activity{
 interface PreparedHomeCB{void ok(JSONObject j);void err(String e);} interface DetailPrepareCB{void done(JSONObject d);}
 int GREEN=Color.rgb(32,224,112); final int BG=Color.rgb(7,17,12),CARD=Color.rgb(16,32,24); LinearLayout root,body,navBar,continueHost,detailNavOverlay; boolean tvMode=false; java.util.WeakHashMap<View,Boolean> tvFocusArmed=new java.util.WeakHashMap<>(); FrameLayout contentFrame; ScrollView mainScroll,savedScroll,homeScrollCache; LinearLayout savedBody,homeBodyCache; ImageView homeHeaderLogo; TextView homeHeaderBrandFallback; int homeScrollY=0; boolean homeViewAvailable=false; TextView navHome,navFav,navTv,navDownloads,navProfile; android.content.SharedPreferences sp; String uid="",reseller="",appName="GreenPlay",logoUrl="",bgUrl=""; boolean authScreen=false,detailOpen=false,searchScreenOpen=false,exitDialogOpen=false,providerSwitchScreen=false,plansScreen=false; int liveOffset=0,currentNavIndex=0,savedNavIndex=0,savedViewGen=0; String liveSearch="",activeHomeTab="Recomendações"; LinearLayout liveListHost,tvCategoryHost,tvChannelHost; TextView liveState; EditText liveSearchBox; String tvSelectedCategory=""; int viewGen=0; int featuredShuffleTick=0; boolean homeExtrasStarted=false; boolean sessionHasLive=false,sessionLiveKnown=false; static JSONObject preparedHomeData=null; static String preparedHomeProvider=""; java.util.HashMap<String,String> detailMemoryCache=new java.util.HashMap<>(); java.util.ArrayDeque<JSONObject> detailPrefetchQueue=new java.util.ArrayDeque<>(); java.util.HashSet<String> detailPrefetchKeys=new java.util.HashSet<>(); int detailPrefetchActive=0; boolean detailPreparing=false; View detailPrepareOverlay; LinearLayout activeSeriesResumeHost; JSONObject activeSeriesDetail,activeSeriesSource;
 public void onCreate(Bundle b){super.onCreate(b);tvMode=isTelevisionDevice();try{setRequestedOrientation(tvMode?android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE:android.content.pm.ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);}catch(Exception ignored){}sp=getSharedPreferences("gp",0);migrateLegacyOfflineDownloads();uid=sp.getString("uid","");reseller=sp.getString("reseller","");Api.PROVIDER=sp.getString("provider_id","");loadIdentityCache();if(uid.isEmpty())login();else startExistingSession();refreshIdentity();}
 @Override protected void onResume(){super.onResume();if(detailOpen&&activeSeriesResumeHost!=null&&activeSeriesDetail!=null)renderSeriesResume(activeSeriesSource,activeSeriesDetail,activeSeriesResumeHost);}

 void migrateLegacyOfflineDownloads(){try{JSONArray a=new JSONArray(sp.getString("offline_items","[]"));JSONArray keep=new JSONArray();boolean changed=false;java.io.File privateDir=new java.io.File(getFilesDir(),"offline");String privatePrefix=privateDir.getAbsolutePath();for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o==null)continue;long did=o.optLong("download_id",0);String path=o.optString("path","");boolean legacy=did>0||(!path.isEmpty()&&!path.startsWith(privatePrefix));if(legacy){changed=true;if(did>0)try{android.app.DownloadManager dm=(android.app.DownloadManager)getSystemService(DOWNLOAD_SERVICE);dm.remove(did);}catch(Exception ignored){}if(!path.isEmpty())try{new java.io.File(path).delete();}catch(Exception ignored){}continue;}keep.put(o);}if(changed)sp.edit().putString("offline_items",keep.toString()).apply();}catch(Exception ignored){}}
 void loadIdentityCache(){appName=sp.getString("app_name","GreenPlay");logoUrl=sp.getString("app_logo","");bgUrl=sp.getString("app_background","");try{GREEN=Color.parseColor(sp.getString("app_color","#20E070"));}catch(Exception e){GREEN=Color.rgb(32,224,112);}}
 void refreshIdentity(){Api.post("general_setting",Api.m(),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");if(a==null)return;android.content.SharedPreferences.Editor ed=sp.edit();for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);String k=x.optString("key"),v=x.optString("value");if(k.equals("greenplay_app_name"))ed.putString("app_name",v);if(k.equals("greenplay_app_logo"))ed.putString("app_logo",v);if(k.equals("greenplay_app_background"))ed.putString("app_background",v);if(k.equals("greenplay_primary_color"))ed.putString("app_color",v);}ed.apply();loadIdentityCache();runOnUiThread(()->{ if(uid.isEmpty()){ if(authScreen) login(); } else { refreshHomeHeaderBranding(); } });}public void err(String e){}}); }
 TextView t(String s,int z){TextView v=new TextView(this);v.setText(s);v.setTextColor(Color.WHITE);v.setTextSize(z);v.setPadding(dp(8),dp(8),dp(8),dp(8));v.setFocusable(true);return v;}
 EditText e(String hint,boolean pass){EditText v=new EditText(this);v.setHint(hint);v.setHintTextColor(0xff799087);v.setTextColor(Color.WHITE);v.setTextSize(17);v.setSingleLine();v.setPadding(dp(16),dp(14),dp(16),dp(14));v.setBackground(round(CARD,14));if(pass)v.setInputType(InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_PASSWORD);return v;}
 GradientDrawable round(int c,int r){GradientDrawable g=new GradientDrawable();g.setColor(c);g.setCornerRadius(dp(r));return g;} int dp(int n){return(int)(n*getResources().getDisplayMetrics().density+.5f);}
 void enableTvRemoteTree(ViewGroup host){if(!tvMode||host==null)return;host.getViewTreeObserver().addOnGlobalLayoutListener(()->prepareTvFocusTree(host));host.post(()->prepareTvFocusTree(host));}
 void prepareTvFocusTree(View v){if(!tvMode||v==null||v.getVisibility()!=View.VISIBLE)return;boolean action=v.isClickable()||v instanceof Button||v instanceof EditText||v instanceof SeekBar;if(action){v.setFocusable(true);v.setFocusableInTouchMode(true);armTvFocus(v);}else if(v instanceof TextView){v.setFocusable(false);v.setFocusableInTouchMode(false);}if(v instanceof ViewGroup){ViewGroup g=(ViewGroup)v;for(int i=0;i<g.getChildCount();i++)prepareTvFocusTree(g.getChildAt(i));}}
 void armTvFocus(View v){if(!tvMode||v==null||tvFocusArmed.containsKey(v))return;tvFocusArmed.put(v,Boolean.TRUE);v.setOnFocusChangeListener((x,has)->{float s=has?1.055f:1f;x.animate().scaleX(s).scaleY(s).setDuration(90).start();if(android.os.Build.VERSION.SDK_INT>=21)x.setTranslationZ(has?dp(8):0);if(has)x.post(()->{try{android.graphics.Rect r=new android.graphics.Rect(0,0,x.getWidth(),x.getHeight());x.requestRectangleOnScreen(r,false);}catch(Exception ignored){}});});}
 void requestTvFocus(View v){if(!tvMode||v==null)return;v.setFocusable(true);v.setFocusableInTouchMode(true);armTvFocus(v);v.postDelayed(()->{if(v.isShown()&&v.isEnabled())v.requestFocus();},120);}
 Button btn(String s){Button b=new Button(this);b.setText(s);b.setTextColor(Color.BLACK);b.setTextSize(16);b.setAllCaps(false);b.setBackground(round(GREEN,14));b.setFocusable(true);return b;}
 GradientDrawable authBox(){GradientDrawable g=new GradientDrawable();g.setColor(0xe619211e);g.setCornerRadius(dp(28));g.setStroke(dp(1),0xff4e5854);return g;}
 EditText authEdit(String hint,boolean pass,int icon){EditText v=new EditText(this);v.setHint(hint);v.setHintTextColor(0xffa9aeac);v.setTextColor(Color.WHITE);v.setTextSize(17);v.setSingleLine();v.setPadding(dp(20),0,dp(18),0);v.setBackground(authBox());v.setCompoundDrawablesWithIntrinsicBounds(icon,0,pass?R.drawable.ic_eye_off:0,0);v.setCompoundDrawablePadding(dp(14));if(pass)v.setInputType(InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_PASSWORD);return v;}
 Button authPrimary(String s){Button b=new Button(this);b.setText(s);b.setTextColor(0xff031108);b.setTextSize(18);b.setTypeface(null,1);b.setAllCaps(false);GradientDrawable g=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{0xff21df70,0xff48f784,0xff20df70});g.setCornerRadius(dp(30));b.setBackground(g);b.setFocusable(true);return b;}
 Button authSecondary(String s){Button b=new Button(this);b.setText(s);b.setTextColor(Color.WHITE);b.setTextSize(15);b.setTypeface(null,1);b.setAllCaps(false);GradientDrawable g=new GradientDrawable();g.setColor(0x66101815);g.setCornerRadius(dp(30));g.setStroke(dp(1),GREEN);b.setBackground(g);b.setFocusable(true);return b;}
 TextView authLabel(String s){TextView v=t(s,15);v.setPadding(dp(2),0,0,dp(6));v.setTextColor(0xfff2f2f2);return v;}
 void openSupport(){String w=sp.getString("support","").replaceAll("\\D","");if(!w.isEmpty()){if(!w.startsWith("55"))w="55"+w;startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse("https://wa.me/"+w)));}else Toast.makeText(this,"Suporte ainda não configurado. Use o cadastro ou fale com sua revenda.",Toast.LENGTH_LONG).show();}
 void base(){base(false);} void base(boolean loginBackground){FrameLayout frame=new FrameLayout(this);frame.setBackgroundColor(BG);if(loginBackground){getWindow().setStatusBarColor(0xff050b08);getWindow().setNavigationBarColor(0xff050b08);ImageView bg=new ImageView(this);bg.setScaleType(ImageView.ScaleType.CENTER_CROP);bg.setImageResource(R.drawable.login_cinema_bg);frame.addView(bg,new FrameLayout.LayoutParams(-1,-1));View shade=new View(this);shade.setBackgroundColor(0x8f020806);frame.addView(shade,new FrameLayout.LayoutParams(-1,-1));}else{getWindow().setStatusBarColor(BG);getWindow().setNavigationBarColor(BG);}root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(loginBackground?dp(22):dp(18),loginBackground?dp(14):dp(18),loginBackground?dp(22):dp(18),loginBackground?dp(18):dp(12));frame.addView(root,new FrameLayout.LayoutParams(-1,-1));setContentView(frame);if(tvMode)enableTvRemoteTree(root);} 
 void brand(){if(!logoUrl.isEmpty()){ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.FIT_CENTER);Img.load(im,logoUrl);LinearLayout.LayoutParams ip=new LinearLayout.LayoutParams(-1,dp(78));ip.setMargins(0,0,0,dp(4));root.addView(im,ip);}else{TextView logo=t(appName.toUpperCase(),30);logo.setTextColor(GREEN);logo.setGravity(Gravity.CENTER);logo.setTypeface(null,1);root.addView(logo);}}
 void login(){authScreen=true;base(true);ScrollView scroll=new ScrollView(this);scroll.setFillViewport(true);scroll.setClipToPadding(false);LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setGravity(Gravity.CENTER_VERTICAL|Gravity.CENTER_HORIZONTAL);c.setMinimumHeight(getResources().getDisplayMetrics().heightPixels-dp(170));c.setPadding(0,dp(12),0,dp(18));scroll.addView(c,new ScrollView.LayoutParams(-1,-2));root.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
  if(!logoUrl.isEmpty()){ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);logo.setAdjustViewBounds(true);logo.setContentDescription(appName);Img.load(logo,logoUrl);LinearLayout.LayoutParams logoLp=new LinearLayout.LayoutParams(-1,dp(82));logoLp.setMargins(dp(24),dp(2),dp(24),0);c.addView(logo,logoLp);}else{TextView logo=t("",35);String brand=(appName==null||appName.trim().isEmpty())?"GreenPlay":appName.trim();android.text.SpannableString ls=new android.text.SpannableString(brand+" ▶");int split=Math.min(5,brand.length());ls.setSpan(new android.text.style.ForegroundColorSpan(Color.WHITE),0,split,android.text.Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);ls.setSpan(new android.text.style.ForegroundColorSpan(GREEN),split,ls.length(),android.text.Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);logo.setText(ls);logo.setTypeface(null,1);logo.setGravity(Gravity.CENTER);logo.setPadding(0,dp(10),0,0);c.addView(logo,new LinearLayout.LayoutParams(-1,dp(66)));}TextView tag=t("MAIS QUE ENTRETENIMENTO",11);tag.setTextColor(0xffc8cfcb);tag.setGravity(Gravity.CENTER);tag.setLetterSpacing(.28f);tag.setPadding(0,0,0,dp(22));c.addView(tag);
  TextView title=t("Bem-vindo de volta!",27);title.setTypeface(null,1);title.setGravity(Gravity.CENTER);title.setPadding(0,dp(4),0,0);c.addView(title);TextView sub=t("Faça login para continuar assistindo.",16);sub.setTextColor(0xffb6b9b7);sub.setGravity(Gravity.CENTER);sub.setPadding(0,dp(4),0,dp(12));c.addView(sub);
  TextView codeToggle=t("Código da revenda",13);codeToggle.setTextColor(0xffc8d2cd);codeToggle.setGravity(Gravity.CENTER);GradientDrawable codeToggleBg=round(0x55101815,18);codeToggleBg.setStroke(dp(1),0xff2d6f51);codeToggle.setBackground(codeToggleBg);LinearLayout.LayoutParams codeToggleLp=new LinearLayout.LayoutParams(dp(210),dp(40));codeToggleLp.gravity=Gravity.CENTER_HORIZONTAL;codeToggleLp.setMargins(0,0,0,dp(14));c.addView(codeToggle,codeToggleLp);EditText code=authEdit("Código da revenda (opcional)",false,R.drawable.ic_store);code.setVisibility(View.GONE);LinearLayout.LayoutParams codeLp=new LinearLayout.LayoutParams(-1,dp(58));codeLp.setMargins(0,0,0,dp(14));c.addView(code,codeLp);codeToggle.setOnClickListener(v->{boolean show=code.getVisibility()!=View.VISIBLE;code.setVisibility(show?View.VISIBLE:View.GONE);codeToggle.setText(show?"Ocultar código":"Código da revenda");});
  c.addView(authLabel("Email"));EditText email=authEdit("seu@email.com",false,R.drawable.ic_email);c.addView(email,new LinearLayout.LayoutParams(-1,dp(64)));Space g1=new Space(this);c.addView(g1,new LinearLayout.LayoutParams(1,dp(18)));c.addView(authLabel("Senha"));EditText pass=authEdit("Sua senha",true,R.drawable.ic_lock);c.addView(pass,new LinearLayout.LayoutParams(-1,dp(64)));final boolean[] vis={false};pass.setOnTouchListener((v,event)->{if(event.getAction()==android.view.MotionEvent.ACTION_UP&&pass.getCompoundDrawables()[2]!=null&&event.getX()>=pass.getWidth()-pass.getTotalPaddingRight()){vis[0]=!vis[0];pass.setInputType(InputType.TYPE_CLASS_TEXT|(vis[0]?InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD:InputType.TYPE_TEXT_VARIATION_PASSWORD));pass.setSelection(pass.length());pass.setCompoundDrawablesWithIntrinsicBounds(R.drawable.ic_lock,0,vis[0]?R.drawable.ic_eye:R.drawable.ic_eye_off,0);return true;}return false;});
  TextView reset=t("Redefinir senha",14);reset.setTextColor(0xffb9bebc);reset.setGravity(Gravity.RIGHT);reset.setPadding(0,dp(7),dp(4),dp(12));reset.setOnClickListener(v->openSupport());c.addView(reset);
  Button go=authPrimary("Entrar  →");c.addView(go,new LinearLayout.LayoutParams(-1,dp(62)));Space g2=new Space(this);c.addView(g2,new LinearLayout.LayoutParams(1,dp(12)));Button create=authSecondary("Criar uma conta");c.addView(create,new LinearLayout.LayoutParams(-1,dp(60)));TextView support=t("Precisa de ajuda? Contate o suporte",14);support.setTextColor(0xffb1b5b3);support.setGravity(Gravity.CENTER);support.setPadding(dp(4),dp(14),dp(4),dp(8));support.setOnClickListener(v->openSupport());c.addView(support);TextView msg=t("",14);msg.setTextColor(0xffff7777);msg.setGravity(Gravity.CENTER);c.addView(msg);create.setOnClickListener(v->registerScreen());
  go.setOnClickListener(v->{String cc=code.getText().toString().trim();if(email.getText().toString().trim().isEmpty()||pass.getText().length()==0){msg.setText("Informe usuário/e-mail e senha.");return;}go.setEnabled(false);if(cc.isEmpty()){reseller="";sp.edit().remove("reseller").putString("reseller_name","GreenPlay").apply();doLogin(email.getText().toString(),pass.getText().toString(),msg,go);return;}Api.post("reseller_bootstrap",Api.m("reseller_code",cc),new Api.CB(){public void ok(JSONObject j){JSONArray ar=j.optJSONArray("result");if(j.optInt("status")!=200||ar==null||ar.length()==0){msg.setText(j.optString("message","Código da revenda inválido"));go.setEnabled(true);return;}JSONObject r=ar.optJSONObject(0);reseller=cc;sp.edit().putString("reseller",cc).putString("support",r.optString("support_whatsapp")).putString("reseller_name",r.optString("name")).apply();doLogin(email.getText().toString(),pass.getText().toString(),msg,go);}public void err(String x){msg.setText("Falha de conexão: "+x);go.setEnabled(true);}});});}
 void registerScreen(){authScreen=true;base(true);TextView back=t("‹ Voltar",16);back.setTextColor(GREEN);root.addView(back);back.setOnClickListener(v->login());brand();TextView title=t("Criar sua conta",23);title.setGravity(Gravity.CENTER);root.addView(title);TextView sub=t("Use o código da revenda ou continue direto com o GreenPlay",15);sub.setTextColor(0xffa8b8b0);sub.setGravity(Gravity.CENTER);root.addView(sub);addGap();EditText code=e("Código da revenda (opcional)",false);root.addView(code);addGap();LinearLayout actions=new LinearLayout(this);actions.setOrientation(LinearLayout.HORIZONTAL);Button verify=btn("Usar código");Button noCode=btn("Não tenho código");actions.addView(verify,new LinearLayout.LayoutParams(0,dp(54),1));Space as=new Space(this);actions.addView(as,new LinearLayout.LayoutParams(dp(8),1));actions.addView(noCode,new LinearLayout.LayoutParams(0,dp(54),1));root.addView(actions);TextView status=t("",15);status.setGravity(Gravity.CENTER);root.addView(status);LinearLayout form=new LinearLayout(this);form.setOrientation(LinearLayout.VERTICAL);form.setVisibility(View.GONE);EditText name=e("Nome completo",false),email=e("E-mail",false),phone=e("WhatsApp (opcional)",false),pass=e("Senha (mínimo 6 caracteres)",true);form.addView(name);Space g1=new Space(this);form.addView(g1,new LinearLayout.LayoutParams(1,dp(10)));form.addView(email);Space g2=new Space(this);form.addView(g2,new LinearLayout.LayoutParams(1,dp(10)));form.addView(phone);Space g3=new Space(this);form.addView(g3,new LinearLayout.LayoutParams(1,dp(10)));form.addView(pass);TextView show=t("Mostrar senha",14);show.setTextColor(GREEN);show.setGravity(Gravity.RIGHT);form.addView(show);final boolean[] vis={false};show.setOnClickListener(v->{vis[0]=!vis[0];pass.setInputType(InputType.TYPE_CLASS_TEXT|(vis[0]?InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD:InputType.TYPE_TEXT_VARIATION_PASSWORD));pass.setSelection(pass.length());show.setText(vis[0]?"Ocultar senha":"Mostrar senha");});Space g4=new Space(this);form.addView(g4,new LinearLayout.LayoutParams(1,dp(10)));Button go=btn("Criar conta e iniciar teste");form.addView(go,new LinearLayout.LayoutParams(-1,dp(58)));TextView msg=t("",14);msg.setTextColor(0xffff7777);form.addView(msg);root.addView(form);noCode.setOnClickListener(v->{reseller="";sp.edit().remove("reseller").putString("reseller_name","GreenPlay principal").remove("support").apply();status.setTextColor(GREEN);status.setText("✓ Cadastro direto com o GreenPlay");code.setEnabled(false);actions.setVisibility(View.GONE);form.setVisibility(View.VISIBLE);});verify.setOnClickListener(v->{String c=code.getText().toString().trim();if(c.isEmpty()){status.setTextColor(0xffff7777);status.setText("Digite o código ou toque em Não tenho código.");return;}verify.setEnabled(false);status.setTextColor(0xffa8b8b0);status.setText("Verificando…");Api.post("reseller_bootstrap",Api.m("reseller_code",c),new Api.CB(){public void ok(JSONObject j){JSONArray ar=j.optJSONArray("result");if(j.optInt("status")!=200||ar==null||ar.length()==0){status.setTextColor(0xffff7777);status.setText(j.optString("message","Código inválido"));verify.setEnabled(true);return;}JSONObject r=ar.optJSONObject(0);reseller=c;sp.edit().putString("reseller",c).putString("support",r.optString("support_whatsapp")).putString("reseller_name",r.optString("name")).apply();status.setTextColor(GREEN);status.setText("✓ Revenda confirmada: "+r.optString("name",c));code.setEnabled(false);actions.setVisibility(View.GONE);form.setVisibility(View.VISIBLE);}public void err(String e){status.setTextColor(0xffff7777);status.setText("Falha de conexão: "+e);verify.setEnabled(true);}});});go.setOnClickListener(v->{if(name.getText().toString().trim().isEmpty()||email.getText().toString().trim().isEmpty()){msg.setText("Informe seu nome e e-mail.");return;}if(pass.getText().length()<6){msg.setText("A senha precisa ter pelo menos 6 caracteres.");return;}go.setEnabled(false);Api.post("register",Api.m("name",name.getText().toString().trim(),"email",email.getText().toString().trim(),"password",pass.getText().toString(),"mobile_number",phone.getText().toString().trim(),"reseller_code",reseller,"device_type","android"),new Api.CB(){public void ok(JSONObject x){JSONArray a=x.optJSONArray("result");if(x.optInt("status")!=200||a==null||a.length()==0){msg.setText(x.optString("message","Não foi possível criar a conta"));go.setEnabled(true);return;}JSONObject u=a.optJSONObject(0);uid=u.optString("id");sp.edit().putString("uid",uid).putString("name",u.optString("full_name",name.getText().toString().trim())).putString("email",u.optString("email",email.getText().toString().trim())).apply();Toast.makeText(MainActivity.this,"Conta criada. Teste grátis iniciado!",Toast.LENGTH_LONG).show();prepareHomeThenShell(msg,go);}public void err(String e){msg.setText("Falha de conexão: "+e);go.setEnabled(true);}});});}
 void doLogin(String email,String pass,TextView msg,Button go){Api.post("login",Api.m("email",email.trim(),"password",pass,"reseller_code",reseller,"device_type","android"),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");if(j.optInt("status")!=200||a==null||a.length()==0){msg.setText(j.optString("message","Dados incorretos"));go.setEnabled(true);return;}JSONObject u=a.optJSONObject(0);uid=u.optString("id");sp.edit().putString("uid",uid).putString("name",u.optString("full_name")).putString("email",u.optString("email")).apply();providerSelectAfterLogin();}public void err(String x){msg.setText("Falha de conexão: "+x);go.setEnabled(true);}});}
 void startExistingSession(){
  if(Api.PROVIDER==null||Api.PROVIDER.trim().isEmpty()){providerSelectAfterLogin();return;}
  JSONObject cache=readHomeCache();
  if(cache!=null&&cache.optJSONArray("result")!=null&&cache.optJSONArray("result").length()>0){shell();warmHomeImages(cache,()->{});prefetchDetailsFromCatalog(cache,10);return;}
  showProviderBootstrap(sp.getString("provider_name","GreenPlay"));
 }
 void providerSelectAfterLogin(){providerSelectAfterLogin(false);}
 void providerSelectAfterLogin(boolean canCancel){
  authScreen=false;providerSwitchScreen=canCancel;base(true);root.setPadding(dp(18),dp(4),dp(18),dp(10));
  if(canCancel){
   LinearLayout closeRow=new LinearLayout(this);closeRow.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);
   TextView close=t("×",28);close.setGravity(Gravity.CENTER);close.setTextColor(Color.WHITE);close.setPadding(0,0,0,0);GradientDrawable xbg=round(0x99131d18,19);xbg.setStroke(dp(1),0xff315344);close.setBackground(xbg);close.setContentDescription("Fechar seleção de servidor");close.setOnClickListener(v->cancelProviderSwitch());
   closeRow.addView(close,new LinearLayout.LayoutParams(dp(40),dp(40)));root.addView(closeRow,new LinearLayout.LayoutParams(-1,dp(44)));
  }
  ScrollView screen=new ScrollView(this);screen.setFillViewport(true);screen.setVerticalScrollBarEnabled(false);screen.setClipToPadding(false);
  LinearLayout wrap=new LinearLayout(this);wrap.setOrientation(LinearLayout.VERTICAL);wrap.setGravity(Gravity.CENTER_HORIZONTAL|Gravity.CENTER_VERTICAL);wrap.setPadding(0,dp(6),0,dp(8));screen.addView(wrap,new ScrollView.LayoutParams(-1,-1));root.addView(screen,new LinearLayout.LayoutParams(-1,0,1));
  if(!logoUrl.isEmpty()){ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);Img.load(logo,logoUrl);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(68));lp.setMargins(dp(70),0,dp(70),dp(4));wrap.addView(logo,lp);}else{TextView mark=t(appName,28);mark.setTextColor(GREEN);mark.setTypeface(null,1);mark.setGravity(Gravity.CENTER);wrap.addView(mark,new LinearLayout.LayoutParams(-1,dp(68)));}
  TextView title=t("Escolha um servidor",24);title.setTypeface(null,1);title.setGravity(Gravity.CENTER);title.setPadding(0,dp(4),0,0);wrap.addView(title,new LinearLayout.LayoutParams(-1,-2));
  TextView sub=t("Selecione o servidor que deseja conectar",14);sub.setTextColor(0xffb1b8b4);sub.setGravity(Gravity.CENTER);sub.setPadding(0,0,0,0);LinearLayout.LayoutParams slp=new LinearLayout.LayoutParams(-1,-2);slp.setMargins(0,dp(6),0,dp(16));wrap.addView(sub,slp);
  LinearLayout list=new LinearLayout(this);list.setOrientation(LinearLayout.VERTICAL);list.setGravity(Gravity.CENTER_HORIZONTAL);list.setPadding(dp(4),0,dp(4),0);wrap.addView(list,new LinearLayout.LayoutParams(-1,-2));
  TextView loading=t("Carregando servidores…",13);loading.setTextColor(0xffb1b8b4);loading.setGravity(Gravity.CENTER);list.addView(loading,new LinearLayout.LayoutParams(-1,dp(54)));
  loadProviderChoices(list,loading);
 }
 void loadProviderChoices(final LinearLayout host,final TextView loading){
  Api.post("general_setting",Api.m(),new Api.CB(){public void ok(JSONObject j){JSONArray cfg=j.optJSONArray("result");String raw="";if(cfg!=null){for(int i=0;i<cfg.length();i++){JSONObject x=cfg.optJSONObject(i);if(x!=null&&"greenplay_providers_json".equals(x.optString("key"))){raw=x.optString("value","");break;}}}try{JSONArray a=raw.isEmpty()?null:new JSONArray(raw);if(a!=null&&a.length()>0){host.removeAllViews();renderProviderChoices(host,a);return;}}catch(Exception ignored){}loadProviderChoicesLegacy(host);}public void err(String e){loadProviderChoicesLegacy(host);}});
 }
 void loadProviderChoicesLegacy(final LinearLayout host){
  Api.post("get_providers",Api.m("user_id",uid,"reseller_code",reseller),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");host.removeAllViews();if(a==null||a.length()==0){providerChoiceError(host,"Nenhum servidor disponível.");return;}renderProviderChoices(host,a);}public void err(String e){host.removeAllViews();providerChoiceError(host,"Não foi possível carregar os servidores.");}});
 }
 void providerChoiceError(LinearLayout host,String message){TextView m=t(message,15);m.setTextColor(0xffff7777);m.setGravity(Gravity.CENTER);host.addView(m,new LinearLayout.LayoutParams(-1,dp(70)));Button retry=authSecondary("Tentar novamente");LinearLayout.LayoutParams rp=new LinearLayout.LayoutParams(-1,dp(56));rp.setMargins(0,dp(8),0,0);host.addView(retry,rp);retry.setOnClickListener(v->{host.removeAllViews();TextView l=t("Carregando servidores…",14);l.setTextColor(0xff9da7a2);l.setGravity(Gravity.CENTER);host.addView(l,new LinearLayout.LayoutParams(-1,dp(64)));loadProviderChoices(host,l);});}
 void renderProviderChoices(LinearLayout host,JSONArray a){for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o!=null)providerChoiceCard(host,o);}}
 void providerChoiceCard(LinearLayout host,JSONObject o){
  String id=o.optString("id",o.optString("provider_id",""));if(id.isEmpty())return;String name=o.optString("name","Servidor");int movies=o.optInt("movies_count",o.optInt("movies",-1));int series=o.optInt("series_count",o.optInt("series",-1));int live=o.optInt("channels_count",o.optInt("live_count",o.optInt("channels",-1)));
  String caps="";if(movies!=0)caps="Filmes";if(series!=0)caps+=(caps.isEmpty()?"":"  •  ")+"Séries";if(live>0)caps+=(caps.isEmpty()?"":"  •  ")+"TV ao vivo";if(caps.isEmpty())caps="Conteúdo disponível";
  LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER_VERTICAL);card.setPadding(dp(12),dp(8),dp(10),dp(8));GradientDrawable bg=round(0xe3161c19,18);bg.setStroke(dp(1),0x6634e77d);card.setBackground(bg);card.setElevation(dp(2));
  TextView icon=t("▦",18);icon.setTextColor(GREEN);icon.setGravity(Gravity.CENTER);icon.setPadding(0,0,0,0);GradientDrawable ig=round(0x3d1bcf69,12);ig.setStroke(dp(1),0x7a34e77d);icon.setBackground(ig);LinearLayout.LayoutParams iLp=new LinearLayout.LayoutParams(dp(46),dp(46));iLp.setMargins(0,0,dp(12),0);card.addView(icon,iLp);
  LinearLayout mid=new LinearLayout(this);mid.setOrientation(LinearLayout.VERTICAL);mid.setGravity(Gravity.CENTER_VERTICAL);mid.setPadding(0,0,dp(4),0);TextView n=t(name,16);n.setTypeface(null,1);n.setTextColor(Color.WHITE);n.setPadding(0,0,0,0);n.setMaxLines(1);n.setEllipsize(android.text.TextUtils.TruncateAt.END);mid.addView(n);TextView c=t(caps,12);c.setTextColor(0xffaeb5b1);c.setPadding(0,dp(3),0,0);mid.addView(c);card.addView(mid,new LinearLayout.LayoutParams(0,-2,1));
  TextView ar=t("›",25);ar.setTextColor(0xffd7ddd9);ar.setGravity(Gravity.CENTER);ar.setPadding(0,0,0,0);card.addView(ar,new LinearLayout.LayoutParams(dp(32),dp(46)));
  card.setOnClickListener(v->connectProviderReady(id,name,movies,series,live,card,ar));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(74));lp.setMargins(0,0,0,dp(10));host.addView(card,lp);
 }
 void connectProviderReady(String id,String name,int movieCount,int seriesCount,int liveCount,View card,TextView arrow){
  providerSwitchScreen=false;
  if(card!=null&&"loading".equals(String.valueOf(card.getTag())))return;
  if(card!=null){card.setTag("loading");card.setEnabled(false);}if(arrow!=null){arrow.setText("…");arrow.setTextColor(GREEN);}
  clearPreparedHome();Api.PROVIDER=id;sessionLiveKnown=liveCount>=0;sessionHasLive=liveCount>0;
  sp.edit().putString("provider_id",id).putString("provider_name",name).putInt("provider_movies_count",movieCount).putInt("provider_series_count",seriesCount).putInt("provider_live_count",liveCount).putBoolean("provider_has_live",sessionHasLive).apply();
  // v16.47: ao escolher o servidor, sai imediatamente da lista e abre a tela de
  // preparação visual. O catálogo continua vindo direto da Xtream e permanece só
  // em memória; a Home só abre depois que o conteúdo crítico estiver pronto.
  showProviderBootstrap(name,movieCount,seriesCount,liveCount);
 }
 void fetchPreparedHome(int movieCount,int seriesCount,PreparedHomeCB cb){
  final boolean wantMovies=movieCount!=0,wantSeries=seriesCount!=0;
  final JSONObject[] moviePart={null},seriesPart={null};final boolean[] movieDone={!wantMovies},seriesDone={!wantSeries};final String[] movieError={""},seriesError={""};
  Runnable finish=()->{if(!movieDone[0]||!seriesDone[0])return;JSONObject merged=mergeHomeParts(moviePart[0],seriesPart[0]);JSONArray a=merged.optJSONArray("result");if(a!=null&&a.length()>0){cb.ok(merged);return;}String error=!movieError[0].isEmpty()?movieError[0]:seriesError[0];cb.err(error.isEmpty()?"Esse servidor não retornou conteúdo agora.":"Não foi possível carregar o conteúdo desse servidor.");};
  if(wantMovies)fetchHomePart(1,1,new PreparedHomeCB(){public void ok(JSONObject j){moviePart[0]=j;movieDone[0]=true;finish.run();}public void err(String e){movieError[0]=e==null?"":e;movieDone[0]=true;finish.run();}});
  if(wantSeries)fetchHomePart(2,1,new PreparedHomeCB(){public void ok(JSONObject j){seriesPart[0]=j;seriesDone[0]=true;finish.run();}public void err(String e){seriesError[0]=e==null?"":e;seriesDone[0]=true;finish.run();}});
  finish.run();
 }


 // v16.52: bootstrap curto direto da Xtream. O painel devolve somente as categorias
 // necessárias para a Home inicial já pronta. O catálogo completo não é percorrido
 // durante a troca de servidor; as demais categorias ficam para as telas Filmes/Séries.
 void fetchProviderSnapshot(int movieCount,int seriesCount,PreparedHomeCB cb){fetchProviderSnapshotAttempt(movieCount,seriesCount,1,cb);}
 void fetchProviderSnapshotAttempt(int movieCount,int seriesCount,int retries,PreparedHomeCB cb){
  // v16.53: UM snapshot completo. Nada de fallback curto ou waterfall por categoria.
  final boolean wantMovies=movieCount!=0,wantSeries=seriesCount!=0,wantLive=sessionHasLive;
  Api.post("bootstrap_home/index.php",Api.m("user_id",uid,"want_movie",wantMovies?"1":"0","want_series",wantSeries?"1":"0","want_live",wantLive?"1":"0","full_catalog","1"),new Api.CB(){public void ok(JSONObject j){
   JSONArray a=j.optJSONArray("result");JSONArray live=j.optJSONArray("live_channels");boolean full=j.optInt("catalog_complete",0)==1;
   if(j.optInt("status",200)==200&&full&&((a!=null&&a.length()>0)||(live!=null&&live.length()>0))){cb.ok(j);return;}
   if(retries>0){new Handler(Looper.getMainLooper()).postDelayed(()->fetchProviderSnapshotAttempt(movieCount,seriesCount,retries-1,cb),450);return;}cb.err(j.optString("message","Não foi possível carregar o catálogo completo."));
  }public void err(String e){if(retries>0){new Handler(Looper.getMainLooper()).postDelayed(()->fetchProviderSnapshotAttempt(movieCount,seriesCount,retries-1,cb),450);return;}cb.err(e==null?"Falha ao carregar o catálogo completo.":e);}});
 }
 void fetchProviderSnapshotFallback(int movieCount,int seriesCount,PreparedHomeCB cb){
  final boolean wantMovies=movieCount!=0,wantSeries=seriesCount!=0;final JSONObject[] moviePart={null},seriesPart={null};final boolean[] md={!wantMovies},sd={!wantSeries};final boolean[] delivered={false};
  Runnable finish=()->{if(delivered[0]||!md[0]||!sd[0])return;delivered[0]=true;JSONObject merged=mergeHomeParts(moviePart[0],seriesPart[0]);try{merged.put("catalog_complete",0);merged.put("catalog_mode","bootstrap_fallback");}catch(Exception ignored){}JSONArray a=merged.optJSONArray("result");if(a!=null&&a.length()>0)cb.ok(merged);else cb.err("A fonte Xtream não retornou conteúdo agora.");};
  if(wantMovies)fetchBootstrapHomePart(1,new PreparedHomeCB(){public void ok(JSONObject j){moviePart[0]=j;md[0]=true;finish.run();}public void err(String e){md[0]=true;finish.run();}});
  if(wantSeries)fetchBootstrapHomePart(2,new PreparedHomeCB(){public void ok(JSONObject j){seriesPart[0]=j;sd[0]=true;finish.run();}public void err(String e){sd[0]=true;finish.run();}});
  finish.run();
 }

 // v16.48: bootstrap rápido. Para abrir a Home não esperamos TODAS as categorias
 // do servidor. Buscamos apenas as primeiras categorias úteis de Filmes/Séries, em
 // paralelo, e o restante continua sendo acrescentado silenciosamente depois da Home.
 // O catálogo segue direto da fonte e não é gravado de forma persistente.
 void fetchBootstrapHomePart(int typeId,PreparedHomeCB cb){
  final String type=typeId==2?"series":"movie";
  Api.post("get_category",Api.m("type",type,"user_id",uid),new Api.CB(){public void ok(JSONObject j){
   if(j.optInt("status",200)!=200){cb.err(j.optString("message","Não foi possível carregar as categorias."));return;}
   JSONArray cats=j.optJSONArray("result");if(cats==null){cb.err("Resposta de categorias inválida.");return;}
   if(cats.length()==0){cb.ok(homePartFromSections(new JSONArray(),"bootstrap_quick"));return;}
   fetchBootstrapCategories(typeId,cats,cb);
  }public void err(String e){cb.err(e==null?"Falha ao carregar categorias.":e);}});
 }
 void fetchBootstrapCategories(int typeId,JSONArray cats,PreparedHomeCB cb){
  final int inspect=Math.min(cats.length(),6),target=Math.min(2,inspect);
  final JSONObject[] built=new JSONObject[inspect];final int[] next={0},active={0},finished={0},okCount={0};final boolean[] delivered={false};
  final Handler h=new Handler(Looper.getMainLooper());final Runnable[] pump=new Runnable[1];
  final Runnable deliver=()->{
   if(delivered[0])return;delivered[0]=true;
   JSONArray sections=new JSONArray();for(JSONObject sec:built)if(sec!=null)sections.put(sec);
   if(sections.length()>0)cb.ok(homePartFromSections(sections,"bootstrap_quick"));else cb.err("A fonte não respondeu a tempo.");
  };
  final Runnable softTimeout=()->{if(!delivered[0])deliver.run();};h.postDelayed(softTimeout,9000);
  pump[0]=()->{
   if(delivered[0])return;
   while(active[0]<4&&next[0]<inspect){final int index=next[0]++;final JSONObject cat=cats.optJSONObject(index);if(cat==null){finished[0]++;continue;}active[0]++;
    fetchCategoryHomeSection(typeId,cat,0,new PreparedHomeCB(){public void ok(JSONObject part){
     if(delivered[0])return;active[0]--;finished[0]++;JSONArray a=part==null?null:part.optJSONArray("result");if(a!=null&&a.length()>0){built[index]=a.optJSONObject(0);okCount[0]++;}
     if(okCount[0]>=target){h.removeCallbacks(softTimeout);deliver.run();return;}pump[0].run();
    }public void err(String e){if(delivered[0])return;active[0]--;finished[0]++;pump[0].run();}});
   }
   if(finished[0]>=inspect&&active[0]==0&&!delivered[0]){h.removeCallbacks(softTimeout);deliver.run();}
  };
  pump[0].run();
 }
 // v16.46: a preparação da Home não depende mais do section_list pesado. Primeiro
 // busca a lista de categorias e carrega a primeira página de cada categoria direto
 // da fonte. Assim provedores com get_vod_streams/get_series gigantes não travam a
 // seleção do servidor. O section_list tipado fica apenas como fallback de emergência.
 void fetchHomePart(int typeId,int retries,PreparedHomeCB cb){
  fetchHomePartByCategories(typeId,new PreparedHomeCB(){public void ok(JSONObject j){cb.ok(j);}public void err(String directError){
   Api.post("section_list",Api.m("user_id",uid,"type_id",String.valueOf(typeId)),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");if(j.optInt("status",200)==200&&a!=null){cb.ok(j);return;}retryHomePart(typeId,retries-1,cb,j.optString("message",directError));}public void err(String e){retryHomePart(typeId,retries-1,cb,(e==null||e.isEmpty())?directError:e);}});
  }});
 }
 void fetchHomePartByCategories(int typeId,PreparedHomeCB cb){
  final String type=typeId==2?"series":"movie";
  Api.post("get_category",Api.m("type",type,"user_id",uid),new Api.CB(){public void ok(JSONObject j){
   if(j.optInt("status",200)!=200){cb.err(j.optString("message","Não foi possível carregar as categorias."));return;}
   JSONArray cats=j.optJSONArray("result");if(cats==null){cb.err("Resposta de categorias inválida.");return;}
   if(cats.length()==0){cb.ok(homePartFromSections(new JSONArray(),"direct_categories"));return;}
   fetchHomeCategoriesBatch(typeId,cats,cb);
  }public void err(String e){cb.err(e==null?"Falha ao carregar categorias.":e);}});
 }
 void fetchHomeCategoriesBatch(int typeId,JSONArray cats,PreparedHomeCB cb){
  final int total=cats.length();final JSONObject[] built=new JSONObject[total];final int[] next={0},active={0},finished={0},errors={0};final boolean[] delivered={false};final Runnable[] pump=new Runnable[1];
  pump[0]=()->{
   if(delivered[0])return;
   while(active[0]<3&&next[0]<total){final int index=next[0]++;final JSONObject cat=cats.optJSONObject(index);if(cat==null){finished[0]++;continue;}active[0]++;
    fetchCategoryHomeSection(typeId,cat,1,new PreparedHomeCB(){public void ok(JSONObject part){active[0]--;finished[0]++;JSONArray a=part==null?null:part.optJSONArray("result");if(a!=null&&a.length()>0)built[index]=a.optJSONObject(0);pump[0].run();}public void err(String e){active[0]--;finished[0]++;errors[0]++;pump[0].run();}});
   }
   if(finished[0]>=total&&active[0]==0&&!delivered[0]){delivered[0]=true;JSONArray sections=new JSONArray();for(JSONObject sec:built)if(sec!=null)sections.put(sec);if(sections.length()>0||errors[0]<total)cb.ok(homePartFromSections(sections,"direct_categories"));else cb.err("A fonte não respondeu às categorias desse servidor.");}
  };
  pump[0].run();
 }
 void fetchCategoryHomeSection(int typeId,JSONObject cat,int retries,PreparedHomeCB cb){
  String cid=cat.optString("category_id",cat.optString("id",""));if(cid.isEmpty()){cb.ok(homePartFromSections(new JSONArray(),"direct_category"));return;}
  int n;try{n=Integer.parseInt(cid);if(typeId==2&&n>=1000000)n-=1000000;}catch(Exception e){cb.ok(homePartFromSections(new JSONArray(),"direct_category"));return;}
  final int raw=typeId==2?1000000+n:n;final int categoryId=n;final String title=fixTitle(cat.optString("category_name",cat.optString("name",typeId==2?"Séries":"Filmes")));
  Api.post("content_by_category",Api.m("user_id",uid,"category_id",String.valueOf(raw),"page_no","1"),new Api.CB(){public void ok(JSONObject j){
   if(j.optInt("status",200)!=200){retryCategoryHomeSection(typeId,cat,retries,cb,j.optString("message","Resposta inválida"));return;}
   JSONArray data=j.optJSONArray("result");if(data==null){retryCategoryHomeSection(typeId,cat,retries,cb,"Resposta sem conteúdo");return;}
   JSONArray sections=new JSONArray();if(data.length()>0){JSONObject sec=new JSONObject();try{sec.put("title",title);sec.put("category_id",categoryId);sec.put("type_id",typeId);sec.put("video_type",typeId);sec.put("screen_layout","portrait");sec.put("data",data);sections.put(sec);}catch(Exception ignored){}}
   cb.ok(homePartFromSections(sections,"direct_category"));
  }public void err(String e){retryCategoryHomeSection(typeId,cat,retries,cb,e);}});
 }
 void retryCategoryHomeSection(int typeId,JSONObject cat,int retries,PreparedHomeCB cb,String error){if(retries<=0){cb.err(error);return;}new Handler(Looper.getMainLooper()).postDelayed(()->fetchCategoryHomeSection(typeId,cat,retries-1,cb),350);}
 JSONObject homePartFromSections(JSONArray sections,String mode){JSONObject out=new JSONObject();try{out.put("status",200);out.put("message","Success");out.put("result",sections==null?new JSONArray():sections);out.put("total_rows",sections==null?0:sections.length());out.put("catalog_mode",mode);}catch(Exception ignored){}return out;}
 void retryHomePart(int typeId,int retries,PreparedHomeCB cb,String error){if(retries<=0){cb.err(error);return;}new Handler(Looper.getMainLooper()).postDelayed(()->fetchHomePart(typeId,retries-1,cb),650);}
 JSONObject mergeHomeParts(JSONObject movies,JSONObject series){
  JSONObject out=new JSONObject();JSONArray result=new JSONArray();java.util.HashSet<String> seen=new java.util.HashSet<>();
  try{JSONObject[] parts={movies,series};for(JSONObject part:parts){if(part==null)continue;JSONArray a=part.optJSONArray("result");if(a==null)continue;for(int i=0;i<a.length();i++){JSONObject sec=a.optJSONObject(i);if(sec==null)continue;String key=sec.optInt("type_id",sec.optInt("video_type",0))+"|"+sec.optString("section_key","")+"|"+sec.optString("category_id","")+"|"+sec.optString("title","");if(seen.add(key))result.put(sec);}}out.put("status",200);out.put("message","Success");out.put("result",result);out.put("total_rows",result.length());out.put("catalog_mode","direct_source_split");}catch(Exception ignored){}return out;
 }
 class BootstrapRow{
  LinearLayout view;TextView icon,label,check;ProgressBar spinner;
 }
 void showProviderBootstrap(String name){
  int movies=sp.getInt("provider_movies_count",-1),series=sp.getInt("provider_series_count",-1),live=sp.getInt("provider_live_count",sp.getBoolean("provider_has_live",false)?1:0);
  showProviderBootstrap(name,movies,series,live);
 }
 void showProviderBootstrap(String name,int movieCount,int seriesCount,int liveCount){
  clearPreparedHome();authScreen=false;sessionLiveKnown=liveCount>=0;sessionHasLive=liveCount>0;base(true);root.setPadding(dp(22),dp(10),dp(22),dp(16));
  LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setGravity(Gravity.CENTER_HORIZONTAL);root.addView(c,new LinearLayout.LayoutParams(-1,-1));
  Space top=new Space(this);c.addView(top,new LinearLayout.LayoutParams(1,dp(66)));
  if(!logoUrl.isEmpty()){ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);Img.load(logo,logoUrl);LinearLayout.LayoutParams llp=new LinearLayout.LayoutParams(-1,dp(72));llp.setMargins(dp(58),0,dp(58),dp(8));c.addView(logo,llp);}else{TextView mark=t(appName,27);mark.setTypeface(null,1);mark.setTextColor(GREEN);mark.setGravity(Gravity.CENTER);c.addView(mark,new LinearLayout.LayoutParams(-1,dp(64)));}
  TextView title=t("Carregando Conteúdo",22);title.setTypeface(null,1);title.setGravity(Gravity.CENTER);title.setPadding(0,dp(4),0,0);c.addView(title,new LinearLayout.LayoutParams(-1,-2));
  TextView sub=t("Preparando a Home antes de abrir",13);sub.setTextColor(0xffaeb7b2);sub.setGravity(Gravity.CENTER);sub.setPadding(0,dp(2),0,0);LinearLayout.LayoutParams subLp=new LinearLayout.LayoutParams(-1,-2);subLp.setMargins(0,0,0,dp(22));c.addView(sub,subLp);

  final boolean wantMovies=movieCount!=0,wantSeries=seriesCount!=0;
  final BootstrapRow movieRow=wantMovies?bootstrapRow("▣","Filmes"):null;
  final BootstrapRow seriesRow=wantSeries?bootstrapRow("▤","Séries"):null;
  final BootstrapRow liveRow=liveCount>0?bootstrapRow("▦","Canais ao Vivo"):null;
  if(movieRow!=null){c.addView(movieRow.view,movieRow.view.getLayoutParams());setBootstrapRow(movieRow,1);}
  if(seriesRow!=null){c.addView(seriesRow.view,seriesRow.view.getLayoutParams());setBootstrapRow(seriesRow,1);}
  if(liveRow!=null){c.addView(liveRow.view,liveRow.view.getLayoutParams());setBootstrapRow(liveRow,2);}
  Space flex=new Space(this);c.addView(flex,new LinearLayout.LayoutParams(1,0,1));
  TextView bottom=t("Buscando direto do servidor…",12);bottom.setTextColor(0xff8e9993);bottom.setGravity(Gravity.CENTER);bottom.setPadding(0,dp(10),0,dp(8));c.addView(bottom,new LinearLayout.LayoutParams(-1,dp(44)));

  final boolean[] finished={false};
  fetchProviderSnapshot(movieCount,seriesCount,new PreparedHomeCB(){public void ok(JSONObject snapshot){
   if(finished[0])return;finished[0]=true;
   if(movieRow!=null)setBootstrapRow(movieRow,homeHasType(snapshot,1)?2:3);
   if(seriesRow!=null)setBootstrapRow(seriesRow,homeHasType(snapshot,2)?2:3);
   JSONArray liveSnapshot=snapshot.optJSONArray("live_channels");
   if(liveRow!=null)setBootstrapRow(liveRow,liveSnapshot!=null&&liveSnapshot.length()>0?2:3);
   sessionLiveKnown=true;sessionHasLive=liveSnapshot!=null&&liveSnapshot.length()>0;
   JSONArray data=snapshot.optJSONArray("result");if((data==null||data.length()==0)&&!sessionHasLive){showBootstrapFailure(c,bottom,name,movieCount,seriesCount,liveCount);return;}
   try{snapshot.put("catalog_complete",1);}catch(Exception ignored){}
   saveHomeCache(snapshot);sp.edit().putBoolean(homeExtrasKey(),true).putBoolean("provider_has_live",sessionHasLive).putInt("provider_live_count",liveSnapshot==null?0:liveSnapshot.length()).apply();homeExtrasStarted=true;
   BootstrapRow finalRow=bootstrapRow("▥","Pronto");finalRow.label.setText("Tudo carregado");setBootstrapRow(finalRow,2);c.addView(finalRow.view,Math.max(0,c.getChildCount()-2),finalRow.view.getLayoutParams());bottom.setText("Abrindo conteúdo…");
   // O catálogo inteiro já está na memória. Não esperamos capa, TMDB nem outra API.
   shell();
  }public void err(String e){if(finished[0])return;finished[0]=true;if(movieRow!=null)setBootstrapRow(movieRow,3);if(seriesRow!=null)setBootstrapRow(seriesRow,3);showBootstrapFailure(c,bottom,name,movieCount,seriesCount,liveCount);}});
 }
 void showBootstrapFailure(LinearLayout c,TextView bottom,String name,int movieCount,int seriesCount,int liveCount){
  BootstrapRow fail=bootstrapRow("!","Não foi possível carregar o conteúdo");setBootstrapRow(fail,3);c.addView(fail.view,Math.max(0,c.getChildCount()-2),fail.view.getLayoutParams());bottom.setText("Tente novamente ou escolha outro servidor.");
  Button retry=authSecondary("Tentar novamente");LinearLayout.LayoutParams rp=new LinearLayout.LayoutParams(-1,dp(52));rp.setMargins(0,dp(6),0,dp(6));c.addView(retry,Math.max(0,c.getChildCount()-2),rp);retry.setOnClickListener(v->showProviderBootstrap(name,movieCount,seriesCount,liveCount));
  TextView change=t("Escolher outro servidor",14);change.setTextColor(GREEN);change.setGravity(Gravity.CENTER);c.addView(change,Math.max(0,c.getChildCount()-2),new LinearLayout.LayoutParams(-1,dp(44)));change.setOnClickListener(v->providerSelectAfterLogin());
 }
 BootstrapRow bootstrapRow(String iconText,String labelText){
  BootstrapRow r=new BootstrapRow();r.view=new LinearLayout(this);r.view.setGravity(Gravity.CENTER_VERTICAL);r.view.setPadding(dp(12),dp(6),dp(10),dp(6));GradientDrawable bg=round(0xd6161c19,13);bg.setStroke(dp(1),0xff2a3530);r.view.setBackground(bg);LinearLayout.LayoutParams vp=new LinearLayout.LayoutParams(-1,dp(60));vp.setMargins(0,0,0,dp(9));r.view.setLayoutParams(vp);
  r.icon=t(iconText,17);r.icon.setTextColor(0xff89938e);r.icon.setGravity(Gravity.CENTER);r.icon.setPadding(0,0,0,0);r.icon.setBackground(round(0xff202825,10));r.view.addView(r.icon,new LinearLayout.LayoutParams(dp(40),dp(40)));
  r.label=t(labelText,14);r.label.setTypeface(null,1);r.label.setTextColor(0xffc6ccc8);r.label.setGravity(Gravity.CENTER_VERTICAL);r.label.setPadding(dp(12),0,dp(8),0);r.view.addView(r.label,new LinearLayout.LayoutParams(0,-1,1));
  FrameLayout end=new FrameLayout(this);r.spinner=new ProgressBar(this);r.spinner.setIndeterminate(true);try{r.spinner.getIndeterminateDrawable().setColorFilter(GREEN,android.graphics.PorterDuff.Mode.SRC_IN);}catch(Exception ignored){}FrameLayout.LayoutParams pp=new FrameLayout.LayoutParams(dp(28),dp(28),Gravity.CENTER);end.addView(r.spinner,pp);r.check=t("",18);r.check.setGravity(Gravity.CENTER);r.check.setPadding(0,0,0,0);end.addView(r.check,new FrameLayout.LayoutParams(-1,-1));r.view.addView(end,new LinearLayout.LayoutParams(dp(42),dp(42)));return r;
 }
 void setBootstrapRow(BootstrapRow r,int state){
  if(r==null)return;boolean active=state==1,ok=state==2,err=state==3;r.spinner.setVisibility(active?View.VISIBLE:View.GONE);r.check.setVisibility(active?View.GONE:View.VISIBLE);r.check.setText(ok?"✓":err?"!":"○");r.check.setTextColor(ok?GREEN:err?0xffff626d:0xff78827d);r.label.setTextColor(ok?0xffe9f4ed:err?0xffff8b92:active?Color.WHITE:0xffaeb7b2);r.icon.setTextColor(ok||active?GREEN:err?0xffff626d:0xff89938e);r.icon.setBackground(round(ok?0xff143522:active?0xff163226:err?0xff3a1c20:0xff202825,10));GradientDrawable g=round(0xd6161c19,13);g.setStroke(dp(1),ok?0xff2b6b46:err?0xff743039:active?GREEN:0xff2a3530);r.view.setBackground(g);
 }
 String homeCacheKey(){return "home_sections_"+uid+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);}
 String homeExtrasKey(){return "home_extras_"+uid+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);}
 // v16.41: o conteúdo preparado na troca do servidor fica SOMENTE na memória da sessão.
 // Não existe cache persistente do catálogo: ao reiniciar o app ou trocar de servidor, prepara de novo direto da fonte.
 // v16.54: o snapshot completo já é grande. Nunca serializar/clonar com toString(),
 // porque isso duplica o catálogo inteiro na heap e pode causar OutOfMemoryError.
 // O catálogo continua SOMENTE em memória e uma única instância é compartilhada pela sessão.
 void saveHomeCache(JSONObject j){if(j==null)return;preparedHomeProvider=Api.PROVIDER==null?"":Api.PROVIDER;preparedHomeData=j;}
 JSONObject readHomeCache(){String p=Api.PROVIDER==null?"":Api.PROVIDER;if(preparedHomeData==null||!p.equals(preparedHomeProvider))return null;return preparedHomeData;}
 void clearPreparedHome(){preparedHomeData=null;preparedHomeProvider="";homeExtrasStarted=false;detailMemoryCache.clear();detailPrefetchQueue.clear();detailPrefetchKeys.clear();}
 boolean homeHasType(JSONObject root,int wanted){JSONArray a=root==null?null:root.optJSONArray("result");if(a==null)return false;for(int i=0;i<a.length();i++){JSONObject sec=a.optJSONObject(i);if(sec==null)continue;int t=sec.optInt("type_id",sec.optInt("video_type",1));JSONArray d=sec.optJSONArray("data");if(t==wanted&&d!=null&&d.length()>0)return true;}return false;}
 JSONObject protectHomePayload(JSONObject fresh){ return fresh; }
 void warmCriticalHomeImages(JSONObject j,Runnable done){
  java.util.ArrayList<String> urls=new java.util.ArrayList<>();java.util.HashSet<String> seen=new java.util.HashSet<>();try{JSONArray sections=j.optJSONArray("result");if(sections!=null){for(int i=0;i<sections.length()&&urls.size()<8;i++){JSONObject sec=sections.optJSONObject(i);if(sec==null)continue;JSONArray data=sec.optJSONArray("data");if(data==null)continue;for(int k=0;k<data.length()&&k<3&&urls.size()<8;k++){JSONObject x=data.optJSONObject(k);if(x==null)continue;String land=x.optString("landscape",x.optString("landscape_img",""));String poster=x.optString("thumbnail",x.optString("portrait_img",x.optString("image","")));String u=!land.isEmpty()?land:poster;if(!u.isEmpty()&&seen.add(u))urls.add(u);}}}}catch(Exception ignored){}
  Img.prefetchCritical(this,urls,6,900,done);
 }
 void warmHomeImages(JSONObject j,Runnable done){
  java.util.ArrayList<String> critical=new java.util.ArrayList<>();java.util.ArrayList<String> all=new java.util.ArrayList<>();try{JSONArray sections=j.optJSONArray("result");if(sections!=null){for(int i=0;i<sections.length()&&all.size()<180;i++){JSONObject sec=sections.optJSONObject(i);if(sec==null)continue;JSONArray data=sec.optJSONArray("data");if(data==null)continue;for(int k=0;k<data.length()&&k<8&&all.size()<180;k++){JSONObject x=data.optJSONObject(k);if(x==null)continue;String poster=x.optString("thumbnail",x.optString("portrait_img",x.optString("image","")));String landscape=x.optString("landscape",x.optString("landscape_img",""));if(!poster.isEmpty()){all.add(poster);if(critical.size()<16)critical.add(poster);}if(!landscape.isEmpty()&&!landscape.equals(poster)){all.add(landscape);if(critical.size()<16)critical.add(landscape);}}}}}catch(Exception ignored){}
  Img.prefetch(this,critical,()->{done.run();Img.prefetchBackground(this,all);});
 }
 void prefetchRowImages(JSONArray a){if(a==null)return;java.util.ArrayList<String> urls=new java.util.ArrayList<>();for(int i=0;i<a.length()&&i<12;i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;String u=x.optString("thumbnail",x.optString("portrait_img",x.optString("image","")));if(!u.isEmpty())urls.add(u);}Img.prefetchBackground(this,urls);}
 void prepareHomeThenShell(TextView msg,Button action){
  if(msg!=null){msg.setTextColor(0xffa8b8b0);msg.setText("Preparando seu catálogo…");}
  fetchPreparedHome(-1,-1,new PreparedHomeCB(){public void ok(JSONObject j){
   JSONArray a=j.optJSONArray("result");if(a!=null&&a.length()>0){saveHomeCache(j);sp.edit().putBoolean(homeExtrasKey(),false).apply();homeExtrasStarted=false;final int[] gates={0};final boolean[] opened={false};Runnable ready=()->{gates[0]++;if(gates[0]>=2&&!opened[0]){opened[0]=true;shell();prefetchDetailsFromCatalog(j,10);}};warmHomeImages(j,ready);prepareCriticalDetails(j,ready);}
   else shell();
  }public void err(String e){shell();}});
 }
 void prepareCriticalDetails(JSONObject rootJson,Runnable done){
  java.util.ArrayList<JSONObject> items=collectDetailPrefetchItems(rootJson,6);if(items.isEmpty()){done.run();return;}final int[] remaining={items.size()};final boolean[] finished={false};Handler h=new Handler(Looper.getMainLooper());Runnable finish=()->{if(!finished[0]){finished[0]=true;done.run();}};h.postDelayed(finish,3500);
  for(JSONObject x:items){if(readDetailCache(x)!=null){remaining[0]--;if(remaining[0]<=0){h.removeCallbacks(finish);finish.run();}continue;}Api.post("content_detail",Api.m("user_id",uid,"video_id",x.optString("id"),"video_type",x.optString("video_type","1")),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d!=null)saveDetailCache(x,d);remaining[0]--;if(remaining[0]<=0){h.removeCallbacks(finish);finish.run();}}public void err(String e){remaining[0]--;if(remaining[0]<=0){h.removeCallbacks(finish);finish.run();}}});}
 }
 java.util.ArrayList<JSONObject> collectDetailPrefetchItems(JSONObject rootJson,int limit){java.util.ArrayList<JSONObject> out=new java.util.ArrayList<>();java.util.HashSet<String> seen=new java.util.HashSet<>();try{JSONArray sections=rootJson.optJSONArray("result");if(sections==null)return out;for(int pass=0;pass<2&&out.size()<limit;pass++){for(int i=0;i<sections.length()&&out.size()<limit;i++){JSONObject sec=sections.optJSONObject(i);if(sec==null)continue;JSONArray a=sec.optJSONArray("data");if(a==null)continue;int max=pass==0?Math.min(2,a.length()):Math.min(5,a.length());for(int k=0;k<max&&out.size()<limit;k++){JSONObject x=a.optJSONObject(k);if(x==null)continue;String key=detailCacheKey(x);if(seen.add(key))out.add(x);}}}}catch(Exception ignored){}return out;}
 void prefetchDetailsFromCatalog(JSONObject rootJson,int limit){for(JSONObject x:collectDetailPrefetchItems(rootJson,limit))queueDetailPrefetch(x);pumpDetailPrefetch();}
 void queueDetailPrefetch(JSONObject x){if(x==null)return;JSONObject c=mergeDetailJson(x,readDetailCache(x));if(c!=null&&!detailNeedsEnrich(c))return;String k=detailCacheKey(x);if(detailPrefetchKeys.contains(k))return;detailPrefetchKeys.add(k);try{detailPrefetchQueue.add(x);}catch(Exception ignored){detailPrefetchKeys.remove(k);}}
 void finishDetailPrefetch(String key){detailPrefetchActive--;detailPrefetchKeys.remove(key);pumpDetailPrefetch();}
 void pumpDetailPrefetch(){while(detailPrefetchActive<3&&!detailPrefetchQueue.isEmpty()){JSONObject x=detailPrefetchQueue.poll();if(x==null)continue;String key=detailCacheKey(x);detailPrefetchActive++;Api.post("content_detail",Api.m("user_id",uid,"video_id",x.optString("id"),"video_type",x.optString("video_type","1")),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d!=null)saveDetailCache(x,d);JSONObject now=mergeDetailJson(x,readDetailCache(x));if(now!=null&&!detailNeedsEnrich(now)){finishDetailPrefetch(key);return;}Api.post("content_enrich",Api.m("user_id",uid,"video_id",x.optString("id"),"video_type",x.optString("video_type","1")),new Api.CB(){public void ok(JSONObject e){JSONArray ea=e.optJSONArray("result");JSONObject ed=(ea!=null&&ea.length()>0)?ea.optJSONObject(0):null;if(ed!=null)saveDetailCache(x,ed);finishDetailPrefetch(key);}public void err(String z){finishDetailPrefetch(key);}});}public void err(String e){Api.post("content_enrich",Api.m("user_id",uid,"video_id",x.optString("id"),"video_type",x.optString("video_type","1")),new Api.CB(){public void ok(JSONObject r){JSONArray a=r.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d!=null)saveDetailCache(x,d);finishDetailPrefetch(key);}public void err(String z){finishDetailPrefetch(key);}});}});}}
 void shell(){
  authScreen=false;providerSwitchScreen=false;detailOpen=false;savedScroll=null;savedBody=null;
  base(false);
  contentFrame=new FrameLayout(this);
  mainScroll=new ScrollView(this);mainScroll.setFillViewport(true);mainScroll.setVerticalScrollBarEnabled(false);
  body=new LinearLayout(this);body.setOrientation(LinearLayout.VERTICAL);body.setPadding(0,dp(2),0,dp(12));mainScroll.addView(body);
  contentFrame.addView(mainScroll,new FrameLayout.LayoutParams(-1,-1));
  homeScrollCache=mainScroll;homeBodyCache=body;homeViewAvailable=true;homeScrollY=0;
  root.addView(contentFrame,new LinearLayout.LayoutParams(-1,0,1));
  navBar=new LinearLayout(this);navBar.setGravity(Gravity.CENTER);navBar.setPadding(0,dp(3),0,0);navBar.setBackgroundColor(0xff090d12);
  navHome=navItem("⌂","Início",0);navFav=navItem("♡","Favoritos",1);navTv=sessionHasLive?navItem("▣","TV",2):null;navDownloads=navItem("⇩","Downloads",3);navProfile=navItem("♙","Perfil",4);
  root.addView(navBar,new LinearLayout.LayoutParams(-1,dp(64)));
  home();if(tvMode)requestTvFocus(navHome);
 }
 void cancelProviderSwitch(){providerSwitchScreen=false;shell();profile();}
 TextView navItem(String icon,String title,int idx){TextView v=t(icon+"\n"+title,11);v.setGravity(Gravity.CENTER);v.setPadding(0,dp(3),0,dp(2));v.setOnClickListener(x->{
  if(searchScreenOpen){searchScreenOpen=false;try{android.view.inputmethod.InputMethodManager im=(android.view.inputmethod.InputMethodManager)getSystemService(INPUT_METHOD_SERVICE);View f=getCurrentFocus();if(im!=null&&f!=null)im.hideSoftInputFromWindow(f.getWindowToken(),0);}catch(Exception ignored){}}
  if(detailOpen){int previous=savedNavIndex;closeDetails();if(idx==previous)return;}
  if(idx==0){if(currentNavIndex==0&&mainScroll==homeScrollCache)return;restoreHomeView();return;}
  if(currentNavIndex==0&&mainScroll==homeScrollCache)leaveHomeForPage();
  if(idx==1)favorites();else if(idx==2)liveContent();else if(idx==3)downloads();else profile();
 });navBar.addView(v,new LinearLayout.LayoutParams(0,-1,1));return v;}
 void setNav(int idx){currentNavIndex=idx;if(navHome==null)return;TextView[] n={navHome,navFav,navTv,navDownloads,navProfile};for(int i=0;i<n.length;i++)if(n[i]!=null)n[i].setTextColor(i==idx?GREEN:0xffa9b0ad);}
 void rememberHomeView(){if(mainScroll!=null&&body!=null&&currentNavIndex==0&&mainScroll==homeScrollCache&&!detailOpen){homeScrollY=mainScroll.getScrollY();homeBodyCache=body;homeViewAvailable=true;}}
 void createTransientPageHost(){if(contentFrame==null)return;if(mainScroll!=null&&mainScroll.getParent()==contentFrame)contentFrame.removeView(mainScroll);mainScroll=new ScrollView(this);mainScroll.setFillViewport(true);mainScroll.setVerticalScrollBarEnabled(false);body=new LinearLayout(this);body.setOrientation(LinearLayout.VERTICAL);body.setPadding(0,dp(2),0,dp(12));mainScroll.addView(body);contentFrame.addView(mainScroll,new FrameLayout.LayoutParams(-1,-1));}
 void leaveHomeForPage(){rememberHomeView();createTransientPageHost();}
 void restoreHomeView(){
  if(homeViewAvailable&&homeScrollCache!=null&&homeBodyCache!=null&&contentFrame!=null){
   if(mainScroll!=homeScrollCache){if(mainScroll!=null&&mainScroll.getParent()==contentFrame)contentFrame.removeView(mainScroll);mainScroll=homeScrollCache;body=homeBodyCache;if(mainScroll.getParent()==null)contentFrame.addView(mainScroll,new FrameLayout.LayoutParams(-1,-1));}
   setNav(0);final int y=homeScrollY;mainScroll.post(()->{mainScroll.scrollTo(0,y);mainScroll.requestLayout();});return;
  }
  home();
 }
  void clear(){viewGen++; body.removeAllViews();}
 void home(){homeTab("Recomendações");}
 void homeTab(String selected){
  activeHomeTab=selected;
  clear();setNav(0);homeScrollCache=mainScroll;homeBodyCache=body;homeViewAvailable=true;homeScrollY=0;homeTop(selected);final int gen=viewGen;
  if(selected.equals("Recomendações")){loadExplore(gen);return;}
  int typeId=selected.equals("Séries")?2:1;
  // v16.57: Filmes/Séries permanecem dentro da Home como na referência:
  // destaque grande primeiro e trilhos abaixo, usando apenas o snapshot já em memória.
  JSONArray featured=featuredForType(typeId,12);
  if(featured.length()>0)featureCarousel(featured);
  loadAllCategorySections(typeId,selected,gen);
 }
 void homeSectionTab(String key,JSONObject sec){
  if(sec==null)return;activeHomeTab=key;clear();setNav(0);homeScrollCache=mainScroll;homeBodyCache=body;homeViewAvailable=true;homeScrollY=0;homeTop(key);final int gen=viewGen;
  JSONArray data=sec.optJSONArray("data");if(data==null||data.length()==0)return;
  // A troca de aba é instantânea: nada de nova chamada ao painel/Xtream.
  featureCarousel(data);
  String title=fixTitle(sec.optString("title","Conteúdos"));
  JSONObject same=sec;sectionHeader(title,()->openSection(same));posterRow(data);
  int typeId=sec.optInt("type_id",sec.optInt("video_type",1));
  JSONObject prepared=readHomeCache();JSONArray sections=prepared==null?null:prepared.optJSONArray("result");int added=0;
  if(sections!=null){for(int i=0;i<sections.length()&&added<2;i++){if(gen!=viewGen)return;JSONObject other=sections.optJSONObject(i);if(other==null||other==sec)continue;int t=other.optInt("type_id",other.optInt("video_type",1));JSONArray a=other.optJSONArray("data");if(t!=typeId||a==null||a.length()==0)continue;String ot=fixTitle(other.optString("title",""));if(ot.equalsIgnoreCase(title))continue;final JSONObject f=other;sectionHeader(ot,()->openSection(f));posterRow(a);added++;}}
 }
 JSONArray featuredForType(int typeId,int max){
  JSONArray out=new JSONArray();JSONObject prepared=readHomeCache();JSONArray sections=prepared==null?null:prepared.optJSONArray("result");if(sections==null||max<=0)return out;
  java.util.ArrayList<JSONObject> pool=new java.util.ArrayList<>();java.util.HashSet<String> seen=new java.util.HashSet<>();
  for(int i=0;i<sections.length();i++){JSONObject sec=sections.optJSONObject(i);if(sec==null)continue;int t=sec.optInt("type_id",sec.optInt("video_type",1));if(t!=typeId)continue;JSONArray a=sec.optJSONArray("data");if(a==null)continue;for(int j=0;j<a.length();j++){JSONObject x=a.optJSONObject(j);if(x==null)continue;String k=itemKey(x);if(seen.add(k))pool.add(x);}}
  java.util.Collections.shuffle(pool,new java.util.Random(System.nanoTime()^((long)(++featuredShuffleTick)*1103515245L)^typeId));
  for(int i=0;i<Math.min(max,pool.size());i++)out.put(pool.get(i));return out;
 }
 void loadExplore(final int gen){
  JSONObject cached=readHomeCache();
  if(cached!=null&&cached.optJSONArray("result")!=null&&cached.optJSONArray("result").length()>0){renderExplore(cached,gen,false);refreshCatalogInBackground();return;}
  final TextView loading=t("Atualizando conteúdo…",14);loading.setTextColor(0xff8f9994);loading.setGravity(Gravity.CENTER);body.addView(loading,new LinearLayout.LayoutParams(-1,dp(64)));
  final Handler timeout=new Handler(Looper.getMainLooper());final boolean[] finished={false};final Runnable failSafe=()->{if(gen==viewGen&&!finished[0]){if(loading.getParent()!=null)body.removeView(loading);TextView m=t("Não foi possível carregar agora. Toque para tentar novamente.",14);m.setTextColor(0xff9da7a2);m.setGravity(Gravity.CENTER);m.setOnClickListener(v->home());body.addView(m,new LinearLayout.LayoutParams(-1,dp(64)));finished[0]=true;}};timeout.postDelayed(failSafe,14000);
  fetchPreparedHome(-1,-1,new PreparedHomeCB(){public void ok(JSONObject j){if(gen!=viewGen||finished[0])return;timeout.removeCallbacks(failSafe);if(loading.getParent()!=null)body.removeView(loading);JSONObject stable=protectHomePayload(j);JSONArray a=stable==null?null:stable.optJSONArray("result");if(a==null||a.length()==0){failSafe.run();return;}finished[0]=true;saveHomeCache(stable);sp.edit().putBoolean(homeExtrasKey(),false).apply();homeExtrasStarted=false;renderExplore(stable,gen,false);refreshCatalogInBackground();}public void err(String x){if(gen!=viewGen||finished[0])return;timeout.removeCallbacks(failSafe);failSafe.run();}});
 }
 void refreshCatalogInBackground(){ /* v16.40: painel v72 lê o catálogo direto da fonte */ }
 void renderExplore(JSONObject rootJson,final int gen,boolean useOneTimeExtras){
  if(gen!=viewGen)return;final java.util.HashSet<String> shownCats=new java.util.HashSet<>();final java.util.HashSet<String> shownNames=new java.util.HashSet<>();
  JSONArray sections=rootJson.optJSONArray("result");boolean rendered=false;
  if(sections!=null&&sections.length()>0){
   JSONArray featured=buildFeaturedMix(sections,12);
   if(featured.length()>0&&gen==viewGen){featureCarousel(featured);promoLive();rendered=true;}
   if(gen!=viewGen)return;
   final JSONArray recentMovies=buildRecentlyAddedMovies(sections,12);
   if(recentMovies.length()>0){
    final JSONObject recentSec=new JSONObject();try{recentSec.put("title","Adicionados recentemente");recentSec.put("category_id",0);recentSec.put("type_id",1);recentSec.put("data",recentMovies);}catch(Exception ignored){}
    sectionHeader("Adicionados recentemente",()->openSection(recentSec));posterRow(recentMovies);rendered=true;
   }
   if(gen!=viewGen)return;continueHost=new LinearLayout(MainActivity.this);continueHost.setOrientation(LinearLayout.VERTICAL);body.addView(continueHost,new LinearLayout.LayoutParams(-1,-2));loadContinueWatchingSafe(gen);

   // A Home de Recomendações deve manter FILMES antes de SÉRIES, independentemente
   // da ordem em que o painel devolve as seções. Também reservamos hosts separados
   // para que categorias de filmes recuperadas de get_category não apareçam depois
   // das categorias de séries por causa do retorno assíncrono.
   final LinearLayout movieHost=new LinearLayout(MainActivity.this);movieHost.setOrientation(LinearLayout.VERTICAL);body.addView(movieHost,new LinearLayout.LayoutParams(-1,-2));
   final LinearLayout seriesHost=new LinearLayout(MainActivity.this);seriesHost.setOrientation(LinearLayout.VERTICAL);body.addView(seriesHost,new LinearLayout.LayoutParams(-1,-2));
   final LinearLayout otherHost=new LinearLayout(MainActivity.this);otherHost.setOrientation(LinearLayout.VERTICAL);body.addView(otherHost,new LinearLayout.LayoutParams(-1,-2));

   // Primeiro registra todas as categorias presentes no payload para evitar duplicação.
   for(int i=0;i<sections.length();i++){JSONObject sec=sections.optJSONObject(i);if(sec==null)continue;if("recently_added".equals(sec.optString("section_key","")))continue;JSONArray data=sec.optJSONArray("data");if(data==null||data.length()==0)continue;int typeId=sec.optInt("type_id",sec.optInt("video_type",1));int cid=sec.optInt("category_id",0);if(cid>0)shownCats.add(typeId+":"+cid);String title=fixTitle(sec.optString("title","Conteúdos"));shownNames.add((typeId+":"+title.trim().toLowerCase(java.util.Locale.ROOT)));}

   // Renderiza filmes primeiro, depois séries. Assim a Home nunca vira visualmente
   // uma lista só de séries quando o section_list vier em ordem diferente.
   for(int wanted=1;wanted<=2;wanted++){
    LinearLayout target=wanted==1?movieHost:seriesHost;
    for(int i=0;i<sections.length();i++){if(gen!=viewGen)return;JSONObject sec=sections.optJSONObject(i);if(sec==null)continue;if("recently_added".equals(sec.optString("section_key","")))continue;JSONArray data=sec.optJSONArray("data");if(data==null||data.length()==0)continue;int typeId=sec.optInt("type_id",sec.optInt("video_type",1));if(typeId!=wanted)continue;String title=fixTitle(sec.optString("title",wanted==1?"Filmes":"Séries"));final JSONObject fsec=sec;sectionHeaderInto(target,title,()->openSection(fsec));posterRowInto(target,data);rendered=true;}
   }
   // Qualquer seção sem tipo reconhecido fica por último, sem interferir na ordem Filme/Série.
   for(int i=0;i<sections.length();i++){if(gen!=viewGen)return;JSONObject sec=sections.optJSONObject(i);if(sec==null)continue;if("recently_added".equals(sec.optString("section_key","")))continue;JSONArray data=sec.optJSONArray("data");if(data==null||data.length()==0)continue;int typeId=sec.optInt("type_id",sec.optInt("video_type",1));if(typeId==1||typeId==2)continue;String title=fixTitle(sec.optString("title","Conteúdos"));final JSONObject fsec=sec;sectionHeaderInto(otherHost,title,()->openSection(fsec));posterRowInto(otherHost,data);rendered=true;}

   // v16.39: a Home não depende mais do payload misto para decidir se existem Filmes.
   // Busca cada família explicitamente no endpoint section_list (type_id=1/2). Isso evita
   // o bug em que um payload/cache dominado por Séries fazia todas as categorias de Filmes
   // desaparecerem da Home. Os hosts continuam em ordem fixa: Filmes primeiro, Séries depois.
   // O bootstrap já carregou o section_list completo direto da fonte. Não refaz a mesma
   // consulta ao entrar na Home; só busca um tipo separadamente se ele realmente estiver ausente.
   // v16.48: a Home abre com o conjunto crítico já pronto e completa o restante
   // silenciosamente, sem mostrar “Carregando recomendações”.
   if(useOneTimeExtras){appendMissingHomeCategoriesCachedInto("movie",1,shownCats,shownNames,gen,rootJson,movieHost);
   appendMissingHomeCategoriesCachedInto("series",2,shownCats,shownNames,gen,rootJson,seriesHost);}
  }
  if(!rendered){TextView m=t("Nenhuma recomendação disponível no momento.",14);m.setTextColor(0xff8f9994);m.setGravity(Gravity.CENTER);body.addView(m,new LinearLayout.LayoutParams(-1,dp(64)));}
 }

 void loadTypedHomeSectionsInto(final int typeId,final LinearLayout host,final java.util.HashSet<String> shownCats,final java.util.HashSet<String> shownNames,final int gen,final JSONObject rootJson){
  final String type=typeId==2?"series":"movie";
  fetchHomePart(typeId,0,new PreparedHomeCB(){public void ok(JSONObject j){
   if(!hostValid(gen,host))return;JSONArray secs=j.optJSONArray("result");
   if(secs!=null&&secs.length()>0){
    // Só substitui o conteúdo desse bloco quando a resposta tipada realmente trouxe dados.
    // Assim uma oscilação de rede não apaga o que já estava visível.
    host.removeAllViews();
    for(int i=0;i<secs.length();i++){JSONObject sec=secs.optJSONObject(i);if(sec==null)continue;if("recently_added".equals(sec.optString("section_key","")))continue;JSONArray data=sec.optJSONArray("data");if(data==null||data.length()==0)continue;int cid=sec.optInt("category_id",0);String title=fixTitle(sec.optString("title",typeId==2?"Séries":"Filmes"));if(cid>0)shownCats.add(typeId+":"+cid);shownNames.add(typeId+":"+title.trim().toLowerCase(java.util.Locale.ROOT));final JSONObject fsec=sec;sectionHeaderInto(host,title,()->openSection(fsec));posterRowInto(host,data);}
   }
   appendMissingHomeCategoriesCachedInto(type,typeId,shownCats,shownNames,gen,rootJson,host);
  }public void err(String e){
   if(hostValid(gen,host))appendMissingHomeCategoriesCachedInto(type,typeId,shownCats,shownNames,gen,rootJson,host);
  }});
 }

 void appendMissingHomeCategoriesCachedInto(String type,int typeId,java.util.HashSet<String> shownCats,java.util.HashSet<String> shownNames,final int gen,final JSONObject rootJson,final LinearLayout host){
  Api.post("get_category",Api.m("type",type,"user_id",uid),new Api.CB(){public void ok(JSONObject j){
   if(!hostValid(gen,host))return;JSONArray cats=j.optJSONArray("result");if(cats==null)return;
   java.util.ArrayList<JSONObject> pending=new java.util.ArrayList<>();java.util.HashSet<String> queuedCats=new java.util.HashSet<>(shownCats);java.util.HashSet<String> queuedNames=new java.util.HashSet<>(shownNames);
   for(int i=0;i<cats.length();i++){JSONObject cat=cats.optJSONObject(i);if(cat==null)continue;String cid=cat.optString("category_id",cat.optString("id",""));if(cid.isEmpty())continue;String key=typeId+":"+cid;if(queuedCats.contains(key))continue;String name=fixTitle(cat.optString("category_name",cat.optString("name",typeId==2?"Séries":"Filmes")));String nameKey=typeId+":"+name.trim().toLowerCase(java.util.Locale.ROOT);if(queuedNames.contains(nameKey))continue;queuedCats.add(key);queuedNames.add(nameKey);pending.add(cat);}
   int[] next={0},active={0};pumpMissingHomeCategories(pending,next,active,typeId,shownCats,shownNames,gen,rootJson,host);
  }public void err(String e){}});
 }
 void pumpMissingHomeCategories(java.util.ArrayList<JSONObject> pending,int[] next,int[] active,int typeId,java.util.HashSet<String> shownCats,java.util.HashSet<String> shownNames,int gen,JSONObject rootJson,LinearLayout host){
  if(!hostValid(gen,host))return;
  while(active[0]<2&&next[0]<pending.size()){
   final JSONObject cat=pending.get(next[0]++);String cid=cat.optString("category_id",cat.optString("id",""));String name=fixTitle(cat.optString("category_name",cat.optString("name",typeId==2?"Séries":"Filmes")));int raw;
   try{int n=Integer.parseInt(cid);raw=typeId==2?1000000+n:n;}catch(Exception e){continue;}
   final String fcid=cid, fname=name;active[0]++;
   Api.post("content_by_category",Api.m("user_id",uid,"category_id",String.valueOf(raw),"page_no","1"),new Api.CB(){public void ok(JSONObject r){
    active[0]--;if(hostValid(gen,host)){JSONArray a=r.optJSONArray("result");if(a!=null&&a.length()>0){shownCats.add(typeId+":"+fcid);shownNames.add(typeId+":"+fname.trim().toLowerCase(java.util.Locale.ROOT));JSONObject sec=new JSONObject();try{sec.put("title",fname);sec.put("category_id",Integer.parseInt(fcid));sec.put("type_id",typeId);sec.put("data",a);JSONArray rootSections=rootJson.optJSONArray("result");if(rootSections!=null){rootSections.put(sec);saveHomeCache(rootJson);}host.post(()->{if(hostValid(gen,host)){sectionHeaderInto(host,fname,()->openSection(sec));posterRowInto(host,a);}});}catch(Exception ignored){}}}pumpMissingHomeCategories(pending,next,active,typeId,shownCats,shownNames,gen,rootJson,host);
   }public void err(String e){active[0]--;pumpMissingHomeCategories(pending,next,active,typeId,shownCats,shownNames,gen,rootJson,host);}});
  }
 }
 void loadContinueWatchingSafe(final int gen){
  final LinearLayout target=continueHost;final LinearLayout host=body;
  if(!hostValid(gen,host)||target==null)return;final JSONArray local=localMovieContinueItems();if(local.length()>0)renderContinueItems(target,local);
  Api.post("get_continue_watching",Api.m("user_id",uid),new Api.CB(){public void ok(JSONObject j){if(!hostValid(gen,host)||target==null)return;JSONArray merged=mergeContinueItems(j.optJSONArray("result"),local);if(merged.length()>0)renderContinueItems(target,merged);}public void err(String e){if(local.length()>0&&hostValid(gen,host))renderContinueItems(target,local);}});
 }
 boolean hostValid(int gen,LinearLayout host){return gen==viewGen||(detailOpen&&savedBody==host);}
 void appendMissingHomeCategories(String type,int typeId,java.util.HashSet<String> shownCats,java.util.HashSet<String> shownNames,final int gen){
  final LinearLayout host=body;
  Api.post("get_category",Api.m("type",type,"user_id",uid),new Api.CB(){public void ok(JSONObject j){if(!hostValid(gen,host))return;JSONArray cats=j.optJSONArray("result");if(cats==null)return;for(int i=0;i<cats.length();i++){if(!hostValid(gen,host))return;JSONObject cat=cats.optJSONObject(i);if(cat==null)continue;String cid=cat.optString("category_id",cat.optString("id",""));if(cid.isEmpty())continue;String key=typeId+":"+cid;if(shownCats.contains(key))continue;shownCats.add(key);String name=fixTitle(cat.optString("category_name",cat.optString("name",typeId==2?"Séries":"Filmes")));String nameKey=name.trim().toLowerCase(java.util.Locale.ROOT);if(shownNames.contains(nameKey))continue;shownNames.add(nameKey);LinearLayout holder=new LinearLayout(MainActivity.this);holder.setOrientation(LinearLayout.VERTICAL);TextView wait=t(name+"  ·  carregando…",15);wait.setTextColor(0xff9da7a2);holder.addView(wait,new LinearLayout.LayoutParams(-1,dp(42)));host.addView(holder,new LinearLayout.LayoutParams(-1,-2));int raw;try{int n=Integer.parseInt(cid);raw=typeId==2?1000000+n:n;}catch(Exception e){host.removeView(holder);continue;}final int fraw=raw;final String fcid=cid;Api.post("content_by_category",Api.m("user_id",uid,"category_id",String.valueOf(fraw),"page_no","1"),new Api.CB(){public void ok(JSONObject r){if(!hostValid(gen,host))return;JSONArray a=r.optJSONArray("result");if(a==null||a.length()==0){host.removeView(holder);return;}holder.removeAllViews();JSONObject sec=new JSONObject();try{sec.put("title",name);sec.put("category_id",Integer.parseInt(fcid));sec.put("type_id",typeId);sec.put("data",a);}catch(Exception e){}sectionHeaderInto(holder,name,()->openSection(sec));posterRowInto(holder,a);}public void err(String e){if(hostValid(gen,host))host.removeView(holder);}});}}public void err(String e){}});
 }
 void loadAllCategorySections(int typeId,String selected,final int gen){
  final LinearLayout host=body;JSONObject prepared=readHomeCache();JSONArray secs=prepared==null?null:prepared.optJSONArray("result");boolean any=false;
  java.util.HashSet<String> shownCats=new java.util.HashSet<>();java.util.HashSet<String> shownNames=new java.util.HashSet<>();
  if(secs!=null){for(int i=0;i<secs.length();i++){JSONObject sec=secs.optJSONObject(i);if(sec==null||"recently_added".equals(sec.optString("section_key","")))continue;int t=sec.optInt("type_id",sec.optInt("video_type",1));JSONArray data=sec.optJSONArray("data");if(t!=typeId||data==null||data.length()==0)continue;String title=fixTitle(sec.optString("title",typeId==2?"Séries":"Filmes"));int cid=sec.optInt("category_id",0);if(cid>0)shownCats.add(typeId+":"+cid);shownNames.add(typeId+":"+title.trim().toLowerCase(java.util.Locale.ROOT));final JSONObject fsec=sec;sectionHeaderInto(host,title,()->openSection(fsec));posterRowInto(host,data);any=true;}}
  if(any&&prepared!=null){if(prepared.optInt("catalog_complete",0)!=1)appendMissingHomeCategoriesCachedInto(typeId==2?"series":"movie",typeId,shownCats,shownNames,gen,prepared,host);return;}
  loadEveryCategory(typeId==2?"series":"movie",typeId,false,gen,host);
 }
 void loadEveryCategory(String type,int typeId,boolean continueWithSeries,final int gen,final LinearLayout host){
  Api.post("get_category",Api.m("type",type,"user_id",uid),new Api.CB(){public void ok(JSONObject j){if(!hostValid(gen,host))return;JSONArray cats=j.optJSONArray("result");if(cats==null||cats.length()==0){if(continueWithSeries)loadEveryCategory("series",2,false,gen,host);else host.addView(t("Nenhuma categoria disponível.",14));return;}loadCategoryAt(cats,0,typeId,continueWithSeries,gen,host);}public void err(String x){if(!hostValid(gen,host))return;if(continueWithSeries)loadEveryCategory("series",2,false,gen,host);else host.addView(t("Não foi possível carregar todas as categorias.",14));}});
 }
 void loadCategoryAt(JSONArray cats,int index,int typeId,boolean continueWithSeries,final int gen,final LinearLayout host){
  if(!hostValid(gen,host))return;if(index>=cats.length()){if(continueWithSeries)loadEveryCategory("series",2,false,gen,host);return;}
  JSONObject cat=cats.optJSONObject(index);if(cat==null){loadCategoryAt(cats,index+1,typeId,continueWithSeries,gen,host);return;}
  String cid=cat.optString("category_id",cat.optString("id",""));String title=fixTitle(cat.optString("category_name",cat.optString("name",typeId==2?"Séries":"Filmes")));
  if(cid.isEmpty()){loadCategoryAt(cats,index+1,typeId,continueWithSeries,gen,host);return;}int numericCid=0;try{numericCid=Integer.parseInt(cid);}catch(Exception ignored){}if(numericCid<=0){loadCategoryAt(cats,index+1,typeId,continueWithSeries,gen,host);return;}final int finalCid=numericCid;int raw=typeId==2?1000000+numericCid:numericCid;
  Api.post("content_by_category",Api.m("user_id",uid,"category_id",String.valueOf(raw),"page_no","1"),new Api.CB(){public void ok(JSONObject j){if(!hostValid(gen,host))return;JSONArray data=j.optJSONArray("result");if(data!=null&&data.length()>0){JSONObject sec=new JSONObject();try{sec.put("title",title);sec.put("category_id",finalCid);sec.put("type_id",typeId);sec.put("data",data);}catch(Exception ignored){}sectionHeaderInto(host,title,()->openSection(sec));posterRowInto(host,data);}loadCategoryAt(cats,index+1,typeId,continueWithSeries,gen,host);}public void err(String x){if(hostValid(gen,host))loadCategoryAt(cats,index+1,typeId,continueWithSeries,gen,host);}});
 }
 void openSection(JSONObject sec){
  if(currentNavIndex==0&&mainScroll==homeScrollCache)leaveHomeForPage();
  clear();setNav(0);final int gen=viewGen;String title=fixTitle(sec.optString("title","Conteúdos"));pageTitle(title,()->restoreHomeView());JSONArray data=sec.optJSONArray("data");if(data!=null)grid(data);
  int cid=sec.optInt("category_id",0);JSONObject prepared=readHomeCache();boolean complete=prepared!=null&&prepared.optInt("catalog_complete",0)==1;
  // v16.53: se o snapshot completo já está em memória, a seção NÃO consulta a rede de novo.
  if(cid>0&&!complete){int raw=sec.optInt("type_id",1)==2?1000000+cid:cid;Api.post("content_by_category",Api.m("user_id",uid,"category_id",String.valueOf(raw),"page_no","1"),new Api.CB(){public void ok(JSONObject j){if(gen!=viewGen)return;JSONArray a=j.optJSONArray("result");if(a!=null&&a.length()>0){body.removeViews(1,Math.max(0,body.getChildCount()-1));grid(a);}}public void err(String x){}});}
 }
 void grid(JSONArray a){
  GridLayout g=new GridLayout(this);g.setColumnCount(3);g.setUseDefaultMargins(false);body.addView(g,new LinearLayout.LayoutParams(-1,-2));
  if(a==null||a.length()==0)return;int w=(getResources().getDisplayMetrics().widthPixels-dp(52))/3;int gen=viewGen;addGridChunk(g,a,0,w,gen);
 }
 void addGridChunk(GridLayout g,JSONArray a,int start,int w,int gen){
  if(gen!=viewGen||g==null||g.getParent()==null)return;int end=Math.min(a.length(),start+12);
  for(int i=start;i<end;i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;LinearLayout c=card(x);GridLayout.LayoutParams lp=new GridLayout.LayoutParams();lp.width=w;lp.height=dp(196);lp.setMargins(dp(3),dp(4),dp(5),dp(8));g.addView(c,lp);}
  if(end<a.length())g.postDelayed(()->addGridChunk(g,a,end,w,gen),16);
 }
 void refreshHomeHeaderBranding(){
  if(homeHeaderLogo==null||homeHeaderBrandFallback==null)return;
  String u=logoUrl==null?"":logoUrl.trim();
  if(!u.isEmpty()){
   homeHeaderLogo.setVisibility(View.VISIBLE);homeHeaderBrandFallback.setVisibility(View.GONE);Img.load(homeHeaderLogo,u);
  }else{
   homeHeaderLogo.setVisibility(View.GONE);homeHeaderBrandFallback.setVisibility(View.VISIBLE);String n=appName==null?"":appName.trim();homeHeaderBrandFallback.setText(n.isEmpty()?"GreenPlay":n);homeHeaderBrandFallback.setTextColor(Color.WHITE);
  }
 }
 void homeTop(String selected){
  // v16.57: medidas e comportamento alinhados à referência enviada em vídeo.
  // O cabeçalho fica mais baixo, a busca mais fina/larga e as abas trocam o
  // conteúdo da própria Home sem abrir uma página separada.
  LinearLayout topWrap=new LinearLayout(this);topWrap.setOrientation(LinearLayout.VERTICAL);topWrap.setPadding(0,dp(34),0,0);

  LinearLayout top=new LinearLayout(this);top.setGravity(Gravity.CENTER_VERTICAL);top.setPadding(0,0,0,0);
  FrameLayout brandSlot=new FrameLayout(this);
  homeHeaderLogo=new ImageView(this);homeHeaderLogo.setScaleType(ImageView.ScaleType.FIT_CENTER);homeHeaderLogo.setAdjustViewBounds(true);brandSlot.addView(homeHeaderLogo,new FrameLayout.LayoutParams(-1,-1));
  homeHeaderBrandFallback=t(appName==null||appName.trim().isEmpty()?"GreenPlay":appName.trim(),14);homeHeaderBrandFallback.setTextColor(Color.WHITE);homeHeaderBrandFallback.setTypeface(null,1);homeHeaderBrandFallback.setGravity(Gravity.CENTER_VERTICAL|Gravity.LEFT);homeHeaderBrandFallback.setPadding(0,0,0,0);brandSlot.addView(homeHeaderBrandFallback,new FrameLayout.LayoutParams(-1,-1));
  LinearLayout.LayoutParams brandLp=new LinearLayout.LayoutParams(dp(56),dp(36));brandLp.setMargins(0,0,dp(9),0);top.addView(brandSlot,brandLp);refreshHomeHeaderBranding();

  LinearLayout searchBox=new LinearLayout(this);searchBox.setGravity(Gravity.CENTER_VERTICAL);searchBox.setPadding(dp(13),0,dp(5),0);GradientDrawable sBg=round(0xff292b2c,21);sBg.setStroke(dp(1),0xff444748);searchBox.setBackground(sBg);
  TextView hint=t("Buscar",14);hint.setTextColor(0xffaeb2b4);hint.setGravity(Gravity.CENTER_VERTICAL);hint.setSingleLine(true);hint.setPadding(0,0,0,0);searchBox.addView(hint,new LinearLayout.LayoutParams(0,dp(38),1));
  TextView si=t("⌕",22);si.setTextColor(Color.WHITE);si.setGravity(Gravity.CENTER);si.setPadding(0,0,0,0);searchBox.addView(si,new LinearLayout.LayoutParams(dp(34),dp(38)));
  searchBox.setOnClickListener(v->searchDialog());top.addView(searchBox,new LinearLayout.LayoutParams(0,dp(38),1));
  topWrap.addView(top,new LinearLayout.LayoutParams(-1,dp(38)));

  HorizontalScrollView hs=new HorizontalScrollView(this);hs.setHorizontalScrollBarEnabled(false);hs.setOverScrollMode(View.OVER_SCROLL_NEVER);hs.setFillViewport(false);
  LinearLayout tabs=new LinearLayout(this);tabs.setOrientation(LinearLayout.HORIZONTAL);tabs.setGravity(Gravity.CENTER_VERTICAL);tabs.setPadding(0,0,0,0);

  // v16.73: topo mais limpo. Categorias reais continuam vindo do provedor,
  // mas não repetimos "Filmes"/"Séries" em praticamente todos os nomes.
  // Ex.: "Filmes Lançamentos" vira "Lançamentos" e "Filmes Guerra" vira "Guerra".
  addHomeTopTab(tabs,"Início","Recomendações",selected,null);
  JSONObject prepared=readHomeCache();JSONArray secs=prepared==null?null:prepared.optJSONArray("result");java.util.ArrayList<JSONObject> extras=new java.util.ArrayList<>();java.util.HashSet<String> extraLabels=new java.util.HashSet<>();
  if(secs!=null){for(int i=0;i<secs.length()&&extras.size()<3;i++){JSONObject sec=secs.optJSONObject(i);if(!validTopSection(sec))continue;String cleaned=cleanTopLabel(fixTitle(sec.optString("title","Categoria")));String norm=cleaned.toLowerCase(java.util.Locale.ROOT);if(cleaned.isEmpty()||norm.equals("filmes")||norm.equals("séries")||norm.equals("series")||extraLabels.contains(norm))continue;extraLabels.add(norm);extras.add(sec);}}
  if(extras.size()>0){JSONObject sec=extras.get(0);addHomeTopTab(tabs,shortTopLabel(cleanTopLabel(fixTitle(sec.optString("title","Categoria")))),topSectionKey(sec),selected,sec);}
  addHomeTopTab(tabs,"Séries","Séries",selected,null);
  addHomeTopTab(tabs,"Filmes","Filmes",selected,null);
  for(int i=1;i<extras.size();i++){JSONObject sec=extras.get(i);addHomeTopTab(tabs,shortTopLabel(cleanTopLabel(fixTitle(sec.optString("title","Categoria")))),topSectionKey(sec),selected,sec);}

  hs.addView(tabs,new HorizontalScrollView.LayoutParams(-2,dp(38)));LinearLayout.LayoutParams hp=new LinearLayout.LayoutParams(-1,dp(38));hp.setMargins(0,dp(12),0,dp(5));topWrap.addView(hs,hp);
  body.addView(topWrap,new LinearLayout.LayoutParams(-1,-2));
 }
 boolean validTopSection(JSONObject sec){
  if(sec==null||"recently_added".equals(sec.optString("section_key","")))return false;JSONArray data=sec.optJSONArray("data");if(data==null||data.length()==0)return false;String title=fixTitle(sec.optString("title",""));if(title.isEmpty())return false;String low=title.toLowerCase(java.util.Locale.ROOT);return !(low.equals("filmes")||low.equals("séries")||low.equals("series")||low.contains("adicionados recentemente")||low.equals("recentes"));
 }
 String cleanTopLabel(String s){
  if(s==null)return "";s=s.trim();if(s.isEmpty())return "";
  // Remove prefixos genéricos que já são representados pelas abas fixas Filmes/Séries.
  String out=s.replaceFirst("(?i)^\\s*(filmes?|movies?|s[eé]ries?|series)\\s*[-:|/•·–—]*\\s*","").trim();
  // Alguns painéis repetem o tipo duas vezes: "Filmes - Filmes Guerra".
  out=out.replaceFirst("(?i)^\\s*(filmes?|movies?|s[eé]ries?|series)\\s*[-:|/•·–—]*\\s*","").trim();
  if(out.isEmpty())out=s;
  return out;
 }
 String shortTopLabel(String s){if(s==null)return "Categoria";s=s.trim();return s.length()>12?s.substring(0,11)+"…":s;}
 String topSectionKey(JSONObject sec){return "sec:"+sec.optInt("type_id",sec.optInt("video_type",1))+":"+sec.optInt("category_id",0)+":"+fixTitle(sec.optString("title","")).toLowerCase(java.util.Locale.ROOT);}
 void addHomeTopTab(LinearLayout tabs,String label,String action,String selected,JSONObject section){
  boolean active=action.equals(selected);TextView tv=t(label,13);tv.setSingleLine(true);tv.setGravity(Gravity.CENTER_VERTICAL);tv.setPadding(0,0,0,0);tv.setTextColor(active?GREEN:0xffb7bab8);tv.setTypeface(null,active?1:0);
  LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-2,dp(38));lp.setMargins(0,0,dp(18),0);tabs.addView(tv,lp);
  if(section!=null){tv.setOnClickListener(v->homeSectionTab(action,section));return;}tv.setOnClickListener(v->homeTab(action));
 }

 void featureCarousel(JSONArray a){
  final HorizontalScrollView hs=new HorizontalScrollView(this);hs.setHorizontalScrollBarEnabled(false);hs.setOverScrollMode(View.OVER_SCROLL_NEVER);hs.setClipToPadding(false);hs.setFillViewport(false);
  final LinearLayout rail=new LinearLayout(this);rail.setOrientation(LinearLayout.HORIZONTAL);final int n=Math.min(12,a.length());if(n<=0)return;
  final int contentW=Math.max(dp(300),getResources().getDisplayMetrics().widthPixels-dp(36));final int cardW=Math.min(dp(250),(int)(contentW*.68f));final int cardH=(int)(cardW*1.27f);final int gap=dp(12);final int step=cardW+gap;final int side=Math.max(dp(18),(contentW-cardW)/2);rail.setPadding(side,dp(4),side,0);hs.addView(rail,new HorizontalScrollView.LayoutParams(-2,-1));
  if(n==1){JSONObject only=a.optJSONObject(0);FrameLayout card=featureCard(only);rail.addView(card,new LinearLayout.LayoutParams(cardW,cardH));body.addView(hs,new LinearLayout.LayoutParams(-1,cardH+dp(8)));final LinearLayout oneDot=new LinearLayout(this);oneDot.setGravity(Gravity.CENTER);body.addView(oneDot,new LinearLayout.LayoutParams(-1,dp(30)));updateDots(oneDot,1,0);hs.post(()->hs.scrollTo(0,0));return;}
  // Trilho circular: clone do último antes do primeiro e clone do primeiro depois do último.
  // Assim sempre existe um card vizinho dos dois lados, inclusive nas bordas do carrossel.
  JSONObject last=a.optJSONObject(n-1);FrameLayout firstClone=featureCard(last);LinearLayout.LayoutParams cloneLp=new LinearLayout.LayoutParams(cardW,cardH);cloneLp.setMargins(0,0,gap,0);rail.addView(firstClone,cloneLp);
  for(int i=0;i<n;i++){JSONObject x=a.optJSONObject(i);FrameLayout card=featureCard(x);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(cardW,cardH);lp.setMargins(0,0,gap,0);rail.addView(card,lp);}
  JSONObject first=a.optJSONObject(0);FrameLayout lastClone=featureCard(first);LinearLayout.LayoutParams endLp=new LinearLayout.LayoutParams(cardW,cardH);rail.addView(lastClone,endLp);
  body.addView(hs,new LinearLayout.LayoutParams(-1,cardH+dp(8)));
  final LinearLayout dotBar=new LinearLayout(this);dotBar.setGravity(Gravity.CENTER);body.addView(dotBar,new LinearLayout.LayoutParams(-1,dp(30)));
  final int[] physical={1};final boolean[] touching={false};final boolean[] normalizing={false};final Handler autoHandler=new Handler(Looper.getMainLooper());final int carouselGen=viewGen;
  updateDots(dotBar,n,0);hs.post(()->hs.scrollTo(step,0));
  final Runnable[] normalize=new Runnable[1];normalize[0]=()->{if(carouselGen!=viewGen||hs.getWindowToken()==null)return;int p=physical[0];if(p==0){normalizing[0]=true;physical[0]=n;hs.scrollTo(n*step,0);normalizing[0]=false;}else if(p==n+1){normalizing[0]=true;physical[0]=1;hs.scrollTo(step,0);normalizing[0]=false;}};
  final Runnable[] auto=new Runnable[1];auto[0]=new Runnable(){public void run(){
   if(detailOpen){autoHandler.postDelayed(this,900);return;}if(carouselGen!=viewGen||hs.getWindowToken()==null)return;if(touching[0]||normalizing[0]||!hs.isShown()){autoHandler.postDelayed(this,1200);return;}
   int next=physical[0]+1;if(next>n+1)next=1;physical[0]=next;int logical=(next==n+1)?0:Math.max(0,next-1);hs.smoothScrollTo(next*step,0);updateDots(dotBar,n,logical);if(next==n+1)autoHandler.postDelayed(normalize[0],520);autoHandler.postDelayed(this,4800);
  }};
  hs.setOnTouchListener((v,e)->{int action=e.getActionMasked();if(action==MotionEvent.ACTION_DOWN){touching[0]=true;autoHandler.removeCallbacks(auto[0]);autoHandler.removeCallbacks(normalize[0]);}else if(action==MotionEvent.ACTION_UP||action==MotionEvent.ACTION_CANCEL){int p=Math.round(hs.getScrollX()/(float)step);p=Math.max(0,Math.min(n+1,p));physical[0]=p;int logical=p==0?n-1:(p==n+1?0:p-1);hs.smoothScrollTo(p*step,0);updateDots(dotBar,n,logical);if(p==0||p==n+1)autoHandler.postDelayed(normalize[0],520);touching[0]=false;autoHandler.removeCallbacks(auto[0]);autoHandler.postDelayed(auto[0],6200);}return false;});
  autoHandler.postDelayed(auto[0],4800);
 }
 JSONArray buildFeaturedMix(JSONArray sections,int max){
  JSONArray out=new JSONArray();if(sections==null||max<=0)return out;
  java.util.ArrayList<JSONObject> movies=new java.util.ArrayList<>(),series=new java.util.ArrayList<>(),other=new java.util.ArrayList<>();java.util.HashSet<String> seen=new java.util.HashSet<>();
  for(int i=0;i<sections.length();i++){JSONObject sec=sections.optJSONObject(i);if(sec==null)continue;int type=sec.optInt("type_id",sec.optInt("video_type",1));JSONArray d=sec.optJSONArray("data");if(d==null)continue;for(int j=0;j<d.length();j++){JSONObject x=d.optJSONObject(j);if(x==null)continue;String k=itemKey(x);if(!seen.add(k))continue;if(type==2)series.add(x);else if(type==1)movies.add(x);else other.add(x);}}
  long seed=System.nanoTime()^((long)(++featuredShuffleTick)*2654435761L);java.util.Random rnd=new java.util.Random(seed);java.util.Collections.shuffle(movies,rnd);java.util.Collections.shuffle(series,rnd);java.util.Collections.shuffle(other,rnd);
  int mi=0,si=0,oi=0;boolean preferSeries=(featuredShuffleTick%2)==0;
  while(out.length()<max&&(mi<movies.size()||si<series.size()||oi<other.size())){
   if(preferSeries&&si<series.size())out.put(series.get(si++));else if(!preferSeries&&mi<movies.size())out.put(movies.get(mi++));
   if(out.length()>=max)break;
   if(preferSeries&&mi<movies.size())out.put(movies.get(mi++));else if(!preferSeries&&si<series.size())out.put(series.get(si++));
   if(out.length()>=max)break;
   if(oi<other.size())out.put(other.get(oi++));
   preferSeries=!preferSeries;
   if(mi>=movies.size()&&si>=series.size()&&oi<other.size())while(out.length()<max&&oi<other.size())out.put(other.get(oi++));
   if(si>=series.size()&&mi<movies.size()&&out.length()<max)out.put(movies.get(mi++));
   if(mi>=movies.size()&&si<series.size()&&out.length()<max)out.put(series.get(si++));
  }
  return out;
 }
 void addFeaturedUnique(JSONArray out,JSONObject x,java.util.HashSet<String> seen,int max){if(x==null||out.length()>=max)return;String key=itemKey(x);if(seen.add(key))out.put(x);}
 String itemKey(JSONObject x){return x.optString("id","")+"|"+x.optString("name",x.optString("title","")).trim().toLowerCase(java.util.Locale.ROOT);}
 JSONObject firstItemFromType(JSONArray sections,int typeId){for(int i=0;i<sections.length();i++){JSONObject sec=sections.optJSONObject(i);if(sec==null||sec.optInt("type_id",sec.optInt("video_type",1))!=typeId)continue;JSONArray d=sec.optJSONArray("data");if(d!=null&&d.length()>0)return d.optJSONObject(0);}return null;}
 JSONObject firstItemFromSectionKind(JSONArray sections,int typeId,boolean launch){for(int i=0;i<sections.length();i++){JSONObject sec=sections.optJSONObject(i);if(sec==null||sec.optInt("type_id",sec.optInt("video_type",1))!=typeId)continue;String title=sec.optString("title","").toLowerCase(java.util.Locale.ROOT);boolean isLaunch=title.contains("lanç")||title.contains("lanc")||title.contains("estreia")||title.contains("novidade");if(isLaunch!=launch)continue;JSONArray d=sec.optJSONArray("data");if(d!=null&&d.length()>0)return d.optJSONObject(0);}return null;}
 JSONArray buildRecentlyAddedMovies(JSONArray sections,int max){
  JSONArray out=new JSONArray();if(sections==null||max<=0)return out;
  // O painel v68 envia uma seção dedicada, calculada por first_seen_at por provedor.
  // Assim "recentemente adicionado" significa que o item apareceu agora na fonte,
  // e não que tem ID alto ou ano de lançamento recente.
  for(int i=0;i<sections.length();i++){JSONObject sec=sections.optJSONObject(i);if(sec==null)continue;if(!"recently_added".equals(sec.optString("section_key","")))continue;JSONArray d=sec.optJSONArray("data");if(d==null)break;for(int j=0;j<Math.min(max,d.length());j++){JSONObject x=d.optJSONObject(j);if(x!=null)out.put(x);}return out;}
  java.util.ArrayList<JSONObject> list=new java.util.ArrayList<>();java.util.HashSet<String> seen=new java.util.HashSet<>();
  for(int i=0;i<sections.length();i++){JSONObject sec=sections.optJSONObject(i);if(sec==null||sec.optInt("type_id",sec.optInt("video_type",1))!=1)continue;JSONArray d=sec.optJSONArray("data");if(d==null)continue;for(int j=0;j<d.length();j++){JSONObject x=d.optJSONObject(j);if(x==null||recentScore(x)<=0)continue;String key=itemKey(x);if(seen.add(key))list.add(x);}}
  java.util.Collections.sort(list,(a,b)->Long.compare(recentScore(b),recentScore(a)));
  for(int i=0;i<Math.min(max,list.size());i++)out.put(list.get(i));return out;
 }
 long recentScore(JSONObject x){
  String[] fields={"first_seen_at","source_added_at","added"};for(String f:fields){String v=x.optString(f,"").trim();if(v.matches("\\d{9,13}")){try{long n=Long.parseLong(v);return n>20000000000L?n/1000L:n;}catch(Exception ignored){}}}
  return 0L;
 }
 FrameLayout featureCard(JSONObject x){
  FrameLayout f=new FrameLayout(this);GradientDrawable outline=round(0xff1a211e,24);outline.setStroke(dp(1),0xff2a332f);f.setBackground(outline);f.setClipToOutline(true);f.setElevation(dp(2));
  ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);Img.load(im,x.optString("thumbnail",x.optString("landscape")));f.addView(im,new FrameLayout.LayoutParams(-1,-1));
  GradientDrawable shade=new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM,new int[]{0x00000000,0x12000000,0xe0000000});View v=new View(this);v.setBackground(shade);f.addView(v,new FrameLayout.LayoutParams(-1,-1));
  String rating=x.optString("rating",x.optString("imdb_rating",x.optString("score",""))).trim();boolean hasRating=!rating.isEmpty()&&!rating.equals("0")&&!rating.equals("0.0");TextView r=t(hasRating?"★  "+formatRatingDisplay(rating):"★  —",13);r.setTypeface(null,1);r.setTextColor(hasRating?Color.WHITE:0xff9da7a2);r.setGravity(Gravity.CENTER);GradientDrawable rg=round(0xc7111714,11);rg.setStroke(dp(1),hasRating?GREEN:0xff46504b);r.setBackground(rg);FrameLayout.LayoutParams rp=new FrameLayout.LayoutParams(dp(82),dp(34),Gravity.LEFT|Gravity.BOTTOM);rp.setMargins(dp(14),0,0,dp(58));f.addView(r,rp);
  TextView name=t(x.optString("name",x.optString("title","")),17);name.setTypeface(null,1);name.setMaxLines(2);name.setEllipsize(android.text.TextUtils.TruncateAt.END);name.setGravity(Gravity.LEFT|Gravity.BOTTOM);name.setPadding(0,0,0,0);FrameLayout.LayoutParams np=new FrameLayout.LayoutParams(-1,dp(62),Gravity.BOTTOM);np.setMargins(dp(14),0,dp(12),dp(6));f.addView(name,np);f.setOnClickListener(z->details(x));f.setOnLongClickListener(z->{toggleFav(x);return true;});return f;
 }
 void updateDots(LinearLayout d,int n,int active){
  if(d.getChildCount()!=n){d.removeAllViews();for(int i=0;i<n;i++){View x=new View(this);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(dp(8),dp(7));lp.setMargins(dp(4),dp(2),dp(4),dp(5));d.addView(x,lp);}}
  for(int i=0;i<n;i++){View x=d.getChildAt(i);if(x==null)continue;x.setBackground(round(i==active?GREEN:0xff4b5350,6));LinearLayout.LayoutParams lp=(LinearLayout.LayoutParams)x.getLayoutParams();int wanted=i==active?dp(22):dp(8);if(lp.width!=wanted){lp.width=wanted;x.setLayoutParams(lp);}}
 }
 void promoLive(){
  if(!sessionHasLive)return;
  LinearLayout promo=new LinearLayout(this);promo.setGravity(Gravity.CENTER_VERTICAL);promo.setPadding(dp(14),dp(7),dp(12),dp(7));GradientDrawable g=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{0xff123526,0xff167546});g.setCornerRadius(dp(18));promo.setBackground(g);
  TextView icon=t("▶",19);icon.setTextColor(GREEN);icon.setGravity(Gravity.CENTER);icon.setBackground(round(0x33000000,14));promo.addView(icon,new LinearLayout.LayoutParams(dp(48),dp(48)));
  LinearLayout text=new LinearLayout(this);text.setOrientation(LinearLayout.VERTICAL);text.setPadding(dp(10),0,0,0);TextView tt=t("Canais ao vivo",16);tt.setTypeface(null,1);tt.setPadding(0,0,0,0);TextView ss=t("TV em tempo real",12);ss.setTextColor(0xffd0d8d4);ss.setPadding(0,0,0,0);text.addView(tt);text.addView(ss);promo.addView(text,new LinearLayout.LayoutParams(0,-2,1));TextView ar=t("›",28);ar.setGravity(Gravity.CENTER);promo.addView(ar,new LinearLayout.LayoutParams(dp(38),dp(48)));promo.setOnClickListener(v->liveContent());LinearLayout.LayoutParams pp=new LinearLayout.LayoutParams(-1,dp(70));pp.setMargins(dp(2),dp(6),dp(2),dp(12));body.addView(promo,pp);
 }
 void sectionHeader(String title,Runnable more){sectionHeaderInto(body,title,more);}
 void sectionHeaderInto(LinearLayout host,String title,Runnable more){LinearLayout h=new LinearLayout(this);h.setGravity(Gravity.CENTER_VERTICAL);h.setPadding(dp(2),dp(6),0,dp(1));TextView t1=t(title,18);t1.setTypeface(null,1);h.addView(t1,new LinearLayout.LayoutParams(0,dp(44),1));TextView ar=t("›",27);ar.setTextColor(GREEN);ar.setGravity(Gravity.CENTER);ar.setOnClickListener(v->more.run());h.addView(ar,new LinearLayout.LayoutParams(dp(38),dp(44)));host.addView(h);}
 void posterRow(JSONArray a){posterRowInto(body,a);}
 void posterRowInto(LinearLayout host,JSONArray a){HorizontalScrollView hs=new HorizontalScrollView(this);hs.setHorizontalScrollBarEnabled(false);LinearLayout r=new LinearLayout(this);r.setOrientation(LinearLayout.HORIZONTAL);if(a!=null)for(int i=0;i<Math.min(12,a.length());i++){JSONObject x=a.optJSONObject(i);LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setBackground(round(CARD,15));im.setClipToOutline(true);Img.loadVisible(im,x.optString("thumbnail",x.optString("portrait_img",x.optString("image",""))));c.addView(im,new LinearLayout.LayoutParams(-1,dp(150)));TextView n=t(x.optString("name",""),12);n.setMaxLines(2);n.setEllipsize(android.text.TextUtils.TruncateAt.END);n.setPadding(dp(3),dp(5),dp(3),0);c.addView(n,new LinearLayout.LayoutParams(-1,dp(40)));c.setOnClickListener(v->details(x));LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(dp(104),dp(194));cp.setMargins(dp(3),0,dp(8),0);r.addView(c,cp);}hs.addView(r);host.addView(hs,new LinearLayout.LayoutParams(-1,dp(198)));}
 void loadContinueWatching(){Api.post("get_continue_watching",Api.m("user_id",uid),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");if(a==null||a.length()==0||continueHost==null)return;continueHost.removeAllViews();LinearLayout h=new LinearLayout(MainActivity.this);h.setGravity(Gravity.CENTER_VERTICAL);TextView ttl=t("Continue assistindo",18);ttl.setTypeface(null,1);h.addView(ttl,new LinearLayout.LayoutParams(0,dp(44),1));TextView ar=t("›",27);ar.setTextColor(GREEN);ar.setGravity(Gravity.CENTER);h.addView(ar,new LinearLayout.LayoutParams(dp(38),dp(44)));continueHost.addView(h);continueLandscapeRow(continueHost,a);}public void err(String x){}});}
 void continueLandscapeRow(LinearLayout host,JSONArray a){HorizontalScrollView hs=new HorizontalScrollView(this);hs.setHorizontalScrollBarEnabled(false);LinearLayout r=new LinearLayout(this);r.setOrientation(LinearLayout.HORIZONTAL);for(int i=0;i<Math.min(8,a.length());i++){JSONObject x=a.optJSONObject(i);LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setBackground(round(CARD,14));im.setClipToOutline(true);Img.loadVisible(im,x.optString("landscape",x.optString("thumbnail",x.optString("landscape_img",""))));c.addView(im,new LinearLayout.LayoutParams(-1,dp(92)));TextView n=t(x.optString("name",x.optString("title","")),12);n.setMaxLines(1);n.setEllipsize(android.text.TextUtils.TruncateAt.END);n.setPadding(dp(2),dp(4),dp(2),0);c.addView(n,new LinearLayout.LayoutParams(-1,dp(30)));c.setOnClickListener(v->details(x));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(dp(158),dp(126));lp.setMargins(dp(3),0,dp(9),0);r.addView(c,lp);}hs.addView(r);host.addView(hs,new LinearLayout.LayoutParams(-1,dp(132)));}
 void landscapeRow(JSONArray a){HorizontalScrollView hs=new HorizontalScrollView(this);hs.setHorizontalScrollBarEnabled(false);LinearLayout r=new LinearLayout(this);r.setOrientation(LinearLayout.HORIZONTAL);for(int i=0;i<Math.min(8,a.length());i++){JSONObject x=a.optJSONObject(i);LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setBackground(round(CARD,14));im.setClipToOutline(true);Img.loadVisible(im,x.optString("landscape",x.optString("thumbnail",x.optString("landscape_img",""))));c.addView(im,new LinearLayout.LayoutParams(-1,dp(92)));TextView n=t(x.optString("name",x.optString("title","")),12);n.setMaxLines(1);n.setEllipsize(android.text.TextUtils.TruncateAt.END);n.setPadding(dp(2),dp(4),dp(2),0);c.addView(n,new LinearLayout.LayoutParams(-1,dp(30)));c.setOnClickListener(v->details(x));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(dp(158),dp(126));lp.setMargins(dp(3),0,dp(9),0);r.addView(c,lp);}hs.addView(r);body.addView(hs,new LinearLayout.LayoutParams(-1,dp(132)));}
 void liveContent(){
  if(!sessionHasLive){home();return;}
  clear();setNav(2);pageTitle("TV ao vivo",()->home());
  LinearLayout searchRow=new LinearLayout(this);searchRow.setGravity(Gravity.CENTER_VERTICAL);liveSearchBox=e("Buscar canal",false);TextView go=t("⌕",24);go.setGravity(Gravity.CENTER);go.setTextColor(GREEN);go.setBackground(round(0xff15261f,16));searchRow.addView(liveSearchBox,new LinearLayout.LayoutParams(0,dp(52),1));LinearLayout.LayoutParams gp=new LinearLayout.LayoutParams(dp(52),dp(52));gp.setMargins(dp(8),0,0,0);searchRow.addView(go,gp);body.addView(searchRow,new LinearLayout.LayoutParams(-1,dp(58)));
  LinearLayout tabs=new LinearLayout(this);tabs.setGravity(Gravity.CENTER_VERTICAL);TextView canais=t("Canais",15);TextView fav=t("Favoritos",15);canais.setGravity(Gravity.CENTER);fav.setGravity(Gravity.CENTER);canais.setTypeface(null,1);canais.setTextColor(GREEN);fav.setTextColor(0xffa8b0ac);tabs.addView(canais,new LinearLayout.LayoutParams(0,dp(44),1));tabs.addView(fav,new LinearLayout.LayoutParams(0,dp(44),1));body.addView(tabs,new LinearLayout.LayoutParams(-1,dp(46)));
  LinearLayout panes=new LinearLayout(this);panes.setOrientation(LinearLayout.HORIZONTAL);panes.setPadding(0,dp(4),0,0);
  ScrollView catScroll=new ScrollView(this);catScroll.setVerticalScrollBarEnabled(false);tvCategoryHost=new LinearLayout(this);tvCategoryHost.setOrientation(LinearLayout.VERTICAL);catScroll.addView(tvCategoryHost);panes.addView(catScroll,new LinearLayout.LayoutParams(dp(128),dp(520)));
  Space sep=new Space(this);panes.addView(sep,new LinearLayout.LayoutParams(dp(8),1));
  ScrollView chanScroll=new ScrollView(this);chanScroll.setVerticalScrollBarEnabled(false);tvChannelHost=new LinearLayout(this);tvChannelHost.setOrientation(LinearLayout.VERTICAL);chanScroll.addView(tvChannelHost);panes.addView(chanScroll,new LinearLayout.LayoutParams(0,dp(520),1));body.addView(panes,new LinearLayout.LayoutParams(-1,dp(524)));
  canais.setOnClickListener(v->{canais.setTextColor(GREEN);canais.setTypeface(null,1);fav.setTextColor(0xffa8b0ac);fav.setTypeface(null,0);tvLoadChannels(tvSelectedCategory,"",false);});
  fav.setOnClickListener(v->{fav.setTextColor(GREEN);fav.setTypeface(null,1);canais.setTextColor(0xffa8b0ac);canais.setTypeface(null,0);tvLoadChannels("","",true);});
  View.OnClickListener doSearch=v->{String q=liveSearchBox.getText().toString().trim();tvLoadChannels("",q,false);};go.setOnClickListener(doSearch);liveSearchBox.setOnEditorActionListener((v,a,event)->{doSearch.onClick(v);return true;});
  tvLoadCategories();
 }
 void tvLoadCategories(){
  if(tvCategoryHost==null)return;tvCategoryHost.removeAllViews();JSONObject prepared=readHomeCache();JSONArray mem=prepared==null?null:prepared.optJSONArray("live_categories");
  if(mem!=null&&mem.length()>0){renderTvCategoriesFromMemory(mem);return;}
  TextView wait=t("Carregando…",13);wait.setTextColor(0xff8f9994);tvCategoryHost.addView(wait);
  Api.post("get_category",Api.m("type","live","user_id",uid),new Api.CB(){public void ok(JSONObject j){if(tvCategoryHost==null)return;JSONArray a=j.optJSONArray("result");if(a==null||a.length()==0){tvCategoryHost.removeAllViews();TextView m=t("Sem categorias",13);m.setTextColor(0xffff7777);tvCategoryHost.addView(m);tvLoadChannels("","",false);return;}renderTvCategoriesFromMemory(a);}public void err(String x){if(tvCategoryHost!=null){tvCategoryHost.removeAllViews();TextView m=t("Falha ao carregar categorias",13);m.setTextColor(0xffff7777);tvCategoryHost.addView(m);}tvLoadChannels("","",false);}});
 }
 void renderTvCategoriesFromMemory(JSONArray a){
  if(tvCategoryHost==null)return;tvCategoryHost.removeAllViews();for(int i=0;i<a.length();i++){JSONObject c=a.optJSONObject(i);if(c==null)continue;String id=c.optString("category_id",c.optString("id",""));String name=fixTitle(c.optString("category_name",c.optString("name","Canais")));TextView item=t(name,13);item.setMaxLines(2);item.setGravity(Gravity.CENTER_VERTICAL);item.setPadding(dp(10),dp(8),dp(8),dp(8));GradientDrawable g=round(i==0?0xff123225:0xff121a16,12);if(i==0)g.setStroke(dp(1),GREEN);item.setBackground(g);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(58));lp.setMargins(0,0,0,dp(6));tvCategoryHost.addView(item,lp);final int pos=i;item.setOnClickListener(v->{for(int k=0;k<tvCategoryHost.getChildCount();k++){View z=tvCategoryHost.getChildAt(k);GradientDrawable gg=round(k==pos?0xff123225:0xff121a16,12);if(k==pos)gg.setStroke(dp(1),GREEN);z.setBackground(gg);}tvSelectedCategory=id;tvLoadChannels(id,"",false);});if(i==0)tvSelectedCategory=id;}tvLoadChannels(tvSelectedCategory,"",false);
 }
 JSONArray filterLiveSnapshot(String categoryId,String search){JSONArray out=new JSONArray();JSONObject prepared=readHomeCache();JSONArray all=prepared==null?null:prepared.optJSONArray("live_channels");if(all==null)return out;String needle=search==null?"":search.trim().toLowerCase(java.util.Locale.ROOT);for(int i=0;i<all.length();i++){JSONObject x=all.optJSONObject(i);if(x==null)continue;if(categoryId!=null&&!categoryId.isEmpty()&&!categoryId.equals(x.optString("category_id","")))continue;String name=x.optString("name","").toLowerCase(java.util.Locale.ROOT);if(!needle.isEmpty()&&!name.contains(needle))continue;out.put(x);}return out;}
 void tvLoadChannels(String categoryId,String search,boolean favoritesOnly){
  if(tvChannelHost==null)return;tvChannelHost.removeAllViews();
  if(favoritesOnly){JSONArray a=liveFavArray();if(a.length()==0){TextView m=t("Nenhum canal favorito",14);m.setTextColor(0xff9aa39f);tvChannelHost.addView(m);return;}renderTvChannelsChunk(tvChannelHost,a,0);return;}
  JSONObject prepared=readHomeCache();if(prepared!=null&&prepared.optInt("catalog_complete",0)==1&&prepared.optJSONArray("live_channels")!=null){JSONArray a=filterLiveSnapshot(categoryId,search);if(a.length()==0){TextView m=t(search.isEmpty()?"Nenhum canal nesta categoria.":"Nenhum canal encontrado.",14);m.setTextColor(0xff9aa39f);tvChannelHost.addView(m);return;}renderTvChannelsChunk(tvChannelHost,a,0);return;}
  TextView wait=t("Carregando canais…",13);wait.setTextColor(0xff8f9994);tvChannelHost.addView(wait);
  Api.post("get_channel",Api.m("user_id",uid,"category_id",categoryId,"limit","100","offset","0","search",search),new Api.CB(){public void ok(JSONObject j){if(tvChannelHost==null)return;tvChannelHost.removeAllViews();JSONArray a=j.optJSONArray("result");if(j.optInt("status",200)!=200||a==null||a.length()==0){TextView m=t(search.isEmpty()?"Nenhum canal nesta categoria.":"Nenhum canal encontrado.",14);m.setTextColor(0xff9aa39f);tvChannelHost.addView(m);return;}renderTvChannelsChunk(tvChannelHost,a,0);}public void err(String x){if(tvChannelHost!=null){tvChannelHost.removeAllViews();TextView m=t("Não foi possível carregar os canais.",14);m.setTextColor(0xffff7777);tvChannelHost.addView(m);}}});
 }
 void renderTvChannelsChunk(LinearLayout host,JSONArray a,int start){
  if(host==null||host!=tvChannelHost||host.getParent()==null)return;int end=Math.min(a.length(),start+12);for(int i=start;i<end;i++){JSONObject x=a.optJSONObject(i);if(x!=null)host.addView(tvChannelCard(x));}if(end<a.length())host.postDelayed(()->renderTvChannelsChunk(host,a,end),16);
 }
 View tvChannelCard(JSONObject x){
  LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER_VERTICAL);card.setPadding(dp(8),dp(7),dp(6),dp(7));card.setBackground(round(0xff141c18,14));ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);logo.setBackground(round(0xff0d2419,12));Img.load(logo,x.optString("thumbnail"));card.addView(logo,new LinearLayout.LayoutParams(dp(54),dp(54)));TextView name=t(x.optString("name","Canal"),13);name.setMaxLines(2);name.setEllipsize(android.text.TextUtils.TruncateAt.END);name.setPadding(dp(9),0,dp(4),0);card.addView(name,new LinearLayout.LayoutParams(0,dp(58),1));TextView heart=t(isLiveFav(x)?"♥":"♡",22);heart.setGravity(Gravity.CENTER);heart.setTextColor(isLiveFav(x)?GREEN:0xffa0aaa5);card.addView(heart,new LinearLayout.LayoutParams(dp(38),dp(58)));heart.setOnClickListener(v->{toggleLiveFav(x);heart.setText(isLiveFav(x)?"♥":"♡");heart.setTextColor(isLiveFav(x)?GREEN:0xffa0aaa5);});card.setOnClickListener(v->openLive(x));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(72));lp.setMargins(0,0,0,dp(7));card.setLayoutParams(lp);return card;
 }
 JSONArray liveFavArray(){try{return new JSONArray(sp.getString("live_favs","[]"));}catch(Exception e){return new JSONArray();}}
 boolean isLiveFav(JSONObject x){JSONArray a=liveFavArray();String id=x.optString("id",x.optString("channel_id",""));for(int i=0;i<a.length();i++){JSONObject y=a.optJSONObject(i);if(y!=null&&id.equals(y.optString("id",y.optString("channel_id",""))))return true;}return false;}
 void toggleLiveFav(JSONObject x){try{JSONArray a=liveFavArray();String id=x.optString("id",x.optString("channel_id",""));for(int i=0;i<a.length();i++){JSONObject y=a.optJSONObject(i);if(y!=null&&id.equals(y.optString("id",y.optString("channel_id","")))){a.remove(i);sp.edit().putString("live_favs",a.toString()).apply();return;}}a.put(new JSONObject(x.toString()));sp.edit().putString("live_favs",a.toString()).apply();}catch(Exception ignored){}}
 void openLive(JSONObject x){String u=x.optString("video_1080",x.optString("video_720",x.optString("video_480",x.optString("video_320",""))));if(u.isEmpty()){Toast.makeText(this,"Canal indisponível",0).show();return;}Intent in=new Intent(this,PlayerActivity.class);in.putExtra("url",u);in.putExtra("url_1080",x.optString("video_1080",""));in.putExtra("url_720",x.optString("video_720",""));in.putExtra("url_480",x.optString("video_480",""));in.putExtra("url_320",x.optString("video_320",""));in.putExtra("title",x.optString("name","Canal"));in.putExtra("live",true);startActivity(in);}
 void pageTitle(String title,Runnable back){LinearLayout h=new LinearLayout(this);h.setGravity(Gravity.CENTER_VERTICAL);TextView b=t("‹",30);b.setTextColor(GREEN);b.setGravity(Gravity.CENTER);b.setOnClickListener(v->back.run());h.addView(b,new LinearLayout.LayoutParams(dp(48),dp(52)));TextView tt=t(title,24);tt.setTypeface(null,1);h.addView(tt,new LinearLayout.LayoutParams(0,dp(52),1));body.addView(h);}
 String fixTitle(String s){if(s==null)return "";return s.replace("Action & Adventure","Ação e Aventura").replace("Sci-Fi & Fantasy","Ficção Científica e Fantasia").replace("Science Fiction & Fantasy","Ficção Científica e Fantasia").replace("Family","Família").replace("Animation","Animação").replace("Crime","Crime").replace("Mystery","Mistério").replace("Comedy","Comédia").replace("Documentary","Documentário").replace("Acao","Ação").replace("acao","ação").replace("Animacao","Animação").replace("animacao","animação").replace("Series","Séries").replace("series","séries");}
  void row(JSONArray a){HorizontalScrollView hs=new HorizontalScrollView(this);hs.setHorizontalScrollBarEnabled(false);LinearLayout r=new LinearLayout(this);r.setOrientation(LinearLayout.HORIZONTAL);r.setPadding(dp(2),0,dp(8),0);hs.addView(r);if(a!=null)for(int i=0;i<Math.min(16,a.length());i++){JSONObject x=a.optJSONObject(i);LinearLayout c=card(x);LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(dp(112),dp(202));cp.setMargins(dp(3),0,dp(8),0);r.addView(c,cp);}body.addView(hs,new LinearLayout.LayoutParams(-1,dp(204)));}
 LinearLayout card(JSONObject x){LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setPadding(dp(2),dp(2),dp(2),0);c.setFocusable(true);FrameLayout poster=new FrameLayout(this);poster.setBackground(round(CARD,13));ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);Img.loadVisible(im,x.optString("thumbnail",x.optString("portrait_img",x.optString("image",""))));poster.addView(im,new FrameLayout.LayoutParams(-1,-1));TextView badge=t("▶",10);badge.setTextColor(Color.WHITE);badge.setGravity(Gravity.CENTER);badge.setBackground(round(0xaa000000,20));FrameLayout.LayoutParams bp=new FrameLayout.LayoutParams(dp(28),dp(28),Gravity.BOTTOM|Gravity.RIGHT);bp.setMargins(0,0,dp(7),dp(7));poster.addView(badge,bp);c.addView(poster,new LinearLayout.LayoutParams(-1,dp(158)));TextView n=t(x.optString("name"),13);n.setPadding(dp(2),dp(6),dp(2),0);n.setMaxLines(2);n.setEllipsize(android.text.TextUtils.TruncateAt.END);c.addView(n,new LinearLayout.LayoutParams(-1,dp(42)));c.setOnClickListener(v->details(x));c.setOnLongClickListener(v->{toggleFav(x);return true;});return c;}

 void details(JSONObject x){
  if(detailOpen||detailPreparing||x==null)return;
  saveDetailCache(x,x);
  JSONObject cached=mergeDetailJson(x,readDetailCache(x));
  // v16.71: se o detalhe já foi preparado/prefetchado, abre instantaneamente.
  // Caso contrário, mantém a Home visível por um instante e só entra na tela
  // depois que detalhe + enriquecimento terminarem. Assim nenhum campo aparece
  // "chegando depois" diante do usuário.
  if(cached!=null&&!detailNeedsEnrich(cached)){openPreparedDetails(x,cached);return;}
  detailPreparing=true;showDetailPrepareOverlay();
  prepareDetailForOpen(x,new DetailPrepareCB(){public void done(JSONObject ready){runOnUiThread(()->{
   if(!detailPreparing)return;detailPreparing=false;hideDetailPrepareOverlay();
   JSONObject merged=mergeDetailJson(x,ready);openPreparedDetails(x,merged==null?x:merged);
  });}});
 }
 void showDetailPrepareOverlay(){
  if(contentFrame==null||detailPrepareOverlay!=null)return;
  FrameLayout ov=new FrameLayout(this);ov.setClickable(true);ov.setFocusable(true);ov.setBackgroundColor(0x7207110c);
  LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER);card.setBackground(round(0xf218211d,22));card.setElevation(dp(8));
  ProgressBar pb=new ProgressBar(this);try{pb.getIndeterminateDrawable().setColorFilter(GREEN,android.graphics.PorterDuff.Mode.SRC_IN);}catch(Exception ignored){}
  card.addView(pb,new LinearLayout.LayoutParams(dp(34),dp(34)));
  FrameLayout.LayoutParams cp=new FrameLayout.LayoutParams(dp(72),dp(72),Gravity.CENTER);ov.addView(card,cp);
  detailPrepareOverlay=ov;contentFrame.addView(ov,new FrameLayout.LayoutParams(-1,-1));
 }
 void hideDetailPrepareOverlay(){if(detailPrepareOverlay!=null){try{if(detailPrepareOverlay.getParent() instanceof ViewGroup)((ViewGroup)detailPrepareOverlay.getParent()).removeView(detailPrepareOverlay);}catch(Exception ignored){}detailPrepareOverlay=null;}}
 void prepareDetailForOpen(JSONObject source,DetailPrepareCB cb){
  saveDetailCache(source,source);JSONObject first=mergeDetailJson(source,readDetailCache(source));if(first!=null&&!detailNeedsEnrich(first)){cb.done(first);return;}
  final boolean[] detailDone={false},enrichDone={false},delivered={false};final Handler h=new Handler(Looper.getMainLooper());
  final Runnable[] deliver=new Runnable[1];deliver[0]=()->{if(delivered[0])return;delivered[0]=true;h.removeCallbacksAndMessages(null);JSONObject ready=mergeDetailJson(source,readDetailCache(source));cb.done(ready==null?source:ready);};
  final Runnable maybe=()->{if(delivered[0])return;JSONObject now=mergeDetailJson(source,readDetailCache(source));if(now!=null&&!detailNeedsEnrich(now)){deliver[0].run();return;}if(detailDone[0]&&enrichDone[0])deliver[0].run();};
  h.postDelayed(deliver[0],4800);
  int vt=source.optInt("video_type",source.optInt("type_id",1));String vid=source.optString("id",source.optString("video_id",""));
  Api.post("content_detail",Api.m("user_id",uid,"video_id",vid,"video_type",String.valueOf(vt)),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d!=null)saveDetailCache(source,d);detailDone[0]=true;maybe.run();}public void err(String e){detailDone[0]=true;maybe.run();}});
  Api.post("content_enrich",Api.m("user_id",uid,"video_id",vid,"video_type",String.valueOf(vt)),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d!=null)saveDetailCache(source,d);enrichDone[0]=true;maybe.run();}public void err(String e){enrichDone[0]=true;maybe.run();}});
 }
 void openPreparedDetails(JSONObject x,JSONObject prepared){
  if(detailOpen)return;
  detailOpen=true;savedViewGen=viewGen;viewGen++;
  if(root!=null)root.setPadding(0,0,0,0);
  savedScroll=mainScroll;savedBody=body;savedNavIndex=currentNavIndex;
  if(savedScroll!=null)savedScroll.setVisibility(View.GONE);
  if(navBar!=null)navBar.setVisibility(View.GONE);
  mainScroll=new ScrollView(this);mainScroll.setFillViewport(true);mainScroll.setClipToPadding(false);mainScroll.setVerticalScrollBarEnabled(false);
  body=new LinearLayout(this);body.setOrientation(LinearLayout.VERTICAL);body.setPadding(0,0,0,dp(28));mainScroll.setPadding(0,0,0,0);mainScroll.setClipToPadding(false);mainScroll.addView(body);
  if(contentFrame!=null)contentFrame.addView(mainScroll,new FrameLayout.LayoutParams(-1,-1));
  setNav(savedNavIndex);
  final String title=x.optString("name",x.optString("title",""));JSONObject ready=mergeDetailJson(x,prepared);if(ready==null)ready=x;saveDetailCache(x,ready);

  FrameLayout hero=new FrameLayout(this);hero.setBackgroundColor(BG);hero.setClipToPadding(false);
  ImageView p=new ImageView(this);p.setScaleType(ImageView.ScaleType.CENTER_CROP);String heroStart=detailValue(ready,"landscape","landscape_img","backdrop","backdrop_path","thumbnail","portrait_img");if(heroStart.isEmpty())heroStart=x.optString("landscape",x.optString("landscape_img",x.optString("thumbnail",x.optString("portrait_img",""))));Img.loadVisible(p,heroStart);hero.addView(p,new FrameLayout.LayoutParams(-1,-1));
  GradientDrawable topShade=new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM,new int[]{0x8f000000,0x20000000,0x00000000});View tsh=new View(this);tsh.setBackground(topShade);hero.addView(tsh,new FrameLayout.LayoutParams(-1,-1));
  GradientDrawable bottomShade=new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM,new int[]{0x00000000,0x18000000,0xaa070d0a,0xff07110c});View bsh=new View(this);bsh.setBackground(bottomShade);hero.addView(bsh,new FrameLayout.LayoutParams(-1,-1));
  TextView back=t("‹",34);back.setTextColor(Color.WHITE);back.setGravity(Gravity.CENTER);back.setBackground(detailGlassCircle());back.setOnClickListener(v->closeDetails());FrameLayout.LayoutParams blp=new FrameLayout.LayoutParams(dp(50),dp(50),Gravity.TOP|Gravity.LEFT);blp.setMargins(dp(10),dp(14),0,0);hero.addView(back,blp);
  TextView heart=t(isFav(x)?"♥":"♡",25);heart.setTextColor(Color.WHITE);heart.setGravity(Gravity.CENTER);heart.setBackground(detailGlassCircle());FrameLayout.LayoutParams hlp=new FrameLayout.LayoutParams(dp(50),dp(50),Gravity.TOP|Gravity.RIGHT);hlp.setMargins(0,dp(14),dp(10),0);hero.addView(heart,hlp);
  heart.setOnClickListener(v->{toggleFav(x);heart.setText(isFav(x)?"♥":"♡");});
  LinearLayout heroInfo=new LinearLayout(this);heroInfo.setOrientation(LinearLayout.VERTICAL);heroInfo.setPadding(dp(18),dp(8),dp(18),dp(10));FrameLayout.LayoutParams ilp=new FrameLayout.LayoutParams(-1,-2,Gravity.BOTTOM);hero.addView(heroInfo,ilp);
  String readyTitle=detailValue(ready,"name","title");if(readyTitle.isEmpty())readyTitle=title;TextView hn=t(readyTitle,27);hn.setTypeface(null,1);hn.setMaxLines(2);hn.setLineSpacing(0,1.02f);hn.setPadding(0,0,0,0);heroInfo.addView(hn);
  LinearLayout.LayoutParams heroLp=new LinearLayout.LayoutParams(-1,dp(365));heroLp.setMargins(0,0,0,dp(6));body.addView(hero,heroLp);

  final LinearLayout detailHost=new LinearLayout(this);detailHost.setOrientation(LinearLayout.VERTICAL);detailHost.setPadding(dp(18),0,dp(18),0);body.addView(detailHost,new LinearLayout.LayoutParams(-1,-2));
  renderDetailContent(detailHost,x,ready,hn,p,heart,readyTitle,false);
 }
 JSONObject readDetailCache(JSONObject x){try{String k=detailCacheKey(x);String mem=detailMemoryCache.get(k);if(mem!=null&&!mem.isEmpty())return new JSONObject(mem);String raw=sp.getString("detail_"+k,"");if(raw.isEmpty())return null;detailMemoryCache.put(k,raw);return new JSONObject(raw);}catch(Exception e){return null;}}
 void saveDetailCache(JSONObject x,JSONObject d){if(d==null)return;try{JSONObject merged=mergeDetailJson(readDetailCache(x),d);String k=detailCacheKey(x),raw=merged.toString();detailMemoryCache.put(k,raw);sp.edit().putString("detail_"+k,raw).apply();}catch(Exception ignored){}}
 JSONObject mergeDetailJson(JSONObject base,JSONObject add){JSONObject out=new JSONObject();try{if(base!=null){java.util.Iterator<String> it=base.keys();while(it.hasNext()){String k=it.next();out.put(k,base.opt(k));}}if(add!=null){java.util.Iterator<String> it=add.keys();while(it.hasNext()){String k=it.next();Object v=add.opt(k);boolean useful=v!=null&&v!=JSONObject.NULL;if(v instanceof String)useful=!((String)v).trim().isEmpty();if(v instanceof JSONArray)useful=((JSONArray)v).length()>0;if(useful)out.put(k,v);}}}catch(Exception ignored){}return out;}
 boolean detailNeedsEnrich(JSONObject d){if(d==null)return true;String desc=detailValue(d,"description","plot","overview"),genre=detailValue(d,"category_name","genre","genres"),rating=detailValue(d,"imdb_rating","rating","vote_average","score"),back=detailValue(d,"landscape","landscape_img","backdrop","backdrop_path");JSONArray cast=d.optJSONArray("cast_list");int vt=d.optInt("video_type",d.optInt("type_id",1));boolean series=vt==2||"series".equalsIgnoreCase(d.optString("type",""));if(series&&detailSeriesSeasons(d).length()==0)return true;return desc.isEmpty()||genre.isEmpty()||rating.isEmpty()||back.isEmpty()||cast==null||cast.length()==0;}
 void requestDetailEnrich(JSONObject source,TextView hn,ImageView heroImage,TextView heart,String fallbackTitle,LinearLayout detailHost,int gen){JSONObject cur=readDetailCache(source);if(!detailNeedsEnrich(cur))return;Api.post("content_enrich",Api.m("user_id",uid,"video_id",source.optString("id"),"video_type",String.valueOf(source.optInt("video_type",source.optInt("type_id",1)))),new Api.CB(){public void ok(JSONObject j){if(gen!=viewGen||!detailOpen)return;JSONArray a=j.optJSONArray("result");JSONObject d=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(d==null)return;saveDetailCache(source,d);JSONObject merged=readDetailCache(source);if(merged==null)return;int y=mainScroll==null?0:mainScroll.getScrollY();detailHost.removeAllViews();renderDetailContent(detailHost,source,merged,hn,heroImage,heart,fallbackTitle,false);if(mainScroll!=null&&y>0)mainScroll.post(()->mainScroll.scrollTo(0,y));}public void err(String e){}});}
 void openResolvedContent(JSONObject source,String title,boolean offline){
  // v16.49: reprodução parte sempre do item autenticado recebido da fonte Xtream.
  // Isso elimina a falha em que categorias carregadas depois da Home vinham sem URL
  // por não enviarem user_id ao content_by_category.
  JSONObject cached=readDetailCache(source);JSONObject ready=mergeDetailJson(cached,source);String u=detailPlayUrl(ready);
  if(!u.isEmpty()){openPlayableUrl(ready,title,offline,u);return;}
  // Primeiro tenta o detalhe. Se o provedor não responder get_vod_info, refaz somente
  // a categoria do item, autenticada, e recupera a URL pronta direto da fonte.
  Api.post("content_detail",Api.m("user_id",uid,"video_id",source.optString("id"),"video_type",String.valueOf(source.optInt("video_type",source.optInt("type_id",1)))),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject fresh=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(fresh!=null){JSONObject withSource=mergeDetailJson(source,fresh);saveDetailCache(source,withSource);JSONObject merged=mergeDetailJson(source,readDetailCache(source));String url=detailPlayUrl(merged);if(!url.isEmpty()){openPlayableUrl(merged,title,offline,url);return;}}resolvePlayableFromCategory(source,title,offline);}public void err(String e){resolvePlayableFromCategory(source,title,offline);}});
 }
 String detailCacheKey(JSONObject x){String provider=Api.PROVIDER==null?"":Api.PROVIDER;String type=String.valueOf(x.optInt("video_type",x.optInt("type_id",1)));String id=x.optString("id",x.optString("video_id",x.optString("tmdb_id",x.optString("name","item"))));return (provider+"_"+type+"_"+id).replaceAll("[^a-zA-Z0-9._-]","_");}
 String detailValue(JSONObject d,String...keys){if(d==null)return "";for(String k:keys){String v=d.optString(k,"");if(v!=null&&!v.trim().isEmpty()&&!"null".equalsIgnoreCase(v.trim()))return v.trim();}return "";}
 JSONArray detailSeriesSeasons(JSONObject d){
  JSONArray out=new JSONArray();if(d==null)return out;java.util.TreeMap<Integer,String> names=new java.util.TreeMap<>();
  Object raw=d.opt("season");if(!(raw instanceof JSONArray))raw=d.opt("seasons");
  if(raw instanceof JSONArray){JSONArray a=(JSONArray)raw;for(int i=0;i<a.length();i++){Object v=a.opt(i);int sn=0;String nm="";if(v instanceof JSONObject){JSONObject s=(JSONObject)v;sn=s.optInt("season_number",s.optInt("id",s.optInt("season",0)));nm=s.optString("name","");}else if(v instanceof Number)sn=((Number)v).intValue();else if(v instanceof String){try{sn=Integer.parseInt(((String)v).replaceAll("[^0-9]",""));}catch(Exception ignored){}}if(sn<=0)sn=i+1;if(nm.isEmpty())nm="Temporada "+sn;names.put(sn,nm);}}
  JSONObject by=d.optJSONObject("episodes_by_season");if(by!=null){java.util.Iterator<String> it=by.keys();while(it.hasNext()){String k=it.next();try{int sn=Integer.parseInt(k.replaceAll("[^0-9]",""));if(sn>0&&!names.containsKey(sn))names.put(sn,"Temporada "+sn);}catch(Exception ignored){}}}
  for(java.util.Map.Entry<Integer,String> e:names.entrySet()){JSONObject s=new JSONObject();try{s.put("id",e.getKey());s.put("season_number",e.getKey());s.put("name",e.getValue());}catch(Exception ignored){}out.put(s);}return out;
 }
 String detailPlayUrl(JSONObject d){return detailValue(d,"video_1080","video_720","video_480","video_320","video_url","stream_url","url");}
 boolean sameContentId(JSONObject a,JSONObject b){if(a==null||b==null)return false;String ai=a.optString("id",a.optString("video_id",""));String bi=b.optString("id",b.optString("video_id",""));return !ai.isEmpty()&&ai.equals(bi);}
 void openPlayableUrl(JSONObject source,String title,boolean offline,String url){if(url==null||url.trim().isEmpty())return;if(offline){downloadOffline(source,url,title.isEmpty()?"conteudo":title,detailValue(source,"thumbnail","portrait_img","poster","poster_path"),source.optString("id","0"),source.optString("video_type","1"));}else{Intent in=new Intent(MainActivity.this,PlayerActivity.class);in.putExtra("url",url);in.putExtra("url_1080",detailValue(source,"video_1080"));in.putExtra("url_720",detailValue(source,"video_720"));in.putExtra("url_480",detailValue(source,"video_480"));in.putExtra("url_320",detailValue(source,"video_320"));in.putExtra("title",title);int vt=source.optInt("video_type",source.optInt("type_id",1));if(vt==1){String movieId=source.optString("id",source.optString("video_id",""));in.putExtra("movie_id",movieId);in.putExtra("movie_title",title);in.putExtra("movie_poster",detailValue(source,"thumbnail","portrait_img","poster","poster_path"));in.putExtra("movie_landscape",detailValue(source,"landscape","landscape_img","backdrop","backdrop_path"));int resume=movieResumePosition(movieId);if(resume>0)in.putExtra("resume_ms",resume);}startActivity(in);}}
 void resolvePlayableFromCategory(JSONObject source,String title,boolean offline){
  int vt=source.optInt("video_type",source.optInt("type_id",1));String cid=source.optString("category_id","");
  if(vt!=1||cid.isEmpty()){Toast.makeText(MainActivity.this,"Conteúdo indisponível agora.",0).show();return;}
  int n;try{n=Integer.parseInt(cid);}catch(Exception e){Toast.makeText(MainActivity.this,"Conteúdo indisponível agora.",0).show();return;}
  Api.post("content_by_category",Api.m("user_id",uid,"category_id",String.valueOf(n),"page_no","1"),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject found=null;if(a!=null)for(int i=0;i<a.length();i++){JSONObject row=a.optJSONObject(i);if(sameContentId(source,row)){found=row;break;}}if(found==null){Toast.makeText(MainActivity.this,"Conteúdo indisponível agora.",0).show();return;}JSONObject merged=mergeDetailJson(source,found);saveDetailCache(source,merged);String url=detailPlayUrl(merged);if(url.isEmpty()){Toast.makeText(MainActivity.this,"Conteúdo indisponível agora.",0).show();return;}openPlayableUrl(merged,title,offline,url);}public void err(String e){Toast.makeText(MainActivity.this,"Não foi possível abrir o conteúdo.",0).show();}});
 }
 void renderDetailContent(LinearLayout host,JSONObject source,JSONObject d,TextView hn,ImageView heroImage,TextView heart,String fallbackTitle,boolean partial){
  if(host==null||d==null)return;
  String tmdbTitle=detailValue(d,"name","title");if(tmdbTitle.isEmpty())tmdbTitle=fallbackTitle;if(!tmdbTitle.isEmpty())hn.setText(tmdbTitle);
  String heroUrl=detailValue(d,"landscape","landscape_img","backdrop","backdrop_path");if(!heroUrl.isEmpty())Img.loadVisible(heroImage,heroUrl);
  String desc=detailValue(d,"description","plot","overview");String date=detailValue(d,"release_date","date","first_air_date");String genre=detailValue(d,"category_name","genre","genres");String cast=detailValue(d,"cast");JSONArray castList=d.optJSONArray("cast_list");String dur=detailValue(d,"video_duration","duration","runtime");String rating=detailValue(d,"imdb_rating","rating","vote_average","score");final String displayTitle=tmdbTitle;
  int vt=d.optInt("video_type",source.optInt("video_type",source.optInt("type_id",1)));boolean isSeries=vt==2||"series".equalsIgnoreCase(d.optString("type",""));
  JSONArray seasons=detailSeriesSeasons(d);

  String providerId=source.optString("id",d.optString("id",""));if(!providerId.isEmpty()){View idBadge=detailIdBadge("ID:  "+providerId);LinearLayout.LayoutParams idlp=new LinearLayout.LayoutParams(-2,-2);idlp.setMargins(0,dp(2),0,dp(12));host.addView(idBadge,idlp);}

  LinearLayout metaRow=new LinearLayout(this);metaRow.setOrientation(LinearLayout.HORIZONTAL);metaRow.setGravity(Gravity.CENTER_VERTICAL);metaRow.setPadding(0,0,0,dp(2));
  if(!rating.isEmpty()&&!rating.equals("0")&&!rating.equals("0.0")){metaRow.addView(detailMetaItem("★",formatRatingDisplay(rating),0xffffcf4a));}
  if(!date.isEmpty()){metaRow.addView(detailMetaItem("▣",shortDate(date),0xffb7c0bb));}
  if(isSeries&&seasons!=null&&seasons.length()>0){String s=seasons.length()+" "+(seasons.length()==1?"Temporada":"Temporadas");metaRow.addView(detailMetaItem("▰",s,0xffb7c0bb));}
  else if(!dur.isEmpty()&&!dur.equals("0")){metaRow.addView(detailMetaItem("◷",formatDurationDisplay(dur),0xffb7c0bb));}
  if(metaRow.getChildCount()>0){LinearLayout.LayoutParams mlp=new LinearLayout.LayoutParams(-1,dp(42));mlp.setMargins(0,0,0,dp(4));host.addView(metaRow,mlp);}

  if(!genre.isEmpty()){TextView gt=t("♣  "+fixTitle(genre),14);gt.setTextColor(0xffaab3ae);gt.setPadding(dp(2),0,0,dp(8));gt.setMaxLines(2);host.addView(gt,new LinearLayout.LayoutParams(-1,-2));}

  if(!isSeries){
   renderMovieResume(source,d,host,displayTitle);
   boolean canResume=movieResumePosition(source.optString("id",d.optString("id","")))>0;
   View play=detailPrimaryAction(canResume?"Continuar assistindo":"Assistir");LinearLayout.LayoutParams plp=new LinearLayout.LayoutParams(-1,dp(62));plp.setMargins(0,dp(8),0,dp(12));host.addView(play,plp);
   play.setOnClickListener(v->showMovieActions(source,d,displayTitle));
  }

  if(!desc.isEmpty()||!partial){
   TextView st=detailSectionTitle("Sinopse");LinearLayout.LayoutParams stlp=new LinearLayout.LayoutParams(-1,-2);stlp.setMargins(0,dp(12),0,dp(4));host.addView(st,stlp);
   LinearLayout synCard=new LinearLayout(this);synCard.setOrientation(LinearLayout.VERTICAL);GradientDrawable sg=round(0xff151b18,18);sg.setStroke(dp(1),0xff252d29);synCard.setBackground(sg);synCard.setPadding(dp(14),dp(14),dp(14),dp(12));
   String fullDesc=desc.isEmpty()?"Sinopse ainda não disponível.":desc;final boolean expandable=fullDesc.length()>165;final boolean[] expanded=new boolean[]{false};
   TextView synopsis=t(fullDesc,15);synopsis.setTextColor(0xffdde2df);synopsis.setLineSpacing(dp(3),1.15f);synopsis.setPadding(0,0,0,0);if(expandable){synopsis.setMaxLines(3);synopsis.setEllipsize(android.text.TextUtils.TruncateAt.END);}synCard.addView(synopsis);
   if(expandable){TextView more=t("Ler mais  ⌄",14);more.setTextColor(GREEN);more.setTypeface(null,1);more.setPadding(0,dp(10),0,0);more.setOnClickListener(v->{expanded[0]=!expanded[0];if(expanded[0]){synopsis.setMaxLines(Integer.MAX_VALUE);synopsis.setEllipsize(null);more.setText("Ler menos  ⌃");}else{synopsis.setMaxLines(3);synopsis.setEllipsize(android.text.TextUtils.TruncateAt.END);more.setText("Ler mais  ⌄");}});synCard.addView(more);}
   LinearLayout.LayoutParams slp=new LinearLayout.LayoutParams(-1,-2);slp.setMargins(0,0,0,dp(14));host.addView(synCard,slp);
  }

  if(isSeries&&seasons!=null&&seasons.length()>0){renderSeriesSeasons(source,d,seasons,host);}

  if((castList!=null&&castList.length()>0)||!cast.isEmpty()){
   TextView ct=detailSectionTitle("Elenco");LinearLayout.LayoutParams ctlp=new LinearLayout.LayoutParams(-1,-2);ctlp.setMargins(0,dp(12),0,dp(2));host.addView(ct,ctlp);
   HorizontalScrollView hs=new HorizontalScrollView(this);hs.setHorizontalScrollBarEnabled(false);hs.setOverScrollMode(View.OVER_SCROLL_NEVER);LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);row.setPadding(dp(2),0,dp(8),0);
   if(castList!=null&&castList.length()>0){for(int ci=0;ci<Math.min(12,castList.length());ci++){JSONObject ca=castList.optJSONObject(ci);if(ca!=null)row.addView(castPerson(ca));}}
   else{String[] names=cast.split(",");int added=0;for(String raw:names){String n=raw.trim();if(n.isEmpty())continue;JSONObject ca=new JSONObject();try{ca.put("name",n);}catch(Exception ignored){}row.addView(castPerson(ca));added++;if(added>=12)break;}}
   hs.addView(row);LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(-1,dp(140));clp.setMargins(0,0,0,dp(8));host.addView(hs,clp);
  }
  Space bottomSpace=new Space(this);host.addView(bottomSpace,new LinearLayout.LayoutParams(1,dp(22)));
 }

 void renderSeriesSeasons(JSONObject source,JSONObject detail,JSONArray seasons,LinearLayout host){
  TextView seasonsTitle=detailSectionTitle("Temporadas");host.addView(seasonsTitle,new LinearLayout.LayoutParams(-1,-2));
  HorizontalScrollView shs=new HorizontalScrollView(this);shs.setHorizontalScrollBarEnabled(false);shs.setOverScrollMode(View.OVER_SCROLL_NEVER);LinearLayout srow=new LinearLayout(this);srow.setOrientation(LinearLayout.HORIZONTAL);srow.setPadding(0,0,dp(8),0);shs.addView(srow);
  LinearLayout.LayoutParams shlp=new LinearLayout.LayoutParams(-1,dp(62));shlp.setMargins(0,0,0,dp(8));host.addView(shs,shlp);

  // v16.63: cartão de continuar aparece entre temporadas e episódios, igual ao fluxo
  // da referência. O progresso é salvo localmente apenas para retomada, sem cachear catálogo.
  final LinearLayout resumeHost=new LinearLayout(this);resumeHost.setOrientation(LinearLayout.VERTICAL);host.addView(resumeHost,new LinearLayout.LayoutParams(-1,-2));
  activeSeriesResumeHost=resumeHost;activeSeriesDetail=detail;activeSeriesSource=source;renderSeriesResume(source,detail,resumeHost);

  TextView episodesTitle=detailSectionTitle("Episódios");host.addView(episodesTitle,new LinearLayout.LayoutParams(-1,-2));
  final LinearLayout episodesHost=new LinearLayout(this);episodesHost.setOrientation(LinearLayout.VERTICAL);host.addView(episodesHost,new LinearLayout.LayoutParams(-1,-2));
  final java.util.ArrayList<TextView> chips=new java.util.ArrayList<>();final int[] selected={0};
  for(int i=0;i<seasons.length();i++){JSONObject s=seasons.optJSONObject(i);if(s==null)continue;final int idx=i;final int sid=s.optInt("id",s.optInt("season_number",i+1));String label=s.optString("name","Temporada "+sid);TextView chip=t(label,14);chip.setTypeface(null,1);chip.setGravity(Gravity.CENTER);chip.setPadding(dp(14),0,dp(14),0);styleSeasonChip(chip,i==0);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-2,dp(50));lp.setMargins(0,0,dp(10),0);srow.addView(chip,lp);chips.add(chip);chip.setOnClickListener(v->{if(selected[0]==idx)return;selected[0]=idx;for(int k=0;k<chips.size();k++)styleSeasonChip(chips.get(k),k==idx);loadSeriesEpisodes(source,detail,sid,episodesHost);});if(i==0)loadSeriesEpisodes(source,detail,sid,episodesHost);}
 }
 void renderSeriesResume(JSONObject source,JSONObject detail,LinearLayout host){
  if(host==null)return;host.removeAllViews();if(source==null||detail==null)return;String sid=source.optString("id",detail.optString("id",""));if(sid.isEmpty())return;String raw=sp.getString(seriesResumeKey(sid),"");if(raw.isEmpty())return;try{JSONObject r=new JSONObject(raw);long pos=r.optLong("position",0),dur=r.optLong("duration",0);if(pos<4000||dur<=0||pos>=dur-4000)return;String eid=r.optString("episode_id","");JSONObject ep=findSeriesEpisode(detail,eid);if(ep==null)return;String epNo=r.optString("episode_number",ep.optString("episode_number",ep.optString("episode_num","")));String title=r.optString("episode_title",ep.optString("name","Episódio"));LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setPadding(dp(14),dp(10),dp(14),dp(9));GradientDrawable cg=round(0xff151b18,14);cg.setStroke(dp(1),0xff315b47);card.setBackground(cg);LinearLayout line=new LinearLayout(this);line.setGravity(Gravity.CENTER_VERTICAL);TextView play=t("▶",18);play.setTextColor(GREEN);play.setGravity(Gravity.CENTER);line.addView(play,new LinearLayout.LayoutParams(dp(38),dp(42)));LinearLayout words=new LinearLayout(this);words.setOrientation(LinearLayout.VERTICAL);TextView small=t("Continuar"+(epNo.isEmpty()?"":" · Ep. "+epNo),12);small.setTextColor(0xff9ca7a1);small.setPadding(0,0,0,0);words.addView(small);TextView tt=t(title,13);tt.setTextColor(Color.WHITE);tt.setTypeface(null,1);tt.setSingleLine(true);tt.setEllipsize(android.text.TextUtils.TruncateAt.END);tt.setPadding(0,dp(2),0,0);words.addView(tt);line.addView(words,new LinearLayout.LayoutParams(0,dp(44),1));card.addView(line,new LinearLayout.LayoutParams(-1,dp(44)));FrameLayout bar=new FrameLayout(this);View track=new View(this);track.setBackground(round(0xff28312d,2));bar.addView(track,new FrameLayout.LayoutParams(-1,dp(4),Gravity.CENTER_VERTICAL));View fill=new View(this);fill.setBackground(round(GREEN,2));FrameLayout.LayoutParams fp=new FrameLayout.LayoutParams(0,dp(4),Gravity.CENTER_VERTICAL);int full=Math.max(dp(40),getResources().getDisplayMetrics().widthPixels-dp(96));fp.width=(int)Math.max(dp(12),Math.min(full,full*(pos/(float)dur)));bar.addView(fill,fp);card.addView(bar,new LinearLayout.LayoutParams(-1,dp(12)));card.setOnClickListener(v->openSeriesEpisode(detail,ep,title,(int)pos));LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(-1,dp(72));clp.setMargins(0,0,0,dp(10));host.addView(card,clp);}catch(Exception ignored){}
 }
 String seriesResumeKey(String seriesId){String provider=Api.PROVIDER==null?"":Api.PROVIDER;return "series_resume_"+(provider+"_"+seriesId).replaceAll("[^a-zA-Z0-9._-]","_");}
 JSONObject findSeriesEpisode(JSONObject detail,String episodeId){if(detail==null||episodeId==null||episodeId.isEmpty())return null;JSONObject by=detail.optJSONObject("episodes_by_season");if(by==null)return null;java.util.Iterator<String> it=by.keys();while(it.hasNext()){JSONArray a=by.optJSONArray(it.next());if(a==null)continue;for(int i=0;i<a.length();i++){JSONObject ep=a.optJSONObject(i);if(ep==null)continue;String id=ep.optString("id",ep.optString("video_id",""));if(episodeId.equals(id))return ep;}}return null;}
 void styleSeasonChip(TextView chip,boolean selected){if(chip==null)return;if(selected){GradientDrawable g=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{GREEN,0xff49e98b});g.setCornerRadius(dp(16));chip.setBackground(g);chip.setTextColor(0xff041109);}else{GradientDrawable g=round(0xff151b18,16);g.setStroke(dp(1),0xff315b47);chip.setBackground(g);chip.setTextColor(0xffd9dfdc);}}
 void loadSeriesEpisodes(JSONObject source,JSONObject detail,int seasonId,LinearLayout host){
  if(host==null)return;host.removeAllViews();
  // v16.62: usa primeiro todos os episódios já entregues no detalhe. Não exibe
  // estado de carregamento; o fallback de rede é silencioso.
  JSONObject bySeason=detail==null?null:detail.optJSONObject("episodes_by_season");JSONArray ready=bySeason==null?null:bySeason.optJSONArray(String.valueOf(seasonId));
  if(ready!=null&&ready.length()>0){renderSeriesEpisodeRow(detail,ready,host,seasonId);return;}
  Api.post("get_video_by_season_id",Api.m("user_id",uid,"show_id",source.optString("id"),"season_id",String.valueOf(seasonId)),new Api.CB(){public void ok(JSONObject j){if(!detailOpen||host.getParent()==null)return;JSONArray a=j.optJSONArray("result");host.removeAllViews();if(a==null||a.length()==0){TextView empty=t("Nenhum episódio disponível.",14);empty.setTextColor(0xff939d98);host.addView(empty);return;}try{JSONObject map=detail.optJSONObject("episodes_by_season");if(map==null){map=new JSONObject();detail.put("episodes_by_season",map);}map.put(String.valueOf(seasonId),a);}catch(Exception ignored){}renderSeriesEpisodeRow(detail,a,host,seasonId);}public void err(String e){if(!detailOpen||host.getParent()==null)return;host.removeAllViews();TextView err=t("Nenhum episódio disponível.",14);err.setTextColor(0xff939d98);host.addView(err);}});
 }
 void renderSeriesEpisodeRow(JSONObject detail,JSONArray a,LinearLayout host,int seasonId){
  if(host==null)return;host.removeAllViews();if(a==null||a.length()==0){TextView empty=t("Nenhum episódio disponível.",14);empty.setTextColor(0xff939d98);host.addView(empty);return;}
  HorizontalScrollView hs=new HorizontalScrollView(this);hs.setHorizontalScrollBarEnabled(false);hs.setOverScrollMode(View.OVER_SCROLL_NEVER);LinearLayout row=new LinearLayout(this);row.setOrientation(LinearLayout.HORIZONTAL);row.setPadding(0,0,dp(8),0);
  for(int i=0;i<a.length();i++){JSONObject ep=a.optJSONObject(i);if(ep==null)continue;final JSONObject episode=ep;String num=episode.optString("episode_number",episode.optString("episode_num",""));String label=num.isEmpty()?String.valueOf(i+1):num;TextView cell=t(label,18);cell.setTypeface(null,1);cell.setTextColor(GREEN);cell.setGravity(Gravity.CENTER);GradientDrawable eg=round(0xff151b18,12);eg.setStroke(dp(1),0xff315b47);cell.setBackground(eg);LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(dp(64),dp(62));cp.setMargins(0,0,dp(10),0);row.addView(cell,cp);cell.setOnClickListener(v->{String url=detailPlayUrl(episode);if(url.isEmpty()){Toast.makeText(MainActivity.this,"Episódio indisponível agora.",0).show();return;}String et=episode.optString("name","Episódio "+label);showEpisodeActions(detail,episode,et,seasonId,label);});}
  hs.addView(row);host.addView(hs,new LinearLayout.LayoutParams(-1,dp(68)));
 }
 java.util.ArrayList<java.util.HashMap<String,String>> buildSeriesEpisodeQueue(JSONObject detail){
  java.util.ArrayList<java.util.HashMap<String,String>> out=new java.util.ArrayList<>();if(detail==null)return out;JSONObject by=detail.optJSONObject("episodes_by_season");if(by==null)return out;
  java.util.TreeSet<Integer> seasonNumbers=new java.util.TreeSet<>();java.util.HashMap<Integer,String> seasonKeys=new java.util.HashMap<>();java.util.ArrayList<String> otherKeys=new java.util.ArrayList<>();java.util.Iterator<String> it=by.keys();while(it.hasNext()){String k=it.next();try{int n=Integer.parseInt(k.replaceAll("[^0-9]",""));if(n>0){seasonNumbers.add(n);seasonKeys.put(n,k);}else otherKeys.add(k);}catch(Exception e){otherKeys.add(k);}}
  java.util.ArrayList<String> keys=new java.util.ArrayList<>();for(Integer n:seasonNumbers)keys.add(seasonKeys.get(n));keys.addAll(otherKeys);
  for(String k:keys){JSONArray arr=by.optJSONArray(k);if(arr==null)continue;for(int i=0;i<arr.length();i++){JSONObject ep=arr.optJSONObject(i);if(ep==null)continue;java.util.HashMap<String,String> m=new java.util.HashMap<>();m.put("id",ep.optString("id",ep.optString("video_id","")));m.put("title",ep.optString("name",ep.optString("title","Episódio "+(i+1))));m.put("season",k.replaceAll("[^0-9]",""));m.put("episode",ep.optString("episode_number",ep.optString("episode_num",String.valueOf(i+1))));m.put("url",detailPlayUrl(ep));m.put("url_1080",detailValue(ep,"video_1080"));m.put("url_720",detailValue(ep,"video_720"));m.put("url_480",detailValue(ep,"video_480"));m.put("url_320",detailValue(ep,"video_320"));if(!m.get("url").isEmpty())out.add(m);}}
  return out;
 }
 boolean isTelevisionDevice(){
  try{
   android.app.UiModeManager ui=(android.app.UiModeManager)getSystemService(android.content.Context.UI_MODE_SERVICE);
   if(ui!=null&&ui.getCurrentModeType()==android.content.res.Configuration.UI_MODE_TYPE_TELEVISION)return true;
   android.content.pm.PackageManager pm=getPackageManager();
   if(pm!=null&&(pm.hasSystemFeature(android.content.pm.PackageManager.FEATURE_LEANBACK)||pm.hasSystemFeature(android.content.pm.PackageManager.FEATURE_TELEVISION)||pm.hasSystemFeature("amazon.hardware.fire_tv")))return true;
  }catch(Exception ignored){}
  return false;
 }
 void showEpisodeActions(JSONObject detail,JSONObject episode,String title,int seasonId,String episodeLabel){
  final Dialog d=new Dialog(this);LinearLayout sheet=new LinearLayout(this);sheet.setOrientation(LinearLayout.VERTICAL);sheet.setPadding(dp(18),dp(12),dp(18),dp(18));GradientDrawable sb=round(0xff111713,22);sb.setStroke(dp(1),0xff28352e);sheet.setBackground(sb);
  View handle=new View(this);handle.setBackground(round(0xff56605b,3));LinearLayout.LayoutParams hp=new LinearLayout.LayoutParams(dp(44),dp(4));hp.gravity=Gravity.CENTER_HORIZONTAL;hp.setMargins(0,0,0,dp(10));sheet.addView(handle,hp);
  LinearLayout head=new LinearLayout(this);head.setGravity(Gravity.CENTER_VERTICAL);TextView num=t(episodeLabel,17);num.setTextColor(GREEN);num.setTypeface(null,1);num.setGravity(Gravity.CENTER);GradientDrawable nb=round(0xff18221d,10);nb.setStroke(dp(1),0xff315b47);num.setBackground(nb);head.addView(num,new LinearLayout.LayoutParams(dp(46),dp(46)));LinearLayout htxt=new LinearLayout(this);htxt.setOrientation(LinearLayout.VERTICAL);TextView small=t("Episódio "+episodeLabel,11);small.setTextColor(0xff96a09b);small.setPadding(0,0,0,0);htxt.addView(small);TextView nm=t(title,14);nm.setTypeface(null,1);nm.setSingleLine(true);nm.setEllipsize(android.text.TextUtils.TruncateAt.END);nm.setPadding(0,dp(2),0,0);htxt.addView(nm);LinearLayout.LayoutParams htp=new LinearLayout.LayoutParams(0,dp(48),1);htp.setMargins(dp(12),0,0,0);head.addView(htxt,htp);sheet.addView(head,new LinearLayout.LayoutParams(-1,dp(54)));
  View watch=episodeActionRow("▶","Assistir Episódio","Reproduzir agora");View cast=null;View down=episodeActionRow("⇩","Baixar Episódio","Disponível sem internet");LinearLayout.LayoutParams ap=new LinearLayout.LayoutParams(-1,dp(62));ap.setMargins(0,dp(8),0,0);sheet.addView(watch,ap);if(!isTelevisionDevice()){cast=episodeActionRow("▣","Espelhar na TV","Dispositivos disponíveis");LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(-1,dp(62));cp.setMargins(0,dp(8),0,0);sheet.addView(cast,cp);}LinearLayout.LayoutParams dpv=new LinearLayout.LayoutParams(-1,dp(62));dpv.setMargins(0,dp(8),0,0);sheet.addView(down,dpv);
  watch.setOnClickListener(v->{d.dismiss();openSeriesEpisode(detail,episode,title,0);});if(cast!=null)cast.setOnClickListener(v->{Toast.makeText(MainActivity.this,"Nenhum dispositivo disponível.",Toast.LENGTH_SHORT).show();});down.setOnClickListener(v->{String url=detailPlayUrl(episode);if(url.isEmpty()){Toast.makeText(MainActivity.this,"Episódio indisponível para download.",0).show();return;}d.dismiss();downloadOffline(episode,url,title,detailValue(episode,"thumbnail","portrait_img","poster","poster_path"),episode.optString("id",episode.optString("video_id","0")),"2");});
  d.setContentView(sheet);Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(Color.TRANSPARENT));w.setDimAmount(.55f);w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);w.setGravity(Gravity.BOTTOM);w.setLayout(-1,-2);}d.setOnShowListener(x->{Window ww=d.getWindow();if(ww!=null){ww.setLayout(-1,-2);ww.setGravity(Gravity.BOTTOM);}if(tvMode){prepareTvFocusTree(sheet);requestTvFocus(watch);}});d.show();
 }
 View episodeActionRow(String icon,String title,String sub){LinearLayout row=new LinearLayout(this);row.setGravity(Gravity.CENTER_VERTICAL);if(tvMode){row.setFocusable(true);row.setFocusableInTouchMode(true);armTvFocus(row);}row.setPadding(dp(12),0,dp(10),0);row.setBackground(round(0xff17201b,13));TextView ic=t(icon,18);ic.setTextColor(GREEN);ic.setGravity(Gravity.CENTER);row.addView(ic,new LinearLayout.LayoutParams(dp(44),dp(48)));LinearLayout words=new LinearLayout(this);words.setOrientation(LinearLayout.VERTICAL);TextView tt=t(title,14);tt.setTypeface(null,1);tt.setPadding(0,0,0,0);words.addView(tt);TextView ss=t(sub,11);ss.setTextColor(0xff909a95);ss.setPadding(0,dp(2),0,0);words.addView(ss);row.addView(words,new LinearLayout.LayoutParams(0,dp(48),1));TextView ar=t("›",24);ar.setTextColor(0xffa5aea9);ar.setGravity(Gravity.CENTER);row.addView(ar,new LinearLayout.LayoutParams(dp(32),dp(48)));return row;}
 void openSeriesEpisode(JSONObject detail,JSONObject episode,String title){openSeriesEpisode(detail,episode,title,0);}
 void openSeriesEpisode(JSONObject detail,JSONObject episode,String title,int resumeMs){
  String url=detailPlayUrl(episode);if(url.isEmpty()){Toast.makeText(this,"Episódio indisponível agora.",0).show();return;}java.util.ArrayList<java.util.HashMap<String,String>> queue=buildSeriesEpisodeQueue(detail);int current=-1;String id=episode.optString("id",episode.optString("video_id",""));for(int i=0;i<queue.size();i++){if(!id.isEmpty()&&id.equals(queue.get(i).get("id"))){current=i;break;}}PlayerActivity.setEpisodeQueue(queue,current);
  String seriesId="";if(activeSeriesSource!=null)seriesId=activeSeriesSource.optString("id","");String season=episode.optString("season_number",episode.optString("season",""));String epNo=episode.optString("episode_number",episode.optString("episode_num",""));
  Intent in=new Intent(MainActivity.this,PlayerActivity.class);in.putExtra("url",url);in.putExtra("url_1080",detailValue(episode,"video_1080"));in.putExtra("url_720",detailValue(episode,"video_720"));in.putExtra("url_480",detailValue(episode,"video_480"));in.putExtra("url_320",detailValue(episode,"video_320"));in.putExtra("title",title);in.putExtra("episode_queue",current>=0&&queue.size()>1);in.putExtra("episode_index",current);in.putExtra("series_id",seriesId);in.putExtra("episode_id",id);in.putExtra("episode_title",title);in.putExtra("season_number",season);in.putExtra("episode_number",epNo);if(resumeMs>0)in.putExtra("resume_ms",resumeMs);startActivity(in);
 }


 String movieResumeKey(String movieId){String provider=Api.PROVIDER==null?"":Api.PROVIDER;return "movie_resume_"+(provider+"_"+movieId).replaceAll("[^a-zA-Z0-9._-]","_");}
 JSONObject movieResume(String movieId){if(movieId==null||movieId.isEmpty())return null;String raw=sp.getString(movieResumeKey(movieId),"");if(raw.isEmpty())return null;try{JSONObject r=new JSONObject(raw);long pos=r.optLong("position",0),dur=r.optLong("duration",0);if(pos<4000||dur<=0||pos>=dur-4000)return null;return r;}catch(Exception e){return null;}}
 int movieResumePosition(String movieId){JSONObject r=movieResume(movieId);return r==null?0:(int)Math.min(Integer.MAX_VALUE,r.optLong("position",0));}
 void clearMovieResume(String movieId){if(movieId==null||movieId.isEmpty())return;sp.edit().remove(movieResumeKey(movieId)).apply();}
 void renderMovieResume(JSONObject source,JSONObject detail,LinearLayout host,String title){if(source==null||host==null)return;String id=source.optString("id",detail==null?"":detail.optString("id",""));JSONObject r=movieResume(id);if(r==null)return;long pos=r.optLong("position",0),dur=r.optLong("duration",0);LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setPadding(dp(14),dp(10),dp(14),dp(9));GradientDrawable cg=round(0xff151b18,14);cg.setStroke(dp(1),0xff315b47);card.setBackground(cg);LinearLayout line=new LinearLayout(this);line.setGravity(Gravity.CENTER_VERTICAL);TextView play=t("▶",18);play.setTextColor(GREEN);play.setGravity(Gravity.CENTER);line.addView(play,new LinearLayout.LayoutParams(dp(38),dp(42)));LinearLayout words=new LinearLayout(this);words.setOrientation(LinearLayout.VERTICAL);TextView small=t("Continuar assistindo",12);small.setTextColor(0xff9ca7a1);small.setPadding(0,0,0,0);words.addView(small);TextView tt=t(title,13);tt.setTextColor(Color.WHITE);tt.setTypeface(null,1);tt.setSingleLine(true);tt.setEllipsize(android.text.TextUtils.TruncateAt.END);tt.setPadding(0,dp(2),0,0);words.addView(tt);line.addView(words,new LinearLayout.LayoutParams(0,dp(44),1));card.addView(line,new LinearLayout.LayoutParams(-1,dp(44)));FrameLayout bar=new FrameLayout(this);View track=new View(this);track.setBackground(round(0xff28312d,2));bar.addView(track,new FrameLayout.LayoutParams(-1,dp(4),Gravity.CENTER_VERTICAL));View fill=new View(this);fill.setBackground(round(GREEN,2));FrameLayout.LayoutParams fp=new FrameLayout.LayoutParams(0,dp(4),Gravity.CENTER_VERTICAL);int full=Math.max(dp(40),getResources().getDisplayMetrics().widthPixels-dp(96));fp.width=(int)Math.max(dp(12),Math.min(full,full*(pos/(float)dur)));bar.addView(fill,fp);card.addView(bar,new LinearLayout.LayoutParams(-1,dp(12)));card.setOnClickListener(v->openResolvedContent(source,title,false));LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(-1,dp(72));clp.setMargins(0,dp(6),0,dp(6));host.addView(card,clp);}
 void showMovieActions(JSONObject source,JSONObject detail,String title){String movieId=source.optString("id",detail==null?"":detail.optString("id",""));JSONObject resume=movieResume(movieId);final Dialog d=new Dialog(this);LinearLayout sheet=new LinearLayout(this);sheet.setOrientation(LinearLayout.VERTICAL);sheet.setPadding(dp(18),dp(12),dp(18),dp(18));GradientDrawable sb=round(0xff111713,22);sb.setStroke(dp(1),0xff28352e);sheet.setBackground(sb);View handle=new View(this);handle.setBackground(round(0xff56605b,3));LinearLayout.LayoutParams hp=new LinearLayout.LayoutParams(dp(44),dp(4));hp.gravity=Gravity.CENTER_HORIZONTAL;hp.setMargins(0,0,0,dp(10));sheet.addView(handle,hp);LinearLayout head=new LinearLayout(this);head.setGravity(Gravity.CENTER_VERTICAL);TextView icon=t("▶",18);icon.setTextColor(GREEN);icon.setGravity(Gravity.CENTER);GradientDrawable ib=round(0xff18221d,10);ib.setStroke(dp(1),0xff315b47);icon.setBackground(ib);head.addView(icon,new LinearLayout.LayoutParams(dp(46),dp(46)));LinearLayout htxt=new LinearLayout(this);htxt.setOrientation(LinearLayout.VERTICAL);TextView small=t("Filme",11);small.setTextColor(0xff96a09b);small.setPadding(0,0,0,0);htxt.addView(small);TextView nm=t(title,14);nm.setTypeface(null,1);nm.setSingleLine(true);nm.setEllipsize(android.text.TextUtils.TruncateAt.END);nm.setPadding(0,dp(2),0,0);htxt.addView(nm);LinearLayout.LayoutParams htp=new LinearLayout.LayoutParams(0,dp(48),1);htp.setMargins(dp(12),0,0,0);head.addView(htxt,htp);sheet.addView(head,new LinearLayout.LayoutParams(-1,dp(54)));
  View watch=episodeActionRow("▶",resume!=null?"Continuar Filme":"Assistir Filme",resume!=null?"Retomar de onde parou":"Reproduzir agora");LinearLayout.LayoutParams ap=new LinearLayout.LayoutParams(-1,dp(62));ap.setMargins(0,dp(8),0,0);sheet.addView(watch,ap);View restart=null;if(resume!=null){restart=episodeActionRow("↺","Assistir do início","Recomeçar o filme");LinearLayout.LayoutParams rp=new LinearLayout.LayoutParams(-1,dp(62));rp.setMargins(0,dp(8),0,0);sheet.addView(restart,rp);}View cast=null;if(!isTelevisionDevice()){cast=episodeActionRow("▣","Espelhar na TV","Dispositivos disponíveis");LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(-1,dp(62));clp.setMargins(0,dp(8),0,0);sheet.addView(cast,clp);}View down=episodeActionRow("⇩","Baixar Filme","Disponível sem internet");LinearLayout.LayoutParams dlp=new LinearLayout.LayoutParams(-1,dp(62));dlp.setMargins(0,dp(8),0,0);sheet.addView(down,dlp);watch.setOnClickListener(v->{d.dismiss();openResolvedContent(source,title,false);});if(restart!=null){final View rr=restart;rr.setOnClickListener(v->{clearMovieResume(movieId);d.dismiss();openResolvedContent(source,title,false);});}if(cast!=null)cast.setOnClickListener(v->{Toast.makeText(MainActivity.this,"Nenhum dispositivo disponível.",Toast.LENGTH_SHORT).show();});down.setOnClickListener(v->{d.dismiss();openResolvedContent(source,title,true);});d.setContentView(sheet);Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(Color.TRANSPARENT));w.setDimAmount(.55f);w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);w.setGravity(Gravity.BOTTOM);w.setLayout(-1,-2);}d.setOnShowListener(x->{Window ww=d.getWindow();if(ww!=null){ww.setLayout(-1,-2);ww.setGravity(Gravity.BOTTOM);}if(tvMode){prepareTvFocusTree(sheet);requestTvFocus(watch);}});d.show();}
 JSONArray localMovieContinueItems(){JSONArray out=new JSONArray();String provider=Api.PROVIDER==null?"":Api.PROVIDER;String prefix="movie_resume_"+(provider+"_").replaceAll("[^a-zA-Z0-9._-]","_");java.util.ArrayList<JSONObject> list=new java.util.ArrayList<>();for(java.util.Map.Entry<String,?> e:sp.getAll().entrySet()){if(e.getKey()==null||!e.getKey().startsWith(prefix)||!(e.getValue() instanceof String))continue;try{JSONObject r=new JSONObject((String)e.getValue());long pos=r.optLong("position",0),dur=r.optLong("duration",0);if(pos<4000||dur<=0||pos>=dur-4000)continue;list.add(r);}catch(Exception ignored){}}java.util.Collections.sort(list,(a,b)->Long.compare(b.optLong("updated_at",0),a.optLong("updated_at",0)));for(int i=0;i<Math.min(8,list.size());i++){JSONObject r=list.get(i);JSONObject x=new JSONObject();try{x.put("id",r.optString("movie_id"));x.put("name",r.optString("movie_title","Filme"));x.put("title",r.optString("movie_title","Filme"));x.put("thumbnail",r.optString("movie_poster"));x.put("portrait_img",r.optString("movie_poster"));x.put("landscape",r.optString("movie_landscape"));x.put("landscape_img",r.optString("movie_landscape"));x.put("video_type",1);x.put("type_id",1);x.put("resume_position",r.optLong("position",0));x.put("resume_duration",r.optLong("duration",0));out.put(x);}catch(Exception ignored){}}return out;}
 JSONArray mergeContinueItems(JSONArray server,JSONArray local){JSONArray out=new JSONArray();java.util.HashSet<String> seen=new java.util.HashSet<>();JSONArray[] all={local,server};for(JSONArray a:all){if(a==null)continue;for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;String key=x.optInt("video_type",x.optInt("type_id",1))+"|"+x.optString("id",x.optString("video_id",x.optString("name","")));if(seen.add(key))out.put(x);}}return out;}
 void renderContinueItems(LinearLayout target,JSONArray a){if(target==null||a==null||a.length()==0)return;target.removeAllViews();TextView h=t("Continue assistindo",20);h.setTypeface(null,1);target.addView(h);HorizontalScrollView hs=new HorizontalScrollView(MainActivity.this);hs.setHorizontalScrollBarEnabled(false);LinearLayout r=new LinearLayout(MainActivity.this);r.setOrientation(LinearLayout.HORIZONTAL);hs.addView(r);for(int i=0;i<Math.min(12,a.length());i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;LinearLayout c=card(x);LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(dp(112),dp(202));cp.setMargins(dp(3),0,dp(8),0);r.addView(c,cp);}target.addView(hs,new LinearLayout.LayoutParams(-1,dp(204)));}


 View detailPrimaryAction(String label){
  LinearLayout box=new LinearLayout(this);box.setGravity(Gravity.CENTER_VERTICAL);box.setPadding(dp(18),0,dp(18),0);GradientDrawable g=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{0xff22e776,0xff53ee8d});g.setCornerRadius(dp(22));g.setStroke(dp(1),0xff76f5a3);box.setBackground(g);box.setElevation(dp(3));
  TextView play=t("▶",21);play.setTextColor(0xff041109);play.setGravity(Gravity.CENTER);box.addView(play,new LinearLayout.LayoutParams(dp(54),-1));TextView txt=t(label,20);txt.setTextColor(0xff041109);txt.setTypeface(null,1);txt.setGravity(Gravity.CENTER);box.addView(txt,new LinearLayout.LayoutParams(0,-1,1));TextView ar=t("›",30);ar.setTextColor(0xff041109);ar.setGravity(Gravity.CENTER);box.addView(ar,new LinearLayout.LayoutParams(dp(42),-1));return box;
 }
 View detailSecondaryAction(String label){
  LinearLayout box=new LinearLayout(this);box.setGravity(Gravity.CENTER);GradientDrawable g=round(0xaa0b1511,20);g.setStroke(dp(1),0xff42c77d);box.setBackground(g);TextView ic=t("⇩",20);ic.setTextColor(0xffeef4f0);ic.setGravity(Gravity.CENTER);box.addView(ic,new LinearLayout.LayoutParams(dp(44),-1));TextView txt=t(label,16);txt.setTextColor(0xfff4f6f5);txt.setTypeface(null,1);txt.setGravity(Gravity.CENTER_VERTICAL);box.addView(txt,new LinearLayout.LayoutParams(-2,-1));return box;
 }
 void showDetailBottomNav(){
  if(contentFrame==null)return;if(detailNavOverlay!=null&&detailNavOverlay.getParent() instanceof ViewGroup)((ViewGroup)detailNavOverlay.getParent()).removeView(detailNavOverlay);
  detailNavOverlay=new LinearLayout(this);detailNavOverlay.setGravity(Gravity.CENTER);detailNavOverlay.setPadding(dp(4),dp(4),dp(4),dp(2));GradientDrawable bg=round(0xf20a120e,18);bg.setStroke(dp(1),0xff173528);detailNavOverlay.setBackground(bg);detailNavOverlay.setElevation(dp(9));
  detailNavOverlay.addView(detailBottomNavItem("⌂","Início",false,v->{closeDetails();if(navHome!=null)navHome.performClick();}),new LinearLayout.LayoutParams(0,-1,1));
  detailNavOverlay.addView(detailBottomNavItem("⌕","Buscar",false,v->{closeDetails();searchDialog();}),new LinearLayout.LayoutParams(0,-1,1));
  detailNavOverlay.addView(detailBottomNavItem("▶","GreenPlay",true,v->{closeDetails();if(navHome!=null)navHome.performClick();}),new LinearLayout.LayoutParams(0,-1,1));
  detailNavOverlay.addView(detailBottomNavItem("♡","Minha Lista",false,v->{closeDetails();if(navFav!=null)navFav.performClick();}),new LinearLayout.LayoutParams(0,-1,1));
  detailNavOverlay.addView(detailBottomNavItem("♙","Perfil",false,v->{closeDetails();if(navProfile!=null)navProfile.performClick();}),new LinearLayout.LayoutParams(0,-1,1));
  FrameLayout.LayoutParams lp=new FrameLayout.LayoutParams(-1,dp(62),Gravity.BOTTOM);lp.setMargins(0,0,0,0);contentFrame.addView(detailNavOverlay,lp);
 }
 View detailBottomNavItem(String icon,String label,boolean active,View.OnClickListener click){LinearLayout item=new LinearLayout(this);item.setOrientation(LinearLayout.VERTICAL);item.setGravity(Gravity.CENTER);TextView ic=t(icon,active?18:17);ic.setGravity(Gravity.CENTER);ic.setTextColor(active?0xff041109:0xffbec8c3);if(active){GradientDrawable cg=round(GREEN,18);ic.setBackground(cg);item.addView(ic,new LinearLayout.LayoutParams(dp(34),dp(34)));}else item.addView(ic,new LinearLayout.LayoutParams(dp(34),dp(30)));TextView tx=t(label,10);tx.setGravity(Gravity.CENTER);tx.setTextColor(active?GREEN:0xffb4beb9);tx.setTypeface(null,active?1:0);tx.setPadding(0,0,0,0);item.addView(tx,new LinearLayout.LayoutParams(-1,dp(20)));item.setOnClickListener(click);return item;}
 void closeDetails(){
  if(!detailOpen)return;
  viewGen=savedViewGen;
  ScrollView detailScroll=mainScroll;
  if(contentFrame!=null&&detailScroll!=null)contentFrame.removeView(detailScroll);
  if(detailNavOverlay!=null&&detailNavOverlay.getParent() instanceof ViewGroup)((ViewGroup)detailNavOverlay.getParent()).removeView(detailNavOverlay);detailNavOverlay=null;
  mainScroll=savedScroll;body=savedBody;savedScroll=null;savedBody=null;detailOpen=false;activeSeriesResumeHost=null;activeSeriesDetail=null;activeSeriesSource=null;
  if(root!=null)root.setPadding(dp(18),dp(18),dp(18),dp(12));
  if(navBar!=null)navBar.setVisibility(View.VISIBLE);
  if(mainScroll!=null){mainScroll.setVisibility(View.VISIBLE);mainScroll.post(()->mainScroll.requestLayout());}
  setNav(savedNavIndex);
 }
 @Override public void onBackPressed(){
  if(providerSwitchScreen){cancelProviderSwitch();return;}
  if(detailOpen){closeDetails();return;}
  if(searchScreenOpen){closeSearchScreen();return;}
  if(plansScreen){profile();return;}
  if(uid!=null&&!uid.isEmpty()&&contentFrame!=null){
   // Nunca fecha o app a partir de uma tela interna. Primeiro volta para a Home.
   if(currentNavIndex!=0){restoreHomeView();return;}
   if(mainScroll!=homeScrollCache){restoreHomeView();return;}
   // Se estiver em Filmes/Séries/categoria do topo, volta primeiro para Início.
   if(!"Recomendações".equals(activeHomeTab)){home();return;}
   showExitConfirm();return;
  }
  super.onBackPressed();
 }
 Button detailPrimaryButton(String s){Button b=new Button(this);b.setText(s);b.setTextColor(0xff031109);b.setTextSize(19);b.setTypeface(null,1);b.setAllCaps(false);GradientDrawable g=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{0xff20dc6d,0xff54f08d});g.setCornerRadius(dp(22));g.setStroke(dp(1),0xff76f5a3);b.setBackground(g);b.setElevation(dp(3));b.setFocusable(true);return b;}
 Button detailOutlineButton(String s){Button b=new Button(this);b.setText(s);b.setTextColor(0xfff2f5f3);b.setTextSize(16);b.setTypeface(null,1);b.setAllCaps(false);GradientDrawable g=new GradientDrawable();g.setColor(0xdd0d1713);g.setCornerRadius(dp(20));g.setStroke(dp(1),0xff3f705b);b.setBackground(g);b.setFocusable(true);return b;}
 String formatRatingDisplay(String raw){try{double v=Double.parseDouble(raw.replace(",","."));return String.format(java.util.Locale.US,"%.1f",v);}catch(Exception e){return raw;}}
 String formatDurationDisplay(String raw){if(raw==null)return "";String s=raw.trim().toLowerCase(java.util.Locale.ROOT);if(s.isEmpty())return "";try{long total=-1;if(s.contains(":")){String[] p=s.split(":");if(p.length>=3){long h=Long.parseLong(p[p.length-3].replaceAll("[^0-9]",""));long m=Long.parseLong(p[p.length-2].replaceAll("[^0-9]",""));total=h*60+m;}else if(p.length==2){long a=Long.parseLong(p[0].replaceAll("[^0-9]",""));long b=Long.parseLong(p[1].replaceAll("[^0-9]",""));total=a*60+b;}}if(total<0){java.util.regex.Matcher mh=java.util.regex.Pattern.compile("(\\d+)\\s*h").matcher(s);java.util.regex.Matcher mm=java.util.regex.Pattern.compile("(\\d+)\\s*(?:min|m)").matcher(s);long h=mh.find()?Long.parseLong(mh.group(1)):0;long min=mm.find()?Long.parseLong(mm.group(1)):0;if(h>0||min>0)total=h*60+min;}if(total<0){String digits=s.replaceAll("[^0-9]","");if(!digits.isEmpty())total=Long.parseLong(digits);}if(total>=0){long h=total/60,mn=total%60;if(h>0)return mn>0?h+"h "+mn+"min":h+"h";return mn+" min";}}catch(Exception ignored){}return raw;}
 View detailIdBadge(String s){TextView v=t(s,12);v.setTypeface(null,1);v.setTextColor(GREEN);v.setPadding(dp(11),dp(6),dp(11),dp(6));GradientDrawable g=round(0x2417d86b,12);g.setStroke(dp(1),0x6635dc7b);v.setBackground(g);return v;}
 View detailMetaItem(String icon,String value,int iconColor){LinearLayout box=new LinearLayout(this);box.setGravity(Gravity.CENTER_VERTICAL);TextView ic=t(icon,14);ic.setTextColor(iconColor);box.addView(ic);TextView txt=t(value,14);txt.setTextColor(0xffe0e5e2);txt.setPadding(dp(6),0,dp(8),0);box.addView(txt);return box;}
 View detailMetaDivider(){View d=new View(this);d.setBackgroundColor(0xff33433c);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(dp(1),dp(18));lp.setMargins(dp(4),0,dp(10),0);d.setLayoutParams(lp);return d;}
 TextView detailSectionTitle(String label){TextView v=t(label,22);v.setTypeface(null,1);v.setTextColor(Color.WHITE);v.setPadding(0,0,0,dp(10));return v;}
 GradientDrawable detailGlassCircle(){GradientDrawable g=round(0x6a0b1511,24);g.setStroke(dp(1),0x553f705b);return g;}
 View castPerson(JSONObject ca){
  LinearLayout box=new LinearLayout(this);box.setOrientation(LinearLayout.VERTICAL);box.setGravity(Gravity.CENTER_HORIZONTAL);
  String name=ca.optString("name",ca.optString("original_name",""));
  String photo=ca.optString("photo",ca.optString("profile",ca.optString("profile_path",ca.optString("image",ca.optString("avatar","")))));photo=normalizeTmdbPersonPhoto(photo);
  FrameLayout avatar=new FrameLayout(this);GradientDrawable bg=round(0xff17221d,48);bg.setStroke(dp(1),0xff3d6655);avatar.setBackground(bg);avatar.setClipToOutline(true);avatar.setElevation(dp(2));
  TextView initials=t(personInitials(name),18);initials.setTypeface(null,1);initials.setTextColor(0xff8aa598);initials.setGravity(Gravity.CENTER);avatar.addView(initials,new FrameLayout.LayoutParams(-1,-1));
  if(!photo.isEmpty()){ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);im.setAdjustViewBounds(false);Img.loadVisible(im,photo);avatar.addView(im,new FrameLayout.LayoutParams(-1,-1));}
  box.addView(avatar,new LinearLayout.LayoutParams(dp(94),dp(94)));
  TextView n=t(name,12);n.setGravity(Gravity.CENTER);n.setTextColor(0xfff0f3f1);n.setMaxLines(1);n.setEllipsize(android.text.TextUtils.TruncateAt.END);n.setPadding(0,dp(7),0,0);box.addView(n,new LinearLayout.LayoutParams(dp(126),dp(28)));
  LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(dp(126),dp(132));lp.setMargins(0,0,dp(10),0);box.setLayoutParams(lp);return box;
 }
 String normalizeTmdbPersonPhoto(String photo){if(photo==null)return "";String x=photo.trim();if(x.isEmpty()||"null".equalsIgnoreCase(x))return "";if(x.startsWith("//"))return "https:"+x;if(x.startsWith("http://image.tmdb.org"))return "https://image.tmdb.org"+x.substring("http://image.tmdb.org".length());if(x.startsWith("https://"))return x;if(x.startsWith("http://"))return x;if(x.startsWith("/"))return "https://image.tmdb.org/t/p/w342"+x;if(x.startsWith("profile/"))x=x.substring(8);if(x.startsWith("t/p/"))return "https://image.tmdb.org/"+x;if(x.matches("[A-Za-z0-9_\\-]+\\.(jpg|jpeg|png|webp)"))return "https://image.tmdb.org/t/p/w342/"+x;return x;}
 String personInitials(String name){if(name==null||name.trim().isEmpty())return "•";String[] p=name.trim().split("\\s+");String a=p[0].substring(0,1);String b=p.length>1?p[p.length-1].substring(0,1):"";return (a+b).toUpperCase(java.util.Locale.getDefault());}
 boolean validTmdbId(String raw){if(raw==null)return false;String d=raw.replaceAll("[^0-9]","");if(d.isEmpty())return false;try{return Long.parseLong(d)>0;}catch(Exception e){return false;}}
 TextView chip(String s){TextView c=t(s,12);c.setTextColor(0xffdfe5e1);c.setGravity(Gravity.CENTER);GradientDrawable g=round(0xff17231e,14);g.setStroke(dp(1),0xff30463c);c.setBackground(g);c.setPadding(dp(13),0,dp(13),0);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-2,dp(32));lp.setMargins(0,0,dp(7),0);c.setLayoutParams(lp);return c;}
 boolean isFav(JSONObject x){try{JSONArray a=new JSONArray(sp.getString("favs","[]"));String id=x.optString("id");for(int i=0;i<a.length();i++){JSONObject y=a.optJSONObject(i);if(y!=null&&id.equals(y.optString("id")))return true;}}catch(Exception ignored){}return false;}
 JSONArray offlineArray(){try{return new JSONArray(sp.getString("offline_items","[]"));}catch(Exception e){return new JSONArray();}}
 void saveOfflineArray(JSONArray a){sp.edit().putString("offline_items",a.toString()).apply();}
 JSONObject offlineItemById(String contentId){JSONArray a=offlineArray();for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o!=null&&contentId.equals(o.optString("content_id")))return o;}return null;}
 void downloadOffline(JSONObject source,String url,String name,String poster,String contentId,String videoType){
  JSONArray urls=new JSONArray();java.util.HashSet<String> seen=new java.util.HashSet<>();addOfflineUrl(urls,seen,url);if(source!=null){String[] keys={"video_1080","video_720","video_480","video_320","video_url","stream_url","url"};for(String k:keys)addOfflineUrl(urls,seen,source.optString(k,""));}downloadOfflineUrls(urls,name,poster,contentId,videoType,null);
 }
 void downloadOffline(String url,String name,String poster,String contentId,String videoType){JSONArray urls=new JSONArray();addOfflineUrl(urls,new java.util.HashSet<String>(),url);downloadOfflineUrls(urls,name,poster,contentId,videoType,null);}
 void addOfflineUrl(JSONArray urls,java.util.HashSet<String> seen,String url){if(url==null)return;String u=url.trim();if(u.isEmpty()||!seen.add(u))return;urls.put(u);}
 void downloadOfflineUrls(JSONArray urls,String name,String poster,String contentId,String videoType,String existingPath){
  try{
   if(urls==null||urls.length()==0){Toast.makeText(this,"Conteúdo indisponível para download.",Toast.LENGTH_SHORT).show();return;}
   java.io.File dir=new java.io.File(getFilesDir(),"offline");if(!dir.exists()&&!dir.mkdirs()){Toast.makeText(this,"Armazenamento indisponível.",1).show();return;}
   String primary=urls.optString(0,"");String ext=offlineExtension(primary);String safe=(videoType+"_"+contentId+"_"+name).replaceAll("[^a-zA-Z0-9._-]","_");if(!safe.endsWith(ext))safe+=ext;java.io.File dest=(existingPath==null||existingPath.isEmpty())?new java.io.File(dir,safe):new java.io.File(existingPath);
   JSONArray a=offlineArray();for(int i=a.length()-1;i>=0;i--){JSONObject old=a.optJSONObject(i);if(old!=null&&contentId.equals(old.optString("content_id"))&&videoType.equals(old.optString("video_type","1")))a.remove(i);}JSONObject o=new JSONObject();o.put("content_id",contentId);o.put("video_type",videoType);o.put("title",name);o.put("poster",poster);o.put("path",dest.getAbsolutePath());o.put("source_url",primary);o.put("source_urls",urls);o.put("status","queued");o.put("downloaded",0);o.put("total",0);o.put("created_at",System.currentTimeMillis());a.put(o);saveOfflineArray(a);
   startOfflineService(o);Toast.makeText(this,"Preparando download.",Toast.LENGTH_SHORT).show();
  }catch(Exception e){Toast.makeText(this,"Não foi possível iniciar o download.",1).show();}
 }
 String offlineExtension(String url){try{String p=android.net.Uri.parse(url).getPath();if(p!=null){String l=p.toLowerCase(java.util.Locale.ROOT);String[] exts={".mp4",".mkv",".webm",".avi",".mov",".m4v",".ts"};for(String e:exts)if(l.endsWith(e))return e;}}catch(Exception ignored){}return ".mp4";}
 void startOfflineService(JSONObject o){try{Intent it=new Intent(this,OfflineDownloadService.class);it.setAction(OfflineDownloadService.ACTION_START);it.putExtra("url",o.optString("source_url",""));JSONArray urls=o.optJSONArray("source_urls");it.putExtra("urls",urls==null?"":urls.toString());it.putExtra("title",o.optString("title","Conteúdo"));it.putExtra("poster",o.optString("poster",""));it.putExtra("content_id",o.optString("content_id","0"));it.putExtra("video_type",o.optString("video_type","1"));it.putExtra("path",o.optString("path",""));if(Build.VERSION.SDK_INT>=26)startForegroundService(it);else startService(it);}catch(Exception e){Toast.makeText(this,"Não foi possível iniciar o download.",Toast.LENGTH_SHORT).show();}}
 void retryOffline(JSONObject old){if(old==null)return;try{JSONArray urls=old.optJSONArray("source_urls");if(urls==null||urls.length()==0){urls=new JSONArray();String u=old.optString("source_url","");if(!u.isEmpty())urls.put(u);}downloadOfflineUrls(urls,old.optString("title","Conteúdo"),old.optString("poster",""),old.optString("content_id","0"),old.optString("video_type","1"),old.optString("path",""));}catch(Exception ignored){}}
 String offlineStateText(JSONObject o){String st=o.optString("status","queued");long done=o.optLong("downloaded",0),total=o.optLong("total",0);if("ready".equals(st))return "Pronto para assistir";if("downloading".equals(st)){if(total>0)return "Baixando "+Math.min(100,(int)(100*done/total))+"%";return "Baixando";}if("queued".equals(st))return "Preparando download";if("failed".equals(st))return "Não foi possível baixar · toque para tentar";return "Preparando download";}
 void removeOffline(int index,JSONObject o){try{String cid=o.optString("content_id","");Intent it=new Intent(this,OfflineDownloadService.class);it.setAction(OfflineDownloadService.ACTION_CANCEL);it.putExtra("content_id",cid);it.putExtra("path",o.optString("path",""));startService(it);String path=o.optString("path","");if(!path.isEmpty()){new java.io.File(path).delete();new java.io.File(path+".part").delete();}JSONArray a=offlineArray();for(int i=a.length()-1;i>=0;i--){JSONObject x=a.optJSONObject(i);if(x!=null&&cid.equals(x.optString("content_id")))a.remove(i);}saveOfflineArray(a);downloads();}catch(Exception e){Toast.makeText(this,"Não foi possível excluir",1).show();}}
 View offlineCard(JSONObject snapshot,int index){
  String cid=snapshot.optString("content_id","");JSONObject current=offlineItemById(cid);final JSONObject o=current!=null?current:snapshot;
  LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER_VERTICAL);card.setPadding(dp(8),dp(8),dp(10),dp(8));card.setBackground(round(0xff141c18,14));ImageView poster=new ImageView(this);poster.setScaleType(ImageView.ScaleType.CENTER_CROP);poster.setClipToOutline(true);poster.setBackground(round(0xff102018,10));Img.load(poster,o.optString("poster",""));card.addView(poster,new LinearLayout.LayoutParams(dp(62),dp(86)));
  LinearLayout mid=new LinearLayout(this);mid.setOrientation(LinearLayout.VERTICAL);mid.setPadding(dp(12),0,dp(4),0);TextView title=t(o.optString("title","Conteúdo offline"),15);title.setTypeface(null,1);title.setMaxLines(2);mid.addView(title);String st=o.optString("status","queued");TextView sub=t(offlineStateText(o),13);sub.setTextColor("ready".equals(st)?GREEN:0xff9ca6a1);mid.addView(sub);card.addView(mid,new LinearLayout.LayoutParams(0,-2,1));TextView arrow=t("ready".equals(st)?"▶":"⋮",22);arrow.setGravity(Gravity.CENTER);arrow.setTextColor("ready".equals(st)?GREEN:0xff9ca6a1);card.addView(arrow,new LinearLayout.LayoutParams(dp(40),dp(72)));
  card.setOnClickListener(v->{JSONObject fresh=offlineItemById(cid);if(fresh==null)return;String state=fresh.optString("status","");java.io.File f=new java.io.File(fresh.optString("path",""));if("ready".equals(state)&&f.exists()){Intent in=new Intent(MainActivity.this,PlayerActivity.class);in.putExtra("url",f.getAbsolutePath());in.putExtra("title",fresh.optString("title","Offline"));in.putExtra("offline",true);startActivity(in);}else if("failed".equals(state)){retryOffline(fresh);}else Toast.makeText(MainActivity.this,"Download em andamento.",0).show();});
  card.setOnLongClickListener(v->{new AlertDialog.Builder(MainActivity.this).setTitle("Excluir download offline?").setMessage(o.optString("title","")).setNegativeButton("Cancelar",null).setPositiveButton("Excluir",(d,w)->removeOffline(index,o)).show();return true;});LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(102));lp.setMargins(0,0,0,dp(8));card.setLayoutParams(lp);return card;
 }
 boolean hasActiveOfflineDownloads(){JSONArray a=offlineArray();for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o==null)continue;String st=o.optString("status","");if("queued".equals(st)||"downloading".equals(st))return true;}return false;}
 void downloads(){clear();setNav(3);final int gen=viewGen;pageTitle("Downloads",()->home());TextView title=t("Downloads",22);title.setTypeface(null,1);body.addView(title);TextView info=t("Assista seus downloads mesmo sem internet.",14);info.setTextColor(0xff9ca6a1);info.setPadding(dp(8),0,dp(8),dp(12));body.addView(info);JSONArray a=offlineArray();if(a.length()==0){TextView empty=t("Nenhum download por enquanto.",15);empty.setTextColor(0xff8f9994);body.addView(empty);return;}for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o!=null)body.addView(offlineCard(o,i));}if(hasActiveOfflineDownloads())new Handler(Looper.getMainLooper()).postDelayed(()->{if(gen==viewGen&&currentNavIndex==3&&!detailOpen)downloads();},1200);}
 void searchDialog(){openSearchScreen();}
 void openSearchScreen(){
  if(detailOpen)closeDetails();
  if(mainScroll==homeScrollCache)leaveHomeForPage();else createTransientPageHost();
  searchScreenOpen=true;clear();setNav(0);
  // v16.75: barra ativa mantém exatamente a geometria da barra da Home,
  // usando componentes simples já presentes no projeto para máxima compatibilidade de compilação.
  body.setPadding(0,0,0,dp(18));

  LinearLayout topWrap=new LinearLayout(this);topWrap.setOrientation(LinearLayout.VERTICAL);topWrap.setPadding(0,dp(34),0,0);
  LinearLayout top=new LinearLayout(this);top.setGravity(Gravity.CENTER_VERTICAL);top.setPadding(0,0,0,0);

  LinearLayout backSlot=new LinearLayout(this);backSlot.setGravity(Gravity.CENTER);backSlot.setPadding(0,0,0,0);
  TextView back=t("‹",32);back.setGravity(Gravity.CENTER);back.setTextColor(Color.WHITE);back.setPadding(0,0,0,0);GradientDrawable bb=round(0xff111a16,18);bb.setStroke(dp(1),0xff2b3b33);back.setBackground(bb);back.setOnClickListener(v->closeSearchScreen());backSlot.addView(back,new LinearLayout.LayoutParams(dp(36),dp(36)));
  LinearLayout.LayoutParams backLp=new LinearLayout.LayoutParams(dp(56),dp(36));backLp.setMargins(0,0,dp(9),0);top.addView(backSlot,backLp);

  LinearLayout box=new LinearLayout(this);box.setGravity(Gravity.CENTER_VERTICAL);box.setPadding(dp(13),0,dp(5),0);GradientDrawable bg=round(0xff292b2c,21);bg.setStroke(dp(1),0xff444748);box.setBackground(bg);
  EditText q=new EditText(this);q.setHint("Buscar");q.setHintTextColor(0xffaeb2b4);q.setTextColor(Color.WHITE);q.setTextSize(14);q.setSingleLine(true);q.setPadding(0,0,0,0);q.setBackgroundColor(Color.TRANSPARENT);q.setImeOptions(android.view.inputmethod.EditorInfo.IME_ACTION_SEARCH);box.addView(q,new LinearLayout.LayoutParams(0,dp(38),1));
  TextView icon=t("⌕",22);icon.setTextColor(Color.WHITE);icon.setGravity(Gravity.CENTER);icon.setPadding(0,0,0,0);box.addView(icon,new LinearLayout.LayoutParams(dp(34),dp(38)));top.addView(box,new LinearLayout.LayoutParams(0,dp(38),1));
  topWrap.addView(top,new LinearLayout.LayoutParams(-1,dp(38)));body.addView(topWrap,new LinearLayout.LayoutParams(-1,dp(72)));

  LinearLayout results=new LinearLayout(this);results.setOrientation(LinearLayout.VERTICAL);body.addView(results,new LinearLayout.LayoutParams(-1,-2));
  renderSearchResults("",results);
  final Runnable doSearch=()->renderSearchResults(q.getText().toString(),results);
  q.addTextChangedListener(new android.text.TextWatcher(){public void beforeTextChanged(CharSequence s,int st,int c,int a){}public void onTextChanged(CharSequence s,int st,int before,int count){results.removeCallbacks(doSearch);results.postDelayed(doSearch,120);}public void afterTextChanged(android.text.Editable e){}});
  q.setOnEditorActionListener((v,action,event)->{if(action==android.view.inputmethod.EditorInfo.IME_ACTION_SEARCH){renderSearchResults(q.getText().toString(),results);return true;}return false;});
  icon.setOnClickListener(v->{renderSearchResults(q.getText().toString(),results);q.requestFocus();});
  q.requestFocus();q.postDelayed(()->{try{android.view.inputmethod.InputMethodManager im=(android.view.inputmethod.InputMethodManager)getSystemService(INPUT_METHOD_SERVICE);im.showSoftInput(q,android.view.inputmethod.InputMethodManager.SHOW_IMPLICIT);}catch(Exception ignored){}},120);
 }
 void closeSearchScreen(){
  searchScreenOpen=false;try{android.view.inputmethod.InputMethodManager im=(android.view.inputmethod.InputMethodManager)getSystemService(INPUT_METHOD_SERVICE);View f=getCurrentFocus();if(im!=null&&f!=null)im.hideSoftInputFromWindow(f.getWindowToken(),0);}catch(Exception ignored){}
  restoreHomeView();
 }
 JSONArray localSearchResults(String q){
  JSONArray out=new JSONArray();String needle=q==null?"":q.trim().toLowerCase(java.util.Locale.ROOT);if(needle.length()<2)return out;JSONObject prepared=readHomeCache();if(prepared==null)return out;java.util.HashSet<String> seen=new java.util.HashSet<>();JSONArray secs=prepared.optJSONArray("result");if(secs==null)return out;
  for(int i=0;i<secs.length()&&out.length()<72;i++){JSONObject sec=secs.optJSONObject(i);if(sec==null)continue;JSONArray d=sec.optJSONArray("data");if(d==null)continue;for(int k=0;k<d.length()&&out.length()<72;k++){JSONObject x=d.optJSONObject(k);if(x==null)continue;String name=x.optString("name",x.optString("title","")).toLowerCase(java.util.Locale.ROOT);if(!name.contains(needle))continue;String key=x.optInt("video_type",x.optInt("type_id",1))+"|"+x.optString("id",x.optString("video_id",""));if(seen.add(key))out.put(x);}}
  return out;
 }
 void renderSearchResults(String query,LinearLayout host){
  if(host==null)return;host.removeAllViews();String q=query==null?"":query.trim();
  if(q.length()<2){TextView hint=t("Digite pelo menos 2 letras para buscar.",14);hint.setTextColor(0xff8f9994);hint.setPadding(dp(4),dp(18),dp(4),0);host.addView(hint);return;}
  JSONArray a=localSearchResults(q);TextView title=t(a.length()>0?"Resultados":"Nenhum resultado encontrado",19);title.setTypeface(null,1);title.setPadding(dp(2),dp(10),dp(2),dp(10));host.addView(title);
  if(a.length()==0)return;
  GridLayout g=new GridLayout(this);g.setColumnCount(3);g.setUseDefaultMargins(false);host.addView(g,new LinearLayout.LayoutParams(-1,-2));int w=(getResources().getDisplayMetrics().widthPixels-dp(52))/3;
  for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;LinearLayout c=card(x);GridLayout.LayoutParams lp=new GridLayout.LayoutParams();lp.width=w;lp.height=dp(196);lp.setMargins(dp(3),dp(4),dp(5),dp(8));g.addView(c,lp);}
 }
 void search(String q){
  if(searchScreenOpen){return;}
  openSearchScreen();
 }
 void showExitConfirm(){
  if(exitDialogOpen)return;exitDialogOpen=true;
  showAppConfirm("Sair do aplicativo?","Deseja realmente fechar o GreenPlay?","Sair",true,()->finishAffinity(),()->exitDialogOpen=false);
 }
 void showLogoutConfirm(){showAppConfirm("Sair da conta?","Você precisará entrar novamente para acessar o GreenPlay.","Sair da conta",true,()->{sp.edit().clear().apply();uid="";login();},null);}
 void showDeleteConfirm(){showAppConfirm("Excluir conta","Esta ação precisa ser confirmada antes de continuar.","Continuar",true,()->showAppNotice("Solicitação ainda não enviada",true),null);}
 void showAppConfirm(String titleText,String messageText,String positiveText,boolean danger,Runnable positiveAction,Runnable onDismiss){
  final Dialog d=new Dialog(this);LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setPadding(dp(22),dp(20),dp(22),dp(18));GradientDrawable cb=round(0xff0d1712,24);cb.setStroke(dp(1),0xff294839);card.setBackground(cb);
  LinearLayout head=new LinearLayout(this);head.setGravity(Gravity.CENTER_VERTICAL);TextView mark=t(danger?"!":"✓",18);mark.setGravity(Gravity.CENTER);mark.setTypeface(null,1);mark.setPadding(0,0,0,0);mark.setTextColor(danger?0xffff6a70:GREEN);GradientDrawable mb=round(danger?0x332b1114:0x3320e070,18);mb.setStroke(dp(1),danger?0x66ff5b63:0x6620e070);mark.setBackground(mb);head.addView(mark,new LinearLayout.LayoutParams(dp(36),dp(36)));TextView title=t(titleText,22);title.setTypeface(null,1);title.setPadding(dp(12),0,0,0);head.addView(title,new LinearLayout.LayoutParams(0,dp(42),1));card.addView(head);
  TextView msg=t(messageText,15);msg.setTextColor(0xffaeb7b2);msg.setPadding(0,dp(12),0,dp(22));card.addView(msg);
  LinearLayout actions=new LinearLayout(this);actions.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);TextView cancel=t("Cancelar",15);cancel.setTextColor(0xffc7ceca);cancel.setTypeface(null,1);cancel.setGravity(Gravity.CENTER);cancel.setPadding(0,0,0,0);GradientDrawable cancelBg=round(0xff17231d,14);cancelBg.setStroke(dp(1),0xff304339);cancel.setBackground(cancelBg);actions.addView(cancel,new LinearLayout.LayoutParams(dp(116),dp(50)));TextView ok=t(positiveText,15);ok.setTextColor(danger?Color.WHITE:0xff061109);ok.setTypeface(null,1);ok.setGravity(Gravity.CENTER);ok.setPadding(dp(10),0,dp(10),0);GradientDrawable okBg=round(danger?0xffb9343d:GREEN,14);okBg.setStroke(dp(1),danger?0xffd94a52:GREEN);ok.setBackground(okBg);LinearLayout.LayoutParams op=new LinearLayout.LayoutParams(0,dp(50),1);op.setMargins(dp(10),0,0,0);actions.addView(ok,op);card.addView(actions,new LinearLayout.LayoutParams(-1,dp(50)));
  cancel.setOnClickListener(v->d.dismiss());ok.setOnClickListener(v->{d.dismiss();if(positiveAction!=null)positiveAction.run();});d.setContentView(card);Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));w.setDimAmount(.72f);w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);w.setGravity(Gravity.CENTER);}d.setOnDismissListener(x->{if(onDismiss!=null)onDismiss.run();});d.setOnShowListener(x->{Window ww=d.getWindow();if(ww!=null)ww.setLayout(Math.min(getResources().getDisplayMetrics().widthPixels-dp(38),dp(500)),-2);if(tvMode){prepareTvFocusTree(card);requestTvFocus(cancel);}});d.show();
 }
 void showAppNotice(String message,boolean error){
  final Dialog d=new Dialog(this);LinearLayout box=new LinearLayout(this);box.setGravity(Gravity.CENTER_VERTICAL);box.setPadding(dp(16),dp(12),dp(16),dp(12));GradientDrawable bg=round(0xff102018,16);bg.setStroke(dp(1),error?0x99d65259:0x9920e070);box.setBackground(bg);TextView dot=t(error?"!":"✓",15);dot.setTypeface(null,1);dot.setGravity(Gravity.CENTER);dot.setTextColor(error?0xffff7379:GREEN);dot.setPadding(0,0,0,0);box.addView(dot,new LinearLayout.LayoutParams(dp(28),dp(28)));TextView txt=t(message,14);txt.setTextColor(Color.WHITE);txt.setPadding(dp(10),0,0,0);box.addView(txt,new LinearLayout.LayoutParams(0,-2,1));d.setContentView(box);Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));w.clearFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);w.setGravity(Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);}d.setOnShowListener(x->{Window ww=d.getWindow();if(ww!=null){ww.setLayout(Math.min(getResources().getDisplayMetrics().widthPixels-dp(42),dp(460)),-2);WindowManager.LayoutParams lp=ww.getAttributes();lp.y=dp(90);ww.setAttributes(lp);}});d.show();new Handler(Looper.getMainLooper()).postDelayed(()->{try{if(d.isShowing())d.dismiss();}catch(Exception ignored){}},1500);
 }
 void toggleFav(JSONObject x){try{JSONArray a=new JSONArray(sp.getString("favs","[]"));for(int i=0;i<a.length();i++)if(a.optJSONObject(i).optInt("id")==x.optInt("id")){a.remove(i);sp.edit().putString("favs",a.toString()).apply();Toast.makeText(this,"Removido dos favoritos",0).show();return;}a.put(x);sp.edit().putString("favs",a.toString()).apply();Toast.makeText(this,"Adicionado aos favoritos",0).show();}catch(Exception ignored){}}
 void favorites(){clear();setNav(1);pageTitle("Favoritos",()->home());try{row(new JSONArray(sp.getString("favs","[]")));}catch(Exception ignored){}}
 void profile(){plansScreen=false;if(navBar!=null)navBar.setVisibility(View.VISIBLE);clear();setNav(4);
  // v16.77: Perfil redesenhado seguindo a composição da referência enviada.
  // Mantém as funções reais do GreenPlay e a identidade verde do painel.
  LinearLayout top=new LinearLayout(this);top.setGravity(Gravity.CENTER_VERTICAL);top.setPadding(dp(2),dp(8),0,dp(12));
  TextView profileIcon=t("♙",27);profileIcon.setTextColor(GREEN);profileIcon.setGravity(Gravity.CENTER);profileIcon.setPadding(0,0,0,0);top.addView(profileIcon,new LinearLayout.LayoutParams(dp(50),dp(54)));
  TextView title=t("Perfil",29);title.setTypeface(null,1);title.setPadding(dp(4),0,0,0);title.setGravity(Gravity.CENTER_VERTICAL);top.addView(title,new LinearLayout.LayoutParams(0,dp(54),1));
  TextView logout=t("↪",30);logout.setTextColor(0xffff555f);logout.setGravity(Gravity.CENTER);logout.setPadding(0,0,0,0);top.addView(logout,new LinearLayout.LayoutParams(dp(52),dp(54)));logout.setOnClickListener(v->showLogoutConfirm());body.addView(top,new LinearLayout.LayoutParams(-1,dp(74)));

  // Cartão do usuário
  LinearLayout person=new LinearLayout(this);person.setGravity(Gravity.CENTER_VERTICAL);person.setPadding(dp(16),dp(14),dp(16),dp(14));GradientDrawable personBg=round(0xff111a16,22);personBg.setStroke(dp(1),0xff1e3128);person.setBackground(personBg);person.setOnClickListener(v->editAccount());
  FrameLayout avatarWrap=new FrameLayout(this);TextView avatar=t("●",36);avatar.setTextColor(Color.WHITE);avatar.setGravity(Gravity.CENTER);avatar.setPadding(0,0,0,0);GradientDrawable avBg=round(0xff0d8f45,38);avBg.setStroke(dp(1),GREEN);avatar.setBackground(avBg);avatarWrap.addView(avatar,new FrameLayout.LayoutParams(dp(72),dp(72)));TextView cam=t("▣",13);cam.setGravity(Gravity.CENTER);cam.setTextColor(Color.WHITE);cam.setPadding(0,0,0,0);GradientDrawable camBg=round(GREEN,13);camBg.setStroke(dp(2),0xff0a1610);cam.setBackground(camBg);FrameLayout.LayoutParams cp=new FrameLayout.LayoutParams(dp(27),dp(27),Gravity.RIGHT|Gravity.BOTTOM);avatarWrap.addView(cam,cp);person.addView(avatarWrap,new LinearLayout.LayoutParams(dp(78),dp(78)));
  LinearLayout who=new LinearLayout(this);who.setOrientation(LinearLayout.VERTICAL);who.setPadding(dp(14),0,0,0);TextView nm=t(sp.getString("name","Cliente"),20);nm.setTypeface(null,1);nm.setPadding(0,0,0,0);who.addView(nm);TextView em=t(sp.getString("email",""),14);em.setTextColor(0xff9ca4a0);em.setPadding(0,dp(5),0,0);who.addView(em);TextView rv=t("Vinculado a: "+sp.getString("reseller_name",reseller.isEmpty()?"GreenPlay":reseller),13);rv.setTextColor(GREEN);rv.setPadding(0,dp(7),0,0);who.addView(rv);person.addView(who,new LinearLayout.LayoutParams(0,-2,1));body.addView(person);profileGap(12);

  // Aviso de assinatura: só aparece quando a conta não está ativa.
  LinearLayout renewal=new LinearLayout(this);renewal.setGravity(Gravity.CENTER_VERTICAL);renewal.setPadding(dp(15),dp(10),dp(12),dp(10));GradientDrawable renewBg=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{0xffd9373f,0xffb81623});renewBg.setCornerRadius(dp(20));renewal.setBackground(renewBg);renewal.setVisibility(View.GONE);
  TextView warn=t("!",25);warn.setTypeface(null,1);warn.setTextColor(0xffffdd52);warn.setGravity(Gravity.CENTER);renewal.addView(warn,new LinearLayout.LayoutParams(dp(42),dp(54)));LinearLayout renewText=new LinearLayout(this);renewText.setOrientation(LinearLayout.VERTICAL);TextView renewTitle=t("Assinar agora",17);renewTitle.setTypeface(null,1);renewTitle.setPadding(0,0,0,0);TextView renewSub=t("Sua assinatura não está ativa",13);renewSub.setTextColor(0xfff0d9dc);renewSub.setPadding(0,dp(3),0,0);renewText.addView(renewTitle);renewText.addView(renewSub);renewal.addView(renewText,new LinearLayout.LayoutParams(0,-2,1));TextView renewBtn=t("ASSINAR",13);renewBtn.setTypeface(null,1);renewBtn.setTextColor(0xff141414);renewBtn.setGravity(Gravity.CENTER);renewBtn.setPadding(dp(10),0,dp(10),0);renewBtn.setBackground(round(Color.WHITE,20));renewal.addView(renewBtn,new LinearLayout.LayoutParams(dp(104),dp(44)));renewal.setOnClickListener(v->plans());body.addView(renewal,new LinearLayout.LayoutParams(-1,dp(78)));

  // Informações da conta no formato da referência.
  LinearLayout infoCard=new LinearLayout(this);infoCard.setOrientation(LinearLayout.VERTICAL);infoCard.setPadding(dp(14),dp(10),dp(14),dp(10));GradientDrawable infoBg=round(0xff12171b,22);infoBg.setStroke(dp(1),0xff29302f);infoCard.setBackground(infoBg);
  LinearLayout infoHead=new LinearLayout(this);infoHead.setGravity(Gravity.CENTER_VERTICAL);TextView infoIc=t("◎",18);infoIc.setTextColor(GREEN);infoIc.setGravity(Gravity.CENTER);infoIc.setPadding(0,0,0,0);infoHead.addView(infoIc,new LinearLayout.LayoutParams(dp(36),dp(42)));TextView infoTitle=t("Informações da Conta",15);infoTitle.setTypeface(null,1);infoTitle.setTextColor(0xffaeb4b1);infoTitle.setPadding(0,0,0,0);infoHead.addView(infoTitle,new LinearLayout.LayoutParams(0,dp(42),1));infoCard.addView(infoHead);
  TextView planValue=profileInfoLine(infoCard,"✪","Plano","—",GREEN);TextView validityValue=profileInfoLine(infoCard,"▦","Validade","—",0xffd3d7d5);TextView screensValue=profileInfoLine(infoCard,"▣","Telas","—",0xfff1f1f1);TextView serverValue=profileInfoLine(infoCard,"▤","Servidor",sp.getString("provider_name","GreenPlay"),0xfff1f1f1);TextView subscriptionValue=profileInfoLine(infoCard,"✪","Assinatura","—",GREEN);body.addView(infoCard);profileGap(12);

  // Opções em um único cartão, como no aplicativo de referência.
  LinearLayout optionsCard=new LinearLayout(this);optionsCard.setOrientation(LinearLayout.VERTICAL);optionsCard.setPadding(dp(12),dp(8),dp(12),dp(8));GradientDrawable optBg=round(0xff12171b,22);optBg.setStroke(dp(1),0xff29302f);optionsCard.setBackground(optBg);
  LinearLayout optHead=new LinearLayout(this);optHead.setGravity(Gravity.CENTER_VERTICAL);TextView gear=t("⚙",19);gear.setTextColor(GREEN);gear.setGravity(Gravity.CENTER);gear.setPadding(0,0,0,0);optHead.addView(gear,new LinearLayout.LayoutParams(dp(42),dp(44)));TextView opts=t("Opções",15);opts.setTypeface(null,1);opts.setTextColor(0xffaeb4b1);opts.setPadding(0,0,0,0);optHead.addView(opts,new LinearLayout.LayoutParams(0,dp(44),1));optionsCard.addView(optHead);
  profileOptionRow(optionsCard,"✪","Benefícios da conta",v->plans(),false);
  profileOptionRow(optionsCard,"⇄","Trocar de Servidor",v->chooseProvider(),false);
  profileOptionRow(optionsCard,"▣","Dispositivos conectados",v->Toast.makeText(MainActivity.this,"Gerenciamento de dispositivos em preparação",Toast.LENGTH_SHORT).show(),false);
  profileOptionRow(optionsCard,"☎","Suporte",v->{String w=sp.getString("support","").replaceAll("\\D","");if(!w.isEmpty()){if(!w.startsWith("55"))w="55"+w;startActivity(new Intent(Intent.ACTION_VIEW,Uri.parse("https://wa.me/"+w)));}else Toast.makeText(MainActivity.this,"Suporte não configurado",Toast.LENGTH_SHORT).show();},false);
  profileOptionRow(optionsCard,"↻","Redefinir senha",v->changePassword(),false);
  Switch adultSwitch=profileSwitchRow(optionsCard,"◇","Conteúdo adulto",sp.getBoolean("adult",false));adultSwitch.setClickable(false);View adultRow=(View)adultSwitch.getTag();if(adultRow!=null)adultRow.setOnClickListener(v->{toggleAdult();adultSwitch.setChecked(sp.getBoolean("adult",false));});
  profileOptionRow(optionsCard,"▣","Alterar PIN",v->changePin(),false);
  profileOptionRow(optionsCard,"▣","Excluir conta",v->showDeleteConfirm(),true);
  body.addView(optionsCard);profileGap(8);

  Api.post("access_status",Api.m("user_id",uid),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");if(a==null||a.length()==0){planValue.setText("Básico");validityValue.setText("Expirada");screensValue.setText("1 de 1");serverValue.setText(sp.getString("provider_name","GreenPlay"));subscriptionValue.setText("Inativa");subscriptionValue.setTextColor(0xffff5963);validityValue.setTextColor(0xffff5963);renewal.setVisibility(View.VISIBLE);return;}JSONObject st=a.optJSONObject(0);if(st==null)return;String mode=st.optString("mode","");String msg=st.optString("message","");String exp=st.optString("expires_at","");String plan=st.optString("plan_name",st.optString("plan",mode));String sc=st.optString("screens",st.optString("telas","1"));String srv=st.optString("provider_name",st.optString("server_name",sp.getString("provider_name","GreenPlay")));boolean trial=mode.toLowerCase().contains("trial")||msg.toLowerCase().contains("teste");boolean active=st.optBoolean("allowed",st.optBoolean("active",true));if(plan.isEmpty())plan=trial?"Teste grátis":"Premium";planValue.setText(plan);validityValue.setText(exp.isEmpty()?"—":shortDate(exp));screensValue.setText(sc+" de "+sc);serverValue.setText(srv.isEmpty()?"GreenPlay":srv);subscriptionValue.setText(active?(trial?"Teste ativo":"Ativa"):"Inativa");subscriptionValue.setTextColor(active?GREEN:0xffff5963);validityValue.setTextColor(active?0xffd3d7d5:0xffff5963);renewSub.setText(trial&&!active?"Seu teste grátis terminou":"Sua assinatura não está ativa");renewal.setVisibility(active?View.GONE:View.VISIBLE);}public void err(String x){subscriptionValue.setText("Indisponível");subscriptionValue.setTextColor(0xffffa35c);}});
 }
 TextView profileInfoLine(LinearLayout host,String icon,String label,String value,int valueColor){LinearLayout row=new LinearLayout(this);row.setGravity(Gravity.CENTER_VERTICAL);row.setPadding(dp(4),0,dp(2),0);TextView ic=t(icon,16);ic.setGravity(Gravity.CENTER);ic.setTextColor(0xff8f9693);ic.setPadding(0,0,0,0);row.addView(ic,new LinearLayout.LayoutParams(dp(38),dp(58)));TextView lb=t(label,14);lb.setTextColor(0xff8f9693);lb.setPadding(0,0,0,0);lb.setGravity(Gravity.CENTER_VERTICAL);row.addView(lb,new LinearLayout.LayoutParams(0,dp(58),1));TextView val=t(value,14);val.setTypeface(null,1);val.setTextColor(valueColor);val.setGravity(Gravity.CENTER_VERTICAL|Gravity.RIGHT);val.setPadding(dp(8),0,dp(6),0);val.setMaxLines(2);row.addView(val,new LinearLayout.LayoutParams(0,dp(58),1));host.addView(row,new LinearLayout.LayoutParams(-1,dp(58)));profileDivider(host,dp(42));return val;}
 void profileDivider(LinearLayout host,int left){View line=new View(this);line.setBackgroundColor(0xff252b2a);LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(1));lp.setMargins(left,0,dp(4),0);host.addView(line,lp);}
 void profileOptionRow(LinearLayout host,String icon,String title,View.OnClickListener click,boolean danger){LinearLayout row=new LinearLayout(this);row.setGravity(Gravity.CENTER_VERTICAL);row.setPadding(dp(5),0,dp(2),0);TextView ic=t(icon,18);ic.setGravity(Gravity.CENTER);ic.setTextColor(danger?0xffff5963:0xff969d99);ic.setPadding(0,0,0,0);row.addView(ic,new LinearLayout.LayoutParams(dp(45),dp(62)));TextView tt=t(title,15);tt.setTypeface(null,1);tt.setTextColor(danger?0xffff7078:Color.WHITE);tt.setGravity(Gravity.CENTER_VERTICAL);tt.setPadding(dp(2),0,0,0);tt.setSingleLine(true);row.addView(tt,new LinearLayout.LayoutParams(0,dp(62),1));TextView ar=t("›",26);ar.setTextColor(0xff69716d);ar.setGravity(Gravity.CENTER);ar.setPadding(0,0,0,0);row.addView(ar,new LinearLayout.LayoutParams(dp(34),dp(62)));row.setOnClickListener(click);host.addView(row,new LinearLayout.LayoutParams(-1,dp(62)));profileDivider(host,dp(52));}
 Switch profileSwitchRow(LinearLayout host,String icon,String title,boolean checked){LinearLayout row=new LinearLayout(this);row.setGravity(Gravity.CENTER_VERTICAL);row.setPadding(dp(5),0,dp(8),0);TextView ic=t(icon,18);ic.setGravity(Gravity.CENTER);ic.setTextColor(0xff969d99);ic.setPadding(0,0,0,0);row.addView(ic,new LinearLayout.LayoutParams(dp(45),dp(62)));TextView tt=t(title,15);tt.setTypeface(null,1);tt.setGravity(Gravity.CENTER_VERTICAL);tt.setPadding(dp(2),0,0,0);row.addView(tt,new LinearLayout.LayoutParams(0,dp(62),1));Switch sw=new Switch(this);sw.setChecked(checked);sw.setShowText(false);row.addView(sw,new LinearLayout.LayoutParams(dp(68),dp(48)));sw.setTag(row);host.addView(row,new LinearLayout.LayoutParams(-1,dp(62)));profileDivider(host,dp(52));return sw;}
 TextView metric(String label,String value){TextView v=t(label+"\n"+value,12);v.setGravity(Gravity.CENTER);v.setTextColor(0xffc9d1cd);v.setMaxLines(3);return v;}
 String shortDate(String x){try{return x.length()>=10?x.substring(8,10)+"/"+x.substring(5,7)+"/"+x.substring(0,4):x;}catch(Exception e){return x;}}
 void profileGap(int h){Space s=new Space(this);body.addView(s,new LinearLayout.LayoutParams(1,dp(h)));}
 void addProfileOption2(String icon,String title,String subtitle,View.OnClickListener click,boolean danger){LinearLayout box=new LinearLayout(this);box.setGravity(Gravity.CENTER_VERTICAL);box.setPadding(dp(12),0,dp(10),0);box.setBackground(round(CARD,14));TextView ic=t(icon,18);ic.setGravity(Gravity.CENTER);ic.setTextColor(danger?0xffff5963:GREEN);box.addView(ic,new LinearLayout.LayoutParams(dp(38),dp(58)));TextView tt=t(title,15);tt.setTypeface(null,1);if(danger)tt.setTextColor(0xffff686f);tt.setGravity(Gravity.CENTER_VERTICAL);tt.setSingleLine(true);box.addView(tt,new LinearLayout.LayoutParams(0,dp(58),1));TextView ar=t("›",24);ar.setTextColor(0xff87938d);ar.setGravity(Gravity.CENTER);box.addView(ar,new LinearLayout.LayoutParams(dp(30),dp(58)));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(58));lp.setMargins(0,0,0,dp(6));body.addView(box,lp);box.setOnClickListener(click);}

 void editAccount(){LinearLayout f=new LinearLayout(this);f.setOrientation(LinearLayout.VERTICAL);f.setPadding(dp(18),0,dp(18),0);EditText n=e("Nome",false);n.setText(sp.getString("name",""));EditText w=e("WhatsApp",false);f.addView(n);f.addView(w);new AlertDialog.Builder(this).setTitle("Minha conta").setView(f).setNegativeButton("Cancelar",null).setPositiveButton("Salvar",(d,x)->Api.post("update_profile",Api.m("user_id",uid,"name",n.getText().toString().trim(),"mobile_number",w.getText().toString().trim()),new Api.CB(){public void ok(JSONObject j){if(j.optInt("status")==200){sp.edit().putString("name",n.getText().toString().trim()).apply();Toast.makeText(MainActivity.this,"Dados atualizados",0).show();profile();}else Toast.makeText(MainActivity.this,j.optString("message","Não foi possível salvar"),1).show();}public void err(String z){Toast.makeText(MainActivity.this,z,1).show();}})).show();}
 void chooseProvider(){providerSelectAfterLogin(true);}
 void loadProvidersFromSettings(){Api.post("general_setting",Api.m(),new Api.CB(){public void ok(JSONObject j){JSONArray cfg=j.optJSONArray("result");String raw="";if(cfg!=null){for(int i=0;i<cfg.length();i++){JSONObject x=cfg.optJSONObject(i);if(x!=null&&"greenplay_providers_json".equals(x.optString("key"))){raw=x.optString("value","");break;}}}try{JSONArray a=raw.isEmpty()?null:new JSONArray(raw);if(a!=null&&a.length()>0){for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o!=null)providerCard(o);}return;}}catch(Exception ignored){}loadProvidersLegacy();}public void err(String z){loadProvidersLegacy();}});}
 void loadProvidersLegacy(){Api.post("get_providers",Api.m("user_id",uid,"reseller_code",reseller),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");if(a==null||a.length()==0){body.addView(t("Nenhum servidor disponível.",16));return;}for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o!=null)providerCard(o);}}public void err(String z){TextView e=t("Não foi possível carregar os servidores. Atualize o painel e tente novamente.",16);e.setTextColor(0xffff7777);body.addView(e);}});}
 void providerCard(JSONObject o){String id=o.optString("id",o.optString("provider_id",""));String name=o.optString("name","Servidor");String active=Api.PROVIDER==null?"":Api.PROVIDER;int movies=o.optInt("movies_count",o.optInt("movies",-1));int series=o.optInt("series_count",o.optInt("series",-1));int live=o.optInt("channels_count",o.optInt("live_count",o.optInt("channels",-1)));String caps="";if(movies>0)caps="Filmes";if(series>0)caps+=(caps.isEmpty()?"":"  •  ")+"Séries";if(live>0)caps+=(caps.isEmpty()?"":"  •  ")+"TV ao vivo";if(caps.isEmpty())caps="Conteúdo disponível";LinearLayout card=new LinearLayout(this);card.setGravity(Gravity.CENTER_VERTICAL);card.setPadding(dp(14),dp(10),dp(12),dp(10));GradientDrawable g=round(0xff171e1b,20);g.setStroke(dp(id.equals(active)?2:1),id.equals(active)?GREEN:0xff27332e);card.setBackground(g);TextView icon=t("▦",24);icon.setTextColor(GREEN);icon.setGravity(Gravity.CENTER);icon.setBackground(round(0xff123225,15));card.addView(icon,new LinearLayout.LayoutParams(dp(58),dp(58)));LinearLayout mid=new LinearLayout(this);mid.setOrientation(LinearLayout.VERTICAL);mid.setPadding(dp(12),0,0,0);TextView n=t(name,17);n.setTypeface(null,1);mid.addView(n);TextView c=t(caps,14);c.setTextColor(0xff9ca6a1);mid.addView(c);card.addView(mid,new LinearLayout.LayoutParams(0,-2,1));TextView ar=t(id.equals(active)?"✓":"›",26);ar.setTextColor(id.equals(active)?GREEN:0xffa8b0ac);ar.setGravity(Gravity.CENTER);card.addView(ar,new LinearLayout.LayoutParams(dp(42),dp(62)));card.setOnClickListener(v->connectProviderReady(id,name,movies,series,live,card,ar));LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,dp(92));lp.setMargins(dp(4),0,dp(4),dp(10));body.addView(card,lp);}
  void showProviderLoading(String name){clear();setNav(4);TextView title=t("Carregando conteúdo",25);title.setTypeface(null,1);title.setGravity(Gravity.CENTER);body.addView(new Space(this),new LinearLayout.LayoutParams(1,dp(120)));body.addView(title);TextView sub=t("Conectando ao servidor "+name+"…",15);sub.setTextColor(0xff9da7a2);sub.setGravity(Gravity.CENTER);body.addView(sub);ProgressBar p=new ProgressBar(this);p.setIndeterminate(true);LinearLayout.LayoutParams pp=new LinearLayout.LayoutParams(dp(52),dp(52));pp.gravity=Gravity.CENTER_HORIZONTAL;pp.setMargins(0,dp(24),0,0);body.addView(p,pp);fetchPreparedHome(-1,-1,new PreparedHomeCB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");if(a!=null&&a.length()>0){saveHomeCache(j);sp.edit().putBoolean(homeExtrasKey(),false).apply();homeExtrasStarted=false;warmHomeImages(j,()->home());}else home();}public void err(String e){home();}});}
 void stabilizeInputDialog(Dialog d,View card){
  if(card!=null){card.setFocusableInTouchMode(true);card.requestFocus();}
  Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));w.setDimAmount(.72f);w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);w.setGravity(Gravity.CENTER);w.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_NOTHING|WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);WindowManager.LayoutParams lp=w.getAttributes();lp.windowAnimations=0;w.setAttributes(lp);}
 }
 void sizeStableInputDialog(Dialog d,View focusRoot){Window w=d.getWindow();if(w==null)return;w.setLayout(Math.min(getResources().getDisplayMetrics().widthPixels-dp(38),dp(500)),-2);WindowManager.LayoutParams lp=w.getAttributes();lp.windowAnimations=0;w.setAttributes(lp);if(focusRoot!=null){focusRoot.setFocusableInTouchMode(true);focusRoot.requestFocus();}}
 void changePassword(){
  final Dialog d=new Dialog(this);LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setPadding(dp(20),dp(18),dp(20),dp(18));GradientDrawable bg=round(0xff0d1712,24);bg.setStroke(dp(1),0xff294839);card.setBackground(bg);TextView title=t("Redefinir senha",22);title.setTypeface(null,1);title.setPadding(0,0,0,dp(6));card.addView(title);TextView sub=t("Crie uma nova senha para sua conta.",14);sub.setTextColor(0xff9eaaa4);sub.setPadding(0,0,0,dp(14));card.addView(sub);EditText p1=e("Nova senha",true),p2=e("Confirmar nova senha",true);GradientDrawable i1=round(0xff102219,14);i1.setStroke(dp(1),0xff2b4539);p1.setBackground(i1);GradientDrawable i2=round(0xff102219,14);i2.setStroke(dp(1),0xff2b4539);p2.setBackground(i2);card.addView(p1,new LinearLayout.LayoutParams(-1,dp(54)));LinearLayout.LayoutParams p2lp=new LinearLayout.LayoutParams(-1,dp(54));p2lp.setMargins(0,dp(9),0,0);card.addView(p2,p2lp);TextView err=t("",12);err.setTextColor(0xffff7379);err.setPadding(dp(2),dp(7),0,dp(4));card.addView(err);
  LinearLayout actions=new LinearLayout(this);actions.setGravity(Gravity.RIGHT);TextView cancel=t("Cancelar",14);cancel.setGravity(Gravity.CENTER);cancel.setTypeface(null,1);cancel.setTextColor(0xffc7ceca);GradientDrawable cb=round(0xff17231d,13);cb.setStroke(dp(1),0xff304339);cancel.setBackground(cb);actions.addView(cancel,new LinearLayout.LayoutParams(dp(112),dp(48)));TextView save=t("Salvar",14);save.setGravity(Gravity.CENTER);save.setTypeface(null,1);save.setTextColor(0xff061109);save.setBackground(round(GREEN,13));LinearLayout.LayoutParams slp=new LinearLayout.LayoutParams(dp(112),dp(48));slp.setMargins(dp(9),0,0,0);actions.addView(save,slp);card.addView(actions);
  cancel.setOnClickListener(v->d.dismiss());save.setOnClickListener(v->{String a=p1.getText().toString();if(a.length()<6){err.setText("Use pelo menos 6 caracteres.");return;}if(!a.equals(p2.getText().toString())){err.setText("As senhas não coincidem.");return;}save.setEnabled(false);err.setText("");Api.post("change_password",Api.m("user_id",uid,"password",a),new Api.CB(){public void ok(JSONObject j){runOnUiThread(()->{d.dismiss();showAppNotice(j.optString("message","Senha atualizada"),false);});}public void err(String z){runOnUiThread(()->{save.setEnabled(true);err.setText(z==null||z.isEmpty()?"Não foi possível alterar a senha.":z);});}});});d.setContentView(card);stabilizeInputDialog(d,card);d.setOnShowListener(x->sizeStableInputDialog(d,card));d.show();
 }
 void toggleAdult(){boolean on=!sp.getBoolean("adult",false);if(on&&!sp.contains("pin")){changePin();return;}sp.edit().putBoolean("adult",on).apply();showAppNotice(on?"Conteúdo adulto ativado":"Conteúdo adulto desativado",false);profile();}
 void changePin(){
  final Dialog d=new Dialog(this);LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setPadding(dp(20),dp(18),dp(20),dp(18));GradientDrawable bg=round(0xff0d1712,24);bg.setStroke(dp(1),0xff294839);card.setBackground(bg);TextView title=t(sp.contains("pin")?"Alterar PIN":"Criar PIN",22);title.setTypeface(null,1);title.setPadding(0,0,0,dp(6));card.addView(title);TextView sub=t("Use 4 números para proteger o conteúdo adulto.",14);sub.setTextColor(0xff9eaaa4);sub.setPadding(0,0,0,dp(14));card.addView(sub);EditText pin=e("PIN de 4 dígitos",true);pin.setInputType(InputType.TYPE_CLASS_NUMBER|InputType.TYPE_NUMBER_VARIATION_PASSWORD);GradientDrawable ib=round(0xff102219,14);ib.setStroke(dp(1),0xff2b4539);pin.setBackground(ib);card.addView(pin,new LinearLayout.LayoutParams(-1,dp(54)));TextView err=t("",12);err.setTextColor(0xffff7379);err.setPadding(dp(2),dp(7),0,dp(4));card.addView(err);LinearLayout actions=new LinearLayout(this);actions.setGravity(Gravity.RIGHT);TextView cancel=t("Cancelar",14);cancel.setGravity(Gravity.CENTER);cancel.setTypeface(null,1);cancel.setTextColor(0xffc7ceca);GradientDrawable cb=round(0xff17231d,13);cb.setStroke(dp(1),0xff304339);cancel.setBackground(cb);actions.addView(cancel,new LinearLayout.LayoutParams(dp(112),dp(48)));TextView save=t("Salvar",14);save.setGravity(Gravity.CENTER);save.setTypeface(null,1);save.setTextColor(0xff061109);save.setBackground(round(GREEN,13));LinearLayout.LayoutParams slp=new LinearLayout.LayoutParams(dp(112),dp(48));slp.setMargins(dp(9),0,0,0);actions.addView(save,slp);card.addView(actions);cancel.setOnClickListener(v->d.dismiss());save.setOnClickListener(v->{String vpin=pin.getText().toString();if(!vpin.matches("\\d{4}")){err.setText("Digite exatamente 4 números.");return;}sp.edit().putString("pin",vpin).apply();d.dismiss();showAppNotice("PIN atualizado",false);profile();});d.setContentView(card);stabilizeInputDialog(d,card);d.setOnShowListener(x->sizeStableInputDialog(d,card));d.show();
 }
 void plans(){
  plansScreen=true;clear();setNav(4);if(navBar!=null)navBar.setVisibility(View.GONE);
  LinearLayout h=new LinearLayout(this);h.setGravity(Gravity.CENTER_VERTICAL);h.setPadding(0,dp(6),0,dp(10));
  TextView back=t("‹",34);back.setTextColor(Color.WHITE);back.setGravity(Gravity.CENTER);back.setPadding(0,0,0,0);back.setOnClickListener(v->profile());h.addView(back,new LinearLayout.LayoutParams(dp(48),dp(54)));
  TextView tt=t("Planos",26);tt.setTypeface(null,1);tt.setPadding(dp(4),0,0,0);tt.setGravity(Gravity.CENTER_VERTICAL);h.addView(tt,new LinearLayout.LayoutParams(0,dp(54),1));body.addView(h,new LinearLayout.LayoutParams(-1,dp(66)));
  TextView intro=t("Escolha o plano ideal para você",15);intro.setTextColor(0xffa7adaa);intro.setPadding(dp(7),0,dp(7),dp(18));body.addView(intro);
  TextView loading=t("Carregando planos…",14);loading.setTextColor(0xff8f9994);loading.setGravity(Gravity.CENTER);body.addView(loading,new LinearLayout.LayoutParams(-1,dp(64)));
  Api.post("subscription_package",Api.m("user_id",uid,"reseller_code",reseller),new Api.CB(){public void ok(JSONObject j){runOnUiThread(()->{if(loading.getParent()!=null)body.removeView(loading);JSONArray a=j.optJSONArray("result");if(a==null||a.length()==0){TextView empty=t("Nenhum plano disponível no momento.",15);empty.setTextColor(0xffa7b0ab);empty.setGravity(Gravity.CENTER);empty.setPadding(dp(8),dp(30),dp(8),dp(30));body.addView(empty);return;}for(int i=0;i<a.length();i++){JSONObject plan=a.optJSONObject(i);if(plan!=null)renderPlanCard(plan);}});}public void err(String x){runOnUiThread(()->{if(loading.getParent()!=null)body.removeView(loading);TextView e=t(x==null||x.isEmpty()?"Não foi possível carregar os planos.":x,14);e.setTextColor(0xffff7379);body.addView(e);});}});
 }
 String cleanPlanEmoji(String raw){if(raw==null)return "";String s=raw.trim();if(s.isEmpty())return "";if(s.matches("\\?{2,}"))return "";return s.replaceAll("\\?{3,}","").trim();}
 String cleanPlanFeature(String raw){if(raw==null)return "";return raw.trim().replaceAll("\\?{3,}","").trim();}
 void renderPlanCard(JSONObject p){
  // v16.82: proporções mais próximas da referência: cartão mais estreito,
  // tipografia menor e menos espaço vertical entre os elementos.
  boolean featured=p.optInt("featured",0)==1;
  LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setPadding(dp(18),dp(18),dp(18),dp(18));
  GradientDrawable bg;if(featured){bg=new GradientDrawable(GradientDrawable.Orientation.TL_BR,new int[]{0xff153321,0xff151b18,0xff121719});}else{bg=new GradientDrawable();bg.setColor(0xff151a1e);}bg.setCornerRadius(dp(22));bg.setStroke(dp(featured?2:1),featured?GREEN:0xff30373a);card.setBackground(bg);
  LinearLayout head=new LinearLayout(this);head.setGravity(Gravity.CENTER_VERTICAL);
  String emoji=cleanPlanEmoji(p.optString("emoji",""));String nm=p.optString("name","Plano").trim();TextView name=t(nm+(emoji.isEmpty()?"":"  "+emoji),19);name.setTypeface(null,1);name.setPadding(0,0,dp(8),0);head.addView(name,new LinearLayout.LayoutParams(0,dp(42),1));
  String badge=p.optString("badge","").trim();if(featured&&badge.isEmpty())badge="MAIS POPULAR";if(!badge.isEmpty()){TextView b=t(badge.toUpperCase(java.util.Locale.ROOT),10);b.setTypeface(null,1);b.setGravity(Gravity.CENTER);b.setTextColor(0xff051109);b.setPadding(dp(11),0,dp(11),0);GradientDrawable bb=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{GREEN,0xff54ef8e});bb.setCornerRadius(dp(17));b.setBackground(bb);head.addView(b,new LinearLayout.LayoutParams(-2,dp(34)));}card.addView(head);
  LinearLayout priceRow=new LinearLayout(this);priceRow.setGravity(Gravity.CENTER_VERTICAL);String priceText="R$ "+p.optString("price_formatted",String.format(java.util.Locale.US,"%.2f",p.optDouble("price",0)).replace('.',','));TextView price=t(priceText,30);price.setTypeface(null,1);price.setTextColor(GREEN);price.setPadding(0,0,0,0);priceRow.addView(price,new LinearLayout.LayoutParams(-2,dp(56)));TextView days=t("/ "+p.optInt("days",p.optInt("time",0))+" dias",13);days.setTextColor(0xffaeb3b1);days.setPadding(dp(7),dp(6),0,0);priceRow.addView(days,new LinearLayout.LayoutParams(-2,dp(50)));card.addView(priceRow);
  int sc=Math.max(1,p.optInt("screens",1));TextView screens=t("▣  "+sc+(sc==1?" tela":" telas simultâneas"),12);screens.setTypeface(null,1);screens.setTextColor(0xffe6e9e7);screens.setGravity(Gravity.CENTER_VERTICAL);screens.setPadding(dp(12),0,dp(12),0);GradientDrawable sb=round(featured?0xff173925:0xff242a2d,17);sb.setStroke(dp(1),featured?0xff2a7048:0xff333a3d);screens.setBackground(sb);LinearLayout.LayoutParams spLp=new LinearLayout.LayoutParams(-2,dp(38));spLp.setMargins(0,dp(2),0,dp(16));card.addView(screens,spLp);
  View line=new View(this);line.setBackgroundColor(0xff30373a);LinearLayout.LayoutParams llp=new LinearLayout.LayoutParams(-1,dp(1));llp.setMargins(0,0,0,dp(10));card.addView(line,llp);
  JSONArray features=p.optJSONArray("features");if(features!=null){for(int i=0;i<features.length();i++){String f=cleanPlanFeature(features.optString(i,""));if(f.isEmpty())continue;LinearLayout row=new LinearLayout(this);row.setGravity(Gravity.CENTER_VERTICAL);TextView check=t("✓",14);check.setTypeface(null,1);check.setGravity(Gravity.CENTER);check.setTextColor(Color.WHITE);check.setPadding(0,0,0,0);GradientDrawable ck=new GradientDrawable(GradientDrawable.Orientation.TL_BR,new int[]{GREEN,0xff12964c});ck.setCornerRadius(dp(15));check.setBackground(ck);row.addView(check,new LinearLayout.LayoutParams(dp(30),dp(30)));TextView ft=t(f.toUpperCase(java.util.Locale.ROOT),13);ft.setTypeface(null,1);ft.setTextColor(0xfff1f3f2);ft.setPadding(dp(12),0,0,0);row.addView(ft,new LinearLayout.LayoutParams(0,dp(44),1));card.addView(row);}}
  TextView buy=t("Assinar agora",15);buy.setTypeface(null,1);buy.setGravity(Gravity.CENTER);buy.setTextColor(0xff051109);buy.setPadding(0,0,0,0);GradientDrawable buyBg=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{0xff17d866,0xff53f08d});buyBg.setCornerRadius(dp(17));buy.setBackground(buyBg);LinearLayout.LayoutParams blp=new LinearLayout.LayoutParams(-1,dp(52));blp.setMargins(0,dp(14),0,0);card.addView(buy,blp);buy.setOnClickListener(v->checkout(p,""));
  LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(-1,-2);cp.setMargins(dp(8),0,dp(8),dp(16));body.addView(card,cp);if(tvMode){prepareTvFocusTree(card);}
 }
 void askCpf(JSONObject p){
  final Dialog d=new Dialog(this);LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setPadding(dp(20),dp(18),dp(20),dp(18));GradientDrawable bg=round(0xff0d1712,24);bg.setStroke(dp(1),0xff294839);card.setBackground(bg);TextView title=t("Pagamento via PIX",21);title.setTypeface(null,1);title.setPadding(0,0,0,dp(5));card.addView(title);TextView sub=t(p.optString("name","Plano")+" · R$ "+p.optString("price_formatted",p.optString("price","")),13);sub.setTextColor(0xff9eaaa4);sub.setPadding(0,0,0,dp(14));card.addView(sub);EditText doc=e("CPF ou CNPJ",false);doc.setInputType(InputType.TYPE_CLASS_NUMBER);GradientDrawable ib=round(0xff102219,14);ib.setStroke(dp(1),0xff2b4539);doc.setBackground(ib);card.addView(doc,new LinearLayout.LayoutParams(-1,dp(54)));TextView err=t("",12);err.setTextColor(0xffff7379);err.setPadding(dp(2),dp(7),0,dp(4));card.addView(err);LinearLayout actions=new LinearLayout(this);actions.setGravity(Gravity.RIGHT);TextView cancel=t("Cancelar",14);cancel.setGravity(Gravity.CENTER);cancel.setTypeface(null,1);cancel.setTextColor(0xffc7ceca);cancel.setBackground(round(0xff17231d,13));actions.addView(cancel,new LinearLayout.LayoutParams(dp(112),dp(48)));TextView go=t("Gerar PIX",14);go.setGravity(Gravity.CENTER);go.setTypeface(null,1);go.setTextColor(0xff061109);go.setBackground(round(GREEN,13));LinearLayout.LayoutParams glp=new LinearLayout.LayoutParams(0,dp(48),1);glp.setMargins(dp(9),0,0,0);actions.addView(go,glp);card.addView(actions);cancel.setOnClickListener(v->d.dismiss());go.setOnClickListener(v->{String digits=doc.getText().toString().replaceAll("\\D+","");if(digits.length()!=11&&digits.length()!=14){err.setText("Informe um CPF ou CNPJ válido.");return;}d.dismiss();checkout(p,digits);});d.setContentView(card);stabilizeInputDialog(d,card);d.setOnShowListener(x->sizeStableInputDialog(d,card));d.show();
 }
 void checkout(JSONObject p,String doc){String pid=p.optString("id");final String sentDoc=doc==null?"":doc;Api.post("create_checkout",Api.m("user_id",uid,"package_id",pid,"payer_document",sentDoc,"reseller_code",reseller),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");if(a==null||a.length()==0){if(sentDoc.isEmpty()&&j.optBoolean("requires_document",false)){runOnUiThread(()->askCpf(p));return;}runOnUiThread(()->showAppNotice(j.optString("message","Não foi possível gerar o PIX."),true));return;}String pix=a.optJSONObject(0).optString("pix_copy_paste");runOnUiThread(()->showPixDialog(pix));}public void err(String x){runOnUiThread(()->showAppNotice(x==null||x.isEmpty()?"Não foi possível gerar o PIX.":x,true));}});}
 void showPixDialog(String pix){final Dialog d=new Dialog(this);LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setPadding(dp(20),dp(18),dp(20),dp(18));GradientDrawable bg=round(0xff0d1712,24);bg.setStroke(dp(1),0xff294839);card.setBackground(bg);TextView title=t("PIX gerado",21);title.setTypeface(null,1);title.setPadding(0,0,0,dp(6));card.addView(title);TextView sub=t("Copie o código abaixo e pague no aplicativo do seu banco.",13);sub.setTextColor(0xff9eaaa4);sub.setPadding(0,0,0,dp(12));card.addView(sub);TextView code=t(pix,12);code.setTextIsSelectable(true);code.setTextColor(0xffd7dfda);code.setPadding(dp(12),dp(12),dp(12),dp(12));code.setBackground(round(0xff102219,12));card.addView(code,new LinearLayout.LayoutParams(-1,-2));TextView copy=t("Copiar código PIX",15);copy.setTypeface(null,1);copy.setGravity(Gravity.CENTER);copy.setTextColor(0xff061109);copy.setBackground(round(GREEN,14));LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(-1,dp(52));clp.setMargins(0,dp(14),0,0);card.addView(copy,clp);TextView close=t("Fechar",14);close.setGravity(Gravity.CENTER);close.setTextColor(0xffc7ceca);LinearLayout.LayoutParams xlp=new LinearLayout.LayoutParams(-1,dp(46));xlp.setMargins(0,dp(7),0,0);card.addView(close,xlp);copy.setOnClickListener(v->{((android.content.ClipboardManager)getSystemService(CLIPBOARD_SERVICE)).setPrimaryClip(android.content.ClipData.newPlainText("PIX",pix));showAppNotice("Código PIX copiado",false);});close.setOnClickListener(v->d.dismiss());d.setContentView(card);Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));w.setDimAmount(.72f);w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);w.setGravity(Gravity.CENTER);}d.setOnShowListener(x->{Window ww=d.getWindow();if(ww!=null)ww.setLayout(Math.min(getResources().getDisplayMetrics().widthPixels-dp(38),dp(500)),-2);});d.show();}
 void addGap(){Space s=new Space(this);root.addView(s,new LinearLayout.LayoutParams(1,dp(10)));}
}

