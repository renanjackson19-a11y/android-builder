package fun.greenplay.app;

import android.content.Context;
import com.google.android.gms.cast.CastMediaControlIntent;
import com.google.android.gms.cast.framework.CastOptions;
import com.google.android.gms.cast.framework.OptionsProvider;
import com.google.android.gms.cast.framework.SessionProvider;
import java.util.List;

public class CastOptionsProvider implements OptionsProvider {
 @Override public CastOptions getCastOptions(Context appContext){
  return new CastOptions.Builder()
      .setReceiverApplicationId(CastMediaControlIntent.DEFAULT_MEDIA_RECEIVER_APPLICATION_ID)
      .setShowSystemOutputSwitcherOnCastIconClick(false)
      .build();
 }
 @Override public List<SessionProvider> getAdditionalSessionProviders(Context appContext){ return null; }
}
