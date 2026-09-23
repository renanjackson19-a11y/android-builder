from pathlib import Path

g=Path("work/app/build.gradle")
s=g.read_text()
assert "versionCode 52863" in s
assert "versionName '5.28.63'" in s
s=s.replace("versionCode 52863","versionCode 52864",1).replace("versionName '5.28.63'","versionName '5.28.64'",1)
g.write_text(s)

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

# Do not discard playable channels just because the M3U has no tvg-id / EPG id.
old='''  String tvg=tvFirstString(x,"tvg-id","tvg_id","epg_channel_id","epg_id","channel_number","stream_num");
  return !u.isEmpty()&&!tvg.isEmpty();'''
new='''  String tvg=tvFirstString(x,"tvg-id","tvg_id","epg_channel_id","epg_id","channel_number","stream_num");
  return !u.isEmpty();'''
assert old in s, "live validity filter not found"
s=s.replace(old,new,1)

# Preserve more logo field spellings from arbitrary M3U sources.
s=s.replace(
'''String[] canonical={"greenplay_logo","epg_logo","tvg_logo","logo_alt","fallback_logo"};''',
'''String[] canonical={"greenplay_logo","epg_logo","tvg_logo","tvg-logo","logo_url","channel_logo","logo_alt","fallback_logo"};''',
1)
s=s.replace(
'''String[] keys={"provider_icon","stream_icon","source_logo","thumbnail","image","landscape","portrait_img","landscape_img","logo","icon","channel_icon","cover","poster","epg_channel_id","epg_id","tvg_id","tvg-id","tvg_name","tvg-name","channel_number","num","category_name","video_320","video_480","video_720","video_1080","video_extension"};''',
'''String[] keys={"provider_icon","stream_icon","source_logo","thumbnail","image","landscape","portrait_img","landscape_img","logo","icon","channel_icon","channel_logo","logo_url","tvg_logo","tvg-logo","cover","poster","epg_channel_id","epg_id","tvg_id","tvg-id","tvg_name","tvg-name","channel_number","num","category_name","video_320","video_480","video_720","video_1080","video_extension"};''',
1)
s=s.replace(
'''String[] canonicalKeys={"greenplay_logo","epg_logo","tvg_logo","logo_alt","fallback_logo"};''',
'''String[] canonicalKeys={"greenplay_logo","epg_logo","tvg_logo","tvg-logo","logo_url","channel_logo","logo_alt","fallback_logo"};''',
1)
s=s.replace(
'''String[] rawCanonical={"greenplay_logo","epg_logo","tvg_logo","logo_alt","fallback_logo"};''',
'''String[] rawCanonical={"greenplay_logo","epg_logo","tvg_logo","tvg-logo","logo_url","channel_logo","logo_alt","fallback_logo"};''',
1)
s=s.replace(
'''String[] ownKeys={"logo","icon","channel_icon","thumbnail","image","landscape","portrait_img","landscape_img","cover","poster"};''',
'''String[] ownKeys={"logo","icon","channel_icon","channel_logo","logo_url","tvg_logo","tvg-logo","thumbnail","image","landscape","portrait_img","landscape_img","cover","poster"};''',
1)
s=s.replace(
'''String[] rawSource={"logo","icon","channel_icon","thumbnail","image","provider_icon","stream_icon","source_logo"};''',
'''String[] rawSource={"logo","icon","channel_icon","channel_logo","logo_url","tvg_logo","tvg-logo","thumbnail","image","provider_icon","stream_icon","source_logo"};''',
1)

p.write_text(s)

p=Path("work/app/src/main/java/fun/greenplay/app/PlayerActivity.java")
s=p.read_text()

# IPTV VOD/series from some M3U sources reject GreenPlay Referer/Origin.
old='''  HashMap<String,String> requestHeaders=new HashMap<>();if(!live){requestHeaders.put("Referer","https://greenplay.fun/");requestHeaders.put("Origin","https://greenplay.fun");}String liveUa=live?"VLC/3.0.18 LibVLC/3.0.18":"Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36";DefaultHttpDataSource.Factory httpFactory=new DefaultHttpDataSource.Factory().setUserAgent(liveUa).setAllowCrossProtocolRedirects(true).setConnectTimeoutMs(8000).setReadTimeoutMs(18000).setDefaultRequestProperties(requestHeaders);'''
new='''  HashMap<String,String> requestHeaders=new HashMap<>();DefaultHttpDataSource.Factory httpFactory=new DefaultHttpDataSource.Factory().setUserAgent("VLC/3.0.18 LibVLC/3.0.18").setAllowCrossProtocolRedirects(true).setConnectTimeoutMs(8000).setReadTimeoutMs(30000).setDefaultRequestProperties(requestHeaders);'''
assert old in s, "player headers block not found"
s=s.replace(old,new,1)

# Make disguised .m3u8 -> MPEG-TS fallback universal, not live-only.
s=s.replace('''if(bufferStarts>=2&&!retryLiveAsTs())downgradeQuality();''','''if(bufferStarts>=2&&!retryAsTs())downgradeQuality();''')
s=s.replace('''if(retryLiveAsTs())return;''','''if(retryAsTs())return;''')
s=s.replace('''if(live&&tsFallbackSource==idx)mb.setMimeType("video/mp2t");''','''if(tsFallbackSource==idx)mb.setMimeType("video/mp2t");''')
old=''' boolean retryLiveAsTs(){if(!live||switching||sourceIndex<0||sourceIndex>=sources.size()||tsFallbackSource==sourceIndex)return false;String u=sources.get(sourceIndex);if(u==null||!u.toLowerCase(java.util.Locale.US).contains(".m3u8"))return false;tsFallbackSource=sourceIndex;switching=true;prepared=false;bufferStarts=0;final int idx=sourceIndex;h.postDelayed(()->{switching=false;startSource(idx,0);},140);return true;}'''
new=''' boolean retryAsTs(){if(switching||sourceIndex<0||sourceIndex>=sources.size()||tsFallbackSource==sourceIndex)return false;String u=sources.get(sourceIndex);if(u==null||!u.toLowerCase(java.util.Locale.US).contains(".m3u8"))return false;tsFallbackSource=sourceIndex;switching=true;prepared=false;bufferStarts=0;final int idx=sourceIndex;final int pos=live?0:safePosition();h.postDelayed(()->{switching=false;startSource(idx,pos);},140);return true;}'''
assert old in s, "retryLiveAsTs method not found"
s=s.replace(old,new,1)

p.write_text(s)
