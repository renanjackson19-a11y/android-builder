from pathlib import Path
root=Path("work")
p=root/"app/src/main/java/fun/greenplay/app/YouTubePlayerActivity.java"
s=p.read_text(encoding="utf-8")

# ONLY requested changes on top of 1.0.44: Yelly logo + replace green accent with Yelly pink.
# Add the same Yelly header logo used by Stories.
anchor='''root.addView(back,bp);'''
if anchor not in s: raise SystemExit("back anchor missing")
insert=anchor+'''
        ImageView yellyLogo=new ImageView(this);
        yellyLogo.setImageResource(R.drawable.yelly_logo_header);
        yellyLogo.setScaleType(ImageView.ScaleType.CENTER_INSIDE);
        FrameLayout.LayoutParams ylp=new FrameLayout.LayoutParams(dp(132),dp(58),Gravity.TOP|Gravity.RIGHT);
        ylp.setMargins(0,dp(20),dp(14),0);
        root.addView(yellyLogo,ylp);'''
s=s.replace(anchor,insert,1)

# Existing top-right green status dot: change to Yelly pink only.
s=s.replace('Color.rgb(45,210,90)','Color.rgb(236,36,126)')

p.write_text(s,encoding="utf-8")
g=root/"app/build.gradle"
t=g.read_text(encoding="utf-8")
if "versionCode 10044" not in t or "versionName '1.0.44'" not in t: raise SystemExit("wrong base")
t=t.replace("versionCode 10044","versionCode 10045",1).replace("versionName '1.0.44'","versionName '1.0.45'",1)
g.write_text(t,encoding="utf-8")
print("YELLY_145_LOGO_AND_PINK_ACCENT_ONLY_OK")
