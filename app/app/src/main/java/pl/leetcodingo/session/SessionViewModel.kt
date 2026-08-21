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
import pl.leetcodingo.data.Corpus
import pl.leetcodingo.data.CorpusRepository
import pl.leetcodingo.data.Exercise
import pl.leetcodingo.data.ProgressStore

sealed interface UiState {
    data object Loading : UiState

    data class Failed(val message: String) : UiState

    data class Running(
        val exercise: Exercise,
        val position: Int,
        val total: Int,
        val picked: List<Int>,
        val revealed: Boolean,
        val correctSoFar: Int,
    ) : UiState {
        val isCorrect: Boolean get() = exercise.isCorrect(picked)
        val canSubmit: Boolean get() = when (exercise.answer) {
            is pl.leetcodingo.data.Answer.Choice -> picked.size == 1
            is pl.leetcodingo.data.Answer.Ordering -> picked.size == exercise.options.size
        }
    }

    data class Finished(val correct: Int, val total: Int) : UiState
}

class SessionViewModel(app: Application) : AndroidViewModel(app) {

    private val progress = ProgressStore(app)
    private val _state = MutableStateFlow<UiState>(UiState.Loading)
    val state: StateFlow<UiState> = _state.asStateFlow()

    private var corpus: Corpus? = null
    private var queue: List<Exercise> = emptyList()
    private var index = 0
    private var correct = 0

    init {
        start()
    }

    fun start() {
        viewModelScope.launch {
            _state.value = UiState.Loading
            val loaded = corpus ?: runCatching {
                withContext(Dispatchers.IO) {
                    CorpusRepository(getApplication<Application>().assets).load()
                }
            }.getOrElse {
                _state.value = UiState.Failed(it.message ?: "nie udało się wczytać korpusu")
                return@launch
            }
            corpus = loaded

            if (loaded.exercises.isEmpty()) {
                _state.value = UiState.Failed("korpus jest pusty")
                return@launch
            }

            queue = pickSession(loaded.exercises, progress.seen())
            index = 0
            correct = 0
            emitCurrent(picked = emptyList(), revealed = false)
        }
    }

    /** Wybor opcji. Przy `choice` zastepuje poprzednia, przy `ordering` dokłada na koniec. */
    fun pick(option: Int) {
        val running = _state.value as? UiState.Running ?: return
        if (running.revealed) return
        val picked = when (running.exercise.answer) {
            is pl.leetcodingo.data.Answer.Choice -> listOf(option)
            is pl.leetcodingo.data.Answer.Ordering ->
                if (option in running.picked) running.picked - option else running.picked + option
        }
        _state.value = running.copy(picked = picked)
    }

    fun submit() {
        val running = _state.value as? UiState.Running ?: return
        if (running.revealed || !running.canSubmit) return
        if (running.isCorrect) correct++
        _state.value = running.copy(revealed = true, correctSoFar = correct)
    }

    fun next() {
        val running = _state.value as? UiState.Running ?: return
        if (!running.revealed) return
        index++
        if (index >= queue.size) {
            viewModelScope.launch { progress.markSeen(queue.map { it.id }) }
            _state.value = UiState.Finished(correct = correct, total = queue.size)
        } else {
            emitCurrent(picked = emptyList(), revealed = false)
        }
    }

    private fun emitCurrent(picked: List<Int>, revealed: Boolean) {
        _state.value = UiState.Running(
            exercise = queue[index],
            position = index + 1,
            total = queue.size,
            picked = picked,
            revealed = revealed,
            correctSoFar = correct,
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
