from pathlib import Path

main = Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s = main.read_text(encoding="utf-8")

def rep(old, new, n=1):
    global s
    if old not in s:
        raise SystemExit("anchor not found: " + old[:160])
    s = s.replace(old, new, n)

rep(
    "boolean authScreen=false,detailOpen=false,searchScreenOpen=false,exitDialogOpen=false,providerSwitchScreen=false,plansScreen=false,providerAvailabilityCheckBusy=false;",
    "boolean authScreen=false,detailOpen=false,searchScreenOpen=false,exitDialogOpen=false,providerSwitchScreen=false,plansScreen=false,providerAvailabilityCheckBusy=false,tvImeActive=false; java.util.WeakHashMap<EditText,Boolean> tvInputArmed=new java.util.WeakHashMap<>();"
)

rep(
    "if(tvMode&&!modeSwitchPending)enterTvImmersiveUi();",
    "if(tvMode&&!modeSwitchPending&&!tvImeActive)enterTvImmersiveUi();"
)

rep(
    "@Override public void onWindowFocusChanged(boolean hasFocus){super.onWindowFocusChanged(hasFocus);if(hasFocus&&tvMode&&!tvInlineFullscreen&&!authScreen)enterTvImmersiveUi();}",
    "@Override public void onWindowFocusChanged(boolean hasFocus){super.onWindowFocusChanged(hasFocus);if(hasFocus&&tvMode&&!tvInlineFullscreen&&!authScreen){View f=getCurrentFocus();if(!(f instanceof EditText))tvImeActive=false;if(!tvImeActive)enterTvImmersiveUi();}}"
)

rep(
'''   if(isTvConfirmKeyCode(key)){
    if(e.getAction()==KeyEvent.ACTION_DOWN&&e.getRepeatCount()==0){View f=getCurrentFocus();if(f!=null&&f.isShown()&&f.isEnabled()&&f.isClickable()&&!(f instanceof EditText)&&!(f instanceof SeekBar)){f.performClick();return true;}}
    if(e.getAction()==KeyEvent.ACTION_UP)return true;
   }''',
'''   if(isTvConfirmKeyCode(key)){
    if(e.getAction()==KeyEvent.ACTION_DOWN&&e.getRepeatCount()==0){
     View f=getCurrentFocus();
     if(f instanceof EditText&&f.isShown()&&f.isEnabled()){showTvKeyboard((EditText)f);return true;}
     if(f!=null&&f.isShown()&&f.isEnabled()&&f.isClickable()&&!(f instanceof SeekBar)){f.performClick();return true;}
    }
    if(e.getAction()==KeyEvent.ACTION_UP)return true;
   }'''
)

rep(
    'EditText e(String hint,boolean pass){EditText v=new EditText(this);v.setHint(hint);v.setHintTextColor(0xff799087);v.setTextColor(Color.WHITE);uiTextSize(v,17);v.setSingleLine();v.setPadding(dp(16),dp(14),dp(16),dp(14));v.setBackground(round(CARD,14));if(pass)v.setInputType(InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_PASSWORD);return v;}',
    'EditText e(String hint,boolean pass){EditText v=new EditText(this);v.setHint(hint);v.setHintTextColor(0xff799087);v.setTextColor(Color.WHITE);uiTextSize(v,17);v.setSingleLine();v.setPadding(dp(16),dp(14),dp(16),dp(14));v.setBackground(round(CARD,14));if(pass)v.setInputType(InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_PASSWORD);if(tvMode)prepareTvTextInput(v);return v;}'
)

rep(
    'void prepareTvFocusTree(View v){if(!tvMode||v==null||v.getVisibility()!=View.VISIBLE)return;boolean input=v instanceof EditText||v instanceof SeekBar;boolean action=v.isClickable()||v instanceof Button||input;if(action){v.setFocusable(true);v.setFocusableInTouchMode(input);armTvFocus(v);}else if(v instanceof TextView){v.setFocusable(false);v.setFocusableInTouchMode(false);}if(v instanceof ViewGroup){ViewGroup g=(ViewGroup)v;for(int i=0;i<g.getChildCount();i++)prepareTvFocusTree(g.getChildAt(i));}}',
    'void prepareTvFocusTree(View v){if(!tvMode||v==null||v.getVisibility()!=View.VISIBLE)return;boolean input=v instanceof EditText||v instanceof SeekBar;boolean action=v.isClickable()||v instanceof Button||input;if(action){v.setFocusable(true);v.setFocusableInTouchMode(input);if(v instanceof EditText)prepareTvTextInput((EditText)v);armTvFocus(v);}else if(v instanceof TextView){v.setFocusable(false);v.setFocusableInTouchMode(false);}if(v instanceof ViewGroup){ViewGroup g=(ViewGroup)v;for(int i=0;i<g.getChildCount();i++)prepareTvFocusTree(g.getChildAt(i));}}'
)

