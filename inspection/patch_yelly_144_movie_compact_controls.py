from pathlib import Path
root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java"
s=p.read_text(encoding="utf-8")
# Keep the full-film video frame exactly as 1.0.42: no floral masks/bands.
# Only make the movie controls compact and lower, as requested.
s=s.replace("controls.setPadding(dp(12),dp(8),dp(12),dp(7));","controls.setPadding(dp(8),dp(4),dp(8),dp(3));",1)
s=s.replace('back10=tx("↶ 10s",15);play=tx("Ⅱ",26);fwd10=tx("10s ↷",15);','back10=tx("↶ 10s",12);play=tx("Ⅱ",20);fwd10=tx("10s ↷",12);',1)
for n in ("b1","b2","b3"):
    s=s.replace(f"LinearLayout.LayoutParams {n}=new LinearLayout.LayoutParams(0,dp(46),1f);",f"LinearLayout.LayoutParams {n}=new LinearLayout.LayoutParams(0,dp(34),1f);",1)
s=s.replace("controls.addView(buttons,new LinearLayout.LayoutParams(-1,dp(48)));","controls.addView(buttons,new LinearLayout.LayoutParams(-1,dp(36)));",1)
s=s.replace("progress.addView(time,new LinearLayout.LayoutParams(dp(112),dp(34)));","progress.addView(time,new LinearLayout.LayoutParams(dp(98),dp(24)));",1)
s=s.replace("progress.addView(seek,new LinearLayout.LayoutParams(0,dp(34),1));","progress.addView(seek,new LinearLayout.LayoutParams(0,dp(24),1));",1)
s=s.replace("controls.addView(progress,new LinearLayout.LayoutParams(-1,dp(34)));","controls.addView(progress,new LinearLayout.LayoutParams(-1,dp(24)));",1)
old="""FrameLayout.LayoutParams cp=new FrameLayout.LayoutParams(-1,dp(94),Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);
        cp.setMargins(dp(14),0,dp(14),dp(10));"""
new="""FrameLayout.LayoutParams cp=new FrameLayout.LayoutParams(-1,dp(64),Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);
        cp.setMargins(dp(28),0,dp(28),dp(6));"""
if old not in s: raise SystemExit("controls anchor missing")
s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")
g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10042" not in t or "versionName '1.0.42'" not in t: raise SystemExit("wrong base")
t=t.replace("versionCode 10042","versionCode 10044",1).replace("versionName '1.0.42'","versionName '1.0.44'",1)
g.write_text(t,encoding="utf-8")
print("YELLY_144_FULL_MOVIE_FRAME_COMPACT_CONTROLS_OK")
