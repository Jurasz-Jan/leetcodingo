package pl.leetcodingo.session

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import pl.leetcodingo.data.Answer
import pl.leetcodingo.data.Corpus
import pl.leetcodingo.data.CorpusRepository
import pl.leetcodingo.data.Exercise
import pl.leetcodingo.data.ProgressStore
import pl.leetcodingo.data.Streak

/** Jeden wzorzec na ekranie wyboru: ile ma ćwiczeń i ilu z nich jeszcze nie widziałeś. */
data class Topic(
    val pattern: String,
    val total: Int,
    val unseen: Int,
)

sealed interface UiState {
    data object Loading : UiState

    data class Failed(val message: String) : UiState

    data class Menu(
        val topics: List<Topic>,
        val total: Int,
        val unseen: Int,
        val streak: Streak,
    ) : UiState

    data class Running(
        val exercise: Exercise,
        val position: Int,
        val total: Int,
        val picked: List<Int>,
        val revealed: Boolean,
        val correctSoFar: Int,
        val topic: String?,
    ) : UiState {
        val isCorrect: Boolean get() = exercise.isCorrect(picked)
        val canSubmit: Boolean get() = when (exercise.answer) {
            is Answer.Choice -> picked.size == 1
            is Answer.Ordering -> picked.size == exercise.options.size
        }
    }

    data class Finished(
        val correct: Int,
        val total: Int,
        val topic: String?,
        val streak: Streak,
    ) : UiState
}

class SessionViewModel(app: Application) : AndroidViewModel(app) {

    private val progress = ProgressStore(app)
    private val _state = MutableStateFlow<UiState>(UiState.Loading)
    val state: StateFlow<UiState> = _state.asStateFlow()

    private var corpus: Corpus? = null

    /**
     * Widziane cwiczenia trzymane takze w pamieci.
     *
     * DataStore zapisuje asynchronicznie, wiec odczyt tuz po odpowiedzi moglby jeszcze
     * nie widziec swiezego wpisu. Ta kopia jest zrodlem prawdy przy doborze sesji, a
     * zapis na dysk sluzy juz tylko przetrwaniu miedzy uruchomieniami.
     */
    private var seenCache: MutableSet<String>? = null
    private var queue: List<Exercise> = emptyList()
    private var index = 0
    private var correct = 0
    private var topic: String? = null

    init {
        openMenu()
    }

    /** Ekran wyboru trybu. Liczby biorą się z korpusu i z tego, co już widziałeś. */
    fun openMenu() {
        viewModelScope.launch {
            _state.value = UiState.Loading
            val loaded = load() ?: return@launch
            val seen = seen()

            val topics = loaded.exercises
                .groupBy { it.pattern }
                .map { (pattern, items) ->
                    Topic(
                        pattern = pattern,
                        total = items.size,
                        unseen = items.count { it.id !in seen },
                    )
                }
                .sortedWith(compareByDescending<Topic> { it.unseen }.thenBy { it.pattern })

            _state.value = UiState.Menu(
                topics = topics,
                total = loaded.exercises.size,
                unseen = loaded.exercises.count { it.id !in seen },
                streak = progress.streak(),
            )
        }
    }

    /** Sesja mieszana: dobiera z całego korpusu. */
    fun startMixed() = startSession(null)

    /** Sesja tematyczna: wyłącznie jeden wzorzec. */
    fun startTopic(pattern: String) = startSession(pattern)

    private fun startSession(pattern: String?) {
        viewModelScope.launch {
            _state.value = UiState.Loading
            val loaded = load() ?: return@launch

            val pool = if (pattern == null) {
                loaded.exercises
            } else {
                loaded.exercises.filter { it.pattern == pattern }
            }
            if (pool.isEmpty()) {
                _state.value = UiState.Failed("brak ćwiczeń dla wybranego tematu")
                return@launch
            }

            topic = pattern
            queue = pickSession(pool, seen())
            index = 0
            correct = 0
            emitCurrent(picked = emptyList(), revealed = false)
        }
    }

    private suspend fun seen(): MutableSet<String> {
        seenCache?.let { return it }
        val loaded = progress.seen().toMutableSet()
        seenCache = loaded
        return loaded
    }

    private suspend fun load(): Corpus? {
        val loaded = corpus ?: runCatching {
            withContext(Dispatchers.IO) {
                CorpusRepository(getApplication<Application>()).load()
            }
        }.getOrElse {
            _state.value = UiState.Failed(it.message ?: "nie udało się wczytać korpusu")
            return null
        }
        corpus = loaded
        if (loaded.exercises.isEmpty()) {
            _state.value = UiState.Failed("korpus jest pusty")
            return null
        }
        return loaded
    }

    /** Wybor opcji. Przy `choice` zastepuje poprzednia, przy `ordering` dokłada na koniec. */
    fun pick(option: Int) {
        val running = _state.value as? UiState.Running ?: return
        if (running.revealed) return
        val picked = when (running.exercise.answer) {
            is Answer.Choice -> listOf(option)
            is Answer.Ordering ->
                if (option in running.picked) running.picked - option else running.picked + option
        }
        _state.value = running.copy(picked = picked)
    }

    fun submit() {
        val running = _state.value as? UiState.Running ?: return
        if (running.revealed || !running.canSubmit) return
        if (running.isCorrect) correct++
        _state.value = running.copy(revealed = true, correctSoFar = correct)

        // Zapis w momencie odpowiedzi, a nie na koncu sesji. Przerwanie w polowie jest
        // w tej aplikacji przypadkiem typowym, wiec zapis na koncu gubilby postep
        // przy wiekszosci sesji.
        val answered = running.exercise.id
        viewModelScope.launch {
            seen().add(answered)
            progress.markSeen(listOf(answered))
        }
    }

    fun next() {
        val running = _state.value as? UiState.Running ?: return
        if (!running.revealed) return
        index++
        if (index >= queue.size) {
            // Zapis serii i przejscie na ekran koncowy dzieja sie razem, bo dopiero
            // wynik zapisu mowi, czy ta sesja przedluzyla serie i czy jest co swietowac.
            viewModelScope.launch {
                _state.value = UiState.Finished(
                    correct = correct,
                    total = queue.size,
                    topic = topic,
                    streak = progress.recordFinishedSession(),
                )
            }
        } else {
            emitCurrent(picked = emptyList(), revealed = false)
        }
    }

    /** Powtórka tego samego trybu, w którym właśnie skończyłeś. */
    fun again() = startSession(topic)

    private fun emitCurrent(picked: List<Int>, revealed: Boolean) {
        _state.value = UiState.Running(
            exercise = queue[index],
            position = index + 1,
            total = queue.size,
            picked = picked,
            revealed = revealed,
            correctSoFar = correct,
            topic = topic,
        )
    }

    /**
     * Sesja to budzet czasu, nie liczba zadan: nowe cwiczenia najpierw, reszta losowo.
     */
    private fun pickSession(all: List<Exercise>, seen: Set<String>): List<Exercise> {
        val unseen = all.filter { it.id !in seen }.shuffled()
        val rest = all.filter { it.id in seen }.shuffled()
        val out = mutableListOf<Exercise>()
        var budget = SESSION_SECONDS
        for (exercise in unseen + rest) {
            if (budget <= 0) break
            out += exercise
            budget -= exercise.estSeconds
        }
        return out
    }

    private companion object {
        const val SESSION_SECONDS = 180
    }
}