rep(
'''void hideKeyboard(View anchor){try{android.view.inputmethod.InputMethodManager im=(android.view.inputmethod.InputMethodManager)getSystemService(INPUT_METHOD_SERVICE);View v=anchor!=null?anchor:getCurrentFocus();if(im!=null&&v!=null)im.hideSoftInputFromWindow(v.getWindowToken(),0);}catch(Exception ignored){}if(tvMode)new Handler(Looper.getMainLooper()).postDelayed(()->{try{enterTvImmersiveUi();}catch(Exception ignored){}},260);}
 ScrollView parentScroll(View v){View cur=v;while(cur!=null){android.view.ViewParent p=cur.getParent();if(p instanceof ScrollView)return (ScrollView)p;if(!(p instanceof View))break;cur=(View)p;}return null;}
 void keepInputAboveKeyboard(EditText input){if(input==null)return;ScrollView sv=parentScroll(input);if(sv==null)return;Runnable move=()->{try{android.graphics.Rect visible=new android.graphics.Rect();View decor=getWindow().getDecorView();decor.getWindowVisibleDisplayFrame(visible);int[] loc=new int[2];input.getLocationOnScreen(loc);int fieldBottom=loc[1]+input.getHeight();int safeBottom=visible.bottom-dp(tvMode?72:46);if(fieldBottom>safeBottom){int delta=fieldBottom-safeBottom+dp(tvMode?36:22);sv.scrollBy(0,Math.max(0,delta));}android.graphics.Rect r=new android.graphics.Rect(0,0,input.getWidth(),input.getHeight()+dp(tvMode?90:58));input.requestRectangleOnScreen(r,true);}catch(Exception ignored){}};sv.post(move);sv.postDelayed(move,90);sv.postDelayed(move,220);sv.postDelayed(move,420);sv.postDelayed(move,650);}
 void installAuthKeyboardLift(ScrollView sv,LinearLayout content){if(sv==null||content==null)return;final View decor=getWindow().getDecorView();decor.getViewTreeObserver().addOnGlobalLayoutListener(()->{try{android.graphics.Rect visible=new android.graphics.Rect();decor.getWindowVisibleDisplayFrame(visible);int rootH=decor.getRootView().getHeight();int hidden=Math.max(0,rootH-visible.bottom);boolean keyboardOpen=hidden>Math.max(dp(140),rootH/6);content.setGravity((keyboardOpen?Gravity.TOP:Gravity.CENTER_VERTICAL)|Gravity.CENTER_HORIZONTAL);if(keyboardOpen){View f=getCurrentFocus();if(f instanceof EditText){EditText e=(EditText)f;keepInputAboveKeyboard(e);sv.postDelayed(()->keepInputAboveKeyboard(e),120);}}}catch(Exception ignored){}});}
 void showTvKeyboard(EditText input){if(input==null)return;try{getWindow().clearFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE);getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE|WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_VISIBLE);input.setFocusable(true);input.setFocusableInTouchMode(true);input.setCursorVisible(true);input.requestFocus();input.setSelection(input.length());keepInputAboveKeyboard(input);}catch(Exception ignored){}Runnable open=()->{try{android.view.inputmethod.InputMethodManager im=(android.view.inputmethod.InputMethodManager)getSystemService(INPUT_METHOD_SERVICE);if(im!=null){input.requestFocus();im.showSoftInput(input,android.view.inputmethod.InputMethodManager.SHOW_IMPLICIT);keepInputAboveKeyboard(input);input.postDelayed(()->{try{if(!im.isActive(input))im.showSoftInput(input,android.view.inputmethod.InputMethodManager.SHOW_FORCED);keepInputAboveKeyboard(input);}catch(Exception ignored2){}},180);}}catch(Exception ignored){}};input.postDelayed(open,70);}''',
'''void hideKeyboard(View anchor){tvImeActive=false;try{android.view.inputmethod.InputMethodManager im=(android.view.inputmethod.InputMethodManager)getSystemService(INPUT_METHOD_SERVICE);View v=anchor!=null?anchor:getCurrentFocus();if(im!=null&&v!=null)im.hideSoftInputFromWindow(v.getWindowToken(),0);}catch(Exception ignored){}if(tvMode)new Handler(Looper.getMainLooper()).postDelayed(()->{try{if(!tvImeActive)enterTvImmersiveUi();}catch(Exception ignored){}},260);}
 void prepareTvTextInput(EditText input){if(!tvMode||input==null)return;input.setFocusable(true);input.setFocusableInTouchMode(true);input.setClickable(true);input.setCursorVisible(true);if(android.os.Build.VERSION.SDK_INT>=21)try{input.setShowSoftInputOnFocus(true);}catch(Exception ignored){}if(tvInputArmed.containsKey(input))return;tvInputArmed.put(input,Boolean.TRUE);input.setOnKeyListener((v,key,event)->{if(event==null||event.getAction()!=KeyEvent.ACTION_DOWN||event.getRepeatCount()!=0)return false;if(isTvConfirmKeyCode(key)){showTvKeyboard((EditText)v);return true;}return false;});}
 ScrollView parentScroll(View v){View cur=v;while(cur!=null){android.view.ViewParent p=cur.getParent();if(p instanceof ScrollView)return (ScrollView)p;if(!(p instanceof View))break;cur=(View)p;}return null;}
 void keepInputAboveKeyboard(EditText input){if(input==null)return;ScrollView sv=parentScroll(input);if(sv==null)return;Runnable move=()->{try{android.graphics.Rect visible=new android.graphics.Rect();View decor=getWindow().getDecorView();decor.getWindowVisibleDisplayFrame(visible);int[] loc=new int[2];input.getLocationOnScreen(loc);int fieldBottom=loc[1]+input.getHeight();int safeBottom=visible.bottom-dp(tvMode?72:46);if(fieldBottom>safeBottom){int delta=fieldBottom-safeBottom+dp(tvMode?36:22);sv.scrollBy(0,Math.max(0,delta));}android.graphics.Rect r=new android.graphics.Rect(0,0,input.getWidth(),input.getHeight()+dp(tvMode?90:58));input.requestRectangleOnScreen(r,true);}catch(Exception ignored){}};sv.post(move);sv.postDelayed(move,90);sv.postDelayed(move,220);sv.postDelayed(move,420);sv.postDelayed(move,650);}
 void installAuthKeyboardLift(ScrollView sv,LinearLayout content){if(sv==null||content==null)return;final View decor=getWindow().getDecorView();decor.getViewTreeObserver().addOnGlobalLayoutListener(()->{try{android.graphics.Rect visible=new android.graphics.Rect();decor.getWindowVisibleDisplayFrame(visible);int rootH=decor.getRootView().getHeight();int hidden=Math.max(0,rootH-visible.bottom);boolean keyboardOpen=hidden>Math.max(dp(140),rootH/6);content.setGravity((keyboardOpen?Gravity.TOP:Gravity.CENTER_VERTICAL)|Gravity.CENTER_HORIZONTAL);if(keyboardOpen){View f=getCurrentFocus();if(f instanceof EditText){EditText e=(EditText)f;keepInputAboveKeyboard(e);sv.postDelayed(()->keepInputAboveKeyboard(e),120);}}}catch(Exception ignored){}});}
 void showTvKeyboard(EditText input){if(input==null)return;tvImeActive=true;prepareTvTextInput(input);try{getWindow().clearFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE);getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE|WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_VISIBLE);input.setFocusable(true);input.setFocusableInTouchMode(true);input.setCursorVisible(true);if(android.os.Build.VERSION.SDK_INT>=21)input.setShowSoftInputOnFocus(true);input.requestFocus();input.setSelection(input.length());keepInputAboveKeyboard(input);}catch(Exception ignored){}Runnable open=()->{try{android.view.inputmethod.InputMethodManager im=(android.view.inputmethod.InputMethodManager)getSystemService(INPUT_METHOD_SERVICE);if(im!=null&&input.getWindowToken()!=null){input.requestFocus();im.restartInput(input);boolean shown=im.showSoftInput(input,android.view.inputmethod.InputMethodManager.SHOW_IMPLICIT);keepInputAboveKeyboard(input);input.postDelayed(()->{try{if(!shown||!im.isActive(input)){input.requestFocus();im.restartInput(input);im.showSoftInput(input,android.view.inputmethod.InputMethodManager.SHOW_FORCED);}keepInputAboveKeyboard(input);}catch(Exception ignored2){}},180);input.postDelayed(()->{try{im.showSoftInput(input,android.view.inputmethod.InputMethodManager.SHOW_FORCED);keepInputAboveKeyboard(input);}catch(Exception ignored3){}},420);}}catch(Exception ignored){}};input.post(open);input.postDelayed(open,80);}'''
)

