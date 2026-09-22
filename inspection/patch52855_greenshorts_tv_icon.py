from pathlib import Path
g=Path("work/app/build.gradle")
s=g.read_text()
s=s.replace("versionCode 52854","versionCode 52855",1).replace("versionName '5.28.54'","versionName '5.28.55'",1)
g.write_text(s)
p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()
old='navShorts=tvHeroNavAction("GreenShorts",()->{if(detailOpen)closeDetails();homeTab("Shorts");});navShorts.setContentDescription("GreenShorts");uiTextSize(navShorts,15);menu.addView(navShorts,new LinearLayout.LayoutParams(dp(126),dp(58)));'
new='navShorts=tvHeroNavAction("",()->{if(detailOpen)closeDetails();homeTab("Shorts");});navShorts.setContentDescription("GreenShorts");navShorts.setGravity(Gravity.CENTER);navShorts.setPadding(0,0,0,0);try{Drawable shorts=getResources().getDrawable(R.drawable.top_shorts);shorts.setBounds(0,0,dp(118),dp(39));navShorts.setCompoundDrawables(shorts,null,null,null);navShorts.setCompoundDrawablePadding(0);}catch(Exception ignored){navShorts.setText("GreenShorts");uiTextSize(navShorts,15);}menu.addView(navShorts,new LinearLayout.LayoutParams(dp(132),dp(58)));'
assert old in s
s=s.replace(old,new,1)
s=s.replace('LinearLayout menu=new LinearLayout(this);menu.setGravity(Gravity.CENTER);menu.setPadding(dp(4),0,dp(4),0);','LinearLayout menu=new LinearLayout(this);menu.setGravity(Gravity.CENTER_HORIZONTAL|Gravity.CENTER_VERTICAL);menu.setPadding(0,0,0,0);',1)
p.write_text(s)
