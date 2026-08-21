package pl.leetcodingo.data

import android.content.Context
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringSetPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.first

private val Context.progressDataStore by preferencesDataStore(name = "progress")

/**
 * Minimum potrzebne do tego, zeby kolejna sesja nie byla powtorka poprzedniej.
 * Wlasciwa mechanika retencji (powtorki rozlozone w czasie) to P1, nie v1.
 */
class ProgressStore(private val context: Context) {

    suspend fun seen(): Set<String> =
        context.progressDataStore.data.first()[SEEN] ?: emptySet()

    suspend fun markSeen(ids: Collection<String>) {
        context.progressDataStore.edit { prefs ->
            prefs[SEEN] = (prefs[SEEN] ?: emptySet()) + ids
        }
    }

    private companion object {
        val SEEN = stringSetPreferencesKey("seen")
    }
}
