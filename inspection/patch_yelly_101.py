from pathlib import Path
import re, colorsys

root=Path('work')
main=root/'app/src/main/java/fun/greenplay/app/MainActivity.java'
s=main.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1, got {n}')
    s=s.replace(old,new,1)

one('void loadIdentityCache(){appName="Yelly Doramas";logoUrl="";bgUrl="";GREEN=Color.rgb(255,79,154);}\n void refreshIdentity(){appName="Yelly Doramas";logoUrl="";bgUrl="";refreshHomeHeaderBranding();}\n void applyAppLogo(ImageView im){if(im==null)return;try{im.setImageResource(R.drawable.yelly_logo);im.setAlpha(1f);}catch(Exception ignored){}}',
'''void loadIdentityCache(){appName=sp.getString("app_name","Yelly Doramas");logoUrl=sp.getString("app_logo","");bgUrl=sp.getString("app_background","");try{GREEN=Color.parseColor(sp.getString("app_color","#B8007D"));}catch(Exception e){GREEN=Color.rgb(184,0,125);}}
 void refreshIdentity(){Api.post("general_setting",Api.m(),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");if(a==null)return;android.content.SharedPreferences.Editor ed=sp.edit();for(int i=0;i<a.length();i++){JSONObject x=a.optJSONObject(i);if(x==null)continue;String k=x.optString("key"),v=x.optString("value");if(k.equals("greenplay_app_name")&&!v.trim().isEmpty())ed.putString("app_name",v);if(k.equals("greenplay_app_logo"))ed.putString("app_logo",v);if(k.equals("greenplay_app_background"))ed.putString("app_background",v);if(k.equals("greenplay_primary_color")&&!v.trim().isEmpty())ed.putString("app_color",v);if(k.equals("greenplay_support_whatsapp")&&!v.trim().isEmpty()&&(reseller==null||reseller.isEmpty()||sp.getString("support","").trim().isEmpty()))ed.putString("support",v);}ed.apply();loadIdentityCache();runOnUiThread(()->{if(uid.isEmpty()){if(authScreen)login();}else refreshHomeHeaderBranding();});}public void err(String e){}});}
 void applyAppLogo(ImageView im){if(im==null)return;try{im.setImageResource(R.drawable.yelly_logo);im.setAlpha(1f);}catch(Exception ignored){}String u=logoUrl==null?"":logoUrl.trim();if(!u.isEmpty())Img.load(im,u);}''','identity')

one('void base(){base(false);} void base(boolean loginBackground){FrameLayout frame=new FrameLayout(this);frame.setBackgroundColor(BG);if(loginBackground){getWindow().setStatusBarColor(0xff050b08);getWindow().setNavigationBarColor(0xff050b08);ImageView bg=new ImageView(this);bg.setScaleType(ImageView.ScaleType.CENTER_CROP);bg.setImageResource(R.drawable.login_cinema_bg);frame.addView(bg,new FrameLayout.LayoutParams(-1,-1));View shade=new View(this);shade.setBackgroundColor(0x8f020806);frame.addView(shade,new FrameLayout.LayoutParams(-1,-1));}else{getWindow().setStatusBarColor(BG);getWindow().setNavigationBarColor(BG);}root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(loginBackground?dp(22):dp(18),loginBackground?dp(14):dp(18),loginBackground?dp(22):dp(18),loginBackground?dp(18):dp(12));frame.addView(root,new FrameLayout.LayoutParams(-1,-1));setContentView(frame);if(tvMode)enableTvRemoteTree(root);}',
'''void base(){base(false);} void base(boolean loginBackground){FrameLayout frame=new FrameLayout(this);frame.setBackgroundColor(BG);if(loginBackground){getWindow().setStatusBarColor(0xff0b060a);getWindow().setNavigationBarColor(0xff0b060a);ImageView bg=new ImageView(this);bg.setScaleType(ImageView.ScaleType.CENTER_CROP);bg.setBackgroundColor(0xff120910);String panelBg=bgUrl==null?"":bgUrl.trim();if(!panelBg.isEmpty())Img.load(bg,panelBg);frame.addView(bg,new FrameLayout.LayoutParams(-1,-1));View shade=new View(this);shade.setBackgroundColor(0x8a090408);frame.addView(shade,new FrameLayout.LayoutParams(-1,-1));}else{getWindow().setStatusBarColor(BG);getWindow().setNavigationBarColor(BG);}root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(loginBackground?dp(22):dp(18),loginBackground?dp(14):dp(18),loginBackground?dp(22):dp(18),loginBackground?dp(18):dp(12));frame.addView(root,new FrameLayout.LayoutParams(-1,-1));setContentView(frame);if(tvMode)enableTvRemoteTree(root);}''','login background')

