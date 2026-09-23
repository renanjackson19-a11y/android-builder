from pathlib import Path
g=Path("work/app/build.gradle")
s=g.read_text()
assert "versionCode 52859" in s
assert "versionName '5.28.59'" in s
s=s.replace("versionCode 52859","versionCode 52860",1).replace("versionName '5.28.59'","versionName '5.28.60'",1)
g.write_text(s)

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

old='''static final int REQ_PROFILE_PHOTO=8601; static final int TAG_SKIP_TV_FOCUS_FX=0x4f120001; static final int TAG_EPG_LOADING=0x4f120002;'''
new='''static final int REQ_PROFILE_PHOTO=8601; static final int TAG_SKIP_TV_FOCUS_FX=0x4f120001; static final int TAG_EPG_LOADING=0x4f120002; static final int TAG_SCROLL_TOP_INSTALLED=0x4f120003;'''
assert old in s
s=s.replace(old,new,1)

old='''TextView navHome,navFav,navTv,navFootball,navMovies,navSeries,navShorts,navKids,navDownloads,navProfile;'''
new='''TextView navHome,navFav,navTv,navFootball,navMovies,navSeries,navShorts,navKids,navDownloads,navProfile,scrollTopButton; ScrollView scrollTopHost;'''
assert old in s
s=s.replace(old,new,1)

anchor=''' int bottomNavIconRes(int idx){if(idx==0)return R.drawable.ic_nav_home;if(idx==1)return R.drawable.ic_nav_favorite;if(idx==2)return R.drawable.ic_nav_tv;if(idx==3)return R.drawable.ic_nav_download;return R.drawable.ic_nav_profile;}'''
methods=''' void bindScrollTopButton(ScrollView sv){
  if(wideTvUi()||contentFrame==null||sv==null){scrollTopHost=null;if(scrollTopButton!=null)scrollTopButton.setVisibility(View.GONE);return;}
  scrollTopHost=sv;
  if(scrollTopButton==null){
   TextView up=t("↑",25);up.setTextColor(GREEN);up.setGravity(Gravity.CENTER);up.setIncludeFontPadding(false);up.setPadding(0,0,0,dp(3));up.setContentDescription("Voltar ao topo");up.setFocusable(false);up.setClickable(true);
   GradientDrawable bg=new GradientDrawable();bg.setShape(GradientDrawable.OVAL);bg.setColor(0xee102018);bg.setStroke(dp(1),0xff3d7255);up.setBackground(bg);if(android.os.Build.VERSION.SDK_INT>=21)up.setElevation(dp(8));
   up.setOnClickListener(v->{ScrollView target=scrollTopHost;if(target!=null){target.smoothScrollTo(0,0);target.postDelayed(()->{if(scrollTopHost==target&&scrollTopButton!=null)scrollTopButton.setVisibility(View.GONE);},280);}});
   scrollTopButton=up;FrameLayout.LayoutParams lp=new FrameLayout.LayoutParams(dp(48),dp(48),Gravity.RIGHT|Gravity.BOTTOM);lp.setMargins(0,0,dp(12),dp(14));contentFrame.addView(up,lp);
  }else{
   ViewParent pp=scrollTopButton.getParent();if(pp instanceof ViewGroup&&pp!=contentFrame)((ViewGroup)pp).removeView(scrollTopButton);if(scrollTopButton.getParent()==null){FrameLayout.LayoutParams lp=new FrameLayout.LayoutParams(dp(48),dp(48),Gravity.RIGHT|Gravity.BOTTOM);lp.setMargins(0,0,dp(12),dp(14));contentFrame.addView(scrollTopButton,lp);}
  }
  scrollTopButton.setVisibility(sv.getScrollY()>dp(360)?View.VISIBLE:View.GONE);scrollTopButton.bringToFront();
  if(sv.getTag(TAG_SCROLL_TOP_INSTALLED)==null){sv.setTag(TAG_SCROLL_TOP_INSTALLED,Boolean.TRUE);final java.lang.ref.WeakReference<ScrollView> wr=new java.lang.ref.WeakReference<>(sv);sv.getViewTreeObserver().addOnScrollChangedListener(()->{ScrollView x=wr.get();if(x==null||scrollTopButton==null||scrollTopHost!=x)return;scrollTopButton.setVisibility(x.getScrollY()>dp(360)?View.VISIBLE:View.GONE);if(scrollTopButton.getVisibility()==View.VISIBLE)scrollTopButton.bringToFront();});}
 }
 void hideScrollTopButton(){scrollTopHost=null;if(scrollTopButton!=null)scrollTopButton.setVisibility(View.GONE);}
'''+anchor
assert anchor in s
s=s.replace(anchor,methods,1)

