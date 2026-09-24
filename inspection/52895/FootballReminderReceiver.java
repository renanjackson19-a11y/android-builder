package fun.greenplay.app;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.Build;
import org.json.JSONArray;
import org.json.JSONObject;

public class FootballReminderReceiver extends BroadcastReceiver {
    static final String CHANNEL_ID = "greenplay_football_reminders";

    @Override public void onReceive(Context context, Intent intent) {
        if (intent == null || !FootballReminderManager.ACTION_CHECK.equals(intent.getAction())) return;
        final PendingResult pending = goAsync();
        final String key = intent.getStringExtra("reminder_key");
        final JSONObject reminder = FootballReminderManager.find(context, key == null ? "" : key);
        if (reminder == null) { pending.finish(); return; }

        Api.PROVIDER = context.getSharedPreferences("gp", 0).getString("provider_id", reminder.optString("provider_id", ""));
        Api.post("football", Api.m("date", reminder.optString("date", "")), new Api.CB() {
            public void ok(JSONObject j) {
                try { handle(context, reminder, j.optJSONArray("result")); }
                finally { pending.finish(); }
            }
            public void err(String e) {
                retry(context, reminder, 2L * 60L * 1000L);
                pending.finish();
            }
        });
    }

    static void handle(Context c, JSONObject r, JSONArray rows) {
        JSONObject game = findGame(r, rows);
        long now = System.currentTimeMillis();
        long original = r.optLong("timestamp", 0) * 1000L;

        if (game != null) {
            long newTs = game.optLong("timestamp", 0) * 1000L;
            if (newTs > 0 && Math.abs(newTs - original) > 30000L) {
                try {
                    r.put("timestamp", game.optLong("timestamp", 0));
                    r.put("date", new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US).format(new java.util.Date(newTs)));
                    FootballReminderManager.update(c, r);
                } catch (Exception ignored) {}
                original = newTs;
            }

            if (game.optBoolean("live", false)) {
                notifyStarted(c, r, game);
                FootballReminderManager.remove(c, r.optString("key", ""), true);
                return;
            }

            String status = game.optString("status", "").toLowerCase(java.util.Locale.ROOT);
            if (status.contains("encerr") || status.contains("cancel") || status.contains("w.o") || status.contains("adiado")) {
                FootballReminderManager.remove(c, r.optString("key", ""), true);
                return;
            }
        }

        if (original > now + 20000L) {
            FootballReminderManager.schedule(c, r, original);
            return;
        }

        if (now - original <= 3L * 60L * 60L * 1000L) retry(c, r, 2L * 60L * 1000L);
        else FootballReminderManager.remove(c, r.optString("key", ""), true);
    }

    static JSONObject findGame(JSONObject r, JSONArray rows) {
        if (rows == null) return null;
        long id = r.optLong("fixture_id", 0);
        String home = r.optString("home", "").trim();
        String away = r.optString("away", "").trim();

        for (int i = 0; i < rows.length(); i++) {
            JSONObject x = rows.optJSONObject(i);
            if (x == null) continue;
            if (id > 0 && x.optLong("id", 0) == id) return x;

            JSONObject h = x.optJSONObject("home");
            JSONObject a = x.optJSONObject("away");
            String hn = h == null ? "" : h.optString("name", "").trim();
            String an = a == null ? "" : a.optString("name", "").trim();

            if (!home.isEmpty() && !away.isEmpty() && home.equalsIgnoreCase(hn) && away.equalsIgnoreCase(an)) return x;
        }
        return null;
    }

    static void retry(Context c, JSONObject r, long delay) {
        long original = r.optLong("timestamp", 0) * 1000L;
        long now = System.currentTimeMillis();

        if (original > 0 && now - original > 3L * 60L * 60L * 1000L) {
            FootballReminderManager.remove(c, r.optString("key", ""), true);
            return;
        }

        FootballReminderManager.schedule(c, r, now + delay);
    }

    static void notifyStarted(Context c, JSONObject r, JSONObject game) {
        if (Build.VERSION.SDK_INT >= 33 && c.checkSelfPermission("android.permission.POST_NOTIFICATIONS") != PackageManager.PERMISSION_GRANTED) return;

        NotificationManager nm = (NotificationManager)c.getSystemService(Context.NOTIFICATION_SERVICE);
        if (nm == null) return;

        if (Build.VERSION.SDK_INT >= 26) {
            NotificationChannel ch = new NotificationChannel(CHANNEL_ID, "Lembretes de jogos", NotificationManager.IMPORTANCE_HIGH);
            ch.setDescription("Avisos quando os jogos marcados começam");
            ch.enableVibration(true);
            nm.createNotificationChannel(ch);
        }

        String home = r.optString("home", "Time 1");
        String away = r.optString("away", "Time 2");
        boolean watch = game != null && game.optBoolean("watch_available", false);

        Intent open = new Intent(c, MainActivity.class);
        open.putExtra("gp_open_football", true);
        open.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);

        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 23) flags |= PendingIntent.FLAG_IMMUTABLE;
        PendingIntent content = PendingIntent.getActivity(c, r.optString("key", "").hashCode(), open, flags);

        Notification.Builder b = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(c, CHANNEL_ID) : new Notification.Builder(c);
        b.setSmallIcon(R.drawable.ic_nav_tv)
         .setColor(Color.rgb(32,224,112))
         .setContentTitle("⚽ O jogo começou!")
         .setContentText(home + " x " + away + (watch ? " • Toque para assistir" : " • Ao vivo agora"))
         .setStyle(new Notification.BigTextStyle().bigText(home + " x " + away + " está ao vivo no GreenPlay. " + (watch ? "Toque para assistir agora." : "Abra o app para acompanhar e localizar a transmissão.")))
         .setAutoCancel(true)
         .setContentIntent(content)
         .setPriority(Notification.PRIORITY_HIGH)
         .setCategory(Notification.CATEGORY_EVENT)
         .setDefaults(Notification.DEFAULT_ALL);

        nm.notify(Math.abs(r.optString("key", "").hashCode()), b.build());
    }
}