rep(
'''if(tvMode){from.setOnClickListener(v->showTvKeyboard(from));from.setOnKeyListener((v,key,event)->{if(event==null||event.getAction()!=KeyEvent.ACTION_DOWN)return false;if(key==KeyEvent.KEYCODE_DPAD_CENTER||key==KeyEvent.KEYCODE_ENTER||key==KeyEvent.KEYCODE_NUMPAD_ENTER){showTvKeyboard(from);return true;}return false;});}}''',
'''if(tvMode){from.setOnClickListener(v->showTvKeyboard(from));from.setOnKeyListener((v,key,event)->{if(event==null||event.getAction()!=KeyEvent.ACTION_DOWN||event.getRepeatCount()!=0)return false;if(isTvConfirmKeyCode(key)){showTvKeyboard(from);return true;}return false;});}}'''
)

rep(
    'EditText authEdit(String hint,boolean pass,int icon){EditText v=new EditText(this);v.setHint(hint);v.setHintTextColor(0xffa9aeac);v.setTextColor(Color.WHITE);uiTextSize(v,17);v.setSingleLine();v.setPadding(dp(20),0,dp(18),0);v.setBackground(authFieldSelector());v.setCompoundDrawablesWithIntrinsicBounds(icon,0,pass?R.drawable.ic_eye_off:0,0);v.setCompoundDrawablePadding(dp(14));v.setFocusable(true);v.setFocusableInTouchMode(true);if(pass)v.setInputType(InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_PASSWORD);return v;}',
    'EditText authEdit(String hint,boolean pass,int icon){EditText v=new EditText(this);v.setHint(hint);v.setHintTextColor(0xffa9aeac);v.setTextColor(Color.WHITE);uiTextSize(v,17);v.setSingleLine();v.setPadding(dp(20),0,dp(18),0);v.setBackground(authFieldSelector());v.setCompoundDrawablesWithIntrinsicBounds(icon,0,pass?R.drawable.ic_eye_off:0,0);v.setCompoundDrawablePadding(dp(14));v.setFocusable(true);v.setFocusableInTouchMode(true);if(pass)v.setInputType(InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_PASSWORD);if(tvMode)prepareTvTextInput(v);return v;}'
)

