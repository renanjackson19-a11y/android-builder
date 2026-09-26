from pathlib import Path

root=Path("work")
java=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
gradle=root/"app/build.gradle"

s=java.read_text(encoding="utf-8")
old=''' void login(){authScreen=true;base(true);try{getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE|WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);}catch(Exception ignored){}ScrollView scroll=new ScrollView(this);scroll.setFillViewport(true);scroll.setClipToPadding(false);scroll.setPadding(0,0,0,dp(tvMode?72:28));LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setGravity(Gravity.CENTER_VERTICAL|Gravity.CENTER_HORIZONTAL);c.setMinimumHeight(getResources().getDisplayMetrics().heightPixels-dp(170));int authSide=wideTvUi()?Math.max(dp(48),(getResources().getDisplayMetrics().widthPixels-dp(560))/2):0;c.setPadding(authSide,dp(12),authSide,dp(tvMode?110:52));scroll.addView(c,new ScrollView.LayoutParams(-1,-2));root.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));installAuthKeyboardLift(scroll,c);
  if(!logoUrl.isEmpty()){ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);logo.setAdjustViewBounds(true);logo.setContentDescription(appName);Img.load(logo,logoUrl);LinearLayout.LayoutParams logoLp=new LinearLayout.LayoutParams(-1,dp(82));logoLp.setMargins(dp(24),dp(2),dp(24),0);c.addView(logo,logoLp);}else{TextView logo=t("",35);String brand=(appName==null||appName.trim().isEmpty())?"GreenPlay":appName.trim();android.text.SpannableString ls=new android.text.SpannableString(brand+" ▶");int split=Math.min(5,brand.length());ls.setSpan(new android.text.style.ForegroundColorSpan(Color.WHITE),0,split,android.text.Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);ls.setSpan(new android.text.style.ForegroundColorSpan(GREEN),split,ls.length(),android.text.Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);logo.setText(ls);logo.setTypeface(null,1);logo.setGravity(Gravity.CENTER);logo.setPadding(0,dp(10),0,0);c.addView(logo,new LinearLayout.LayoutParams(-1,dp(66)));}TextView tag=t("MAIS QUE ENTRETENIMENTO",11);tag.setTextColor(0xffc8cfcb);tag.setGravity(Gravity.CENTER);tag.setLetterSpacing(.28f);tag.setPadding(0,0,0,dp(22));c.addView(tag);
  TextView title=t("Bem-vindo de volta!",27);title.setTypeface(null,1);title.setGravity(Gravity.CENTER);title.setPadding(0,dp(4),0,0);c.addView(title);TextView sub=t("Faça login para continuar assistindo.",16);sub.setTextColor(0xffb6b9b7);sub.setGravity(Gravity.CENTER);sub.setPadding(0,dp(4),0,dp(12));c.addView(sub);
'''
new=''' void login(){authScreen=true;base(true);try{getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE|WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);}catch(Exception ignored){}
  if(tvMode)root.setPadding(dp(16),dp(6),dp(16),dp(6));
  ScrollView scroll=new ScrollView(this);scroll.setFillViewport(true);scroll.setClipToPadding(false);scroll.setVerticalScrollBarEnabled(false);scroll.setPadding(0,0,0,dp(tvMode?0:28));LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setGravity(Gravity.CENTER_VERTICAL|Gravity.CENTER_HORIZONTAL);
  int screenW=getResources().getDisplayMetrics().widthPixels,screenH=getResources().getDisplayMetrics().heightPixels;int authSide=0;
  if(tvMode){int target=Math.min(screenW-dp(52),Math.max(dp(700),(int)(screenW*.74f)));authSide=Math.max(dp(26),(screenW-target)/2);c.setMinimumHeight(Math.max(dp(520),screenH-dp(20)));c.setPadding(authSide,dp(2),authSide,dp(16));}else{c.setMinimumHeight(screenH-dp(170));c.setPadding(0,dp(12),0,dp(52));}
  scroll.addView(c,new ScrollView.LayoutParams(-1,-2));root.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));installAuthKeyboardLift(scroll,c);
  if(tvMode){ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);logo.setAdjustViewBounds(true);logo.setContentDescription(appName);applyAppLogo(logo);LinearLayout.LayoutParams logoLp=new LinearLayout.LayoutParams(-1,dp(112));logoLp.setMargins(dp(18),0,dp(18),dp(2));c.addView(logo,logoLp);}else if(!logoUrl.isEmpty()){ImageView logo=new ImageView(this);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);logo.setAdjustViewBounds(true);logo.setContentDescription(appName);Img.load(logo,logoUrl);LinearLayout.LayoutParams logoLp=new LinearLayout.LayoutParams(-1,dp(82));logoLp.setMargins(dp(24),dp(2),dp(24),0);c.addView(logo,logoLp);}else{TextView logo=t("",35);String brand=(appName==null||appName.trim().isEmpty())?"GreenPlay":appName.trim();android.text.SpannableString ls=new android.text.SpannableString(brand+" ▶");int split=Math.min(5,brand.length());ls.setSpan(new android.text.style.ForegroundColorSpan(Color.WHITE),0,split,android.text.Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);ls.setSpan(new android.text.style.ForegroundColorSpan(GREEN),split,ls.length(),android.text.Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);logo.setText(ls);logo.setTypeface(null,1);logo.setGravity(Gravity.CENTER);logo.setPadding(0,dp(10),0,0);c.addView(logo,new LinearLayout.LayoutParams(-1,dp(66)));}TextView tag=t("MAIS QUE ENTRETENIMENTO",11);tag.setTextColor(0xffc8cfcb);tag.setGravity(Gravity.CENTER);tag.setLetterSpacing(.28f);tag.setPadding(0,0,0,dp(tvMode?8:22));c.addView(tag);
  TextView title=t("Bem-vindo de volta!",tvMode?24:27);title.setTypeface(null,1);title.setGravity(Gravity.CENTER);title.setPadding(0,dp(tvMode?0:4),0,0);c.addView(title);TextView sub=t("Faça login para continuar assistindo.",tvMode?14:16);sub.setTextColor(0xffb6b9b7);sub.setGravity(Gravity.CENTER);sub.setPadding(0,dp(2),0,dp(tvMode?8:12));c.addView(sub);
'''
if old not in s:
    raise SystemExit("TV login base block not found")
s=s.replace(old,new,1)
java.write_text(s,encoding="utf-8")

g=gradle.read_text(encoding="utf-8")
if "versionCode 52897" not in g or "versionName '5.28.97'" not in g:
    raise SystemExit("Unexpected base version")
g=g.replace("versionCode 52897","versionCode 52898",1)
g=g.replace("versionName '5.28.97'","versionName '5.28.98'",1)
gradle.write_text(g,encoding="utf-8")
print("GreenPlay 5.28.98 TV login responsive patch applied")
