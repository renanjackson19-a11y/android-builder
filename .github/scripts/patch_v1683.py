import os
from pathlib import Path

root = Path(os.environ["GP_WORK"])
main = root / "app/src/main/java/fun/greenplay/app/MainActivity.java"
gradle = root / "app/build.gradle"

s = main.read_text(encoding="utf-8")
old = 'buy.setOnClickListener(v->checkout(p,""));'
if old not in s:
    raise SystemExit("buy handler v16.82 not found")
s = s.replace(old, 'buy.setOnClickListener(v->showPlanSummary(p));', 1)
s = s.replace(
    "// v16.82: proporções mais próximas da referência: cartão mais estreito,",
    "// v16.83: cartões compactos preservados; novo fluxo PIX sem CPF no app.",
    1,
)

start = s.find(" void askCpf(JSONObject p){")
end = s.find(" void addGap(){", start)
if start < 0 or end < 0:
    raise SystemExit("payment block v16.82 not found")

block = r''' void showPlanSummary(JSONObject p){
  final Dialog d=new Dialog(this);LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setPadding(dp(20),dp(18),dp(20),dp(18));GradientDrawable bg=round(0xff0d1712,24);bg.setStroke(dp(1),0xff294839);card.setBackground(bg);
  TextView title=t("Resumo do plano",22);title.setTypeface(null,1);title.setPadding(0,0,0,dp(6));card.addView(title);
  TextView name=t(p.optString("name","Plano"),18);name.setTypeface(null,1);name.setTextColor(GREEN);name.setPadding(0,dp(4),0,dp(8));card.addView(name);
  String price=p.optString("price_formatted",String.format(java.util.Locale.US,"%.2f",p.optDouble("price",0)).replace('.',','));int days=p.optInt("days",p.optInt("time",0));int screens=Math.max(1,p.optInt("screens",1));
  TextView info=t("R$ "+price+"  •  "+days+" dias  •  "+screens+(screens==1?" tela":" telas"),14);info.setTextColor(0xffc9d1cd);info.setPadding(0,0,0,dp(10));card.addView(info);
  JSONArray fs=p.optJSONArray("features");if(fs!=null){for(int i=0;i<fs.length()&&i<6;i++){String f=cleanPlanFeature(fs.optString(i,""));if(f.isEmpty())continue;TextView row=t("✓  "+f,13);row.setTextColor(0xffe8eeeb);row.setPadding(0,dp(3),0,dp(3));card.addView(row);}}
  TextView note=t("O acesso será liberado automaticamente após a confirmação do PIX.",12);note.setTextColor(0xff8fa098);note.setPadding(0,dp(10),0,dp(12));card.addView(note);
  LinearLayout actions=new LinearLayout(this);actions.setGravity(Gravity.RIGHT);TextView cancel=t("Voltar",14);cancel.setGravity(Gravity.CENTER);cancel.setTypeface(null,1);cancel.setTextColor(0xffc7ceca);cancel.setBackground(round(0xff17231d,13));actions.addView(cancel,new LinearLayout.LayoutParams(dp(105),dp(48)));TextView go=t("Confirmar e pagar",14);go.setGravity(Gravity.CENTER);go.setTypeface(null,1);go.setTextColor(0xff061109);go.setBackground(round(GREEN,13));LinearLayout.LayoutParams glp=new LinearLayout.LayoutParams(0,dp(48),1);glp.setMargins(dp(9),0,0,0);actions.addView(go,glp);card.addView(actions);
  cancel.setOnClickListener(v->d.dismiss());go.setOnClickListener(v->{d.dismiss();showGeneratingPayment(p);});d.setContentView(card);stabilizeInputDialog(d,card);d.setOnShowListener(x->sizeStableInputDialog(d,card));d.show();
 }
 void showGeneratingPayment(JSONObject p){
  final Dialog loading=new Dialog(this);LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setGravity(Gravity.CENTER_HORIZONTAL);card.setPadding(dp(24),dp(24),dp(24),dp(24));GradientDrawable bg=round(0xff0d1712,24);bg.setStroke(dp(1),0xff294839);card.setBackground(bg);ProgressBar bar=new ProgressBar(this);card.addView(bar,new LinearLayout.LayoutParams(dp(48),dp(48)));TextView title=t("Gerando pagamento",20);title.setTypeface(null,1);title.setGravity(Gravity.CENTER);title.setPadding(0,dp(12),0,dp(4));card.addView(title);TextView sub=t("Preparando seu PIX com segurança…",13);sub.setTextColor(0xff9eaaa4);sub.setGravity(Gravity.CENTER);card.addView(sub);loading.setCancelable(false);loading.setContentView(card);stabilizeInputDialog(loading,card);loading.setOnShowListener(x->sizeStableInputDialog(loading,card));loading.show();createCheckout(p,loading);
 }
 String firstNonEmpty(JSONObject o,String...keys){if(o==null)return "";for(String k:keys){String v=o.optString(k,"").trim();if(!v.isEmpty()&&!v.equalsIgnoreCase("null"))return v;}return "";}
 void createCheckout(JSONObject p,Dialog loading){
  String pid=p.optString("id");Api.post("create_checkout",Api.m("user_id",uid,"package_id",pid,"reseller_code",reseller),new Api.CB(){public void ok(JSONObject j){JSONArray a=j.optJSONArray("result");JSONObject r=(a!=null&&a.length()>0)?a.optJSONObject(0):null;if(r==null){runOnUiThread(()->{if(loading!=null&&loading.isShowing())loading.dismiss();String m=j.optString("message","Não foi possível gerar o PIX.");if(j.optBoolean("requires_document",false))m="Configure o CPF padrão para PIX no painel antes de gerar cobranças.";showAppNotice(m,true);});return;}runOnUiThread(()->{if(loading!=null&&loading.isShowing())loading.dismiss();showPixDialog(p,r);});}public void err(String x){runOnUiThread(()->{if(loading!=null&&loading.isShowing())loading.dismiss();showAppNotice(x==null||x.isEmpty()?"Não foi possível gerar o PIX.":x,true);});}});
 }
 android.graphics.Bitmap qrBitmap(String raw){try{if(raw==null||raw.trim().isEmpty())return null;String v=raw.trim();int comma=v.indexOf(',');if(comma>=0)v=v.substring(comma+1);byte[] b=android.util.Base64.decode(v,android.util.Base64.DEFAULT);return android.graphics.BitmapFactory.decodeByteArray(b,0,b.length);}catch(Exception e){return null;}}
 void showPixDialog(JSONObject p,JSONObject r){
  final Dialog d=new Dialog(this);final boolean[] active={true};final android.os.CountDownTimer[] timer={null};LinearLayout card=new LinearLayout(this);card.setOrientation(LinearLayout.VERTICAL);card.setPadding(dp(20),dp(18),dp(20),dp(18));GradientDrawable bg=round(0xff0d1712,24);bg.setStroke(dp(1),0xff294839);card.setBackground(bg);
  TextView title=t("Pagamento PIX",21);title.setTypeface(null,1);title.setGravity(Gravity.CENTER);title.setPadding(0,0,0,dp(4));card.addView(title);TextView sub=t(p.optString("name","Plano")+" • aguardando pagamento",13);sub.setTextColor(0xff9eaaa4);sub.setGravity(Gravity.CENTER);sub.setPadding(0,0,0,dp(10));card.addView(sub);
  String pix=firstNonEmpty(r,"pix_copy_paste","copyPaste","copy_paste","pix","brcode");String tx=firstNonEmpty(r,"transaction_id","transactionId","gateway_transaction_id","mistic_transaction_id");String qr64=firstNonEmpty(r,"qr_code_base64","qrCodeBase64","qrcode_base64");String qrUrl=firstNonEmpty(r,"qrcode_url","qrcodeUrl","qr_code_url");
  ImageView qr=new ImageView(this);qr.setScaleType(ImageView.ScaleType.FIT_CENTER);android.graphics.Bitmap bm=qrBitmap(qr64);if(bm!=null){qr.setImageBitmap(bm);card.addView(qr,new LinearLayout.LayoutParams(-1,dp(240)));}else if(!qrUrl.isEmpty()){Img.load(qr,qrUrl);card.addView(qr,new LinearLayout.LayoutParams(-1,dp(240)));}
  TextView countdown=t("Expira em 15:00",13);countdown.setTextColor(GREEN);countdown.setGravity(Gravity.CENTER);countdown.setTypeface(null,1);countdown.setPadding(0,dp(8),0,dp(8));card.addView(countdown);
  TextView code=t(pix.isEmpty()?"Código PIX indisponível":pix,11);code.setTextIsSelectable(true);code.setTextColor(0xffd7dfda);code.setMaxLines(4);code.setPadding(dp(12),dp(12),dp(12),dp(12));code.setBackground(round(0xff102219,12));card.addView(code,new LinearLayout.LayoutParams(-1,-2));
  TextView copy=t("Copiar PIX",15);copy.setTypeface(null,1);copy.setGravity(Gravity.CENTER);copy.setTextColor(0xff061109);copy.setBackground(round(GREEN,14));LinearLayout.LayoutParams clp=new LinearLayout.LayoutParams(-1,dp(52));clp.setMargins(0,dp(12),0,0);card.addView(copy,clp);
  TextView state=t("Verificando pagamento automaticamente…",12);state.setGravity(Gravity.CENTER);state.setTextColor(0xff9eaaa4);state.setPadding(0,dp(9),0,dp(3));card.addView(state);TextView close=t("Cancelar",14);close.setGravity(Gravity.CENTER);close.setTextColor(0xffc7ceca);LinearLayout.LayoutParams xlp=new LinearLayout.LayoutParams(-1,dp(44));xlp.setMargins(0,dp(4),0,0);card.addView(close,xlp);
  copy.setOnClickListener(v->{if(pix.isEmpty())return;((android.content.ClipboardManager)getSystemService(CLIPBOARD_SERVICE)).setPrimaryClip(android.content.ClipData.newPlainText("PIX",pix));Toast.makeText(this,"PIX copiado",Toast.LENGTH_SHORT).show();});close.setOnClickListener(v->d.dismiss());d.setContentView(card);Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));w.setDimAmount(.72f);w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);w.setGravity(Gravity.CENTER);}d.setOnShowListener(x->{Window ww=d.getWindow();if(ww!=null)ww.setLayout(Math.min(getResources().getDisplayMetrics().widthPixels-dp(30),dp(500)),-2);});d.setOnDismissListener(x->{active[0]=false;if(timer[0]!=null)timer[0].cancel();});d.show();
  long expires=Math.max(60,r.optLong("expires_in",r.optLong("expiresIn",900)));timer[0]=new android.os.CountDownTimer(expires*1000L,1000L){public void onTick(long ms){long sec=ms/1000L;countdown.setText(String.format(java.util.Locale.ROOT,"Expira em %02d:%02d",sec/60,sec%60));}public void onFinish(){countdown.setText("PIX expirado");state.setText("Gere um novo PIX para continuar.");active[0]=false;}};timer[0].start();pollCheckout(d,p,tx,state,active);
 }
 void pollCheckout(Dialog d,JSONObject p,String tx,TextView state,boolean[] active){
  if(!active[0]||d==null||!d.isShowing())return;if(tx==null||tx.trim().isEmpty()){state.setText("Aguardando identificador da transação…");return;}Api.post("check_checkout",Api.m("user_id",uid,"package_id",p.optString("id"),"transaction_id",tx,"reseller_code",reseller),new Api.CB(){public void ok(JSONObject j){if(!active[0])return;JSONArray a=j.optJSONArray("result");JSONObject r=(a!=null&&a.length()>0)?a.optJSONObject(0):null;boolean paid=j.optBoolean("paid",false)||j.optBoolean("activated",false);String st="";if(r!=null){paid=paid||r.optBoolean("paid",false)||r.optBoolean("activated",false)||r.optBoolean("subscription_active",false);st=firstNonEmpty(r,"payment_status","transaction_state","transactionState","status");}if(!paid&&!st.isEmpty()){String u=st.toUpperCase(java.util.Locale.ROOT);paid=u.equals("COMPLETO")||u.equals("PAID")||u.equals("APPROVED")||u.equals("CONFIRMED")||u.equals("PAGO")||u.equals("ATIVA")||u.equals("ACTIVE");}if(paid){active[0]=false;runOnUiThread(()->{state.setTextColor(GREEN);state.setText("Pagamento confirmado. Ativando assinatura…");new Handler(Looper.getMainLooper()).postDelayed(()->{if(d.isShowing())d.dismiss();showAppNotice("Assinatura ativada com sucesso!",false);profile();},700);});return;}runOnUiThread(()->state.setText("Aguardando confirmação do PIX…"));new Handler(Looper.getMainLooper()).postDelayed(()->pollCheckout(d,p,tx,state,active),4000);}public void err(String x){if(!active[0])return;runOnUiThread(()->state.setText("Aguardando pagamento…"));new Handler(Looper.getMainLooper()).postDelayed(()->pollCheckout(d,p,tx,state,active),5000);}});
 }
'''

s = s[:start] + block + s[end:]
main.write_text(s, encoding="utf-8")

g = gradle.read_text(encoding="utf-8")
g = g.replace("versionCode 104", "versionCode 105", 1)
g = g.replace("versionName '1.16.82.0'", "versionName '1.16.83.0'", 1)
gradle.write_text(g, encoding="utf-8")

(root / "README_V16_83_FLUXO_PIX_AUTOMATICO.txt").write_text(
    """GreenPlay Android v16.83

- Base direta: v16.82.
- Planos compactos preservados.
- Novo fluxo: Planos -> Resumo do plano -> Confirmar e pagar -> Gerando pagamento -> PIX.
- CPF/CNPJ não é solicitado no aplicativo. O backend deve usar o CPF padrão configurado no painel.
- Tela PIX aceita QR Code Base64/URL, copia e cola, contador e verificação automática.
- O app consulta check_checkout até o backend confirmar e aplicar a assinatura.
- A ativação real de validade, telas e benefícios continua obrigatoriamente no backend.
- Token, logo, provedor e demais configurações existentes foram preservados.
- Painel esperado: patch v72.13 sobre v72.12.
""",
    encoding="utf-8",
)
