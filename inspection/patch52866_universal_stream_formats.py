from pathlib import Path

g=Path("work/app/build.gradle")
s=g.read_text()
assert "versionCode 52865" in s
assert "versionName '5.28.65'" in s
s=s.replace("versionCode 52865","versionCode 52866",1).replace("versionName '5.28.65'","versionName '5.28.66'",1)
g.write_text(s)

# TV / inline live player: do not trust URL extension alone.
p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

old='''int tvInlineSourceIndex=0,tvInlineTsFallbackIndex=-1,tvInlineBufferStarts=0,tvSavedScrollY=0,tvEpgRequestToken=0,tvInlineRecoveryCount=0;'''
new='''int tvInlineSourceIndex=0,tvInlineFormatAttemptIndex=-1,tvInlineFormatAttemptMask=0,tvInlineFormatMode=0,tvInlineBufferStarts=0,tvSavedScrollY=0,tvEpgRequestToken=0,tvInlineRecoveryCount=0;'''
assert old in s
s=s.replace(old,new,1)

old='''tvPlaybackGeneration++;tvInlineSwitching=false;tvInlineRecoveryCount=0;tvInlineTsFallbackIndex=-1;'''
new='''tvPlaybackGeneration++;tvInlineSwitching=false;tvInlineRecoveryCount=0;tvInlineFormatAttemptIndex=-1;tvInlineFormatAttemptMask=0;tvInlineFormatMode=0;'''
assert old in s
s=s.replace(old,new,1)

old='''androidx.media3.common.MediaItem.Builder itemBuilder=new androidx.media3.common.MediaItem.Builder().setUri(Uri.parse(url));if(tvInlineTsFallbackIndex==index)itemBuilder.setMimeType("video/mp2t");androidx.media3.common.MediaItem item=itemBuilder.build();'''
new='''androidx.media3.common.MediaItem.Builder itemBuilder=new androidx.media3.common.MediaItem.Builder().setUri(Uri.parse(url));if(tvInlineFormatAttemptIndex==index&&tvInlineFormatMode==1)itemBuilder.setMimeType("video/mp2t");else if(tvInlineFormatAttemptIndex==index&&tvInlineFormatMode==2)itemBuilder.setMimeType(androidx.media3.common.MimeTypes.APPLICATION_M3U8);androidx.media3.common.MediaItem item=itemBuilder.build();'''
assert old in s
s=s.replace(old,new,1)

old='''  int current=Math.max(0,Math.min(tvInlineSourceIndex,tvInlineSources.size()-1));String currentUrl=tvInlineSources.get(current);boolean disguisedTs=currentUrl!=null&&currentUrl.toLowerCase(java.util.Locale.US).contains(".m3u8")&&tvInlineTsFallbackIndex!=current;int target;if(disguisedTs){tvInlineTsFallbackIndex=current;target=current;}else{boolean canRetrySame=tvInlineRecoveryCount<2;target=canRetrySame?current:(current+1<tvInlineSources.size()?current+1:current);}tvInlineRecoveryCount++;final int generation=tvPlaybackGeneration;'''
new='''  int current=Math.max(0,Math.min(tvInlineSourceIndex,tvInlineSources.size()-1));String currentUrl=tvInlineSources.get(current);int target=current;boolean changedFormat=false;if(fromError){if(tvInlineFormatAttemptIndex!=current){tvInlineFormatAttemptIndex=current;tvInlineFormatAttemptMask=0;tvInlineFormatMode=0;}String path="";try{path=Uri.parse(currentUrl==null?"":currentUrl).getPath();}catch(Exception ignored){}String low=(path==null?"":path).toLowerCase(java.util.Locale.US);boolean dottedHls=low.endsWith(".m3u8")||low.endsWith(".m3u");boolean bareHls=low.endsWith("/m3u8")||low.endsWith("/m3u")||low.equals("m3u8")||low.equals("m3u");boolean ts=low.endsWith(".ts")||low.endsWith("/ts")||low.equals("ts");boolean knownProgressive=low.endsWith(".mp4")||low.endsWith(".mkv")||low.endsWith(".avi")||low.endsWith(".webm")||low.endsWith(".mov")||low.endsWith(".m4v");int nextMode=0;if(dottedHls){if((tvInlineFormatAttemptMask&1)==0)nextMode=1;}else if(bareHls){if((tvInlineFormatAttemptMask&2)==0)nextMode=2;else if((tvInlineFormatAttemptMask&1)==0)nextMode=1;}else if(ts){if((tvInlineFormatAttemptMask&2)==0)nextMode=2;}else if(!knownProgressive){if((tvInlineFormatAttemptMask&2)==0)nextMode=2;else if((tvInlineFormatAttemptMask&1)==0)nextMode=1;}if(nextMode!=0){tvInlineFormatMode=nextMode;tvInlineFormatAttemptMask|=nextMode==1?1:2;changedFormat=true;}}if(!changedFormat){boolean canRetrySame=!fromError&&tvInlineRecoveryCount<1;target=canRetrySame?current:(current+1<tvInlineSources.size()?current+1:current);}tvInlineRecoveryCount++;final int generation=tvPlaybackGeneration;final int retryTarget=target;'''
assert old in s
s=s.replace(old,new,1)

old='''tvStartInlineSource(target);},fromError?350:500);'''
new='''tvStartInlineSource(retryTarget);},fromError?350:500);'''
assert old in s
s=s.replace(old,new,1)

