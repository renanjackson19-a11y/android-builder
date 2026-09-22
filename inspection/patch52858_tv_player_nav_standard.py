from pathlib import Path

gradle=Path("work/app/build.gradle")
g=gradle.read_text()
assert "versionCode 52857" in g
assert "versionName '5.28.57'" in g
g=g.replace("versionCode 52857","versionCode 52858",1)
g=g.replace("versionName '5.28.57'","versionName '5.28.58'",1)
gradle.write_text(g)

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

repls=[
(
'''if(currentProviderHasLive()){navTv=tvHeroNavAction("",()->tvNavigate(2));navTv.setContentDescription("TV");try{Drawable tvIcon=getResources().getDrawable(R.drawable.top_tv);tvIcon.setBounds(0,0,dp(58),dp(32));navTv.setCompoundDrawables(tvIcon,null,null,null);navTv.setCompoundDrawablePadding(0);}catch(Exception ignored){navTv.setText("TV");uiTextSize(navTv,16);}menu.addView(navTv,new LinearLayout.LayoutParams(dp(66),dp(58)));}else navTv=null;''',
'''if(currentProviderHasLive()){navTv=tvHeroNavAction("",()->tvNavigate(2));navTv.setContentDescription("TV");navTv.setGravity(Gravity.CENTER);try{Drawable tvIcon=getResources().getDrawable(R.drawable.top_tv);tvIcon.setBounds(0,0,dp(76),dp(38));navTv.setCompoundDrawables(tvIcon,null,null,null);navTv.setCompoundDrawablePadding(0);}catch(Exception ignored){navTv.setText("TV");uiTextSize(navTv,16);}menu.addView(navTv,new LinearLayout.LayoutParams(dp(104),dp(60)));}else navTv=null;'''
),
(
'''navHome=tvHeroNavAction("Destaque",()->{goHomeNow();if(!"Recomendações".equals(activeHomeTab))homeTab("Recomendações");});uiTextSize(navHome,16);menu.addView(navHome,new LinearLayout.LayoutParams(dp(106),dp(58)));''',
'''navHome=tvHeroNavAction("Destaque",()->{goHomeNow();if(!"Recomendações".equals(activeHomeTab))homeTab("Recomendações");});uiTextSize(navHome,16);navHome.setGravity(Gravity.CENTER);menu.addView(navHome,new LinearLayout.LayoutParams(dp(104),dp(60)));'''
),
(
'''navFootball=tvHeroNavAction("",()->openTvFootball());navFootball.setContentDescription("Futebol");try{Drawable fut=getResources().getDrawable(R.drawable.football_logo);fut.setBounds(0,0,dp(108),dp(38));navFootball.setCompoundDrawables(fut,null,null,null);navFootball.setCompoundDrawablePadding(0);}catch(Exception ignored){navFootball.setText("Futebol");}menu.addView(navFootball,new LinearLayout.LayoutParams(dp(116),dp(58)));''',
'''navFootball=tvHeroNavAction("",()->openTvFootball());navFootball.setContentDescription("Futebol");navFootball.setGravity(Gravity.CENTER);try{Drawable fut=getResources().getDrawable(R.drawable.football_logo);fut.setBounds(0,0,dp(76),dp(38));navFootball.setCompoundDrawables(fut,null,null,null);navFootball.setCompoundDrawablePadding(0);}catch(Exception ignored){navFootball.setText("Futebol");}menu.addView(navFootball,new LinearLayout.LayoutParams(dp(104),dp(60)));'''
),
(
'''navMovies=tvHeroNavAction("",()->{if(tvMode)openTvCatalogBrowser(1,"Filmes",false);else{if(detailOpen)closeDetails();homeTab("Filmes");}});navMovies.setContentDescription("Filmes");try{Drawable movieIcon=getResources().getDrawable(R.drawable.top_filmes);movieIcon.setBounds(0,0,dp(82),dp(30));navMovies.setCompoundDrawables(movieIcon,null,null,null);navMovies.setCompoundDrawablePadding(0);}catch(Exception ignored){navMovies.setText("Filmes");uiTextSize(navMovies,16);}menu.addView(navMovies,new LinearLayout.LayoutParams(dp(90),dp(58)));''',
'''navMovies=tvHeroNavAction("",()->{if(tvMode)openTvCatalogBrowser(1,"Filmes",false);else{if(detailOpen)closeDetails();homeTab("Filmes");}});navMovies.setContentDescription("Filmes");navMovies.setGravity(Gravity.CENTER);try{Drawable movieIcon=getResources().getDrawable(R.drawable.top_filmes);movieIcon.setBounds(0,0,dp(76),dp(38));navMovies.setCompoundDrawables(movieIcon,null,null,null);navMovies.setCompoundDrawablePadding(0);}catch(Exception ignored){navMovies.setText("Filmes");uiTextSize(navMovies,16);}menu.addView(navMovies,new LinearLayout.LayoutParams(dp(104),dp(60)));'''
),
(
'''navSeries=tvHeroNavAction("",()->{if(tvMode)openTvCatalogBrowser(2,"Séries",false);else{if(detailOpen)closeDetails();homeTab("Séries");}});navSeries.setContentDescription("Séries");try{Drawable seriesIcon=getResources().getDrawable(R.drawable.top_series);seriesIcon.setBounds(0,0,dp(82),dp(30));navSeries.setCompoundDrawables(seriesIcon,null,null,null);navSeries.setCompoundDrawablePadding(0);}catch(Exception ignored){navSeries.setText("Séries");uiTextSize(navSeries,16);}menu.addView(navSeries,new LinearLayout.LayoutParams(dp(90),dp(58)));''',
'''navSeries=tvHeroNavAction("",()->{if(tvMode)openTvCatalogBrowser(2,"Séries",false);else{if(detailOpen)closeDetails();homeTab("Séries");}});navSeries.setContentDescription("Séries");navSeries.setGravity(Gravity.CENTER);try{Drawable seriesIcon=getResources().getDrawable(R.drawable.top_series);seriesIcon.setBounds(0,0,dp(76),dp(38));navSeries.setCompoundDrawables(seriesIcon,null,null,null);navSeries.setCompoundDrawablePadding(0);}catch(Exception ignored){navSeries.setText("Séries");uiTextSize(navSeries,16);}menu.addView(navSeries,new LinearLayout.LayoutParams(dp(104),dp(60)));'''
),
(
'''navShorts=tvHeroNavAction("",()->{if(detailOpen)closeDetails();homeTab("Shorts");});navShorts.setContentDescription("GreenShorts");navShorts.setGravity(Gravity.CENTER);navShorts.setPadding(0,0,0,0);try{Drawable shorts=getResources().getDrawable(R.drawable.top_shorts);shorts.setBounds(0,0,dp(118),dp(39));navShorts.setCompoundDrawables(shorts,null,null,null);navShorts.setCompoundDrawablePadding(0);}catch(Exception ignored){navShorts.setText("GreenShorts");uiTextSize(navShorts,15);}menu.addView(navShorts,new LinearLayout.LayoutParams(dp(132),dp(58)));''',
'''navShorts=tvHeroNavAction("",()->{if(detailOpen)closeDetails();homeTab("Shorts");});navShorts.setContentDescription("GreenShorts");navShorts.setGravity(Gravity.CENTER);navShorts.setPadding(0,0,0,0);try{Drawable shorts=getResources().getDrawable(R.drawable.top_shorts);shorts.setBounds(0,0,dp(76),dp(38));navShorts.setCompoundDrawables(shorts,null,null,null);navShorts.setCompoundDrawablePadding(0);}catch(Exception ignored){navShorts.setText("GreenShorts");uiTextSize(navShorts,15);}menu.addView(navShorts,new LinearLayout.LayoutParams(dp(104),dp(60)));'''
),
(
'''navKids=tvHeroNavAction("",()->{if(tvMode)openTvCatalogBrowser(1,"Kids",true);else openTvKids();});navKids.setContentDescription("Kids");try{Drawable kids=getResources().getDrawable(R.drawable.kids_logo);kids.setBounds(0,0,dp(90),dp(36));navKids.setCompoundDrawables(kids,null,null,null);navKids.setCompoundDrawablePadding(0);}catch(Exception ignored){navKids.setText("Kids");}menu.addView(navKids,new LinearLayout.LayoutParams(dp(98),dp(58)));''',
'''navKids=tvHeroNavAction("",()->{if(tvMode)openTvCatalogBrowser(1,"Kids",true);else openTvKids();});navKids.setContentDescription("Kids");navKids.setGravity(Gravity.CENTER);try{Drawable kids=getResources().getDrawable(R.drawable.kids_logo);kids.setBounds(0,0,dp(76),dp(38));navKids.setCompoundDrawables(kids,null,null,null);navKids.setCompoundDrawablePadding(0);}catch(Exception ignored){navKids.setText("Kids");}menu.addView(navKids,new LinearLayout.LayoutParams(dp(104),dp(60)));'''
),
(
'''navFav=tvHeroNavAction("Favoritos",()->tvNavigate(1));uiTextSize(navFav,16);navFav.setSingleLine(true);navFav.setEllipsize(null);menu.addView(navFav,new LinearLayout.LayoutParams(dp(112),dp(58)));''',
'''navFav=tvHeroNavAction("Favoritos",()->tvNavigate(1));uiTextSize(navFav,16);navFav.setSingleLine(true);navFav.setEllipsize(null);navFav.setGravity(Gravity.CENTER);menu.addView(navFav,new LinearLayout.LayoutParams(dp(104),dp(60)));'''
)
]
for old,new in repls:
    assert old in s, old[:90]
    s=s.replace(old,new,1)

