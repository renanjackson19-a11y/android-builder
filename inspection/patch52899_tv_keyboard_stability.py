from pathlib import Path

root=Path("work")
java=root/"app/src/main/java/fun/greenplay/app/MainActivity.java"
gradle=root/"app/build.gradle"
s=java.read_text(encoding="utf-8")

old=''' @Override public boolean dispatchKeyEvent(KeyEvent e){
  if(tvMode&&e!=null){
   int key=e.getKeyCode();
   // v16.204: controles da TV continuam ativos em tela cheia.
'''
new=''' @Override public boolean dispatchKeyEvent(KeyEvent e){
  if(tvMode&&e!=null){
   int key=e.getKeyCode();
   // 5.28.99: enquanto o teclado da TV estiver aberto, o controle pertence ao IME.
   // Não intercepta setas/OK para não reabrir o teclado a cada tecla nem travar TV Box.
   View focused=getCurrentFocus();boolean imeField=tvImeActive&&focused instanceof EditText&&focused.isShown()&&focused.isEnabled();
   if(imeField){
    boolean backKey=key==KeyEvent.KEYCODE_BACK||key==KeyEvent.KEYCODE_ESCAPE||key==KeyEvent.KEYCODE_BUTTON_B;
    if(backKey){if(e.getAction()==KeyEvent.ACTION_DOWN&&e.getRepeatCount()==0){hideKeyboard(focused);return true;}if(e.getAction()==KeyEvent.ACTION_UP)return true;}
    return super.dispatchKeyEvent(e);
   }
   // v16.204: controles da TV continuam ativos em tela cheia.
'''
assert old in s
s=s.replace(old,new,1)

old=''' void prepareTvTextInput(EditText input){if(!tvMode||input==null)return;input.setFocusable(true);input.setFocusableInTouchMode(true);input.setClickable(true);input.setCursorVisible(true);if(android.os.Build.VERSION.SDK_INT>=21)try{input.setShowSoftInputOnFocus(true);}catch(Exception ignored){}if(tvInputArmed.containsKey(input))return;tvInputArmed.put(input,Boolean.TRUE);input.setOnKeyListener((v,key,event)->{if(event==null||event.getAction()!=KeyEvent.ACTION_DOWN||event.getRepeatCount()!=0)return false;if(isTvConfirmKeyCode(key)){showTvKeyboard((EditText)v);return true;}return false;});}
'''
new=''' void prepareTvTextInput(EditText input){if(!tvMode||input==null)return;input.setFocusable(true);input.setFocusableInTouchMode(true);input.setClickable(true);input.setCursorVisible(true);if(android.os.Build.VERSION.SDK_INT>=21)try{input.setShowSoftInputOnFocus(true);}catch(Exception ignored){}if(tvInputArmed.containsKey(input))return;tvInputArmed.put(input,Boolean.TRUE);input.setOnKeyListener((v,key,event)->{if(tvImeActive)return false;if(event==null||event.getAction()!=KeyEvent.ACTION_DOWN||event.getRepeatCount()!=0)return false;if(isTvConfirmKeyCode(key)){showTvKeyboard((EditText)v);return true;}return false;});}
'''
assert old in s
s=s.replace(old,new,1)