old='''tvInlinePrepared=false;tvInlineSwitching=false;tvInlineBufferStarts=0;tvInlineRecoveryCount=0;tvInlineBufferingSince=0;'''
new='''tvInlinePrepared=false;tvInlineSwitching=false;tvInlineBufferStarts=0;tvInlineRecoveryCount=0;tvInlineFormatAttemptIndex=-1;tvInlineFormatAttemptMask=0;tvInlineFormatMode=0;tvInlineBufferingSince=0;'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

# Fullscreen / movie / series / live player.
p=Path("work/app/src/main/java/fun/greenplay/app/PlayerActivity.java")
s=p.read_text()

old='''int sourceIndex=0,tsFallbackSource=-1,pendingSeek=0,bufferStarts=0,episodeIndex=-1,displayMode=0,pendingSeekProgress=-1;'''
new='''int sourceIndex=0,formatAttemptSource=-1,formatAttemptMask=0,formatMode=0,pendingSeek=0,bufferStarts=0,episodeIndex=-1,displayMode=0,pendingSeekProgress=-1;'''
assert old in s
s=s.replace(old,new,1)

# Buffering alone is not evidence that a valid HLS stream is actually MPEG-TS.
old='''if(bufferStarts>=2&&!retryAsTs())downgradeQuality();'''
new='''if(bufferStarts>=4&&!live)downgradeQuality();'''
assert old in s
s=s.replace(old,new,1)

old='''@Override public void onPlayerError(PlaybackException error){if(retryAsTs())return;if(sourceIndex+1<sources.size()){downgradeQuality();return;}Toast.makeText(PlayerActivity.this,"Não foi possível reproduzir este conteúdo.",Toast.LENGTH_LONG).show();}'''
new='''@Override public void onPlayerError(PlaybackException error){if(retryAlternateFormat())return;if(sourceIndex+1<sources.size()){downgradeQuality();return;}Toast.makeText(PlayerActivity.this,"Não foi possível reproduzir este conteúdo.",Toast.LENGTH_LONG).show();}'''
assert old in s
s=s.replace(old,new,1)

old='''MediaItem.Builder mb=new MediaItem.Builder().setUri(sourceUri(u));if(tsFallbackSource==idx)mb.setMimeType("video/mp2t");player.setMediaItem(mb.build());'''
new='''MediaItem.Builder mb=new MediaItem.Builder().setUri(sourceUri(u));if(formatAttemptSource==idx&&formatMode==1)mb.setMimeType("video/mp2t");else if(formatAttemptSource==idx&&formatMode==2)mb.setMimeType(androidx.media3.common.MimeTypes.APPLICATION_M3U8);player.setMediaItem(mb.build());'''
assert old in s
s=s.replace(old,new,1)

old='''}catch(Exception e){if(retryAsTs())return;if(sourceIndex+1<sources.size())downgradeQuality();else Toast.makeText(this,"Não foi possível reproduzir este conteúdo.",Toast.LENGTH_LONG).show();}}'''
new='''}catch(Exception e){if(retryAlternateFormat())return;if(sourceIndex+1<sources.size())downgradeQuality();else Toast.makeText(this,"Não foi possível reproduzir este conteúdo.",Toast.LENGTH_LONG).show();}}'''
assert old in s
s=s.replace(old,new,1)

old=''' boolean retryAsTs(){if(switching||sourceIndex<0||sourceIndex>=sources.size()||tsFallbackSource==sourceIndex)return false;String u=sources.get(sourceIndex);if(u==null||!u.toLowerCase(java.util.Locale.US).contains(".m3u8"))return false;tsFallbackSource=sourceIndex;switching=true;prepared=false;bufferStarts=0;final int idx=sourceIndex;final int pos=live?0:safePosition();h.postDelayed(()->{switching=false;startSource(idx,pos);},140);return true;}'''
new=''' boolean retryAlternateFormat(){if(switching||sourceIndex<0||sourceIndex>=sources.size())return false;String u=sources.get(sourceIndex);if(u==null)return false;if(formatAttemptSource!=sourceIndex){formatAttemptSource=sourceIndex;formatAttemptMask=0;formatMode=0;}String path="";try{path=sourceUri(u).getPath();}catch(Exception ignored){}String low=(path==null?"":path).toLowerCase(java.util.Locale.US);boolean dottedHls=low.endsWith(".m3u8")||low.endsWith(".m3u");boolean bareHls=low.endsWith("/m3u8")||low.endsWith("/m3u")||low.equals("m3u8")||low.equals("m3u");boolean ts=low.endsWith(".ts")||low.endsWith("/ts")||low.equals("ts");boolean knownProgressive=low.endsWith(".mp4")||low.endsWith(".mkv")||low.endsWith(".avi")||low.endsWith(".webm")||low.endsWith(".mov")||low.endsWith(".m4v");int nextMode=0;if(dottedHls){if((formatAttemptMask&1)==0)nextMode=1;}else if(bareHls){if((formatAttemptMask&2)==0)nextMode=2;else if((formatAttemptMask&1)==0)nextMode=1;}else if(ts){if((formatAttemptMask&2)==0)nextMode=2;}else if(!knownProgressive){if((formatAttemptMask&2)==0)nextMode=2;else if((formatAttemptMask&1)==0)nextMode=1;}if(nextMode==0)return false;formatMode=nextMode;formatAttemptMask|=nextMode==1?1:2;switching=true;prepared=false;bufferStarts=0;final int idx=sourceIndex;final int pos=live?0:safePosition();h.postDelayed(()->{switching=false;startSource(idx,pos);},180);return true;}'''
assert old in s
s=s.replace(old,new,1)

old='''sourceIndex=0;pendingSeek=0;bufferStarts=0;switching=false;prepared=false;buildSources();'''
new='''sourceIndex=0;formatAttemptSource=-1;formatAttemptMask=0;formatMode=0;pendingSeek=0;bufferStarts=0;switching=false;prepared=false;buildSources();'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)
