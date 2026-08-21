package pl.leetcodingo.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.intOrNull

/**
 * Kontrakt miedzy generatorem a rendererem. Kazde pole pochodzi z plikow JSON
 * w katalogu `corpus`; aplikacja nie zna zadnej tresci poza tym, co z nich przeczyta.
 */
@Serializable
data class CorpusFile(
    val pattern: PatternMeta,
    val exercises: List<ExerciseDto>,
)

@Serializable
data class PatternMeta(
    val id: String,
    val name: String = id,
    @SerialName("recognition_cues") val recognitionCues: List<String> = emptyList(),
)

@Serializable
data class ExerciseDto(
    val id: String,
    val pattern: String,
    val problem: String,
    val type: String,
    val ui: String,
    val difficulty: Int,
    val spec: String,
    val prompt: String,
    val code: String,
    val options: List<String>,
    val answer: JsonElement,
    val explanation: String,
    @SerialName("spec_ref") val specRef: String? = null,
    @SerialName("est_seconds") val estSeconds: Int,
    val source: String = "generated",
    val tags: List<String> = emptyList(),
)

/**
 * `answer` ma w JSON-ie dwa ksztalty, bo `ui` mowi rendererowi, jak przyjac odpowiedz:
 * indeks jednej opcji albo permutacja wszystkich.
 */
sealed interface Answer {
    data class Choice(val index: Int) : Answer
    data class Ordering(val order: List<Int>) : Answer
}

data class Exercise(
    val id: String,
    val pattern: String,
    val problem: String,
    val type: String,
    val difficulty: Int,
    val spec: String,
    val prompt: String,
    val code: String,
    val options: List<String>,
    val answer: Answer,
    val explanation: String,
    val specRef: String?,
    val estSeconds: Int,
    val tags: List<String>,
) {
    fun isCorrect(picked: List<Int>): Boolean = when (answer) {
        is Answer.Choice -> picked.size == 1 && picked[0] == answer.index
        is Answer.Ordering -> picked == answer.order
    }
}

val corpusJson: Json = Json { ignoreUnknownKeys = true }

/**
 * Zwraca null dla wpisu, ktorego nie da sie zinterpretowac. Build korpusu ma wlasny
 * walidator, wiec to sie nie powinno zdarzyc - ale zle ćwiczenie nie moze wywalic sesji.
 */
fun ExerciseDto.toExerciseOrNull(): Exercise? {
    val parsed = when (ui) {
        "choice" -> (answer as? JsonPrimitive)?.intOrNull
            ?.takeIf { it in options.indices }
            ?.let { Answer.Choice(it) }

        "ordering" -> (answer as? JsonArray)
            ?.mapNotNull { (it as? JsonPrimitive)?.intOrNull }
            ?.takeIf { it.sorted() == options.indices.toList() }
            ?.let { Answer.Ordering(it) }

        else -> null
    } ?: return null

    if (options.size < 2 || spec.isBlank() || explanation.isBlank()) return null

    return Exercise(
        id = id,
        pattern = pattern,
        problem = problem,
        type = type,
        difficulty = difficulty,
        spec = spec,
        prompt = prompt,
        code = code,
        options = options,
        answer = parsed,
        explanation = explanation,
        specRef = specRef,
        estSeconds = estSeconds,
        tags = tags,
    )
}