start='  if(!logoUrl.isEmpty()){ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);logo.setAdjustViewBounds(true);logo.setContentDescription(appName);Img.load(logo,logoUrl);LinearLayout.LayoutParams logoLp=new LinearLayout.LayoutParams(-1,dp(82));logoLp.setMargins(dp(24),dp(2),dp(24),0);c.addView(logo,logoLp);}else{TextView logo=t("",35);String brand=(appName==null||appName.trim().isEmpty())?"Yelly":appName.trim();android.text.SpannableString ls=new android.text.SpannableString(brand+" ▶");int split=Math.min(5,brand.length());ls.setSpan(new android.text.style.ForegroundColorSpan(Color.WHITE),0,split,android.text.Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);ls.setSpan(new android.text.style.ForegroundColorSpan(GREEN),split,ls.length(),android.text.Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);logo.setText(ls);logo.setTypeface(null,1);logo.setGravity(Gravity.CENTER);logo.setPadding(0,dp(10),0,0);c.addView(logo,new LinearLayout.LayoutParams(-1,dp(66)));}'
repl='  ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);logo.setAdjustViewBounds(true);logo.setContentDescription(appName);applyAppLogo(logo);LinearLayout.LayoutParams logoLp=new LinearLayout.LayoutParams(-1,dp(82));logoLp.setMargins(dp(24),dp(2),dp(24),0);c.addView(logo,logoLp);'
one(start,repl,'login logo')

old='void doLogin(String email,String pass,TextView msg,Button go){Api.post("login",Api.m("email",email.trim(),"password",pass,"device_type",currentDeviceType(),"device_id",deviceId(),"device_name",currentDeviceName()),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");if(j.optInt("status")!=200||a==null||a.length()==0){msg.setText(j.optString("message","Dados incorretos"));go.setEnabled(true);return;}JSONObject u=a.optJSONObject(0);uid=u.optString("id");android.content.SharedPreferences.Editor ed=sp.edit().putString("uid",uid).putString("name",u.optString("full_name")).putString("username",u.optString("username",u.optString("user_name",""))).putString("email",u.optString("email"));String rc=u.optString("reseller_code","");String rn=u.optString("reseller_name","");String sw=u.optString("support_whatsapp","");if(!rc.isEmpty()){reseller=rc;ed.putString("reseller",rc);}if(!rn.isEmpty())ed.putString("reseller_name",rn);if(!sw.isEmpty())ed.putString("support",sw);ed.apply();syncDevice(null);refreshAccountContext(null);refreshEntitlements(()->shell());}public void err(String x){msg.setText("Falha de conexão: "+x);go.setEnabled(true);}});}'
new='void doLogin(String email,String pass,TextView msg,Button go){String id=email==null?"":email.trim();Api.post("login",Api.m("identifier",id,"email",id,"password",pass,"device_type",currentDeviceType(),"device_id",deviceId(),"device_name",currentDeviceName()),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");if(j.optInt("status")!=200||a==null||a.length()==0){msg.setText(j.optString("message","Dados incorretos"));go.setEnabled(true);return;}JSONObject u=a.optJSONObject(0);uid=u.optString("id");android.content.SharedPreferences.Editor ed=sp.edit().putString("uid",uid).putString("name",u.optString("full_name")).putString("username",u.optString("username",u.optString("user_name",""))).putString("email",u.optString("email"));String rc=u.optString("reseller_code","");String rn=u.optString("reseller_name","");String sw=u.optString("support_whatsapp","");if(!rc.isEmpty()){reseller=rc;ed.putString("reseller",rc);}if(!rn.isEmpty())ed.putString("reseller_name",rn);if(!sw.isEmpty())ed.putString("support",sw);ed.apply();authScreen=false;shell();syncDevice(null);refreshAccountContext(null);refreshEntitlements(()->{});}public void err(String x){msg.setText("Falha de conexão: "+x);go.setEnabled(true);}});}'
one(old,new,'login transition')

one('Drawable authFieldSelector(){StateListDrawable s=new StateListDrawable();GradientDrawable focus=new GradientDrawable();focus.setColor(0xff26352f);focus.setCornerRadius(dp(28));focus.setStroke(dp(3),0xff31f080);s.addState(new int[]{android.R.attr.state_focused},focus);s.addState(new int[]{android.R.attr.state_pressed},focus);s.addState(new int[]{},authBox());return s;}',
    'Drawable authFieldSelector(){StateListDrawable s=new StateListDrawable();GradientDrawable focus=new GradientDrawable();focus.setColor(0xff2b1522);focus.setCornerRadius(dp(28));focus.setStroke(dp(3),GREEN);s.addState(new int[]{android.R.attr.state_focused},focus);s.addState(new int[]{android.R.attr.state_pressed},focus);s.addState(new int[]{},authBox());return s;}','auth field')