old=''' void keepInputAboveKeyboard(EditText input){if(input==null)return;ScrollView sv=parentScroll(input);if(sv==null)return;Runnable move=()->{try{android.graphics.Rect visible=new android.graphics.Rect();View decor=getWindow().getDecorView();decor.getWindowVisibleDisplayFrame(visible);int[] loc=new int[2];input.getLocationOnScreen(loc);int fieldBottom=loc[1]+input.getHeight();int safeBottom=visible.bottom-dp(tvMode?72:46);if(fieldBottom>safeBottom){int delta=fieldBottom-safeBottom+dp(tvMode?36:22);sv.scrollBy(0,Math.max(0,delta));}android.graphics.Rect r=new android.graphics.Rect(0,0,input.getWidth(),input.getHeight()+dp(tvMode?90:58));input.requestRectangleOnScreen(r,true);}catch(Exception ignored){}};sv.post(move);sv.postDelayed(move,90);sv.postDelayed(move,220);sv.postDelayed(move,420);sv.postDelayed(move,650);}
 void installAuthKeyboardLift(ScrollView sv,LinearLayout content){if(sv==null||content==null)return;final View decor=getWindow().getDecorView();decor.getViewTreeObserver().addOnGlobalLayoutListener(()->{try{android.graphics.Rect visible=new android.graphics.Rect();decor.getWindowVisibleDisplayFrame(visible);int rootH=decor.getRootView().getHeight();int hidden=Math.max(0,rootH-visible.bottom);boolean keyboardOpen=hidden>Math.max(dp(140),rootH/6);content.setGravity((keyboardOpen?Gravity.TOP:Gravity.CENTER_VERTICAL)|Gravity.CENTER_HORIZONTAL);if(keyboardOpen){View f=getCurrentFocus();if(f instanceof EditText){EditText e=(EditText)f;keepInputAboveKeyboard(e);sv.postDelayed(()->keepInputAboveKeyboard(e),120);}}}catch(Exception ignored){}});}
 void showTvKeyboard(EditText input){if(input==null)return;tvImeActive=true;prepareTvTextInput(input);try{getWindow().clearFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE);getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE|WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_VISIBLE);input.setFocusable(true);input.setFocusableInTouchMode(true);input.setCursorVisible(true);if(android.os.Build.VERSION.SDK_INT>=21)input.setShowSoftInputOnFocus(true);input.requestFocus();input.setSelection(input.length());keepInputAboveKeyboard(input);}catch(Exception ignored){}Runnable open=()->{try{android.view.inputmethod.InputMethodManager im=(android.view.inputmethod.InputMethodManager)getSystemService(INPUT_METHOD_SERVICE);if(im!=null&&input.getWindowToken()!=null){input.requestFocus();im.restartInput(input);boolean shown=im.showSoftInput(input,android.view.inputmethod.InputMethodManager.SHOW_IMPLICIT);keepInputAboveKeyboard(input);input.postDelayed(()->{try{if(!shown||!im.isActive(input)){input.requestFocus();im.restartInput(input);im.showSoftInput(input,android.view.inputmethod.InputMethodManager.SHOW_FORCED);}keepInputAboveKeyboard(input);}catch(Exception ignored2){}},180);input.postDelayed(()->{try{im.showSoftInput(input,android.view.inputmethod.InputMethodManager.SHOW_FORCED);keepInputAboveKeyboard(input);}catch(Exception ignored3){}},420);}}catch(Exception ignored){}};input.post(open);input.postDelayed(open,80);}
'''
new=''' void keepInputAboveKeyboard(EditText input){if(input==null)return;ScrollView sv=parentScroll(input);if(sv==null)return;Runnable move=()->{try{android.graphics.Rect visible=new android.graphics.Rect();View decor=getWindow().getDecorView();decor.getWindowVisibleDisplayFrame(visible);int[] loc=new int[2];input.getLocationOnScreen(loc);int fieldBottom=loc[1]+input.getHeight();int safeBottom=visible.bottom-dp(tvMode?72:46);if(fieldBottom>safeBottom){int delta=fieldBottom-safeBottom+dp(tvMode?36:22);sv.scrollBy(0,Math.max(0,delta));}android.graphics.Rect r=new android.graphics.Rect(0,0,input.getWidth(),input.getHeight()+dp(tvMode?90:58));input.requestRectangleOnScreen(r,true);}catch(Exception ignored){}};sv.post(move);sv.postDelayed(move,120);}
 void installAuthKeyboardLift(ScrollView sv,LinearLayout content){if(sv==null||content==null)return;final View decor=getWindow().getDecorView();final boolean[] wasOpen={false};final Runnable[] pending={null};decor.getViewTreeObserver().addOnGlobalLayoutListener(()->{try{android.graphics.Rect visible=new android.graphics.Rect();decor.getWindowVisibleDisplayFrame(visible);int rootH=decor.getRootView().getHeight();int hidden=Math.max(0,rootH-visible.bottom);boolean keyboardOpen=hidden>Math.max(dp(140),rootH/6);if(keyboardOpen!=wasOpen[0])content.setGravity((keyboardOpen?Gravity.TOP:Gravity.CENTER_VERTICAL)|Gravity.CENTER_HORIZONTAL);if(keyboardOpen){View f=getCurrentFocus();if(f instanceof EditText){EditText field=(EditText)f;if(pending[0]!=null)sv.removeCallbacks(pending[0]);pending[0]=()->{if(tvImeActive&&field==getCurrentFocus())keepInputAboveKeyboard(field);};sv.postDelayed(pending[0],90);}}else if(wasOpen[0])tvImeActive=false;wasOpen[0]=keyboardOpen;}catch(Exception ignored){}});}
 void showTvKeyboard(EditText input){if(input==null)return;try{android.view.inputmethod.InputMethodManager active=(android.view.inputmethod.InputMethodManager)getSystemService(INPUT_METHOD_SERVICE);if(tvImeActive&&input.hasFocus()&&active!=null&&active.isActive(input)){keepInputAboveKeyboard(input);return;}}catch(Exception ignored){}tvImeActive=true;prepareTvTextInput(input);try{getWindow().clearFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE);getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE|WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_VISIBLE);input.setFocusable(true);input.setFocusableInTouchMode(true);input.setCursorVisible(true);if(android.os.Build.VERSION.SDK_INT>=21)input.setShowSoftInputOnFocus(true);input.requestFocus();input.setSelection(input.length());keepInputAboveKeyboard(input);}catch(Exception ignored){}input.post(()->{try{android.view.inputmethod.InputMethodManager im=(android.view.inputmethod.InputMethodManager)getSystemService(INPUT_METHOD_SERVICE);if(im!=null&&input.getWindowToken()!=null){input.requestFocus();im.restartInput(input);boolean shown=im.showSoftInput(input,android.view.inputmethod.InputMethodManager.SHOW_IMPLICIT);keepInputAboveKeyboard(input);if(!shown)input.postDelayed(()->{try{if(tvImeActive&&input.hasFocus()&&!im.isActive(input)){im.restartInput(input);im.showSoftInput(input,android.view.inputmethod.InputMethodManager.SHOW_IMPLICIT);keepInputAboveKeyboard(input);}}catch(Exception ignored2){}},180);}}catch(Exception ignored){}});}
'''
assert old in s
s=s.replace(old,new,1)

old='''if(tvMode){from.setOnClickListener(v->showTvKeyboard(from));from.setOnKeyListener((v,key,event)->{if(event==null||event.getAction()!=KeyEvent.ACTION_DOWN||event.getRepeatCount()!=0)return false;if(isTvConfirmKeyCode(key)){showTvKeyboard(from);return true;}return false;});}}'''
new='''if(tvMode){from.setOnClickListener(v->showTvKeyboard(from));from.setOnKeyListener((v,key,event)->{if(tvImeActive)return false;if(event==null||event.getAction()!=KeyEvent.ACTION_DOWN||event.getRepeatCount()!=0)return false;if(isTvConfirmKeyCode(key)){showTvKeyboard(from);return true;}return false;});}}'''
assert old in s
s=s.replace(old,new,1)
java.write_text(s,encoding="utf-8")

g=gradle.read_text(encoding="utf-8")
assert "versionCode 52898" in g and "versionName '5.28.98'" in g
g=g.replace("versionCode 52898","versionCode 52899",1)
g=g.replace("versionName '5.28.98'","versionName '5.28.99'",1)
gradle.write_text(g,encoding="utf-8")
print("GreenPlay 5.28.99 TV keyboard stability patch applied")
