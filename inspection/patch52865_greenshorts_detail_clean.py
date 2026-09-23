from pathlib import Path

g=Path("work/app/build.gradle")
s=g.read_text()
assert "versionCode 52864" in s
assert "versionName '5.28.64'" in s
s=s.replace("versionCode 52864","versionCode 52865",1).replace("versionName '5.28.64'","versionName '5.28.65'",1)
g.write_text(s)

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

old='''   if(isYoutube)renderGreenShortsResume(source,host,displayTitle);else renderMovieResume(source,d,host,displayTitle);
   boolean canResume=isYoutube?greenShortResumePosition(source)>0:movieResumePosition(source.optString("id",d.optString("id","")))>0;'''
new='''   if(!isYoutube)renderMovieResume(source,d,host,displayTitle);
   boolean canResume=isYoutube?greenShortResumePosition(source)>0:movieResumePosition(source.optString("id",d.optString("id","")))>0;'''
assert old in s, "GreenShorts resume block call not found"
s=s.replace(old,new,1)

p.write_text(s)