one('Drawable authPrimarySelector(){StateListDrawable s=new StateListDrawable();GradientDrawable focus=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{0xff48f784,0xff7dffa7,0xff48f784});focus.setCornerRadius(dp(30));focus.setStroke(dp(3),Color.WHITE);GradientDrawable normal=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{0xff21df70,0xff48f784,0xff20df70});normal.setCornerRadius(dp(30));s.addState(new int[]{android.R.attr.state_focused},focus);s.addState(new int[]{android.R.attr.state_pressed},focus);s.addState(new int[]{},normal);return s;}',
    'Drawable authPrimarySelector(){StateListDrawable s=new StateListDrawable();GradientDrawable focus=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{GREEN,0xffff78b7,GREEN});focus.setCornerRadius(dp(30));focus.setStroke(dp(3),Color.WHITE);GradientDrawable normal=new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT,new int[]{GREEN,0xffff5aa6,GREEN});normal.setCornerRadius(dp(30));s.addState(new int[]{android.R.attr.state_focused},focus);s.addState(new int[]{android.R.attr.state_pressed},focus);s.addState(new int[]{},normal);return s;}','auth primary')
one('Drawable authSecondarySelector(){StateListDrawable s=new StateListDrawable();GradientDrawable focus=new GradientDrawable();focus.setColor(0xff183626);focus.setCornerRadius(dp(30));focus.setStroke(dp(3),0xff43f58c);GradientDrawable normal=new GradientDrawable();normal.setColor(0x66101815);normal.setCornerRadius(dp(30));normal.setStroke(dp(1),GREEN);s.addState(new int[]{android.R.attr.state_focused},focus);s.addState(new int[]{android.R.attr.state_pressed},focus);s.addState(new int[]{},normal);return s;}',
    'Drawable authSecondarySelector(){StateListDrawable s=new StateListDrawable();GradientDrawable focus=new GradientDrawable();focus.setColor(0xff331321);focus.setCornerRadius(dp(30));focus.setStroke(dp(3),GREEN);GradientDrawable normal=new GradientDrawable();normal.setColor(0x66180d14);normal.setCornerRadius(dp(30));normal.setStroke(dp(1),GREEN);s.addState(new int[]{android.R.attr.state_focused},focus);s.addState(new int[]{android.R.attr.state_pressed},focus);s.addState(new int[]{},normal);return s;}','auth secondary')
s=s.replace('Button authPrimary(String s){Button b=new Button(this);b.setText(s);b.setTextColor(0xff031108);','Button authPrimary(String s){Button b=new Button(this);b.setText(s);b.setTextColor(Color.WHITE);',1)

grad=root/'app/build.gradle'
g=grad.read_text(encoding='utf-8').replace('versionCode 10000','versionCode 10001').replace("versionName '1.0.0'","versionName '1.0.1'")
grad.write_text(g,encoding='utf-8')

def shift_green_literals(text):
    pat=re.compile(r'0x([0-9a-fA-F]{2})([0-9a-fA-F]{6})')
    def f(m):
        a=m.group(1); rgb=m.group(2)
        r,g,b=[int(rgb[i:i+2],16) for i in (0,2,4)]
        h,sat,val=colorsys.rgb_to_hsv(r/255,g/255,b/255)
        deg=h*360
        if not (75 <= deg <= 170 and sat > .18 and val > .12): return m.group(0)
        nr,ng,nb=colorsys.hsv_to_rgb(330/360,sat,val)
        return '0x'+a+f'{round(nr*255):02x}{round(ng*255):02x}{round(nb*255):02x}'
    return pat.sub(f,text)

s=shift_green_literals(s)
s=s.replace('sp.getString("app_color","#20E070")','sp.getString("app_color","#B8007D")')
main.write_text(s,encoding='utf-8')

for p in list((root/'app/src/main/java/fun/greenplay/app').glob('*.java'))+list((root/'app/src/main/res').rglob('*.xml')):
    if p==main: continue
    try: z=p.read_text(encoding='utf-8')
    except Exception: continue
    nz=shift_green_literals(z)
    nz=nz.replace('#20E070','#B8007D').replace('#20e070','#b8007d')
    if nz!=z: p.write_text(nz,encoding='utf-8')

(root/'app/RELEASE_NOTES.txt').write_text('''Yelly Doramas 1.0.1
Logo, fundo e cor agora sincronizam com o painel Yelly.
Removidos os tons verdes restantes da interface Yelly.
Login entra no catálogo imediatamente após autenticação.
Identificador aceita usuário, e-mail ou código de acesso.
''',encoding='utf-8')
print('YELLY_101_PATCH_OK')
