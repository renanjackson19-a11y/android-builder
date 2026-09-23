from pathlib import Path

g=Path("work/app/build.gradle")
s=g.read_text()
assert "versionCode 52867" in s
assert "versionName '5.28.67'" in s
s=s.replace("versionCode 52867","versionCode 52868",1).replace("versionName '5.28.67'","versionName '5.28.68'",1)
g.write_text(s)

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

old='''String raw="catalog52852_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);'''
new='''String raw="catalog52868_"+(uid==null?"":uid)+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);'''
assert old in s
s=s.replace(old,new,1)

old='''String homeExtrasKey(){return "home_extras_"+uid+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);}'''
new='''String homeExtrasKey(){return "home_extras_52868_"+uid+"_"+(Api.PROVIDER==null?"":Api.PROVIDER);}'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)
