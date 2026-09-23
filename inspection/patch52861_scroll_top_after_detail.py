from pathlib import Path
g=Path("work/app/build.gradle")
s=g.read_text()
assert "versionCode 52860" in s
assert "versionName '5.28.60'" in s
s=s.replace("versionCode 52860","versionCode 52861",1).replace("versionName '5.28.60'","versionName '5.28.61'",1)
g.write_text(s)

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()
old='''  if(mainScroll!=null){mainScroll.setVisibility(View.VISIBLE);mainScroll.post(()->mainScroll.requestLayout());}
  if(tvPageRoot!=null&&tvPageRoot.getParent()==contentFrame&&body==tvPageRoot){tvPageRoot.setVisibility(View.VISIBLE);tvPageRoot.bringToFront();tvPageRoot.post(()->tvPageRoot.requestLayout());}
  setNav(savedNavIndex);'''
new='''  if(mainScroll!=null){
   mainScroll.setVisibility(View.VISIBLE);
   bindScrollTopButton(mainScroll);
   mainScroll.post(()->{mainScroll.requestLayout();if(scrollTopButton!=null){scrollTopButton.setVisibility(mainScroll.getScrollY()>dp(360)?View.VISIBLE:View.GONE);if(scrollTopButton.getVisibility()==View.VISIBLE)scrollTopButton.bringToFront();}});
  }else hideScrollTopButton();
  if(tvPageRoot!=null&&tvPageRoot.getParent()==contentFrame&&body==tvPageRoot){tvPageRoot.setVisibility(View.VISIBLE);tvPageRoot.bringToFront();tvPageRoot.post(()->tvPageRoot.requestLayout());}
  setNav(savedNavIndex);'''
assert old in s, "closeDetails restore block not found"
s=s.replace(old,new,1)
p.write_text(s)
