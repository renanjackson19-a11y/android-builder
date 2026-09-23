from pathlib import Path

g=Path("work/app/build.gradle")
s=g.read_text()
assert "versionCode 52862" in s
assert "versionName '5.28.62'" in s
s=s.replace("versionCode 52862","versionCode 52863",1).replace("versionName '5.28.62'","versionName '5.28.63'",1)
g.write_text(s)

p=Path("work/app/src/main/java/fun/greenplay/app/MainActivity.java")
s=p.read_text()

old='''int tvInlineSourceIndex=0,tvInlineBufferStarts=0,tvSavedScrollY=0,tvEpgRequestToken=0,tvInlineRecoveryCount=0;'''
new='''int tvInlineSourceIndex=0,tvInlineTsFallbackIndex=-1,tvInlineBufferStarts=0,tvSavedScrollY=0,tvEpgRequestToken=0,tvInlineRecoveryCount=0;'''
assert old in s
s=s.replace(old,new,1)

old='''tvPlaybackGeneration++;tvInlineSwitching=false;tvInlineRecoveryCount=0;'''
new='''tvPlaybackGeneration++;tvInlineSwitching=false;tvInlineRecoveryCount=0;tvInlineTsFallbackIndex=-1;'''
assert old in s
s=s.replace(old,new,1)

old='''androidx.media3.common.MediaItem item=new androidx.media3.common.MediaItem.Builder().setUri(Uri.parse(url)).build();'''
new='''androidx.media3.common.MediaItem.Builder itemBuilder=new androidx.media3.common.MediaItem.Builder().setUri(Uri.parse(url));if(tvInlineTsFallbackIndex==index)itemBuilder.setMimeType("video/mp2t");androidx.media3.common.MediaItem item=itemBuilder.build();'''
assert old in s
s=s.replace(old,new,1)

old='''  int current=Math.max(0,Math.min(tvInlineSourceIndex,tvInlineSources.size()-1));boolean canRetrySame=tvInlineRecoveryCount<2;int target=canRetrySame?current:(current+1<tvInlineSources.size()?current+1:current);tvInlineRecoveryCount++;final int generation=tvPlaybackGeneration;'''
new='''  int current=Math.max(0,Math.min(tvInlineSourceIndex,tvInlineSources.size()-1));String currentUrl=tvInlineSources.get(current);boolean disguisedTs=currentUrl!=null&&currentUrl.toLowerCase(java.util.Locale.US).contains(".m3u8")&&tvInlineTsFallbackIndex!=current;int target;if(disguisedTs){tvInlineTsFallbackIndex=current;target=current;}else{boolean canRetrySame=tvInlineRecoveryCount<2;target=canRetrySame?current:(current+1<tvInlineSources.size()?current+1:current);}tvInlineRecoveryCount++;final int generation=tvPlaybackGeneration;'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

p=Path("work/app/src/main/java/fun/greenplay/app/PlayerActivity.java")
s=p.read_text()

old='''boolean live=false,prepared=false,switching=false,tickerStarted=false,episodeQueue=false,tvMode=false,forcePortrait=false,resumeAfterBackground=false,seekingTouch=false,shortsLandscapeCanvas=false; int sourceIndex=0,pendingSeek=0,bufferStarts=0,episodeIndex=-1,displayMode=0,pendingSeekProgress=-1;'''
new='''boolean live=false,prepared=false,switching=false,tickerStarted=false,episodeQueue=false,tvMode=false,forcePortrait=false,resumeAfterBackground=false,seekingTouch=false,shortsLandscapeCanvas=false; int sourceIndex=0,tsFallbackSource=-1,pendingSeek=0,bufferStarts=0,episodeIndex=-1,displayMode=0,pendingSeekProgress=-1;'''
assert old in s
s=s.replace(old,new,1)

old='''else if(state==Player.STATE_BUFFERING&&prepared&&!switching){long now=SystemClock.elapsedRealtime();bufferStarts=(now-lastBufferAt<30000)?bufferStarts+1:1;lastBufferAt=now;if(bufferStarts>=2)downgradeQuality();}'''
new='''else if(state==Player.STATE_BUFFERING&&prepared&&!switching){long now=SystemClock.elapsedRealtime();bufferStarts=(now-lastBufferAt<30000)?bufferStarts+1:1;lastBufferAt=now;if(bufferStarts>=2&&!retryLiveAsTs())downgradeQuality();}'''
assert old in s
s=s.replace(old,new,1)

old='''@Override public void onPlayerError(PlaybackException error){if(sourceIndex+1<sources.size()){downgradeQuality();return;}Toast.makeText(PlayerActivity.this,"Não foi possível reproduzir este conteúdo.",Toast.LENGTH_LONG).show();}});'''
new='''@Override public void onPlayerError(PlaybackException error){if(retryLiveAsTs())return;if(sourceIndex+1<sources.size()){downgradeQuality();return;}Toast.makeText(PlayerActivity.this,"Não foi possível reproduzir este conteúdo.",Toast.LENGTH_LONG).show();}});'''
assert old in s
s=s.replace(old,new,1)

old=''' void startSource(int idx,int seekMs){if(idx<0||idx>=sources.size()||player==null)return;sourceIndex=idx;pendingSeek=Math.max(0,seekMs);prepared=false;switching=false;String u=sources.get(idx);try{player.stop();player.clearMediaItems();player.setMediaItem(MediaItem.fromUri(sourceUri(u)));if(pendingSeek>0&&!live)player.seekTo(pendingSeek);pendingSeek=0;player.setPlayWhenReady(true);player.prepare();playerView.requestFocus();}catch(Exception e){if(sourceIndex+1<sources.size())downgradeQuality();else Toast.makeText(this,"Não foi possível reproduzir este conteúdo.",Toast.LENGTH_LONG).show();}}'''
new=''' void startSource(int idx,int seekMs){if(idx<0||idx>=sources.size()||player==null)return;sourceIndex=idx;pendingSeek=Math.max(0,seekMs);prepared=false;switching=false;String u=sources.get(idx);try{player.stop();player.clearMediaItems();MediaItem.Builder mb=new MediaItem.Builder().setUri(sourceUri(u));if(live&&tsFallbackSource==idx)mb.setMimeType("video/mp2t");player.setMediaItem(mb.build());if(pendingSeek>0&&!live)player.seekTo(pendingSeek);pendingSeek=0;player.setPlayWhenReady(true);player.prepare();playerView.requestFocus();}catch(Exception e){if(retryLiveAsTs())return;if(sourceIndex+1<sources.size())downgradeQuality();else Toast.makeText(this,"Não foi possível reproduzir este conteúdo.",Toast.LENGTH_LONG).show();}}'''
assert old in s
s=s.replace(old,new,1)

anchor=''' void downgradeQuality(){if(switching||sourceIndex+1>=sources.size())return;switching=true;int pos=live?0:safePosition();sourceIndex++;bufferStarts=0;h.postDelayed(()->startSource(sourceIndex,pos),120);}'''
helper=''' boolean retryLiveAsTs(){if(!live||switching||sourceIndex<0||sourceIndex>=sources.size()||tsFallbackSource==sourceIndex)return false;String u=sources.get(sourceIndex);if(u==null||!u.toLowerCase(java.util.Locale.US).contains(".m3u8"))return false;tsFallbackSource=sourceIndex;switching=true;prepared=false;bufferStarts=0;final int idx=sourceIndex;h.postDelayed(()->{switching=false;startSource(idx,0);},140);return true;}
'''+anchor
assert anchor in s
s=s.replace(anchor,helper,1)

p.write_text(s)
