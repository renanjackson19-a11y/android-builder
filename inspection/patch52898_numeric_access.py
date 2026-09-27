from pathlib import Path

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text(encoding="utf-8")

def rep(old,new,n=1):
    global s
    if old not in s:
        raise SystemExit("anchor not found: "+old[:180])
    s=s.replace(old,new,n)

rep(
'''  // v5.15: login identifica automaticamente a conta e a revenda pelo usuário/e-mail/código de acesso.
c.addView(authLabel("Usuário, e-mail ou código de acesso"));EditText email=authEdit("Digite usuário, e-mail ou código",false,R.drawable.ic_email);''',
'''  // v5.28.98: acesso simples, somente usuário + senha.
c.addView(authLabel("Usuário"));EditText email=authEdit("Digite seu usuário de 8 dígitos",false,R.drawable.ic_email);'''
)
rep('EditText pass=authEdit("Sua senha",true,R.drawable.ic_lock);','EditText pass=authEdit("Sua senha de 8 dígitos",true,R.drawable.ic_lock);')
rep(
'''TextView reset=t("Esqueci minha senha",13);reset.setTextColor(0xffb9bebc);reset.setGravity(Gravity.RIGHT);reset.setPadding(0,dp(6),dp(4),dp(10));reset.setOnClickListener(v->showForgotPasswordDialog(email));c.addView(reset);
  Button go=authPrimary("Entrar  →");''',
'''  Button go=authPrimary("Entrar  →");'''
)
rep('msg.setText("Informe usuário, e-mail ou código e a senha.");','msg.setText("Informe usuário e senha.");')

start=s.index(' void registerScreen(){')
end=s.index(' void doLogin(',start)
newreg=r''' void registerScreen(){
  authScreen=true;base(true);
  TextView back=t("‹ Voltar",16);back.setTextColor(GREEN);back.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);back.setOnClickListener(v->login());root.addView(back,new LinearLayout.LayoutParams(-1,dp(44)));
  ScrollView screen=new ScrollView(this);screen.setFillViewport(true);screen.setClipToPadding(false);screen.setVerticalScrollBarEnabled(false);LinearLayout page=new LinearLayout(this);page.setOrientation(LinearLayout.VERTICAL);page.setGravity(Gravity.CENTER_HORIZONTAL);int side=wideTvUi()?Math.max(dp(48),(getResources().getDisplayMetrics().widthPixels-dp(620))/2):0;page.setPadding(side,dp(4),side,dp(34));screen.addView(page,new ScrollView.LayoutParams(-1,-2));root.addView(screen,new LinearLayout.LayoutParams(-1,0,1));installAuthKeyboardLift(screen,page);
  brandInto(page);TextView title=t("Fazer teste grátis",23);title.setTypeface(null,1);title.setGravity(Gravity.CENTER);page.addView(title);TextView sub=t("O usuário e a senha de 8 dígitos serão gerados automaticamente.",15);sub.setTextColor(0xffa8b8b0);sub.setGravity(Gravity.CENTER);page.addView(sub);Space topGap=new Space(this);page.addView(topGap,new LinearLayout.LayoutParams(1,dp(12)));
  LinearLayout form=new LinearLayout(this);form.setOrientation(LinearLayout.VERTICAL);EditText name=e("Nome completo",false),phone=e("WhatsApp (opcional)",false);name.setInputType(InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_PERSON_NAME);phone.setInputType(InputType.TYPE_CLASS_PHONE);form.addView(name,new LinearLayout.LayoutParams(-1,dp(58)));Space g1=new Space(this);form.addView(g1,new LinearLayout.LayoutParams(1,dp(10)));form.addView(phone,new LinearLayout.LayoutParams(-1,dp(58)));Space g2=new Space(this);form.addView(g2,new LinearLayout.LayoutParams(1,dp(12)));Button go=btn("Gerar acesso e iniciar teste");form.addView(go,new LinearLayout.LayoutParams(-1,dp(58)));TextView msg=t("",14);msg.setTextColor(0xffff7777);msg.setGravity(Gravity.CENTER);msg.setPadding(0,dp(8),0,0);form.addView(msg);page.addView(form,new LinearLayout.LayoutParams(-1,-2));
  bindImeMove(name,phone,android.view.inputmethod.EditorInfo.IME_ACTION_NEXT);bindImeMove(phone,go,android.view.inputmethod.EditorInfo.IME_ACTION_DONE);if(tvMode){linkTvVertical(name,phone);linkTvVertical(phone,go);}
  go.setOnClickListener(v->{hideKeyboard(go);if(name.getText().toString().trim().isEmpty()){msg.setText("Informe o nome.");if(tvMode)requestTvFocus(name);return;}go.setEnabled(false);msg.setText("Gerando seu acesso…");Api.post("register",Api.m("name",name.getText().toString().trim(),"mobile_number",phone.getText().toString().trim(),"device_type","android"),new Api.CB(){public void ok(JSONObject x){JSONArray a=x.optJSONArray("result");if(x.optInt("status")!=200||a==null||a.length()==0){msg.setText(x.optString("message","Não foi possível iniciar o teste grátis"));go.setEnabled(true);if(tvMode)requestTvFocus(go);return;}JSONObject u=a.optJSONObject(0);String un=u.optString("username",u.optString("user_name",""));String pw=u.optString("generated_password","");uid=u.optString("id");sp.edit().putString("uid",uid).putString("name",u.optString("full_name",name.getText().toString().trim())).putString("username",un).remove("email").apply();new android.app.AlertDialog.Builder(MainActivity.this).setTitle("Seu acesso foi criado").setMessage("Usuário: "+un+"\nSenha: "+pw+"\n\nGuarde estes dados. A entrada no aplicativo é somente com usuário e senha.").setCancelable(false).setPositiveButton("Continuar",(dd,which)->refreshEntitlements(()->prepareHomeThenShell(msg,go))).show();}public void err(String e){msg.setText("Falha de conexão: "+e);go.setEnabled(true);if(tvMode)requestTvFocus(go);}});});
  if(tvMode){prepareTvFocusTree(page);requestTvFocus(name);}
 }
'''
s=s[:start]+newreg+s[end:]

old='TextView em=t(sp.getString("email",""),13);'
if old in s:
    s=s.replace(old,'TextView em=t("Usuário: "+sp.getString("username",""),13);',1)

p.write_text(s,encoding="utf-8")

gpath=Path("work/app/build.gradle")
g=gpath.read_text(encoding="utf-8")
g=g.replace("versionCode 52897","versionCode 52898")
g=g.replace("versionName '5.28.97'","versionName '5.28.98'")
gpath.write_text(g,encoding="utf-8")

notes=Path("work/app/RELEASE_NOTES.txt")
oldnotes=notes.read_text(encoding="utf-8") if notes.exists() else ""
notes.write_text("5.28.98\n- Login somente com usuário e senha.\n- Novos acessos usam usuário numérico de 8 dígitos e senha numérica aleatória de 8 dígitos.\n- Teste grátis não solicita e-mail; o acesso é gerado automaticamente.\n\n"+oldnotes,encoding="utf-8")
