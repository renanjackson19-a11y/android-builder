from pathlib import Path

gradle = Path("work/app/build.gradle")
g = gradle.read_text()
assert "versionCode 52855" in g
assert "versionName '5.28.55'" in g
g = g.replace("versionCode 52855", "versionCode 52856", 1)
g = g.replace("versionName '5.28.55'", "versionName '5.28.56'", 1)
gradle.write_text(g)

p = Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s = p.read_text()

old = '''int side=wideTvUi()?tvContentSide():dp(18);int usable=getResources().getDisplayMetrics().widthPixels-(wideTvUi()?side*2:dp(52));int w=Math.max(dp(112),usable/cols);int gen=viewGen;'''
new = '''int usable;if(wideTvUi()){int screen=getResources().getDisplayMetrics().widthPixels;int left=body==null?dp(28):body.getPaddingLeft();int right=body==null?dp(28):body.getPaddingRight();usable=Math.max(dp(720),screen-left-right);int gaps=dp(10)*cols;usable=Math.max(dp(720),usable-gaps);}else usable=getResources().getDisplayMetrics().widthPixels-dp(52);int w=Math.max(dp(112),usable/cols);int gen=viewGen;'''
assert old in s, "grid width block not found"
s = s.replace(old, new, 1)

old2 = '''lp.setMargins(dp(4),dp(5),dp(6),dp(9));g.addView(c,lp);'''
new2 = '''lp.setMargins(dp(4),dp(5),dp(6),dp(9));g.addView(c,lp);'''
assert old2 in s

p.write_text(s)
