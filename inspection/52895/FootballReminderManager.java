package fun.greenplay.app;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import org.json.JSONArray;
import org.json.JSONObject;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

final class FootballReminderManager {
    static final String PREF_KEY = "football_reminders_v1";
    static final String ACTION_CHECK = "fun.greenplay.app.FOOTBALL_REMINDER_CHECK";

    private FootballReminderManager() {}

    static String gameKey(JSONObject game) {
        long id = game == null ? 0 : game.optLong("id", 0);
        if (id > 0) return "id:" + id;
        JSONObject h = game == null ? null : game.optJSONObject("home");
        JSONObject a = game == null ? null : game.optJSONObject("away");
        String hn = h == null ? "" : h.optString("name", "").trim();
        String an = a == null ? "" : a.optString("name", "").trim();
        long ts = game == null ? 0 : game.optLong("timestamp", 0);
        return "fallback:" + ts + ":" + hn + ":" + an;
    }

    static boolean isActive(Context c, JSONObject game) {
        String key = gameKey(game);
        JSONArray arr = read(c);
        for (int i = 0; i < arr.length(); i++) {
            JSONObject r = arr.optJSONObject(i);
            if (r != null && key.equals(r.optString("key", ""))) return true;
        }
        return false;
    }

    static boolean toggle(Context c, JSONObject game) {
        String key = gameKey(game);
        if (isActive(c, game)) {
            remove(c, key, true);
            return false;
        }
        JSONObject r = fromGame(c, game);
        if (r == null) return false;
        JSONArray arr = read(c);
        arr.put(r);
        write(c, arr);
        schedule(c, r, Math.max(System.currentTimeMillis() + 3000L, r.optLong("timestamp", 0) * 1000L));
        return true;
    }

    static JSONObject fromGame(Context c, JSONObject game) {
        long ts = game.optLong("timestamp", 0);
        if (ts <= 0) return null;
        JSONObject h = game.optJSONObject("home");
        JSONObject a = game.optJSONObject("away");
        try {
            JSONObject r = new JSONObject();
            r.put("key", gameKey(game));
            r.put("fixture_id", game.optLong("id", 0));
            r.put("timestamp", ts);
            r.put("date", new SimpleDateFormat("yyyy-MM-dd", Locale.US).format(new Date(ts * 1000L)));
            r.put("home", h == null ? "" : h.optString("name", "").trim());
            r.put("away", a == null ? "" : a.optString("name", "").trim());
            r.put("provider_id", c.getSharedPreferences("gp", 0).getString("provider_id", ""));
            return r;
        } catch (Exception e) {
            return null;
        }
    }

    static JSONArray read(Context c) {
        try {
            return new JSONArray(c.getSharedPreferences("gp", 0).getString(PREF_KEY, "[]"));
        } catch (Exception e) {
            return new JSONArray();
        }
    }

    static void write(Context c, JSONArray a) {
        c.getSharedPreferences("gp", 0).edit().putString(PREF_KEY, a == null ? "[]" : a.toString()).apply();
    }

    static JSONObject find(Context c, String key) {
        JSONArray arr = read(c);
        for (int i = 0; i < arr.length(); i++) {
            JSONObject r = arr.optJSONObject(i);
            if (r != null && key.equals(r.optString("key", ""))) return r;
        }
        return null;
    }

    static void update(Context c, JSONObject updated) {
        if (updated == null) return;
        String key = updated.optString("key", "");
        JSONArray arr = read(c), out = new JSONArray();
        boolean done = false;
        for (int i = 0; i < arr.length(); i++) {
            JSONObject r = arr.optJSONObject(i);
            if (r == null) continue;
            if (!done && key.equals(r.optString("key", ""))) {
                out.put(updated);
                done = true;
            } else out.put(r);
        }
        if (!done) out.put(updated);
        write(c, out);
    }

    static void remove(Context c, String key, boolean cancelAlarm) {
        JSONArray arr = read(c), out = new JSONArray();
        for (int i = 0; i < arr.length(); i++) {
            JSONObject r = arr.optJSONObject(i);
            if (r == null || key.equals(r.optString("key", ""))) continue;
            out.put(r);
        }
        write(c, out);
        if (cancelAlarm) cancel(c, key);
    }

    static PendingIntent pending(Context c, String key) {
        Intent i = new Intent(c, FootballReminderReceiver.class);
        i.setAction(ACTION_CHECK);
        i.putExtra("reminder_key", key);
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 23) flags |= PendingIntent.FLAG_IMMUTABLE;
        return PendingIntent.getBroadcast(c, key.hashCode(), i, flags);
    }

    static void schedule(Context c, JSONObject r, long whenMs) {
        if (r == null) return;
        String key = r.optString("key", "");
        if (key.isEmpty()) return;
        AlarmManager am = (AlarmManager)c.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return;
        long trigger = Math.max(System.currentTimeMillis() + 2000L, whenMs);
        try {
            am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, trigger, pending(c, key));
        } catch (Throwable e) {
            try { am.set(AlarmManager.RTC_WAKEUP, trigger, pending(c, key)); } catch (Throwable ignored) {}
        }
    }

    static void cancel(Context c, String key) {
        AlarmManager am = (AlarmManager)c.getSystemService(Context.ALARM_SERVICE);
        if (am != null) try { am.cancel(pending(c, key)); } catch (Throwable ignored) {}
    }

    static void rescheduleAll(Context c) {
        JSONArray arr = read(c);
        long now = System.currentTimeMillis();
        for (int i = 0; i < arr.length(); i++) {
            JSONObject r = arr.optJSONObject(i);
            if (r == null) continue;
            long ts = r.optLong("timestamp", 0) * 1000L;
            if (ts <= 0 || now - ts > 3L * 60L * 60L * 1000L) continue;
            schedule(c, r, ts > now ? ts : now + 5000L);
        }
    }
}
