from pathlib import Path
root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java"
s=p.read_text(encoding="utf-8")

# Full-film player: same Yelly/Stories visual framing, without changing movie playback.
# Use the existing floral asset only in the app-owned top/bottom framing.
s=s.replace("View topMask=new View(this);topMask.setBackgroundColor(Color.BLACK);",
'''View topMask=new View(this);topMask.setBackgroundResource(R.drawable.yelly_story_bg);''',1)
s=s.replace("View bottomMask=new View(this);bottomMask.setBackgroundColor(Color.BLACK);",
'''View bottomMask=new View(this);bottomMask.setBackgroundResource(R.drawable.yelly_story_bg);''',1)

# Smaller, lower-profile movie controls.
old='''controls.setPadding(dp(12),dp(8),dp(12),dp(7));'''
new='''controls.setPadding(dp(9),dp(5),dp(9),dp(4));'''
if old not in s: raise SystemExit("controls padding anchor missing")
s=s.replace(old,new,1)
s=s.replace('''back10=tx("↶ 10s",15);play=tx("Ⅱ",26);fwd10=tx("10s ↷",15);''',
'''back10=tx("↶ 10s",13);play=tx("Ⅱ",22);fwd10=tx("10s ↷",13);''',1)
s=s.replace("LinearLayout.LayoutParams b1=new LinearLayout.LayoutParams(0,dp(46),1f);","LinearLayout.LayoutParams b1=new LinearLayout.LayoutParams(0,dp(38),1f);",1)
s=s.replace("LinearLayout.LayoutParams b2=new LinearLayout.LayoutParams(0,dp(46),1f);","LinearLayout.LayoutParams b2=new LinearLayout.LayoutParams(0,dp(38),1f);",1)
s=s.replace("LinearLayout.LayoutParams b3=new LinearLayout.LayoutParams(0,dp(46),1f);","LinearLayout.LayoutParams b3=new LinearLayout.LayoutParams(0,dp(38),1f);",1)
s=s.replace("controls.addView(buttons,new LinearLayout.LayoutParams(-1,dp(48)));","controls.addView(buttons,new LinearLayout.LayoutParams(-1,dp(40)));",1)
s=s.replace('''progress.addView(time,new LinearLayout.LayoutParams(dp(112),dp(34)));''','''progress.addView(time,new LinearLayout.LayoutParams(dp(104),dp(28)));''',1)
s=s.replace('''progress.addView(seek,new LinearLayout.LayoutParams(0,dp(34),1));''','''progress.addView(seek,new LinearLayout.LayoutParams(0,dp(28),1));''',1)
s=s.replace('''controls.addView(progress,new LinearLayout.LayoutParams(-1,dp(34)));''','''controls.addView(progress,new LinearLayout.LayoutParams(-1,dp(28)));''',1)
old='''FrameLayout.LayoutParams cp=new FrameLayout.LayoutParams(-1,dp(94),Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);
        cp.setMargins(dp(14),0,dp(14),dp(10));'''
new='''FrameLayout.LayoutParams cp=new FrameLayout.LayoutParams(-1,dp(74),Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);
        cp.setMargins(dp(24),0,dp(24),dp(8));'''
if old not in s: raise SystemExit("controls container anchor missing")
s=s.replace(old,new,1)

p.write_text(s,encoding="utf-8")
g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10042" not in t or "versionName '1.0.42'" not in t: raise SystemExit("wrong base")
t=t.replace("versionCode 10042","versionCode 10043",1).replace("versionName '1.0.42'","versionName '1.0.43'",1)
g.write_text(t,encoding="utf-8")
print("YELLY_143_MOVIE_STORIES_STYLE_SMALL_CONTROLS_OK")