rep(
    'screen.addView(page,new ScrollView.LayoutParams(-1,-2));root.addView(screen,new LinearLayout.LayoutParams(-1,0,1));',
    'screen.addView(page,new ScrollView.LayoutParams(-1,-2));root.addView(screen,new LinearLayout.LayoutParams(-1,0,1));installAuthKeyboardLift(screen,page);'
)

rep(
    'EditText q=new EditText(this);q.setHint("Buscar");',
    'EditText q=new EditText(this);if(tvMode)prepareTvTextInput(q);q.setHint("Buscar");'
)

rep(
'''void stabilizeInputDialog(Dialog d,View card){
  if(card!=null){card.setFocusableInTouchMode(true);card.requestFocus();}
  Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));w.setDimAmount(.72f);w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);w.setGravity(Gravity.CENTER);w.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_NOTHING|WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);WindowManager.LayoutParams lp=w.getAttributes();lp.windowAnimations=0;w.setAttributes(lp);}
 }
 void sizeStableInputDialog(Dialog d,View focusRoot){Window w=d.getWindow();if(w==null)return;w.setLayout(Math.min(getResources().getDisplayMetrics().widthPixels-dp(38),dp(500)),-2);WindowManager.LayoutParams lp=w.getAttributes();lp.windowAnimations=0;w.setAttributes(lp);if(focusRoot!=null){focusRoot.setFocusableInTouchMode(true);focusRoot.requestFocus();}}''',
'''void stabilizeInputDialog(Dialog d,View card){
  if(card!=null){if(tvMode){card.setFocusable(false);prepareTvFocusTree(card);}else{card.setFocusableInTouchMode(true);card.requestFocus();}}
  Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));w.setDimAmount(.72f);w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);w.setGravity(Gravity.CENTER);w.setSoftInputMode((tvMode?WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE:WindowManager.LayoutParams.SOFT_INPUT_ADJUST_NOTHING)|WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);WindowManager.LayoutParams lp=w.getAttributes();lp.windowAnimations=0;w.setAttributes(lp);}
  d.setOnDismissListener(x->{tvImeActive=false;if(tvMode)new Handler(Looper.getMainLooper()).postDelayed(()->{try{enterTvImmersiveUi();}catch(Exception ignored){}},180);});
 }
 void sizeStableInputDialog(Dialog d,View focusRoot){Window w=d.getWindow();if(w==null)return;w.setLayout(Math.min(getResources().getDisplayMetrics().widthPixels-dp(38),dp(500)),-2);WindowManager.LayoutParams lp=w.getAttributes();lp.windowAnimations=0;w.setAttributes(lp);if(focusRoot!=null){if(tvMode)prepareTvFocusTree(focusRoot);else{focusRoot.setFocusableInTouchMode(true);focusRoot.requestFocus();}}}'''
)

