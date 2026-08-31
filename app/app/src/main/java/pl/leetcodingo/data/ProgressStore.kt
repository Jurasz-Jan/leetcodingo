package pl.leetcodingo.data

import android.content.Context
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.core.stringSetPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.first
import java.time.LocalDate

private val Context.progressDataStore by preferencesDataStore(name = "progress")

/**
 * Seria dni z ukończoną sesją.
 *
 * `extendedToday` mówi, czy właśnie zaliczona sesja była pierwszą dzisiaj. Tylko wtedy
 * warto świętować: druga sesja tego samego dnia niczego do serii nie dokłada.
 */
data class Streak(
    val days: Int,
    val best: Int,
    val extendedToday: Boolean,
)

/**
 * Minimum potrzebne do tego, zeby kolejna sesja nie byla powtorka poprzedniej,
 * plus seria dni.
 *
 * Wlasciwa mechanika retencji (powtorki rozlozone w czasie) to P1. Seria jest
 * informacja zwrotna, a nie mechanika: ma pokazywac, ze wracasz, a nie zastepowac
 * odstepy miedzy powtorkami.
 */
class ProgressStore(private val context: Context) {

    suspend fun seen(): Set<String> =
        context.progressDataStore.data.first()[SEEN] ?: emptySet()

    suspend fun markSeen(ids: Collection<String>) {
        context.progressDataStore.edit { prefs ->
            prefs[SEEN] = (prefs[SEEN] ?: emptySet()) + ids
        }
    }

    /** Odczyt bez zmiany stanu, na ekran wyboru. */
    suspend fun streak(today: LocalDate = LocalDate.now()): Streak {
        val prefs = context.progressDataStore.data.first()
        val last = prefs[LAST_DAY]?.let(LocalDate::parse)
        val stored = prefs[STREAK] ?: 0
        val best = prefs[BEST_STREAK] ?: 0

        // Seria wygasa dopiero po opuszczeniu całego dnia: wczoraj wciąż się liczy,
        // bo dzisiejsza sesja jeszcze przed nami.
        val alive = last != null && (last == today || last == today.minusDays(1))
        return Streak(
            days = if (alive) stored else 0,
            best = best,
            extendedToday = last == today,
        )
    }

    /**
     * Zapisuje ukończoną sesję i zwraca stan serii po tym zapisie.
     *
     * Dzień liczy się raz: druga i kolejna sesja tego samego dnia zostawiają serię bez
     * zmian i zwracają `extendedToday = false`, żeby nie świętować dwa razy.
     */
    suspend fun recordFinishedSession(today: LocalDate = LocalDate.now()): Streak {
        var result = Streak(days = 0, best = 0, extendedToday = false)

        context.progressDataStore.edit { prefs ->
            val last = prefs[LAST_DAY]?.let(LocalDate::parse)
            val stored = prefs[STREAK] ?: 0
            val best = prefs[BEST_STREAK] ?: 0

            val days = when (last) {
                today -> stored
                today.minusDays(1) -> stored + 1
                else -> 1
            }
            val newBest = maxOf(best, days)

            prefs[LAST_DAY] = today.toString()
            prefs[STREAK] = days
            prefs[BEST_STREAK] = newBest

            result = Streak(days = days, best = newBest, extendedToday = last != today)
        }
        return result
    }

    private companion object {
        val SEEN = stringSetPreferencesKey("seen")
        val LAST_DAY = stringPreferencesKey("last_day")
        val STREAK = intPreferencesKey("streak")
        val BEST_STREAK = intPreferencesKey("best_streak")
    }
}