old='''contentFrame.addView(mainScroll,new FrameLayout.LayoutParams(-1,-1));
  homeScrollCache=mainScroll;'''
new='''contentFrame.addView(mainScroll,new FrameLayout.LayoutParams(-1,-1));bindScrollTopButton(mainScroll);
  homeScrollCache=mainScroll;'''
assert old in s
s=s.replace(old,new,1)

old='''mainScroll.addView(body);contentFrame.addView(mainScroll,new FrameLayout.LayoutParams(-1,-1));ensureGlobalCastButton();}'''
new='''mainScroll.addView(body);contentFrame.addView(mainScroll,new FrameLayout.LayoutParams(-1,-1));bindScrollTopButton(mainScroll);ensureGlobalCastButton();}'''
assert old in s
s=s.replace(old,new,1)

old='''if(homeScrollCache.getParent()==null)contentFrame.addView(homeScrollCache,new FrameLayout.LayoutParams(-1,-1));ensureGlobalCastButton();
  }
 }'''
new='''if(homeScrollCache.getParent()==null)contentFrame.addView(homeScrollCache,new FrameLayout.LayoutParams(-1,-1));bindScrollTopButton(mainScroll);ensureGlobalCastButton();
  }else bindScrollTopButton(mainScroll);
 }'''
assert old in s
s=s.replace(old,new,1)

old='''mainScroll=null;tvPageRoot=new LinearLayout(this);'''
new='''mainScroll=null;hideScrollTopButton();tvPageRoot=new LinearLayout(this);'''
assert old in s
s=s.replace(old,new,1)

old='''if(parentScroll.getParent()==null)contentFrame.addView(parentScroll,new FrameLayout.LayoutParams(-1,-1));
   activeHomeTab=''' 
new='''if(parentScroll.getParent()==null)contentFrame.addView(parentScroll,new FrameLayout.LayoutParams(-1,-1));bindScrollTopButton(parentScroll);
   activeHomeTab='''
assert old in s
s=s.replace(old,new,1)

old='''if(contentFrame!=null){contentFrame.setBackgroundColor(BG);contentFrame.addView(mainScroll,new FrameLayout.LayoutParams(-1,-1));mainScroll.bringToFront();}'''
new='''if(contentFrame!=null){contentFrame.setBackgroundColor(BG);contentFrame.addView(mainScroll,new FrameLayout.LayoutParams(-1,-1));bindScrollTopButton(mainScroll);mainScroll.bringToFront();if(scrollTopButton!=null)scrollTopButton.bringToFront();}'''
assert old in s
s=s.replace(old,new,1)

old='''mainScroll=playerReturnScroll;body=playerReturnBody;if(playerReturnScroll.getParent()==null)contentFrame.addView(playerReturnScroll,new FrameLayout.LayoutParams(-1,-1));}'''
new='''mainScroll=playerReturnScroll;body=playerReturnBody;if(playerReturnScroll.getParent()==null)contentFrame.addView(playerReturnScroll,new FrameLayout.LayoutParams(-1,-1));bindScrollTopButton(mainScroll);}'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)