p.write_text(s)

yp=Path("work/app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java")
y=yp.read_text()

old='''        int screenH=getResources().getDisplayMetrics().heightPixels;
        int topMaskH=Math.max(dp(48),Math.min(dp(82),(int)(screenH*0.09f)));
        int bottomMaskH=Math.max(dp(64),Math.min(dp(110),(int)(screenH*0.11f)));

        View topMask=new View(this);
        topMask.setBackgroundColor(Color.BLACK);
        FrameLayout.LayoutParams topMaskLp=new FrameLayout.LayoutParams(-1,topMaskH,Gravity.TOP);
        root.addView(topMask,topMaskLp);

        View bottomMask=new View(this);
        bottomMask.setBackgroundColor(Color.BLACK);
        FrameLayout.LayoutParams bottomMaskLp=new FrameLayout.LayoutParams(-1,bottomMaskH,Gravity.BOTTOM);
        root.addView(bottomMask,bottomMaskLp);'''
new='''        if(!tvMode){
            int screenH=getResources().getDisplayMetrics().heightPixels;
            int topMaskH=Math.max(dp(48),Math.min(dp(82),(int)(screenH*0.09f)));
            int bottomMaskH=Math.max(dp(64),Math.min(dp(110),(int)(screenH*0.11f)));
            View topMask=new View(this);topMask.setBackgroundColor(Color.BLACK);
            FrameLayout.LayoutParams topMaskLp=new FrameLayout.LayoutParams(-1,topMaskH,Gravity.TOP);root.addView(topMask,topMaskLp);
            View bottomMask=new View(this);bottomMask.setBackgroundColor(Color.BLACK);
            FrameLayout.LayoutParams bottomMaskLp=new FrameLayout.LayoutParams(-1,bottomMaskH,Gravity.BOTTOM);root.addView(bottomMask,bottomMaskLp);
        }'''
assert old in y
y=y.replace(old,new,1)

old='''        String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'>"+
            "<style>html,body,#p{margin:0;padding:0;width:100%;height:100%;background:#000;overflow:hidden}iframe{width:100%!important;height:100%!important;border:0}</style>"+'''
new='''        String tvCss=tvMode?"transform:scale(1.48);transform-origin:50% 50%;":"";
        String html="<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no'>"+
            "<style>html,body,#p{margin:0;padding:0;width:100%;height:100%;background:#000;overflow:hidden}iframe{width:100%!important;height:100%!important;border:0;"+tvCss+"}</style>"+'''
assert old in y
y=y.replace(old,new,1)

yp.write_text(y)