rep(
'''cancel.setOnClickListener(v->d.dismiss());save.setOnClickListener(v->{String a=p1.getText().toString();if(a.length()<6){err.setText("Use pelo menos 6 caracteres.");return;}if(!a.equals(p2.getText().toString())){err.setText("As senhas não coincidem.");return;}save.setEnabled(false);err.setText("");Api.post("change_password",Api.m("user_id",uid,"password",a),new Api.CB(){public void ok(JSONObject j){runOnUiThread(()->{if(j.optInt("status",200)!=200){save.setEnabled(true);err.setText(j.optString("message","Não foi possível alterar a senha."));return;}d.dismiss();showAppNotice("Senha atualizada",false);});}public void err(String z){runOnUiThread(()->{save.setEnabled(true);err.setText(z==null||z.isEmpty()?"Não foi possível alterar a senha.":z);});}});});d.setContentView(card);stabilizeInputDialog(d,card);d.setOnShowListener(x->sizeStableInputDialog(d,card));d.show();''',
'''cancel.setOnClickListener(v->d.dismiss());save.setOnClickListener(v->{String a=p1.getText().toString();if(a.length()<6){err.setText("Use pelo menos 6 caracteres.");return;}if(!a.equals(p2.getText().toString())){err.setText("As senhas não coincidem.");return;}save.setEnabled(false);err.setText("");Api.post("change_password",Api.m("user_id",uid,"password",a),new Api.CB(){public void ok(JSONObject j){runOnUiThread(()->{if(j.optInt("status",200)!=200){save.setEnabled(true);err.setText(j.optString("message","Não foi possível alterar a senha."));return;}d.dismiss();showAppNotice("Senha atualizada",false);});}public void err(String z){runOnUiThread(()->{save.setEnabled(true);err.setText(z==null||z.isEmpty()?"Não foi possível alterar a senha.":z);});}});});if(tvMode){bindImeMove(p1,p2,android.view.inputmethod.EditorInfo.IME_ACTION_NEXT);bindImeMove(p2,save,android.view.inputmethod.EditorInfo.IME_ACTION_DONE);linkTvVertical(p1,p2);linkTvVertical(p2,save);}d.setContentView(card);stabilizeInputDialog(d,card);d.setOnShowListener(x->{sizeStableInputDialog(d,card);if(tvMode)requestTvFocus(p1);});d.show();'''
)

s = s.replace(
    '(key==KeyEvent.KEYCODE_ENTER||key==KeyEvent.KEYCODE_DPAD_CENTER||key==KeyEvent.KEYCODE_NUMPAD_ENTER)',
    'isTvConfirmKeyCode(key)'
)

main.write_text(s, encoding="utf-8")

gradle = Path("work/app/build.gradle")
g = gradle.read_text(encoding="utf-8")
g = g.replace("versionCode 52896", "versionCode 52897")
g = g.replace("versionName '5.28.96'", "versionName '5.28.97'")
gradle.write_text(g, encoding="utf-8")

notes = Path("work/app/RELEASE_NOTES.txt")
old = notes.read_text(encoding="utf-8") if notes.exists() else ""
notes.write_text(
    "Correção global do teclado em Fire TV Stick, Android TV e TV Box.\n"
    "OK em qualquer campo de texto abre o teclado do sistema no modo TV.\n"
    "Formulários e diálogos com senha/PIN agora ajustam a tela ao teclado.\n"
    "Tela de cadastro se move para manter o campo selecionado visível.\n" + old,
    encoding="utf-8"
)
