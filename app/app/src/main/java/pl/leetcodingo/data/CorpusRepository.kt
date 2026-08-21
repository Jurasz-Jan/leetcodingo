package pl.leetcodingo.data

import android.content.res.AssetManager

data class Corpus(
    val patterns: List<PatternMeta>,
    val exercises: List<Exercise>,
    val skipped: Int,
)

/**
 * Czyta korpus z assetow. Pliki trafiaja tam zadaniem `copyCorpus` przy kazdym
 * buildzie, wiec przebudowa korpusu nie wymaga zmiany kodu aplikacji.
 */
class CorpusRepository(private val assets: AssetManager) {

    fun load(): Corpus {
        val files = assets.list(ASSET_DIR).orEmpty().filter { it.endsWith(".json") }.sorted()
        val patterns = mutableListOf<PatternMeta>()
        val exercises = mutableListOf<Exercise>()
        var skipped = 0

        for (name in files) {
            val raw = assets.open("$ASSET_DIR/$name").bufferedReader().use { it.readText() }
            val file = corpusJson.decodeFromString<CorpusFile>(raw)
            patterns += file.pattern
            for (dto in file.exercises) {
                val exercise = dto.toExerciseOrNull()
                if (exercise == null) skipped++ else exercises += exercise
            }
        }
        return Corpus(patterns = patterns, exercises = exercises, skipped = skipped)
    }

    private companion object {
        const val ASSET_DIR = "corpus"
    }
}
