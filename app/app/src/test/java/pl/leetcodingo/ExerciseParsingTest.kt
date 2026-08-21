package pl.leetcodingo

import kotlinx.serialization.json.JsonPrimitive
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test
import pl.leetcodingo.data.Answer
import pl.leetcodingo.data.CorpusFile
import pl.leetcodingo.data.corpusJson
import pl.leetcodingo.data.toExerciseOrNull

private const val CORPUS = """
{
  "pattern": {"id": "sliding-window", "name": "Sliding window"},
  "exercises": [
    {
      "id": "sliding-window/min-subarray/cmp-swap-00",
      "pattern": "sliding-window",
      "problem": "min-subarray",
      "type": "find-bug",
      "ui": "choice",
      "difficulty": 3,
      "spec": "Zwraca długość najkrótszego spójnego podciągu o sumie >= target.",
      "prompt": "Który test wykryje błąd?",
      "code": "def solution(nums, target): ...",
      "options": ["a", "b", "c", "d"],
      "answer": 2,
      "explanation": "bo tak",
      "spec_ref": "sumie >= target",
      "est_seconds": 60,
      "source": "generated",
      "tags": ["which-test", "cmp_swap"]
    },
    {
      "id": "sliding-window/min-subarray/order-steps",
      "pattern": "sliding-window",
      "problem": "min-subarray",
      "type": "order-steps",
      "ui": "ordering",
      "difficulty": 2,
      "spec": "spec",
      "prompt": "Ułóż kroki",
      "code": "",
      "options": ["x", "y", "z"],
      "answer": [2, 0, 1],
      "explanation": "kolejność",
      "spec_ref": null,
      "est_seconds": 60,
      "source": "handwritten",
      "tags": ["order-steps"]
    }
  ]
}
"""

class ExerciseParsingTest {

    private val file = corpusJson.decodeFromString<CorpusFile>(CORPUS)

    @Test
    fun `czyta oba ksztalty pola answer`() {
        val choice = file.exercises[0].toExerciseOrNull()
        val ordering = file.exercises[1].toExerciseOrNull()

        assertEquals(Answer.Choice(2), choice?.answer)
        assertEquals(Answer.Ordering(listOf(2, 0, 1)), ordering?.answer)
    }

    @Test
    fun `ocena odpowiedzi jednokrotnego wyboru`() {
        val exercise = file.exercises[0].toExerciseOrNull()!!

        assertTrue(exercise.isCorrect(listOf(2)))
        assertFalse(exercise.isCorrect(listOf(0)))
        assertFalse(exercise.isCorrect(emptyList()))
        assertFalse(exercise.isCorrect(listOf(2, 0)))
    }

    @Test
    fun `ocena ukladania kolejnosci wymaga pelnej permutacji`() {
        val exercise = file.exercises[1].toExerciseOrNull()!!

        assertTrue(exercise.isCorrect(listOf(2, 0, 1)))
        assertFalse(exercise.isCorrect(listOf(0, 1, 2)))
        assertFalse(exercise.isCorrect(listOf(2, 0)))
    }

    @Test
    fun `wpis z odpowiedzia poza zakresem opcji jest odrzucany`() {
        val broken = file.exercises[0].copy(answer = JsonPrimitive(9))

        assertNull(broken.toExerciseOrNull())
    }

    @Test
    fun `wpis bez specyfikacji jest odrzucany`() {
        assertNull(file.exercises[0].copy(spec = "").toExerciseOrNull())
        assertNotNull(file.exercises[0].toExerciseOrNull())
    }
}
